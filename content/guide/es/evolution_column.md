# Evolución paragenética y la columna estratigráfica

## Para qué sirve

La **evolución paragenética** pone en un solo cuadro las fases diagenéticas de varias muestras — una formación, un
campo, una consulta: los eventos en orden, su régimen (eo-, meso-, telodiagénesis), la fuente del agua de cada uno, la
cantidad media y el número de muestras, las edades U-Pb y fotos de las fases. La **columna estratigráfica** ubica las
formaciones con sus edades de depósito y las edades U-Pb de las muestras, para mostrar que cada cemento es más joven
que la roca que lo contiene.

## Antes de empezar

* Descripciones con su composición y relaciones paragenéticas (página [Diagénesis: ambientes, secuencia paragenética y grafo de conocimiento](diagenesis.md)).
* Para las edades: fases datadas (página [Datación U-Pb en el diagrama de Tera-Wasserburg](dating.md)).
* Para la columna: las formaciones con sus edades de depósito (abajo).

## Paso a paso

### La evolución

1. En RockFace Explorer, abra la pestaña **Evolución** y luego **Evolución paragenética**.
2. Las descripciones son las de la consulta de la pestaña Consulta (**Solo las descripciones de la consulta**), o
   todas.
3. La tabla lista los **Eventos (fases)** en orden, con su **Régimen**, **Fuente del agua**, **% medio (n)** y **Edad
   U-Pb**. "N muestras, P fases, C relaciones en contradicción entre muestras."
4. Cambie el **Régimen** o la **Fuente del agua** de una fase en su celda (Marina, Meteórica, Evaporítica, Lago
   alcalino, Agua de poro somera, De cuenca (soterramiento), Hidrotermal, Sin interpretar): su elección queda en el
   proyecto.
5. **Fotos de las fases** añade fotos de cada fase al cuadro: las fotos de sus puntos datados, luego las imágenes Atlas
   anotadas con su constituyente.
6. **Cuadro de evolución…** guarda el cuadro (PNG, SVG, PDF); **Eventos (CSV)…**, la tabla.

### La columna estratigráfica

1. Abra **Edades en la estratigrafía**.
2. En **Formaciones, de techo a base (edades de depósito, Ma)**, **Añadir formación** y dé el nombre de la
   **Formación**, el **Techo (Ma)**, la **Base (Ma)** y el **Color**. **Guardar formaciones**.
3. La columna muestra cada formación con su intervalo de edad y, al lado, las edades U-Pb guardadas para sus muestras.
4. **Columna estratigráfica…** la guarda.

## Opciones

| Opción | Qué cambia |
|---|---|
| Solo las descripciones de la consulta | La evolución de las muestras encontradas, o de todas. |
| Régimen, Fuente del agua | Fijados a mano para una fase (se borran con un valor vacío). |
| Fotos de las fases | Fotos en el cuadro. |

## Cómo funciona

Cada fase es un constituyente con su hábito y su tipo (precipitación o disolución), reunido entre las muestras. Los
eventos se ordenan por régimen, luego por las relaciones paragenéticas de todas las muestras juntas, luego por su
lugar en la secuencia de cada muestra; las relaciones que se contradicen entre muestras se cuentan y quedan fuera. El
régimen viene de las reglas diagenéticas (una fase sin régimen toma el de las fases anteriores), la fuente del agua de
los ambientes interpretados, salvo que se fijen a mano. Las edades se ponen en la fase que datan (mineral y hábito de
la edad guardada).

## Desde un script

```python
evo = prj.evolution(formation="Example Formation", path="evolucion.png")
for ph in evo.phases:
    print(ph.event, ph.label, ph.regime, ph.water, ph.share_mean, ph.ages)
prj.set_phase(evo.phases[-1].key, water="hydrothermal")
prj.stratigraphy = [{"name": "Example Formation", "top": 100.0, "base": 108.0, "colour": "#E9D7A5"}]
prj.strat_column("columna.pdf")
```

## Límites y problemas comunes

* Una fase sin relaciones paragenéticas en ninguna muestra se ubica solo por su régimen y su lugar en la secuencia de
  cada muestra.
* La columna necesita las edades de depósito de las formaciones (base más antigua que el techo).

## Cobertura

L8 (secuencia paragenética de varias muestras), L12 (edades en la estratigrafía; evolución paragenética de varias
muestras con cuantificación y fotos).
