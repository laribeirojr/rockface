# O ChatGPT e o Gemini no RockFace

## Para que serve

O painel do assistente de IA do RockFace conversa com o **Claude** (Anthropic), o **ChatGPT** (OpenAI) ou o
**Gemini** (Google), como você escolher. Os três usam as mesmas ferramentas do RockFace e seguem as mesmas regras do
Claude (veja [O Claude no RockFace](claude.md)): leem as amostras do projeto, encontram as páginas deste guia, olham
as imagens da lâmina e a janela, abrem uma descrição e uma aba e propõem campos da descrição microscópica e do
sistema poroso — sempre **desmarcados**, para você decidir.

Os apps de computador também trabalham no RockFace, pelo servidor MCP do RockFace: o **Claude Desktop**, o **app do
ChatGPT para computador** (e o Codex, que compartilha a configuração dele) e o **Google Antigravity**, no computador e
na linha de comando, onde o Gemini trabalha.

## Antes de começar

* **Para o painel**, a chave da API da empresa cujo assistente você usa. As chaves da API são pagas pelo uso e não
  fazem parte da assinatura dos apps do ChatGPT ou do Gemini:
  * ChatGPT — OpenAI Platform, platform.openai.com → API keys (ou a variável `OPENAI_API_KEY`);
  * Gemini — Google AI Studio, aistudio.google.com → Get API key (ou `GEMINI_API_KEY`, ou `GOOGLE_API_KEY`);
  * Claude — Claude Console (ou `ANTHROPIC_API_KEY`).
  Cada chave fica num arquivo da sua pasta de usuário que só você pode ler, nunca num projeto.
* **Para um app de computador**, o app instalado e com a sua conta: ali não precisa de chave da API.
* **Os seus dados.** O que um assistente lê — a pergunta, as respostas das ferramentas, as imagens que ele olha — vai
  para a empresa dele. Dados públicos, tudo bem; **dados privados, não use**: use a Mio, que roda neste computador. O
  RockFace pergunta antes da primeira conversa com cada assistente, e de novo em cada sessão num projeto marcado como
  confidencial.

## Passo a passo

### Escolher o assistente do painel

1. Clique em **Assistente de IA** (Início → Ferramentas, ou `Ctrl+Alt+K`).
2. No painel, escolha **Claude**, **ChatGPT** ou **Gemini** e depois o modelo:
   * ChatGPT: **GPT-6.1 Sol** (padrão; US$ 2 / 10 por milhão de tokens, entrada / saída), **GPT-6 Astra** (o mais
     capaz; US$ 10 / 50), **GPT-6.1 Terra** (US$ 1 / 5), **GPT-6 Luna** (o mais rápido e barato; US$ 0,10 / 0,50);
   * Gemini: **Gemini 4 Argon** (padrão; US$ 2 / 10 até 30 de novembro de 2026, depois US$ 4 / 20),
     **Gemini 3.8 Flash** (mais rápido e barato; US$ 0,75 / 3,75, preço de lançamento), **Gemini 3.1 Pro (preview)**
     (US$ 2 / 12).
   Cada assistente guarda o seu modelo; trocar de assistente começa uma conversa nova.
3. Na primeira vez, clique no botão de **configurações**, escolha o assistente em **Chaves e modelos de**, cole a chave
   e clique em **Salvar**.
4. Pergunte, na sua língua, como com o Claude: "Abra a ILL-TS-001, olhe a imagem e proponha a seleção e os poros." As
   propostas chegam numa janela, desmarcadas; marque o que você vê e clique em **Aplicar as marcadas**.

### Deixar um app de computador trabalhar no RockFace

Nas configurações do painel:

* **Escrever no app do ChatGPT para computador** inclui o RockFace em `~/.codex/config.toml`, que o app do ChatGPT
  para computador, o Codex e a extensão dele para editores compartilham (uma cópia datada do arquivo antigo é
  guardada). No app do ChatGPT, abra Settings → MCP servers e reinicie as extensões; o RockFace aparece ali. (Também
  dá para incluí-lo à mão ali: STDIO, com o comando mostrado por `rockface assistant config chatgpt`.)
