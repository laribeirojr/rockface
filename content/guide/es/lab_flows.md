# RockFace Lab: flujos, la lámina entera y NetCDF

## Para qué sirve

Un **flujo** ejecuta la cadena entera — segmentación, separación en objetos, medida — en una imagen o en muchas
(todas las imágenes de una lámina, o del proyecto) de una vez, y da una tabla con una fila por muestra y archivos LAS
de los tamaños de poro por profundidad para cada pozo. **Lámina entera** segmenta una imagen completa de lámina a
resolución completa, bloque a bloque. **Importar y exportar** lee y escribe imágenes de etiquetas y archivos NetCDF
para intercambiar mapas con otros programas.

## Antes de empezar

Imágenes de las láminas en RockFace Lab; para el flujo PP/XP, la imagen XP de cada lámina; para LAS, descripciones con
pozo y profundidad.

## Paso a paso

### Un flujo

1. Abra la pestaña **Flujos**.
2. **Flujo**:
   * **PP: poros y granos** — segmentación por la resina azul, poros y granos separados y medidos;
   * **PP/XP: granos separados por los colores XP** — granos distinguidos por sus colores de extinción en nícoles
     cruzados (**XP: unir colores más cercanos que (ΔE*ab)**);
   * **Mapa mineral (QEMSCAN…): objetos de cada fase**.
3. **Imágenes de**: **esta lámina** o **todo el proyecto**; marque las imágenes a usar.
4. **Separación de poros** (watershed, SNOW, islas), **Distancia mínima entre centros**, **Objetos menores que
   (descartados)**, **Separar también los granos**.
5. **Ejecutar el flujo en las imágenes marcadas**. "Ejecutando el flujo: imagen k de n…", luego "Flujo hecho en N
   imágenes (M con errores)".
6. La tabla tiene una fila por muestra: pozo, profundidad, lámina, porosidad, las fracciones de las fases y las
   estadísticas de tamaño. Expórtela (CSV, XLSX).
7. **Curva LAS de los poros** (la columna de tamaño) y **LAS por profundidad**: un archivo LAS por pozo con el máximo,
   la media, la mediana, el mínimo y la desviación estándar de la columna y la porosidad en cada profundidad de
   muestra.

### La lámina entera

1. En **Lámina entera (sin aprendizaje automático)**, seleccione una imagen.
2. **Cuantificar la lámina entera** la segmenta a resolución completa, bloque a bloque, con el método de la pestaña
   Segmentación (métodos píxel a píxel; si no, la resina azul). "…: N píxeles contados", con la porosidad y la parte
   de cada segmento.

Para la lámina entera segmentada por una red neuronal, vea [RockFace IA: segmentar con modelos, entrenar, ajustar y validar](ai_segmentation.md).

### Importar y exportar

* **Importar una imagen de etiquetas…** (PNG, TIFF) — **Etiquetas como mapa de segmentación** o **Etiquetas como mapa
  de objetos**.
* **Exportar el mapa como etiquetas (TIFF)…**
* **Importar NetCDF…** y **Exportar la lámina como NetCDF…** — las imágenes y mapas de la lámina con su escala, origen
  y fases (NetCDF clásico; lee NetCDF-4).

## Opciones

| Opción | Qué cambia |
|---|---|
| Flujo | PP, PP/XP o mapa mineral. |
| Imágenes de | Una lámina o todo el proyecto. |
| XP: unir colores más cercanos que | Los granos cuyos colores XP difieren menos que esto son un solo grano. |
| Curva LAS de los poros | La columna de tamaño escrita en los archivos LAS. |

## Cómo funciona

* Los flujos usan las mismas funciones que las pestañas; así, un flujo da el resultado que darían las pestañas paso a
  paso.
* Los granos separados con los colores XP se encontraron con exhaustividad de 0,87–0,89, frente a 0,46–0,51 solo con
  PP, en láminas de granos conocidos.
* La lámina entera se procesa bloque a bloque con márgenes superpuestos: en una lámina de 27 Mpx el resultado fue
  idéntico al de la imagen entera de una vez, y la porosidad igual a la verdad.
* Las idas y vueltas de NetCDF y de TIFF de etiquetas son idénticas.

## Desde un script

```python
pp = prj.image("ILLUSTRATIVE mosaic PP")
r = pp.run_flow("pp")
pores, grains = r.measurements
print(r.porosity, grains.summary(exclude_edge=True)["d50_mm"])
results = prj.run_flow(prj.images(kind="slide", modality="pp"), flow="pp")
prj.flow_table(results).to_csv("por_muestra.csv")
prj.las_by_depth(results, "las", column="feret_max_um")
seg, fractions, porosity = pp.quantify_whole("resin")
prj.export_netcdf([pp, seg], "lamina.nc")
```

## Límites y problemas comunes

* "Marque al menos una imagen."
* "La lámina no tiene imagen XP para esta imagen." — el flujo PP/XP necesita las dos luces.
* Las muestras sin pozo o sin profundidad aparecen en la tabla, pero no en los archivos LAS.

## Cobertura

GT14 (LAS por profundidad, NetCDF), GT15 (flujos predefinidos PP, PP/XP, QEMSCAN), GT16 (análisis de varias imágenes),
GT17 (exportación e importación de fuentes estándar), L7 (cuantificación de la lámina entera, clásica).
