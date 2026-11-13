# Microporosidad: mapas de porosidad, permeabilidad de Darcy y las simulaciones Microtom

## Para qué sirve

Un volumen de micro-CT resuelve los poros grandes, pero no los poros más pequeños que su vóxel: un vóxel de cemento o
de arcilla microporosa es gris, entre el poro y el grano. La pestaña **Microporosidad** de RockFace MC convierte el
volumen en un **mapa de porosidad** (cada vóxel 0 = sólido … 1 = poro resuelto, la microporosidad entre ambos),
calcula la **permeabilidad de Darcy** de ese mapa y ejecuta las simulaciones **Microtom** sobre una segmentación:
distribuciones de tamaño de poro, intrusión de mercurio y drenaje capilar, imbibición y la permeabilidad absoluta por
lattice Boltzmann.

## Antes de empezar

* Un volumen de micro-CT en grises y su segmentación en la misma malla (pestaña Segmentación), con un segmento para los
  poros resueltos, uno para la fase microporosa y uno para los granos.
* Para el método por saturación: un escaneo seco y uno del mismo plug saturado con un fluido de contraste, registrados
  en la misma malla (pestaña Registro), y la segmentación.
* Las simulaciones Microtom trabajan sobre una segmentación con el papel "pore" en sus segmentos de poro.

## Paso a paso

### Crear un mapa de porosidad

1. Abra el volumen en grises y vaya a la pestaña **Microporosidad**.
2. En **Mapa de porosidad**, elija **A partir de**: *una segmentación* o *un escaneo seco y uno saturado*.
3. Elija el **Volumen de grises** (o el **Escaneo seco** y el **Escaneo saturado**) y la **Segmentación**.
4. Revise el **Papel de cada segmento**, escrito como `Segmento=papel; …`: `macro` (poro resuelto, porosidad 1),
   `micro` (microporoso: porosidad a partir de la atenuación), `solid` (porosidad 0) y `high` (minerales densos,
   porosidad 0). La propuesta viene de los nombres y papeles de los segmentos; escriba encima para cambiarla.
5. Mantenga **Atenuaciones de poro y sólido a partir de las medianas de sus segmentos**, o desmárquelo y escriba la
   **Atenuación de poro / sólido**.
6. Pulse **Crear el mapa de porosidad**. El mapa es un nuevo volumen (categoría *porosity*); la tabla da la porosidad
   total, la parte resuelta y la microporosidad.

### Permeabilidad de Darcy del mapa

1. Abra el mapa de porosidad.
2. En **Permeabilidad de Darcy del mapa**, elija la **Permeabilidad de un vóxel**: *ley de potencia k = a·φ^b*
   (escriba a en mD y b) o *Kozeny–Carman* (escriba el **Diámetro de grano**). Los poros resueltos reciben la
   permeabilidad de un tubo del ancho del vóxel.
3. Pulse **Calcular la permeabilidad del mapa actual**: K según x, y y z.

### Simulaciones Microtom

1. Abra la segmentación.
2. Elija la **Simulación** y sus opciones, y pulse **Simular sobre la segmentación actual**. Un mapa hecho por la
   simulación (radio de poro, radio de entrada) se guarda como nuevo volumen; el gráfico y la tabla muestran la curva.

## Opciones

| Campo | Qué cambia |
|---|---|
| Simulación | *Distribución de tamaños de poro (espesor local)*: el radio de la mayor esfera que contiene cada vóxel de poro, como curva acumulada. *Distribución de tamaños de poro (esferas sin solape)*: esferas colocadas de la mayor a la menor sin solaparse (conteo jerárquico). *Intrusión de mercurio (MICP)*: σ 0,485 N/m, θ 140°, desde una cara. *Drenaje capilar*: lo mismo con su σ y θ. *Imbibición* e *Imbibición con atrapamiento (Sor)*: el fluido mojante vuelve por los poros pequeños; con atrapamiento, el petróleo aislado de la salida queda (Sor). *Permeabilidad absoluta (lattice Boltzmann)* y su *REV* en cubos de arista creciente |
| Dirección de invasión | La cara por donde entra el fluido (x, y o z) |
| Pasos de radio | Número de radios de las curvas |
| Tensión interfacial / ángulo de contacto | σ y θ del drenaje y de la imbibición |
| Tiempo de relajación / tolerancia | τ del modelo de lattice Boltzmann (1,5 por defecto) y la variación relativa de la velocidad media a la que el flujo es estacionario |
| Como máximo (vóxeles) | La simulación usa el nivel más fino de la pirámide con como máximo este número de vóxeles |

## Cómo funciona

* **Porosidad por la atenuación**: en la fase microporosa φ = (I_sólido − I) / (I_sólido − I_poro), limitada a 0…1;
  los poros resueltos valen 1, el sólido 0. Con un escaneo seco y uno saturado, φ = (Δ − Δ_sólido) / (Δ_poro −
  Δ_sólido) con Δ = I_saturado − I_seco, la diferencia de los dos escaneos respecto a las de un poro resuelto y del
  sólido. Ambos son modelos lineales de mezcla de la atenuación.
* **Permeabilidad de Darcy del mapa**: cada vóxel recibe k(φ) y la ecuación de la presión ∇·(k ∇p) = 0 se resuelve por
  volúmenes finitos (medias armónicas entre vóxeles), presión fija en dos caras opuestas; K = Q L / (A Δp). Exacta en
  mapas en capas (medias aritmética y armónica).
* **Tamaños de poro**: espesor local (Hildebrand & Rüegsegger 1997) a partir del mapa de distancias euclídeas.
* **Drenaje y MICP**: invasión morfológica (Hilpert & Miller 2001): en el radio r el fluido no mojante llena las esferas
  de radio r cuyos centros se conectan con la cara de entrada; P = 2σ|cos θ| / r (Washburn 1921).
* **Lattice Boltzmann**: D3Q19, colisión de dos tiempos de relajación (Ginzburg, Verhaeghe & d'Humières 2008) con el parámetro mágico 1/8, que
  pone la pared de bounce-back a medio camino entre los nodos; una fuerza de cuerpo mueve el flujo y K = ν ⟨u⟩ / g. La
  muestra se une a su imagen especular a lo largo del flujo, de modo que las fronteras son periódicas. Comprobado en el
  flujo de Poiseuille plano (exacto) y en arreglos de esferas frente a Sangani & Acrivos (1982).

## Desde un script

```python
grey, seg = prj.volume("plug grey"), prj.volume("plug segmentation")
phi, info = grey.porosity_map(seg, {1: "macro", 2: "micro", 3: "solid"})
k = phi.darcy(model="power", a_md=50, b=3)
psd = seg.microtom("psd")
lbm = seg.lbm_permeability(axes=("x", "y", "z"))
```

## Límites y problemas comunes

* La atenuación de la fase microporosa debe estar entre las del poro y del sólido; un mineral denso en el segmento
  microporoso se lee como sólido. Dé a esos minerales un segmento propio con el papel `high`.
* El lattice Boltzmann crece con el número de vóxeles de poro: un cubo de 128³ de una arenisca tarda cerca de una hora
  en dos núcleos de procesador. Envíelo como trabajo (pestaña Multiescala → Trabajos) o reduzca **Como máximo
  (vóxeles)**.
* Por debajo de unos 4 vóxeles de ancho, una garganta no la resuelve el lattice Boltzmann; el tamaño del vóxel define el
  menor poro que fluye.

## Cobertura

GV9 (microporosidad), GV10 (Microtom), GV11 (modelado de flujo y permeabilidad).
