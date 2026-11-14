# Conectores da Mio: Google, Microsoft 365, referências, dados geológicos e tarefas

## Para que serve

Os **conectores** levam o trabalho do RockFace para os serviços que a equipe já usa e trazem de lá o que ajuda a
descrição. Com eles a Mio pode:

* mandar a tabela das amostras de uma consulta para uma **planilha** do Google Sheets ou do Excel;
* escrever um **documento** (Google Docs, Word) ou montar uma **apresentação** com o resultado;
* preparar um **e-mail** (Gmail, Outlook) para o endereço que você der, ou marcar um **evento** na agenda;
* criar uma **tarefa** ou um cartão (Trello, Jira, Google Tasks, Planner);
* achar uma **referência** e o seu DOI no Crossref ou na sua biblioteca Zotero;
* trazer os dados de um **mineral** do Mindat e de uma **unidade estratigráfica** do Macrostrat;
* abrir um relato de problema (**issue**) no GitHub.

Os conectores do Google, do Microsoft 365, do Trello e do Jira usam o **Model Context Protocol (MCP)**, o padrão
aberto com que assistentes de IA falam com serviços externos. Crossref, Zotero, Mindat, Macrostrat e GitHub são
chamados diretamente pelo RockFace.

## Antes de começar

* Um projeto aberto.
* Para o Google, o Microsoft 365 e o Jira: o servidor MCP correspondente instalado no computador. Esses servidores
  não fazem parte do RockFace; o catálogo só sabe como iniciá-los. O do Google pede `uv` (comando `uvx`) e uma
  credencial OAuth "Aplicativo para computador" criada no Google Cloud; o do Microsoft 365 pede `Node.js` (comando
  `npx`) e faz o login da conta na primeira vez.
* Para Mindat, Zotero e GitHub: a chave de API ou o token da sua conta. Crossref e Macrostrat são abertos.
* Para os servidores remotos (Google Drive do próprio Google, GitHub, Trello): o token da conta.

## Passo a passo

### Ligar um conector no projeto

1. No painel da Mio clique em **Conectores** (ou, no Petro, na aba Ajuda, **Conectores…**).
2. A tabela mostra cada conector: grupo, tipo (embutido ou MCP, com o modo de início), o que faz e, entre
   colchetes, as chaves que ainda faltam neste computador.
3. Marque **Ligado neste projeto** na linha do conector. Todos começam desligados; ligar vale só para este projeto.
4. Selecione a linha e clique em **Chaves e tokens…** para informar as chaves (guardadas só neste computador) e os
   ajustes do conector (o número de usuário do Zotero, o repositório do GitHub, o e-mail de contato do Crossref).
5. Clique em **Testar**: o RockFace inicia o servidor e lista as ferramentas, sem enviar dado nenhum do projeto.

### Pedir à Mio

Escreva no painel da Mio, como numa conversa. Exemplos:

* `@mio ache a referência Folk 1980 petrology no crossref`
* `@mio dados do mineral dolomita no mindat` — a Mio traduz o nome pela nomenclatura (Dolomite)
* `@mio unidade estratigráfica Barreirinhas no macrostrat`
* `@mio envie as amostras com calcita para uma planilha do Google`
* `@mio crie um documento no Word com as amostras do poço ILLUSTRATIVE-1`
* `@mio agende na agenda a revisão das lâminas do poço ILLUSTRATIVE-2`
* `@mio crie uma tarefa no Trello: recontar a lâmina TS-002`
* `@mio abra uma issue no github: a exportação LAS pula amostras sem profundidade`

A Mio faz a parte do RockFace (as amostras pedidas, a tabela, o texto), escolhe o conector ligado e a ferramenta do
serviço que serve, e **prepara** a chamada. Uma janela mostra o conector, a ferramenta, os argumentos e se dados do
projeto saem do computador. Só **Confirmar e executar** envia; **Cancelar** não envia nada. O resultado aparece no
painel (no Crossref, já como lista de referências).

### Projeto confidencial

Marque **Projeto confidencial** no diálogo dos conectores. Nesse projeto toda chamada que leva dados do projeto para
fora pede uma segunda confirmação, com aviso; consultas que só levam as palavras digitadas (uma referência, um
mineral) seguem a regra normal.

### Um servidor MCP de sua escolha

**Adicionar um servidor MCP…** pede um nome curto e um comando (`uvx meu-servidor`, `python servidor.py`) ou um
endereço (`https://…`). O servidor entra desligado na tabela e funciona como os do catálogo.

## Opções

