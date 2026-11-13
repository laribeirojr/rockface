# Da composição 2D à composição 3D, e a publicação

## Para que serve

O mapa mineral de uma lâmina diz o que cada grão é; a micro-CT do plugue mostra os grãos em 3D, mas não o que eles
são. A **composição 3D** leva as fases do mapa para o volume inteiro e dá a cada fase as suas propriedades. A
**publicação** envia o projeto — amostras, descrições, análises, imagens — ao ambiente corporativo de dados, numa
periodicidade, só o que mudou.

## Antes de começar

* Um volume de micro-CT da amostra e um mapa mineral (ou uma segmentação) da sua lâmina.
* O mapa localizado no volume: **MC → Registro → Localizar a imagem** (ou as duas imagens calibradas no referencial
  da lâmina, quando foi localizada outra imagem da mesma lâmina).
* Para publicar: uma pasta vigiada pela ingestão da plataforma, ou o endereço de uma plataforma OSDU e um token.

## Passo a passo

1. Localize o mapa (ou a foto óptica) no volume e salve a posição.
2. Num script ou na janela de scripts: `prj.composite_3d(mapa, volume)` — as fases do mapa na fatia treinam um
   modelo sobre o volume em cinza, um quarto da fatia fica de fora para medir a concordância, e o volume inteiro é
   classificado.
3. Dê às fases as suas propriedades: `rf.composite3d.property_volume(...)` cria um volume de números por propriedade.
4. Publicação: `rockface publish projeto.rockface --folder <pasta> --period 24` (ou `--url <plataforma>`), depois
   `rockface publish projeto.rockface --if-due` pelo agendador do sistema (`--schedule` imprime as linhas).

## Opções

| Ajuste | Significado |
|---|---|
| hold_out | parte da fatia deixada fora do treino para medir a concordância (padrão 0,25) |
| method | floresta aleatória ou modelo bayesiano gaussiano |
| target | `folder` (arquivos de manifesto) ou `rafs` (OSDU Storage + RAFS DDMS) |
| period_hours | a cada quantas horas o `--if-due` publica |
| token_env | a variável de ambiente com o token de acesso (ROCKFACE_OSDU_TOKEN); nunca é guardado |
| analysis_type, content_version | tipo de conteúdo RAFS e versão do esquema das análises de rotina |

## Como funciona

* O mapa é amostrado em cada voxel da fatia posicionada, pela matriz da posição; as fases de fundo não treinam. O
  modelo é a floresta aleatória do MC com os atributos do volume em cinza.
* A publicação monta o manifesto OSDU do projeto, compara cada registro com o SHA-256 do que já foi enviado e manda
  só os que mudaram: para uma pasta (um JSON numerado, gravado de forma atômica) ou para a plataforma — poços e
  trechos de poço por `PUT /api/storage/v2/records`, amostras por `POST /api/rafs-ddms/v2/masterdata`, descrições e
  análises por `POST /api/rafs-ddms/v2/samplesanalysis` e as análises de rotina como dados de conteúdo
  (`/samplesanalysis/{id}/data/{tipo}`), com os cabeçalhos `Authorization` e `data-partition-id`.

## Por script

```python
c = prj.composite_3d(mapa, vol)                       # Composite3D(labels_id, held_out={'accuracy': …}, …)
pv = rf.composite3d.property_volume(prj.raw, c.labels_id, {"Calcite": 2.71, "Quartz": 2.65}, "Grain density",
                                    "g/cm³")
prj.publication(target="folder", folder="//servidor/osdu-entrada", period_hours=24)
prj.publish()                                         # {'sent': …, 'unchanged': …, 'file': …}
```

## Limites e problemas comuns

* A composição 3D é tão boa quanto o contraste das fases na CT: fases com a mesma atenuação (calcita e dolomita em
  baixa energia) só se separam com um segundo volume (outra energia) como canal extra.
* Confira o esquema de conteúdo RAFS da plataforma (`GET /api/rafs-ddms/v2/samplesanalysis/{tipo}/data/schema`)
  antes da primeira publicação; a petrografia vai em ExtensionProperties até o RAFS ter um esquema para ela.

## Cobertura

L13 (composição 2D → tomografia → composição 3D com propriedades; contêineres, hub de modelos, incorporação periódica,
OSDU RAFS DDMS).
