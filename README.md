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

### Título da Feature/Correção

:star: Breve descrição

Detalhamento completo da alteração...

### Outra Alteração

:warning: Breve descrição

Detalhamento da correção...

</details>

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
     - Subtítulos para cada alteração (usando `###`)
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
