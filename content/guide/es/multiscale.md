# Multiescala: generación de imágenes (MPS), comparación de las realizaciones y la red de poros de dos escalas

## Para qué sirve

Un plug escaneado en alta resolución cubre unos milímetros; un perfil de imagen o un escaneo de testigo cubre metros
con una resolución más gruesa. La pestaña **Multiescala** de RockFace MC une las escalas: **genera imágenes 3D** de la
escala fina con las estadísticas de un volumen de entrenamiento, condicionadas por lo que se conoce en la escala
gruesa (datos duros, o un perfil de imagen envuelto en la pared del pozo), **compara** las realizaciones con la imagen
de entrenamiento y extrae una **red de poros de dos escalas** de un mapa de porosidad, en la que los vóxeles
microporosos pasan a ser poros no resueltos.

## Antes de empezar

* Para la MPS: un volumen de entrenamiento (una segmentación, para una simulación categórica, o un volumen de grises o
  de porosidad, para una continua). Opcionalmente un volumen de datos duros en la malla de la simulación (0 o vacío =
  sin dato) o un perfil de imagen del pozo.
* Para la red de dos escalas: un mapa de porosidad (pestaña Microporosidad).

## Paso a paso

### Generar imágenes (MPS)

1. Vaya a la pestaña **Multiescala**; en **Generación de imágenes (MPS)** elija el **Volumen de entrenamiento**.
2. Opcionalmente elija **Datos duros (volumen)** o **Datos duros (perfil de imagen en un cilindro)**: las columnas del
   perfil se colocan en la pared de un cilindro vertical de la malla, una fila por corte.
3. Escriba la **Malla (z y x)** de la simulación (vacío: la malla del volumen de entrenamiento), el número de
   **Realizaciones** y la **semilla**.
4. Ajuste los **Vecinos / radio de búsqueda / umbral de distancia** del muestreo directo y pulse **Simular**. Cada
   realización es un nuevo volumen de la muestra (categoría *simulation*).

### Comparar las realizaciones

Pulse **Comparar las realizaciones**: el gráfico muestra la porosidad de cada corte de cada realización frente a la
imagen de entrenamiento, y la tabla el radio medio de poro de cada una (distribución de tamaños de poro por espesor
local).

### Red de poros de dos escalas

1. En **Red de poros de dos escalas** elija el **Mapa de porosidad**.
2. Elija el **Radio de los poros no resueltos**: *fijo* (escríbalo), *J de Leverett (a partir de k)* o *a partir de una
   curva MICP*, y la **tortuosidad** y el tamaño del **bloque** (vóxeles de microporosidad reunidos en un poro no
   resuelto).
3. Pulse **Extraer y calcular la permeabilidad**. La red queda guardada en el proyecto (pestaña Red de poros, donde
   todas las simulaciones de la 0.24 corren sobre ella) con su permeabilidad según x, y y z.

## Opciones

| Campo | Qué cambia |
|---|---|
| Vecinos | Número de nodos informados más cercanos al nodo simulado que forman su patrón (24 por defecto) |
| Radio de búsqueda | Hasta dónde se buscan los vecinos (vóxeles) |
| Umbral de distancia | La imagen de entrenamiento se recorre hasta que un patrón difiera menos que esta fracción (0,05: como máximo un vecino de cada veinte de otra clase) |
| Radio de los poros no resueltos | *fijo*: un radio; *Leverett*: r = √(8k/φ) a partir de una permeabilidad k de la fase microporosa; *MICP*: radios sorteados de una curva de mercurio, los mayores para los bloques más porosos |
| Tortuosidad / bloque | τ del modelo de haz de capilares de los tapones microporosos; la arista de los cubos de vóxeles microporosos que forman un poro no resuelto |

## Cómo funciona

* **Muestreo directo** (Mariethoz, Renard & Straubhaar 2010): los nodos se visitan en un orden aleatorio; para cada
  uno, el patrón de sus vecinos informados se compara con patrones en lugares aleatorios de la imagen de entrenamiento,
  y se pega el valor del primer lugar suficientemente cercano (o del más cercano recorrido). Los datos duros están
  informados desde el inicio y se mantienen.
* **La red de dos escalas** (según Bultreys et al. 2015): los poros resueltos (φ = 1) se extraen por SNOW como en la
  0.24; los vóxeles microporosos se reúnen en cubos que pasan a ser poros no resueltos, de volumen Σφ y radio dado por
  el modelo de subescala. Un conducto que toca un poro no resuelto es un tapón poroso de permeabilidad k = φ r² / (8 τ)
  (un haz de capilares de radio r y tortuosidad τ), conductancia k A / L. Un mapa binario da exactamente la red de la
  0.24; un bloque microporoso uniforme da exactamente el k del tapón.

## Desde un script

```python
seg = prj.volume("plug segmentation")
reals = seg.mps(realizations=5, shape=(64, 128, 128), log=prj.log("AMP image log"), seed=3)
net = prj.volume("plug porosity map").multiscale_network({"kind": "fixed", "radius_um": 0.5}, tortuosity=2.0)
print(net.kabs())
```

## Límites y problemas comunes

* El muestreo directo se vuelve lento con imágenes de entrenamiento grandes y umbrales estrictos: empiece con una malla
  pequeña, umbral 0,1 y fracción recorrida 0,05 (``fraction`` en un script), y luego refine. Las ejecuciones largas
  pueden ir como trabajos.
* La red generativa (RockSinGAN) del programa de referencia es un modelo de IA; llega con la etapa de IA (0.26).
* Los modelos de subescala son simples: los tapones microporosos son haces de capilares; use una curva MICP de la fase
  microporosa cuando el laboratorio la tenga.

## Cobertura

GV13 (multiescala), GM5 (generación de imágenes — MPS; la red generativa en la 0.26), GM6 (posprocesamiento), GM7 (red
de poros entre escalas), GM3 (preprocesamiento de perfiles de imagen: el perfil en un cilindro), GM4 y GM8
(preprocesamiento y segmentación de las escalas, con las herramientas de la 0.20–0.23).
