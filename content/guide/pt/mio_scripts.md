# A Mio escreve scripts para tarefas repetitivas

## Para que serve

Toda tarefa que você repete — o relatório de cada descrição, a tabela de classificações de um poço, o LAS de cada
poço, as figuras de todas as amostras, um fluxo do Lab sobre todas as imagens — pode virar um **script em Python**
que roda em segundos. Você não precisa escrever o script: peça à Mio. Ela escreve o script a partir do pedido, já com
as amostras que você descreveu, e o abre na janela de scripts. Você lê, ajusta se quiser e executa. Nada roda sozinho.

## Antes de começar

* Um projeto aberto.
* Nenhum conhecimento de Python é necessário para usar o script que a Mio escreve; para mudá-lo, o guia
  [Scripts em Python](scripting.md) explica a interface de programação.

## Passo a passo

### Pedir um script

1. Abra o painel da Mio (botão Mio, ou Ctrl+Alt+M).
2. Peça com a palavra **script** (ou **automatize**, **rotina**, **python**) e diga a tarefa e as amostras:
   * `@mio escreva um script que gere o relatório em Word de cada descrição com calcita`
   * `@mio script da tabela de classificações de Folk e McBride`
   * `@mio script que exporte LAS de cada poço`
   * `@mio automatize a apresentação powerpoint das amostras com porosidade acima de 15`
   * `@mio script do diagrama ternário de Dickinson`
   * `@mio script das amostras sem porosidade`
   * `@mio script que rode o fluxo do lab em todas as imagens`
3. A Mio responde com o nome do script e as condições que leu ("amostras: diagenetic.constituent"), e o script abre
   na janela de scripts como um script novo, chamado "Mio — …".
4. Leia o cabeçalho: ele repete o pedido e diz o que mudar. A linha `CRITERIA = [...]` contém as amostras do pedido,
   como critérios do Explorer; a lista vazia quer dizer todas as descrições.
5. Clique em **Executar** (ou F5). A saída mostra cada arquivo escrito. Marque **Botão** para o script aparecer no
   menu Scripts da faixa de opções e rodar com um clique na próxima vez.

### Mudar um script

Os valores que você costuma mudar estão no topo do corpo do script: a pasta, o formato (`FMT = 'docx'`), as
classificações, as curvas do LAS, o caminho do arquivo. Mude e execute de novo. Salve o script no projeto para a
equipe usá-lo.

## Opções

As tarefas que a Mio sabe escrever (cada uma testada no projeto de exemplo):

| Tarefa | Palavras que a chamam | O que o script faz |
|---|---|---|
| Relatório de cada descrição | relatório, laudo | um PDF, Word, Excel ou HTML por descrição, numa pasta |
| Tabela de totais e classificações | classificação, totais, Folk, Dickinson, tabela | uma linha por descrição, em CSV |
| Resultado da consulta em planilha | planilha, excel, csv | a tabela de um conceito do Explorer em XLSX ou CSV |
| Arquivo LAS de cada poço | LAS, Petrel, curvas | um LAS 2.0 por poço com as curvas escolhidas |
| Páginas HTML | html, página | uma página por descrição e um índice |
| Arquivos de intercâmbio | xml, backup, cópia | um arquivo de intercâmbio por descrição |
| Apresentação PowerPoint | apresentação, powerpoint, slides | a apresentação de uma consulta |
| Diagrama ternário | ternário, diagrama | as amostras num diagrama (Folk, McBride, Dickinson…) |
| Sequência paragenética | paragênese, sequência | a figura de cada descrição |
| Contagem por poço ou fácies | conte, quantas, resumo | quantas amostras por poço (ou fácies) |
| Valores faltando | falta, sem, vazio | as descrições sem um valor (a porosidade, por padrão) |
| Fluxo do Lab | fluxo, segmentar, imagens | um fluxo em todas as imagens, tabela por amostra |
| Porosidade dos volumes | volume, micro-CT, tomografia | a porosidade de cada volume segmentado, em CSV |
| Imagens com anotações | fotos, imagens, anotações | as imagens exportadas com as anotações |

Formatos reconhecidos no pedido: PDF, Word, Excel, HTML, CSV. Classificações: Folk, McBride, Dickinson (QtFL e
QmFLt), Dunham, Embry & Klovan, Wright, Grabau, Bramkamp & Powers. Idioma do relatório: "em inglês", "em espanhol",
"em português".

## Como funciona

A Mio não inventa código. Ela escolhe a receita pelas palavras do pedido, preenche os parâmetros (formato,
classificação, arquivo) e lê as amostras pedidas com as mesmas regras da busca em linguagem natural — por isso a
linha `CRITERIA` diz exatamente o que ela entendeu. Toda receita é executada pelos testes automáticos do RockFace no
projeto ILUSTRATIVO de exemplo, de modo que o script que a Mio escreve funciona. Se nenhuma receita servir, ela diz
quais sabe escrever.

Para tarefas que as receitas não cobrem, um assistente maior ligado ao RockFace pelo [servidor MCP](mcp_server.md)
pode escrever scripts novos com a referência completa da interface de programação.

## Por script

```python
s = prj.mio_script("relatório em Word de cada descrição com calcita", lang="pt")
print(s.recipe, s.params, s.criteria)
print(s.code)                                   # o script, pronto para rodar
exec(compile(s.code, "<mio>", "exec"), {"rf": rf, "project": prj})

for r in rf.script_recipes():                   # as tarefas que a Mio sabe escrever
    print(r["key"], r["title"], r["params"])
s = prj.mio_script("tabela", recipe="table_classifications", classifications=["folk1980", "mcbride1963"])
```

## Limites e problemas comuns

* "Ainda não tenho um script para isso": a tarefa não tem receita; peça uma das tarefas da tabela ou escreva o
  script a partir de um parecido.
* Um pedido sem a palavra script vira uma pergunta comum: "relatório de cada descrição" pergunta; "script do
  relatório de cada descrição" escreve o script.
* Se a linha `CRITERIA` não tiver as amostras que você queria, corrija-a à mão ou reformule o pedido com os termos
  da nomenclatura ("com calcita", "do poço ILLUSTRATIVE-1", "porosidade acima de 15").
* Um script grava arquivos na pasta atual do programa; use caminhos completos se preferir outra pasta.

## Cobertura

Etapa 0.30 do ROADMAP (pedido do proprietário de 13/11/2026: a Mio prepara scripts Python para tarefas
repetitivas).
