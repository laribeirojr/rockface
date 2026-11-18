# O Claude no RockFace

## Para que serve

O Claude, o assistente de IA da Anthropic, pode trabalhar **junto** com o RockFace, como faz num editor de textos ou
numa planilha: lê as amostras do projeto, encontra as páginas deste guia, olha as imagens das lâminas e a janela,
abre uma descrição e uma aba e propõe campos da descrição microscópica e do sistema poroso. Ele chega ao RockFace de
três formas, que podem ser usadas juntas:

1. **O painel do Claude**, dentro de cada programa do RockFace (ao lado da Mio): você conversa com o Claude sem sair
   do RockFace.
2. **O Claude Desktop**, com a **extensão do RockFace** (um clique duplo a instala): você conversa com o Claude no
   app dele e ele trabalha no RockFace.
3. **A janela ao vivo**: seja qual for a forma de conversar, o Claude trabalha na janela do RockFace que está aberta
   — a descrição em que você está, a aba que você vê, as imagens da lâmina dela.

As três usam as mesmas ferramentas, as mesmas regras e a mesma auditoria: o que o Claude faz pelo Claude Desktop é o
que ele faz pelo painel.

A Mio continua como é: local, gratuita e sem internet. O Claude é uma opção para quem quer um modelo mais forte e
aceita que a conversa vá para a Anthropic.

Desde a 1.2.0 o mesmo painel também conversa com o ChatGPT e o Gemini, e o app do ChatGPT para computador e o
Google Antigravity também trabalham no RockFace: veja [O ChatGPT e o Gemini no RockFace](assistants.md).

## Antes de começar

* Para o **painel**: uma **chave da API do Claude**. Ela é criada no Claude Console (platform.claude.com → API keys)
  e é paga pelo uso; a assinatura dos apps do Claude (Pro, Max, Team) não a inclui. Cole-a nas configurações do
  painel: ela fica num arquivo da sua pasta de usuário que só você pode ler, nunca num projeto. Uma chave na variável
  `ANTHROPIC_API_KEY` é usada primeiro.
* Para o **Claude Desktop**: o app Claude Desktop, com a sua conta. Não precisa de chave da API — o Claude Desktop
  usa o seu plano do Claude.
* **Os seus dados.** O que o Claude lê — a pergunta, as respostas das ferramentas, as imagens que ele olha — é
  enviado à Anthropic. Dados públicos, tudo bem; **dados privados, não use o Claude**: use a Mio, que roda neste
  computador. O RockFace pergunta antes da primeira conversa, e de novo em cada sessão num projeto marcado como
  confidencial (*Ferramentas → Conectores*).

## Passo a passo

### Conversar com o Claude no RockFace (o painel)

1. Clique em **Claude** (Início → Ferramentas, ou `Ctrl+Alt+K`). O painel abre à direita.
2. Na primeira vez, clique no botão de **configurações** do painel, cole a chave da API e clique em **Salvar**.
   Escolha o modelo:
   * **Claude Sonnet 5.5** (padrão) — rápido e capaz; US$ 2 / 10 por milhão de tokens (entrada / saída);
   * **Claude Opus 5.5** — o mais capaz para trabalhos longos; US$ 4 / 20;
   * **Claude Haiku 5.5** — o mais rápido e barato; a partir de US$ 0,10 / 0,50;
   * **Claude Fable 5.2** — as tarefas de pesquisa mais difíceis; US$ 8 / 40.
3. Pergunte, na sua língua. Por exemplo:
   * "Quais amostras do projeto têm cimento de calcita acima de 10 %? Faça uma tabela com a porosidade delas."
   * "Abra a ILL-TS-001, olhe a imagem e proponha a seleção, o arredondamento e os poros."
   * "Como faço um diagrama ternário da contagem de pontos?"
4. O painel mostra cada ferramenta que o Claude usou (linhas ⚙) e a resposta dele. **Parar** encerra uma vez longa;
   **Nova conversa** recomeça. Os tokens gastos aparecem abaixo do modelo.

### O Claude propõe, você decide

* **Propostas.** Quando o Claude propõe campos da descrição, uma janela os lista **desmarcados**: o campo, o valor e
  as palavras que o Claude usou. Marque o que você mesmo vê, clique em **Aplicar as marcadas** e **salve** a
  descrição como sempre. Nada é gravado antes disso.
* **Scripts.** Se você ligar **Deixar os assistentes proporem scripts** (configurações), o Claude pode escrever um script
  Python para uma tarefa; ele é mostrado numa janela e só roda quando você clica em **Rodar**. Uma descrição com
  alterações não salvas não é tocada.
* **Navegação.** O Claude pode abrir uma descrição e mostrar uma aba; ele não sai de uma descrição com alterações não
  salvas.

### O Claude Desktop trabalha no RockFace (a extensão)

1. Nas configurações do painel do Claude, clique em **Instalar no Claude Desktop…**. O RockFace grava
   `RockFace-Suite.mcpb` (na sua pasta de usuário, `.rockface/claude`), abre o arquivo e liga a janela ao vivo.
