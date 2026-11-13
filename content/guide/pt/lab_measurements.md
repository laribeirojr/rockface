# RockFace Lab: medidas e distribuições de tamanho

## Para que serve

A aba **Medidas** mede cada objeto de um mapa de objetos — cada grão ou poro: área, perímetro, diâmetros de Feret, a
elipse ajustada, fatores de forma, orientação, brilho e cor — e, para poros, as gargantas entre eles e o número de
coordenação. Ela dá as classes de tamanho (Udden–Wentworth para grãos, Choquette & Pray para poros), as estatísticas
de Folk & Ward, tabelas com colunas calculadas e filtros, gráficos e as exportações.

## Antes de começar

Um mapa de objetos (página [RockFace Lab: edição de mapas e objetos](lab_editing_objects.md)), de preferência com a sua escala.

## Passo a passo

### Medir

1. Abra **Medidas** e escolha o **Mapa de objetos**.
2. **Medida do tamanho** (a coluna usada para os tamanhos: diâmetro de Feret máximo, diâmetro equivalente…) e
   **Distribuição por**: **número de objetos** ou **área (como uma contagem de pontos)**.
3. **Excluir objetos cortados pela borda**; **Objetos de pelo menos** N pixels.
4. **Medir**. "N objetos medidos: …".
5. O resumo: "Tamanho: média … µm (classe); D10, D50, D90", "Folk & Ward (φ): média, seleção (classe), assimetria,
   curtose", "Forma: razão de aspecto média, circularidade média" e, para poros, "Número de coordenação médio … (N
   gargantas)".

### A tabela

* Uma linha por objeto com **Área**, **Perímetro**, **Perímetro / área**, **Diâmetro equivalente**, **Diâmetro de
  Feret máximo**, **mínimo** e **médio**, **Ângulo do Feret máximo**, **Razão de aspecto**, **Alongamento**, **Eixo
  maior** e **menor da elipse**, **Orientação (elipse)**, **Excentricidade**, **Fator de forma**, **Circularidade**,
  **Solidez**, **Convexidade**, **γ (perímetro / círculo)**, **Centro x, y** (px e mm), **Na borda**, o **Número de
  coordenação** dos poros, e o brilho e a cor da imagem sob o objeto.
* **Filtro**, por exemplo `area_um2 > 500 & aspect_ratio < 0.6`, e depois **Aplicar o filtro** ("Objetos mostrados: n
  de N").
* **Nova coluna** com uma **Fórmula**, por exemplo `feret_max_um / feret_min_um`, e depois **Adicionar a coluna**.
* A tabela pode ser ordenada, filtrada por coluna, exportada para CSV ou XLSX e mostrada como histograma.

### Classes e gráficos

1. **Classes**: **Tamanho de grão (Udden–Wentworth)** (14 classes, de argila a matacão), **Tamanho de poro (Choquette
   & Pray)** ou **Grupos de área semelhante** — com a contagem, a % em número e a % em área de cada uma.
2. Gráfico: **Histograma de tamanhos (φ)** com a sua curva acumulada, **Gráfico cruzado com histogramas**, **Diagrama
   de roseta das orientações**, **Classes de tamanho**, ou **Transições entre fases (barras empilhadas)** (página
   [Transições entre fases](transitions.md)). **Desenhar o gráfico**; grave-o em PNG.
3. Exporte as tabelas (CSV, XLSX) e os objetos em cores (PNG).

## Opções

| Opção | O que muda |
|---|---|
| Medida do tamanho | O diâmetro usado para as classes e estatísticas. |
| Distribuição por área | Cada objeto pesa pela sua área, como numa contagem de pontos. |
| Excluir objetos cortados pela borda | Objetos que tocam a borda da imagem não são contados. |

## Como funciona

* Perímetro pela fórmula de Crofton; diâmetros de Feret a partir do fecho convexo do contorno subpixel; a elipse dos
  mesmos momentos de segunda ordem; fatores de forma segundo a ISO 9276-6.
* Gargantas: o comprimento da fronteira entre dois poros que se tocam; o número de coordenação é o número de poros que
  cada um toca.
* Conferido em formas de tamanho conhecido em posições e ângulos aleatórios: a partir de 20 px, área, perímetro,
  diâmetros de Feret e elipse dentro de cerca de 2 %, orientação dentro de uma fração de grau; coordenação 4 e 6 em
  empacotamentos quadrado e hexagonal; as medidas de Folk & Ward de 517 discos de uma lei log-normal conhecida iguais
  às dos diâmetros sorteados.

## Por script

```python
grains = prj.image("ILLUSTRATIVE mosaic PP").segment("resin").objects(2, "watershed", min_px=40)
m = grains.measure()
print(m.summary(exclude_edge=True))                       # Folk & Ward, D10/D50/D90, forma, coordenação
t = m.table.filter("touches_edge == 0")
t.add_column("ratio", "feret_max_um / feret_min_um")
print(rf.measure.class_table(t, "feret_max_um", "wentworth"))
rf.measure.chart("rose", t, "orientacoes.png", x="ellipse_angle")
rf.measure.to_xlsx("graos.xlsx", {"graos": t})
```

## Limites e problemas comuns

* "O mapa não tem escala: os comprimentos estão em pixels." — dê a escala da imagem no Atlas.
* Objetos de um ou dois pixels têm formas sem sentido: aumente **Objetos de pelo menos**.
* O perímetro de Crofton fica 5–7 % abaixo em lados retos longos.

## Cobertura

GT11 (medidas por objeto), GT12 (gargantas 2D e coordenação), GT13 (classes de tamanho; grupos por área semelhante),
GT14 (saídas: tabelas XLSX, objetos coloridos), GT19 (tabelas, filtro, gráficos).
