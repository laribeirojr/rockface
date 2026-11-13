# Composición

## Para qué sirve

La pestaña **Composición** es la tabla de lo que forma la roca: constituyentes primarios, constituyentes
diagenéticos y tipos de poro, cada uno con sus atributos (localización, hábito, modificador, relación paragenética) y
su cantidad — puntos contados, un porcentaje manual o una estimación visual. Los totales, las clasificaciones, la
interpretación diagenética, los informes y las consultas se calculan a partir de ella.

## Antes de empezar

Una descripción abierta. Los constituyentes y atributos vienen de la base de conocimiento (página
[Nomenclatura, escalas y referencias (la base de conocimiento)](nomenclature_knowledge_base.md)).

## Paso a paso

### Añadir líneas

1. Abra la pestaña **Composición**.
2. **Añadir…** (Ins). En el diálogo **Línea de composición**, elija el **Constituyente** en las listas agrupadas
   (constituyentes primarios, constituyentes diagenéticos, poros); escriba en el filtro para encontrarlo en cualquier
   idioma.
3. Dé los atributos que admite su tipo:
   * primario — **Localización**, **Modificador**;
   * diagenético — **Hábito**, **Localización**, **Modificador**, **Relación** (paragenética), **Constituyente
     relacionado** y **Su localización**;
   * poro — **Localización**, **Modificador**, **Relación**, **Constituyente relacionado**.
4. Dé la cantidad, una de estas:
   * **Puntos** — puntos contados;
   * **% manual** — un porcentaje medido de otra forma;
   * **Cantidad nominal** — una estimación visual en los escalones de las cartas de comparación (traza, 1, 2, 3, 5, 7,
     10, 15, 20, 25, 30, 40, 50 %).
5. **Observación** — una nota sobre esta línea. **Aceptar**.

El mismo constituyente puede aparecer en varias líneas con atributos distintos (por ejemplo, calcita como cemento
poiquilotópico intergranular y como reemplazo de feldespato).

### Contar con clics y teclas

* Un **doble clic** en la celda de Puntos de una línea añade un punto; **Alt + doble clic** quita uno.
* **Teclas…** asigna líneas a las teclas 1–0 y Ctrl+1–0 (veinte teclas): pulsar una tecla suma un punto a su línea.
* La línea bajo la tabla muestra los puntos y las fracciones: "… puntos · primarios … % · diagenéticos … % · poros …
  % · total … %".
* **Borrar puntos** pone todos los conteos en cero y conserva las líneas.

Para contar sobre la imagen de la lámina, guardando la posición de cada punto, use la pestaña **Conteo de puntos**
(página [Conteo de puntos](point_counting.md)).

### Editar la tabla

| Botón | Tecla | Hace |
|---|---|---|
| Atributos… | Enter | Edita la línea seleccionada. F2 edita una sola celda. |
| Eliminar | Supr | Elimina las líneas seleccionadas. |
| Copiar, Pegar | Ctrl+C, Ctrl+V | Copia líneas, también a otra descripción. |
| Subir, Bajar | Ctrl+↑, Ctrl+↓ | Mueve las líneas seleccionadas. |
| Agrupar, Desagrupar | Ctrl+G, Ctrl+U | Reúne líneas bajo un grupo con nombre, o lo deshace; **Vista agrupada** muestra los grupos. |
| Color de las líneas seleccionadas… | | Un color para las líneas (usado también en el conteo de puntos y los informes). |
| Deshacer, Rehacer | Ctrl+Z, Ctrl+Y | Todo cambio de la tabla. |
| Plantilla… | | Carga la composición de una plantilla: reemplazar las líneas, o añadir las que faltan. |
| Preferencias… | | **Dobles clics por punto** y **Recordarme guardar cada** N puntos. |

**Guardar** (Ctrl+S) al terminar; el recordatorio aparece tras el número de puntos fijado en las preferencias.

## Opciones

| Opción | Qué cambia |
|---|---|
| Dobles clics por punto | Cuántos dobles clics hacen un punto (al menos 1). |
| Recordarme guardar cada | Un recordatorio en la barra de estado tras N puntos (0 = nunca). |
| Vista agrupada | Líneas bajo sus grupos, o como una sola lista. |

## Cómo funciona

* Las líneas con % manual o cantidad nominal conservan ese valor ("líneas fijas"); las líneas contadas reparten lo que
  queda, 100 − fijas, en proporción a sus puntos. Sin ningún punto contado, los porcentajes son solo los valores
  fijos. Una línea con puntos y un % cuenta por sus puntos (con un aviso).
* Los escalones nominales siguen las cartas de comparación de Terry y Chilingar (1955); una traza cuenta como 0 %.
* Los atributos que puede tener un constituyente vienen de la base de conocimiento ("Se aplica a"), por lo que nunca se
  da un hábito a un grano primario.

## Desde un script

```python
d = prj["TS-9"]
d.add_line("quartz_mono", points=112, location="framework")
d.add_line("calcite_dia", points=24, habit="poikilotopic", location="ig_pore_filling")
d.add_line("kaolinite", nominal="3", habit="booklet", location="intragranular_replacive",
           relation="replaces", related="k_feldspar")
for line in d.lines():
    print(line["constituent"], round(line["share"], 2))      # quartz_mono 79.88, calcite_dia 17.12, kaolinite 3.0
d.save()
```

## Límites y problemas comunes

* "… no se aplica a …": un atributo que el tipo del constituyente no admite.
* "… aparece dos veces con los mismos atributos (vea la línea …)": junte las dos líneas.
* "Los porcentajes manuales y nominales suman … %, más de 100 %."
* "…: sin localización." — un aviso para constituyentes diagenéticos.
* "Se indicó la localización del constituyente relacionado sin el constituyente."

## Cobertura

P18 (tabla de composición), P19 (atributos), P20 (puntos, % manual, cantidad nominal, observación), P21 (grupos y
colores), P22 (copiar, pegar, mover, deshacer), P23 (teclas), P24 (borrar puntos, plantilla, preferencias,
recordatorio de guardar).
