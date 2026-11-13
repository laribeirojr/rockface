# RockFace Atlas: lâminas inteiras, fotos de detalhe e a biblioteca de imagens

## Para que serve

O RockFace Atlas guarda as imagens de cada lâmina: imagens da lâmina inteira de qualquer tamanho (a lâmina de vários
gigapixels de um scanner, um mosaico de microscópio) em várias luzes, e fotos de detalhe colocadas na sua posição
exata na lâmina, com a posição da platina onde foram tiradas. A **biblioteca de imagens** encontra qualquer imagem do
projeto pelo nome, legenda, poço, lâmina, tipo, luz ou objetiva, e o visualizador vai da lâmina inteira à resolução
plena na hora.

## Antes de começar

* Uma descrição **salva**: as imagens pertencem à sua lâmina ("Salve primeiro uma descrição: as imagens pertencem à
  sua lâmina.").
* Arquivos de imagem: PNG, JPEG, TIFF, BigTIFF, OME-TIFF, BMP, GIF, WebP; formatos de scanner (SVS, NDPI, MRXS, SCN)
  com o OpenSlide instalado; Zeiss CZI com o extra `czi`.

## Passo a passo

### Abrir o Atlas

**Início → Imagens → Atlas** (Ctrl+Shift+A) no RockFace Petro abre o Atlas no mesmo projeto e lâmina; ou
`rockface atlas projeto.rockface`.

### Importar uma lâmina inteira

1. **Importar…** (Ctrl+I) e escolha os arquivos.
2. Em **Importar imagens**, confira a **Lâmina delgada**, o **Tipo** (lâmina inteira), a **Categoria** (mosaico de
   microscópio, scanner de lâminas, fotomicrografia, foto macroscópica, outro) e a **Luz / sinal** (luz polarizada
   plana, nicóis cruzados, luz refletida, catodoluminescência, ultravioleta, fluorescência, MEV, outro).
3. Escala: **µm por pixel** — do arquivo quando ele a traz, senão digitada, senão da **Objetiva** e da tabela de
   **Objetivas…**.
4. **Blocos**: **JPEG (fotografias; menor)** ou **PNG (sem perda; mapas)**.
5. **OK**. "Construindo a pirâmide da imagem…" mostra o progresso; uma imagem muito grande demora, uma vez só.

### Fotos de detalhe

1. **Foto de detalhe…**: escolha a foto, a sua **Objetiva**, a luz e, quando conhecidas, a sua **Posição x, y (mm)**
   na lâmina e a **Platina x, y (mm)** onde foi tirada.
2. Ou posicione-a depois: selecione-a em **Fotos de detalhe**, escolha a ferramenta **Posicionar foto** e clique onde
   ela fica na lâmina inteira.
3. **Mostrar na lâmina** enquadra o campo da foto; **Abrir** mostra a própria foto; **Platina a este campo** manda a
   platina (ou o simulador) de volta para onde ela foi tirada.
4. **Fotografar de novo…** acrescenta uma nova foto do mesmo campo, com a mesma posição, posição de platina e
   objetiva, ligada à primeira ("N fotos deste campo").

### O visualizador

* Arraste para mover; a roda do mouse aproxima e afasta. **Ajustar**, **1:1**, **Aproximar**, **Afastar**.
* **Por cima:** sobrepõe outra imagem da lâmina à imagem aberta (XP sobre PP, CL, um mapa mineralógico), com a
  **Opacidade da imagem sobreposta**.
* Mostre ou esconda as **Fotos** (os campos das fotos de detalhe, numerados), a **Escala**, a **Visão geral** e o
  contorno da **Lâmina redonda**.
* **Pontos contados de:** mostra os pontos contados numa descrição, coloridos por constituinte (página
  [Contagem de pontos](point_counting.md)).
* **Ferramentas**: **Medir** (clique em dois pontos: a distância em µm), **Calibrar** (clique em dois pontos e dê a
  sua distância: define a escala), **Posicionar foto**, **Ponto** (página [Análises pontuais: geoquímica, datação e inclusões fluidas](spot_analyses.md)).
* **Exportar vista…** grava o que é mostrado, ou a imagem inteira, em PNG, JPEG ou TIFF.

### A biblioteca de imagens

1. A **Biblioteca de imagens** lista todas as imagens do projeto. Digite em **Buscar nomes, legendas, poços,
   lâminas…**.
2. **Filtros**: tipo, categoria, luz, objetiva e **Poço ou afloramento**; **Só esta lâmina**.
3. **Por conceito** encontra imagens pelo que as suas anotações mostram (página [Anotações do Atlas e a busca por conceito](atlas_annotations.md)).
4. Selecione uma imagem para ver e editar o seu **Nome**, tipo, categoria, luz, objetiva, escala e **Legenda**;
   **Salvar alterações**. **Ler barra de escala** encontra a barra de escala gravada numa foto e lê o seu comprimento
   (OCR).
5. **Excluir imagem** remove a imagem e os seus blocos do projeto.

## Opções

| Campo | O que muda |
|---|---|
| Objetivas… | µm por pixel da câmera em cada objetiva, medido uma vez numa régua micrométrica. |
| Blocos | JPEG (menor, para fotografias) ou PNG (sem perda, para mapas e rótulos). |
| Posição x, y (mm) | Onde a foto fica na lâmina (o seu centro), no sistema da lâmina. |
| Platina x, y (mm) | Onde estava a platina quando a foto foi tirada (para voltar a ela). |

## Como funciona

Cada imagem é guardada no projeto como uma pirâmide de blocos: só os blocos que estão na tela são lidos, no nível que
corresponde ao zoom, e assim uma lâmina de 2 gigapixels abre numa fração de segundo e se move sem esperar. Toda imagem
tem o seu lugar no sistema da lâmina (milímetros), compartilhado com a contagem de pontos, as anotações, os mapas
mineralógicos e as análises pontuais: o que está num ponto de uma imagem está no mesmo ponto das outras.

## Por script

```python
d = prj["TS-9"]
slide = d.add_image("TS-9_PP.tif", category="scanner", modality="pp")
photo = d.add_photo("campo1.jpg", x_mm=4.2, y_mm=3.6, magnification=10, stage_x_mm=31.2, stage_y_mm=24.6)
slide.overview("TS-9_campos.png", width=2400)              # a lâmina com os campos das fotos numerados
crop = slide.region(*slide.to_px(4.0, 3.4), 400, 300)      # um array NumPy em resolução plena
for img in prj.images(kind="photo", modality="xp", well="ILLUSTRATIVE W-1"):
    print(img.name, img.um_per_px, img.x_mm, img.y_mm)
prj.objectives = {"10": 0.65, "20": 0.325}                 # µm por pixel de cada objetiva
```

## Limites e problemas comuns

* "Esta lâmina não tem imagem da lâmina inteira." — as fotos podem ser importadas mesmo assim, e posicionadas depois.
* "A posição de platina desta foto não é conhecida." — Platina a este campo precisa da posição de platina.
* "Uma escala precisa de dois pontos diferentes e um comprimento maior que zero."
* Para levar vários gigabytes de imagens para outro projeto, **Salvar projeto como…** é mais rápido que um arquivo de
  intercâmbio.

## Cobertura

R1 (banco de fotomicrografias com consultas rápidas), GT1 (imagens de lâminas com escala), GT21 (CZI e a barra de
escala), L6 (fotos tiradas de novo na mesma posição referenciada).
