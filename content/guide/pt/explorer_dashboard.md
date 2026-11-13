# RockFace Explorer: o painel de uma coleção

## Para que serve

A aba **Painel** mostra uma coleção de relance: as amostras por fácies, a porosidade contra a permeabilidade, a
densidade de grão, as profundidades amostradas em cada poço, os tipos de amostra e galerias das imagens (mosaicos PP e
XP, lâminas de scanner, fotos de detalhe, mapas mineralógicos). Filtros por campo, formação, zona, poço, fácies e
categoria de imagem estreitam todos os gráficos de uma vez.

## Antes de começar

Um projeto com descrições, de preferência com petrofísica (aba Análises, página [Análises e solicitações de análise](analyses_requests.md)) e imagens
(RockFace Atlas).

## Passo a passo

1. No RockFace Explorer, abra a aba **Painel**.
2. Os gráficos:
   * **Amostras por fácies (clique para filtrar)** — um mapa de árvore; clique numa fácies para ficar só com ela;
   * **Porosidade × permeabilidade (mD)** — um ponto por amostra, colorido pela fácies, permeabilidade em eixo
     logarítmico;
   * **Densidade de grão** — um histograma;
   * **Profundidades por poço** — as profundidades **Medida (topo)**, **Corrigida** e **Ajustada** das amostras de
     cada poço;
   * **Tipos de amostra** — plugues, testemunhos inteiros, amostras laterais, amostras de calha, amostras de
     afloramento.
3. **Filtros**: marque valores de **Campo**, **Formação**, **Zona**, **Poço**, **Fácies** e **Categoria de imagem**;
   todos os gráficos e galerias acompanham. "N de M amostras". **Limpar filtros** os remove.
4. **Só as descrições da consulta** limita o painel às descrições encontradas na aba Consulta.
5. **Galerias**: **Mosaico PP**, **Mosaico XP**, **Scanner**, **Fotos de detalhe**, **Mineralogia (mapas)**. Clique duas
   vezes numa imagem para abri-la no RockFace Atlas.

## Opções

| Opção | O que muda |
|---|---|
| Filtros | Todos os gráficos e galerias mostram só as amostras que correspondem. |
| Só as descrições da consulta | O painel do resultado da consulta. |

## Como funciona

O painel lê os mesmos fatos que as consultas: a petrofísica vem das análises de petrofísica convencional de cada
amostra; a fácies, o campo, a formação, a zona e o poço, da identificação; as galerias, das imagens Atlas de cada
lâmina (por categoria e luz). O mapa de árvore é "squarified" (a área de cada retângulo é o número de amostras).

## Por script

```python
board = prj.dashboard(field="Example Field A")
print(board.facies())                    # amostras por fácies
for phi, k, facies, did in board.phi_k():
    print(phi, k, facies)
print(board.grain_density(10), board.depths(), board.sample_types())
print(board.gallery("mosaic_pp"))        # ids das imagens
```

## Limites e problemas comuns

* "Sem dados para as descrições mostradas." — nenhuma petrofísica ou nenhuma imagem entre as amostras filtradas.
* Uma amostra sem fácies aparece sob "—".

## Cobertura

L1 (painéis), Q2 (conceitos de petrofísica na coleção).
