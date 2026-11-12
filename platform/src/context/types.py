"""Definições de tipos e modelos de dados para o subsistema de Context Engineering."""

from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
from typing import Any


class ContextPriority(IntEnum):
    """Prioridade de alocação de fatias de contexto na janela do modelo."""
    EPHEMERAL = 0   # Informações descartáveis, logs auxiliares
    LOW = 1         # Documentação de apoio, histórico distante
    MEDIUM = 2      # Histórico conversacional recente, outputs de ferramentas
    HIGH = 3        # Especificação da tarefa atual, handoff ativo, erros recentes
    CRITICAL = 4    # Estado imediato do projeto, instruções de execução
    MANDATORY = 5   # Contratos permanentes (AGENTS.md), regras de segurança


class ContextCategory(StrEnum):
    """Categorias conceituais de fragmentos de contexto."""
    PERMANENT_CONTRACT = "permanent_contract"
    SYSTEM_INSTRUCTION = "system_instruction"
    PROJECT_STATE = "project_state"
    TASK_SPECIFICATION = "task_specification"
    CONVERSATION_HISTORY = "conversation_history"
    TOOL_RESULT = "tool_result"
    REFERENCE_DOCUMENTATION = "reference_documentation"
    SCRATCHPAD = "scratchpad"


@dataclass(frozen=True)
class TokenBudget:
    """Orçamento e partição da janela de contexto do LLM."""
    total_window: int = 128_000
    output_reservation: int = 4_096
    safety_margin: int = 2_048

    def __post_init__(self):
        if self.total_window <= 0:
            raise ValueError("total_window deve ser maior que zero.")
        if self.output_reservation < 0 or self.safety_margin < 0:
            raise ValueError("Reservas de tokens não podem ser negativas.")
        if (self.output_reservation + self.safety_margin) >= self.total_window:
            raise ValueError("As reservas excedem o tamanho total da janela de contexto.")

    @property
    def available_for_context(self) -> int:
        """Quantidade líquida de tokens reservada para o prompt e contexto de entrada."""
        return self.total_window - self.output_reservation - self.safety_margin


@dataclass
class ContextSlice:
    """Representa uma fatia atômica de conteúdo a ser injetada no contexto do modelo."""
    slice_id: str
    category: ContextCategory
    priority: ContextPriority
    content: str
    is_truncatable: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
    token_count: int = 0

    def __post_init__(self):
        if not self.slice_id:
            raise ValueError("slice_id não pode ser vazio.")


@dataclass
class ContextAssemblyResult:
    """Resultado da montagem determinística do contexto compilado para o modelo."""
    assembled_text: str
    total_tokens: int
    budget: TokenBudget
    included_slices: list[ContextSlice] = field(default_factory=list)
    dropped_slices: list[ContextSlice] = field(default_factory=list)
    truncated_slices: list[ContextSlice] = field(default_factory=list)

    @property
    def utilization_percentage(self) -> float:
        """Percentual de utilização do orçamento disponível de contexto."""
        if self.budget.available_for_context == 0:
            return 0.0
        return round((self.total_tokens / self.budget.available_for_context) * 100, 2)
