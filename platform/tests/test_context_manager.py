"""Testes unitários automatizados para o subsistema de Context Engineering."""

import pytest
from context.types import (
    ContextCategory,
    ContextPriority,
    ContextSlice,
    TokenBudget,
)
from context.token_counter import TokenCounter
from context.context_manager import ContextManager, ContextOverflowError


def test_token_budget_validation():
    """Valida as restrições e cálculos do TokenBudget."""
    budget = TokenBudget(total_window=10_000, output_reservation=1_000, safety_margin=500)
    assert budget.available_for_context == 8_500

    with pytest.raises(ValueError, match="total_window deve ser maior que zero"):
        TokenBudget(total_window=0)

    with pytest.raises(ValueError, match="As reservas excedem"):
        TokenBudget(total_window=1_000, output_reservation=800, safety_margin=300)


def test_token_counter_counting():
    """Valida a precisão da contagem aproximada de tokens."""
    counter = TokenCounter()
    assert counter.count("") == 0
    assert counter.count("Olá mundo!") > 0

    code_snippet = "func calculateBalance(expenses: [Double]) -> Double { return expenses.reduce(0, +) }"
    tokens = counter.count(code_snippet)
    assert tokens > 10


def test_token_counter_truncation():
    """Valida o truncamento controlado respeitando limites de tokens."""
    counter = TokenCounter()
    long_text = "\n".join([f"Linha de log número {i} com informações detalhadas de execução." for i in range(100)])
    max_tokens = 50

    truncated = counter.truncate_to_tokens(long_text, max_tokens=max_tokens)
    assert counter.count(truncated) <= max_tokens + 5  # margem segura para o marcador
    assert "CONTEÚDO TRUNCADO" in truncated


def test_mandatory_slices_are_always_preserved():
    """Garante que fatias com prioridade MANDATORY nunca sejam descartadas."""
    # Orçamento curto para forçar descarte de eletivas
    budget = TokenBudget(total_window=500, output_reservation=100, safety_margin=50)
    manager = ContextManager(budget=budget)

    mandatory_slice = ContextSlice(
        slice_id="agents_core_rules",
        category=ContextCategory.PERMANENT_CONTRACT,
        priority=ContextPriority.MANDATORY,
        content="Regras permanentes e contratos inegociáveis de governança.",
    )
    low_priority_slice = ContextSlice(
        slice_id="verbose_debug_logs",
        category=ContextCategory.SCRATCHPAD,
        priority=ContextPriority.LOW,
        content="Log longo " * 150,  # Ultrapassa o orçamento
    )

    manager.register_slice(mandatory_slice)
    manager.register_slice(low_priority_slice)

    result = manager.assemble()
    included_ids = [s.slice_id for s in result.included_slices]
    dropped_ids = [s.slice_id for s in result.dropped_slices]

    assert "agents_core_rules" in included_ids
    assert "verbose_debug_logs" in dropped_ids
    assert "agents_core_rules" in result.assembled_text


def test_priority_ordering_selection():
    """Valida que fatias de maior prioridade são alocadas antes das de menor prioridade."""
    # Orçamento ajustado para permitir apenas s1 (HIGH) e s2 (MEDIUM), descartando s3 (LOW)
    budget = TokenBudget(total_window=550, output_reservation=100, safety_margin=50)  # Disponível = 400
    manager = ContextManager(budget=budget)

    high_slice = ContextSlice(
        slice_id="task_prd",
        category=ContextCategory.TASK_SPECIFICATION,
        priority=ContextPriority.HIGH,
        content="Especificação técnica detalhada do requisito do aplicativo financeiro iOS. " * 5,  # 175 tokens
    )
    medium_slice = ContextSlice(
        slice_id="chat_history",
        category=ContextCategory.CONVERSATION_HISTORY,
        priority=ContextPriority.MEDIUM,
        content="Mensagens anteriores do desenvolvedor com o arquiteto. " * 5,  # 130 tokens
    )
    low_slice = ContextSlice(
        slice_id="reference_manual",
        category=ContextCategory.REFERENCE_DOCUMENTATION,
        priority=ContextPriority.LOW,
        content="Manual de estilo Swift da Apple com dezenas de exemplos de tipagem. " * 15,  # 525 tokens
    )

    manager.register_slice(low_slice)
    manager.register_slice(high_slice)
    manager.register_slice(medium_slice)

    result = manager.assemble()
    included_ids = [s.slice_id for s in result.included_slices]
    dropped_ids = [s.slice_id for s in result.dropped_slices]

    # HIGH e MEDIUM cabem no orçamento de 400 (175 + 130 = 305 <= 400); LOW (525) estoura o restante (95) e é descartado
    assert "task_prd" in included_ids
    assert "chat_history" in included_ids
    assert "reference_manual" in dropped_ids


def test_truncatable_slice_partial_inclusion():
    """Valida que uma fatia truncável é aproveitada parcialmente quando não cabe inteira."""
    budget = TokenBudget(total_window=300, output_reservation=50, safety_margin=50)
    manager = ContextManager(budget=budget)

    critical_slice = ContextSlice(
        slice_id="active_state",
        category=ContextCategory.PROJECT_STATE,
        priority=ContextPriority.CRITICAL,
        content="Estado ativo: Fase I, Módulo 01 em execução. " * 3,
        is_truncatable=False,
    )
    truncatable_doc = ContextSlice(
        slice_id="apple_doc_swiftui",
        category=ContextCategory.REFERENCE_DOCUMENTATION,
        priority=ContextPriority.HIGH,
        content="SwiftUI Documentação oficial extensa: " + ("View protocol and state management details. " * 40),
        is_truncatable=True,
    )

    manager.register_slice(critical_slice)
    manager.register_slice(truncatable_doc)

    result = manager.assemble()
    included_ids = [s.slice_id for s in result.included_slices]
    truncated_ids = [s.slice_id for s in result.truncated_slices]

    assert "active_state" in included_ids
    assert "apple_doc_swiftui" in included_ids
    assert "apple_doc_swiftui" in truncated_ids
    assert "CONTEÚDO TRUNCADO" in result.assembled_text


def test_mandatory_overflow_raises_error():
    """Garante que ContextOverflowError seja lançado se fatias obrigatórias estourarem a janela."""
    budget = TokenBudget(total_window=200, output_reservation=50, safety_margin=50)  # Disponível = 100
    manager = ContextManager(budget=budget)

    massive_mandatory = ContextSlice(
        slice_id="inviolable_contracts",
        category=ContextCategory.PERMANENT_CONTRACT,
        priority=ContextPriority.MANDATORY,
        content="Texto de contrato mandatório gigantesco que consome muitos tokens. " * 50,
    )
    manager.register_slice(massive_mandatory)

    with pytest.raises(ContextOverflowError, match="Fatias obrigatórias .* excedem o orçamento"):
        manager.assemble()


def test_slice_removal_and_clear():
    """Valida a remoção pontual e a limpeza geral do catálogo de fatias."""
    manager = ContextManager()
    slice_item = ContextSlice(
        slice_id="temp_slice",
        category=ContextCategory.SCRATCHPAD,
        priority=ContextPriority.EPHEMERAL,
        content="Conteúdo temporário",
    )
    manager.register_slice(slice_item)
    assert manager.remove_slice("temp_slice") is True
    assert manager.remove_slice("temp_slice") is False

    manager.register_slice(slice_item)
    manager.clear()
    result = manager.assemble()
    assert result.total_tokens == 0
    assert len(result.included_slices) == 0
