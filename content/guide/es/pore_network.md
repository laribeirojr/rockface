# Red de poros: extracción, permeabilidad, intrusión de mercurio, permeabilidad relativa, producción

## Para qué sirve

El espacio poroso de un volumen de micro-CT convertido en una red de poros (los cuerpos) unidos por gargantas (las
constricciones), sobre la cual se calcula el flujo: la permeabilidad absoluta en x, y y z, la curva de intrusión de
mercurio (MICP) para comparar con el laboratorio, las curvas de permeabilidad relativa de petróleo y agua (drenaje y
luego imbibición), la recuperación de petróleo de una inyección de agua, y cómo todo esto cambia con la mojabilidad.

## Antes de empezar

* Un volumen segmentado de la muestra en RockFace MC (pestaña Segmentación), con los segmentos de poro marcados con el
  papel "poro" — o un volumen de objetos (pestaña Análisis → Objetos del espacio poroso), cuyos objetos pasan a ser los
  poros.
* O una red en el formato Statoil (los cuatro archivos `*_node1.dat`, `*_node2.dat`, `*_link1.dat`, `*_link2.dat` de
  pnextract y pnflow, como las redes del Imperial College).
* Un volumen grande se extrae en el nivel más fino de su pirámide por debajo de 64 millones de vóxeles; recórtelo antes
  (Volumen → Recortar) para trabajar en resolución completa.

## Paso a paso

### Extraer la red

1. Abra el volumen segmentado y vaya a la pestaña **Red de poros**.
2. En **Extracción (SNOW)**, mantenga **Suavizado del mapa de distancias** 0,40 y **Radio de la búsqueda de picos** 4
   vóxeles (los valores del algoritmo SNOW), dé un **Nombre** si lo desea y pulse **Extraer la red de este volumen**.
3. La red aparece en **Red** con sus números (poros, gargantas, número de coordinación medio, poros aislados, radios
   medios, porosidad de la red), dibujada en 3D: arrastre para girar, rueda para acercar; **Color de los poros** por
   radio o por número de coordinación. Las regiones de los poros quedan guardadas como un volumen de objetos.
4. **Importar Statoil…** lee una red hecha en otro programa; **Exportar Statoil…** escribe la actual (flujo según el
   eje elegido en **Flujo según**); **Borrar la red** la quita del proyecto.

### Ejecutar una simulación

Elija la **Simulación**, sus parámetros, y pulse **Ejecutar**. El gráfico y la tabla muestran el resultado; todo
resultado queda guardado con la red.

* **Permeabilidad absoluta (una fase)** — K en x, y, z (o en un eje) en mD y m².
* **Intrusión de mercurio (MICP)** — la saturación de mercurio contra la presión (log), con el radio de garganta de
  cada paso en la tabla.
* **Permeabilidad relativa (dos fases)** — drenaje (petróleo entrando en la roca llena de agua) y luego imbibición (el
  agua de vuelta): krw y kro contra Sw, Pc de cada paso; Swi, Sor y los puntos extremos en la barra de estado.
* **Prueba de sensibilidad** — la corrida de dos fases repetida para cada valor de un parámetro (**Variar**, valores
  separados por `;`): la nube de curvas y su media, la tabla de resultados de cada corrida y las correlaciones del
  parámetro con cada resultado.
* **Kabs VER** — el volumen cortado en cubos centrados de arista creciente, cada uno extraído de nuevo, y la
  permeabilidad de cada tamaño: donde deja de cambiar, el volumen es representativo.

### Después de una corrida de dos fases

* **Animar los ciclos** — los poros coloreados por su fluido en cada paso (petróleo rojo, agua azul); el deslizador
  elige el paso.
* **Predicción de producción** — la inyección de agua de la curva de imbibición (Buckley–Leverett): petróleo
  recuperado contra los volúmenes porosos de agua inyectados; después de una prueba de sensibilidad, todas las curvas
  y las predicciones pesimista, neutral y optimista (P10, P50, P90).
* **Curva de referencia (CSV)…** — una curva krel medida (columnas `Sw`, `krw`, `kro`) dibujada junto a la simulada.
* **Informe (HTML)…** — una página con la red, la permeabilidad, MICP, krel, producción y VER.

