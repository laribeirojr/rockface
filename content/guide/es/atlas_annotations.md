# Anotaciones del Atlas y la búsqueda por concepto

## Para qué sirve

Las anotaciones marcan lo que muestra una imagen — una flecha en un agregado de caolinita, un rectángulo alrededor de
un feldespato disuelto, el contorno de un poro, una etiqueta — y ligan cada marca a la nomenclatura como una
**característica**: un constituyente con su hábito, localización, modificador y relación, como en una línea de la
composición. RockFace escribe la **leyenda automática** de la imagen a partir de ellas, exporta figuras con o sin las
marcas, y encuentra imágenes por lo que muestran: tipo de roca → concepto → atributo → valor.

## Antes de empezar

Una imagen abierta en RockFace Atlas (página [RockFace Atlas: láminas enteras, fotos de detalle y la biblioteca de imágenes](atlas_viewer.md)).

## Paso a paso

### Dibujar

1. Abra la pestaña **Anotaciones** del panel **Imagen, anotaciones y mapa**.
2. Elija una herramienta:
   * **Flecha** — clic donde empieza, luego hacia dónde apunta;
   * **Rectángulo** — clic en dos esquinas opuestas; **Elipse** — dos esquinas del rectángulo que la rodea;
   * **Contorno** — clic en los puntos; un doble clic, Enter o el primer punto lo cierra;
   * **Etiqueta** — clic donde va el texto y escríbalo.
3. **Seleccionar** — clic en una anotación para elegirla, arrástrela para moverla, Supr la borra.
4. **Color**, grosor de **Línea** y tamaño del **Texto**; **Aplicar estilo** los da a la anotación seleccionada.

### Decir qué muestra

1. Seleccione una anotación y pulse **Característica…**. En **Qué muestra la anotación**, elija el constituyente y su
   hábito, localización, modificador y relación (las mismas listas de la composición).
2. **Texto…** cambia el texto de una etiqueta o añade un texto a cualquier anotación.
3. Las anotaciones que dicen algo reciben las letras A, B, C… en el orden en que se dibujaron; las letras se dibujan en
   la imagen y las usa la leyenda.

### La nota y la leyenda

1. **Nota de la imagen** — un texto sobre la imagen entera, con **Añadir característica…** para lo que muestra toda la
   imagen; **Guardar la nota**.
2. **Leyenda automática** — el nombre, el tipo y la luz, el objetivo, la muestra, la profundidad y la lámina, la
   posición en la lámina, la nota, "(A) …; (B) …" y la escala. **Copiar**, o **Usar como leyenda** de la imagen.

### Exportar figuras

1. **Exportar imágenes…**
2. **Imágenes**: **La imagen abierta**, **Todas las imágenes de su lámina** o **Las imágenes de la lista de la
   biblioteca**.
3. **Anotaciones**: **Con anotaciones**, **Sin anotaciones** o **Ambas (dos archivos cada una)**.
4. **Lado mayor como máximo** (píxeles) y **Un archivo de leyenda (.txt) junto a cada imagen**.
5. Elija la carpeta.

### Encontrar imágenes por concepto

1. En la **Biblioteca de imágenes**, abra **Por concepto**.
2. **Buscar en**: **las anotaciones de las imágenes**, **las composiciones de las descripciones**, o **anotaciones y
   composiciones**.
3. Abra el árbol **Tipo de roca › concepto › atributo › valor** — por ejemplo *Subarcosa › Caolinita › Hábito › En
   libros (booklet)* — y seleccione un nodo: la biblioteca muestra las imágenes encontradas, con **Encontrada en: …**
   (las letras, la nota o la descripción). **Mostrar todas las imágenes** borra la búsqueda.

## Opciones

| Opción | Qué cambia |
|---|---|
| Color, Línea, Texto | El estilo de la anotación (también en las figuras exportadas). |
| Característica | Lo que muestra la anotación, con la nomenclatura de RockFace. |
| Buscar en | Buscar en las anotaciones, en las composiciones de las láminas, o en ambas. |

## Cómo funciona

Las anotaciones se guardan en los píxeles a resolución completa de su imagen, por lo que quedan en su lugar con
cualquier zoom y en cualquier exportación. Las características usan los códigos de la base de conocimiento; así, una
leyenda se escribe en el idioma de la interfaz (o de la exportación), y la búsqueda encuentra una imagen sea cual sea
el idioma en que se anotó. El tipo de roca de una imagen es la clasificación de las descripciones de su lámina.

## Desde un script

```python
img = prj.image("Field B — kaolinite booklets")
img.annotate("rect", [[820, 410], [1260, 760]], features=[rf.Feature("kaolinite", habit="booklet")])
img.annotate("label", [[1300, 420]], text="Kln")
img.note("Libros de caolinita rellenan los poros.", [{"constituent": "kaolinite"}])
print(img.caption_auto("es"))
for found, reasons in prj.search_images(concept="kaolinite", attribute="habit", value="booklet"):
    found.export(f"{found.name}.png", max_side=3000, annotated=True, caption_file=True)
prj.export_images("figuras", annotated=True, caption_file=True, lang="es")
```

## Límites y problemas comunes

* Se rechaza una característica con un código desconocido para la base de conocimiento.
* Una sola nota por imagen: una nueva nota reemplaza la anterior.
* "¿Eliminar esta anotación?" — eliminar no se puede deshacer; las letras de las demás se reordenan.

## Cobertura

R2 (búsqueda jerárquica: tipo de roca → concepto → atributo → valor), R3 (editor de imágenes: flechas, contornos,
letras, notas; características con la nomenclatura).
