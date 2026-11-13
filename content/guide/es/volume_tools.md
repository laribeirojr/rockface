# Herramientas de volumen: filtros, sombreado, efectos del editor de segmentos, objetos, registro, análisis

## Para qué sirve

Las herramientas de RockFace MC que preparan un volumen de micro-CT, corrigen su segmentación y lo miden: un filtro
que preserva los bordes, la corrección del sombreado (endurecimiento del haz), los efectos de un editor de segmentos,
la separación del espacio poroso en objetos, el registro de dos adquisiciones giradas una respecto de la otra, y el
variograma, el volumen elemental representativo y los atributos de un volumen.

## Antes de empezar

Un volumen abierto en RockFace MC. Cada herramienta escribe un volumen **nuevo**; el original nunca se modifica.

## Paso a paso

### Difusión anisotrópica (pestaña Volumen)

1. En **Volumen → Filtros**, elija **Difusión anisotrópica (preserva bordes)**.
2. Ajuste **Conductancia** (menor preserva más bordes) e **Iteraciones** (más suaviza más), pulse **Añadir** y luego
   **Aplicar**.

### Corrección de sombreado (pestaña Volumen)

1. **Corrección de sombreado (corte a corte)**: elija dónde se ajusta el fondo — **Todo el corte**, el cilindro del
   plug o el interior de un volumen segmentado.
2. Opcional: **Suavizado entre cortes** (en cortes).
3. Pulse **Corregir el sombreado**.

### Efectos sobre el volumen segmentado (pestaña Segmentación)

Abra un volumen segmentado. En **Efectos sobre el volumen segmentado**, elija el **Efecto**, el **Segmento** y, cuando
se pida, el **Otro segmento**, **Vóxeles / tamaño / tolerancia** o **Región o volumen gris**, y pulse **Aplicar el
efecto (volumen nuevo)**:

* **Margen** hace crecer (vóxeles positivos) o encoge (negativos) un segmento;
* **Suavizado** quita la aspereza de un segmento;
* **Islas** quita las piezas menores que el tamaño dado;
* **Operadores lógicos** suman, restan, intersecan, copian, invierten o vacían segmentos;
* **Máscara** conserva solo lo que está dentro de otro volumen segmentado;
* **Expandir segmentos** llena los vóxeles en 0 con el segmento más cercano;
* **Quitar bordes** vacía los vóxeles donde se tocan dos segmentos;
* **Crecer desde semillas** hace crecer los vóxeles pintados de una anotación sobre un volumen gris;
* **Trazado de nivel desde la cruz** toma los vóxeles conectados de un volumen gris cercanos al valor bajo la cruz.

### Objetos del espacio poroso (pestaña Análisis)

1. Abra un volumen segmentado. En **Objetos del espacio poroso**, elija **Separados por**: *Watershed del mapa de
   distancias* (los poros que se tocan se separan) o *Piezas conectadas*.
2. Ajuste **Distancia mínima entre centros** y **Objeto más pequeño**, y pulse **Separar en objetos**.
3. La tabla lista cada objeto: vóxeles, volumen, diámetro equivalente, ejes, centroide, el radio de la mayor esfera
   inscrita y si toca el borde.

### Registro con rotación (pestaña Registro)

Elija los volúmenes **Fijo** y **Móvil**, marque **Buscar también la rotación (sin puntos de control)** y pulse
**Buscar el desplazamiento (correlación de fase 3D)**. La rotación (en torno a x, y, z) y el desplazamiento quedan
guardados en el volumen móvil; **Remuestrear el volumen móvil sobre el fijo** lo escribe en la malla del fijo.

### Variograma, VER y atributos (pestaña Análisis)

* **Variograma (x, y, z, todas las direcciones)**: el semivariograma de un volumen gris, o de los poros de uno
  segmentado, con el modelo ajustado (alcance, meseta, efecto pepita) en la tabla.
* **Volumen elemental representativo**: la desviación estándar de la media de cubos aleatorios de arista creciente;
  el VER es donde la curva se estabiliza.
* **Informe (HTML)…** escribe los gráficos y las tablas en una página.
* **Mostrar los atributos** lista tamaño, vóxel, valores, historial; **Importar un archivo PCR…** añade los
  parámetros de reconstrucción del tomógrafo (el mínimo y el máximo de la escala de gris).

La **Tabla** de la pestaña se filtra por una expresión (`voxels > 100 and not border`), se exporta a CSV o Excel y
muestra el histograma de la columna elegida.

## Cómo funciona

* Difusión anisotrópica: Perona & Malik (1990); la conductancia se escala por la raíz de la media cuadrática del
  gradiente, como en la difusión anisotrópica de ITK. Calculada bloque a bloque, igual que todo el volumen.
* Sombreado: en cada corte se ajusta un polinomio de segundo grado f(x, y) a puntos aleatorios de la máscara y el corte
  pasa a s / f · M (M la media de la máscara).
* Objetos: el watershed (Vincent & Soille 1991) del mapa de distancias suavizado, un marcador por máximo local.
* Rotación: una búsqueda del ángulo en torno a z con la correlación de fase 3D del desplazamiento, y luego los seis
  parámetros refinados por la correlación cruzada normalizada.
* Variograma: Matheron (1963); modelo esférico; con una región, solo cuentan los pares con ambos extremos dentro.

## Desde un script

```python
vol = prj.volume("Plug A")
suave = vol.filter(("anisotropic", {"conductance": 1.0, "iterations": 5}))
plano = vol.shading_correction("cylinder")
seg = plano.segment()
objetos = seg.partition(min_distance=4)
filas = objetos.objects()
t = prj.volume("Plug A, segunda adquisición").register_rigid(vol)
v = seg.variogram()
seg.variogram_report("variograma.html")
mayor = seg.edit("margin", segment=1, voxels=2)
```

## Límites y problemas comunes

* Los efectos y los objetos trabajan con todo el volumen en memoria: por encima de 64 millones de vóxeles trabajan en
  un nivel reducido del volumen.
* La búsqueda de la rotación supone el mismo tamaño de vóxel en ambos volúmenes.
* Los atributos de Gabor, de Minkowski y del alcance del variograma del segmentador de GeoSlicer no se ofrecen.

## Cobertura

GV4, GV6, GV7, GV14 (Filters, Polynomial Shading Correction, Segment Editor, Segment Inspector, Register, Variogram
Analysis, Attribute Tools, Tables).
