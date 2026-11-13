# RockFace MC: segmentación, porosidad y registro de volúmenes

## Para qué sirve

La pestaña **Segmentación** corta los niveles de gris de un volumen de micro-CT en segmentos — poro y sólido, o más
fases — por cortes escritos o por el método de Otsu, limitada al cilindro de un plug cuando hace falta, y mide la
porosidad, su perfil a lo largo de un eje, la conectividad del espacio poroso y su correlación de dos puntos. La
pestaña **Registro** alinea dos volúmenes de la misma muestra y encuentra dónde está una imagen de lámina en un
volumen, añadiendo el corte correspondiente a la lámina.

## Antes de empezar

Un volumen en RockFace MC (página [RockFace MC: volúmenes de micro-CT — importación, vistas y procesamiento](mc_volumes.md)), filtrado si tiene ruido.

## Paso a paso

### Segmentar

1. Abra **Segmentación** y seleccione el volumen de gris.
2. **Cortes**: escríbalos, o déjelo vacío para Otsu (**vacío: Otsu**); **Segmentos (Otsu)** da el número de
   segmentos; **Buscar los cortes (Otsu)** los muestra en el histograma.
3. **Región**: el **volumen entero**, el **cilindro del plug** (hallado automáticamente), o **dentro de** otro volumen
   segmentado.
4. **Segmentar**. "Segmentado: porosidad … %." El segmento más oscuro es el poro. El volumen segmentado aparece bajo la
   muestra y puede ponerse sobre el de gris con **Superponer**.

### Análisis del volumen segmentado

* **Porosidad** — la porosidad de la región, y la porosidad de cada corte a lo largo de un eje (**corte a lo largo de
  x, y, z**).
* **Conectividad** — a lo largo de un eje: porosidad conectada y aislada, el número de grupos de poros, y si el espacio
  poroso atraviesa el volumen.
* **Dos puntos** — la correlación de dos puntos de los poros a lo largo de x, y y z, y la longitud de correlación de
  cada uno.

Los efectos sobre los segmentos (crecer, encoger, suavizar, operaciones lógicas con otro segmento) están en **Efectos
sobre el volumen segmentado** (página [Herramientas de volumen: filtros, sombreado, efectos del editor de segmentos, objetos, registro, análisis](volume_tools.md)).

### Registrar dos volúmenes

1. Abra **Registro**. En **Dos volúmenes de la muestra**, elija el volumen **Fijo** y el **Móvil**.
2. **Buscar el desplazamiento (correlación de fase 3D)**: "Desplazamiento encontrado: x, y, z vóxeles", guardado en el
   volumen móvil. Marque **Buscar también la rotación (sin puntos de control)** para un escaneo girado (página
   [Herramientas de volumen: filtros, sombreado, efectos del editor de segmentos, objetos, registro, análisis](volume_tools.md)).
3. **Remuestrear el volumen móvil sobre el fijo** lo escribe sobre la malla fija, vóxel a vóxel.

### Una imagen de lámina en el volumen

1. En **Una imagen de lámina en el volumen**, elija la **Imagen** (una foto o lámina de una de las láminas de la
   muestra) y **Cortes según** (el eje).
2. **Ubicar la imagen**. RockFace busca el corte que muestra la imagen, con su rotación, escala y desplazamiento:
   "Corte z = …; rotación …°, … vóxeles por píxel; ECC …".
3. **Añadir el corte a la lámina**: el corte del volumen se añade a las imágenes de la lámina en Atlas, superpuesto a
   la imagen — el enlace entre la lámina y la tomografía.

## Opciones

| Opción | Qué cambia |
|---|---|
| Cortes / Segmentos (Otsu) | Dónde se cortan los niveles de gris, escritos o por Otsu de varios niveles. |
| Región | Volumen entero, el cilindro del plug, o dentro de un volumen segmentado. |
| Cortes según | El eje según el cual se cortó la lámina del plug. |

## Cómo funciona

* La porosidad de la arenisca Berea del Imperial College London (400³ vóxeles, 5,345 µm) es 19,645 % frente al 19,6 %
  publicado; un escaneo gris simulado a partir de ella y segmentado por Otsu dio 19,54–21,06 %.
* El desplazamiento entre dos volúmenes se encuentra por correlación de fase 3D (un desplazamiento conocido encontrado
  exactamente); los puntos de control ajustan una transformación rígida, de semejanza o afín.
* Una imagen de lámina se ubica por una búsqueda de corte, ángulo y escala, refinada por el coeficiente de correlación
  mejorado: imágenes de un corte con otros tamaños de píxel y ángulos (20° a 137°) se ubicaron en el corte correcto
  dentro de 0,01–0,83 vóxel.

## Desde un script

```python
ct = prj.volume("ILLUSTRATIVE plug")
pores = ct.filter(("median", {"size": 3})).segment(roi="cylinder")          # Otsu, dos segmentos
print(pores.porosity()["porosity"], pores.connectivity("z")["percolates"])
print(pores.profile("z")[:5], pores.two_point()["length_x"])
other = prj.volume("ILLUSTRATIVE plug, second scan")
other.register(ct)                                                           # el desplazamiento automático
aligned = other.resample_on(ct)
found = prj["TS-9"].images("photo")[0].locate_in(ct, axis="z", add_slice=True)
```

## Límites y problemas comunes

* "Elija dos volúmenes distintos."
* Una imagen de lámina solo se encuentra si el volumen contiene ese corte: dé el eje según el cual se cortó la lámina.
* El cilindro de un plug se encuentra por el aire que lo rodea: en un recorte sin aire, use el volumen entero o una
  región.

## Cobertura

GV6 (segmentación), GV7 (registro), L2 (enlaces de las muestras con la tomografía), L13 en parte (imagen 2D →
tomografía).
