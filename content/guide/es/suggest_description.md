# Sugerir descripción: del mapa de segmentación a la descripción

## Para qué sirve

Un mapa de segmentación ya dice cuánto de la lámina ocupa cada mineral y los poros. **Sugerir descripción** lo
convierte en propuestas para la descripción de la lámina — una línea de composición para cada constituyente con sus
puntos, la porosidad visual y, de un mapa de objetos de granos, la moda granulométrica principal y la selección — y
escribe solo lo que usted marque. Ahorra escribir lo que el mapa ya midió y mantiene al petrógrafo al mando.

## Antes de empezar

* En Lab, una lámina con mapa de segmentación: hecho en **Lab → Segmentación**, por un modelo de IA en **Lab → IA**, o
  importado como mapa mineralógico en Atlas.
* Una descripción de esa lámina (creada en Petro).
* Las fases del mapa nombradas con conceptos de la nomenclatura (la leyenda del mapa; Atlas → mapa mineralógico →
  fases).

## Paso a paso

1. **Lab** → elija la lámina; abra el mapa (o deje cualquier imagen: se usa el último mapa de la lámina).
2. Haga clic en **Sugerir descripción** en la barra de herramientas. Si la lámina tiene varias descripciones, elija
   una.
3. El diálogo muestra la sugerencia como una frase y una casilla por ítem:
   * cada constituyente con su fracción del área contada y sus puntos en un conteo de 300 puntos — cuando la fase del
     mapa admite varios constituyentes (una fase llamada "cuarzo"), los otros aparecen (*o …*) para revisar;
   * la porosidad visual (las fases de poro);
   * la moda granulométrica y la selección, cuando se da un mapa de objetos de granos (script).
4. Desmarque lo que no quiera y haga clic en **Escribir lo marcado**. Cada línea escrita dice en su observación que
   fue sugerida a partir del mapa.

En el panel de Mio, `@mio sugiere la descripción de ILL-NL-003` (o la skill *ficha de la muestra*) muestra la misma
sugerencia como texto, sin escribir nada.

## Opciones

| Ítem | Se escribe en |
|---|---|
| Línea de composición | la composición: una línea nueva con los puntos, o los puntos del mismo constituyente reemplazados |
| Porosidad visual | el sistema poroso: porosidad total |
| Granulometría | la textura de la lámina: moda principal (mm y clase de Wentworth) |
| Selección | la textura de la lámina: clase de selección y σI |

## Cómo funciona

* El mapa se cuantifica sin las fases de fondo y no clasificadas (como en Atlas → mapa mineralógico); la fracción de
  cada fase se vuelve puntos de un conteo de 300 puntos, redondeados (una fracción menor que un punto aparece pero no
  es aplicable).
* Los conceptos de la fase dan el constituyente: el primer constituyente nombrado, o el primer constituyente de un
  grupo nombrado; su clase (primario, diagenético, poro) viene de la base de conocimiento.
* Granulometría y selección son las medidas gráficas de Folk y Ward (1957) de los diámetros de Feret máximos de los
  objetos de grano, clasificadas por Wentworth (1922) y los términos de selección de Folk y Ward.
* La frase se escribe desde una plantilla en español, inglés o portugués, así que cada número es un número del mapa;
  un modelo de lenguaje puede reescribirla, y la reescritura se conserva solo con exactamente los mismos números.

## Desde un script

```python
d = prj["ILL-NL-003"]
s = d.suggestion()                                   # el último mapa de su lámina
print(rf.suggest.text(s, "es", prj.kb))
print([(i.key, i.percent, i.points) for i in s.items])
d.apply_suggestion(s, accept=["porosity", "line:calcite_dia"])
s = prj.suggest_description("mi mapa", objects="mis granos")      # con granulometría y selección
```

## Límites y problemas comunes

* "Esta lámina no tiene mapa de segmentación": haga uno en Lab → Segmentación o Lab → IA.
* Una fase nombrada solo por una clase ("Cemento") aparece pero no es aplicable: nómbrela con un constituyente en la
  leyenda del mapa.
* Los puntos reemplazan los del mismo constituyente en la composición (sin hábito ni ubicación); las líneas con
  hábito o ubicación quedan como están.

## Cobertura

"Segmentación convertida en sugerencias de descripción" de la etapa 0.27 del ROADMAP; L7 (cuantificación de la
lámina entera) llevada a la descripción.
