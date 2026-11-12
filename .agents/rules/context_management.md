---
trigger: always_on
description: Diretrizes de Context Engineering, carregamento progressivo e prevencao de saturacao de contexto.
---

# Diretrizes de Context Engineering e Gestão de Contexto

1. **Carregamento Progressivo (Progressive Loading):**
   * Não leia pastas inteiras ou grandes volumes de documentação no início de uma tarefa.
   * Consulte primeiro os índices (`state/PROJECT_STATE.md`, `state/TASKS.md`, `state/HANDOFF.md`).
   * Leia arquivos de especificação (`docs/specs/`, `docs/adr/`) e código sob demanda específica da tarefa ativa.

2. **Limites de Tamanho e Orçamento:**
   * Mantenha arquivos de regras e instruções concisos (máximo de 24 KB por arquivo para conformidade com Antigravity CLI).
   * Evite duplicar informações entre arquivos de estado. Cada arquivo possui uma responsabilidade delimitada:
     * `PROJECT_STATE.md`: Visão consolidada em tempo real.
     * `ROADMAP.md`: Macroplanejamento temporal.
     * `TASKS.md`: Backlog operacional atômico.
     * `PROGRESS.md`: Competências pedagógicas.
     * `HANDOFF.md`: Passagem de bastão pontual.
     * `SESSION_LOG.md`: Trilha cronológica de auditoria.

3. **Compactação de Sessão:**
   * Caso a sessão se aproxime do limite de tokens ou o usuário utilize `/compact`, certifique-se de que o estado já esteja persistido em disco antes que a compactação ocorra.
