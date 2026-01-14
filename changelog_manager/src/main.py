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
from task_manager import TaskManager


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
  Modo Ciclo (documenta ciclo completo):
    python main.py --modo ciclo --ciclo 124 --versao "09.91.47.20"

  Modo Tarefa (documenta tarefa individual):
    python main.py --modo tarefa --tarefa-id 12345 --versao "09.91.47.20"

  Salvar em arquivo (opcional, para compatibilidade):
    python main.py --modo ciclo --ciclo 124 --versao "09.91.47.20" --output resultado.json
        """
    )

    parser.add_argument(
        '--modo', '-m',
        type=str,
        choices=['ciclo', 'tarefa'],
        required=True,
        help='Modo de operação: "ciclo" (ciclo completo) ou "tarefa" (tarefa individual)'
    )

    parser.add_argument(
        '--ciclo', '-c',
        type=str,
        help='Número do ciclo para consulta (obrigatório se --modo=ciclo)'
    )

    parser.add_argument(
        '--tarefa-id', '-t',
        type=str,
        help='ID da tarefa para consulta (obrigatório se --modo=tarefa)'
    )

    parser.add_argument(
        '--versao', '-v',
        type=str,
        required=True,
        help='Versão do changelog (ex: "09.91.47.20")'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Nome do arquivo JSON de saída (opcional - se omitido, imprime em stdout)'
    )

    parser.add_argument(
        '--no-register',
        action='store_true',
        help='Não registra as tarefas na tabela de documentadas'
    )

    return parser.parse_args()


def main():
    """Função principal da aplicação"""
    print("=" * 70, file=sys.stderr)
    print("CHANGELOG MANAGER - Gerador de JSON para Documentação", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    # Parse dos argumentos
    args = parse_arguments()

    # Valida combinação de parâmetros
    if args.modo == 'ciclo' and not args.ciclo:
        print("\nERRO: Modo 'ciclo' requer o parâmetro --ciclo", file=sys.stderr)
        return 1

    if args.modo == 'tarefa' and not args.tarefa_id:
        print("\nERRO: Modo 'tarefa' requer o parâmetro --tarefa-id", file=sys.stderr)
        return 1

    # Exibe parâmetros
    print(f"\nParâmetros:", file=sys.stderr)
    print(f"  Modo: {args.modo}", file=sys.stderr)
    if args.modo == 'ciclo':
        print(f"  Ciclo: {args.ciclo}", file=sys.stderr)
    else:
        print(f"  Tarefa ID: {args.tarefa_id}", file=sys.stderr)
    print(f"  Versão: {args.versao}", file=sys.stderr)
    if args.output:
        print(f"  Output File: {args.output}", file=sys.stderr)
    else:
        print(f"  Output: stdout (JSON)", file=sys.stderr)
    print(file=sys.stderr)

    try:
        # Valida configurações
        print("Validando configurações do .env...", file=sys.stderr)
        config.validate()
        print("Configurações OK!\n", file=sys.stderr)

        # Conecta ao banco de dados
        with Database() as db:
            results = []

            # Executa de acordo com o modo
            if args.modo == 'ciclo':
                # Modo Ciclo - busca todas as tarefas do ciclo
                print("Executando consulta SQL (modo ciclo)...", file=sys.stderr)
                executor = QueryExecutor()
                parameters = {'cicloCod': args.ciclo}
                results = executor.execute_sql_file(db, 'consulta_tarefas.sql', parameters)

            elif args.modo == 'tarefa':
                # Modo Tarefa - busca tarefa individual
                print(f"Buscando tarefa {args.tarefa_id}...", file=sys.stderr)
                task_mgr = TaskManager(db)
                results = task_mgr.get_task_by_id(args.tarefa_id)

            # Valida resultados
            if not results:
                print("\nNENHUM RESULTADO ENCONTRADO!", file=sys.stderr)
                if args.modo == 'ciclo':
                    print("Verifique se:", file=sys.stderr)
                    print("  1. O ciclo informado está correto", file=sys.stderr)
                    print("  2. Existem tarefas para documentar neste ciclo", file=sys.stderr)
                    print("  3. As tarefas não foram documentadas anteriormente", file=sys.stderr)
                else:
                    print("Verifique se:", file=sys.stderr)
                    print("  1. O ID da tarefa está correto", file=sys.stderr)
                    print("  2. A tarefa não foi documentada anteriormente", file=sys.stderr)
                    print("  3. A tarefa está concluída (TrfFim ou trffeito = 1)", file=sys.stderr)
                return 1

            # Gera JSON
            print("\nGerando JSON...", file=sys.stderr)
            generator = JsonGenerator()
            json_data = generator.generate_json(
                versao=args.versao,
                data_results=results,
                modo=args.modo,
                output_filename=args.output  # None = stdout, string = arquivo
            )

            # Exibe resumo (em stderr)
            generator.display_summary(json_data)

            # Registra tarefas como documentadas (se habilitado)
            if not args.no_register and 'novidades' in json_data:
                print("Registrando tarefas como documentadas...", file=sys.stderr)
                for novidade in json_data['novidades']:
                    if 'numeroTarefa' in novidade:
                        numero_tarefa = novidade['numeroTarefa']
                        sistema = novidade['sistema']
                        arquivo_md = f"{sistema}/{args.versao}.md"

                        try:
                            db.register_documented_task(numero_tarefa, arquivo_md)
                        except Exception as e:
                            print(f"  Erro ao registrar tarefa {numero_tarefa}: {e}",
                                  file=sys.stderr)

            print("\n" + "=" * 70, file=sys.stderr)
            print("PROCESSAMENTO CONCLUÍDO COM SUCESSO!", file=sys.stderr)
            print("=" * 70, file=sys.stderr)

            # Output final em stdout (apenas se não houver --output)
            if not args.output:
                import json
                print(json.dumps(json_data, ensure_ascii=False, indent=2))
            else:
                print(f"\nArquivo gerado: {args.output}", file=sys.stderr)

            return 0

    except ValueError as e:
        print(f"\nERRO DE CONFIGURAÇÃO: {e}", file=sys.stderr)
        return 1

    except FileNotFoundError as e:
        print(f"\nERRO: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"\nERRO INESPERADO: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
