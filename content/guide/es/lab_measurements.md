# RockFace Lab: medidas y distribuciones de tamaño

## Para qué sirve

La pestaña **Medidas** mide cada objeto de un mapa de objetos — cada grano o poro: área, perímetro, diámetros de
Feret, la elipse ajustada, factores de forma, orientación, brillo y color — y, para poros, las gargantas entre ellos y
el número de coordinación. Da las clases de tamaño (Udden–Wentworth para granos, Choquette y Pray para poros), las
estadísticas de Folk y Ward, tablas con columnas calculadas y filtros, gráficos y las exportaciones.

## Antes de empezar

Un mapa de objetos (página [RockFace Lab: edición de mapas y objetos](lab_editing_objects.md)), de preferencia con su escala.

## Paso a paso

### Medir

1. Abra **Medidas** y elija el **Mapa de objetos**.
2. **Medida del tamaño** (la columna usada para los tamaños: diámetro de Feret máximo, diámetro equivalente…) y
   **Distribución por**: **número de objetos** o **área (como un conteo de puntos)**.
3. **Excluir objetos cortados por el borde**; **Objetos de al menos** N píxeles.
4. **Medir**. "N objetos medidos: …".
5. El resumen: "Tamaño: media … µm (clase); D10, D50, D90", "Folk & Ward (φ): media, selección (clase), asimetría,
   curtosis", "Forma: relación de aspecto media, circularidad media" y, para poros, "Número de coordinación medio …
   (N gargantas)".

### La tabla

* Una fila por objeto con **Área**, **Perímetro**, **Perímetro / área**, **Diámetro equivalente**, **Diámetro de Feret
  máximo**, **mínimo** y **medio**, **Ángulo del Feret máximo**, **Relación de aspecto**, **Elongación**, **Eje
  mayor** y **menor de la elipse**, **Orientación (elipse)**, **Excentricidad**, **Factor de forma**,
  **Circularidad**, **Solidez**, **Convexidad**, **γ (perímetro / círculo)**, **Centro x, y** (px y mm), **En el
  borde**, el **Número de coordinación** de los poros, y el brillo y el color de la imagen bajo el objeto.
* **Filtrar**, por ejemplo `area_um2 > 500 & aspect_ratio < 0.6`, y luego **Aplicar el filtro** ("Objetos mostrados: n
  de N").
* **Nueva columna** con una **Fórmula**, por ejemplo `feret_max_um / feret_min_um`, y luego **Añadir la columna**.
* La tabla se puede ordenar, filtrar por columna, exportar a CSV o XLSX y mostrar como histograma.

### Clases y gráficos

1. **Clases**: **Tamaño de grano (Udden–Wentworth)** (14 clases, de arcilla a bloque), **Tamaño de poro (Choquette &
   Pray)** o **Grupos de área similar** — con el recuento, el % en número y el % en área de cada una.
2. Gráfico: **Histograma de tamaños (φ)** con su curva acumulada, **Gráfico cruzado con histogramas**, **Diagrama de
   rosa de orientaciones**, **Clases de tamaño**, o **Transiciones entre fases (barras apiladas)** (página
   [Transiciones entre fases](transitions.md)). **Dibujar el gráfico**; guárdelo en PNG.
3. Exporte las tablas (CSV, XLSX) y los objetos en color (PNG).

## Opciones

| Opción | Qué cambia |
|---|---|
| Medida del tamaño | El diámetro usado para las clases y estadísticas. |
| Distribución por área | Cada objeto pesa por su área, como en un conteo de puntos. |
| Excluir objetos cortados por el borde | Los objetos que tocan el borde de la imagen no se cuentan. |

## Cómo funciona

* Perímetro por la fórmula de Crofton; diámetros de Feret a partir de la envolvente convexa del contorno subpíxel; la
  elipse de los mismos momentos de segundo orden; factores de forma según la ISO 9276-6.
* Gargantas: la longitud de la frontera entre dos poros que se tocan; el número de coordinación es el número de poros
  que toca cada uno.
* Comprobado en formas de tamaño conocido en posiciones y ángulos aleatorios: desde 20 px, área, perímetro, diámetros
  de Feret y elipse dentro de un 2 %, orientación dentro de una fracción de grado; coordinación 4 y 6 en
  empaquetamientos cuadrado y hexagonal; las medidas de Folk y Ward de 517 discos de una ley log-normal conocida
  iguales a las de los diámetros sorteados.

## Desde un script

```python
grains = prj.image("ILLUSTRATIVE mosaic PP").segment("resin").objects(2, "watershed", min_px=40)
m = grains.measure()
print(m.summary(exclude_edge=True))                       # Folk y Ward, D10/D50/D90, forma, coordinación
t = m.table.filter("touches_edge == 0")
t.add_column("ratio", "feret_max_um / feret_min_um")
print(rf.measure.class_table(t, "feret_max_um", "wentworth"))
rf.measure.chart("rose", t, "orientaciones.png", x="ellipse_angle")
rf.measure.to_xlsx("granos.xlsx", {"granos": t})
```

## Límites y problemas comunes

* "El mapa no tiene escala: las longitudes están en píxeles." — dé la escala de la imagen en Atlas.
* Los objetos de uno o dos píxeles tienen formas sin sentido: aumente **Objetos de al menos**.
* El perímetro de Crofton queda un 5–7 % por debajo en lados rectos largos.

## Cobertura

GT11 (medidas por objeto), GT12 (gargantas 2D y coordinación), GT13 (clases de tamaño; grupos por área similar),
GT14 (salidas: tablas XLSX, objetos coloreados), GT19 (tablas, filtro, gráficos).