| Conector | Grupo | Como funciona | Precisa de |
|---|---|---|---|
| Google Workspace | google | servidor MCP da comunidade no computador (`uvx workspace-mcp --tool-tier core`): Sheets, Docs, Slides, Drive, Agenda, Gmail, Tarefas | `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET` e a sua conta `USER_GOOGLE_EMAIL` |
| Google Drive (servidor do Google) | google | servidor remoto do próprio Google (Developer Preview) | `TOKEN` |
| Microsoft 365 | microsoft | servidor da comunidade (`npx -y @softeria/ms-365-mcp-server`): Outlook, Calendário, OneDrive, Excel, Word, To Do, OneNote, Teams, SharePoint | login da conta Microsoft na primeira vez |
| Microsoft 365 (CLI) | microsoft | CLI for Microsoft 365 da comunidade PnP: SharePoint, Teams, Planner, OneDrive | login da conta |
| Crossref | references | direto, aberto | opcional: `mailto` |
| Zotero | references | direto | `API_KEY` e o ajuste `user_id` |
| Mindat | geodata | direto | `API_KEY` (gratuita) |
| Macrostrat | geodata | direto, aberto | — |
| GitHub | dev | direto (issues) | `TOKEN` e, se quiser, o ajuste `repo` |
| GitHub (servidor do GitHub) | dev | servidor remoto do GitHub | `TOKEN` |
| Trello | dev | servidor remoto da Atlassian | `TOKEN` |
| Jira e Confluence | dev | servidor da comunidade (`uvx mcp-atlassian`) | `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN` |

As chaves podem vir também de variáveis de ambiente `ROCKFACE_<CONECTOR>_<NOME>` (por exemplo
`ROCKFACE_GITHUB_TOKEN`), que valem mais que o arquivo.

## Como funciona

* **Desligados por padrão.** A lista dos conectores ligados fica no projeto; as chaves ficam só no computador, no
  arquivo `~/.rockface/connectors.json` (permissão 600), nunca no projeto nem na auditoria.
* **Mostrado antes de executar.** Toda chamada é preparada primeiro; nada sai sem a sua confirmação.
* **Auditoria.** Toda chamada — feita, recusada, cancelada ou com falha — gera uma linha na auditoria do projeto
  (`connector`), com a ferramenta e um resumo criptográfico dos argumentos; o diálogo mostra as últimas.
* **A ferramenta certa.** Os servidores MCP dizem quais ferramentas têm. Para mandar uma tabela, a Mio procura a
  ferramenta cujo nome e descrição falam de planilha e de criar, e põe a tabela no parâmetro de dados (`values`,
  `rows`, `data`…). Ela nunca propõe uma ferramenta de apagar. Você vê a ferramenta escolhida antes de confirmar.
* **O que a ferramenta leva (0.31).** Entre as ferramentas que servem, a Mio prefere a que leva o conteúdo — uma
  planilha importada de CSV em vez de uma planilha vazia, um documento importado de Markdown (com título e tabela)
  em vez de texto corrido. Ferramentas do tipo `manage_event` e `manage_task` recebem a ação `create`; a lista de
  tarefas padrão é `@default`. A data e a hora de um evento vêm da frase (*amanhã às 10h*, *dia 02/12 às 14h*,
  *tomorrow at 3pm*), com uma hora de duração. Um e-mail só é preparado com o endereço escrito no pedido.
* **A sua conta.** Os servidores que pedem a conta em cada chamada (o do Google pede `user_google_email`) a recebem
  do segredo `USER_GOOGLE_EMAIL` deste computador; sem ele, a Mio diz o que falta em vez de adivinhar.
* **Segurança.** Documentos e e-mails que voltam de um serviço podem conter instruções escritas por outras pessoas;
  a Mio não as segue — ela só mostra o resultado.

## Por script

```python
prj.enable_connector("crossref")
r = prj.connector_call("crossref", "search_works", {"query": "Folk 1980 petrology"}, confirm=True)
for item in r.data:
    print(rf.connectors.reference_text(item))

prj.enable_connector("google")
header, rows = prj.query_table("identification", ("diagenetic", "constituent", "calcite_dia"))
call = prj.connector_plan("google", "export_table", {"title": "Amostras com calcita", "rows": [header] + rows})
print(call.preview("pt"))                        # o que vai sair
res = prj.connector_run(call, confirm=True)      # você escreveu a chamada: confirm=True
print(res.ok, res.text)
print(prj.connector_calls()[-1])                 # a linha da auditoria
```

Na linha de comando: `rockface connectors list projeto.rockface`, `rockface connectors enable projeto.rockface
crossref`, `rockface connectors secret github TOKEN`, `rockface connectors test projeto.rockface google`,
`rockface connectors call projeto.rockface crossref search_works '{"query": "Folk 1980"}'`.

## Limites e problemas comuns

* "O conector … está desligado": ligue-o na tabela, para este projeto.
* "faltam …": informe as chaves em **Chaves e tokens…**.
* O teste não responde: o servidor não está instalado (`uvx`, `npx` não encontrados) ou a conta ainda não fez login.
* Servidores diferentes dão nomes diferentes às ferramentas; se a Mio escolher mal, use **Por script** com a
  ferramenta certa (`prj.connector_tools("google")` lista todas) ou peça de outra forma.
* O servidor remoto do Gmail do próprio Google cria rascunhos, não envia: é você quem envia. O servidor da
  comunidade no nível `core` só tem a ferramenta de **enviar**: confira o destinatário na janela de confirmação.

## Cobertura

Etapa 0.30 do ROADMAP (pedido do proprietário de 13/11/2026: os conectores MCP da Mio, primeiro as ferramentas do
Google; e, por escolha dele, Microsoft 365, referências e dados geológicos, GitHub e tarefas).
