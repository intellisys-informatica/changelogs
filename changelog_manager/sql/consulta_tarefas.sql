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

select case when SUBSTRING(p.PrjNome,1,CHARINDEX('-', p.PrjNome)) = 'ICRM3 -' then 'icrmweb' else p.PrjNome end as Sistema,
	SUBSTRING(t.TrfNome,CHARINDEX('-', t.TrfNome)+1, LEN(t.TrfNome)) as Resumo,
	t.TrfObservacao2 as Detalhes,
	t.Tarefaid as NumeroTarefa
from TSK_Tarefa t left join tsk_tarefasdocumentadas td on (t.Tarefaid = td.NumeroTarefa) join TSK_Ciclo c on ( t.CicloId = c.CicloId) join TSK_Projeto p on (c.ProjetoId = p.ProjetoId)
where td.NumeroTarefa is null and t.CicloId = {cicloCod} and (t.TrfFim is not null or t.trffeito = 1)
