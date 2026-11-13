# Arquivos dos programas de referência

## Para que serve

O RockFace abre os arquivos que o GeoSlicer e os laboratórios entregam, sem conversão prévia: volumes de micro-CT
do Amira/Avizo, HDF5, séries DICOM e reconstruções TESCAN; lâminas escaneadas Zeiss CZI; cenas e segmentações do
GeoSlicer; as tabelas de laudos de laboratório em PDF; e a barra de escala gravada numa foto de microscópio.

## Antes de começar

* Um projeto com uma amostra (volumes) ou uma lâmina (imagens).
* Pacotes opcionais, instalados uma vez: `pip install rockface[formats]` (HDF5, DICOM, PDF, OCR) e, para CZI,
  `pip install rockface[czi]`. O OCR também precisa do programa Tesseract.

## Passo a passo

1. **Volumes — MC → Importar.** Escolha o arquivo ou a pasta: `.am`, `.h5`/`.hdf5`, um `.dcm` ou uma pasta DICOM,
   uma pasta TESCAN (com `*.acq.1.xml` e `recon/`), ou uma cena `.mrml` ou segmentação `.seg.nrrd` do GeoSlicer.
   Clique em **Importar**.
2. **Saída de volumes — MC → Volume → Exportar** agora também grava `.am`, `.h5` e, para uma segmentação,
   `.seg.nrrd`.
3. **CZI — Atlas → Importar imagens** um `.czi` como qualquer lâmina.
4. **Laudo — Petro → Início → Importar laudo de laboratório (PDF)…**: escolha o PDF, o poço e a tolerância de
   profundidade; cada linha vira uma análise petrofísica convencional da amostra naquela profundidade.
5. **Barra de escala — Atlas → propriedades da imagem → Ler barra de escala**: a barra é encontrada e o comprimento
   lido; se o texto não puder ser lido, digite o comprimento.

## Opções

| Formato | O que o RockFace lê |
|---|---|
| Amira `.am` | binário (little ou big endian) ou ASCII; de byte a double; bruto, HxByteRLE ou HxZip; voxel pelo BoundingBox e Units |
| HDF5 | qualquer conjunto 3D (o maior por padrão); voxel por `voxel_um`, `spacing` + `units`, `element_size_um` |
| DICOM | a maior série da pasta, fatias ordenadas pela normal, unidades Hounsfield; nenhum campo do paciente é guardado |
| TESCAN | as fatias de `recon/`, voxel = VoxelSize (mm) do `*.rec.1.xml`, origem do `*.acq.1.xml` |
| `_NNNNNnm` no nome | tamanho do voxel em nanômetros quando o arquivo não o informa |
| CZI | a primeira cena, RGB ou cinza, µm por pixel pela escala do arquivo |
| `.mrml`, `.seg.nrrd` | volumes, mapas de rótulos e segmentações (3D ou em camadas) com nomes e cores dos segmentos |
| Laudo em PDF | profundidade, diâmetro, comprimento, massa, permeabilidade, porosidade, massa específica dos grãos (cabeçalhos em PT, EN, ES; vírgula ou ponto) |

## Como funciona

* Cada leitor transforma o arquivo numa fonte de volume lida em fatias, de modo que arquivos grandes não ocupam a
  memória; o voxel vem do arquivo, senão do nome, senão do formulário de importação.
* Laudos: tabelas com linhas são lidas pelas linhas; tabelas de texto alinhado, pelas colunas dos números; os
  cabeçalhos são reconhecidos pelas palavras (*Profundidade*, *Permeabilidade*, *Massa específica*…).
* Barra de escala: a barra horizontal sólida mais longa que contrasta com o entorno; depois o texto ao lado, lido
  pelo Tesseract ("500 µm", "0,5 mm"); µm por pixel = comprimento ÷ pixels da barra.

## Por script

```python
src = rf.volume.open_volume("scan.am")                        # ou .h5, uma pasta DICOM ou TESCAN
v = rf.volume.add_volume(prj.raw, src, sample_id)
rf.volume.export(prj.raw, v.id, "saida.seg.nrrd")             # um volume de rótulos para o GeoSlicer
rf.geoslicer.import_scene(prj.raw, "projeto.mrml", sample_id)
prj.import_lab_report("rca.pdf", "ILL-WELL-1", tolerance_m=0.1)
rf.atlas.read_scale_bar(prj.raw, image_id)                    # Scale(bar, text, value_um, um_per_px)
```

## Limites e problemas comuns

* O CZI precisa do pylibCZIrw (LGPL-3.0, opcional, como o OpenSlide para outros formatos de lâmina).
* Um laudo cuja tabela é uma imagem (escaneada) não tem texto: passe um OCR no PDF antes.
* Sem unidades, o BoundingBox do Amira é interpretado pelo tamanho do voxel (metros, milímetros ou micrômetros); a
  escolha fica registrada no histórico do volume.

## Cobertura

Formatos GV1 e GT1 (0.28), GC1 DICOM, tabelas de laudos, barra de escala; auditoria do GeoSlicer da 0.28.
