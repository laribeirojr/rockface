# Ferramentas de volume: filtros, sombreamento, efeitos do editor de segmentos, objetos, registro, análises

## Para que serve

As ferramentas do RockFace MC que preparam um volume de micro-CT, corrigem a sua segmentação e o medem: um filtro que
preserva as bordas, a correção do sombreamento (endurecimento do feixe), os efeitos de um editor de segmentos, a
separação do espaço poroso em objetos, o registro de duas aquisições giradas uma em relação à outra, e o variograma,
o volume elementar representativo e os atributos de um volume.

## Antes de começar

Um volume aberto no RockFace MC. Cada ferramenta grava um volume **novo**; o original nunca é alterado.

## Passo a passo

### Difusão anisotrópica (aba Volume)

1. Em **Volume → Filtros**, escolha **Difusão anisotrópica (preserva bordas)**.
2. Ajuste **Condutância** (menor preserva mais bordas) e **Iterações** (mais suaviza mais), clique em **Adicionar** e
   depois em **Aplicar**.

### Correção de sombreamento (aba Volume)

1. **Correção de sombreamento (corte a corte)**: escolha onde o fundo é ajustado — **O corte inteiro**, o cilindro do
   plugue ou o interior de um volume segmentado.
2. Opcional: **Suavização entre cortes** (em cortes).
3. Clique em **Corrigir o sombreamento**.

### Efeitos sobre o volume segmentado (aba Segmentação)

Abra um volume segmentado. Em **Efeitos sobre o volume segmentado**, escolha o **Efeito**, o **Segmento** e, quando
pedido, o **Outro segmento**, **Voxels / tamanho / tolerância** ou **Região ou volume cinza**, e clique em **Aplicar
o efeito (volume novo)**:

* **Margem** aumenta (voxels positivos) ou encolhe (negativos) um segmento;
* **Suavização** tira a aspereza de um segmento;
* **Ilhas** remove as peças menores que o tamanho dado;
* **Operadores lógicos** somam, subtraem, intersectam, copiam, invertem ou limpam segmentos;
* **Máscara** mantém só o que está dentro de outro volume segmentado;
* **Expandir segmentos** preenche os voxels em 0 com o segmento mais próximo;
* **Remover bordas** esvazia os voxels onde dois segmentos se tocam;
* **Crescer a partir de sementes** faz crescer os voxels pintados de uma anotação sobre um volume cinza;
* **Traçado de nível a partir da cruz** pega os voxels conectados de um volume cinza próximos do valor sob a cruz.

### Objetos do espaço poroso (aba Análises)

1. Abra um volume segmentado. Em **Objetos do espaço poroso**, escolha **Separados por**: *Watershed do mapa de
   distâncias* (poros que se tocam são separados) ou *Peças conectadas*.
2. Ajuste **Distância mínima entre centros** e **Menor objeto**, e clique em **Separar em objetos**.
3. A tabela lista cada objeto: voxels, volume, diâmetro equivalente, eixos, centroide, o raio da maior esfera inscrita
   e se ele toca a borda.

### Registro com rotação (aba Registro)

Escolha os volumes **Fixo** e **Móvel**, marque **Encontrar também a rotação (sem pontos de controle)** e clique em
**Encontrar o deslocamento (correlação de fase 3D)**. A rotação (em torno de x, y, z) e o deslocamento ficam guardados
no volume móvel; **Reamostrar o volume móvel sobre o fixo** grava-o na grade do fixo.

### Variograma, VER e atributos (aba Análises)

* **Variograma (x, y, z, todas as direções)**: o semivariograma de um volume cinza, ou dos poros de um segmentado,
  com o modelo ajustado (alcance, patamar, efeito pepita) na tabela.
* **Volume elementar representativo**: o desvio padrão da média de cubos aleatórios de aresta crescente; o VER é onde
  a curva se estabiliza.
* **Relatório (HTML)…** grava os gráficos e as tabelas numa página.
* **Mostrar os atributos** lista tamanho, voxel, valores, histórico; **Importar um arquivo PCR…** acrescenta os
  parâmetros de reconstrução do tomógrafo (o mínimo e o máximo da escala de cinza).

A **Tabela** da aba é filtrada por uma expressão (`voxels > 100 and not border`), exportada para CSV ou Excel, e
mostra o histograma da coluna escolhida.

## Como funciona

* Difusão anisotrópica: Perona & Malik (1990); a condutância é escalada pela raiz da média quadrática do gradiente,
  como na difusão anisotrópica do ITK. Calculada bloco a bloco, igual ao volume inteiro.
* Sombreamento: em cada corte, um polinômio de segundo grau f(x, y) é ajustado a pontos aleatórios da máscara e o
  corte passa a s / f · M (M a média da máscara).
* Objetos: o watershed (Vincent & Soille 1991) do mapa de distâncias suavizado, um marcador por máximo local.
* Rotação: uma busca do ângulo em torno de z com a correlação de fase 3D do deslocamento, e depois os seis parâmetros
  refinados pela correlação cruzada normalizada.
* Variograma: Matheron (1963); modelo esférico; com uma região, só contam os pares com as duas pontas dentro dela.

## Por script

```python
vol = prj.volume("Plugue A")
suave = vol.filter(("anisotropic", {"conductance": 1.0, "iterations": 5}))
plano = vol.shading_correction("cylinder")
seg = plano.segment()
objetos = seg.partition(min_distance=4)
linhas = objetos.objects()
t = prj.volume("Plugue A, segunda aquisição").register_rigid(vol)
v = seg.variogram()
seg.variogram_report("variograma.html")
maior = seg.edit("margin", segment=1, voxels=2)
```

## Limites e problemas comuns

* Os efeitos e os objetos trabalham com o volume inteiro na memória: acima de 64 milhões de voxels, trabalham num
  nível reduzido do volume.
* A busca da rotação supõe o mesmo tamanho de voxel nos dois volumes.
* Os atributos de Gabor, de Minkowski e do alcance do variograma do segmentador do GeoSlicer não são oferecidos.

## Cobertura

GV4, GV6, GV7, GV14 (Filters, Polynomial Shading Correction, Segment Editor, Segment Inspector, Register, Variogram
Analysis, Attribute Tools, Tables).
