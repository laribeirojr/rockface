# Dados abertos de rochas: imagens públicas de micro-CT

## Para que serve

Para experimentar o RockFace MC, comparar métodos ou ensinar sem imagens próprias: imagens públicas de micro-CT de
arenitos e carbonatos, baixadas e importadas numa amostra com a sua licença e a sua citação.

## Antes de começar

* Um projeto com pelo menos uma amostra (uma descrição), e conexão com a Internet.
* Espaço em disco: uma imagem de 1000³ voxels ocupa cerca de 1 GB, e o arquivo de 2015 do Imperial College vários GB.

## Passo a passo

1. No RockFace MC, aba **Importar**, clique em **Dados abertos de rochas (imagens públicas)…**.
2. Escolha uma imagem na tabela (coleção, rocha, imagem, tamanho, licença). Abaixo da tabela: a citação, a licença, o
   tamanho do download e a página da fonte. **Leia a licença antes de usar os dados, e cite a fonte.**
3. Escolha a **Amostra** que recebe o volume e a **Pasta de download**.
4. Clique em **Baixar e importar**. O arquivo é baixado uma vez (uma segunda importação o reaproveita) e importado
   como um volume da amostra; a sua legenda guarda a citação e a licença.

## Opções

* **Eleven Sandstones** (Digital Rocks Portal): onze arenitos a 2,25 µm, 1000³ voxels, em três formas — cinza,
  filtrada e binária. Licença ODC-BY 1.0.
* **ICL sandstones and carbonates 2009** (Imperial College London): imagens binárias do Berea, dos arenitos S e LV60 e
  de carbonatos, em arquivos 7-Zip (é preciso o pacote `py7zr` para abri-los).
* **ICL micro-CT 2015** (Imperial College London): Bentheimer, Doddington, Estaillades e Ketton, 1000³, cinza, num
  arquivo de vários gigabytes.

## Como funciona

A lista de imagens, endereços, tamanhos e tamanhos de voxel segue a biblioteca `drd` de L. Mosser (Apache 2.0), usada
pelo GeoSlicer; os arquivos são baixados por um arquivo temporário `.part` e importados fora da memória, um bloco por
vez.

## Por script

```python
for e in rf.ProjectAPI.rock_data()[:3]:
    print(e.id, e.rock, e.licence)
v = prj.download_rock_data("eleven/Berea/binary", prj.descriptions()[0], folder="dados")
```

## Limites e problemas comuns

* **"O download … falhou"** — sem conexão, ou a fonte mudou o arquivo de lugar; tente mais tarde ou baixe-o pela
  página da fonte e importe-o em **Importar** (RAW, 1000 × 1000 × 1000, 8 bits).
* **"Este arquivo está no formato 7-Zip"** — instale o `py7zr` (`pip install py7zr`).
* As imagens binárias são importadas como volumes de cinza com dois valores: segmente-as com um limiar (aba
  Segmentação).

## Cobertura

GV17 (Open Rock Data).
