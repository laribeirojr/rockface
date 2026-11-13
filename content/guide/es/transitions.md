# Transiciones entre fases

## Para qué sirve

Qué minerales tocan a cuáles: ¿la dolomita bordea los poros? ¿El cuarzo está rodeado de cemento de calcita? La tabla
de transiciones de un mapa mineral o de una segmentación dice, para cada fase, cómo se reparten sus píxeles vecinos
entre las demás fases. El gráfico de barras apiladas lo muestra de un vistazo.

## Antes de empezar

Un mapa mineral o una segmentación de una lámina en RockFace Lab.

## Paso a paso

1. Abra la lámina en RockFace Lab y vaya a la pestaña **Medidas**.
2. En **Transiciones entre las fases de**, elija el mapa y pulse **Calcular**.
3. La tabla (en lugar de las clases de tamaño) tiene una columna por fase: el % de sus píxeles vecinos que pertenecen a
   cada fase (las filas). El gráfico muestra una barra por fase, apilada por las fases que toca.
4. **Gráfico (PNG)** guarda el gráfico en un archivo PNG.

## Cómo funciona

Cada píxel se compara con sus 8 vecinos sobre todo el mapa en resolución completa; los contactos de una fase consigo
misma quedan fuera; cada columna se divide por su total (la "transition analysis" del Segment Inspector de GeoSlicer).

## Desde un script

```python
seg = prj.image("ILLUSTRATIVE mosaic PP (segmentation)")
tabla = seg.transitions()                 # rf.Table: "phase" y una columna por fase, en %
print(tabla.rows())
```

## Límites y problemas comunes

* "Se necesita una segmentación o un mapa mineral": las transiciones se calculan sobre mapas, no sobre imágenes.
* Las fases que no aparecen en el mapa quedan fuera.

## Cobertura

GT19 (Segment Inspector: transition analysis; Charts: transition).
