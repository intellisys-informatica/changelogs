"""
Módulo para gerar arquivo JSON estruturado a partir dos resultados do banco
"""
import json
import sys
from pathlib import Path


class JsonGenerator:
    """Classe para gerar JSON estruturado para processamento pelo Claude"""

    def __init__(self, output_dir=None):
        """
        Inicializa o gerador de JSON

        Args:
            output_dir (str, optional): Diretório de saída.
                                       Se None, usa o diretório raiz do projeto
        """
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            # Diretório padrão: raiz do projeto
            self.output_dir = Path(__file__).parent.parent

    def generate_json(self, versao, data_results, modo='ciclo', output_filename=None):
        """
        Gera JSON estruturado (retorna dados, opcionalmente salva arquivo)

        Args:
            versao (str): Versão do changelog (ex: "09.91.47.20")
            data_results (list): Lista de dicionários com dados do banco
            modo (str): Modo de operação ('ciclo' ou 'tarefa')
            output_filename (str, optional): Nome do arquivo de saída.
                                            Se None, não salva arquivo (apenas retorna dados)

        Returns:
            dict: Estrutura JSON gerada

        Raises:
            ValueError: Se os dados não tiverem os campos necessários

        Expected data_results format:
            [
                {
                    'Sistema': 'iCRM4',
                    'Resumo': 'Nova funcionalidade X',
                    'Detalhes': 'Descrição completa...',
                    'NumeroTarefa': '12345',
                    ... outros campos ...
                },
                ...
            ]
        """
        # Valida campos necessários
        required_fields = ['Sistema', 'Resumo', 'Detalhes']

        novidades = []
        for idx, record in enumerate(data_results):
            # Verifica se os campos obrigatórios existem
            missing_fields = [field for field in required_fields if field not in record]
            if missing_fields:
                print(
                    f"AVISO: Registro {idx + 1} não possui os campos: {', '.join(missing_fields)}. "
                    f"Ignorando registro."
                )
                continue

            novidade = {
                'sistema': record['Sistema'],
                'resumo': record['Resumo'],
                'detalhes': record['Detalhes']
            }

            # Adiciona campos opcionais se existirem
            if 'NumeroTarefa' in record:
                novidade['numeroTarefa'] = record['NumeroTarefa']

            novidades.append(novidade)

        # Estrutura final do JSON
        output_data = {
            'versao': versao,
            'modo': modo,
            'novidades': novidades
        }

        # Salva o arquivo JSON apenas se output_filename for fornecido
        if output_filename:
            output_path = self.output_dir / output_filename
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

            print(f"\nJSON gerado com sucesso: {output_path}", file=sys.stderr)
            print(f"Total de novidades: {len(novidades)}", file=sys.stderr)
        else:
            # Modo stdout: apenas log em stderr
            print(f"Total de novidades: {len(novidades)}", file=sys.stderr)

        return output_data

    def read_json(self, filename='output.json'):
        """
        Lê um arquivo JSON gerado anteriormente

        Args:
            filename (str): Nome do arquivo JSON

        Returns:
            dict: Dados do JSON

        Raises:
            FileNotFoundError: Se o arquivo não existir
        """
        json_path = self.output_dir / filename

        if not json_path.exists():
            raise FileNotFoundError(f"Arquivo JSON não encontrado: {json_path}")

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    def display_summary(self, json_data):
        """
        Exibe um resumo do JSON gerado (em stderr para não interferir com stdout)

        Args:
            json_data (dict): Dados do JSON
        """
        print("\n" + "=" * 60, file=sys.stderr)
        print(f"RESUMO - Versão: {json_data['versao']} (Modo: {json_data.get('modo', 'N/A')})",
              file=sys.stderr)
        print("=" * 60, file=sys.stderr)

        for idx, novidade in enumerate(json_data['novidades'], 1):
            print(f"\n{idx}. Sistema: {novidade['sistema']}", file=sys.stderr)
            resumo = novidade['resumo'][:80]
            if len(novidade['resumo']) > 80:
                resumo += "..."
            print(f"   Resumo: {resumo}", file=sys.stderr)
            if 'numeroTarefa' in novidade:
                print(f"   Tarefa: {novidade['numeroTarefa']}", file=sys.stderr)

        print("\n" + "=" * 60, file=sys.stderr)
        print(f"Total: {len(json_data['novidades'])} novidade(s)", file=sys.stderr)
        print("=" * 60 + "\n", file=sys.stderr)
