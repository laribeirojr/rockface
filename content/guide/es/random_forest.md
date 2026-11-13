# Segmentar por ejemplos pintados (bosque aleatorio)

## Para qué sirve

Algunas fases no se distinguen por un color o un valor de gris: un cemento con el color de los granos, vúgulos con el
gris medio de la matriz. Usted pinta algunos píxeles (o vóxeles) de cada segmento, y el programa aprende de la imagen
**alrededor** de ellos —suavidad, textura, bordes— y clasifica toda la imagen o todo el volumen. Cada trazo nuevo lo
entrena de nuevo y la vista previa cambia enseguida, así que usted corrige donde se equivoca.

Funciona en **RockFace Lab**, en imágenes de lámina, y en **RockFace MC**, en volúmenes de micro-CT.

## Antes de empezar

* Lab: una imagen de una lámina (una imagen con nícoles cruzados de la misma lámina puede entrar como segunda imagen,
  si está registrada sobre la primera o si ambas tienen el referencial de la lámina).
* MC: un volumen en gris. En un volumen grande, recorte antes una parte representativa (**Volumen → Recortar**) para
  pintar y ver rápido; después el modelo se aplica a todo el volumen.

## Paso a paso

### En Lab (imágenes)

1. Abra la imagen y vaya a la pestaña **Segmentación**.
2. En **Método**, elija **Bosque aleatorio (ejemplos pintados)**. Se proponen dos segmentos (poro y sólido):
   cámbieles el nombre y añada otros con **Añadir segmento**.
3. Acerque una parte representativa de la imagen: la vista previa se calcula sobre la parte que está en pantalla.
4. Elija un segmento en la tabla, pulse **Pintar ejemplos del segmento elegido** y pinte algunos trazos sobre él.
   Haga lo mismo con cada segmento. Pinte los bordes y los lugares fáciles de confundir.
5. Con **Actualizar la vista previa tras cada trazo (la parte de la imagen en pantalla)** marcado, la vista previa
   sigue cada trazo. Mire dónde se equivoca y pinte ahí.
6. Pulse **Aplicar a toda la imagen** para clasificar toda la imagen en el tamaño de píxel en que entrenó, bloque a
   bloque, o **Guardar la segmentación como mapa** para guardar solo la parte calculada.

### En MC (volúmenes)

1. Abra el volumen en gris y vaya a la pestaña **Bosque aleatorio**.
2. Escriba los segmentos en **Segmentos (separados por ;)** (por ejemplo `Vúgulo; Matriz`) y pulse **Nueva anotación
   en este volumen**. La anotación aparece sobre los cortes.
3. Elija el segmento en **Pintar con**, el **Radio del pincel**, y pulse **Pintar en los cortes**. Arrastre el ratón
   en cualquiera de las tres vistas de corte. **— borrador —** borra; **Deshacer** quita el último trazo. Marque
   **Esfera (también los cortes vecinos)** para pintar también los cortes vecinos.
4. Pinte algunos vóxeles de cada segmento, en varios cortes.
5. **Entrenar y previsualizar (corte z actual)** muestra el resultado en una ventana del corte actual; con **Entrenar
   de nuevo y previsualizar tras cada trazo**, sigue cada trazo.
6. Pulse **Aplicar a todo el volumen**. El resultado es un volumen segmentado nuevo, con su porosidad.

## Opciones

* **Atributos** — lo que mira el bosque, como en el Interactive Segmenter de GeoSlicer:
  * *Nítido (detalles finos)*: el valor, gaussiana σ 1 y 2, varianza local 5 × 5;
  * *Equilibrado*: el valor, gaussiana 1, 2, 4, varianza 5 y 9 — un buen comienzo;
  * *Suave* y *Muy suave*: escalas mayores, segmentos más suaves;
  * *Completo (todos los atributos)*: todos, más el gradiente y el laplaciano.
* **Árboles** — más árboles, un resultado más estable (32 basta casi siempre).
* **Segunda imagen / Segundo volumen (misma malla)** — más canales en la misma malla (la imagen XP de una lámina).
* **Método** (MC) — *Bosque aleatorio* o *Inferencia bayesiana (gaussiana)* (cada segmento una distribución normal
  de los atributos).
* **Modelo** — *Entrenar con los ejemplos pintados*, o un modelo guardado en el proyecto. Todo modelo aplicado queda
  guardado en el proyecto; **Exportar modelo…** lo escribe en un archivo `.rfmodel` e **Importar modelo…** lee uno (de
  un colega, por ejemplo).

## Cómo funciona

* Para cada píxel o vóxel, los atributos del conjunto elegido se calculan en cada canal (L\*, a\*, b\* de una imagen
  en color; el gris de un volumen). Un bosque aleatorio (Breiman 2001) de árboles de decisión aprende de los puntos
  pintados qué atributos separan los segmentos; cada punto recibe el segmento votado por la mayoría de los árboles.
* Un atributo depende solo de los puntos en un margen a su alrededor; por eso la imagen se clasifica bloque a bloque
  con ese margen y el resultado es igual al de toda la imagen de una vez, sea cual sea su tamaño.
* Un modelo se guarda como números (los nodos de los árboles), nunca como código de programa: un modelo recibido de
  otra persona se puede abrir con seguridad.
* Fuente: L. Breiman (2001), *Random forests*, Machine Learning 45, 5–32; los conjuntos de atributos siguen el manual
  de GeoSlicer.

## Desde un script

```python
import rockface.api as rf
prj = rf.open("proyecto.rockface")
pp = prj.image("ILLUSTRATIVE mosaic PP")
seg, bosque = pp.forest(strokes=[(1, [(120, 80), (140, 90)], 6), (2, [(600, 420)], 6)],
                        segments=["Poro", "Sólido"], preset="balanced")
toda, fracciones, porosidad = pp.apply_forest(bosque)
vol = prj.volume("Plug A")
anot = vol.new_annotation(["Vúgulo", "Matriz"])
anot.paint("z", 40, [(30, 30), (36, 30)], 2.0, 1)
f3 = vol.train_forest(anot, name="Vúgulos")
seg3 = vol.apply_forest(f3)
```

## Límites y problemas comunes

* **"Pinte ejemplos de al menos dos segmentos."** Cada segmento necesita algunos trazos.
* **La vista previa está bien y toda la imagen no.** Los trazos vinieron de una sola parte; pinte otras partes también.
* **"El modelo se entrenó con … canales"**: un modelo entrenado con segunda imagen la necesita ahora.
* En Lab, la vista previa y el entrenamiento usan los trazos que están en pantalla; los de fuera quedan guardados para
  después.
* Las redes preentrenadas de GeoSlicer (U-Net) llegan en la etapa 0.26.

## Cobertura

GV6, GT7, GT8 (Interactive Segmenter, Segmenter — métodos bosque aleatorio y bayesiano).
