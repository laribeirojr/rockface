# Informes

## Para qué sirve

Un **informe** escribe una o muchas descripciones como documento: PDF para imprimir o archivar, Word (DOCX) o Excel
(XLSX) para editar, o páginas HTML para leer en un navegador — en inglés, español o portugués, sea cual sea el idioma
de la interfaz. Contiene las secciones que usted elija: identificación, descripción, composición, totales,
clasificaciones con sus diagramas ternarios, diagénesis con el gráfico paragenético, análisis, solicitudes, las
imágenes de la lámina y sus análisis puntuales.

## Antes de empezar

Las descripciones guardadas: los cambios sin guardar no entran en el informe.

## Paso a paso

1. **Inicio → Informes e intercambio → Informe…** (Ctrl+P).
2. **Descripciones**: marque las que van en el informe (**Todas**, **Ninguna**). La descripción abierta viene
   marcada.
3. **Formato**: PDF, Word, Excel o HTML.
4. **Idioma del informe**: English, Español o Português.
5. **Secciones**: Identificación, Macroscópica, Microscópica, Sistema poroso, Composición, Totales, Clasificaciones,
   Diagénesis, Análisis, Solicitudes, Imágenes de la lámina, Análisis puntuales.
6. Diagramación:
   * **Ancho de las imágenes (mm)** y **Ancho de los diagramas ternarios (mm)**;
   * **Figuras**: **En sus secciones** o **Todas al final**;
   * **También la composición original (antes de la diagénesis)**.
7. Para HTML, marque **HTML: una página por descripción, con una página índice** y elija la **Carpeta para las
   páginas HTML**: cada descripción tiene su página, e `index.html` las enlaza.
8. **Abrir el archivo al terminar** y luego **Generar informe…**, eligiendo dónde guardarlo.

"Los archivos Word, Excel y HTML se pueden editar después de exportar."

## Opciones

| Opción | Qué cambia |
|---|---|
| Formato | PDF (A4), DOCX, XLSX (una hoja con la lista de descripciones y una hoja por descripción) o HTML. |
| Idioma del informe | Independiente del idioma de la interfaz. |
| Secciones | Solo se escriben las secciones marcadas. |
| Ancho de las imágenes / de los diagramas ternarios | Tamaño de las figuras en el documento, en mm. |
| Figuras | Dentro de sus secciones, o todas reunidas al final. |
| Composición original | Añade la composición antes de la diagénesis, con sus totales y clasificaciones. |

## Cómo funciona

El informe se arma con los mismos registros que muestran los formularios (los códigos traducidos al idioma del
informe); los números se escriben con el separador decimal de ese idioma. Los diagramas ternarios y el gráfico
paragenético se dibujan como en el programa. Explorer genera informes de las descripciones encontradas por una
consulta con el mismo diálogo (página [RockFace Explorer: consultas, tablas de resultados y exportaciones](explorer_queries.md)).

## Desde un script

```python
with rf.open("estudio.rockface") as prj:
    prj["TS-9"].report("TS-9.pdf", lang="es")
    prj.report("pozo-1.docx", names=["TS-9", "TS-10"], lang="en",
               sections=["identification", "composition", "classification"], figure_mm=120, figures="end")
    prj.html_pages("sitio", lang="pt")                 # una página por descripción e index.html
```

## Límites y problemas comunes

* "Ninguna descripción elegida."
* Word y Excel necesitan el extra `reports` (python-docx, openpyxl), instalado con `.[all]`.
* Las imágenes de láminas enteras muy grandes se escriben reducidas al ancho de imagen elegido.

## Cobertura

P10 (informes en inglés, portugués y español), P34 (informes: PDF, Excel, HTML, Word; idioma; configuración), P36
(generador de HTML por lotes).
