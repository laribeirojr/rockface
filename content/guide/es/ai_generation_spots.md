# RockFace IA: modelo generativo de un volumen (SinGAN) y el ciclo de puntos

## Para qué sirve

**Generar imágenes de roca.** A partir de un volumen de entrenamiento — un volumen de micro-CT segmentado o de grises —
una red generativa aprende su textura y hace tantos volúmenes nuevos como usted quiera, del mismo tamaño o mayores, con
la misma porosidad y los mismos tamaños de poro, para simulaciones que necesitan varias realizaciones o un volumen
mayor que la tomografía. Está junto a la generación por MPS de 0.25 (pestaña Multiescala).

**El ciclo de puntos.** Cuando algunos puntos de análisis de un proyecto (microsonda, LA-ICP-MS, EDS…) tienen su
constituyente nombrado por el petrógrafo, un clasificador aprende el constituyente a partir de los valores medidos,
dice con qué frecuencia acierta en láminas que no vio, y propone un constituyente con su probabilidad para los puntos
aún sin nombre. Usted acepta, corrige o rechaza cada propuesta; el entrenamiento siguiente las usa.

## Antes de empezar

* SinGAN: RockFace IA con entrenamiento (extra `ai-train`); una tarjeta gráfica para entrenamientos 3D de tamaño útil.
* Ciclo de puntos: puntos de análisis con valores (Atlas → Puntos, o importados de CSV), al menos 6 puntos nombrados de
  al menos 2 constituyentes; los constituyentes son términos de la nomenclatura.

## Paso a paso

### Modelo generativo (MC → IA)

1. Abra el volumen de entrenamiento (segmentado o de grises).
2. En **Modelo generativo (SinGAN)**, ajuste las **Iteraciones** por escala y el tamaño **Volumen de entrenamiento
   hasta** (el volumen se lee en el nivel que cabe en él), y haga clic en **Entrenar con el volumen**. El resultado
   compara 4 volúmenes generados con ruido nuevo con el volumen de entrenamiento: porosidad, probabilidad de dos puntos
   (S2) y longitud de correlación. El modelo queda guardado en el proyecto con su ficha.
3. Seleccione el modelo en la tabla (tarea *Generación 3D*), ajuste **Volúmenes**, **Tamaño × entrenamiento** (1,5 hace
   cada lado 1,5 veces más largo) y **Semilla**, y haga clic en **Generar volúmenes**: se añaden a la muestra, como
   volúmenes de etiquetas con la leyenda del volumen de entrenamiento cuando era segmentado.
4. Para volúmenes grandes ejecute el entrenamiento como trabajo: **Multiescala → Trabajos**, cálculo *IA: entrenar un
   modelo generativo (SinGAN)*, aquí o en una computadora remota con tarjeta gráfica; **Traer los resultados** añade
   el modelo.

### Ciclo de puntos (Lab → IA)

1. Elija el tipo de **Puntos** y **De** *esta lámina* o *todo el proyecto*, y haga clic en **Aprender**. El resultado
   muestra la exactitud y las notas por clase en validación cruzada con partes por lámina (una lámina nunca está a la
   vez en el entrenamiento y en la validación).
2. Elija el **Clasificador** y **Proponer desde probabilidad** (p. ej. 0,6), y haga clic en **Proponer**: la tabla
   lista los puntos sin nombre con el constituyente propuesto y su probabilidad.
3. Desmarque lo que rechaza, escriba sobre un constituyente para corregirlo, y haga clic en **Aceptar marcados**: los
   constituyentes se escriben en los puntos, cada uno con el modelo y la probabilidad en su registro (así siempre se
   distingue un nombre dado a mano de una propuesta aceptada).
4. Aprenda de nuevo: el nuevo clasificador usa también los puntos aceptados.

## Opciones

| Campo | Qué cambia |
|---|---|
| Iteraciones | Pasos de entrenamiento por escala de la pirámide |
| Volumen de entrenamiento hasta | El mayor volumen de entrenamiento (vóxeles por lado); se usa el nivel del volumen que cabe |
| Volúmenes, Tamaño × entrenamiento, Semilla | Cuántos volúmenes, de qué tamaño y con qué ruido |
| Proponer desde probabilidad | Las propuestas por debajo no se listan |

## Cómo funciona

* **SinGAN** (Shaham, Dekel & Michaeli 2019), en 3D como en el módulo RockSinGAN de GeoSlicer: una pirámide de pequeños
  generadores convolucionales y discriminadores de parches, entrenados de lo grueso a lo fino con el único volumen de
  entrenamiento; cada escala se entrena con la pérdida de Wasserstein con penalización de gradiente (Gulrajani et al.
  2017) más la reconstrucción del volumen de entrenamiento a partir de un ruido fijo; el ruido de cada escala más fina
  se escala por el error de reconstrucción de la escala inferior. Toda la pirámide es un único grafo ONNX, así que la
  generación corre en cualquier dispositivo.
* **Comparación**: porosidad, la probabilidad de dos puntos S2(h) a lo largo de x y la longitud en que S2 recorrió 1/e
  del camino hasta φ² (Torquato 2002).
* **Clasificador de puntos**: el bosque aleatorio de 0.23 sobre los valores (bajo el límite de detección = 0; ausente
  = mediana de los puntos de entrenamiento), en validación cruzada con partes agrupadas por lámina.

## Desde un script

```python
vol = prj.volume("segmentación del tapón")
model, comparison = vol.ai_generator(iterations=300, max_voxels=32 ** 3)
new = vol.ai_generate(model, n=4, scale=1.5)
rid, metrics = prj.ai_spots_train(kind="geochemistry")
props = prj.ai_spots_propose(rid, kind="geochemistry", min_probability=0.6)
prj.ai_spots_accept(props, rid)
```

## Límites y problemas comunes

* Un generador 3D se entrena en minutos en una tarjeta gráfica y en horas en un procesador; empiece con un tamaño de
  entrenamiento pequeño y pocas iteraciones para verificar el resultado, luego ejecute el entrenamiento completo como
  trabajo.
* Un generador aprende una textura: un volumen de entrenamiento con una tendencia (una capa, una fractura) se reproduce
  como textura, no como tendencia; use MPS con datos duros cuando la disposición importa.
* Las propuestas de puntos sólo son tan buenas como los puntos nombrados: nombre ejemplos de todos los constituyentes
  esperados, de más de una lámina.

## Cobertura

GM5 (generación de imágenes: la red generativa RockSinGAN), L11 (anotación → ML → validación → extrapolación →
reentrenamiento, para geoquímica de puntos).