* **Escrever no Google Antigravity (Gemini)** inclui o RockFace em `~/.gemini/config/mcp_config.json`, que o app
  Antigravity para computador e a linha de comando dele (`agy`) compartilham. Rode `/mcp` ali para ver as ferramentas
  do RockFace.
* **Instalar no Claude Desktop…** e **Escrever na configuração do Claude Desktop**: veja
  [O Claude no RockFace](claude.md).

Cada um desses botões também liga **Deixar os assistentes de IA trabalharem nesta janela**, para que o app trabalhe na
janela que você tem aberta (e no arquivo do projeto, quando nenhuma janela está aberta, se você escolheu um).

## Como funciona

* **Um só conjunto de ferramentas, três conversas.** As ferramentas, as regras e a auditoria são as do Claude no
  RockFace. O painel fala com o ChatGPT pela Responses API da OpenAI (`store: false`: a OpenAI não guarda a conversa;
  o raciocínio do modelo volta cifrado entre as vezes) e com o Gemini pela API do Gemini (`generateContent` com
  declarações de funções; cada vez do modelo volta como veio, com a assinatura do raciocínio). As imagens vão para o
  ChatGPT numa mensagem depois das respostas das ferramentas e para o Gemini junto com elas; só as duas últimas ficam
  na conversa.
* **A janela das propostas** diz qual assistente as fez ("Propostas do Gemini"); quando um app de computador chama,
  ela diz "assistente de IA", porque o RockFace não sabe qual app é.
* **Auditoria.** Cada chamada de ferramenta é gravada na auditoria do projeto com a origem: `panel:` para o painel,
  `mcp:` para um app de computador.
* **As versões web do ChatGPT e do Gemini** não alcançam um programa no seu computador; o RockFace não se abre para a
  internet. Use os apps de computador.

## Por script

```python
rf.assistants()                                     # os assistentes, se há chave, os modelos e os preços
rf.assistant_ask("Qual fácies tem a maior porosidade?", prj, assistant="gemini")
rf.assistant_ask("Quantas amostras têm calcita?", prj, assistant="chatgpt", model="gpt-6-luna")
rf.assistant_config("chatgpt")                      # a tabela [mcp_servers.rockface], como texto
rf.assistant_config("gemini", install=True)         # gravada na configuração do Antigravity
```

Pela linha de comando: `rockface assistant list`, `rockface assistant ask projeto.rockface "pergunta" --with
chatgpt`, `rockface assistant config chatgpt|gemini|claude`.

## Limites e problemas comuns

* "A chave da API foi recusada": a chave de uma empresa não serve para outra; confira se a chave nas configurações está
  no assistente certo.
* "A chave não tem permissão para isso (crédito ou modelo)": a conta está sem crédito ou sem acesso àquele modelo — as
  chaves do ChatGPT e do Gemini precisam de cobrança ativada para esses modelos.
* O app do ChatGPT não mostra o RockFace: reinicie as extensões dele (Settings → MCP servers) ou o app.
* O Antigravity não mostra o RockFace: confira `/mcp`; um Gemini CLI antigo lê `~/.gemini/settings.json` (inclua ali,
  em `mcpServers`, a entrada mostrada por `rockface mcp config --live`).
* Os modelos e os preços mudam com frequência; o RockFace mostra os de novembro de 2026.
* Sem internet, ou com dados privados, use a Mio.

## Cobertura

O10 (o pedido do proprietário de 2026-11-18: o ChatGPT e o Gemini trabalhando no RockFace como o Claude).

Referências: OpenAI, Responses API e chamada de funções, https://platform.openai.com/docs; OpenAI, Model Context
Protocol no app do ChatGPT para computador e no Codex, https://learn.chatgpt.com/docs/extend/mcp; Google, chamada de
funções na API do Gemini, https://ai.google.dev/gemini-api/docs; Google Antigravity, migração do Gemini CLI,
https://antigravity.google/docs/cli/gcli-migration.
