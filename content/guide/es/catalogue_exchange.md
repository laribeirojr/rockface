# Catálogo de muestras, tabla para Touchstone y XML por mapeo

## Para qué sirve

**Catálogo de muestras** recorre los pozos y las muestras de un catálogo corporativo e importa los archivos elegidos.
La **Tabla para Touchstone** escribe las cantidades petrográficas que usa el modelado diagenético. **Importar XML con un
mapeo** lee descripciones escritas por otro programa.

## Antes de empezar

* Catálogo: una carpeta compartida `<pozo>/<muestra>/` (con un `sample.json` opcional de `top_m`, `base_m`, `type`),
  o una plataforma OSDU con el token en `ROCKFACE_OSDU_TOKEN`.
* Importar XML: el archivo XML y un mapeo (JSON) que dice dónde está cada cosa en él.

## Paso a paso

1. **Petro → Inicio → Catálogo de muestras…**: elija *Carpeta compartida* o *Plataforma OSDU*, la dirección,
   **Conectar**; busque un pozo; marque los archivos de sus muestras; **Importar los archivos marcados**. Las imágenes
   van a Atlas, los volúmenes a MC, los LAS a los perfiles del pozo, los informes en PDF a los análisis de la muestra.
2. **Petro → Inicio → Tabla para Touchstone…**: elija dónde guardar el CSV.
3. **Petro → Inicio → Importar XML con un mapeo…**: elija el XML y luego el mapeo. Se listan los códigos sin
   correspondencia.

## Opciones

| Clave del mapeo (XML) | Significado |
|---|---|
| description | ruta del elemento de una descripción (p. ej. `.//description`) |
| name, well, top_depth, thin_section | rutas dentro de él (`@atributo`, `hijo`, `hijo/@atributo`) |
| line, code, percent, points | las líneas de composición y sus campos |
| codes | los códigos del otro programa → constituyentes de RockFace |

El mapeo de Touchstone lista las columnas: cada una un campo (nombre, pozo, profundidad, tamaño de grano, selección) o
una suma de totales o constituyentes.

## Cómo funciona

* El catálogo usa conectores con las mismas tres preguntas (pozos, muestras, un archivo): una carpeta, o el servicio
  de búsqueda de OSDU (`POST /api/search/v2/query`). El pozo y la muestra se encuentran o se crean por nombre y
  profundidad.
* El formato de entrada de Touchstone no está publicado: la tabla trae las cantidades del modelo publicado (Lander &
  Walderhaug 1999; Lander et al. 2008) y dice en su primera línea que no es ese formato.
* XML por mapeo: cada código debe corresponder a un constituyente de la nomenclatura; nada se adivina.

## Desde un script

```python
cat = rf.catalogue.FolderConnector("//servidor/catalogo")
s = cat.samples("ILL-WELL-A")[0]
rf.catalogue.import_items(prj.raw, cat, s, s.items)
prj.touchstone_table("touchstone.csv")
prj.import_mapped_xml("descripciones.xml", mapeo)
```

## Límites y problemas comunes

* Un conector a un catálogo corporativo de muestras se agregará cuando su interfaz esté documentada para RockFace.
* El XML de otro programa y el "formato de Touchstone" solo se llamarán así después de leer archivos reales.

## Cobertura

GV16 (navegador de catálogo; conector corporativo pendiente), P35 (Touchstone; definitivo con un archivo real), P37
(importador de XML).
