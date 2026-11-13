# Archivos de los programas de referencia

## Para qué sirve

RockFace abre los archivos que entregan GeoSlicer y los laboratorios, sin convertirlos antes: volúmenes de micro-CT de
Amira/Avizo, HDF5, series DICOM y reconstrucciones TESCAN; láminas escaneadas Zeiss CZI; escenas y segmentaciones de
GeoSlicer; las tablas de informes de laboratorio en PDF; y la barra de escala grabada en una foto de microscopio.

## Antes de empezar

* Un proyecto con una muestra (volúmenes) o una lámina (imágenes).
* Paquetes opcionales, instalados una vez: `pip install rockface[formats]` (HDF5, DICOM, PDF, OCR) y, para CZI,
  `pip install rockface[czi]`. El OCR también necesita el programa Tesseract.

## Paso a paso

1. **Volúmenes — MC → Importar.** Elija el archivo o la carpeta: `.am`, `.h5`/`.hdf5`, un `.dcm` o una carpeta DICOM,
   una carpeta TESCAN (con `*.acq.1.xml` y `recon/`), o una escena `.mrml` o segmentación `.seg.nrrd` de GeoSlicer.
   Haga clic en **Importar**.
2. **Salida de volúmenes — MC → Volumen → Exportar** ahora también escribe `.am`, `.h5` y, para una segmentación,
   `.seg.nrrd`.
3. **CZI — Atlas → Importar imágenes** un `.czi` como cualquier lámina.
4. **Informe — Petro → Inicio → Importar informe de laboratorio (PDF)…**: elija el PDF, el pozo y la tolerancia de
   profundidad; cada fila pasa a ser un análisis petrofísico convencional de la muestra a esa profundidad.
5. **Barra de escala — Atlas → propiedades de la imagen → Leer barra de escala**: se encuentra la barra y se lee su
   longitud; si el texto no se puede leer, escriba la longitud.

## Opciones

| Formato | Lo que RockFace lee |
|---|---|
| Amira `.am` | binario (little o big endian) o ASCII; de byte a double; crudo, HxByteRLE o HxZip; vóxel por BoundingBox y Units |
| HDF5 | cualquier conjunto 3D (el mayor por defecto); vóxel por `voxel_um`, `spacing` + `units`, `element_size_um` |
| DICOM | la mayor serie de la carpeta, cortes ordenados por su normal, unidades Hounsfield; no se guarda ningún campo del paciente |
| TESCAN | los cortes de `recon/`, vóxel = VoxelSize (mm) de `*.rec.1.xml`, origen de `*.acq.1.xml` |
| `_NNNNNnm` en el nombre | tamaño del vóxel en nanómetros cuando el archivo no lo da |
| CZI | la primera escena, RGB o gris, µm por píxel por la escala del archivo |
| `.mrml`, `.seg.nrrd` | volúmenes, mapas de etiquetas y segmentaciones (3D o en capas) con nombres y colores de los segmentos |
| Informe en PDF | profundidad, diámetro, longitud, masa, permeabilidad, porosidad, densidad de granos (encabezados en PT, EN, ES; coma o punto) |

## Cómo funciona

* Cada lector convierte el archivo en una fuente de volumen leída por bloques, así los archivos grandes no ocupan la
  memoria; el vóxel viene del archivo, si no del nombre, si no del formulario de importación.
* Informes: las tablas con líneas se leen por sus líneas; las de texto alineado, por las columnas de los números; los
  encabezados se reconocen por sus palabras (*Profundidade*, *Permeabilidade*, *Massa específica*…).
* Barra de escala: la barra horizontal sólida más larga que contrasta con su entorno; luego el texto junto a ella,
  leído por Tesseract ("500 µm", "0,5 mm"); µm por píxel = longitud ÷ píxeles de la barra.

## Desde un script

```python
src = rf.volume.open_volume("scan.am")                        # o .h5, una carpeta DICOM o TESCAN
v = rf.volume.add_volume(prj.raw, src, sample_id)
rf.volume.export(prj.raw, v.id, "salida.seg.nrrd")            # un volumen de etiquetas para GeoSlicer
rf.geoslicer.import_scene(prj.raw, "proyecto.mrml", sample_id)
prj.import_lab_report("rca.pdf", "ILL-WELL-1", tolerance_m=0.1)
rf.atlas.read_scale_bar(prj.raw, image_id)                    # Scale(bar, text, value_um, um_per_px)
```

## Límites y problemas comunes

* CZI necesita pylibCZIrw (LGPL-3.0, opcional, como OpenSlide para otros formatos de lámina).
* Un informe cuya tabla es una imagen (escaneada) no tiene texto: pase un OCR al PDF antes.
* Sin unidades, el BoundingBox de Amira se interpreta por el tamaño del vóxel (metros, milímetros o micrómetros); la
  elección queda en el historial del volumen.

## Cobertura

Formatos GV1 y GT1 (0.28), GC1 DICOM, tablas de informes, barra de escala; auditoría de GeoSlicer de 0.28.
