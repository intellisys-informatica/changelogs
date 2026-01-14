-- ============================================================================
-- Consulta de Tarefa Individual por ID
-- ============================================================================
-- Busca uma tarefa específica por seu ID para documentação
--
-- IMPORTANTE: Mantenha as seguintes colunas no SELECT:
--   - Sistema       (nome do sistema/projeto)
--   - Resumo        (descrição resumida da alteração)
--   - Detalhes      (descrição completa)
--   - NumeroTarefa  (ID da tarefa para controle)
--
-- A tag {tarefaId} será substituída automaticamente pelo ID informado
-- na linha de comando via parâmetro --tarefa-id
-- ============================================================================

SELECT
    case when CHARINDEX('-', t.TrfNome) > 0 then SUBSTRING(t.TrfNome,1,CHARINDEX('-', t.TrfNome)-1) else t.TrfNome end as Sistema,
		case when CHARINDEX('-', t.TrfNome) > 0 then SUBSTRING(t.TrfNome,CHARINDEX('-', t.TrfNome)+1, LEN(t.TrfNome)) else t.TrfNome end as Resumo,
		t.TrfObservacao2 AS Detalhes,
    t.Tarefaid AS NumeroTarefa
FROM
    TSK_Tarefa t
    LEFT JOIN TSK_TarefasDocumentadas td ON (t.Tarefaid = td.NumeroTarefa)
WHERE
    t.Tarefaid = {tarefaId}
    AND td.NumeroTarefa IS NULL
