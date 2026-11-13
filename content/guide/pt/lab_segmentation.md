# RockFace Lab: segmentação e porosidade

## Para que serve

A **segmentação** separa os pixels de uma imagem de lâmina em segmentos — poro, grãos, cimento, matriz… — e guarda o
resultado como um **mapa** sobre a imagem. O seu segmento de poro dá a **porosidade**. O RockFace Lab oferece os
métodos clássicos: a resina azul, limiares de um canal (também Otsu de vários níveis), uma faixa de cor, um
classificador bayesiano aprendido de amostras desenhadas na imagem, k-médias (também sobre superpixels), sementes que
crescem por watershed, e uma floresta aleatória treinada com exemplos pintados.

## Antes de começar

Uma imagem da lâmina no RockFace Lab, de preferência recortada e filtrada (página [RockFace Lab: recorte, filtros e a máscara da amostra](lab_preparation.md)). Uma máscara da
amostra limita a segmentação à rocha.

## Passo a passo

1. Abra a aba **Segmentação** e selecione uma imagem (não um mapa).
2. **Método**:
   * **Resina azul (poro / sólido)** — a resina epóxi azul é poro. Em CIELAB a resina é achada pelo seu azul (b*), com
     o corte escolhido automaticamente (Otsu) ou digitado, e o **Croma mínimo**; ou pelo **Ângulo de matiz CIELAB**. A
     resina pode ser separada pela claridade: **não: toda a resina é poro**, **poro aberto = resina clara (Otsu)**, ou
     **poro aberto = L* no mínimo…** — a parte escura, tingida pela resina, é então microporosidade.
   * **Limiares de um canal** — escolha o **Canal** (luminância, vermelho, verde, azul, matiz, saturação e valor HSV,
     L*, a*, b*, croma e ângulo de matiz CIELAB) e os cortes; vazio: automático (Otsu de vários níveis).
   * **Faixa de cor (HSV)** — as faixas de matiz, saturação e valor de um segmento.
   * **Classificador bayesiano (amostras)** — **Desenhar uma amostra do segmento escolhido** para cada segmento (pelo
     menos 8 pixels cada); o classificador aprende as suas cores.
   * **K-médias (não supervisionado)** — o número de **Grupos**, sobre pixels ou sobre **Superpixels**.
   * **Crescer a partir de sementes (watershed)** — **Pintar sementes do segmento escolhido** com o **Raio do pincel**.
   * **Floresta aleatória (exemplos pintados)** — página [Segmentar por exemplos pintados (floresta aleatória)](random_forest.md).
3. **Segmentos**: **Adicionar segmento**, **Remover segmento**; cada um com o seu nome, cor e **Papel** (poro, sólido,
   não classificado).
4. Região: a imagem inteira, ou uma máscara da amostra.
5. **Segmentar**. A pré-visualização mostra o mapa sobre a imagem e a "Parte da área contada" de cada segmento, a
   **Porosidade (poro / poro + sólido)** e os limiares usados.
6. Limpe o mapa: **Ilhas menores que** (pixels dados à vizinhança) e **Suavização (maioria)**.
7. **Nome do mapa** e depois **Guardar a segmentação como mapa**. "Segmentação guardada: … (porosidade … %)."

O mapa pode ser corrigido à mão e separado em objetos (página [RockFace Lab: edição de mapas e objetos](lab_editing_objects.md)), e depois medido (página
[RockFace Lab: medidas e distribuições de tamanho](lab_measurements.md)).

## Opções

| Opção | O que muda |
|---|---|
| Resina azul — a separação por L* | Toda a resina é poro, ou só a resina clara (poro aberto); a resina escura é microporosidade. |
| Canal, cortes | Qual canal é cortado, e onde (vazio: Otsu). |
| Superpixels (k-médias) | Agrupar superpixels SLIC em vez de pixels: segmentos mais suaves. |
| Papel | Poro e sólido fazem a porosidade; não classificado fica fora dela. |

## Como funciona

* As cores são convertidas para CIELAB (dentro de 0,0049 do scikit-image em 100 000 cores) e para HSV; são oferecidos
  12 canais.
* Em três lâminas ILUSTRATIVAS de verdade exata (22,3–25,6 % de porosidade), a resina azul, o Otsu de b* e o
  classificador bayesiano foram exatos em imagens limpas e ficaram dentro de 0,5 ponto (IoU ≥ 0,95) com desfoque,
  ruído e resina mais fina juntos.
* Nas 20 lâminas carbonáticas do GO-Forward D2.1 (CC BY 4.0), cujos valores publicados são a porosidade aberta de uma
  segmentação SLIC + k-médias, a resina por ângulo de matiz com a separação por L* acompanha esses valores com
  correlação de 0,97; contar toda a resina dá a porosidade óptica total.
* O mapa é uma imagem em blocos como as outras, no sistema da lâmina, e por isso se sobrepõe a todas as imagens da
  lâmina no Atlas e no Lab.

## Por script

```python
pp = prj.image("ILLUSTRATIVE mosaic PP")
seg = pp.segment("resin", post=[("islands", {"min_px": 20})])
print(f"porosidade {seg.porosity():.2f} %")
km = pp.segment("kmeans", k=4, superpixels=5000, save=False)          # uma olhada, nada é gravado
otsu = pp.segment("thresholds", channel="b", classes=3, name="Otsu de b*")
```

## Limites e problemas comuns

* "Escolha uma imagem da lâmina (não um mapa) para segmentar."
* "Desenhe uma amostra (de pelo menos 8 pixels) de cada segmento." / "Pinte sementes de pelo menos um segmento."
* A pré-visualização é calculada num nível reduzido em imagens grandes ("Calculado no nível …"); o mapa guardado está
  em resolução plena.
* Lâminas sem resina azul: use limiares, uma faixa de cor, o classificador ou a floresta aleatória.

## Cobertura

GT7 (segmentação manual e por limiares), GT8 (poro / não poro por inferência bayesiana), L7 em parte (quantificação da
lâmina inteira, clássica).
