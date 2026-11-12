# Plataforma Agêntica Empresarial para Desenvolvimento Mobile iOS

Repositório da plataforma agêntica corporativa para engenharia de software de aplicações móveis iOS nativas e ambiente de aprendizado contínuo.

---

## Estrutura do Repositório

* `AGENTS.md`: Contratos permanentes, regras invioláveis, protocolos de bootloader e encerramento.
* `.agents/`: Customizações do Google Antigravity CLI (regras hierárquicas e skills operacionais).
* `state/`: Estado dinâmico do projeto, controle de tarefas, roadmap, checkpoints e handoffs.
* `sessions/`: Registro histórico e auditável de todas as sessões de trabalho e execuções.
* `docs/`: Artefatos de engenharia (ADRs, PRDs, especificações técnicas e runbooks).
* `course/`: Material didático, tutoriais aprofundados e laboratórios de engenharia agêntica.
* `platform/`: Código-fonte da plataforma agêntica (Python, LangGraph, MCP, Evals).
* `mobile/`: Código-fonte do aplicativo iOS gerado (Swift, SwiftUI, Clean Architecture).
* `.worktrees/`: Diretório de isolamento para execução concorrente de agentes via Git Worktree.

---

## Protocolo de Continuidade e Governança

Para assegurar a integridade do projeto independentemente de limites de contexto de LLMs ou reinicializações de sessão:
1. Toda sessão executa o **Bootloader de Contexto** (descrito em `AGENTS.md`) antes de qualquer implementação.
2. Nenhuma alteração é declarada pronta sem validação física e registro de evidências.
3. Toda sessão é finalizada com atualização de `state/PROJECT_STATE.md`, `state/TASKS.md`, `sessions/SESSION_LOG.md` e geração de `state/HANDOFF.md`.
