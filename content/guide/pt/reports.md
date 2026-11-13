# Relatórios

## Para que serve

Um **relatório** escreve uma ou muitas descrições como documento: PDF para imprimir ou arquivar, Word (DOCX) ou Excel
(XLSX) para editar, ou páginas HTML para ler num navegador — em inglês, espanhol ou português, qualquer que seja o
idioma da interface. Ele contém as seções que você escolher: identificação, descrição, composição, totais,
classificações com os diagramas ternários, diagênese com o gráfico paragenético, análises, solicitações, as imagens
da lâmina e as suas análises pontuais.

## Antes de começar

As descrições salvas: as mudanças não salvas não entram no relatório.

## Passo a passo

1. **Início → Relatórios e intercâmbio → Relatório…** (Ctrl+P).
2. **Descrições**: marque as que vão no relatório (**Todas**, **Nenhuma**). A descrição aberta vem marcada.
3. **Formato**: PDF, Word, Excel ou HTML.
4. **Idioma do relatório**: English, Español ou Português.
5. **Seções**: Identificação, Macroscópica, Microscópica, Sistema poroso, Composição, Totais, Classificações,
   Diagênese, Análises, Solicitações, Imagens da lâmina, Análises pontuais.
6. Diagramação:
   * **Largura das imagens (mm)** e **Largura dos diagramas ternários (mm)**;
   * **Figuras**: **Nas suas seções** ou **Todas no fim**;
   * **Também a composição original (antes da diagênese)**.
7. Para HTML, marque **HTML: uma página por descrição, com uma página de índice** e escolha a **Pasta para as páginas
   HTML**: cada descrição ganha a sua página, e `index.html` liga todas.
8. **Abrir o arquivo ao terminar** e depois **Gerar relatório…**, escolhendo onde gravá-lo.

"Os arquivos Word, Excel e HTML podem ser editados depois de exportados."

## Opções

| Opção | O que muda |
|---|---|
| Formato | PDF (A4), DOCX, XLSX (uma folha com a lista das descrições e uma folha por descrição) ou HTML. |
| Idioma do relatório | Independente do idioma da interface. |
| Seções | Só as seções marcadas são escritas. |
| Largura das imagens / dos diagramas ternários | Tamanho das figuras no documento, em mm. |
| Figuras | Dentro das suas seções, ou todas reunidas no fim. |
| Composição original | Acrescenta a composição antes da diagênese, com os seus totais e classificações. |

## Como funciona

O relatório é montado a partir dos mesmos registros que os formulários mostram (os códigos traduzidos para o idioma do
relatório); os números são escritos com o separador decimal desse idioma. Os diagramas ternários e o gráfico
paragenético são desenhados como no programa. O Explorer gera relatórios das descrições achadas por uma consulta pelo
mesmo diálogo (página [RockFace Explorer: consultas, tabelas de resultados e exportações](explorer_queries.md)).

## Por script

```python
with rf.open("estudo.rockface") as prj:
    prj["TS-9"].report("TS-9.pdf", lang="pt")
    prj.report("poco-1.docx", names=["TS-9", "TS-10"], lang="en",
               sections=["identification", "composition", "classification"], figure_mm=120, figures="end")
    prj.html_pages("site", lang="es")                  # uma página por descrição e index.html
```

## Limites e problemas comuns

* "Nenhuma descrição escolhida."
* Word e Excel precisam do extra `reports` (python-docx, openpyxl), instalado com `.[all]`.
* Imagens de lâminas inteiras muito grandes são escritas reduzidas à largura de imagem escolhida.

## Cobertura

P10 (relatórios em inglês, português e espanhol), P34 (relatórios: PDF, Excel, HTML, Word; idioma; configuração),
P36 (gerador de HTML em lote).
