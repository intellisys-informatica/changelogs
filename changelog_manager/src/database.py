"""
Módulo de conexão com banco de dados SQL Server
"""
import pyodbc
from config import config


class Database:
    """Classe para gerenciar conexões com SQL Server"""

    def __init__(self):
        """Inicializa a classe de conexão"""
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Estabelece conexão com o banco de dados SQL Server

        Raises:
            Exception: Se houver erro na conexão
        """
        try:
            connection_string = config.get_connection_string()
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            print(f"Conectado ao banco de dados: {config.db_database}")
        except pyodbc.Error as e:
            raise Exception(f"Erro ao conectar ao banco de dados: {e}")

    def disconnect(self):
        """Fecha a conexão com o banco de dados"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Conexão com banco de dados fechada")

    def execute_query(self, query):
        """
        Executa uma query SELECT e retorna os resultados

        Args:
            query (str): Query SQL a ser executada

        Returns:
            list: Lista de dicionários com os resultados

        Raises:
            Exception: Se houver erro na execução da query
        """
        if not self.connection:
            raise Exception("Conexão não estabelecida. Execute connect() primeiro.")

        try:
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            results = []

            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))

            print(f"Query executada com sucesso. {len(results)} registro(s) retornado(s).")
            return results

        except pyodbc.Error as e:
            raise Exception(f"Erro ao executar query: {e}")

    def execute_insert(self, query, params):
        """
        Executa um INSERT no banco de dados

        Args:
            query (str): Query INSERT a ser executada
            params (tuple): Parâmetros para a query

        Raises:
            Exception: Se houver erro na execução
        """
        if not self.connection:
            raise Exception("Conexão não estabelecida. Execute connect() primeiro.")

        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print(f"INSERT executado com sucesso. {self.cursor.rowcount} linha(s) afetada(s).")

        except pyodbc.Error as e:
            self.connection.rollback()
            raise Exception(f"Erro ao executar INSERT: {e}")

    def check_task_documented(self, task_id):
        """
        Verifica se tarefa já está na tabela de documentadas

        Args:
            task_id (str): ID da tarefa

        Returns:
            bool: True se documentada, False caso contrário
        """
        table_name = config.db_table_documentadas

        query = f"""
            SELECT COUNT(*) as Total
            FROM {table_name}
            WHERE NumeroTarefa = ?
        """

        try:
            self.cursor.execute(query, (str(task_id),))
            result = self.cursor.fetchone()
            return result[0] > 0
        except Exception as e:
            print(f"AVISO: Erro ao verificar tarefa documentada {task_id}: {e}")
            return False

    def register_documented_task(self, numero_tarefa, arquivo_md):
        """
        Registra uma tarefa como documentada na tabela de controle

        Args:
            numero_tarefa (str): Número da tarefa documentada
            arquivo_md (str): Nome do arquivo .md onde foi documentada

        Raises:
            Exception: Se houver erro ao registrar
        """
        table_name = config.db_table_documentadas
        query = f"""
            INSERT INTO {table_name} (NumeroTarefa, ArquivoMD, DataExportacao)
            VALUES (?, ?, GETDATE())
        """

        try:
            self.execute_insert(query, (numero_tarefa, arquivo_md))
        except Exception as e:
            print(f"AVISO: Não foi possível registrar tarefa {numero_tarefa}: {e}")

    def __enter__(self):
        """Suporte para context manager (with statement)"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fecha conexão automaticamente ao sair do context manager"""
        self.disconnect()
