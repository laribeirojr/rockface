# Superfícies 3D, salvar num arquivo NetCDF existente e o pacote para o Geolog

## Para que serve

Três ferramentas de troca da aba **Multiescala** do RockFace MC:

* **Superfícies 3D**: os modelos de fotogrametria de testemunhos, plugues e afloramentos (Wavefront OBJ com os seus
  materiais MTL e as figuras de textura) guardados no projeto e mostrados em 3D, e a superfície de um segmento de um
  volume criada e escrita como OBJ.
* **Salvar num arquivo NetCDF existente**: os volumes feitos no RockFace escritos como novas variáveis do arquivo
  NetCDF de onde vieram os dados, que mantém tudo o que tinha (atributos, dimensões e outras variáveis).
* **Geolog (arquivos)**: os perfis de um poço escritos como um pacote que o Geolog carrega com os seus próprios
  carregadores de LAS e DLIS, e os arquivos que o Geolog escreve lidos de volta, com os seus valores nulos.

## Antes de começar

* Uma superfície: um arquivo `.obj` (com o seu `.mtl` e as figuras na mesma pasta), ou um volume segmentado.
* NetCDF: um arquivo NetCDF clássico existente (ou NetCDF-4, com o h5py instalado) e o volume a salvar.
* Geolog: os perfis de um poço (aba Perfis de poço); arquivos DLIS são escritos quando o `dliswriter` está instalado e
  lidos quando o `dlisio` está instalado; LAS sempre.

## Passo a passo

### Superfícies 3D

1. Em **Superfícies 3D**, digite os **mm por unidade do arquivo OBJ** (1 quando o modelo está em mm; 1000 em metros) e
   clique em **Importar OBJ…**. A superfície fica com a amostra atual e é mostrada: arraste para girar, roda do mouse
   para ampliar.
2. Para criar uma a partir de um volume, abra uma segmentação, escolha o **Segmento** e clique em **A partir do
   segmento**.
3. **Exportar OBJ…** escreve o OBJ, o seu MTL e as texturas em PNG; **Excluir a superfície** a remove.

### Salvar num arquivo NetCDF

1. Abra o volume a salvar e, em **Salvar num arquivo NetCDF existente**, escolha o **Arquivo NetCDF**.
2. Marque **Substituir uma variável de mesmo nome** para sobrescrever uma; senão, é dado um nome novo (`_2`, `_3`…).
3. Clique em **Salvar o volume atual no arquivo**. Um volume com a mesma forma de uma variável do arquivo recebe as
   dimensões dela, de modo que fica alinhado com a imagem de onde veio.

### Geolog

1. Em **Geolog (arquivos)** escolha o **Poço** e clique em **Escrever um pacote para o Geolog…**, depois uma pasta: um
   LAS por perfil de imagem, um LAS por malha de profundidade para as curvas, um DLIS com todos os perfis,
   `rockface_geolog.json` e `README_geolog.txt`.
2. Para ler os arquivos do Geolog, digite os **Valores nulos** (−999,25; −999; −9999; −99999 por padrão) e o
   **Diâmetro** do poço, e clique em **Ler arquivos do Geolog…** na pasta (ou num arquivo).

## Opções

| Campo | O que muda |
|---|---|
| mm por unidade do arquivo OBJ | Escala dos vértices para mm |
| Substituir uma variável de mesmo nome | Sobrescrever em vez de acrescentar um sufixo |
| Valores nulos | Valores lidos como faltantes nos arquivos LAS e DLIS, além do NULL de cada LAS |
| Diâmetro | Diâmetro do poço posto nos perfis de imagem lidos |

## Como funciona

* **OBJ/MTL**: vértices (com cores por vértice opcionais), coordenadas de textura, normais, faces de qualquer número de
  lados divididas em triângulos, índices negativos, `usemtl` e `mtllib`; materiais com `Kd`, `d` e `map_Kd`. Um
  vértice usado com duas coordenadas de textura vira dois vértices. A vista desenha as faces de trás para a frente
  (algoritmo do pintor) com a cor da textura no seu centro e sombreamento de Lambert; malhas pesadas são reduzidas
  para a vista por agrupamento de vértices (Rossignac & Borrel 1993). A partir de um volume, a superfície é feita por
  marching cubes (Lorensen & Cline 1987) depois de uma leve suavização gaussiana da máscara (área de uma esfera
  dentro de 0,5 %).
* **NetCDF**: um arquivo clássico é reescrito por um arquivo temporário com tudo o que tinha mais as novas variáveis,
  depois substituído; um NetCDF-4 recebe as variáveis no próprio arquivo e as escalas de dimensão da variável
  correspondente são ligadas.
* **Geolog**: mnemônicos em maiúsculas, letras, dígitos e sublinhado, no máximo 32 caracteres, únicos; o manifesto
  guarda o que o LAS não guarda (tipos, legendas dos segmentos, azimutes, diâmetro), para o pacote voltar inteiro ao
  RockFace.

## Por script

```python
s = prj.import_surface("core_box.obj", sample, scale_mm=1000)
s.render("core_box.png")
prj.volume("plug segmentation").save_into_netcdf("plug.nc")
prj.geolog_export("Well A", "to_geolog")
logs = prj.geolog_import("from_geolog", "Well A", nulls=(-999.25, -9999))
```

## Limites e problemas comuns

* A vista mostra uma cor por face; texturas muito finas em faces grandes ficam planas (o OBJ escrito mantém a textura
  inteira).
* Arquivos NetCDF clássicos acima de 2 GB precisam do formato de offset de 64 bits, que a reescrita mantém; o
  NetCDF-4 precisa do h5py.
* O RockFace não abre ele mesmo um projeto do Geolog: a troca é por arquivos, que o Geolog carrega e escreve.

## Cobertura

GV18 (superfícies 3D texturizadas), GV15 (salvar num arquivo NetCDF existente), GM1 (integração com o Geolog), GM2
(ferramentas de importação e exportação).