## Opciones

* **Mercurio**: tensión superficial 0,485 N/m y ángulo de contacto 140° por defecto.
* **Tensión interfacial petróleo–agua** (0,03 N/m), **viscosidades** del agua y del petróleo.
* **Ángulo de contacto de retroceso** (drenaje) — su centro y su **amplitud** (los ángulos de los elementos repartidos
  de modo uniforme en la amplitud); **Ángulo de avance − retroceso**: el ángulo de avance de la imbibición. Por debajo
  de 90° la roca es mojable al agua, por encima de 90° al petróleo.
* **Paso de Sw** — la saturación entre dos puntos calculados; **Swi mínima** — donde se detiene el drenaje.
* **Plano inferior / superior de la caja** — la saturación y el flujo se calculan entre estos planos (0,1 y 0,9 de la
  longitud por defecto, como la caja de cálculo de pnflow): los poros más allá fijan las presiones.

## Cómo funciona

* **Extracción**: el mapa de distancias del espacio poroso, suavizado, sus máximos como marcadores (un marcador más
  cerca de otro más alto que del sólido se descarta), el watershed: cada región un poro, cada contacto de dos regiones
  una garganta (Gostick 2017). Radio del poro: la mayor distancia en la región; radio de la garganta: la mayor en el
  contacto; factor de forma de la garganta G = r² / (4 A) por su área A.
* **Flujo**: cada conducto (medio poro, garganta, medio poro) tres ductos en serie, g = k G A² / μ (k = 3/5 triángulo,
  0,5623 cuadrado, 1/2 círculo; Patzek & Silin 2001); las presiones de los poros resueltas; K = Q μ L / (A ΔP).
* **MICP**: el mercurio entra por todas las caras, un elemento a P = −2 σ cos θ / r (Washburn 1921) si un vecino ya está
  lleno.
* **Dos fases**: drenaje por percolación invasiva desde la cara de entrada, agua retenida en las esquinas; imbibición
  por snap-off en las gargantas, σ (cos θ − sen θ tg β) / r, y llenado tipo pistón, 2 σ cos θ / r, el petróleo atrapado
  cuando pierde su camino hacia la salida; kr por las conductancias de cada fase (Valvatne & Blunt 2004, simplificado).
* **Producción**: el flujo fraccional, la tangente de Welge y la recuperación (Buckley & Leverett 1942; Welge 1952).

## Desde un script

```python
seg = prj.volume("ILLUSTRATIVE sphere pack")
net = seg.extract_network(name="ILLUSTRATIVE network")
print(net.stats()["coordination_mean"])
k = net.kabs()                         # {"x": {"K_mD": …}, …, "mean_mD"}
m = net.micp()
kr = net.two_phase(theta_r=30, separation=20, swi_min=0.2)
pr = net.production(kr, mu_w=1e-3, mu_o=5e-3)
runs = net.sensitivity({"theta_r": [20, 40, 60]})
net.export_statoil("pack")             # pack_node1.dat …
net.report("red.html")
berea = prj.import_statoil("Berea_node1.dat")
```

## Límites y problemas comunes

* **"Nada fluye de cara a cara"** — los poros no unen las dos caras en ese eje: pruebe otro eje, o la segmentación
  pierde los poros pequeños.
* El modelo de dos fases es simplificado: sin llenado cooperativo de los poros, sin capas de petróleo, sin hinchamiento
  de películas; en una roca muy mojable al agua domina el snap-off y kro cae pronto. Compare con curvas medidas (Curva
  de referencia) antes de usar los valores.
* Los radios extraídos vienen del mapa de distancias en los centros de los vóxeles: las gargantas de un vóxel de ancho
  no se resuelven.
* Extraer 64 millones de vóxeles (400³) toma cerca de 1,5 minutos y 3,5 GB de memoria.
* La microporosidad (poros no resueltos) y las redes multiescala llegan en la etapa 0.25.

## Cobertura

GV12 (Pore Network: Extraction, Simulation — una fase, dos fases, inyección de mercurio —, Kabs REV, Krel EDA,
Production Prediction, Cycles Visualization, informe PNM).
