# ADR-0001: Arquitetura de Continuidade de Contexto e Persistência Desacoplada

* **Status:** APROVADO
* **Data:** 2026-11-12
* **Decisores:** Principal Software Architect, Orchestrator Agent
* **Aprovador:** Usuário / Tech Lead

---

## 1. Contexto e Problema

O desenvolvimento de software de alta criticidade auxiliado por agentes de IA enfrenta o desafio inerente da efemeridade da memória de trabalho dos Modelos de Linguagem de Grande Porte (LLMs):
1. **Limites de Janela de Contexto:** Mesmo modelos com janelas expandidas (1M+ tokens) sofrem degradação de atenção (*needle-in-a-haystack decay*), além de aumento proibitivo de custo e latência quando todo o histórico de conversação é reenviado continuamente.
2. **Volatilidade de Sessão:** O encerramento de um processo, compactação automática de histórico ou troca de modelo elimina o contexto volátil da memória do agente.
3. **Alucinações e Falta de Auditoria:** Agentes que confiam em sua própria "lembrança" conversacional frequentemente inventam tarefas concluídas, arquivos fictícios e testes inexistentes.
4. **Concorrência e Paralelismo:** Múltiplos agentes operando em paralelo não podem compartilhar um único fluxo conversacional sem corromper o estado global.

---

## 2. Decisão Arquitetural

Decidimos estruturar uma **Infraestrutura de Continuidade Desacoplada (Projeto Zero)** fundamentada no próprio repositório Git e no sistema de arquivos local como **Fonte Única da Verdade (Single Source of Truth - SSOT)**.

A arquitetura adota os seguintes pilares:
1. **Desacoplamento entre Runtime e Memória:** A memória de longo prazo e o estado do projeto não residem no agente, mas em arquivos estruturados versionados (`state/PROJECT_STATE.md`, `state/TASKS.md`, `state/PROGRESS.md`, `state/HANDOFF.md`, `sessions/SESSION_LOG.md`).
2. **Protocolo Transacional de Sessão:**
   * **Bootloader Obrigatório:** Nenhuma ação de implementação ocorre antes que o agente execute o protocolo de 10 passos para reconstruir o estado mental a partir do disco.
   * **Shutdown & Checkpoint Obrigatório:** Nenhuma sessão é finalizada sem que evidências reais de testes sejam gravadas e o bastão de handoff seja passado formalmente.
3. **Isolamento de Concorrência via Git Worktree:** Agentes paralelos operam em diretórios de trabalho independentes (`.worktrees/task-<id>/`), escrevendo apenas em arquivos de estado da branch local. Apenas o Orchestrator / Git Agent consolida os arquivos globais sob `state/` na branch principal após validação e merge.
4. **Integração Nativa com Google Antigravity CLI:**
   * Regras perenes em `AGENTS.md` (respeitando o limite de 24 KB / 20k tokens).
   * Regras contextuais em `.agents/rules/*.md`.
   * Habilidades operacionais carregadas sob demanda (*progressive disclosure*) em `.agents/skills/*/SKILL.md`.

---

## 3. Consequências

### Positivas
* **Resiliência a Falhas:** Sessões podem ser destruídas, compactadas ou reiniciadas sem perda de rastreabilidade ou progresso.
* **Auditabilidade Completa:** Todas as decisões, testes e alterações geram diffs no Git e registros no log de sessões.
* **Independência de Fornecedor:** O projeto pode ser operado pelo Google Antigravity CLI, terminais convencionais, IDEs ou qualquer outro agente de IA, pois a lógica de continuidade é agnóstica.
* **Prevenção de Alucinações:** A regra da evidência física impede que agentes declarem funcionalidades prontas sem testes reais no disco.

### Negativas / Mitigações
* **Overhead Operacional:** Cada início de sessão exige alguns segundos para leitura dos arquivos de estado (mitigado por arquivos concisos e leitura seletiva).
* **Risco de Conflitos em Arquivos de Controle:** Se múltiplos agentes escrevessem em `PROJECT_STATE.md` concorrentemente, haveria conflito no Git (mitigado pela regra de que agentes paralelos só escrevem no estado de sua branch local, cabendo ao Orchestrator a consolidação na branch `main`).
