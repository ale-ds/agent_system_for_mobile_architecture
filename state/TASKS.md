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

## Tarefas da Etapa 1 — Infraestrutura de Continuidade (CONCLUÍDA E APROVADA)

| ID | Tarefa | Agente | Status | Branch / Worktree | Dependência | Critério de Aceitação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TASK-000** | Planejamento Geral e Arquitetura da Solução | Orchestrator | `COMPLETED` | `main` | Nenhuma | Documento aprovado pelo usuário no Passo 1. |
| **TASK-001** | Criação da Topologia de Diretórios e .gitignore | Orchestrator | `COMPLETED` | `main` | TASK-000 | Estrutura física criada e .gitignore configurado. |
| **TASK-002** | Contratos de Continuidade e Regras (`AGENTS.md`) | Tech Lead Agent | `COMPLETED` | `main` | TASK-001 | Regras inegociáveis, boot/shutdown gravados. |
| **TASK-003** | Documentos de Estado e Persistência (`state/`) | Orchestrator | `COMPLETED` | `main` | TASK-002 | `PROJECT_STATE.md`, `ROADMAP.md`, `TASKS.md`, `PROGRESS.md`, `HANDOFF.md`, `SESSION_LOG.md` ativos. |
| **TASK-004** | Elaboração do ADR-0001 (Arquitetura de Continuidade) | Tech Lead Agent | `COMPLETED` | `main` | TASK-003 | Decisão formal gravada em `docs/adr/0001-context-continuity-architecture.md`. |
| **TASK-005** | Configuração de Regras e Skills do Antigravity CLI | Orchestrator | `COMPLETED` | `main` | TASK-003 | Regras em `.agents/rules/` e skills em `.agents/skills/` validadas. |
| **TASK-006** | Teste Experimental de Recuperação e Handoff Inter-Sessão | QA / Git Agent | `COMPLETED` | `main` | TASK-004, TASK-005 | Teste automatizado executado com 14/14 critérios `PASSED` comprovados em log. |
| **TASK-007** | Relatório de Validação e Solicitação de Aprovação da Etapa 1 | Orchestrator | `COMPLETED` | `main` | TASK-006 | Relatório consolidado emitido e aprovado pelo usuário. |

---

## Tarefas da Etapa 2 — Programa de Aprendizado e Plataforma Mobile iOS

| ID | Tarefa | Agente | Status | Branch / Worktree | Dependência | Critério de Aceitação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TASK-101** | Módulo 01: Context Engineering e Context Window Management | Instrutor / Tech Lead | `COMPLETED` | `main` | TASK-007 | Teoria aprofundada explicada em `course/module_01_context_eng/`, Context Manager implementado e testado com 8/8 testes aprovados. |
| **TASK-102** | Módulo 02: Fundamentos de LLMs e Modelos Google | Instrutor / Developer | `TODO` | `main` | TASK-101 | LLMProvider multi-modelo implementado e validado. |
| **TASK-103** | Módulo 03: Engenharia de Prompts Estruturada | Instrutor / Developer | `TODO` | `main` | TASK-102 | Motor de prompts tipados com Pydantic v2. |
| **TASK-104** | Módulo 04: Fundamentos de Agentes e Loop ReAct | Instrutor / Developer | `TODO` | `main` | TASK-103 | ReAct puro implementado sem frameworks pesados. |
| **TASK-105** | Módulos 05 a 07: Ferramentas, MCP e Memória | Instrutor / Developer | `BLOCKED` | `main` | TASK-104 | ToolRegistry, MCP Client/Server e ChromaDB Apple Docs. |
| **TASK-106** | Módulos 08 a 10: Orquestração com LangGraph e Multiagentes | Instrutor / Orchestrator | `BLOCKED` | `main` | TASK-105 | Grafos cíclicos, checkpoints, HITL e orquestração. |
| **TASK-107** | Módulos 11 a 13: Harness Engineering, LangSmith e Evals | Instrutor / QA Agent | `BLOCKED` | `main` | TASK-106 | Middlewares, tracing LangSmith e suíte de Evals. |
| **TASK-108** | Módulos 14 a 16: Git Agent, Worktrees e Paralelismo | Git Agent / Developer | `BLOCKED` | `main` | TASK-107 | Execução concorrente em múltiplos worktrees isolados. |
| **TASK-109** | Módulos 17 e 18: Construção do Aplicativo Financeiro iOS | Multiagente Completo | `BLOCKED` | `main` | TASK-108 | App financeiro iOS completo, compilado e testado via xcodebuild. |
