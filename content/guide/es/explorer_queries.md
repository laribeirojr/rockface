# RockFace Explorer: consultas, tablas de resultados y exportaciones

## Para qué sirve

RockFace Explorer hace preguntas a una colección entera: *¿qué muestras tienen barita?*, *¿qué muestras del pozo X
tienen datación U-Pb?*, *los grainstones con porosidad mayor que 15 % y permeabilidad mayor que 100 mD*. Una consulta
puede usar cualquier concepto de una descripción — identificación, textura, composición con sus atributos, sistema
poroso, petrofísica, análisis, clasificaciones, totales, la interpretación diagenética, imágenes, análisis puntuales,
mapas minerales — y da las descripciones encontradas, una tabla de cualquier concepto para ellas con sus fotos, y
exportaciones.

## Antes de empezar

* Un proyecto con descripciones. Para probar Explorer: Ayuda → **Abrir la colección ILUSTRATIVA** (48 descripciones).
* Una pregunta también se puede escribir en lenguaje natural en el cuadro de búsqueda de arriba (página [Mio: preguntas en lenguaje natural y el modelo de lenguaje local](mio.md)).

## Paso a paso

### Abrir Explorer

**Inicio → Colección → Explorer** (Ctrl+Shift+E), o `rockface explorer proyecto.rockface`. Se abre la pestaña
**Consulta**.

### Una consulta simple

1. **Atributos**: un atributo de la identificación (pozo, campo, formación, zona, facies, tipo de roca,
   profundidades, tipo de muestra, usos…).
2. **Valores (descripciones)** lista sus valores con el número de descripciones que tiene cada uno. Marque o
   seleccione uno o más.
3. Para un número, dé el **Intervalo numérico**: **Desde** y **Hasta** (un extremo puede quedar vacío); "Encontrado: …
   a …" muestra el intervalo en la colección.
4. **Añadir a los criterios**. El criterio aparece en **Criterios de selección (Supr elimina)**.
5. Añada más criterios: una descripción debe cumplirlos todos. "N de M descripciones cumplen todos los criterios."

### Una consulta avanzada

1. **Avanzada** muestra los **Conceptos**: Identificación, Textura macroscópica y microscópica, Composición primaria,
   Composición diagenética, Poros en la composición, Sistema poroso, Petrofísica, Análisis de laboratorio,
   Clasificaciones, Totales, Interpretación diagenética, Imágenes, Análisis puntuales, Mapas minerales.
2. Elija un concepto, luego un atributo y sus valores o intervalo, y **Añadir a los criterios**.
3. Dentro de un concepto, los criterios deben cumplirse en **la misma fila**: "constituyente diagenético = calcita" y
   "hábito = poiquilotópico" encuentran las muestras con calcita poiquilotópica, no las que tienen algo de calcita y
   algo poiquilotópico.

### La tabla de resultados

1. **Descripciones encontradas** las lista; elija algunas para ver solo esas en la tabla y exportarlas (ninguna
   elegida: todas).
2. **Tabla de**: el concepto a mostrar — por ejemplo Petrofísica, o Composición diagenética con la fracción de cada
   línea. **Todas las filas** muestra todas las filas de las descripciones encontradas, no solo las que cumplen los
   criterios.
3. La columna **Fotos** da el número de imágenes de cada lámina; seleccione una fila para ver la foto, haga doble clic
   para abrir la descripción en RockFace Petro.
4. Haga clic en el encabezado de una columna para ordenar.

### Guardar y exportar

* **Guardar consulta…** (dé un nombre), **Abrir consulta…**, **Nueva consulta**; el diálogo **Consultas guardadas**
  también las **Carga** y **Elimina**. Las consultas quedan en el proyecto.
* **Exportar**:
  * **Tabla de resultados a Excel o CSV…** — los números siguen siendo números;
  * **Descripciones encontradas (HTML, Excel, PDF, Word)…** — con el diálogo de informe (página [Informes](reports.md));
  * **Descripciones seleccionadas en la tabla a HTML…** o **a XML…** (un archivo de intercambio, página [Exportar e importar descripciones](exchange.md));
  * **Pozos a LAS (Petrel)…** y **Presentación de la consulta (.pptx)…** (página [Grupos, figuras y presentaciones](groups_figures.md)).
* **Leer de nuevo** recarga las descripciones tras cambios hechos en Petro.

## Opciones

| Opción | Qué cambia |
|---|---|
| Avanzada | Todos los conceptos en vez de solo la identificación. |
| Todas las filas | Todas las filas de las descripciones encontradas, no solo las que cumplen los criterios. |
| Descripciones encontradas (elegidas) | Limitan la tabla y las exportaciones a ellas. |

## Cómo funciona

Cada descripción se lee en *hechos*, por concepto: una fila por línea de composición, por análisis, por punto, por
fase de mapa… Una descripción cumple la consulta cuando, para cada concepto nombrado, una misma fila cumple todos los
criterios de ese concepto, y se cumplen todos los conceptos. Los hechos se leen en unos 8 ms por descripción y una
consulta se responde en alrededor de 1 ms sobre 480 descripciones. Las plantillas quedan fuera.

## Desde un script

```python
with rf.open("coleccion.rockface") as prj:
    print([d.name for d in prj.query(("diagenetic", "constituent", "barite"))])          # ¿qué muestras tienen barita?
    print([d.name for d in prj.query(("spots", "system", "U-Pb"), well="ILLUSTRATIVE-A2")])   # datadas, en el pozo A2
    buenas = prj.query(("petrophysics", "porosity", 15, None), ("petrophysics", "permeability", 100, None))
    prj.save_query("Buen reservorio", ("petrophysics", "porosity", 15, None))
    header, rows = prj.query_table("petrophysics", facies="Grainstone")
    prj.export_table("buenas.xlsx", "petrophysics", ("petrophysics", "porosity", 15, None))
```

## Límites y problemas comunes

* "Marque o seleccione al menos un valor." / "Escriba números para el intervalo (un extremo puede quedar vacío)."
* "La consulta aún no tiene criterios." / "Dé un nombre a la consulta."
* "Nada que exportar: ninguna descripción encontrada o seleccionada."

## Cobertura

Q1 (consulta simple), Q2 (consulta avanzada sobre todos los conceptos), Q3 (intervalos numéricos), Q4 (lista de
criterios), Q5 (tabla de resultados), Q6 (consultas guardadas), Q7 (exportación a Excel), Q8 (descripciones
encontradas a HTML, Excel y PDF), Q9 (descripciones seleccionadas a HTML y XML), Q10 (configuración de la
exportación), Q11 (columna de fotos), L1 (búsqueda: "¿qué muestras tienen barita?").
