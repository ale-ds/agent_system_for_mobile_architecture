# PROGRESSO PEDAGÓGICO E CURRICULAR (PROGRESS)

Este documento registra o avanço do aprendizado em Engenharia de Sistemas Agênticos, detalhando conceitos dominados, implementações concluídas e competências validadas.

---

## Métricas Gerais

* **Total de Fases Planejadas:** 6 fases (após Etapa 1)
* **Total de Módulos:** 18 módulos
* **Módulos Concluídos:** 1 de 18 (5.55%)
* **Etapa Vigente:** Etapa 2 — Programa de Aprendizado e Plataforma Mobile iOS
* **Fase Vigente:** Fase I — Engenharia de Contexto e Fundamentos Agênticos

---

## Registro de Competências por Módulo

### Etapa 1: Infraestrutura de Continuidade (CONCLUÍDA E APROVADA)
* **Conceitos Dominados:**
  * Context Decay e Saturation em LLMs.
  * Single Source of Truth (SSOT) em repositórios Git.
  * Protocolo de Início de Sessão (Bootloader de Contexto).
  * Checkpointing e Protocolo de Handoff Inter-Sessão.
  * Isolamento de ambientes de trabalho com Git Worktrees.
  * Hierarquia de regras e progressive disclosure do Google Antigravity CLI.
* **Implementações Validadas:**
  * Topologia de diretórios corporativa (`state/`, `sessions/`, `docs/`, `platform/`, `mobile/`).
  * Contratos e protocolos permanentes (`AGENTS.md`).
  * Suíte de teste experimental aprovando os 14 critérios de aceitação.

---

### Etapa 2: Módulos do Curso

| Módulo | Título | Status | Competências Teóricas | Implementação Prática |
| :--- | :--- | :--- | :--- | :--- |
| **M01** | Context Engineering & Context Window | `CONCLUÍDO` | Janela de contexto, auto-atenção $O(N^2)$, diluição de softmax, budgeting e podas | `ContextManager`, `TokenBudget`, `TokenCounter` em `platform/src/context/` com 8/8 testes pytest |
| **M02** | Fundamentos de LLMs & Modelos Google | `PRONTO` | Transformers, Function Calling, Gemini APIs | LLMProvider multi-modelo |
| **M03** | Engenharia de Prompts Estruturada | `BLOQUEADO` | CoT, ReAct, Schemas Pydantic, Metaprompting | Motor de prompts tipado |
| **M04** | Fundamentos de Agentes & ReAct Loop | `BLOQUEADO` | Loop Reason-Act-Observe, parsing | ReAct Agent em Python puro |
| **M05** | Tool Engineering & Sandboxing | `BLOQUEADO` | Contratos de ferramentas, isolamento de shell | ToolRegistry validado |
| **M06** | Model Context Protocol (MCP) | `BLOQUEADO` | Padrão MCP, JSON-RPC, transportes stdio | MCP Client & MCP Server Docs |
| **M07** | Memória & RAG Especializado | `BLOQUEADO` | Embeddings, Chunking, ChromaDB, Apple Docs | RAG Engine para documentação iOS |
| **M08** | LangGraph: Grafos & Estados | `BLOQUEADO` | Grafos cíclicos, Redutores de estado | Primeiro Grafo de Requisitos |
| **M09** | LangGraph Avançado: Checkpoints & HITL | `BLOQUEADO` | Persistência transacional, aprovação humana | Grafo com Human-in-the-Loop |
| **M10** | Sistemas Multiagentes & Handoffs | `BLOQUEADO` | Topologias, Supervisão, Handoffs | Núcleo Multiagente da Plataforma |
| **M11** | Harness Engineering & Contenção | `BLOQUEADO` | Limites operacionais, circuit breaker | Middleware de contenção agêntica |
| **M12** | Observabilidade com LangSmith | `BLOQUEADO` | Tracing distribuído, telemetria, custos | Instrumentação LangSmith |
| **M13** | Evals Automatizados & LLM-as-a-Judge | `BLOQUEADO` | Métricas de corretude, datasets sintéticos | Suíte de Evals com pytest |
| **M14** | Git Agent & Git Worktrees | `BLOQUEADO` | Concorrência, Worktrees, Branch hygiene | GitAgent automatizado |
| **M15** | Governança & Segurança (RBAC) | `BLOQUEADO` | OWASP for LLMs, Prompt Injection, RBAC | Prompt Security Agent |
| **M16** | Orquestração Paralela de Agentes | `BLOQUEADO` | Execução assíncrona, mediação de conflitos | Pipeline multi-worktree concorrente |
| **M17** | SDLC de Engenharia de Software iOS | `BLOQUEADO` | Clean Architecture, SwiftUI, xcodebuild | Agentes integrados ao toolchain iOS |
| **M18** | Construção do Aplicativo Financeiro iOS | `BLOQUEADO` | Ciclo ponta a ponta autônomo e auditado | Aplicativo iOS compilado e testado |
