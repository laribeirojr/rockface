# Proyectos y descripciones

## Para qué sirve

Un **proyecto** guarda una colección: sus pozos y afloramientos, muestras, láminas, descripciones, imágenes,
análisis, volúmenes y perfiles. Una **descripción** es el registro del petrógrafo sobre una lámina. Esta página trata
de crear y abrir proyectos, y de crear, cargar, guardar, copiar, eliminar y usar descripciones como plantillas.

## Antes de empezar

RockFace Petro abierto (página [Primeros pasos](getting_started.md)).

## Paso a paso

### Un proyecto

1. **Inicio → Proyecto → Nuevo proyecto** (Ctrl+Shift+N): elija una carpeta y un nombre. El archivo termina en
   `.rockface`.
2. **Abrir proyecto…** (Ctrl+O) abre uno existente; la lista **Recientes** de la página de inicio guarda los últimos.
3. **Guardar proyecto como…** escribe una copia del proyecto entero con otro nombre y sigue en la copia.
4. **Cerrar proyecto** vuelve a la página de inicio.

Un proyecto en un servidor del equipo se abre con **Conectar al servidor** (página [Trabajar en equipo en un servidor](server.md)).

### Una nueva descripción

1. **Inicio → Descripción → Nueva descripción** (Ctrl+N).
2. Escriba el **Nombre de la nueva descripción** y elija su **Lámina delgada**:
   * una lámina nueva, o
   * una ya existente, cuando varios petrógrafos (o varios estudios) describen la misma lámina. La identificación
     empieza entonces con lo que ya se sabe de esa lámina: pozo, profundidades, muestra, números.
3. Se abre la pestaña **Identificación**. Complétela (página [Identificación de una muestra](identification.md)) y las otras pestañas que necesite.
4. **Guardar** (Ctrl+S). Todas las pestañas se comprueban juntas: cualquier error impide guardar, y se muestra la
   primera pestaña con un error, con el campo marcado.

En el panel **Proyecto**, un doble clic en una lámina también empieza una nueva descripción de ella.

### Cargar, guardar y copiar

* **Cargar descripción…** (Ctrl+L) lista las descripciones con su pozo, profundidad y lámina; escriba en **Filtrar…**
  para acortar la lista. Un doble clic en el panel **Proyecto** hace lo mismo.
* **Guardar** (Ctrl+S) escribe la descripción abierta. Si carga otra o cierra el proyecto con cambios sin guardar,
  RockFace pregunta antes.
* **Guardar como…** (Ctrl+Shift+S) escribe una copia con otro nombre (**Nombre de la copia**). El nombre de una
  descripción guardada no se puede cambiar: use Guardar como y elimine la antigua.
* **Eliminar** borra la descripción abierta, con sus partes y su conteo de puntos, tras una confirmación. No se puede
  deshacer. Cuando era la última descripción de una lámina, la lámina se va también, salvo que tenga imágenes del
  Atlas o análisis puntuales, o que su muestra tenga análisis o solicitudes: esos nunca se descartan. El pozo siempre
  queda.
* **Inicio → Formulario → Limpiar** vacía la pestaña mostrada, para empezarla de nuevo.

### Plantillas

Una plantilla es una descripción guardada como punto de partida: una lista habitual de constituyentes, el petrógrafo
y la institución, un conjunto estándar de usos.

1. Abra una descripción que sea un buen comienzo y use **Guardar como…**.
2. Marque **Marcar la copia como plantilla**.
3. Las plantillas aparecen con la etiqueta *plantilla* en el panel y quedan fuera del recuento de descripciones y de
   las consultas de Explorer; una exportación solo las incluye cuando se pide.
4. Para usar una: cárguela, **Guardar como…** con el nombre de la nueva muestra (sin la marca) y cambie lo que sea
   distinto.

## Opciones

| Campo | Qué cambia |
|---|---|
| Lámina delgada (Nueva descripción) | Lámina nueva, o una lámina ya en el proyecto: varias descripciones de una lámina comparten sus imágenes, el sistema de coordenadas del conteo y los análisis. |
| Marcar la copia como plantilla | La copia es una plantilla: queda aparte de la colección. |

## Cómo funciona

El modelo de datos sigue a la roca: cuenca → campo → pozo (o afloramiento) → testigo → muestra → lámina →
descripción, con las imágenes, análisis, volúmenes y perfiles ligados a la muestra o a la lámina. Todo cambio queda
escrito en la tabla de auditoría del proyecto (quién, cuándo, qué). Una descripción se guarda como una transacción: la
identificación y todas sus partes, o nada.

## Desde un script

```python
import rockface.api as rf
with rf.create("estudio.rockface") as prj:                 # un proyecto nuevo, vacío
    d = prj.new("TS-9", well_name="ILLUSTRATIVE W-1", top_depth=2501.3, thin_section_no="9")
    prj.copy("TS-9", "TS-9 plantilla", template=True)      # una plantilla
    print([x.name for x in prj], len(prj.descriptions(templates=True)))
with rf.open("estudio.rockface") as prj:
    prj.delete("TS-9")
```

## Límites y problemas comunes

* "Ya existe una descripción llamada … en este proyecto": los nombres son únicos en un proyecto.
* "El nombre de una descripción guardada no se puede cambiar; use Guardar como."
* "No guardado: …" en la barra de estado nombra el campo a corregir; se muestra la pestaña con el error.
* En un servidor, las descripciones escritas por otra persona se abren solo para lectura para un petrógrafo (página
  [Trabajar en equipo en un servidor](server.md)).

## Cobertura

P1 (ventana principal), P2 (Nueva, Cargar, Guardar, Guardar como, plantillas, Eliminar), P6 (lámina elegida para una
descripción), P9 (Cargar descripción).
