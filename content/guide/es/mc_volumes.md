# RockFace MC: volúmenes de micro-CT — importación, vistas y procesamiento

## Para qué sirve

RockFace MC guarda los volúmenes de micro-CT de cada muestra — un plug, un testigo entero, un frasco de recortes de
perforación — junto a sus láminas y descripciones. Importa los formatos usuales, guarda volúmenes de cualquier tamaño
fuera de la memoria, los muestra en tres cortes y en 3D, y los recorta, filtra, remuestrea, combina y exporta. Cada
operación escribe un nuevo volumen con su historial; el original nunca se modifica.

## Antes de empezar

* Una descripción guardada: un volumen pertenece a la muestra de la descripción (y puede ligarse a una de sus
  láminas).
* Abra MC: **Inicio → Imágenes → MC** (Ctrl+Shift+M) en RockFace Petro, o `rockface mc proyecto.rockface`.

## Paso a paso

### La ventana

* **Volúmenes** a la izquierda, por muestra (y los pozos con sus perfiles, página [RockFace MC: perfiles de imagen](mc_image_logs.md)); seleccione uno
  para mostrarlo.
* Tres vistas de cortes (x, y, z) y la **Vista 3D** (**proyección de máximos**, **proyección media**, o **apagada**).
  Haga clic en un corte para mover los demás; el estado muestra "Vóxel x, y, z: valor".
* **Ventana** (niveles de gris mostrados) y **Ventana automática**; **Superponer** pone un volumen segmentado sobre el
  de gris.
* Las pestañas: **Importar**, **Volumen**, **Segmentación**, **Registro**, **Testigos**, **Perfiles**, **Bosque
  aleatorio**, **Análisis**, **Red de poros**, **Microporosidad**, **Multiescala**, **IA**, **Más**.

### Importar un volumen

1. Abra **Importar**. **Archivo…** o **Carpeta…**: una carpeta de cortes, una carpeta TESCAN o DICOM, un TIFF de
   varias páginas, RAW, MetaImage (.mhd/.mha), NRRD, NetCDF, HDF5, Amira (.am) o ASCII del Imperial (.dat).
2. Para RAW: **Tamaño (RAW)** en vóxeles, **Tipo (RAW)**, **Orden de bytes (RAW)** (little- o big-endian) y
   **Encabezado a saltar (RAW)**. Los demás formatos lo dicen en su encabezado.
3. **Tamaño del vóxel** (del archivo, o escrito en µm).
4. **Contenido**: **niveles de gris** o **segmentado**; para un volumen segmentado, **Valores y segmentos** asocia cada
   valor del archivo a un segmento.
5. **Muestra** y, opcionalmente, la **Lámina**; el **Nombre**.
6. **Importar**. "… importado: nx × ny × nz vóxeles."

Las imágenes públicas de micro-CT se pueden descargar con su licencia: **Datos abiertos de rocas (imágenes
públicas)…** (página [Datos abiertos de rocas: imágenes públicas de micro-CT](open_rock_data.md)).

### Procesar (la pestaña Volumen)

* **Recortar (vóxeles, de – a)** en x, y y z, y luego **Recortar**.
* **Filtros**: **Filtrar** (gaussiano, mediana, media, máscara de enfoque, ventana a 8 bits, invertir, difusión
  anisotrópica) con sus parámetros, **Añadir** a la lista, **Limpiar**, **Aplicar**. Los filtros se aplican bloque a
  bloque.
* **Corrección de sombreado (corte a corte)** — página [Herramientas de volumen: filtros, sombreado, efectos del editor de segmentos, objetos, registro, análisis](volume_tools.md).
* **Remuestrear**: **Nuevo tamaño de vóxel**, **Interpolación** (vecino más cercano, lineal, cúbica), **Remuestrear**.
* **Calculadora de volúmenes**: una **Fórmula** sobre los volúmenes del mismo tamaño (listados en "Volúmenes de este
  tamaño:"), por ejemplo `(a − b) / 2` o `a > 120` (una condición da un volumen segmentado 0/1); **Calcular**.
* **Exportar**: **Exportar…** a .mhd (+ .raw), .mha, .nrrd, .tif o .nc, con el tamaño del vóxel.
* **Eliminar volumen** (no se puede deshacer).

## Opciones

| Opción | Qué cambia |
|---|---|
| Contenido | Niveles de gris, o segmentado (etiquetas con sus segmentos). |
| Interpolación | Vecino más cercano para volúmenes segmentados; lineal o cúbica para niveles de gris. |
| Ventana | Solo la visualización; los valores guardados no cambian. |

## Cómo funciona

Los volúmenes se guardan en el proyecto como bloques comprimidos de 64³ vóxeles con una pirámide de niveles reducidos a
la mitad; así, las vistas leen solo lo que muestran, y un volumen mayor que la memoria se procesa un bloque cada vez:
403 millones de vóxeles se importaron y segmentaron con alrededor de 1 GB de memoria. Los filtros bloque a bloque son
iguales al volumen entero de una vez; cinco formatos se leyeron de vuelta idénticos.

## Desde un script

```python
d = prj["TS-9"]
ct = d.import_volume("plug.mhd")                               # o prj.import_volume(ruta, d, voxel_um=5.0)
small = ct.crop((0, 400, 0, 400, 0, 400)).resample(factor=0.5)  # caja (z0, z1, y0, y1, x0, x1) en vóxeles
smooth = ct.filter(("median", {"size": 3}), ("gaussian", {"sigma": 0.8}))
diff = prj.calculate_volumes("a - b", {"a": ct, "b": smooth}, name="residuo")
print(ct.shape, ct.voxel_um)                                    # (nz, ny, nx), µm
smooth.export("plug_suave.nrrd")
```

## Límites y problemas comunes

* "Elija un archivo o carpeta y una muestra."
* Un archivo RAW leído con el tamaño o el tipo equivocado parece ruido: revise el tamaño, el tipo y el orden de bytes.
* Las importaciones muy grandes tardan; se muestra el avance y el trabajo puede cancelarse.

## Cobertura

GV1 (importación), GV2 (exportación), GV3 (recorte), GV4 (filtros), GV5 (remuestreo), GV8 (imágenes grandes fuera de
la memoria), GV14 (calculadora de volúmenes), L2 (enlaces de las muestras con la tomografía).
