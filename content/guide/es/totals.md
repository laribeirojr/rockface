# Totales

## Para qué sirve

Un **total** suma las líneas de la composición de un tipo: todo el cuarzo, los feldespatos, el cemento intergranular,
la porosidad de disolución, los bioclastos… RockFace tiene 50 totales incorporados y las medidas de compactación IGV,
COPL, CEPL e ICOMPACT, calculados sobre la composición actual y sobre la **original** (antes de la diagénesis). Un
proyecto puede añadir sus propios totales. Las clasificaciones, figuras, consultas y curvas LAS los usan.

## Antes de empezar

Una descripción con su composición (página [Composición](composition.md)).

## Paso a paso

### Leer los totales

1. Abra la pestaña **Clasificación**. La tabla **Totales** está a la izquierda.
2. Cada fila da un total en % del volumen de la roca, en dos columnas:
   * **Actual** — de la composición tal como se describió;
   * **Original** — de la composición antes de la diagénesis: la fracción de cada línea de reemplazo o de disolución
     vuelve al constituyente que reemplazó o disolvió.
3. Los totales se guardan automáticamente con la descripción: no hay botón que pulsar.

### Un total personalizado

1. **Totales personalizados…** abre **Totales personalizados del proyecto**.
2. **Nueva** y dé al total un **Código** y un nombre.
3. Añada **Condiciones**: una línea se elige cuando coincide con todas las columnas de una condición — tipo, grupo,
   constituyente, localización, hábito, modificador, relación. Haga doble clic en una celda para elegir códigos:
   marcado significa *incluir*, parcialmente marcado significa *excluir*; una celda vacía (*cualquiera*) acepta todo.
   **Añadir condición**, **Quitar condición**.
4. **En esta descripción: … %** muestra el resultado al instante.
5. **Aceptar**. El total aparece, marcado *personalizado*, en todas las descripciones del proyecto.

## Opciones

Los totales incorporados incluyen:

| Grupo | Totales |
|---|---|
| Roca entera | volumen, primarios, diagenéticos, porosidad, granos del armazón |
| Origen | extracuencales, intracuencales, intracuencales no carbonáticos (Zuffa 1980) |
| Proveniencia | Qm, Qp, chert, cuarzo, Qt, feldespatos, feldespatos potásicos, plagioclasa, fragmentos de roca por tipo, L, Lt (Dickinson 1985) |
| Otros | micas, minerales pesados, matriz, matriz deposicional |
| Carbonatos | granos no esqueletales, bioclastos, constituyentes del presal, aloquímicos, lodo calcáreo, dolomita, carbonatos, evaporitas |
| Diagénesis | cementos (todos, intergranular, silíceo, carbonático, arcilloso, de sulfatos), feldespato diagenético, de reemplazo, desplazantes |
| Poros | intergranular, intragranular y móldica, de disolución, de fractura, microporosidad |
| Compactación | IGV, COPL, CEPL, ICOMPACT |

## Cómo funciona

* Un total suma los porcentajes de las líneas elegidas por cualquiera de sus condiciones.
* IGV = porosidad intergranular + cemento intergranular + matriz deposicional (Paxton et al. 2002).
* COPL = Pi − ((100 − Pi) × IGV) / (100 − IGV) y CEPL = (Pi − COPL) × C / IGV, con Pi = 40 % (Lundegard 1992);
  ICOMPACT = COPL / (COPL + CEPL) (Ehrenberg 1995).
* La lista de todos los totales, con sus condiciones y fuentes, está en `docs/NOMENCLATURE.md` del código fuente.

## Desde un script

```python
d = prj["TS-9"]
t = d.totals()                       # todos los totales en % de la roca
print(t["qt"], t["intergranular_cement"], t["igv"], d.totals(original=True)["feldspar"])
prj.add_total("kaolinite_all", "Caolinita (toda)", rf.Selector(constituents=["kaolinite"]))
rows = prj.table(totals=["volume", "igv", "kaolinite_all"])
prj.to_csv("totales.csv", rows)
```

## Límites y problemas comunes

* Se rechaza un total personalizado con un código ya usado.
* IGV, COPL y CEPL se definieron para areniscas; RockFace los calcula para cualquier roca, así que léalos con cuidado
  en carbonatos.
* La composición original solo es tan buena como las relaciones paragenéticas dadas en la composición (reemplaza,
  disolución de…).

## Cobertura

P26 (tabla de totales, totales personalizados, guardados automáticamente), P27 (más de 30 totales automáticos), P28
(editor de totales personalizados).
