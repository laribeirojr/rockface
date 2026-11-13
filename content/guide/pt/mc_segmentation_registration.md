# RockFace MC: segmentação, porosidade e registro de volumes

## Para que serve

A aba **Segmentação** corta os níveis de cinza de um volume de micro-CT em segmentos — poro e sólido, ou mais fases —
por cortes digitados ou pelo método de Otsu, limitada ao cilindro de um plugue quando preciso, e mede a porosidade, o
seu perfil ao longo de um eixo, a conectividade do espaço poroso e a sua correlação de dois pontos. A aba **Registro**
alinha dois volumes da mesma amostra e encontra onde uma imagem de lâmina fica num volume, acrescentando a fatia
correspondente à lâmina.

## Antes de começar

Um volume no RockFace MC (página [RockFace MC: volumes de micro-CT — importação, vistas e processamento](mc_volumes.md)), filtrado se tiver ruído.

## Passo a passo

### Segmentar

1. Abra **Segmentação** e selecione o volume de cinza.
2. **Cortes**: digite-os, ou deixe vazio para Otsu (**vazio: Otsu**); **Segmentos (Otsu)** dá o número de segmentos;
   **Encontrar os cortes (Otsu)** os mostra no histograma.
3. **Região**: o **volume inteiro**, o **cilindro do plugue** (achado automaticamente), ou **dentro de** outro volume
   segmentado.
4. **Segmentar**. "Segmentado: porosidade … %." O segmento mais escuro é o poro. O volume segmentado aparece sob a
   amostra e pode ser posto sobre o de cinza com **Sobrepor**.

### Análises do volume segmentado

* **Porosidade** — a porosidade da região, e a porosidade de cada fatia ao longo de um eixo (**fatia ao longo de x,
  y, z**).
* **Conectividade** — ao longo de um eixo: porosidade conectada e isolada, o número de grupos de poros, e se o espaço
  poroso atravessa o volume.
* **Dois pontos** — a correlação de dois pontos dos poros ao longo de x, y e z, e o comprimento de correlação de cada
  um.

Os efeitos sobre os segmentos (crescer, encolher, suavizar, operações lógicas com outro segmento) estão em **Efeitos
sobre o volume segmentado** (página [Ferramentas de volume: filtros, sombreamento, efeitos do editor de segmentos, objetos, registro, análises](volume_tools.md)).

### Registrar dois volumes

1. Abra **Registro**. Em **Dois volumes da amostra**, escolha o volume **Fixo** e o **Móvel**.
2. **Encontrar o deslocamento (correlação de fase 3D)**: "Deslocamento encontrado: x, y, z voxels", guardado no volume
   móvel. Marque **Encontrar também a rotação (sem pontos de controle)** para um escaneamento girado (página
   [Ferramentas de volume: filtros, sombreamento, efeitos do editor de segmentos, objetos, registro, análises](volume_tools.md)).
3. **Reamostrar o volume móvel sobre o fixo** o grava na malha fixa, voxel a voxel.

### Uma imagem de lâmina no volume

1. Em **Uma imagem de lâmina no volume**, escolha a **Imagem** (uma foto ou lâmina de uma das lâminas da amostra) e
   **Fatias segundo** (o eixo).
2. **Localizar a imagem**. O RockFace procura a fatia que mostra a imagem, com a sua rotação, escala e deslocamento:
   "Fatia z = …; rotação …°, … voxels por pixel; ECC …".
3. **Adicionar a fatia à lâmina**: a fatia do volume é acrescentada às imagens da lâmina no Atlas, sobreposta à imagem
   — a ligação entre a lâmina e a tomografia.

## Opções

| Opção | O que muda |
|---|---|
| Cortes / Segmentos (Otsu) | Onde os níveis de cinza são cortados, digitados ou por Otsu de vários níveis. |
| Região | Volume inteiro, o cilindro do plugue, ou dentro de um volume segmentado. |
| Fatias segundo | O eixo segundo o qual a lâmina foi cortada do plugue. |

## Como funciona

* A porosidade do arenito Berea do Imperial College London (400³ voxels, 5,345 µm) é 19,645 % contra os 19,6 %
  publicados; um escaneamento cinza simulado a partir dele e segmentado por Otsu deu 19,54–21,06 %.
* O deslocamento entre dois volumes é achado pela correlação de fase 3D (um deslocamento conhecido achado exatamente);
  os pontos de controle ajustam uma transformação rígida, de similaridade ou afim.
* Uma imagem de lâmina é localizada por uma busca de fatia, ângulo e escala, refinada pelo coeficiente de correlação
  melhorado: imagens de uma fatia em outros tamanhos de pixel e ângulos (20° a 137°) foram postas na fatia certa
  dentro de 0,01–0,83 voxel.

## Por script

```python
ct = prj.volume("ILLUSTRATIVE plug")
pores = ct.filter(("median", {"size": 3})).segment(roi="cylinder")          # Otsu, dois segmentos
print(pores.porosity()["porosity"], pores.connectivity("z")["percolates"])
print(pores.profile("z")[:5], pores.two_point()["length_x"])
other = prj.volume("ILLUSTRATIVE plug, second scan")
other.register(ct)                                                           # o deslocamento automático
aligned = other.resample_on(ct)
found = prj["TS-9"].images("photo")[0].locate_in(ct, axis="z", add_slice=True)
```

## Limites e problemas comuns

* "Escolha dois volumes diferentes."
* Uma imagem de lâmina só é achada se o volume contém aquela fatia: dê o eixo segundo o qual a lâmina foi cortada.
* O cilindro de um plugue é achado pelo ar em volta dele: num recorte sem ar, use o volume inteiro ou uma região.

## Cobertura

GV6 (segmentação), GV7 (registro), L2 (ligações das amostras com a tomografia), L13 em parte (imagem 2D →
tomografia).
