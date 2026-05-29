# Convenções de Changelog

Este guia define o padrão obrigatório para criação de novos arquivos de changelog.
Siga a estrutura abaixo para manter a consistência entre todos os sistemas.

---

## Nomenclatura dos arquivos

Cada arquivo representa uma versão de um sistema e deve ser criado em:

```
{Sistema}/{versao}.md
```

**Exemplos:**
```
iCRM4/09.96.52.00.md
SenderService/06.92.49.00.md
```

O versionamento segue o formato `major.minor.patch.build` com zeros à esquerda.

---

## Template

Copie o template abaixo como ponto de partida para novos changelogs:

```markdown
# NomeSistema

# :file_folder: X.XX.XX.XX

## :memo: O que foi alterado?

<details open>
<summary>Resumo</summary>

- :star: Item novo 1
- :warning: Correção 1
- :arrow_up: Melhoria 1

</details>

:star: Novo &nbsp; :warning: Correção &nbsp; :arrow_up: Melhoria

<details open>
<summary>Detalhes</summary>

:star: Item novo 1

Descrição detalhada da funcionalidade adicionada...

:warning: Correção 1

Descrição do problema corrigido e o comportamento esperado...

</details>

---

## :cd: Banco de dados

Não houve alteração no banco de dados.

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

Não há configurações necessárias para este deploy.
```

---

## Estrutura das seções

### Cabeçalho

```markdown
# NomeSistema
# :file_folder: X.XX.XX.XX
```

- A primeira linha é o nome do sistema (ex: `# iCRM4`)
- A segunda linha é a versão com o emoji de pasta

### O que foi alterado?

Use `## :memo: O que foi alterado?` como título da seção.

Contém dois blocos `<details open>`:

**Resumo** — lista de itens com emoji no início:

```markdown
- :star: Breve descrição do item novo
- :warning: Breve descrição da correção
- :arrow_up: Breve descrição da melhoria
```

**Detalhes** — cada item com emoji, seguido de parágrafo explicativo:

```markdown
:star: Título do item

Explicação completa do que foi feito, por que foi feito e qual o impacto...
```

### Banco de dados

Use `## :cd: Banco de dados` como título.

Sempre inclua os três blocos `<details open>` — Resumo, Detalhes e Scripts — mesmo que estejam vazios.
Se não houve alteração, indique: `Não houve alteração no banco de dados.`

### Configurações necessárias

Use `## :wrench: Configurações necessárias` como título.

Detalhe todos os passos que o implantador precisa executar: parâmetros, arquivos de configuração, testes pós-deploy, dependências externas.

---

## Emojis e categorias

| Emoji | Código | Uso |
|---|---|---|
| ⭐ | `:star:` | Nova funcionalidade |
| ⚠️ | `:warning:` | Correção de bug |
| ⬆️ | `:arrow_up:` | Melhoria em funcionalidade existente |
| 📁 | `:file_folder:` | Versão (no cabeçalho) |
| 📝 | `:memo:` | Seção "O que foi alterado?" |
| 💿 | `:cd:` | Seção "Banco de dados" |
| 🔧 | `:wrench:` | Seção "Configurações necessárias" |

---

## Regras importantes

- **Encoding**: salve todos os arquivos em **UTF-8**
- **Títulos de seção**: use os emojis como prefixo do título (`## :memo: O que foi alterado?`), nunca como o título inteiro (`### Novas Funcionalidades :star:`)
- **Banco de dados**: sempre inclua os 3 blocos `<details open>`, mesmo vazios
- **Detalhes**: cada item nos detalhes deve ter o emoji no início da linha, seguido de parágrafo com a explicação
- **Sidebar**: ao criar um novo arquivo, adicione o link correspondente no `_sidebar.md` no topo da seção do sistema (versões mais recentes primeiro)

---

## Atualizar o sidebar

Ao criar um novo changelog, adicione uma entrada no arquivo [`_sidebar.md`](_sidebar.md) na seção do sistema correspondente, **antes das versões mais antigas**:

```markdown
**iCRM4**

- [09.97.53.00](iCRM4/09.97.53.00.md)   ← nova linha adicionada aqui
- [09.96.52.00](iCRM4/09.96.52.00.md)
- [09.93.49.00](iCRM4/09.93.49.00.md)
```

---

## Geração automática

Para gerar changelogs automaticamente a partir do banco de dados, use a [ferramenta de automação](changelog_manager/README.md).
