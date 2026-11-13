# Conteo de puntos

## Para qué sirve

La pestaña **Conteo de puntos** cuenta la composición en una malla de puntos sobre la lámina — por ejemplo 300
puntos — en la imagen de la lámina o con una platina motorizada. Cada punto guarda su posición en milímetros en el
sistema de la lámina: un nuevo conteo cae en los mismos puntos, cualquier punto contado puede revisitarse, y el mapa
de los puntos contados muestra la composición de la lámina. Los conteos completan la columna Puntos de la composición.

## Antes de empezar

* Una descripción con sus líneas de composición (página [Composición](composition.md)): usted cuenta *como* una de las líneas.
* Guardada al menos una vez: desde entonces cada punto contado se escribe en el proyecto al instante, y ningún punto
  se pierde ("Guarde la descripción para conservar el conteo…").
* Opcional: una imagen de la lámina (**Imagen de la lámina…**), o la imagen de la lámina entera de RockFace Atlas.

## Paso a paso

### La malla

1. Abra la pestaña **Conteo de puntos**. Deje el **Modo** en **Malla**.
2. O escriba los **Puntos deseados** (por ejemplo 300) y el **Área an × al (mm)** y pulse **Repartir N puntos**, o dé
   la malla usted mismo: **Origen x, y (mm)**, **Paso x, y (mm)** y **Columnas × filas**.
3. **Recorrido**: **Serpenteante** (ida y vuelta) o **Fila por fila**. Marque **Lámina redonda** para quedarse solo
   con los puntos dentro de una lámina redonda.
4. **Crear malla**. El mapa de la izquierda muestra los puntos.

### La imagen de la lámina

1. **Imagen de la lámina…** carga una foto de la lámina; en **Imagen y calibración** dé su **µm por píxel** y el
   **Origen de la imagen x, y (px)** (el píxel en 0, 0 mm).
2. Los puntos se dibujan sobre la imagen. Sin imagen, los puntos se dibujan solos.

### Contar

1. **Iniciar** va al primer punto. Con **Seguir** activado, cada conteo pasa al siguiente punto aún no contado.
2. Elija la línea en **Contar como** y pulse **Contar**, o pulse la tecla de la línea (1–0 y Ctrl+1–0, definidas en
   **Teclas…** de la pestaña Composición).
3. **Saltar** omite un punto (en la resina fuera de la lámina, en un agujero…); **Descontar** deshace el conteo del
   punto actual; **Volver** vuelve al punto anterior.
4. **Observación en el punto** e **Imágenes en el punto…** guardan una nota y fotos del punto bajo la cruz.
5. El contador muestra "N de M puntos contados"; los puntos de la composición acompañan al instante.

### Moverse

* Haga clic en un punto del mapa para ir a él; **Ir al punto…** por su número.
* **Ajustar**, **Acercar**, **Alejar**, la rueda del ratón; **Solo el mapa** oculta el panel.
* El recorrido seguido, el punto actual y la posición de la platina se dibujan en el mapa, con los puntos contados en
  el color de su línea.

### Con una platina motorizada (modo libre)

1. Elija la **Platina** (**Simulador (sin equipo)** para practicar) y pulse **Controlador…** para moverla con el
   teclado numérico: 8, 2, 4, 6 y las diagonales 7, 9, 1, 3.
2. **Modo → Libre**: dé el **Eje de conteo**, el **Paso (mm)**, la **Separación de traversas (mm)** e **Invertir x · y**
   para una platina montada al revés. Cada conteo mueve la platina un paso; al final del área pasa a la siguiente
   traversa.

### Coordenadas

* **Coordenadas…** lista los puntos contados como cada constituyente, con x e y en mm; **Exportar CSV…** los guarda.
* **Importar puntos…** lee puntos de un archivo CSV (x, y y la etiqueta de la línea), en mm o en píxeles con su
  tamaño.
* **Borrar conteo** olvida todos los puntos contados y conserva la malla.

## Opciones

| Campo | Qué cambia |
|---|---|
| Puntos deseados, Área | Repartir N puntos: pasos cuadrados sobre el área, exactamente N puntos. |
| Recorrido | Serpenteante o fila por fila. |
| Lámina redonda | Solo los puntos dentro de la elipse inscrita en el área de la malla. |
| Seguir | Ir al siguiente punto no contado tras cada conteo. |
| Eje de conteo, Paso, Separación de traversas | Modo libre con platina. |

## Cómo funciona

Los mismos parámetros de malla dan siempre los mismos puntos (pedido L10: posiciones nunca perdidas,
reproducibles). La malla no se puede cambiar cuando ya hay puntos contados ("Ya hay … puntos contados: la malla se
mantiene"); borre el conteo antes. Las líneas de composición que usa el conteo reciben exactamente el número de puntos
contados como ellas; las demás líneas conservan sus puntos. Los puntos contados aparecen también en RockFace Atlas,
sobre la imagen de la lámina entera, y en las figuras de la lámina.

## Desde un script

```python
d = prj["TS-9"]
q = d.add_line("quartz_mono")
c = d.add_line("calcite_dia", habit="poikilotopic", location="ig_pore_filling")
d.count.set_grid(rf.ct.grid_for(300, 20.0, 30.0))       # 300 puntos en un área de 20 × 30 mm
d.count.assign(q.uid)                                    # el punto actual contado como cuarzo; pasa al siguiente
d.count.assign(c.uid)
rf.ct.sync_points(d.composition, d.count)                # los puntos de la composición siguen al conteo
d.save()
print(d.count.counted, d.count.coordinates_by_line())
```

## Límites y problemas comunes

* "Aún no hay puntos: cree una malla o cuente en modo libre."
* "Todos los puntos están contados o saltados." — el conteo está completo.
* RockFace trae el simulador de platina; una platina motorizada de un fabricante dado necesita su controlador,
  escrito sobre la interfaz `Stage` de `rockface.core.counting` (por ejemplo como complemento).

## Cobertura

P25 (botones de la platina: Iniciar, Seguir, Saltar, Controlador), S1 (modo libre), S2 (registro del movimiento,
regreso a los puntos, ir a un punto, zoom, colores por constituyente), S3 (mapa de los puntos contados, porcentajes,
regreso a cualquier punto), L10 (una malla de puntos con coordenadas en cada lámina).
