-- ============================================================================
-- TEMPLATE SQL - Consulta de Tarefas para Documentação
-- ============================================================================
-- Este é um arquivo de exemplo. Você deve modificá-lo de acordo com a
-- estrutura real do seu banco de dados.
--
-- IMPORTANTE: Mantenha as seguintes colunas no SELECT:
--   - Sistema    (nome do sistema/projeto)
--   - Resumo     (descrição resumida da alteração)
--   - Detalhes   (descrição completa)
--   - NumeroTarefa (opcional, mas recomendado para controle)
--
-- A tag {cicloCod} será substituída automaticamente pelo número do ciclo
-- informado na linha de comando.
-- ============================================================================

select
		case when CHARINDEX('-', t.TrfNome) > 0 then SUBSTRING(t.TrfNome,1,CHARINDEX('-', t.TrfNome)-1) else t.TrfNome end as Sistema,
		case when CHARINDEX('-', t.TrfNome) > 0 then SUBSTRING(t.TrfNome,CHARINDEX('-', t.TrfNome)+1, LEN(t.TrfNome)) else t.TrfNome end as Resumo,
		t.TrfObservacao2 as Detalhes,
		t.Tarefaid as NumeroTarefa
from
		TSK_Tarefa t
		left join tsk_tarefasdocumentadas td on (t.Tarefaid = td.NumeroTarefa)
where
		td.NumeroTarefa is null
		and t.CicloId = {cicloCod}
		and (t.TrfFim is not null or t.trffeito = 1)
