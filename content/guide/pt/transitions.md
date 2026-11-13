# Transições entre fases

## Para que serve

Quais minerais tocam quais: a dolomita borda os poros? O quartzo está cercado de cimento de calcita? A tabela de
transições de um mapa mineral ou de uma segmentação diz, para cada fase, como os seus pixels vizinhos se dividem entre
as outras fases. O gráfico de barras empilhadas mostra isso de relance.

## Antes de começar

Um mapa mineral ou uma segmentação de uma lâmina no RockFace Lab.

## Passo a passo

1. Abra a lâmina no RockFace Lab e vá à aba **Medidas**.
2. Em **Transições entre as fases de**, escolha o mapa e clique em **Calcular**.
3. A tabela (no lugar das classes de tamanho) tem uma coluna por fase: a % dos seus pixels vizinhos que pertencem a
   cada fase (as linhas). O gráfico mostra uma barra por fase, empilhada pelas fases que ela toca.
4. **Gráfico (PNG)** guarda o gráfico num arquivo PNG.

## Como funciona

Cada pixel é comparado com os seus 8 vizinhos sobre o mapa inteiro em resolução plena; os contatos de uma fase com ela
mesma ficam de fora; cada coluna é dividida pelo seu total (a "transition analysis" do Segment Inspector do
GeoSlicer).

## Por script

```python
seg = prj.image("ILLUSTRATIVE mosaic PP (segmentation)")
tabela = seg.transitions()                # rf.Table: "phase" e uma coluna por fase, em %
print(tabela.rows())
```

## Limites e problemas comuns

* "É preciso uma segmentação ou um mapa mineral": as transições são calculadas sobre mapas, não sobre imagens.
* As fases que não aparecem no mapa ficam de fora.

## Cobertura

GT19 (Segment Inspector: transition analysis; Charts: transition).
