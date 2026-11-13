# RockFace IA: segmentar con modelos, entrenar, ajustar y validar

## Para qué sirve

Una red neuronal entrenada con muchos ejemplos segmenta una imagen, una lámina entera, un volumen de micro-CT o un
perfil de imagen con un clic, y da el área de cada clase con la confianza del resultado. Cuando un modelo no se ajusta
a su material — otra resina, otra tinción, otro tomógrafo — usted **pinta algunos ejemplos** y **ajusta** el modelo:
la nueva versión aprende su material, y su exactitud se mide en una parte de su anotación que nunca vio. Es el ciclo
anotación → entrenamiento → validación → aplicación → reentrenamiento. La segmentación **sin anotación** divide una
imagen en sus texturas sin ninguna anotación, y el **segmentador de instancias** de perfiles de imagen encuentra los
orificios de muestreo lateral y los vugs como objetos separados.

## Antes de empezar

* RockFace IA instalado (vea *RockFace IA: instalación, dispositivo y el hub de modelos*). El entrenamiento necesita
  también el extra `ai-train`.
* Una lámina con una imagen (Lab), o un volumen de grises o un perfil de imagen (MC).

## Paso a paso

### Lab — una imagen o una lámina entera

1. Abra la lámina en **Lab**, abra la imagen y vaya a la pestaña **IA**.
2. **Aplicar**: seleccione un modelo de la tarea *Segmentación 2D* (p. ej. `rockface-thinsection-pores`) y haga clic
   en **Segmentar la imagen (lámina entera, bloque a bloque)**. La imagen se clasifica a resolución completa, bloque a
   bloque, y se guarda como mapa de segmentación; el resultado muestra el área de cada clase, la porosidad y la
   confianza media. Un modelo de la tarea *Objetos (instancias) 2D* entrenado en imágenes da un mapa de objetos, con
   un número por grano, medido en la pestaña **Medidas**.
3. **Entrenar o ajustar**:
   * **Anotación**: *Trazos de la pestaña Segmentación* (pinte allí ejemplos de cada segmento, como para el bosque
     aleatorio) o un mapa de segmentación de la imagen (hecho por cualquier método, corregido a mano), u *Objetos: …*
     — un mapa de objetos de la imagen (granos o poros separados en la pestaña **Edición y objetos** y corregidos a
     mano) para entrenar un **modelo de instancias** que separa granos que se tocan (el modelo textural de
     instancias);
   * marque **Ajustar el modelo seleccionado** para partir del modelo seleccionado en la tabla (las clases deben
     coincidir);
   * elija el **Tamaño de la red** (small, standard, large), las **Épocas**, los **Pasos por época**, la parte
     **Reservado para validación** y un **Nombre del modelo**, y haga clic en **Entrenar**. El resultado muestra la
     exactitud, la IoU media y el Dice de cada clase en la parte reservada; el modelo queda guardado en el proyecto.
4. **Validar**: elija un **Mapa de referencia** que no se usó en el entrenamiento (de esta u otra imagen) y haga clic
   en **Validar**: las métricas del modelo seleccionado frente a él. Las clases se emparejan por nombre.
5. **Sin anotación**: ajuste **Segmentos como máximo / como mínimo**, **Iteraciones** y el **Tamaño de trabajo**, y
   haga clic en **Segmentar sin anotación**. Los segmentos del mapa se llaman *Segment 1…k* por área decreciente;
   renómbrelos y únalos en la pestaña **Edición y objetos**.

### MC — un volumen o un perfil de imagen

1. Abra un volumen de grises y vaya a la pestaña **IA**.
2. **Aplicar**: seleccione un modelo (p. ej. `rockface-microct-pores`; un modelo 2D corre corte a corte) y haga clic
   en **Segmentar el volumen**: un volumen de etiquetas con las fracciones, la porosidad y la confianza media.
3. **Entrenar, ajustar y validar**: elija el **Volumen de grises** y la **Anotación (volumen de etiquetas)** — pintada
   en la pestaña **Bosque aleatorio** o una segmentación corregida a mano —, la **Red** (2D corte a corte, o 3D) y
   haga clic en **Entrenar**. En 2D se reserva una parte de los cortes anotados; en 3D, bloques del volumen.
   **Validar** mide el modelo seleccionado frente a un volumen segmentado de la misma malla.
