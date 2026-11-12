---
name: session-lifecycle
description: Procedimento operacional padronizado para execucao do Bootloader de inicio de sessao, checkpointing intermediario e protocolo de encerramento com handoff.
---

# Procedimento Operacional: Ciclo de Vida de Sessões (Session Lifecycle)

Esta Skill define as etapas e contratos para execução do Bootloader de Contexto, salvamento de Checkpoint e Encerramento de Sessão com Handoff estruturado.

---

## 1. Procedimento de Bootloader (Início de Sessão)

Quando uma nova sessão for iniciada ou o agente for instanciado para continuar o projeto:

1. **Leitura de Contratos:** Ler `AGENTS.md` para carregar diretrizes inegociáveis.
2. **Leitura do Estado Consolidado:** Inspecionar `state/PROJECT_STATE.md`.
3. **Leitura do Último Handoff:** Inspecionar `state/HANDOFF.md` para identificar o ponto de parada anterior.
4. **Leitura da Fila de Tarefas:** Inspecionar `state/TASKS.md` para identificar qual tarefa está `IN_PROGRESS` ou pronta para início.
5. **Checagem do Git:**
   * Executar `git status`.
   * Verificar a branch ativa e a integridade da árvore de trabalho.
6. **Verificação de Consistência:**
   * Comparar as informações de `HANDOFF.md` com os arquivos presentes em disco.
   * Se houver discrepância física, reportar imediatamente ao usuário antes de alterar código.
7. **Emissão do Resumo de Boot:**
   * Apresentar ao usuário o diagnóstico: Etapa atual, tarefa ativa, branch e próxima ação imediata.

---

## 2. Procedimento de Encerramento e Checkpoint

Ao concluir uma tarefa ou preparar o encerramento da sessão:

1. **Execução de Validação Física:**
   * Rodar a suíte de testes relevante (ex.: testes unitários ou scripts de validação).
   * Confirmar que não há quebras no build ou linters.
2. **Registro de Evidências:**
   * Salvar saídas de teste em `sessions/logs/` ou registrar no log da sessão.
3. **Atualização de Estado:**
   * Atualizar `state/TASKS.md` com status da tarefa, data e notas.
   * Atualizar `state/PROJECT_STATE.md` com o novo panorama consolidado.
   * Atualizar `state/PROGRESS.md` se competências ou módulos foram validados.
4. **Auditoria de Sessão:**
   * Adicionar entrada em `sessions/SESSION_LOG.md` registrando o resumo do que foi realizado.
5. **Geração do Bastão de Handoff:**
   * Atualizar `state/HANDOFF.md` indicando explicitamente:
     * O que foi finalizado nesta sessão.
     * O que está pendente para a próxima.
     * A próxima ação exata autorizada.
6. **Commit no Repositório:**
   * Executar `git add` e commit com mensagem convencional descritiva.
