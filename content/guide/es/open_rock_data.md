# Datos abiertos de rocas: imágenes públicas de micro-CT

## Para qué sirve

Para probar RockFace MC, comparar métodos o enseñar sin imágenes propias: imágenes públicas de micro-CT de areniscas y
carbonatos, descargadas e importadas en una muestra con su licencia y su cita.

## Antes de empezar

* Un proyecto con al menos una muestra (una descripción), y conexión a Internet.
* Espacio en disco: una imagen de 1000³ vóxeles ocupa cerca de 1 GB, y el archivo de 2015 del Imperial College varios
  GB.

## Paso a paso

1. En RockFace MC, pestaña **Importar**, pulse **Datos abiertos de rocas (imágenes públicas)…**.
2. Elija una imagen en la tabla (colección, roca, imagen, tamaño, licencia). Debajo de la tabla: la cita, la licencia,
   el tamaño de la descarga y la página de la fuente. **Lea la licencia antes de usar los datos, y cite la fuente.**
3. Elija la **Muestra** que recibe el volumen y la **Carpeta de descarga**.
4. Pulse **Descargar e importar**. El archivo se descarga una vez (una segunda importación lo reutiliza) y se importa
   como un volumen de la muestra; su leyenda guarda la cita y la licencia.

## Opciones

* **Eleven Sandstones** (Digital Rocks Portal): once areniscas a 2,25 µm, 1000³ vóxeles, en tres formas — gris,
  filtrada y binaria. Licencia ODC-BY 1.0.
* **ICL sandstones and carbonates 2009** (Imperial College London): imágenes binarias del Berea, de las areniscas S y
  LV60 y de carbonatos, en archivos 7-Zip (se necesita el paquete `py7zr` para abrirlos).
* **ICL micro-CT 2015** (Imperial College London): Bentheimer, Doddington, Estaillades y Ketton, 1000³, gris, en un
  archivo de varios gigabytes.

## Cómo funciona

La lista de imágenes, direcciones, tamaños y tamaños de vóxel sigue la biblioteca `drd` de L. Mosser (Apache 2.0), que
usa GeoSlicer; los archivos se descargan a través de un archivo temporal `.part` y se importan fuera de la memoria, un
bloque a la vez.

## Desde un script

```python
for e in rf.ProjectAPI.rock_data()[:3]:
    print(e.id, e.rock, e.licence)
v = prj.download_rock_data("eleven/Berea/binary", prj.descriptions()[0], folder="datos")
```

## Límites y problemas comunes

* **"Falló la descarga de …"** — sin conexión, o la fuente movió el archivo; inténtelo más tarde o descárguelo desde
  la página de la fuente e impórtelo en **Importar** (RAW, 1000 × 1000 × 1000, 8 bits).
* **"Este archivo está en formato 7-Zip"** — instale `py7zr` (`pip install py7zr`).
* Las imágenes binarias se importan como volúmenes de gris con dos valores: segméntelas con un umbral (pestaña
  Segmentación).

## Cobertura

GV17 (Open Rock Data).
