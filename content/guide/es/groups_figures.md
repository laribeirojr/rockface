# Grupos, figuras y presentaciones

## Para qué sirve

RockFace Explorer dibuja varios **grupos** de muestras juntos en una clasificación ternaria — las muestras de cada pozo
en el QFR de Folk, cada facies en el QtFL de Dickinson — con sus símbolos y colores. Su **generador de figuras** hace
figuras de publicación a partir de cualquier atributo de la colección (gráficos cruzados, histogramas, barras,
diagramas de caja, curvas contra la profundidad por pozo, diagramas ternarios), con el tamaño de una revista, y las
exporta también como proyecto de SciVelyx Graphs. Una **presentación** reúne figuras, tablas y galerías de imágenes en
un archivo de PowerPoint.

## Antes de empezar

Un proyecto con descripciones; las consultas guardadas ayudan (página [RockFace Explorer: consultas, tablas de resultados y exportaciones](explorer_queries.md)).

## Paso a paso

### Grupos en una clasificación ternaria

1. Abra la pestaña **Grupos** de Explorer.
2. **Método de clasificación**: la **Clasificación ternaria** (Folk 1980, McBride 1963, Dickinson QtFL y QmFLt, o una
   del proyecto) y, si quiere, **Composición original (restaurada)**.
3. **Añadir grupo** (hasta diez). Para cada grupo, en **Grupos de descripciones**:
   * las descripciones: **Consulta de la pestaña Consulta**, **Criterios del grupo** o una consulta guardada;
     **Elegidas a mano** añade otras ("Las encontradas por la consulta son fijas; marque otras para añadirlas a
     mano");
   * **Símbolo del punto**, **Color de relleno**, **Color del borde**; **Mostrar el grupo**; **Quitar el grupo**.
4. **Clasificar** dibuja todos los grupos, con la leyenda. "N puntos en G grupos; M descripciones sin punto en esta
   clasificación."
5. En el diagrama: **Tamaño de los puntos**, **Sin colores**, **Nombres de todos los puntos (o clic en un punto)**,
   **Acercar**, **Alejar**; el cuadro bajo el ratón da el nombre y los valores de los vértices; "Campo bajo el
   puntero: …".
6. **Exportar imagen…**; **Guardar grupos…** y **Abrir grupos…** guardan los conjuntos en el proyecto.

### Una figura

1. Abra la pestaña **Figuras**.
2. **Tipo**: **Gráfico cruzado**, **Histograma**, **Barras (número de muestras)**, **Diagrama de caja por categoría**,
   **Contra la profundidad, por pozo** o **Ternario con grupos**.
3. **Atributo (X)** y **Atributo (Y)** — cualquier atributo de cualquier concepto (por ejemplo Petrofísica ›
   Porosidad, Totales › Qt); **Color por** un atributo o **Grupos (pestaña Grupos)**; **Clases** para histogramas;
   **Profundidad** (medida, corregida, ajustada) para curvas contra la profundidad.
4. **X logarítmico**, **Y logarítmico**, **Nombres de las muestras**, **Leyenda**, **Solo las descripciones de la
   consulta**.
5. **Título**; **Tamaño de revista** (Nature, Elsevier, AAPG, ACS a una o dos columnas, una diapositiva 16:9) o
   **Tamaño libre** con **Ancho (mm)**, **Alto (mm)** y **Tamaño de letra (pt)**.
6. **Exportar…** escribe PNG, TIFF, JPEG, SVG, PDF, los datos graficados en CSV, o un proyecto de SciVelyx Graphs
   (`.scivelyx.json`) para terminar la figura allí.
7. **Guardar figura…** la guarda en el proyecto; **Abrir figura…** vuelve a dibujar una figura guardada con los
   registros más recientes.

### Una presentación

1. En **Presentación**, añada diapositivas: **+ Figura** (la figura mostrada), **+ Tabla** (la tabla de resultados de
   un concepto), **+ Imágenes** (una galería de las láminas).
2. **Escribir presentación (.pptx)…**. La presentación es 16:9 y se abre con una diapositiva de título y los criterios
   de la consulta.
3. O, en la pestaña Consulta, **Exportar → Presentación de la consulta (.pptx)…** escribe una de una vez.

## Opciones

| Opción | Qué cambia |
|---|---|
| Composición original (restaurada) | Los grupos se ubican con la composición antes de la diagénesis. |
| Tamaño de revista | Ancho, alto y letras de la columna de la revista (o de una diapositiva). |
| Cuando una descripción tiene varias filas | Se usa la media, salvo cuando X e Y son del mismo concepto (un punto por fila). |

## Cómo funciona

Los grupos y las figuras se recalculan a partir de las descripciones guardadas cada vez que se dibujan; así, una figura
guardada muestra siempre los datos más recientes. Las figuras se dibujan con Matplotlib a 600 dpi por defecto; el
proyecto de SciVelyx Graphs lleva los mismos datos y estilos, y la figura puede terminarse en SciVelyx Graphs.

## Desde un script

```python
wells = [rf.Group(w, rf.Query([rf.Criterion("identification", "well", [w])])) for w in ("ILLUSTRATIVE-A1", "ILLUSTRATIVE-A2")]
prj.figure("qfr.pdf", kind="ternary", scheme="folk1980", groups=wells, colour_by="groups")
phik = prj.figure("phi_k.png", kind="crossplot", x="petrophysics.porosity", y="petrophysics.permeability",
                  log_y=True, colour_by="identification.facies", preset="elsevier-1col")
prj.figure("phi_k.scivelyx.json", phik)                      # abrirla en SciVelyx Graphs
prj.save_figure("Porosidad y permeabilidad", phik)
prj.presentation("barita.pptx", ("diagenetic", "constituent", "barite"), figures_=[phik])
```

## Límites y problemas comunes

* "Como máximo 10 grupos."
* "Aún no hay figuras guardadas en este proyecto." / "Aún no hay grupos guardados en este proyecto."
* "Añada diapositivas primero." — una presentación necesita al menos una diapositiva.
* Las presentaciones de PowerPoint necesitan el extra `explorer` (python-pptx), instalado con `.[all]`.

## Cobertura

M1 (hasta 10 grupos a partir de consultas guardadas), M2 (símbolo, color de relleno y de borde por grupo), M3 (métodos
de clasificación recalculados con los datos más recientes), M4 (leyenda, cuadro bajo el ratón, etiquetas, zoom,
exportación), L5 (generador de figuras y presentaciones).
