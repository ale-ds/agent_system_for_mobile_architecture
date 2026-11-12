"""Gerenciador central de montagem, priorização e poda de contexto."""

from typing import Optional
from .types import (
    ContextAssemblyResult,
    ContextPriority,
    ContextSlice,
    TokenBudget,
)
from .token_counter import TokenCounter


class ContextOverflowError(Exception):
    """Exceção levantada quando fatias mandatórias ultrapassam o orçamento de contexto."""
    pass


class ContextManager:
    """Gerenciador determinístico de janela de contexto para agentes de IA."""

    def __init__(self, budget: Optional[TokenBudget] = None, token_counter: Optional[TokenCounter] = None):
        """
        Inicializa o ContextManager.
        :param budget: Configuração de orçamento da janela de contexto.
        :param token_counter: Instância do calculador de tokens.
        """
        self.budget = budget or TokenBudget()
        self.counter = token_counter or TokenCounter()
        self._slices: dict[str, ContextSlice] = {}

    def register_slice(self, slice_item: ContextSlice) -> None:
        """
        Registra ou atualiza uma fatia de contexto.
        :param slice_item: Fragmento de contexto a ser adicionado ao catálogo.
        """
        # Calcula os tokens da fatia antes do armazenamento
        slice_item.token_count = self.counter.count(slice_item.content)
        self._slices[slice_item.slice_id] = slice_item

    def remove_slice(self, slice_id: str) -> bool:
        """
        Remove uma fatia de contexto previamente registrada.
        :param slice_id: Identificador da fatia.
        :return: True se a fatia existia e foi removida, False caso contrário.
        """
        return self._slices.pop(slice_id, None) is not None

    def clear(self) -> None:
        """Limpa todas as fatias registradas no gerenciador."""
        self._slices.clear()

    def assemble(self) -> ContextAssemblyResult:
        """
        Compila o contexto determinístico respeitando estritamente o TokenBudget.
        Garante a preservação de fatias MANDATORY e aloca fatias subsequentes por prioridade.
        :return: ContextAssemblyResult contendo texto final e métricas de alocação.
        """
        available_budget = self.budget.available_for_context

        # Separação entre fatias mandatórias e eletivas
        mandatory_slices: list[ContextSlice] = []
        elective_slices: list[ContextSlice] = []

        for item in self._slices.values():
            if item.priority == ContextPriority.MANDATORY:
                mandatory_slices.append(item)
            else:
                elective_slices.append(item)

        # Ordena fatias eletivas pela prioridade (decrescente)
        elective_slices.sort(key=lambda s: s.priority, reverse=True)

        # 1. Aloca fatias mandatórias
        allocated_tokens = 0
        included: list[ContextSlice] = []
        truncated: list[ContextSlice] = []
        dropped: list[ContextSlice] = []

        for mand in mandatory_slices:
            if allocated_tokens + mand.token_count > available_budget:
                raise ContextOverflowError(
                    f"Fatias obrigatórias (MANDATORY) excedem o orçamento de contexto disponível: "
                    f"requerido={allocated_tokens + mand.token_count}, disponível={available_budget}."
                )
            included.append(mand)
            allocated_tokens += mand.token_count

        # 2. Aloca fatias eletivas por prioridade
        for item in elective_slices:
            remaining_budget = available_budget - allocated_tokens
            if remaining_budget <= 0:
                dropped.append(item)
                continue

            if item.token_count <= remaining_budget:
                included.append(item)
                allocated_tokens += item.token_count
            elif item.is_truncatable and remaining_budget >= 50:
                # Fatias truncáveis podem ser aproveitadas parcialmente se houver margem mínima
                truncated_content = self.counter.truncate_to_tokens(item.content, remaining_budget)
                truncated_tokens = self.counter.count(truncated_content)

                # Cria uma cópia truncada da fatia
                truncated_slice = ContextSlice(
                    slice_id=item.slice_id,
                    category=item.category,
                    priority=item.priority,
                    content=truncated_content,
                    is_truncatable=True,
                    metadata={**item.metadata, "original_token_count": item.token_count},
                    token_count=truncated_tokens,
                )
                included.append(truncated_slice)
                truncated.append(truncated_slice)
                allocated_tokens += truncated_tokens
            else:
                dropped.append(item)

        # 3. Montagem do texto compilado
        assembled_blocks: list[str] = []
        for slice_item in included:
            header = f"--- [BLOCO: {slice_item.category.value.upper()} | ID: {slice_item.slice_id}] ---"
            block = f"{header}\n{slice_item.content.strip()}\n"
            assembled_blocks.append(block)

        final_text = "\n".join(assembled_blocks).strip()
        final_total_tokens = self.counter.count(final_text)

        return ContextAssemblyResult(
            assembled_text=final_text,
            total_tokens=final_total_tokens,
            budget=self.budget,
            included_slices=included,
            dropped_slices=dropped,
            truncated_slices=truncated,
        )
