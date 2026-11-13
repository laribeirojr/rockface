# Del compuesto 2D al compuesto 3D, y la publicación

## Para qué sirve

El mapa mineral de una lámina dice qué es cada grano; la micro-CT del plug muestra los granos en 3D, pero no qué son.
El **compuesto 3D** lleva las fases del mapa a todo el volumen y da a cada fase sus propiedades. La **publicación**
envía el proyecto — muestras, descripciones, análisis, imágenes — al entorno corporativo de datos, con una
periodicidad, solo lo que cambió.

## Antes de empezar

* Un volumen de micro-CT de la muestra y un mapa mineral (o una segmentación) de su lámina.
* El mapa ubicado en el volumen: **MC → Registro → Ubicar la imagen** (o las dos imágenes calibradas en el marco de la
  lámina, cuando se ubicó otra imagen de la misma lámina).
* Para publicar: una carpeta vigilada por la ingesta de la plataforma, o la dirección de una plataforma OSDU y un
  token.

## Paso a paso

1. Ubique el mapa (o la foto óptica) en el volumen y guarde la posición.
2. En un script o en la ventana de scripts: `prj.composite_3d(mapa, volumen)` — las fases del mapa en el corte
   entrenan un modelo sobre el volumen en gris, un cuarto del corte queda fuera para medir la concordancia y se
   clasifica todo el volumen.
3. Dé a las fases sus propiedades: `rf.composite3d.property_volume(...)` crea un volumen numérico por propiedad.
4. Publicación: `rockface publish proyecto.rockface --folder <carpeta> --period 24` (o `--url <plataforma>`), luego
   `rockface publish proyecto.rockface --if-due` desde el programador del sistema (`--schedule` imprime las líneas).

## Opciones

| Ajuste | Significado |
|---|---|
| hold_out | parte del corte dejada fuera del entrenamiento para medir la concordancia (0,25 por defecto) |
| method | bosque aleatorio o modelo bayesiano gaussiano |
| target | `folder` (archivos de manifiesto) o `rafs` (OSDU Storage + RAFS DDMS) |
| period_hours | cada cuántas horas publica `--if-due` |
| token_env | la variable de entorno con el token de acceso (ROCKFACE_OSDU_TOKEN); nunca se guarda |
| analysis_type, content_version | tipo de contenido RAFS y versión del esquema de los análisis de rutina |

## Cómo funciona

* El mapa se muestrea en cada vóxel del corte ubicado mediante la matriz de la posición; las fases de fondo no
  entrenan. El modelo es el bosque aleatorio de MC con los atributos del volumen en gris.
* La publicación arma el manifiesto OSDU del proyecto, compara cada registro con el SHA-256 de lo ya enviado y manda
  solo lo que cambió: a una carpeta (un JSON numerado, escrito de forma atómica) o a la plataforma — pozos y tramos
  por `PUT /api/storage/v2/records`, muestras por `POST /api/rafs-ddms/v2/masterdata`, descripciones y análisis por
  `POST /api/rafs-ddms/v2/samplesanalysis` y los análisis de rutina como datos de contenido
  (`/samplesanalysis/{id}/data/{tipo}`), con los encabezados `Authorization` y `data-partition-id`.

## Desde un script

```python
c = prj.composite_3d(mapa, vol)                       # Composite3D(labels_id, held_out={'accuracy': …}, …)
pv = rf.composite3d.property_volume(prj.raw, c.labels_id, {"Calcite": 2.71, "Quartz": 2.65}, "Grain density",
                                    "g/cm³")
prj.publication(target="folder", folder="//servidor/osdu-entrada", period_hours=24)
prj.publish()                                         # {'sent': …, 'unchanged': …, 'file': …}
```

## Límites y problemas comunes

* El compuesto 3D es tan bueno como el contraste de las fases en la CT: fases con la misma atenuación (calcita y
  dolomita a baja energía) solo se separan con un segundo volumen (otra energía) como canal extra.
* Verifique el esquema de contenido RAFS de la plataforma (`GET /api/rafs-ddms/v2/samplesanalysis/{tipo}/data/schema`)
  antes de la primera publicación; la petrografía va en ExtensionProperties hasta que RAFS tenga un esquema para ella.

## Cobertura

L13 (compuesto 2D → tomografía → compuesto 3D con propiedades; contenedores, hub de modelos, incorporación periódica,
OSDU RAFS DDMS).
