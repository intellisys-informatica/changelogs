# Changelog Manager

Aplicação Python para gerar JSON estruturado de changelogs a partir do banco de dados SQL Server, facilitando a automação da documentação com o Claude.

## Índice

- [Visão Geral](#visão-geral)
- [Modos de Operação](#modos-de-operação)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Formato do JSON](#formato-do-json)
- [Fluxo de Trabalho](#fluxo-de-trabalho)
- [Exemplos](#exemplos)
- [Troubleshooting](#troubleshooting)

## Visão Geral

Esta aplicação automatiza o processo de documentação de changelogs ao:

1. Conectar-se ao banco de dados SQL Server
2. Executar queries SQL customizadas com parâmetros dinâmicos
3. **Retornar JSON estruturado via stdout** (ou opcionalmente salvar em arquivo)
4. Registrar tarefas documentadas para controle

O JSON retornado é processado pelo Claude Code para criar ou atualizar automaticamente os arquivos `.md` de changelog.

## Modos de Operação

O Changelog Manager suporta dois modos de operação:

### 1. Modo Ciclo
Documenta todas as tarefas de um ciclo completo de desenvolvimento.

**Uso:**
```bash
python src/main.py --modo ciclo --ciclo 124 --versao "09.92.48.11"
```

**Características:**
- Busca todas as tarefas de um ciclo específico
- Agrupa tarefas por sistema
- Ideal para releases completos de versão

### 2. Modo Tarefa
Documenta uma tarefa individual específica.

**Uso:**
```bash
python src/main.py --modo tarefa --tarefa-id 12345 --versao "09.92.48.11"
```

**Características:**
- Busca uma única tarefa por ID
- Ideal para hotfixes e documentação incremental
- Permite adicionar tarefas a changelogs existentes

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

### 2. Scripts SQL

O projeto utiliza dois scripts SQL:

#### `sql/consulta_tarefas.sql` (Modo Ciclo)
Busca todas as tarefas de um ciclo completo.

```sql
SELECT
    SUBSTRING(t.TrfNome, 1, CHARINDEX('-', t.TrfNome)-1) AS Sistema,
    SUBSTRING(t.TrfNome, CHARINDEX('-', t.TrfNome)+1, LEN(t.TrfNome)) AS Resumo,
    t.TrfObservacao2 AS Detalhes,
    t.Tarefaid AS NumeroTarefa
FROM TSK_Tarefa t
    LEFT JOIN TSK_TarefasDocumentadas td ON (t.Tarefaid = td.NumeroTarefa)
WHERE td.NumeroTarefa IS NULL
    AND t.CicloId = {cicloCod}
    AND (t.TrfFim IS NOT NULL OR t.trffeito = 1)
```

**Tag dinâmica:** `{cicloCod}` - Substituída pelo parâmetro `--ciclo`

#### `sql/consulta_tarefa_individual.sql` (Modo Tarefa)
Busca uma tarefa específica por ID.

```sql
SELECT
    SUBSTRING(t.TrfNome, 1, CHARINDEX('-', t.TrfNome)-1) AS Sistema,
    SUBSTRING(t.TrfNome, CHARINDEX('-', t.TrfNome)+1, LEN(t.TrfNome)) AS Resumo,
    t.TrfObservacao2 AS Detalhes,
    t.Tarefaid AS NumeroTarefa
FROM TSK_Tarefa t
    LEFT JOIN TSK_TarefasDocumentadas td ON (t.Tarefaid = td.NumeroTarefa)
WHERE t.Tarefaid = {tarefaId}
    AND td.NumeroTarefa IS NULL
    AND (t.TrfFim IS NOT NULL OR t.trffeito = 1)
```

**Tag dinâmica:** `{tarefaId}` - Substituída pelo parâmetro `--tarefa-id`

**Colunas obrigatórias no SELECT:**
- `Sistema` - Nome do sistema/projeto
- `Resumo` - Descrição resumida da alteração
- `Detalhes` - Descrição completa
- `NumeroTarefa` - ID da tarefa (para controle)

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

**Modo Ciclo:**
```bash
python src/main.py --modo ciclo --ciclo <NUMERO_CICLO> --versao <VERSAO>
```

**Modo Tarefa:**
```bash
python src/main.py --modo tarefa --tarefa-id <ID_TAREFA> --versao <VERSAO>
```

### Parâmetros

| Parâmetro | Alias | Obrigatório | Descrição | Exemplo |
|-----------|-------|-------------|-----------|---------|
| `--modo` | `-m` | Sim | Modo de operação (`ciclo` ou `tarefa`) | `ciclo` |
| `--ciclo` | `-c` | Condicional* | Número do ciclo | `124` |
| `--tarefa-id` | `-t` | Condicional** | ID da tarefa | `12345` |
| `--versao` | `-v` | Sim | Versão do changelog | `"09.91.47.20"` |
| `--output` | `-o` | Não | Nome do arquivo de saída (se omitido, usa stdout) | `output.json` |
| `--no-register` | - | Não | Não registra tarefas documentadas | - |

**\* Obrigatório se --modo=ciclo**
**\*\* Obrigatório se --modo=tarefa**

### Comportamento de Saída

Por padrão, o JSON é retornado em **stdout**, permitindo que o Claude Code processe diretamente em memória:

```bash
python src/main.py --modo tarefa --tarefa-id 12345 --versao "09.92.48.11"
# Retorna JSON em stdout
```

Para compatibilidade ou debug, você pode salvar em arquivo:

```bash
python src/main.py --modo ciclo --ciclo 124 --versao "09.92.48.11" --output resultado.json
# Salva JSON em arquivo
```

**Importante:** Logs e mensagens são enviados para **stderr**, mantendo stdout limpo para o JSON.

## Estrutura do Projeto

```
changelog_manager/
├── src/
│   ├── main.py              # Entry point da aplicação
│   ├── config.py            # Gerenciamento de configurações (.env)
│   ├── database.py          # Conexão e operações com SQL Server
│   ├── query_executor.py    # Execução de queries SQL
│   ├── json_generator.py    # Geração de JSON estruturado
│   └── task_manager.py      # Gerenciamento de tarefas individuais [NOVO]
├── sql/
│   ├── consulta_tarefas.sql           # Query para modo ciclo
│   └── consulta_tarefa_individual.sql # Query para modo tarefa [NOVO]
├── .env                     # Configurações (não versionado)
├── .env.example             # Template de configurações
├── .gitignore               # Arquivos ignorados pelo Git
├── requirements.txt         # Dependências Python
└── README.md                # Esta documentação
```

## Formato do JSON

### Estrutura de Saída

```json
{
  "versao": "09.92.48.11",
  "modo": "tarefa",
  "novidades": [
    {
      "sistema": "iCRM4",
      "resumo": "Correção no cálculo de impostos",
      "detalhes": "Corrigido problema que causava erro no cálculo...",
      "numeroTarefa": "12345"
    }
  ]
}
```

### Campos

- **versao** (string): Versão do changelog
- **modo** (string): Modo de operação (`"ciclo"` ou `"tarefa"`)
- **novidades** (array): Lista de alterações
  - **sistema** (string): Nome do sistema
  - **resumo** (string): Descrição resumida
  - **detalhes** (string): Descrição completa
  - **numeroTarefa** (string): ID da tarefa

## Fluxo de Trabalho

### Modo Tarefa Individual (Novo)

```bash
# 1. Executar a aplicação Python
python src/main.py --modo tarefa --tarefa-id 12345 --versao "09.92.48.11"

# 2. JSON é retornado em stdout (Claude captura automaticamente)

# 3. Claude processa JSON e gerencia arquivo .md:
#    - Se arquivo existe: adiciona tarefa
#    - Se não existe: cria novo arquivo
```

### Modo Ciclo Completo

```bash
# 1. Executar a aplicação Python
python src/main.py --modo ciclo --ciclo 124 --versao "09.92.48.11"

# 2. JSON com todas as tarefas é retornado em stdout

# 3. Claude agrupa por sistema e processa cada arquivo .md
```

### Integração com Claude Code

Quando estiver usando o Claude Code:

**Para adicionar tarefa individual:**
```
Claude, adicionar a tarefa 12345 ao changelog, versão: 09.92.48.11
```

**Para atualizar ciclo completo:**
```
Claude, atualizar documentação. ciclo: 124, versão: 09.92.48.11
```

O Claude irá:
1. Executar a aplicação Python
2. Receber o JSON em memória (stdout)
3. Verificar se os arquivos `.md` já existem
4. Criar ou atualizar os arquivos de changelog
5. Evitar duplicação de tarefas

## Exemplos

### Exemplo 1: Adicionar Tarefa Individual

```bash
python src/main.py --modo tarefa --tarefa-id 12345 --versao "09.92.48.11"
```

**Saída (stdout):**
```json
{
  "versao": "09.92.48.11",
  "modo": "tarefa",
  "novidades": [
    {
      "sistema": "iCRM4",
      "resumo": "Correção no módulo de vendas",
      "detalhes": "Corrigido bug que impedia...",
      "numeroTarefa": "12345"
    }
  ]
}
```

### Exemplo 2: Processar Ciclo Completo

```bash
python src/main.py --modo ciclo --ciclo 124 --versao "09.92.48.11"
```

**Saída (stdout):**
```json
{
  "versao": "09.92.48.11",
  "modo": "ciclo",
  "novidades": [
    {
      "sistema": "iCRM4",
      "resumo": "Nova funcionalidade X",
      "detalhes": "Implementado...",
      "numeroTarefa": "12345"
    },
    {
      "sistema": "SenderService",
      "resumo": "Correção no envio de emails",
      "detalhes": "Corrigido...",
      "numeroTarefa": "12346"
    }
  ]
}
```

### Exemplo 3: Salvar em Arquivo (Opcional)

```bash
python src/main.py --modo tarefa --tarefa-id 12345 --versao "09.92.48.11" --output resultado.json
```

Gera arquivo `resultado.json` com o conteúdo JSON.

### Exemplo 4: Sem Registrar no Banco

```bash
python src/main.py --modo tarefa --tarefa-id 12345 --versao "09.92.48.11" --no-register
```

Retorna JSON mas não registra na tabela `TSK_TarefasDocumentadas`.

## Troubleshooting

### Erro: "Configurações obrigatórias faltando no arquivo .env"

**Solução:**
1. Verifique se o arquivo `.env` existe
2. Certifique-se de que todas as variáveis estão preenchidas
3. Copie do `.env.example` se necessário

### Erro: "Modo 'ciclo' requer o parâmetro --ciclo"

**Solução:**
- Se usando modo ciclo, forneça o parâmetro `--ciclo`
- Se usando modo tarefa, forneça o parâmetro `--tarefa-id`

### Erro: "pyodbc.Error: Data source name not found"

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
1. Verifique se `sql/consulta_tarefas.sql` existe (modo ciclo)
2. Verifique se `sql/consulta_tarefa_individual.sql` existe (modo tarefa)
3. Certifique-se de estar no diretório correto

### NENHUM RESULTADO ENCONTRADO (Modo Ciclo)

**Solução:**
1. Verifique se o ciclo informado existe no banco
2. Execute a query manualmente no SQL Server
3. Substitua `{cicloCod}` por um valor real para testar
4. Confirme se há tarefas naquele ciclo que não foram documentadas

### NENHUM RESULTADO ENCONTRADO (Modo Tarefa)

**Solução:**
1. Verifique se o ID da tarefa está correto
2. Confirme se a tarefa não foi documentada anteriormente
3. Verifique se a tarefa está concluída (`TrfFim IS NOT NULL` ou `trffeito = 1`)
4. Execute a query manualmente substituindo `{tarefaId}`

### Encoding/Acentos aparecendo incorretos

**Solução:**
- Todos os arquivos usam UTF-8
- Verifique o encoding do seu terminal
- No Windows, use: `chcp 65001` antes de executar

## Diferenças Entre os Modos

| Aspecto | Modo Tarefa | Modo Ciclo |
|---------|-------------|------------|
| **Entrada** | ID de uma tarefa específica | Código do ciclo completo |
| **Query SQL** | `consulta_tarefa_individual.sql` | `consulta_tarefas.sql` |
| **Saída** | JSON com uma única tarefa | JSON com todas as tarefas do ciclo |
| **Uso típico** | Hotfixes, tarefas urgentes, documentação incremental | Release completo de versão |
| **Parâmetro obrigatório** | `--tarefa-id` | `--ciclo` |

## Manutenção

### Adicionar Novos Campos no JSON

Edite `src/json_generator.py`, método `generate_json`:

```python
novidade = {
    'sistema': record['Sistema'],
    'resumo': record['Resumo'],
    'detalhes': record['Detalhes'],
    'novoCampo': record['NovoCampo']  # Adicione aqui
}
```

### Modificar Queries SQL

- **Modo Ciclo:** Edite `sql/consulta_tarefas.sql`
- **Modo Tarefa:** Edite `sql/consulta_tarefa_individual.sql`

Mantenha as colunas obrigatórias: `Sistema`, `Resumo`, `Detalhes`, `NumeroTarefa`

## Novidades da Versão Atual

### Principais Mudanças

✅ **Novo Modo Tarefa Individual** - Documente tarefas específicas sem processar ciclo inteiro

✅ **Output em stdout** - JSON retornado diretamente, sem gerar arquivos físicos (comportamento padrão)

✅ **Claude gerencia arquivos .md** - Separação clara de responsabilidades entre Python e Claude

✅ **Validação aprimorada** - Verificação de tarefas já documentadas antes do processamento

✅ **Logs em stderr** - Mantém stdout limpo para o JSON

### Compatibilidade

- ✅ Modo ciclo mantém comportamento anterior
- ✅ Parâmetro `--output` disponível para compatibilidade
- ✅ Estrutura do banco de dados inalterada
- ✅ Sem breaking changes

## Suporte

Para dúvidas ou problemas:
1. Revise esta documentação
2. Verifique os exemplos na seção [Exemplos](#exemplos)
3. Consulte os logs de erro detalhados (stderr)
4. Teste componentes individualmente (conexão, SQL, etc.)

## Licença

Uso interno da organização.
