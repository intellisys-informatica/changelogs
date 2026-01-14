"""
Módulo para gerenciamento de tarefas individuais
Responsável por buscar e validar tarefas específicas por ID
"""
import sys
from pathlib import Path


class TaskManager:
    """Gerencia busca e validação de tarefas individuais"""

    def __init__(self, database):
        """
        Inicializa o gerenciador de tarefas

        Args:
            database: Instância da classe Database conectada
        """
        self.db = database
        self.sql_dir = Path(__file__).parent.parent / 'sql'

    def get_task_by_id(self, task_id):
        """
        Busca tarefa específica por ID

        Args:
            task_id (str): ID da tarefa

        Returns:
            list: Lista com dados da tarefa (vazia se não encontrada)
        """
        sql_file = self.sql_dir / 'consulta_tarefa_individual.sql'

        if not sql_file.exists():
            raise FileNotFoundError(
                f"Arquivo SQL não encontrado: {sql_file}\n"
                "Certifique-se de que 'consulta_tarefa_individual.sql' existe no diretório sql/"
            )

        # Lê o arquivo SQL
        with open(sql_file, 'r', encoding='utf-8') as f:
            query = f.read()

        # Substitui o parâmetro {tarefaId}
        query = query.replace('{tarefaId}', str(task_id))

        # Executa a query
        results = self.db.execute_query(query)

        if not results:
            print(f"AVISO: Tarefa {task_id} não encontrada ou já foi documentada",
                  file=sys.stderr)

        return results

    def is_task_documented(self, task_id):
        """
        Verifica se tarefa já foi documentada

        Args:
            task_id (str): ID da tarefa

        Returns:
            bool: True se já documentada, False caso contrário
        """
        return self.db.check_task_documented(task_id)

    def validate_task_data(self, task_data):
        """
        Valida se os dados da tarefa estão completos

        Args:
            task_data (dict): Dados da tarefa

        Returns:
            tuple: (bool, str) - (valido, mensagem_erro)
        """
        if not task_data:
            return False, "Dados da tarefa estão vazios"

        # Valida campo Sistema
        if not task_data.get('Sistema'):
            return False, "Tarefa sem sistema identificado. Verifique o formato do nome da tarefa."

        # Valida campo Resumo
        if not task_data.get('Resumo'):
            return False, "Tarefa sem resumo. Verifique o formato do nome da tarefa."

        # Detalhes é opcional, mas recomendado
        if not task_data.get('Detalhes'):
            print("AVISO: Tarefa sem detalhes na coluna TrfObservacao2",
                  file=sys.stderr)

        return True, ""

    def validate_task(self, task_id):
        """
        Valida se tarefa pode ser documentada (wrapper completo)

        Args:
            task_id (str): ID da tarefa

        Returns:
            tuple: (bool, str, dict) - (valido, mensagem_erro, dados_tarefa)
        """
        # Busca tarefa
        results = self.get_task_by_id(task_id)

        if not results:
            return False, f"Tarefa {task_id} não encontrada ou já foi documentada", None

        task_data = results[0]

        # Valida dados
        is_valid, error_msg = self.validate_task_data(task_data)

        if not is_valid:
            return False, error_msg, None

        return True, "", task_data
