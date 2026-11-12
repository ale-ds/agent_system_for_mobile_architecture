# MARCOS HISTÓRICOS E REGISTRO DE EVIDÊNCIAS (MILESTONES)

Este documento registra os marcos consolidados do projeto, acompanhados de evidências físicas e verificáveis no repositório.

---

## Marcos da Etapa 1 — Infraestrutura de Continuidade (CONCLUÍDA)

### MARCO 1.0 — Aprovação do Planejamento Geral (Passo 1)
* **Data de Conclusão:** 2026-11-12
* **Responsável:** Orchestrator Agent
* **Aprovador Humano:** Usuário (Confirmação explícita no chat)
* **Evidências:** Apresentação integral dos 12 tópicos arquiteturais e pedagógicos.
* **Status:** `APROVADO`

---

### MARCO 1.1 — Topologia de Diretórios e Contratos Fundamentais
* **Data de Conclusão:** 2026-11-12
* **Responsável:** Orchestrator & Tech Lead Agent
* **Arquivos Produzidos e Validados:**
  * Topologia criada: `state/`, `sessions/`, `docs/`, `.agents/`, `platform/`, `mobile/`, `.worktrees/`.
  * `.gitignore` configurado com preservação de `.worktrees/.gitkeep`.
  * `AGENTS.md`, `PROJECT_STATE.md`, `ROADMAP.md`, `TASKS.md`, `PROGRESS.md`, `HANDOFF.md`.
  * Decisão registrada: `docs/adr/0001-context-continuity-architecture.md`.
  * Regras e skills do Antigravity CLI registradas.
* **Status:** `CONCLUÍDO E VALIDADO`

---

### MARCO 1.2 — Validação Experimental da Continuidade (14 Critérios)
* **Data de Conclusão:** 2026-11-12
* **Responsável:** QA Agent & Git Agent
* **Aprovador Humano:** Usuário (Autorização explícita: "podemos seguir para a etapa 2")
* **Evidências:** `sessions/logs/validation_evidence.log`, 14/14 critérios `PASSED` comprovados em log e commit `effc2c1`.
* **Status:** `APROVADO FORMALMENTE`

---

## Marcos da Etapa 2 — Programa de Aprendizado e Plataforma Mobile iOS

### MARCO 2.1 — Módulo 01: Context Engineering e Gestão da Janela de Contexto
* **Data de Conclusão:** 2026-11-12
* **Responsável:** Instrutor Técnico / Tech Lead Agent
* **Arquivos Produzidos e Validados:**
  * Material didático: `course/module_01_context_eng/README.md`.
  * Código de produção: `platform/src/context/` (`types.py`, `token_counter.py`, `context_manager.py`).
  * Arquitetura de decisão: `docs/adr/0002-context-manager-architecture.md`.
  * Testes unitários automatizados: `platform/tests/test_context_manager.py`.
* **Evidências de Teste:**
  * 8 testes unitários executados via pytest com 100% de aprovação.
  * Preservação inviolável de fatias `MANDATORY`, alocação por prioridade, truncamento controlado e prevenção de overflow validados.
* **Status:** `CONCLUÍDO E VALIDADO (AGUARDANDO APROVAÇÃO PARA MÓDULO 02)`
