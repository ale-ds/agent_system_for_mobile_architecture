"""Subsistema de Engenharia e Gerenciamento de Contexto."""

from .types import (
    ContextCategory,
    ContextPriority,
    ContextSlice,
    TokenBudget,
    ContextAssemblyResult,
)
from .token_counter import TokenCounter
from .context_manager import ContextManager

__all__ = [
    "ContextCategory",
    "ContextPriority",
    "ContextSlice",
    "TokenBudget",
    "ContextAssemblyResult",
    "TokenCounter",
    "ContextManager",
]