4. **Perfiles de imagen**: abra un perfil de amplitud; seleccione un modelo de la tarea *Objetos (instancias) 2D*
   (p. ej. `rockface-imagelog-instances`), elija el perfil de **Tiempo de tránsito** del mismo pozo cuando el modelo
   lo toma, y haga clic en **Aplicar al perfil de imagen**: un perfil de objetos con la tabla de los objetos (tamaños,
   profundidades, azimuts), editable con el editor de perfiles de 0.23. Un modelo de *Segmentación 2D* da un perfil de
   etiquetas.

## Opciones

| Campo | Qué cambia |
|---|---|
| Tamaño de la red | small (8 filtros en la primera capa), standard (16), large (32): mayor aprende más, necesita más memoria y tiempo |
| Épocas, Pasos por época | Cuánto dura el entrenamiento; se guarda la red con la mejor exactitud en los datos reservados |
| Reservado para validación | La parte de la anotación dejada fuera del entrenamiento para medir el modelo (bloques de 64 px en 2D, cortes o bloques de 32 vóxeles en MC) |
| Ajustar el modelo seleccionado | Parte de ese modelo (tasa de aprendizaje ×0,3); la nueva versión lo tiene como padre |
| Segmentos como máximo / como mínimo | Los límites de la segmentación sin anotación |
| Objeto más pequeño | Los objetos del segmentador de instancias por debajo de esta área se descartan |

## Cómo funciona

* **Red**: una U-Net (Ronneberger, Fischer & Brox 2015) de cuatro niveles con normalización por lotes, en 2D o 3D;
  pérdida = entropía cruzada ponderada por clases más Dice, sólo en los píxeles anotados (Milletari, Navab & Ahmadi
  2016); AdamW (Loshchilov & Hutter 2019) con programa coseno; reflejos y rotaciones de 90° aleatorios.
* **Métricas** (en datos reservados): exactitud, intersección sobre unión y Dice por clase, la matriz de confusión.
* **Imágenes y volúmenes grandes**: bloques con margen, reflejados en los bordes, clasificados por lotes; el margen
  limita las costuras entre bloques.
* **Sin anotación**: una red pequeña entrenada en la propia imagen, con las clases hechas constantes en los
  superpíxeles SLIC y continuas en el espacio (Kanezaki 2018; Kim, Kanezaki & Tanaka 2020; Achanta et al. 2012); el
  número de clases baja a medida que la red las une.
* **Instancias**: la red clasifica fondo, interior y borde de los objetos; los interiores son las semillas de un
  watershed sobre los objetos, a través de la costura 0°/360° del perfil.

## Desde un script

```python
pic = prj.image("ILLUSTRATIVE mosaic PP")
seg, fr, por, conf = pic.ai_segment("rockface-thinsection-pores")          # lámina entera, bloque a bloque
model, met = pic.ai_train(map=seg, base="rockface-thinsection-pores", epochs=10)   # ajuste, métricas reservadas
print(pic.ai_validate(model, "mapa de referencia"))
seg2, fr2 = pic.ai_unsupervised(max_segments=8)
grains, n = pic.ai_objects(pic.ai_train_objects("objetos de los granos")[0])  # el modelo textural de instancias
vol = prj.volume("tomografía del tapón")
labels, fr, por, conf = vol.ai_segment("rockface-microct-pores")
model, met = vol.ai_train("cortes pintados", base="rockface-microct-pores")
objects, table, n = prj.log("AMP").ai_instances("rockface-imagelog-instances", transit_time="TT")
```

## Límites y problemas comunes

* "La anotación tiene k clases y el modelo m": el ajuste mantiene las clases del modelo; pinte los mismos segmentos.
* "Ninguna clase de la referencia coincide por nombre con una clase del modelo": renombre los segmentos del mapa de
  referencia.
* Un modelo aplicado a imágenes de otro aumento: el modelo de láminas que viene con el programa se entrenó más o menos
  a la resolución de las imágenes GO-Forward; ajústelo con algunos trazos de sus imágenes.
* Entrenar en el procesador lleva minutos para una imagen y puede llevar horas para una red 3D; ejecute los
  entrenamientos largos en una tarjeta gráfica o como trabajo (MC → Multiescala → Trabajos: *IA: entrenar un
  segmentador de volúmenes*).

## Cobertura

GT18 (segmentadores preentrenados, lámina), GV19 (segmentadores preentrenados de volúmenes), GI11 (segmentador de
instancias de perfiles de imagen), GT20 (segmentación sin anotación), L7 (cuantificación de la lámina entera por ML),
L11 (anotación → ML → validación → extrapolación → reentrenamiento, para mineralogía y textura).
