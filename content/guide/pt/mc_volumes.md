# RockFace MC: volumes de micro-CT — importação, vistas e processamento

## Para que serve

O RockFace MC guarda os volumes de micro-CT de cada amostra — um plugue, um testemunho inteiro, um pote de amostra de
calha — ao lado das suas lâminas e descrições. Ele importa os formatos usuais, guarda volumes de qualquer tamanho fora
da memória, mostra-os em três fatias e em 3D, e os recorta, filtra, reamostra, combina e exporta. Cada operação grava
um novo volume com o seu histórico; o original nunca é alterado.

## Antes de começar

* Uma descrição salva: um volume pertence à amostra da descrição (e pode ser ligado a uma das suas lâminas).
* Abra o MC: **Início → Imagens → MC** (Ctrl+Shift+M) no RockFace Petro, ou `rockface mc projeto.rockface`.

## Passo a passo

### A janela

* **Volumes** à esquerda, por amostra (e os poços com os seus perfis, página [RockFace MC: perfis de imagem](mc_image_logs.md)); selecione um para
  mostrá-lo.
* Três vistas de fatias (x, y, z) e a **Vista 3D** (**projeção de máximos**, **projeção média**, ou **desligada**).
  Clique numa fatia para mover as outras; o status mostra "Voxel x, y, z: valor".
* **Janela** (níveis de cinza mostrados) e **Janela automática**; **Sobrepor** põe um volume segmentado sobre o de
  cinza.
* As abas: **Importar**, **Volume**, **Segmentação**, **Registro**, **Testemunhos**, **Perfis**, **Floresta
  aleatória**, **Análises**, **Rede de poros**, **Microporosidade**, **Multiescala**, **IA**, **Mais**.

### Importar um volume

1. Abra **Importar**. **Arquivo…** ou **Pasta…**: uma pasta de fatias, uma pasta TESCAN ou DICOM, um TIFF de várias
   páginas, RAW, MetaImage (.mhd/.mha), NRRD, NetCDF, HDF5, Amira (.am) ou ASCII do Imperial (.dat).
2. Para RAW: **Tamanho (RAW)** em voxels, **Tipo (RAW)**, **Ordem dos bytes (RAW)** (little- ou big-endian) e
   **Cabeçalho a pular (RAW)**. Os outros formatos o dizem no seu cabeçalho.
3. **Tamanho do voxel** (do arquivo, ou digitado em µm).
4. **Conteúdo**: **níveis de cinza** ou **segmentado**; para um volume segmentado, **Valores e segmentos** associa
   cada valor do arquivo a um segmento.
5. **Amostra** e, opcionalmente, a **Lâmina**; o **Nome**.
6. **Importar**. "… importado: nx × ny × nz voxels."

Imagens públicas de micro-CT podem ser baixadas com a sua licença: **Dados abertos de rochas (imagens públicas)…**
(página [Dados abertos de rochas: imagens públicas de micro-CT](open_rock_data.md)).

### Processar (a aba Volume)

* **Recortar (voxels, de – até)** em x, y e z, e depois **Recortar**.
* **Filtros**: **Filtrar** (gaussiano, mediana, média, máscara de nitidez, janela para 8 bits, inverter, difusão
  anisotrópica) com os seus parâmetros, **Adicionar** à lista, **Limpar**, **Aplicar**. Os filtros rodam bloco a bloco.
* **Correção de sombreamento (corte a corte)** — página [Ferramentas de volume: filtros, sombreamento, efeitos do editor de segmentos, objetos, registro, análises](volume_tools.md).
* **Reamostrar**: **Novo tamanho de voxel**, **Interpolação** (vizinho mais próximo, linear, cúbica), **Reamostrar**.
* **Calculadora de volumes**: uma **Fórmula** sobre os volumes do mesmo tamanho (listados em "Volumes deste
  tamanho:"), por exemplo `(a − b) / 2` ou `a > 120` (uma condição dá um volume segmentado 0/1); **Calcular**.
* **Exportar**: **Exportar…** para .mhd (+ .raw), .mha, .nrrd, .tif ou .nc, com o tamanho do voxel.
* **Excluir volume** (não é possível desfazer).

## Opções

| Opção | O que muda |
|---|---|
| Conteúdo | Níveis de cinza, ou segmentado (rótulos com os seus segmentos). |
| Interpolação | Vizinho mais próximo para volumes segmentados; linear ou cúbica para níveis de cinza. |
| Janela | Só a exibição; os valores guardados não mudam. |

## Como funciona

Os volumes são guardados no projeto como blocos comprimidos de 64³ voxels com uma pirâmide de níveis reduzidos à
metade; assim, as vistas leem só o que mostram, e um volume maior que a memória é processado um bloco de cada vez: 403
milhões de voxels foram importados e segmentados com cerca de 1 GB de memória. Os filtros bloco a bloco são iguais ao
volume inteiro de uma vez; cinco formatos foram lidos de volta idênticos.

## Por script

```python
d = prj["TS-9"]
ct = d.import_volume("plug.mhd")                               # ou prj.import_volume(caminho, d, voxel_um=5.0)
small = ct.crop((0, 400, 0, 400, 0, 400)).resample(factor=0.5)  # caixa (z0, z1, y0, y1, x0, x1) em voxels
smooth = ct.filter(("median", {"size": 3}), ("gaussian", {"sigma": 0.8}))
diff = prj.calculate_volumes("a - b", {"a": ct, "b": smooth}, name="residuo")
print(ct.shape, ct.voxel_um)                                    # (nz, ny, nx), µm
smooth.export("plug_suave.nrrd")
```

## Limites e problemas comuns

* "Escolha um arquivo ou pasta e uma amostra."
* Um arquivo RAW lido com o tamanho ou tipo errado parece ruído: confira o tamanho, o tipo e a ordem dos bytes.
* Importações muito grandes demoram; o progresso aparece e o trabalho pode ser cancelado.

## Cobertura

GV1 (importação), GV2 (exportação), GV3 (recorte), GV4 (filtros), GV5 (reamostragem), GV8 (imagens grandes fora da
memória), GV14 (calculadora de volumes), L2 (ligações das amostras com a tomografia).
