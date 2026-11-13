# RockFace Atlas: láminas enteras, fotos de detalle y la biblioteca de imágenes

## Para qué sirve

RockFace Atlas guarda las imágenes de cada lámina: imágenes de la lámina entera de cualquier tamaño (la lámina de
varios gigapíxeles de un escáner, un mosaico de microscopio) en varias luces, y fotos de detalle ubicadas en su
posición exacta en la lámina, con la posición de la platina donde se tomaron. La **biblioteca de imágenes** encuentra
cualquier imagen del proyecto por su nombre, leyenda, pozo, lámina, tipo, luz u objetivo, y el visor va de la lámina
entera a la resolución completa al instante.

## Antes de empezar

* Una descripción **guardada**: las imágenes pertenecen a su lámina ("Guarde primero una descripción: las imágenes
  pertenecen a su lámina.").
* Archivos de imagen: PNG, JPEG, TIFF, BigTIFF, OME-TIFF, BMP, GIF, WebP; formatos de escáner (SVS, NDPI, MRXS, SCN)
  con OpenSlide instalado; Zeiss CZI con el extra `czi`.

## Paso a paso

### Abrir Atlas

**Inicio → Imágenes → Atlas** (Ctrl+Shift+A) en RockFace Petro abre Atlas en el mismo proyecto y lámina; o
`rockface atlas proyecto.rockface`.

### Importar una lámina entera

1. **Importar…** (Ctrl+I) y elija los archivos.
2. En **Importar imágenes**, revise la **Lámina delgada**, el **Tipo** (lámina entera), la **Categoría** (mosaico de
   microscopio, escáner de láminas, fotomicrografía, foto macroscópica, otra) y la **Luz / señal** (luz polarizada
   plana, nícoles cruzados, luz reflejada, catodoluminiscencia, ultravioleta, fluorescencia, MEB, otra).
3. Escala: **µm por píxel** — del archivo cuando la trae, si no escrita, si no del **Objetivo** y de la tabla de
   **Objetivos…**.
4. **Teselas**: **JPEG (fotografías; menor)** o **PNG (sin pérdida; mapas)**.
5. **Aceptar**. "Construyendo la pirámide de la imagen…" muestra el avance; una imagen muy grande tarda, una sola vez.

### Fotos de detalle

1. **Foto de detalle…**: elija la foto, su **Objetivo**, la luz y, cuando se conocen, su **Posición x, y (mm)** en la
   lámina y la **Platina x, y (mm)** donde se tomó.
2. O ubíquela después: selecciónela en **Fotos de detalle**, elija la herramienta **Ubicar foto** y haga clic donde
   está en la lámina entera.
3. **Mostrar en la lámina** encuadra el campo de la foto; **Abrir** muestra la foto misma; **Platina a este campo**
   envía la platina (o el simulador) de vuelta a donde se tomó.
4. **Volver a fotografiar…** añade una nueva foto del mismo campo, con la misma posición, posición de platina y
   objetivo, ligada a la primera ("N fotos de este campo").

### El visor

* Arrastre para moverse; la rueda del ratón acerca y aleja. **Ajustar**, **1:1**, **Acercar**, **Alejar**.
* **Encima:** superpone otra imagen de la lámina a la abierta (XP sobre PP, CL, un mapa mineralógico), con la
  **Opacidad de la imagen superpuesta**.
* Muestre u oculte las **Fotos** (los campos de las fotos de detalle, numerados), la **Escala**, la **Vista general** y
  el contorno de la **Lámina redonda**.
* **Puntos contados de:** muestra los puntos contados en una descripción, coloreados por constituyente (página
  [Conteo de puntos](point_counting.md)).
* **Herramientas**: **Medir** (clic en dos puntos: la distancia en µm), **Calibrar** (clic en dos puntos y dé su
  distancia: fija la escala), **Ubicar foto**, **Punto** (página [Análisis puntuales: geoquímica, datación e inclusiones fluidas](spot_analyses.md)).
* **Exportar vista…** guarda lo que se muestra, o la imagen entera, en PNG, JPEG o TIFF.

### La biblioteca de imágenes

1. La **Biblioteca de imágenes** lista todas las imágenes del proyecto. Escriba en **Buscar nombres, leyendas, pozos,
   láminas…**.
2. **Filtros**: tipo, categoría, luz, objetivo y **Pozo o afloramiento**; **Solo esta lámina**.
3. **Por concepto** encuentra imágenes por lo que muestran sus anotaciones (página [Anotaciones del Atlas y la búsqueda por concepto](atlas_annotations.md)).
4. Seleccione una imagen para ver y editar su **Nombre**, tipo, categoría, luz, objetivo, escala y **Leyenda**;
   **Guardar cambios**. **Leer barra de escala** encuentra la barra de escala grabada en una foto y lee su longitud
   (OCR).
5. **Eliminar imagen** borra la imagen y sus teselas del proyecto.

## Opciones

| Campo | Qué cambia |
|---|---|
| Objetivos… | µm por píxel de la cámara con cada objetivo, medido una vez en un micrómetro de platina. |
| Teselas | JPEG (menor, para fotografías) o PNG (sin pérdida, para mapas y etiquetas). |
| Posición x, y (mm) | Dónde está la foto en la lámina (su centro), en el sistema de la lámina. |
| Platina x, y (mm) | Dónde estaba la platina cuando se tomó la foto (para volver a ella). |

## Cómo funciona

Cada imagen se guarda en el proyecto como una pirámide de teselas: solo se leen las teselas que están en pantalla, en
el nivel que corresponde al zoom, por lo que una lámina de 2 gigapíxeles se abre en una fracción de segundo y se mueve
sin esperas. Toda imagen tiene su lugar en el sistema de la lámina (milímetros), compartido con el conteo de puntos,
las anotaciones, los mapas mineralógicos y los análisis puntuales: lo que está en un punto de una imagen está en el
mismo punto de las otras.

## Desde un script

```python
d = prj["TS-9"]
slide = d.add_image("TS-9_PP.tif", category="scanner", modality="pp")
photo = d.add_photo("campo1.jpg", x_mm=4.2, y_mm=3.6, magnification=10, stage_x_mm=31.2, stage_y_mm=24.6)
slide.overview("TS-9_campos.png", width=2400)              # la lámina con los campos de las fotos numerados
crop = slide.region(*slide.to_px(4.0, 3.4), 400, 300)      # un array NumPy a resolución completa
for img in prj.images(kind="photo", modality="xp", well="ILLUSTRATIVE W-1"):
    print(img.name, img.um_per_px, img.x_mm, img.y_mm)
prj.objectives = {"10": 0.65, "20": 0.325}                 # µm por píxel de cada objetivo
```

## Límites y problemas comunes

* "Esta lámina no tiene imagen de lámina entera." — las fotos se pueden importar igual, y ubicar después.
* "No se conoce la posición de platina de esta foto." — Platina a este campo necesita la posición de platina.
* "Una escala necesita dos puntos distintos y una longitud mayor que cero."
* Para llevar varios gigabytes de imágenes a otro proyecto, **Guardar proyecto como…** es más rápido que un archivo de
  intercambio.

## Cobertura

R1 (base de fotomicrografías con consultas rápidas), GT1 (imágenes de láminas con escala), GT21 (CZI y la barra de
escala), L6 (fotos tomadas de nuevo en la misma posición referenciada).
