# MC → Mais: copos, mapa de distâncias, vigia de pasta, reconstrução, transferência de escala e escoamento bifásico

## Para que serve

Ferramentas encontradas na auditoria do código do GeoSlicer: calibrar os valores de cinza com **copos de
referência**, medir a **distância** à borda de um segmento, importar tomografias de uma **pasta** enquanto o tomógrafo
as grava, **reconstruir** uma aquisição SkyScan, levar medidas do testemunho para as amostras de profundidade de um
**LAS** e medidas de plugues **ao longo do testemunho**; nos perfis de imagem, segmentar um **intervalo de
profundidade** e traçar um nível através da emenda 0/360°; simular **escoamento bifásico** num volume segmentado
com o LBPM.

## Antes de começar

Uma amostra com volumes (MC), ou um poço com perfis de imagem.

## Passo a passo

1. **MC → Mais → Copos de referência**: abra a tomografia com o plugue e os copos de teflon, quartzo e alumínio;
   **Encontrar os copos em volta do plugue**; digite os valores que eles devem ter; **Reescalar os valores de cinza**
   (um volume novo).
2. **Mapa de distâncias**: num volume segmentado, escolha o segmento; **Distância à borda do segmento (µm)**.
3. **Vigiar uma pasta**: escolha a pasta de saída do tomógrafo; **Começar a vigiar**: cada tomografia que parou de
   crescer é importada; nomes numerados formam uma sequência no tempo.
4. **Reconstrução (FDK)**: uma pasta SkyScan (projeções e `.log`); **Reconstruir**.
5. **Escoamento bifásico (LBPM)**: abra um volume segmentado; indique os segmentos do fluido A (rótulo 1 do LBPM) e
   do fluido B (rótulo 2), os componentes sólidos que molham de outro modo, a afinidade de molhamento do sólido e a
   grade de processos; **Escrever o caso** (a pasta, o comando e um script de SLURM `run_lbpm.sh`), ou **Executar
   aqui como trabalho** / **Executar no computador remoto** (o computador de MC → Multiescala →
   Trabalhos (lote e remotos)); **Ler os resultados** mostra os pontos finais e as curvas.
6. A transferência para LAS, do plugue ao testemunho e as ferramentas de perfil estão na API (abaixo).

## Como funciona

* Copos: o cilindro do plugue é encontrado, os voxels em volta são separados por um Otsu de quatro classes (ar e as
  três referências) e k-médias 1-D; a reescala é a reta de mínimos quadrados pelas referências.
* Distância: a transformada de distância euclidiana com o voxel de cada eixo.
* Vigia de pasta: um conjunto é importado quando o tamanho e a hora são os mesmos em duas olhadas.
* Reconstrução: Feldkamp–Davis–Kress para feixe cônico em órbita circular (Feldkamp et al. 1984; Kak & Slaney 1988) e
  retroprojeção filtrada para feixe paralelo, em NumPy (a do GeoSlicer usa o ASTRA, GPL, que o RockFace não pode
  distribuir); atenuação em 1/mm.
* LAS: a média dos valores do testemunho dentro da janela de cada amostra do LAS; do plugue ao testemunho: uma
  floresta aleatória (ou ajuste linear) dos valores dos plugues sobre os atributos de CT do testemunho, conferida por
  deixar-um-fora antes do uso.
* Perfis: um intervalo de profundidade gravado como segmento; o traçado de nível cresce a região de valores parecidos
  a partir de uma semente, conectada através da emenda de um perfil de volta inteira.
* Escoamento bifásico: LBPM (McClure et al. 2021; GPL-3.0, por isso o RockFace não o contém — executa a instalação do
  próprio usuário). O caso: o volume como o RAW de 8 bits do LBPM (x mais rápido) e o `input.db`, com o `Domain`
  escrito de acordo — tamanho, grade de processos e subdomínios, voxel em µm, os segmentos mapeados para 0 (sólido),
  1, 2 e rótulos negativos para os componentes sólidos com sua `ComponentAffinity`; as outras seções vêm da
  documentação do LBPM (modelo de cor, protocolo de fluxo fracionário). Os resultados: `timelog.csv`
  (permeabilidade relativa contra a saturação) e `subphase.csv` (saturação pelos volumes das fases conectadas e
  desconectadas, pressão capilar pn − pw, área interfacial, característica de Euler), como o Pore Scale Modelling do
  GeoSlicer os lê.

## Por script

```python
c = rf.gs_tools.cups(prj.raw, vol_id); rf.gs_tools.remap(prj.raw, vol_id, c.medians, {"teflon": 1000, "aluminium": 3000})
rf.gs_tools.distance_map(prj.raw, labels_id, 1)
vol, voxel_um = rf.gs_tools.reconstruct_skyscan("pasta_da_aquisicao")
rf.gs_tools.upscale_to_las(prof, porosidade, "poco.las", "saida.las", compare="PHIT")
rf.gs_tools.plug_to_core(prof_testemunho, atributos, prof_plugues, porosidade_plugues)
rf.log_edit.fill_depth_range(prj.raw, log_id, 1001.0, 1001.2, 2)
rf.log_edit.level_trace(prj.raw, grey_id, labels_id, azimuth=10, depth=1000.5, tolerance=10, value=3)
res = prj.lbpm(labels_id, {1: "fluid_a", 2: "fluid_b"}, "caso-lbpm", nproc=(2, 2, 1))   # requer o LBPM instalado
prj.lbpm(labels_id, {1: "fluid_a"}, "caso-lbpm", run=False)       # só o caso e o comando
```
`rockface notebook projeto.rockface` grava um caderno Jupyter que abre o projeto com a API.

## Limites e problemas comuns

* A reconstrução espera projeções já corrigidas pelo campo claro (como o SkyScan grava) e o eixo de rotação centrado.
* Do plugue ao testemunho precisa de plugues que cubram a faixa do testemunho; o erro de deixar-um-fora diz o quanto
  confiar.
* O LBPM precisa estar instalado onde o trabalho roda (aqui, no computador remoto ou no cluster); cada dimensão do
  volume deve ser divisível pela grade de processos. As pressões estão em unidades de rede.

## Cobertura

Auditoria do GeoSlicer da 0.28 (GV20–GV28, GI12–GI13).
