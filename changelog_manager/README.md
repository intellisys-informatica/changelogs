# Changelog Manager

Aplicação Python para gerar JSON estruturado de changelogs a partir do banco de dados SQL Server, facilitando a automação da documentação com o Claude.

## Índice

- [Visão Geral](#visão-geral)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Fluxo de Trabalho](#fluxo-de-trabalho)
- [Exemplos](#exemplos)
- [Troubleshooting](#troubleshooting)

## Visão Geral

Esta aplicação automatiza o processo de documentação de changelogs ao:

1. Conectar-se ao banco de dados SQL Server
2. Executar queries SQL customizadas com parâmetros dinâmicos
3. Gerar arquivos JSON estruturados
4. Registrar tarefas documentadas para controle

O JSON gerado pode ser processado pelo Claude para criar automaticamente os arquivos `.md` de changelog.

## Requisitos

- Python 3.7+
- SQL Server (com driver ODBC 17 instalado)
- Acesso ao banco de dados com permissões de leitura e escrita

### Instalação do ODBC Driver

**Windows:**
- Baixe em: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

**Linux:**
```bash
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17
```

## Instalação

1. Clone ou navegue até o diretório do projeto:
```bash
cd c:\Documentação\changelogs\changelog_manager
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Configuração

### 1. Arquivo .env

Copie o arquivo de exemplo e configure suas credenciais:

```bash
copy .env.example .env
```

Edite o arquivo `.env`:

```env
# Configurações de Conexão com SQL Server
DB_SERVER=seu_servidor.database.windows.net
DB_DATABASE=nome_do_banco
DB_USERNAME=seu_usuario
DB_PASSWORD=sua_senha
DB_DRIVER=ODBC Driver 17 for SQL Server

# Nome da tabela que armazena tarefas já documentadas
DB_TABLE_DOCUMENTADAS=TSK_TarefasDocumentadas
```

### 2. Script SQL

Edite o arquivo `sql/consulta_tarefas.sql` com sua query real:

```sql
SELECT
    s.Nome AS Sistema,
    t.Resumo AS Resumo,
    t.Descricao AS Detalhes,
    t.Numero AS NumeroTarefa
FROM
    TabelaTarefas t
    INNER JOIN TabelaSistemas s ON t.SistemaID = s.ID
WHERE
    t.CicloCod = {cicloCod}
    AND t.Status = 'Concluída'
ORDER BY
    s.Nome, t.Prioridade DESC
```

**Colunas obrigatórias no SELECT:**
- `Sistema` - Nome do sistema/projeto
- `Resumo` - Descrição resumida da alteração
- `Detalhes` - Descrição completa
- `NumeroTarefa` - (Opcional) Para controle de documentação

**Tag dinâmica:**
- `{cicloCod}` - Será substituída pelo parâmetro `--ciclo`

### 3. Tabela de Controle (Opcional)

Se quiser rastrear tarefas documentadas, crie esta tabela:

```sql
CREATE TABLE TSK_TarefasDocumentadas (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    NumeroTarefa VARCHAR(50) NOT NULL,
    ArquivoMD VARCHAR(200) NOT NULL,
    DataExportacao DATETIME NOT NULL,
    CONSTRAINT UQ_TSK_TarefasDocumentadas_NumeroTarefa UNIQUE (NumeroTarefa)
);
```

## Uso

### Sintaxe Básica

```bash
python src/main.py --ciclo <NUMERO_CICLO> --versao <VERSAO>
```

### Parâmetros

| Parâmetro | Alias | Obrigatório | Descrição | Exemplo |
|-----------|-------|-------------|-----------|---------|
| `--ciclo` | `-c` | Sim | Número do ciclo | `124` |
| `--versao` | `-v` | Sim | Versão do changelog | `"09.91.47.20"` |
| `--sql` | `-s` | Não | Arquivo SQL customizado | `consulta_custom.sql` |
| `--output` | `-o` | Não | Nome do arquivo de saída | `resultado.json` |
| `--no-register` | - | Não | Não registra tarefas documentadas | - |

### Exemplos de Uso

**Uso básico:**
```bash
python src/main.py --ciclo 124 --versao "09.91.47.20"
```

**Com arquivo SQL customizado:**
```bash
python src/main.py -c 124 -v "09.91.47.20" -s consulta_hotfix.sql
```

**Com nome de saída personalizado:**
```bash
python src/main.py -c 124 -v "09.91.47.20" -o ciclo_124.json
```

**Sem registrar no banco:**
```bash
python src/main.py -c 124 -v "09.91.47.20" --no-register
```

## Estrutura do Projeto

```
changelog_manager/
├── src/
│   ├── main.py              # Entry point da aplicação
│   ├── config.py            # Gerenciamento de configurações (.env)
│   ├── database.py          # Conexão e operações com SQL Server
│   ├── query_executor.py    # Execução de queries SQL
│   └── json_generator.py    # Geração de JSON estruturado
├── sql/
│   └── consulta_tarefas.sql # Template SQL (editável)
├── .env                     # Configurações (não versionado)
├── .env.example             # Template de configurações
├── .gitignore               # Arquivos ignorados pelo Git
├── requirements.txt         # Dependências Python
└── README.md                # Esta documentação
```

## Fluxo de Trabalho

### 1. Execução Manual

```bash
# 1. Executar a aplicação Python
python src/main.py --ciclo 124 --versao "09.91.47.20"

# 2. Revisar o JSON gerado
notepad output.json

# 3. Processar com Claude (manualmente ou via prompt)
```

### 2. Integração com Claude

Quando estiver usando o Claude Code, você pode dizer:

```
Claude, atualizar documentação. ciclo: 124, versão "09.91.47.20"
```

O Claude irá:
1. Executar a aplicação Python
2. Ler o `output.json` gerado
3. Verificar se os arquivos `.md` já existem
4. Criar ou atualizar os arquivos de changelog

## Formato do JSON Gerado

```json
{
  "versao": "09.91.47.20",
  "novidades": [
    {
      "sistema": "iCRM4",
      "resumo": "Nova funcionalidade de relatórios",
      "detalhes": "Implementado módulo completo de relatórios customizados...",
      "numeroTarefa": "12345"
    },
    {
      "sistema": "SenderService",
      "resumo": "Correção no envio de emails",
      "detalhes": "Corrigido problema que causava falha...",
      "numeroTarefa": "12346"
    }
  ]
}
```

## Troubleshooting

### Erro: "Configurações obrigatórias faltando no arquivo .env"

**Solução:**
1. Verifique se o arquivo `.env` existe
2. Certifique-se de que todas as variáveis estão preenchidas
3. Copie do `.env.example` se necessário

### Erro: "pyodbc.Error: [Microsoft][ODBC Driver Manager] Data source name not found"

**Solução:**
1. Verifique se o ODBC Driver 17 está instalado
2. Confirme o nome correto do driver no `.env`
3. Liste drivers disponíveis:
```python
import pyodbc
print(pyodbc.drivers())
```

### Erro: "Arquivo SQL não encontrado"

**Solução:**
1. Verifique se `sql/consulta_tarefas.sql` existe
2. Se usando arquivo customizado, confirme o nome correto
3. Use caminho relativo ao diretório `sql/`

### Erro: "Login failed for user"

**Solução:**
1. Verifique credenciais no `.env`
2. Teste conexão no SQL Server Management Studio
3. Confirme permissões do usuário

### NENHUM RESULTADO ENCONTRADO

**Solução:**
1. Verifique se o ciclo informado existe no banco
2. Execute a query manualmente no SQL Server
3. Substitua `{cicloCod}` por um valor real para testar
4. Confirme se há tarefas naquele ciclo

### Encoding/Acentos aparecendo incorretos

**Solução:**
- Todos os arquivos usam UTF-8
- Verifique o encoding do seu terminal
- No Windows, use: `chcp 65001` antes de executar

## Manutenção

### Adicionar Novos Parâmetros SQL

Edite `src/query_executor.py`, método `replace_parameters`:

```python
def execute_sql_file(self, database, filename, parameters=None):
    # Exemplo: adicionar {dataInicio} e {dataFim}
    parameters = {
        'cicloCod': args.ciclo,
        'dataInicio': args.data_inicio,
        'dataFim': args.data_fim
    }
```

### Adicionar Campos no JSON

Edite `src/json_generator.py`, método `generate_json`:

```python
novidade = {
    'sistema': record['Sistema'],
    'resumo': record['Resumo'],
    'detalhes': record['Detalhes'],
    'novoCampo': record['NovoCampo']  # Adicione aqui
}
```

## Suporte

Para dúvidas ou problemas:
1. Revise esta documentação
2. Verifique os exemplos na seção [Exemplos](#exemplos)
3. Consulte os logs de erro detalhados
4. Teste componentes individualmente (conexão, SQL, etc.)

## Licença

Uso interno da organização.
