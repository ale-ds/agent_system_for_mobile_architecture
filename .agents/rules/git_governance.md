---
trigger: always_on
description: Regras de governanca do Git, protecao de branches e padronizacao de commits e worktrees.
---

# Regras de Governança Git e Git Worktree

1. **Proteção da Branch Principal (`main`):**
   * Nenhum agente deve realizar commits com modificações de implementação diretamente na branch `main` sem validação de testes.
   * Modificações de código de produto devem ser desenvolvidas em branches de feature (`feat/<task-id>-<slug>`) ou correção (`fix/<task-id>-<slug>`).
   * Apenas o Orchestrator Agent e o Git Agent têm permissão para atualizar os arquivos globais de controle em `state/` na branch `main`.

2. **Padrão de Mensagens de Commit (Conventional Commits):**
   * Todo commit deve seguir o formato: `<tipo>(<escopo>): <descrição sucinta em imperativo>`.
   * Tipos válidos: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`, `perf`.
   * Exemplos:
     * `docs(continuity): implementar contratos em AGENTS.md e estado do projeto`
     * `feat(git-agent): criar automacao para provisionamento de worktrees`

3. **Governança de Git Worktrees:**
   * Worktrees efêmeros devem ser provisionados exclusivamente no diretório `.worktrees/task-<id>/`.
   * Cada worktree deve estar estritamente associado a uma única tarefa e branch.
   * Ao finalizar a tarefa e realizar o merge, o worktree correspondente deve ser desprovisionado com `git worktree remove`.

4. **Operações Proibidas:**
   * É estritamente proibido o uso de `git push --force`, `git reset --hard` na branch `main` ou qualquer comando destrutivo sem consentimento humano explícito.
