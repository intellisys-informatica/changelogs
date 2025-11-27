-- ============================================================================
-- Criação da Tabela de Controle - TSK_TarefasDocumentadas
-- ============================================================================
-- Esta tabela é OPCIONAL e serve para rastrear quais tarefas já foram
-- documentadas em arquivos .md, evitando duplicação.
--
-- Execute este script no seu banco de dados SQL Server antes de usar
-- a aplicação pela primeira vez (se desejar usar esse recurso).
-- ============================================================================

-- Verifica se a tabela já existe antes de criar
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'TSK_TarefasDocumentadas')
BEGIN
    CREATE TABLE TSK_TarefasDocumentadas (
        ID INT IDENTITY(1,1) PRIMARY KEY,
        NumeroTarefa VARCHAR(50) NOT NULL,
        ArquivoMD VARCHAR(200) NOT NULL,
        DataExportacao DATETIME NOT NULL DEFAULT GETDATE(),

        -- Constraint para evitar duplicação de tarefas
        CONSTRAINT UQ_TSK_TarefasDocumentadas_NumeroTarefa
            UNIQUE (NumeroTarefa)
    );

    PRINT 'Tabela TSK_TarefasDocumentadas criada com sucesso!';
END
ELSE
BEGIN
    PRINT 'Tabela TSK_TarefasDocumentadas já existe.';
END
GO

-- Adiciona índices para melhor performance
IF NOT EXISTS (SELECT * FROM sys.indexes
               WHERE name = 'IX_TSK_TarefasDocumentadas_DataExportacao')
BEGIN
    CREATE INDEX IX_TSK_TarefasDocumentadas_DataExportacao
        ON TSK_TarefasDocumentadas(DataExportacao DESC);

    PRINT 'Índice IX_TSK_TarefasDocumentadas_DataExportacao criado!';
END
GO

-- ============================================================================
-- QUERIES ÚTEIS PARA CONSULTA
-- ============================================================================

-- Ver todas as tarefas documentadas
-- SELECT * FROM TSK_TarefasDocumentadas ORDER BY DataExportacao DESC;

-- Ver tarefas documentadas em um arquivo específico
-- SELECT * FROM TSK_TarefasDocumentadas
-- WHERE ArquivoMD LIKE '%09.91.47.20%';

-- Ver tarefas documentadas hoje
-- SELECT * FROM TSK_TarefasDocumentadas
-- WHERE CAST(DataExportacao AS DATE) = CAST(GETDATE() AS DATE);

-- Contar tarefas por arquivo
-- SELECT ArquivoMD, COUNT(*) as Total
-- FROM TSK_TarefasDocumentadas
-- GROUP BY ArquivoMD
-- ORDER BY Total DESC;

-- Verificar se uma tarefa específica já foi documentada
-- SELECT * FROM TSK_TarefasDocumentadas WHERE NumeroTarefa = '12345';

-- ============================================================================
-- MANUTENÇÃO
-- ============================================================================

-- Limpar registros antigos (mais de 1 ano)
-- DELETE FROM TSK_TarefasDocumentadas
-- WHERE DataExportacao < DATEADD(YEAR, -1, GETDATE());

-- Remover uma tarefa específica (para re-documentar)
-- DELETE FROM TSK_TarefasDocumentadas WHERE NumeroTarefa = '12345';

-- ============================================================================
