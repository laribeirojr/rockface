# RockFace MC: perfis de imagem

## Para que serve

A aba **Perfis** guarda os perfis de imagem de um poço — amplitude acústica e tempo de trânsito, resistividade,
condutividade, desenrolados de testemunho, perfis de TC — com as suas curvas, num só eixo de profundidade. Ela importa
e exporta os formatos usuais, recorta-os e os processa (excentricidade, filtro de espiral, qualidade e
heterogeneidade, correção de azimute, CLAHE), preenche as suas falhas, segmenta-os em vugues com os seus tamanhos por
profundidade, ajusta as senoides de feições planares e põe desenrolados de testemunho sobre o perfil de imagem.

## Antes de começar

* Os arquivos de perfil: LAS 2.0 (com curvas de imagem empilhadas), CSV (matriz, Techlog, forma longa; também gzip),
  NetCDF ou grades GMT, DLIS (com o extra opcional `dlis`), uma imagem com as profundidades do topo e da base, ou uma
  pasta de desenrolados de testemunho.
* O nome do poço; o diâmetro do poço, para comprimentos em milímetros.

## Passo a passo

### Importar

1. Abra **Perfis**. **Arquivo ou pasta** (LAS, CSV, NetCDF/grd, DLIS, imagem, pasta de desenrolados).
2. **Poço**, **Diâmetro do poço**, **Medida** (amplitude acústica, tempo de trânsito, resistividade, condutividade, TC,
   fotografia, outra); para uma imagem, o seu **Topo e base da imagem**.
3. **Importar**. "N perfil(is) importado(s)." Os poços e os seus perfis aparecem no painel da esquerda; as trilhas são
   mostradas lado a lado num só eixo de profundidade, com uma **Paleta**.

### Recorte e processamento

1. **Profundidades** e **Recortar**.
2. **Processo** — escolha um, com os seus parâmetros, e depois **Aplicar**:
   * **Excentricidade** — corrige a amplitude de uma ferramenta fora do centro do poço, usando o **Perfil de tempo de
     trânsito**;
   * **Filtro de espiral** — remove o padrão em espiral da ferramenta (**Comprimento de onda mínimo** e **máximo
     (m)**); "Filtrado: …% da imagem mudou";
   * **Indicador de qualidade** e **Índice de heterogeneidade** — curvas por profundidade (**Janela (m)**);
   * **Correção de azimute** — gira a imagem por uma **Curva de desvio de azimute**;
   * **CLAHE** — contraste local (**Limite de corte**).

### Registro do desenrolado e preenchimento

1. **Desenrolado do testemunho** e **Maior deslocamento**, depois **Colocar o desenrolado sobre o perfil**:
   "Desenrolado movido … m e girado …° (correlação …)".
2. **Preenchimento**: **linear (linha a linha)**, **harmônico (suave)** ou **biarmônico**; **Preencher também (perfil
   segmentado)** para uma máscara; **Preencher as falhas** — as falhas entre os patins da ferramenta e as áreas
   mascaradas são preenchidas.

### Segmentação, objetos e tamanhos de poro

1. **Cortes** (vazio: Otsu), depois **Segmentar**.
2. **Objetos**: os vugues como objetos através da emenda de 0/360° (**Menor objeto**): "N objetos; diâmetro equivalente
   médio … mm, maior … mm", com a sua tabela.
3. **Tamanhos de poro**: a espessura local do espaço poroso em mm e os seus histogramas por **Intervalo de
   profundidade**.

### Feições planares

1. **Marcar pontos**: clique em pelo menos três pontos de um plano de acamamento ou fratura na trilha da imagem.
2. **Ajustar a senoide**: "Plano em … m: mergulho …° para …°".
3. **Trama dominante**: a senoide dominante das profundidades na tela.

### Exportar

**Exportar…** grava LAS, CSV (matriz ou Techlog), NetCDF, PNG/TIFF ou DLIS (com o dliswriter opcional).

## Opções

| Opção | O que muda |
|---|---|
| Medida | O que o perfil é; amplitude e tempo de trânsito vão juntos para a excentricidade. |
| Preenchimento | Linear (rápido), harmônico (suave), biarmônico (segue os gradientes). |
| Menor objeto | Vugues menores que isso ficam de fora. |

## Como funciona

* Os perfis são guardados por profundidade com uma pirâmide; assim, poços longos são mostrados na hora.
* No poço ILUSTRATIVO (camadas inclinadas e vugues de verdade conhecida): trama dominante 25,0°/120,0° exata; um patim
  escondido preenchido com RMSE 0,043–0,050 contra 0,083 da média da linha; 38 de 40 vugues achados.
* Num perfil FMI real (teste interno): um patim escondido preenchido com RMSE 14,97 (linear) contra 29,07 da média da
  linha; duas passadas coincidindo dentro de 0,8 mm.
* Editar segmentações de perfil com o pincel e revisar objetos: página [Editar a segmentação de um perfil e os seus objetos](log_editing.md); modelo de permeabilidade de
  perfis segmentados: página [Modelo de permeabilidade de perfis de imagem](permeability_model.md).

## Por script

```python
amp, tt = prj.import_log("amplitude.las", "W-1", diameter_mm=216)[:2]
(fixed, tau, _), = amp.eccentricity(tt)
clean, changed = fixed.inpaint(method="biharmonic").spiral_filter(4, 20)
print(clean.dominant_sinusoid(2501, 2510).dip_deg)
vugs, table = clean.segment().objects(min_px=6)
table.to_csv("vugues.csv")
clean.export("limpo.las")
```

## Limites e problemas comuns

* "Escolha um arquivo ou pasta."
* "Nenhum perfil a mostrar." — o poço ainda não tem perfis, ou nenhum nas profundidades mostradas.
* DLIS precisa do extra `dlis` (dlisio, LGPL, carregado só quando usado).

## Cobertura

GI1 (importação), GI2 (desenrolado), GI3 (exportação), GI4 (recorte), GI5 (processamento), GI6 (registro do
desenrolado), GI7 (preenchimento), GI8 (segmentação, feições planares), GI9 (distribuição de tamanhos de poro).
