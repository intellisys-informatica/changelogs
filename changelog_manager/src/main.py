"""
Changelog Manager - Entry Point
Aplicação para gerar JSON estruturado de changelogs a partir do banco de dados
"""
import sys
import argparse
from pathlib import Path

# Adiciona o diretório src ao path para imports
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from database import Database
from query_executor import QueryExecutor
from json_generator import JsonGenerator


def parse_arguments():
    """
    Processa argumentos da linha de comando

    Returns:
        argparse.Namespace: Argumentos processados
    """
    parser = argparse.ArgumentParser(
        description='Gerador de JSON de changelogs a partir do banco de dados',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --ciclo 124 --versao "09.91.47.20"
  python main.py -c 124 -v "09.91.47.20" -s consulta_custom.sql
  python main.py --ciclo 124 --versao "09.91.47.20" --output resultado.json
        """
    )

    parser.add_argument(
        '--ciclo', '-c',
        type=str,
        required=True,
        help='Número do ciclo para consulta (será substituído na tag {cicloCod})'
    )

    parser.add_argument(
        '--versao', '-v',
        type=str,
        required=True,
        help='Versão do changelog (ex: "09.91.47.20")'
    )

    parser.add_argument(
        '--sql', '-s',
        type=str,
        default='consulta_tarefas.sql',
        help='Nome do arquivo SQL a ser executado (padrão: consulta_tarefas.sql)'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output.json',
        help='Nome do arquivo JSON de saída (padrão: output.json)'
    )

    parser.add_argument(
        '--no-register',
        action='store_true',
        help='Não registra as tarefas na tabela de documentadas'
    )

    return parser.parse_args()


def main():
    """Função principal da aplicação"""
    print("=" * 70)
    print("CHANGELOG MANAGER - Gerador de JSON para Documentação")
    print("=" * 70)

    # Parse dos argumentos
    args = parse_arguments()

    print(f"\nParâmetros:")
    print(f"  Ciclo: {args.ciclo}")
    print(f"  Versão: {args.versao}")
    print(f"  SQL File: {args.sql}")
    print(f"  Output: {args.output}")
    print()

    try:
        # Valida configurações
        print("Validando configurações do .env...")
        config.validate()
        print("Configurações OK!\n")

        # Conecta ao banco de dados
        with Database() as db:
            # Executa query SQL
            print("Executando consulta SQL...")
            executor = QueryExecutor()
            parameters = {'cicloCod': args.ciclo}
            results = executor.execute_sql_file(db, args.sql, parameters)

            if not results:
                print("\nNENHUM RESULTADO ENCONTRADO!")
                print("Verifique se:")
                print("  1. O ciclo informado está correto")
                print("  2. Existem tarefas para documentar neste ciclo")
                print("  3. A query SQL está retornando dados")
                return 1

            # Gera arquivo JSON
            print("\nGerando arquivo JSON...")
            generator = JsonGenerator()
            json_data = generator.generate_json(args.versao, results, args.output)

            # Exibe resumo
            generator.display_summary(json_data)

            # Registra tarefas como documentadas (se habilitado)
            if not args.no_register and 'novidades' in json_data:
                print("Registrando tarefas como documentadas...")
                for novidade in json_data['novidades']:
                    if 'numeroTarefa' in novidade:
                        numero_tarefa = novidade['numeroTarefa']
                        sistema = novidade['sistema']
                        arquivo_md = f"{sistema}/{args.versao}.md"

                        try:
                            db.register_documented_task(numero_tarefa, arquivo_md)
                        except Exception as e:
                            print(f"  Erro ao registrar tarefa {numero_tarefa}: {e}")

            print("\n" + "=" * 70)
            print("PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
            print("=" * 70)
            print(f"\nArquivo gerado: {args.output}")
            print("Próximos passos:")
            print("  1. Revise o arquivo JSON gerado")
            print("  2. Use o Claude para processar o JSON e gerar os arquivos .md")
            print()

            return 0

    except ValueError as e:
        print(f"\nERRO DE CONFIGURAÇÃO: {e}")
        return 1

    except FileNotFoundError as e:
        print(f"\nERRO: {e}")
        return 1

    except Exception as e:
        print(f"\nERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