2. O Claude Desktop mostra a instalação: clique em **Install**. (Ou abra o Claude Desktop → Settings → Extensions e
   arraste o arquivo para lá.) Nas opções dela você pode escolher um **projeto** — usado quando nenhuma janela do
   RockFace está aberta — e **Deixar os assistentes proporem scripts**.
3. No Claude Desktop, pergunte como no painel: "No RockFace, o que está aberto agora?", "Olhe a imagem desta amostra
   e proponha a descrição."

Se o seu Claude Desktop não aceitar extensões, clique em **Escrever na configuração do Claude Desktop**: o RockFace
se inclui no `claude_desktop_config.json` (guardando uma cópia datada do arquivo antigo); reinicie o Claude Desktop.

### A janela ao vivo

**Deixar os assistentes de IA trabalharem nesta janela** (configurações) abre um canal só neste computador (127.0.0.1, uma porta
sorteada e um segredo num arquivo que só você pode ler). Ligado, o Claude Desktop trabalha na janela que você tem
aberta; desligado, trabalha no projeto escolhido na extensão, ou em nada. Fica ligado nas próximas sessões até você
desligar; fecha com a janela.

## Como funciona

* **Um só conjunto de ferramentas.** `search`, `table`, `ask` (a Mio), `describe`, `guide`, `write_script`,
  `api_reference`, `description_fields` e, numa janela, `window_state`, `open_description`, `show_tab`,
  `list_pictures`, `look_at` (uma imagem, ou a própria janela, reduzida a 1 568 pixels), `propose_description` e,
  quando permitido, `run_script`. No painel, o Claude as chama pela API Messages do Claude com uso de ferramentas;
  pelo Claude Desktop, pelo servidor MCP do RockFace (`rockface mcp serve --live`), que passa cada chamada à janela
  aberta.
* **As propostas usam as palavras do RockFace.** `propose_description` lê linhas "Campo: valor" com o mesmo leitor
  do ditado e do *Mio olha*; só as palavras do vocabulário do RockFace viram propostas, e elas começam desmarcadas —
  as pessoas seguem conselhos automáticos mesmo quando estão errados (viés de automação), então você decide cada
  campo.
* **Imagens.** Só as duas últimas imagens ficam na conversa; as anteriores viram uma nota, o que mantém o custo baixo.
* **Auditoria.** Cada chamada de ferramenta é gravada na auditoria do projeto, com a origem (`panel:` ou `mcp:`).
* **Nenhum pacote novo.** O painel fala com a API pelo cliente HTTP do próprio Python; a extensão é um ZIP feito no
  seu computador, apontando para o seu RockFace.

## Por script

```python
rf.claude_models()                                   # os modelos, com os preços
rf.claude_ask("Quantas amostras têm calcita?", prj)  # precisa de ANTHROPIC_API_KEY ou da chave do painel
rf.claude_extension()                                # o arquivo .mcpb para o Claude Desktop
rf.claude_desktop_config(install=True)               # ou gravar a configuração do Claude Desktop
rf.live_windows()                                    # as janelas que deixam o Claude trabalhar nelas
rf.mcp_config(live=True)                             # a entrada mcpServers para outro assistente
```

Pela linha de comando: `rockface claude extension`, `rockface claude config`, `rockface claude ask projeto.rockface
"pergunta"`, `rockface claude windows` e `rockface mcp serve --live`.

## Limites e problemas comuns

* "Ainda não há chave da API": o painel precisa de uma chave do Claude Console; o Claude Desktop, não.
* "A chave da API foi recusada" (401) ou "A chave não tem permissão para isso" (403, muitas vezes falta de crédito):
  confira a chave no Claude Console. "Pedidos demais por agora" (429) ou "O Claude está ocupado agora" (529): espere
  um pouco e pergunte de novo.
* O Claude Desktop diz que nenhuma janela do RockFace o deixa trabalhar: abra o RockFace e ligue **Deixar os assistentes de IA
  trabalharem nesta janela**, ou escolha um projeto nas opções da extensão.
* A extensão aponta para o RockFace do computador que a criou; depois de reinstalar o RockFace em outra pasta, crie-a
  de novo.
* O Claude é um modelo geral, não um petrógrafo: confira cada proposta com a imagem, como no *Mio olha*.
* Sem internet, use a Mio.

## Cobertura

O9 (o pedido do proprietário de 2026-11-18: o Claude operando o RockFace, como nos apps do Word, Excel e PowerPoint —
o painel, a janela ao vivo e a extensão do Claude Desktop juntos).

Referências: Anthropic, API Messages do Claude e uso de ferramentas, https://docs.claude.com; Model Context Protocol,
https://modelcontextprotocol.io; MCP Bundles (.mcpb), https://github.com/modelcontextprotocol/mcpb; Goddard, Roudsari &
Wyatt (2012), viés de automação, https://doi.org/10.1136/amiajnl-2011-000089.
