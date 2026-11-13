# RockFace MC: testemunhos inteiros e fotos de caixas de testemunho

## Para que serve

A aba **Testemunhos** processa em lote as tomografias de testemunhos inteiros de um poço: cada testemunho é achado no
seu tubo (liner) e centrado, recebe o seu poço e profundidade, é orientado (pelo acamamento do primeiro testemunho ou
por um perfil de imagem do poço), movido e girado, desenrolado como uma imagem da sua superfície externa, posto como um
desenrolamento do poço e como um perfil de TC, tem as suas fraturas preenchidas, e é exportado. As fotografias de
caixas de testemunho são cortadas nos seus testemunhos e postas por profundidade como uma faixa única do poço.

## Antes de começar

* As tomografias importadas como volumes de cinza de uma amostra do poço (página [RockFace MC: volumes de micro-CT — importação, vistas e processamento](mc_volumes.md)).
* A profundidade do topo do primeiro testemunho e o diâmetro do testemunho; opcionalmente, uma tabela do topo e da
  base de cada testemunho (CSV).
* Para orientar por um perfil de imagem: o perfil de imagem do poço (página [RockFace MC: perfis de imagem](mc_image_logs.md)).

## Passo a passo

### Processar as tomografias

1. Abra **Testemunhos**. Em **Tomografias da amostra**, marque as tomografias.
2. **Poço**, **Topo do primeiro testemunho**, **Diâmetro do testemunho**; **Limites (CSV)** (opcional: topo e base de
   cada testemunho, em m).
3. **Corrigir a atenuação radial (endurecimento do feixe)** se o testemunho é mais claro na borda.
4. **Processar os testemunhos**. "Encontrando e centrando os testemunhos…", depois "N testemunho(s) processado(s)".
   Cada testemunho mostra "Testemunho de …: topo–base m, … mm, rotação …°, deslocamento … m".

### Orientação e posição

1. **Orientar por**: **acamamento do primeiro testemunho** (os outros girados para acompanhá-lo), ou **um perfil de
   imagem do poço** (escolha o **Perfil de imagem**).
2. **Orientar os testemunhos marcados**. "Rotações: …".
3. À mão: **Deslocamento em profundidade** e **Rotação**, depois **Mover e girar o testemunho**.

### Desenrolamento e perfis

1. **Profundidade radial** (a que profundidade, dentro da superfície, o desenrolado é lido), depois **Desenrolar o
   testemunho**: uma imagem da superfície externa, profundidade para baixo, azimute de lado, posta nos perfis do poço.
2. **Diâmetro do poço** e **Desenrolamento do poço**: os testemunhos marcados como um desenrolado do poço, no diâmetro
   do poço.
3. **Perfil de TC**: o valor médio de TC por profundidade, como uma curva do poço.

### Preenchimento, exportação, fluxo

* **Fraturas (volume segmentado)** e **Preencher as fraturas**: as fraturas de um testemunho segmentado preenchidas
  fatia a fatia.
* **Exportar os testemunhos marcados…**: um resumo HTML, a matriz CSV e a forma do Techlog com profundidade, o
  desenrolado em PNG, o volume em TIFF. "N arquivos gravados em …".
* **Fluxo de testemunho: testemunho → segmentação**: importação → testemunho → recorte → segmentação e porosidade, de
  uma vez.

### Fotografias de caixas de testemunho

1. Em **Fotografias de caixas de testemunho**, **Adicionar fotografias…** e dê a cada uma o seu **Topo (m)** e **Base
   (m)**.
2. **Canais por caixa** (fileiras de testemunhos numa caixa), ou **automático**.
3. **Formar a faixa**: as fileiras de testemunhos são achadas pela cor do fundo, cortadas e postas ponta a ponta por
   profundidade como uma faixa única do poço.

## Opções

| Opção | O que muda |
|---|---|
| Corrigir a atenuação radial | Remove o clareamento da borda causado pelo endurecimento do feixe. |
| Orientar por | O acamamento do primeiro testemunho, ou um perfil de imagem. |
| Profundidade radial | Profundidade dentro da superfície em que o desenrolado é lido (mm). |
| Canais por caixa | O número de fileiras de testemunhos em cada foto de caixa. |

## Como funciona

* O tubo e o testemunho são achados como círculos nas fatias; no poço ILUSTRATIVO, o raio do testemunho foi achado em
  49,6–49,7 mm para 50 mm, e numa tomografia real de testemunho inteiro (teste interno) o testemunho dentro do tubo em
  130,4 mm.
* A orientação pelo acamamento ajusta a senoide dominante do desenrolado de cada testemunho; por um perfil de imagem,
  correlaciona os gradientes de profundidade do desenrolado e do perfil: dentro de 0,1° e 2 mm no poço ILUSTRATIVO.
* As fotos de caixas de testemunho formaram uma faixa exata no poço ILUSTRATIVO.

## Por script

```python
scans = prj["TS-9"].volumes()                                 # as tomografias da amostra, do topo à base
cores = [prj.process_core(v, 2500.0 + 0.9 * k, 100.0, well="W-1") for k, v in enumerate(scans)]
print(cores[0].core["diameter_mm"], cores[0].core["top_m"])
prj.orient_cores(cores, "sinusoid")                            # ou "image_log", log=prj.log("AMP")
unwrap = cores[0].unwrap(radial_depth_mm=1.0)
well_unwrap = prj.well_unwrap(cores, well_diameter_mm=216)
ct = prj.ct_log(cores)
prj.export_cores(cores, "testemunhos")
strip = prj.load_core_photos("W-1", [("caixa1.jpg", 2500.0, 2503.0), ("caixa2.jpg", 2503.0, 2506.0)])
```

## Limites e problemas comuns

* "Marque pelo menos uma tomografia ou um testemunho."
* "Indique o topo e a base de cada fotografia."
* Um testemunho encostado no tubo pode ser achado como o tubo: confira o diâmetro mostrado, e dê o diâmetro do
  testemunho.

## Cobertura

GC1 (multitestemunho), GC2 (carregador de fotos de testemunho), GC3 (recorte), GC4 (transformações de
multitestemunho), GC5 (segmentação), GC6 (preenchimento de testemunho), GC7 (exportação), GC8 (fluxos), GI2
(desenrolados de testemunhos processados).
