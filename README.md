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

1. **Cabeçalho** - Nome do sistema e número da versão
2. **Data de atualização** - Data da última modificação do changelog (formato: *Atualizado em: DD/MM/AAAA*)
3. **O que foi alterado** - Resumo e detalhes das alterações
4. **Banco de dados** - Scripts SQL necessários
5. **Configurações necessárias** - Passos para configuração após deploy

## Convenções

- Alterações são categorizadas por tipo (novo, correção, melhoria)
- Utiliza emojis e ícones para facilitar identificação visual
- Inclui detalhes técnicos e instruções de configuração
- Versionamento semântico no formato major.minor.patch.build
- **Encoding**: Todos os arquivos devem ser salvos em **UTF-8** para garantir a correta exibição de caracteres especiais e emojis
