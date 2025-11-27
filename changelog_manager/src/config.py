"""
Módulo de configuração - Carrega variáveis de ambiente do arquivo .env
"""
import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Classe para gerenciar configurações da aplicação"""

    def __init__(self):
        """Inicializa e carrega as configurações do .env"""
        # Encontra o diretório raiz do projeto
        self.base_dir = Path(__file__).parent.parent
        self.env_path = self.base_dir / '.env'

        # Carrega variáveis do .env
        load_dotenv(self.env_path)

        # Configurações do banco de dados
        self.db_server = os.getenv('DB_SERVER')
        self.db_database = os.getenv('DB_DATABASE')
        self.db_username = os.getenv('DB_USERNAME')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_driver = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')
        self.db_table_documentadas = os.getenv('DB_TABLE_DOCUMENTADAS', 'TSK_TarefasDocumentadas')

    def validate(self):
        """
        Valida se todas as configurações obrigatórias estão presentes

        Raises:
            ValueError: Se alguma configuração obrigatória estiver faltando
        """
        required_fields = {
            'DB_SERVER': self.db_server,
            'DB_DATABASE': self.db_database,
            'DB_USERNAME': self.db_username,
            'DB_PASSWORD': self.db_password,
        }

        missing = [key for key, value in required_fields.items() if not value]

        if missing:
            raise ValueError(
                f"Configurações obrigatórias faltando no arquivo .env: {', '.join(missing)}\n"
                f"Por favor, copie o arquivo .env.example para .env e preencha os valores."
            )

    def get_connection_string(self):
        """
        Retorna a string de conexão para o SQL Server

        Returns:
            str: String de conexão ODBC
        """
        return (
            f"DRIVER={{{self.db_driver}}};"
            f"SERVER={self.db_server};"
            f"DATABASE={self.db_database};"
            f"UID={self.db_username};"
            f"PWD={self.db_password};"
        )


# Instância global de configuração
config = Config()
