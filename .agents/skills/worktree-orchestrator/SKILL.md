---
name: worktree-orchestrator
description: Procedimento operacional para provisionamento, isolamento, execucao concorrente e limpeza de Git Worktrees em tarefas de agentes.
---

# Procedimento Operacional: Orquestração de Git Worktrees

Esta Skill define o ciclo de vida e os contratos para utilização de Git Worktrees no isolamento de tarefas concorrentes executadas por agentes especializados.

---

## 1. Provisionamento de Git Worktree

Quando uma tarefa exigir isolamento de workspace (ex.: implementação de feature paralela pelo Developer Agent enquanto QA cria testes):

1. **Criação do Worktree e Branch:**
   ```bash
   git worktree add .worktrees/task-<id>-<slug> -b feat/<id>-<slug>
   ```
2. **Registro de Alocação:**
   * Atualizar `state/TASKS.md` informando a branch `feat/<id>-<slug>` e o caminho `.worktrees/task-<id>-<slug>`.
3. **Isolamento de Estado:**
   * Dentro do worktree, o agente deve trabalhar exclusivamente no diretório alocado.
   * Modificações de estado da tarefa devem ser gravadas em `.worktrees/task-<id>-<slug>/TASK_STATE.md`.
   * **O agente não deve alterar arquivos em `state/` na branch principal.**

---

## 2. Validação e Integração (Merge)

Ao concluir a tarefa no worktree:

1. **Validação Local:**
   * Executar os testes automatizados dentro do diretório do worktree.
2. **Commit Local:**
   * Criar commits convencionais com as alterações implementadas.
3. **Solicitação ao Git Agent:**
   * O Git Agent verifica se a branch principal possui novos commits.
   * Executa rebase ou merge fast-forward se aprovado pelo Orchestrator.
4. **Consolidação de Estado Global:**
   * O Orchestrator Agent (no workspace principal) consolida `state/TASKS.md`, `state/PROJECT_STATE.md` e `sessions/SESSION_LOG.md`.

---

## 3. Desprovisionamento e Limpeza

1. **Remoção do Worktree:**
   ```bash
   git worktree remove .worktrees/task-<id>-<slug>
   ```
2. **Limpeza de Metadados Git:**
   ```bash
   git worktree prune
   ```
3. **Verificação de Integridade:**
   * Executar `git worktree list` para confirmar que apenas o workspace principal permanece ativo.
