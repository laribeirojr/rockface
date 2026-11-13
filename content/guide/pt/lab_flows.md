# RockFace Lab: fluxos, a lâmina inteira e NetCDF

## Para que serve

Um **fluxo** roda a cadeia inteira — segmentação, separação em objetos, medida — numa imagem ou em muitas (todas as
imagens de uma lâmina, ou do projeto) de uma vez, e dá uma tabela com uma linha por amostra e arquivos LAS dos tamanhos
de poro por profundidade para cada poço. **Lâmina inteira** segmenta uma imagem completa de lâmina em resolução plena,
bloco a bloco. **Importar e exportar** lê e grava imagens de rótulos e arquivos NetCDF para trocar mapas com outros
programas.

## Antes de começar

Imagens das lâminas no RockFace Lab; para o fluxo PP/XP, a imagem XP de cada lâmina; para LAS, descrições com poço e
profundidade.

## Passo a passo

### Um fluxo

1. Abra a aba **Fluxos**.
2. **Fluxo**:
   * **PP: poros e grãos** — segmentação pela resina azul, poros e grãos separados e medidos;
   * **PP/XP: grãos separados pelas cores XP** — grãos distinguidos pelas cores de extinção em nicóis cruzados
     (**XP: unir cores mais próximas que (ΔE*ab)**);
   * **Mapa mineral (QEMSCAN…): objetos de cada fase**.
3. **Imagens de**: **esta lâmina** ou **todo o projeto**; marque as imagens a usar.
4. **Separação dos poros** (watershed, SNOW, ilhas), **Distância mínima entre centros**, **Objetos menores que
   (descartados)**, **Separar também os grãos**.
5. **Executar o fluxo nas imagens marcadas**. "Executando o fluxo: imagem k de n…", depois "Fluxo feito em N imagens
   (M com erros)".
6. A tabela tem uma linha por amostra: poço, profundidade, lâmina, porosidade, as frações das fases e as estatísticas
   de tamanho. Exporte-a (CSV, XLSX).
7. **Curva LAS dos poros** (a coluna de tamanho) e **LAS por profundidade**: um arquivo LAS por poço com o máximo, a
   média, a mediana, o mínimo e o desvio padrão da coluna e a porosidade em cada profundidade de amostra.

### A lâmina inteira

1. Em **Lâmina inteira (sem aprendizado de máquina)**, selecione uma imagem.
2. **Quantificar a lâmina inteira** a segmenta em resolução plena, bloco a bloco, com o método da aba Segmentação
   (métodos pixel a pixel; senão, a resina azul). "…: N pixels contados", com a porosidade e a parte de cada segmento.

Para a lâmina inteira segmentada por uma rede neural, veja [RockFace IA: segmentar com modelos, treinar, ajustar e validar](ai_segmentation.md).

### Importar e exportar

* **Importar uma imagem de rótulos…** (PNG, TIFF) — **Rótulos como mapa de segmentação** ou **Rótulos como mapa de
  objetos**.
* **Exportar o mapa como rótulos (TIFF)…**
* **Importar NetCDF…** e **Exportar a lâmina como NetCDF…** — as imagens e mapas da lâmina com a sua escala, origem e
  fases (NetCDF clássico; lê NetCDF-4).

## Opções

| Opção | O que muda |
|---|---|
| Fluxo | PP, PP/XP ou mapa mineral. |
| Imagens de | Uma lâmina ou todo o projeto. |
| XP: unir cores mais próximas que | Grãos cujas cores XP diferem menos que isso são um grão só. |
| Curva LAS dos poros | A coluna de tamanho gravada nos arquivos LAS. |

## Como funciona

* Os fluxos usam as mesmas funções das abas; assim, um fluxo dá o resultado que as abas dariam passo a passo.
* Os grãos separados com as cores XP foram achados com revocação de 0,87–0,89, contra 0,46–0,51 só com PP, em lâminas
  de grãos conhecidos.
* A lâmina inteira é processada bloco a bloco com margens sobrepostas: numa lâmina de 27 Mpx o resultado foi idêntico
  ao da imagem inteira de uma vez, e a porosidade igual à verdade.
* As idas e voltas de NetCDF e de TIFF de rótulos são idênticas.

## Por script

```python
pp = prj.image("ILLUSTRATIVE mosaic PP")
r = pp.run_flow("pp")
pores, grains = r.measurements
print(r.porosity, grains.summary(exclude_edge=True)["d50_mm"])
results = prj.run_flow(prj.images(kind="slide", modality="pp"), flow="pp")
prj.flow_table(results).to_csv("por_amostra.csv")
prj.las_by_depth(results, "las", column="feret_max_um")
seg, fractions, porosity = pp.quantify_whole("resin")
prj.export_netcdf([pp, seg], "lamina.nc")
```

## Limites e problemas comuns

* "Marque pelo menos uma imagem."
* "A lâmina não tem imagem XP para esta imagem." — o fluxo PP/XP precisa das duas luzes.
* Amostras sem poço ou sem profundidade aparecem na tabela, mas não nos arquivos LAS.

## Cobertura

GT14 (LAS por profundidade, NetCDF), GT15 (fluxos predefinidos PP, PP/XP, QEMSCAN), GT16 (análise de várias imagens),
GT17 (exportação e importação de fontes padrão), L7 (quantificação da lâmina inteira, clássica).
