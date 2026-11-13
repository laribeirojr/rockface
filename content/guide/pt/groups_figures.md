# Grupos, figuras e apresentações

## Para que serve

O RockFace Explorer desenha vários **grupos** de amostras juntos numa classificação ternária — as amostras de cada poço
no QFR de Folk, cada fácies no QtFL de Dickinson — com os seus símbolos e cores. O seu **gerador de figuras** faz
figuras de publicação a partir de qualquer atributo da coleção (gráficos cruzados, histogramas, barras, diagramas de
caixa, curvas contra a profundidade por poço, diagramas ternários), no tamanho de uma revista, e as exporta também
como projeto do SciVelyx Graphs. Uma **apresentação** reúne figuras, tabelas e galerias de imagens num arquivo do
PowerPoint.

## Antes de começar

Um projeto com descrições; consultas salvas ajudam (página [RockFace Explorer: consultas, tabelas de resultados e exportações](explorer_queries.md)).

## Passo a passo

### Grupos numa classificação ternária

1. Abra a aba **Grupos** do Explorer.
2. **Método de classificação**: a **Classificação ternária** (Folk 1980, McBride 1963, Dickinson QtFL e QmFLt, ou uma
   do projeto) e, se quiser, **Composição original (restaurada)**.
3. **Adicionar grupo** (até dez). Para cada grupo, em **Grupos de descrições**:
   * as descrições: **Consulta da aba Consulta**, **Critérios do grupo** ou uma consulta salva; **Escolhidas à mão**
     acrescenta outras ("As encontradas pela consulta são fixas; marque outras para adicioná-las à mão");
   * **Símbolo do ponto**, **Cor de preenchimento**, **Cor da borda**; **Mostrar o grupo**; **Remover o grupo**.
4. **Classificar** desenha todos os grupos, com a legenda. "N pontos em G grupos; M descrições sem ponto nesta
   classificação."
5. No diagrama: **Tamanho do ponto**, **Sem cores**, **Nomes de todos os pontos (ou clique num ponto)**, **Aproximar**,
   **Afastar**; a caixa sob o mouse dá o nome e os valores dos vértices; "Campo sob o ponteiro: …".
6. **Exportar imagem…**; **Salvar grupos…** e **Abrir grupos…** guardam os conjuntos no projeto.

### Uma figura

1. Abra a aba **Figuras**.
2. **Tipo**: **Gráfico cruzado**, **Histograma**, **Barras (número de amostras)**, **Diagrama de caixa por
   categoria**, **Contra a profundidade, por poço** ou **Ternário com grupos**.
3. **Atributo (X)** e **Atributo (Y)** — qualquer atributo de qualquer conceito (por exemplo Petrofísica › Porosidade,
   Totais › Qt); **Cor por** um atributo ou **Grupos (aba Grupos)**; **Classes** para histogramas; **Profundidade**
   (medida, corrigida, ajustada) para curvas contra a profundidade.
4. **X logarítmico**, **Y logarítmico**, **Nomes das amostras**, **Legenda**, **Só as descrições da consulta**.
5. **Título**; **Tamanho de revista** (Nature, Elsevier, AAPG, ACS uma ou duas colunas, um slide 16:9) ou **Tamanho
   livre** com **Largura (mm)**, **Altura (mm)** e **Tamanho da fonte (pt)**.
6. **Exportar…** grava PNG, TIFF, JPEG, SVG, PDF, os dados plotados em CSV, ou um projeto do SciVelyx Graphs
   (`.scivelyx.json`) para terminar a figura lá.
7. **Salvar figura…** a guarda no projeto; **Abrir figura…** desenha de novo uma figura salva com os registros mais
   recentes.

### Uma apresentação

1. Em **Apresentação**, acrescente slides: **+ Figura** (a figura mostrada), **+ Tabela** (a tabela de resultados de
   um conceito), **+ Imagens** (uma galeria das lâminas).
2. **Gravar apresentação (.pptx)…**. A apresentação é 16:9 e abre com um slide de título e os critérios da consulta.
3. Ou, na aba Consulta, **Exportar → Apresentação da consulta (.pptx)…** grava uma de uma vez.

## Opções

| Opção | O que muda |
|---|---|
| Composição original (restaurada) | Os grupos são posicionados com a composição antes da diagênese. |
| Tamanho de revista | Largura, altura e fontes da coluna da revista (ou de um slide). |
| Quando uma descrição tem várias linhas | Usa-se a média, exceto quando X e Y são do mesmo conceito (um ponto por linha). |

## Como funciona

Grupos e figuras são recalculados a partir das descrições salvas cada vez que são desenhados; assim, uma figura salva
mostra sempre os dados mais recentes. As figuras são desenhadas com o Matplotlib a 600 dpi por padrão; o projeto do
SciVelyx Graphs leva os mesmos dados e estilos, e a figura pode ser terminada no SciVelyx Graphs.

## Por script

```python
wells = [rf.Group(w, rf.Query([rf.Criterion("identification", "well", [w])])) for w in ("ILLUSTRATIVE-A1", "ILLUSTRATIVE-A2")]
prj.figure("qfr.pdf", kind="ternary", scheme="folk1980", groups=wells, colour_by="groups")
phik = prj.figure("phi_k.png", kind="crossplot", x="petrophysics.porosity", y="petrophysics.permeability",
                  log_y=True, colour_by="identification.facies", preset="elsevier-1col")
prj.figure("phi_k.scivelyx.json", phik)                      # abrir no SciVelyx Graphs
prj.save_figure("Porosidade e permeabilidade", phik)
prj.presentation("barita.pptx", ("diagenetic", "constituent", "barite"), figures_=[phik])
```

## Limites e problemas comuns

* "No máximo 10 grupos."
* "Ainda não há figuras salvas neste projeto." / "Ainda não há grupos salvos neste projeto."
* "Adicione slides primeiro." — uma apresentação precisa de pelo menos um slide.
* As apresentações do PowerPoint precisam do extra `explorer` (python-pptx), instalado com `.[all]`.

## Cobertura

M1 (até 10 grupos a partir de consultas salvas), M2 (símbolo, cor de preenchimento e de borda por grupo), M3 (métodos
de classificação recalculados com os dados mais recentes), M4 (legenda, caixa sob o mouse, rótulos, zoom,
exportação), L5 (gerador de figuras e apresentações).
