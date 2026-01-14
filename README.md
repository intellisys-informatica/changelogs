# Changelogs - Intellisys

Repositório de documentação de changelogs dos sistemas da Intellisys.

## Sobre

Este repositório centraliza as documentações de versões (changelogs) dos sistemas desenvolvidos pela Intellisys, incluindo:

- **iCRM4** - Sistema principal de gestão de relacionamento com cliente
- **iCRMWeb** - Interface web do sistema iCRM
- **WebConsulta4** - Portal de consultas
- **CRMRelService** - Serviço de relatórios
- **CRMImpressor** - Serviço de impressão
- **SenderService** - Serviço de envio de mensagens
- **WebClienteJacomar** - Portal do cliente Jacomar
- **WebClientePinheiro** - Portal do cliente Pinheiro

## Estrutura

Cada sistema possui seu próprio diretório com arquivos de changelog organizados por versão no formato `X.XX.XX.XX.md`.

Os changelogs documentam:
- Novas funcionalidades (marcadas com :star:)
- Correções de bugs (marcadas com :warning:)
- Melhorias (marcadas com :arrow_up:)
- Alterações no banco de dados
- Configurações necessárias para implantação

## Formato dos Changelogs

Cada arquivo de changelog segue uma estrutura padronizada:

### Estrutura Obrigatória

```markdown
# NomeSistema

# :file_folder: X.XX.XX.XX

## :memo: O que foi alterado?

<details open>
<summary>Resumo</summary>

- :star: Item novo 1
- :star: Item novo 2
- :warning: Correção 1
- :arrow_up: Melhoria 1

</details>

:star: Novo
:warning: Correção
:arrow_up: Melhoria

<details open>
<summary>Detalhes</summary>

:star: Item novo 1

Detalhamento completo da alteração...

:warning: Correção 1

Detalhamento da correção...

</details>

---

## :cd: Banco de dados

Não houve alteração no banco de dados.
OU
Descrição das alterações no banco de dados.

<details open>
<summary>Resumo</summary>
</details>

<details open>
<summary>Detalhes</summary>
</details>

<details open>
<summary>Scripts</summary>
</details>

---

## :wrench: Configurações necessárias

Descrição das configurações necessárias após deploy.
```

### Componentes da Estrutura

1. **Cabeçalho**
   - Nome do sistema (ex: `# ICRMWSREST`)
   - Versão com emoji (ex: `# :file_folder: 09.92.48.11`)

2. **Seção "O que foi alterado?"**
   - Usar `## :memo: O que foi alterado?`
   - **Resumo** dentro de `<details open>` com lista de itens usando emojis:
     - `:star:` para novos itens
     - `:warning:` para correções
     - `:arrow_up:` para melhorias
   - **Legenda de emojis** (obrigatória):
     ```
     :star: Novo
     :warning: Correção
     :arrow_up: Melhoria
     ```
   - **Detalhes** dentro de `<details open>` com:
     - Emoji no início de cada item (`:star:`, `:warning:`, ou `:arrow_up:`)
     - Descrição detalhada

3. **Seção "Banco de dados"**
   - Usar `## :cd: Banco de dados`
   - Informar se houve ou não alterações
   - Incluir 3 blocos `<details open>` vazios ou preenchidos:
     - Resumo
     - Detalhes
     - Scripts

4. **Seção "Configurações necessárias"**
   - Usar `## :wrench: Configurações necessárias`
   - Detalhar todos os passos de configuração, parâmetros, testes e dependências

## Convenções

- **IMPORTANTE**: NÃO usar `### Novas Funcionalidades :star:` como título de seção
- Os emojis devem ser usados no início de cada item da lista, não como parte de títulos de seção
- Alterações são categorizadas por tipo no resumo e nos detalhes
- Utiliza emojis (:star:, :warning:, :arrow_up:) para facilitar identificação visual
- Inclui detalhes técnicos e instruções de configuração
- Versionamento semântico no formato major.minor.patch.build
- **Encoding**: Todos os arquivos devem ser salvos em **UTF-8** para garantir a correta exibição de caracteres especiais e emojis
- Sempre incluir os 3 blocos `<details open>` na seção de banco de dados, mesmo que vazios

## Tools

### Changelog Manager - Automação de Documentação

O projeto inclui uma ferramenta Python ([changelog_manager](changelog_manager/)) que automatiza a geração de changelogs a partir do banco de dados SQL Server.

#### Modos de Operação

O Changelog Manager suporta dois modos de operação:

**1. Modo Ciclo** - Documenta todas as tarefas de um ciclo completo
**2. Modo Tarefa** - Documenta uma tarefa individual

#### Comandos Disponíveis

##### Adicionar Tarefa Individual

Para adicionar uma tarefa específica ao changelog:

```
Claude, adicionar a tarefa {tarefaId} ao changelog, versão: {versao}
```

**Exemplo:**
```
Claude, adicionar a tarefa 12345 ao changelog, versão: 09.92.48.11
```

##### Atualizar Documentação de Ciclo Completo

Para gerar automaticamente os arquivos de changelog de um ciclo completo:

```
Claude, atualizar documentação. ciclo: {codigo}, versão: {NomeVersao}
```

**Exemplo:**
```
Claude, atualizar documentação. ciclo: 124, versão: 09.92.48.11
```

