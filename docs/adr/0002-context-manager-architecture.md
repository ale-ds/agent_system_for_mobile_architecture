# ADR-0002: Arquitetura do Gerenciador de Contexto e Orçamento de Tokens

* **Status:** APROVADO
* **Data:** 2026-11-12
* **Decisores:** Principal Software Architect, Tech Lead Agent
* **Aprovador:** Usuário / Tech Lead

---

## 1. Contexto e Problema

Modelos de Linguagem de Grande Porte (LLMs) operam sob limites estritos de janela de contexto. Mesmo quando a janela é massiva (1M a 2M tokens), ocorrem três patologias graves quando o contexto é preenchido sem critério:
1. **Degradação de Atenção (*Needle-in-a-Haystack*):** A capacidade do modelo de recuperar e correlacionar instruções críticas decai à medida que o espaço de atenção é preenchido por tokens irrelevantes.
2. **Custo e Latência:** A atenção Transformer possui custo computacional e latência crescentes com o volume de tokens ($O(N^2)$ no self-attention padrão e custos lineares por token processado).
3. **Estouro de Janela e Falhas Não Determinísticas:** Se uma ferramenta ou arquivo grande for inserido sem controle, a chamada à API do LLM falha por estouro do limite máximo de contexto.

---

## 2. Decisão Arquitetural

Decidimos projetar e implementar um componente de controle determinístico denominado `ContextManager` em `platform/src/context/`:

1. **Partição Estrita do Orçamento (`TokenBudget`):**
   * A janela total é particionada em: (1) Reserva de saída (`output_reservation`), (2) Margem de segurança para reasoning e buffers de sistema (`safety_margin`), e (3) Orçamento líquido disponível para o contexto de entrada (`available_for_context`).
2. **Fatias Atômicas de Contexto (`ContextSlice`):**
   * Cada pedaço de texto entregue ao modelo é classificado por categoria (`ContextCategory`) e prioridade (`ContextPriority` de 0 a 5).
3. **Inviolabilidade das Regras Mandatórias:**
   * Fatias classificadas como `MANDATORY` (ex.: `AGENTS.md`, contratos de segurança) têm garantia matemática de inclusão. Se o conjunto obrigatório exceder a janela líquida, uma exceção explícita (`ContextOverflowError`) é disparada antes de chamar o modelo, impedindo execuções cegas.
4. **Alocação Gulosa por Prioridade com Truncamento Controlado:**
   * Fatias eletivas são alocadas em ordem decrescente de prioridade. Fatias marcadas como truncáveis (`is_truncatable=True`) podem ser aproveitadas parcialmente se houver margem residual, recebendo marcadores formais de truncamento.
5. **Auditoria de Montagem (`ContextAssemblyResult`):**
   * A montagem retorna métricas exatas de tokens, percentual de ocupação, lista de fatias incluídas, fatias truncadas e fatias descartadas por falta de espaço.

---

## 3. Consequências

### Positivas
* **Previsibilidade Operacional:** Zero chamadas com estouro acidental de janela.
* **Preservação de Instruções Críticas:** As regras de governança e contratos nunca são descartadas.
* **Transparência e Observabilidade:** O sistema sabe exatamente quais documentos foram descartados ou truncados em cada turno.

### Negativas / Mitigações
* **Perda de Contexto Eletivo:** Informações de prioridade baixa (documentação acessória, históricos distantes) podem ser descartadas quando a tarefa exigir muitos tokens de especificação técnica (mitigado no Módulo 07 através de RAG seletivo).
