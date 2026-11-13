# RockFace Lab: recorte, filtros y la máscara de la muestra

## Para qué sirve

RockFace Lab prepara las imágenes de una lámina para el análisis. **Recortar** corta todas las imágenes de la lámina
con el mismo rectángulo, conservando su lugar en la lámina. **Filtros** mejoran una imagen — brillo y contraste,
saturación, gamma, niveles, ecualización del histograma, corrección de sombreado, suavizado, realce — con vista previa.
La **Máscara** encuentra el área útil de la lámina (la roca, sin el vidrio ni los bordes) y la separa en fragmentos.

## Antes de empezar

* Una lámina con imágenes en RockFace Atlas (página [RockFace Atlas: láminas enteras, fotos de detalle y la biblioteca de imágenes](atlas_viewer.md)).
* Abra Lab: **Inicio → Imágenes → Lab** (Ctrl+Shift+L) en RockFace Petro, o `rockface lab proyecto.rockface`.

## Paso a paso

### La ventana

* **Lámina:** arriba elige la lámina; **Imágenes de la lámina** lista sus imágenes (las originales y las hechas por
  Lab, con lo que las hizo).
* El visor muestra la imagen seleccionada: **Ajustar**, **1:1**, **Acercar**, **Alejar**.
* Las pestañas de la derecha: **Recortar**, **Filtros**, **Máscara**, **Registro**, **Calculadora**, **Segmentación**,
  **Edición y objetos**, **Medidas**, **Flujos**, **IA**.

Cada herramienta escribe una **nueva imagen** de la lámina; la original nunca se modifica.

### Recortar

1. Abra **Recortar**. Dé el rectángulo en el sistema de la lámina: **Izquierda (mm)**, **Arriba (mm)**, **Derecha
   (mm)**, **Abajo (mm)**, o:
   * **Dibujar en la imagen** — arrastre un rectángulo;
   * **Imagen entera**; **Caja de la máscara**;
   * un rectángulo de las **Regiones guardadas** o de las **Últimas usadas**.
2. **Nombre de la región** y **Guardar región** lo guardan para las próximas láminas; **Borrar región**.
3. En **Imágenes a recortar**, marque las imágenes (PP, XP, un mapa…). Cada una se recorta en la parte que cubre.
4. **Recortar las imágenes marcadas**. "N imagen(es) recortada(s) añadida(s)."

### Filtros

1. Abra **Filtros** y elija la imagen.
2. **Añadir** un filtro a la lista:
   * **Brillo y contraste**, **Saturación**, **Gamma**;
   * **Niveles automáticos** (**Percentil bajo** y **Percentil alto**, canales juntos o cada uno);
   * **Ecualización del histograma**;
   * **Corrección de sombreado** (iluminación desigual: **Referencia** resina, claro, todo, máscara o plana; **Grado
     de la superficie**; **Ganancia máxima**);
   * **Suavizado gaussiano** (**Sigma (px)**), **Filtro de mediana** (**Tamaño (px)**), **Máscara de desenfoque
     (realzar)** (**Sigma**, **Cantidad**);
   * **Pintar fuera de la muestra** (con una máscara en **Imagen** y su **Relleno**).
3. Los filtros se aplican en orden: **Subir**, **Bajar**, **Quitar**, **Deshacer**, **Rehacer**. El visor muestra el
   resultado al instante; **Mostrar el original** compara.
4. **Nombre de la nueva imagen** y luego **Escribir como nueva imagen**. "Imagen filtrada añadida: …".

### Máscara de la muestra

1. Abra **Máscara**. La máscara se encuentra **por color (resina azul)** o **por muestras dibujadas**: **Dibujar
   muestra de roca** y **Dibujar muestra de resina** en la imagen.
2. **Separar en fragmentos** por la resina entre ellos: **Resina más ancha que**, **Conservar los mayores** (N
   fragmentos, o todos), **Suavizado**, **Área mínima**.
3. **Hallar la muestra**. "Muestra: …% de la imagen, N fragmento(s)". "No se halló vidrio ni borde: toda la imagen es
   la muestra." cuando la imagen es toda roca.
4. **Nombre de la máscara** y luego **Guardar la máscara**. La máscara la usan el Recorte (**Caja de la máscara**),
   **Pintar fuera de la muestra**, la segmentación y las medidas.

## Opciones

| Opción | Qué cambia |
|---|---|
| Corrección de sombreado — Referencia | Qué debe quedar uniforme: la resina, las zonas claras, toda la imagen, una máscara, o una imagen de campo plano. |
| Niveles automáticos — Canales | Estirar los tres canales juntos (conserva los colores) o cada uno aparte. |
| Resina más ancha que | La franja de resina más estrecha que separa dos fragmentos (fracción del lado menor). |

## Cómo funciona

* Brillo, contraste y saturación dan exactamente lo que da ImageEnhance de Pillow, y la ecualización del histograma de
  la luminancia exactamente lo que da OpenCV (comprobado en 26 imágenes, 20 de ellas recortes de láminas reales).
* Los filtros se aplican bloque a bloque: una lámina entera de cualquier tamaño se filtra con poca memoria, y el
  resultado es el mismo que filtrar la imagen entera de una vez.
* La corrección de sombreado ajusta una superficie polinómica a la referencia (la resina, por defecto) y la divide:
  una desigualdad de 0,086–0,130 volvió a 0,021 en láminas de prueba.
* La máscara encuentra el vidrio y los bordes por color y textura; en láminas PP y XP coincidió con la máscara
  verdadera con IoU de 0,97–0,9996.

## Desde un script

```python
pp, xp = prj.image("ILLUSTRATIVE mosaic PP"), prj.image("ILLUSTRATIVE mosaic XP")
pp_c, xp_c = prj.crop([pp, xp], roi=(2.0, 2.0, 8.0, 6.0))          # mm del sistema de la lámina
mejor = pp_c.filter(["shading", ("brightness_contrast", {"contrast": 20}), ("unsharp", {"sigma": 1.5})])
mask = pp.sample_mask(split=True, n_largest=2)
print(mask.areas_mm2())
prj.save_roi("Centro", (2.0, 2.0, 8.0, 6.0))
```

## Límites y problemas comunes

* "Indique un rectángulo para recortar." / "Marque al menos una imagen."
* "La lámina aún no tiene máscara (pestaña Máscara)."
* En una lámina sin resina azul, encuentre la máscara **por muestras dibujadas**.

## Cobertura

GT3 (recorte), GT4 (filtros de realce), GT6 (área útil de la muestra: fragmentos, conservar los N mayores).