#### Processo Executado

##### Modo Tarefa Individual

Quando o comando de adicionar tarefa individual é recebido:

1. **Executar o script Python no modo tarefa**
   ```bash
   cd changelog_manager
   python src/main.py --modo tarefa --tarefa-id {tarefaId} --versao "{versao}"
   ```

2. **Receber JSON em stdout** (não gera arquivo físico)
   - O Python retorna o JSON diretamente via stdout:
     ```json
     {
       "versao": "XX.XX.XX.XX",
       "modo": "tarefa",
       "novidades": [
         {
           "sistema": "NomeSistema",
           "resumo": "Descrição resumida",
           "detalhes": "Descrição completa",
           "numeroTarefa": "12345"
         }
       ]
     }
     ```

3. **Processar JSON e gerenciar arquivo .md**
   - Identificar sistema e versão da tarefa
   - Verificar se arquivo `{Sistema}/{versao}.md` já existe:
     - **Se EXISTE**: Adicionar tarefa ao arquivo existente (append lógico)
     - **Se NÃO EXISTE**: Criar novo arquivo seguindo o template padrão
   - Classificar tarefa automaticamente como :star: (Novo), :warning: (Correção) ou :arrow_up: (Melhoria)
   - Adicionar tarefa nas seções de Resumo e Detalhes
   - Evitar duplicação de tarefas
   - Salvar arquivo em UTF-8

4. **Apresentar resumo**
   - Informar arquivo criado ou atualizado
   - Confirmar tarefa adicionada

##### Modo Ciclo Completo

Quando o comando de atualização de ciclo é recebido:

1. **Executar o script Python no modo ciclo**
   ```bash
   cd changelog_manager
   python src/main.py --modo ciclo --ciclo {codigo} --versao "{NomeVersao}"
   ```

2. **Receber JSON em stdout** (não gera arquivo físico)
   - O JSON contém todas as tarefas do ciclo agrupadas:
     ```json
     {
       "versao": "XX.XX.XX.XX",
       "modo": "ciclo",
       "novidades": [
         {
           "sistema": "NomeSistema1",
           "resumo": "Descrição resumida",
           "detalhes": "Descrição completa",
           "numeroTarefa": "12345"
         },
         {
           "sistema": "NomeSistema2",
           "resumo": "Outra descrição",
           "detalhes": "Outros detalhes",
           "numeroTarefa": "12346"
         }
       ]
     }
     ```

3. **Processar novidades e gerar/atualizar arquivos .md**
   - Agrupar novidades por sistema
   - Para cada sistema:
     - Verificar se arquivo `{Sistema}/{versao}.md` já existe
     - **Se EXISTE**: Adicionar tarefas ao arquivo existente
     - **Se NÃO EXISTE**: Criar novo arquivo no formato padrão
   - Seguir a estrutura obrigatória definida na seção [Estrutura Obrigatória](#estrutura-obrigatória)
   - Classificar cada novidade como :star: (Novo), :warning: (Correção) ou :arrow_up: (Melhoria)
   - Incluir todas as seções obrigatórias:
     - O que foi alterado? (com Resumo e Detalhes)
     - Banco de dados (com os 3 blocos `<details open>`)
     - Configurações necessárias
   - Salvar todos os arquivos em UTF-8

4. **Apresentar resumo das alterações**
   - Listar arquivos criados/atualizados
   - Informar número de novidades por sistema

#### Diferenças Entre os Modos

| Aspecto | Modo Tarefa | Modo Ciclo |
|---------|-------------|------------|
| **Entrada** | ID de uma tarefa específica | Código do ciclo completo |
| **Saída** | JSON com uma única tarefa | JSON com todas as tarefas do ciclo |
| **Uso típico** | Hotfixes, tarefas urgentes, documentação incremental | Release completo de versão |
| **Comando** | `--modo tarefa --tarefa-id X` | `--modo ciclo --ciclo X` |
| **Query SQL** | `consulta_tarefa_individual.sql` | `consulta_tarefas.sql` |

#### Comportamento de Arquivos .md

O Claude gerencia automaticamente os arquivos de changelog:

- **Arquivo NÃO existe**: Cria novo arquivo com estrutura completa
- **Arquivo EXISTE**: Adiciona tarefas preservando conteúdo existente
- **Duplicação**: Evita adicionar tarefas já documentadas no arquivo
- **Formatação**: Mantém padrão estabelecido com emojis e estrutura markdown

#### Requisitos

- Python 3.7+ instalado
- Ambiente virtual configurado no diretório `changelog_manager`
- Arquivo `.env` configurado com credenciais do banco de dados
- Queries SQL configuradas:
  - `changelog_manager/sql/consulta_tarefas.sql` (modo ciclo)
  - `changelog_manager/sql/consulta_tarefa_individual.sql` (modo tarefa)

#### Observações Importantes

- O Python **não gera arquivos físicos** - retorna JSON em stdout
- O Claude recebe o JSON em memória e gerencia os arquivos .md
- Tarefas são automaticamente registradas na tabela `TSK_TarefasDocumentadas` após processamento
- Validação de tarefas já documentadas ocorre no Python antes do retorno

Para mais detalhes sobre configuração e uso do Changelog Manager, consulte [changelog_manager/README.md](changelog_manager/README.md).
