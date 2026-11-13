# Scripts en Python

## Para qué sirve

Todos los programas de RockFace se pueden manejar con scripts en Python mediante una API pública, `rockface.api`:
para completar muchas descripciones a la vez, generar las tablas y figuras de un estudio, revisar una colección entera
o automatizar cualquier tarea de Atlas, Explorer, Lab y MC. Los scripts se guardan en el proyecto, pueden ser botones
de la cinta de opciones y se ejecutan también sin la interfaz, desde una terminal o un cuaderno Jupyter.

## Antes de empezar

* Un proyecto abierto, para guardar scripts en él ("Abra un proyecto para guardar scripts en él.").
* Python básico. El botón **API…** y el `docs/SCRIPTING.md` del código fuente listan todas las llamadas.

## Paso a paso

### La ventana de scripts

1. **Herramientas → Python → Scripts** (Ctrl+Shift+P). Se abre la ventana **Scripts de Python**.
2. **Scripts del proyecto** a la izquierda: **Nuevo**, **Eliminar**, **Importar .py…**, **Exportar .py…**.
3. Dé al script un **Nombre**. Marque **Botón** para listarlo bajo la flecha del botón **Scripts** de la cinta de
   opciones.
4. Escriba el script en el editor (números de línea, resaltado de Python). En un script:
   * `rf` — la API; `project` — el proyecto abierto; `current` — la descripción abierta en la interfaz;
   * `ui.message(texto)` escribe en la barra de estado; `ui.open(nombre)` abre una descripción cuando termina el
     script.
5. **Ejecutar** (F5 o Ctrl+Shift+J) ejecuta todo el script; **Ejecutar selección** (Ctrl+J) ejecuta las líneas
   seleccionadas o la línea actual.
6. **Salida** muestra lo que imprime el script y sus errores, con la línea del error marcada en el editor ("El script
   se detuvo con un error en la línea …").
7. La **consola** bajo la salida evalúa una línea en el mismo espacio de nombres de la última ejecución — Enter la
   ejecuta.
8. **Guardar en el proyecto** (Ctrl+S).

Si la descripción abierta tiene cambios sin guardar, RockFace pregunta si guardarla antes de la ejecución, y la
recarga después.

### Un primer script

```python
for d in project:
    t = d.totals()
    print(d.name, round(t["porosity"], 1), d.classify("folk1980", label=True))
rows = project.table(totals=["volume", "qt", "feldspar", "igv"], classifications=["folk1980"])
project.to_csv("resumen.csv", rows)
ui.message(f"{len(rows)} descripciones escritas")
```

### Sin la interfaz

```
rockface script mi_script.py --project estudio.rockface -- arg1 arg2
```

En Jupyter o en cualquier programa de Python:

```python
import rockface.api as rf
with rf.open("estudio.rockface") as prj:
    print(len(prj))
```

`rockface notebook estudio.rockface` escribe un cuaderno que abre el proyecto (página [MC → Más: copas, mapa de distancias, vigilancia de carpeta, reconstrucción, cambio de escala y flujo bifásico](mc_more_tools.md)).

### Los scripts de ejemplo

El proyecto de ejemplo ILUSTRATIVO trae los scripts de ejemplo: una tabla resumen, una figura de proveniencia, un
total personalizado, una revisión de todas las descripciones, el resumen de la diagénesis, informes por lotes, la
vista general del Atlas, figuras anotadas, mapas mineralógicos, análisis puntuales, consultas y figuras de Explorer,
datación y evolución, y los ejemplos de Lab y MC.

## Opciones

| Opción | Qué hace |
|---|---|
| Botón | Lista el script bajo el botón Scripts de la cinta de opciones (pestaña Herramientas). |
| Ejecutar selección | Ejecuta solo las líneas seleccionadas, o la línea actual. |

## Cómo funciona

* **Las mismas comprobaciones.** Un script no puede guardar lo que los formularios rechazarían: `d.save()` valida
  exactamente como los formularios y lanza `rf.ScriptError` con los mensajes, sin escribir nada.
* **Auditoría.** Lo que escribe un script queda registrado con el nombre del usuario seguido de ` [script]`.
* **Scripts escritos por otros.** Un script guardado en un proyecto y escrito por otra persona solo se ejecuta tras
  una confirmación ("Un script puede leer y modificar el proyecto y los archivos de esta computadora. ¿Ejecutarlo?").
* **Estabilidad.** `rf.API_VERSION` sigue el versionado semántico: dentro de la 1.x los nombres solo se añaden.
* **Licencia.** Los scripts que usan la API son obra del propio usuario: escribirlos, ejecutarlos y compartirlos está
  permitido.

## Desde un script

Esta página trata de los scripts; la sección "Desde un script" de cada otra página de esta guía muestra las llamadas
de esa función.

## Límites y problemas comunes

* "El script se detuvo con un error en la línea …": el traceback en la salida muestra solo las líneas del propio
  script.
* Un script se ejecuta con sus derechos en la computadora: ejecute solo scripts en los que confíe.
* Un script largo bloquea la ventana mientras se ejecuta; para cálculos largos de MC use trabajos (página [Trabajos: cómputo por lotes y remoto](jobs.md)).

## Cobertura

O1 (scripts en Python en todas las aplicaciones de RockFace).
