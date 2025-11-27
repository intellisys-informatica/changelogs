"""
Módulo para executar queries SQL a partir de arquivos
"""
from pathlib import Path


class QueryExecutor:
    """Classe para carregar e executar queries SQL de arquivos"""

    def __init__(self, sql_dir=None):
        """
        Inicializa o executor de queries

        Args:
            sql_dir (str, optional): Diretório onde estão os arquivos SQL.
                                    Se None, usa o diretório padrão ../sql/
        """
        if sql_dir:
            self.sql_dir = Path(sql_dir)
        else:
            # Diretório padrão: ../sql/ relativo ao arquivo atual
            self.sql_dir = Path(__file__).parent.parent / 'sql'

    def load_sql_file(self, filename):
        """
        Carrega conteúdo de um arquivo SQL

        Args:
            filename (str): Nome do arquivo SQL (ex: 'consulta_tarefas.sql')

        Returns:
            str: Conteúdo do arquivo SQL

        Raises:
            FileNotFoundError: Se o arquivo não existir
        """
        sql_path = self.sql_dir / filename

        if not sql_path.exists():
            raise FileNotFoundError(
                f"Arquivo SQL não encontrado: {sql_path}\n"
                f"Certifique-se de criar o arquivo no diretório: {self.sql_dir}"
            )

        with open(sql_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        print(f"Arquivo SQL carregado: {filename}")
        return sql_content

    def replace_parameters(self, sql_content, parameters):
        """
        Substitui tags de parâmetros no SQL

        Args:
            sql_content (str): Conteúdo SQL com tags
            parameters (dict): Dicionário com parâmetros para substituir
                              Ex: {'cicloCod': '124'}

        Returns:
            str: SQL com parâmetros substituídos

        Example:
            >>> sql = "SELECT * FROM Tarefas WHERE Ciclo = {cicloCod}"
            >>> params = {'cicloCod': '124'}
            >>> result = replace_parameters(sql, params)
            >>> print(result)
            "SELECT * FROM Tarefas WHERE Ciclo = 124"
        """
        result = sql_content

        for key, value in parameters.items():
            tag = f"{{{key}}}"
            if tag in result:
                result = result.replace(tag, str(value))
                print(f"Parâmetro substituído: {tag} -> {value}")
            else:
                print(f"AVISO: Tag {tag} não encontrada no SQL")

        return result

    def execute_sql_file(self, database, filename, parameters=None):
        """
        Carrega e executa um arquivo SQL

        Args:
            database (Database): Instância da classe Database conectada
            filename (str): Nome do arquivo SQL
            parameters (dict, optional): Parâmetros para substituir no SQL

        Returns:
            list: Resultados da query (lista de dicionários)

        Raises:
            Exception: Se houver erro ao carregar ou executar o SQL
        """
        # Carrega o arquivo SQL
        sql_content = self.load_sql_file(filename)

        # Substitui parâmetros se fornecidos
        if parameters:
            sql_content = self.replace_parameters(sql_content, parameters)

        # Executa a query
        print("Executando query SQL...")
        results = database.execute_query(sql_content)

        return results
