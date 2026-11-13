# Pozos a LAS

## Para qué sirve

Las descripciones de un pozo escritas como un archivo **LAS 2.0** — uno por pozo —, para que los programas de
modelado de reservorios como Petrel, Techlog o Geolog lean la petrografía como curvas contra la profundidad: porosidad
y permeabilidad, totales, clasificaciones, facies… Los atributos de texto pasan a ser curvas discretas con sus tablas
de códigos.

## Antes de empezar

* Descripciones con un pozo y una profundidad.
* Opcional: una consulta en Explorer, para escribir solo las descripciones encontradas.

## Paso a paso

1. En RockFace Explorer, **Exportar → Pozos a LAS (Petrel)…**. Se abre el diálogo **Pozos a LAS 2.0**.
2. **Profundidad de las muestras**: medida (tope), corregida o ajustada.
3. **Empresa** — escrita en el encabezado.
4. **Solo las N descripciones de la consulta**, o todas las descripciones.
5. **Curvas (un valor por profundidad de muestra)**: marque los atributos a escribir (porosidad, permeabilidad,
   densidad de grano, totales, clasificaciones, facies, zona…). Cada uno tiene su mnemónico y unidad.
6. **Primer archivo** muestra el comienzo del primer archivo, para revisar.
7. **Escribir…** y elija la carpeta. "N archivos LAS escritos en …".

## Opciones

| Opción | Qué cambia |
|---|---|
| Profundidad de las muestras | Qué profundidad de la identificación es la curva DEPT. |
| Curvas | Curvas numéricas, o curvas discretas para atributos de texto (códigos enteros con su tabla). |

## Cómo funciona

* Un archivo LAS 2.0 por pozo, con paso de profundidad irregular (`STEP 0`) y `NULL -999.25`.
* Los atributos de texto (facies, una clasificación) pasan a ser curvas discretas de códigos enteros; la tabla de
  códigos va en las secciones Parameter y Other.
* Dos muestras a la misma profundidad se unen.
* Los archivos se comprobaron con dos lectores independientes (lasio y el LASReader de W. Weckesser): cada valor es
  igual al registro, los elementos obligatorios del encabezado están presentes y lasio no da ningún aviso.

## Desde un script

```python
prj.export_las("las", ("identification", "formation", "Example Carbonate Unit"),
               curves=["petrophysics.porosity", "petrophysics.permeability", rf.Curve("totals.qt", "QT", "%"),
                       "identification.facies"],
               depth="corrected_depth", company="ILLUSTRATIVE")
las = rf.las.read("las/ILLUSTRATIVE-A1.las")             # lee de vuelta un archivo LAS 2.0
```

## Límites y problemas comunes

* "Ninguna muestra con esta profundidad." — la profundidad elegida está vacía en esas muestras (por ejemplo, sin
  profundidad ajustada).
* Las muestras sin pozo quedan fuera.
* Para perfiles de imagen y curvas de RockFace MC, vea [RockFace MC: perfiles de imagen](mc_image_logs.md) (LAS, CSV, DLIS, NetCDF) y la exportación
  WITSML (página [Exportar pozos a WITSML y muestras a OSDU](exports.md)).

## Cobertura

P38 (exportación a LAS para programas de modelado de reservorios), L4 (exportador de LAS para Petrel).
