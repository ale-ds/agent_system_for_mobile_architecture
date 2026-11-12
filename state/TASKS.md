# MATRIZ DE TAREFAS E DEPENDÊNCIAS (TASKS BACKLOG)

Este documento registra todas as tarefas atômicas do projeto, seus estados de ciclo de vida, agentes atribuídos, branches e critérios de aceitação.

---

## Legenda de Status
* `TODO`: Planejada, aguardando dependências ou autorização.
* `IN_PROGRESS`: Em desenvolvimento ativo pelo agente designado.
* `IN_REVIEW`: Concluída tecnicamente, aguardando testes de aceitação ou aprovação.
* `COMPLETED`: Validada com evidências físicas no repositório.
* `BLOCKED`: Impedida por fator externo ou falha prévia.

---

## Tarefas da Etapa 1 — Infraestrutura de Continuidade

| ID | Tarefa | Agente | Status | Branch / Worktree | Dependência | Critério de Aceitação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TASK-000** | Planejamento Geral e Arquitetura da Solução | Orchestrator | `COMPLETED` | `main` | Nenhuma | Documento aprovado pelo usuário no Passo 1. |
| **TASK-001** | Criação da Topologia de Diretórios e .gitignore | Orchestrator | `COMPLETED` | `main` | TASK-000 | Estrutura física de diretórios criada e .gitignore configurado. |
| **TASK-002** | Elaboração dos Contratos de Continuidade e Regras (`AGENTS.md`) | Tech Lead Agent | `COMPLETED` | `main` | TASK-001 | Regras inegociáveis, protocolos de boot/shutdown e governança gravados. |
| **TASK-003** | Criação dos Documentos de Estado e Persistência (`state/` e `sessions/`) | Orchestrator | `COMPLETED` | `main` | TASK-002 | `PROJECT_STATE.md`, `ROADMAP.md`, `TASKS.md`, `PROGRESS.md`, `HANDOFF.md`, `SESSION_LOG.md` ativos. |
| **TASK-004** | Elaboração do ADR-0001 (Arquitetura de Continuidade) | Tech Lead Agent | `COMPLETED` | `main` | TASK-003 | Registro formal da decisão arquitetural em `docs/adr/0001-context-continuity-architecture.md`. |
| **TASK-005** | Configuração das Regras e Skills do Antigravity CLI | Orchestrator | `COMPLETED` | `main` | TASK-003 | Regras em `.agents/rules/` e skills em `.agents/skills/` validadas. |
| **TASK-006** | Teste Experimental de Recuperação e Handoff Inter-Sessão | QA / Git Agent | `COMPLETED` | `main` | TASK-004, TASK-005 | Teste automatizado executado com 14/14 critérios `PASSED` comprovados em log. |
| **TASK-007** | Relatório de Validação e Solicitação de Aprovação da Etapa 1 | Orchestrator | `COMPLETED` | `main` | TASK-006 | Relatório consolidado emitido para o usuário com evidências dos 14 critérios. |

---

## Tarefas da Etapa 2 — Curso e Plataforma (Bloqueadas até aprovação da Etapa 1)

| ID | Tarefa | Agente | Status | Branch / Worktree | Dependência |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TASK-101** | Módulo 01: Context Engineering e Context Window Management | Instrutor / Tech Lead | `BLOCKED` | `main` | Aprovação Formal da Etapa 1 |
| **TASK-102** | Módulo 02: Fundamentos de LLMs e Modelos Google | Instrutor / Developer | `BLOCKED` | `main` | TASK-101 |
| **TASK-103** | Módulo 03: Engenharia de Prompts Estruturada | Instrutor / Developer | `BLOCKED` | `main` | TASK-102 |
| **TASK-104** | Módulo 04: Fundamentos de Agentes e Loop ReAct | Instrutor / Developer | `BLOCKED` | `main` | TASK-103 |
| **TASK-105** | Módulos 05 a 07: Ferramentas, MCP e Memória | Instrutor / Developer | `BLOCKED` | `main` | TASK-104 |
| **TASK-106** | Módulos 08 a 10: Orquestração com LangGraph e Multiagentes | Instrutor / Orchestrator | `BLOCKED` | `main` | TASK-105 |
| **TASK-107** | Módulos 11 a 13: Harness Engineering, LangSmith e Evals | Instrutor / QA Agent | `BLOCKED` | `main` | TASK-106 |
| **TASK-108** | Módulos 14 a 16: Git Agent, Worktrees e Paralelismo | Git Agent / Developer | `BLOCKED` | `main` | TASK-107 |
| **TASK-109** | Módulos 17 e 18: Construção do Aplicativo Financeiro iOS | Multiagente Completo | `BLOCKED` | `main` | TASK-108 |
