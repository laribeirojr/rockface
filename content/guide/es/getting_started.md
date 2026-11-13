# Primeros pasos

## Para qué sirve

RockFace Suite describe, fotografía, consulta y mide rocas sedimentarias, de la lámina delgada a la base de datos. Son
cinco programas que abren el mismo proyecto y la misma lámina: lo que uno guarda, los otros lo leen al instante.

| Programa | Para | Se abre con |
|---|---|---|
| **RockFace Petro** | la descripción de una lámina: identificación, composición, conteo de puntos, clasificaciones, diagénesis, informes | `rockface-petro` |
| **RockFace Atlas** | imágenes de láminas enteras y fotos de detalle en su lugar en la lámina, anotaciones, mapas mineralógicos, análisis puntuales | Inicio → **Atlas** (Ctrl+Shift+A) o `rockface-atlas` |
| **RockFace Explorer** | consultas sobre una colección, el panel, grupos, figuras, presentaciones, LAS, datación, evolución paragenética | Inicio → **Explorer** (Ctrl+Shift+E) o `rockface-explorer` |
| **RockFace Lab** | análisis de imágenes de una lámina: recorte, filtros, registro, segmentación, objetos, medidas | Inicio → **Lab** (Ctrl+Shift+L) o `rockface-lab` |
| **RockFace MC** | volúmenes de micro-CT, testigos enteros y perfiles de imagen de un pozo | Inicio → **MC** (Ctrl+Shift+M) o `rockface-mc` |

## Antes de empezar

* RockFace instalado en su computadora con el instalador que le dio el equipo de RockFace (las descargas públicas empiezan con la versión 1.0). RockFace IA y el
  modelo de lenguaje local se instalan aparte (páginas [RockFace IA: instalación, dispositivo y el hub de modelos](ai_setup_hub.md) y [Mio: preguntas en lenguaje natural y el modelo de lenguaje local](mio.md)).
* Nada más: el primer proyecto puede ser el ejemplo ILUSTRATIVO.

## Paso a paso

### La página de inicio

1. Abra **RockFace Petro**. La página de inicio muestra **Nuevo proyecto**, **Abrir proyecto…**, **Conectar al
   servidor** y **Abrir el ejemplo ilustrativo**, los proyectos **Recientes** y los cinco programas de **La suite
   RockFace**.
2. Elija **Abrir el ejemplo ilustrativo** para conocer el programa. Escribe un pequeño proyecto con muestras
   inventadas (todos los nombres marcados ILLUSTRATIVE) y lo abre.
3. O arrastre un archivo `.rockface` a la ventana para abrirlo.

### La ventana

* La **cinta de opciones**, arriba, tiene cuatro pestañas:
  * **Inicio** — los grupos **Proyecto**, **Servidor**, **Descripción**, **Imágenes** (Atlas, Lab, MC), **Colección**
    (Explorer), **Informes e intercambio** y **Formulario**;
  * **Ver** — **Tema oscuro** y el **Idioma**;
  * **Herramientas** — la **Base de conocimiento** (Nomenclatura, Escalas, Referencias, Grafo de conocimiento),
    **Python** (Scripts) y **Mio**;
  * **Ayuda** — **Contenido de la ayuda** (F1), **Acerca de RockFace**, **Licencia**, **Soporte…**, **Complementos y
    actualizaciones…**, el grafo de conocimiento y los dos proyectos ILUSTRATIVOS.
* El panel **Proyecto**, a la izquierda, lista los pozos, sus láminas y las descripciones de cada lámina.
* Las **pestañas de la descripción**, en el centro: Identificación, Macroscópica, Microscópica, Composición, Conteo de
  puntos, Sistema poroso, Clasificación, Diagénesis, Análisis y Solicitudes.
* La **barra de estado**, abajo, da el resultado de cada acción; a la derecha, el número de descripciones y el nombre
  del proyecto.

### Idioma y tema

1. **Ver → Idioma**: English, Español o Português. Todas las ventanas cambian al instante, y la elección se guarda
   para la próxima vez.
2. **Ver → Tema oscuro** alterna entre el tema claro y el oscuro.

El proyecto no depende del idioma: un proyecto escrito en español se abre, y genera informes, en inglés o portugués.
Solo cambian las etiquetas; los valores guardados son los mismos códigos.

### Ayuda dentro del programa

* **Ayuda → Contenido de la ayuda** (F1) abre esta guía en el idioma de la interfaz, con **Contenido**, **Índice** y
  **Buscar**.
* **Mio**, la asistente de RockFace, responde preguntas del tipo "¿cómo hago…?" con la página de esta guía que lo
  explica (página [Mio: preguntas en lenguaje natural y el modelo de lenguaje local](mio.md)).
* **Ayuda → Soporte…** reúne las versiones de RockFace y de sus bibliotecas para enviar con una pregunta (sin nombres
  de archivos y sin contenido del proyecto).

### La colección ILUSTRATIVA

**Ayuda → Abrir la colección ILUSTRATIVA** escribe un proyecto de 48 descripciones inventadas de cuatro pozos, con
imágenes, análisis, puntos U-Pb y una tabla estratigráfica. Sirve para probar RockFace Explorer.

## Opciones

| Dónde | Qué cambia |
|---|---|
| Ver → Idioma | El idioma de la interfaz (inglés, español, portugués) de todos los programas. |
| Ver → Tema oscuro | Ventanas claras u oscuras. Los diagramas y figuras siempre se dibujan en colores de papel. |
| Ayuda → Complementos y actualizaciones… | Los complementos instalados y la búsqueda de un RockFace más nuevo (página [Ayuda, soporte, complementos y actualizaciones](help_plugins.md)). |

## Cómo funciona

Un proyecto es un archivo `.rockface` (una base SQLite) o una base en un servidor PostgreSQL compartido por un equipo
(página [Trabajar en equipo en un servidor](server.md)). Cada imagen, punto contado y análisis puntual se guarda en el sistema de coordenadas de su lámina
(milímetros), nunca solo en píxeles de la imagen; por eso los cinco programas coinciden en dónde están las cosas. Los
archivos escritos por una versión más antigua se actualizan al abrirlos; un archivo escrito por una versión más nueva
se rechaza con un mensaje.

## Desde un script

```python
import rockface.api as rf
with rf.example("demo.rockface") as prj:           # el proyecto de ejemplo ILUSTRATIVO
    print(len(prj), [d.name for d in prj])
```

En una terminal:

```
rockface example demo.rockface        # escribe el proyecto de ejemplo ILUSTRATIVO
rockface collection coll.rockface     # escribe la colección ILUSTRATIVA (48 descripciones)
rockface petro demo.rockface          # lo abre en RockFace Petro (también atlas, explorer, lab, mc)
```

## Límites y problemas comunes

* "Este proyecto fue escrito por un RockFace más nuevo": actualice RockFace para abrirlo.
* "… no es un proyecto RockFace": el archivo no es una base de RockFace (o está dañado).
* Las preferencias (idioma, tema, proyectos recientes) son de su usuario en esta computadora, no del proyecto.

## Cobertura

P1 (ventana principal), P3 (barra de estado), P10 (interfaz en inglés, portugués y español), P40 (contenido de la
ayuda), O1 (scripts).
