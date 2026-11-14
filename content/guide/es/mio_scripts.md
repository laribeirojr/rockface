# Mio escribe scripts para tareas repetitivas

## Para qué sirve

Toda tarea que usted repite — el informe de cada descripción, la tabla de clasificaciones de un pozo, el LAS de cada
pozo, las figuras de todas las muestras, un flujo del Lab sobre todas las imágenes — puede volverse un **script en
Python** que corre en segundos. No necesita escribirlo: pídalo a Mio. Ella escribe el script a partir de la
petición, ya con las muestras que usted describió, y lo abre en la ventana de scripts. Usted lo lee, lo cambia si
quiere y lo ejecuta. Nada corre solo.

## Antes de empezar

* Un proyecto abierto.
* No hace falta saber Python para usar el script que Mio escribe; para cambiarlo, la página
  [Scripts en Python](scripting.md) explica la interfaz de programación.

## Paso a paso

### Pedir un script

1. Abra el panel de Mio (botón Mio, o Ctrl+Alt+M).
2. Pida con la palabra **script** (o **automatizar**, **rutina**, **python**) y diga la tarea y las muestras:
   * `@mio escriba un script que genere el informe en Word de cada descripción con calcita`
   * `@mio script de la tabla de clasificaciones de Folk y McBride`
   * `@mio script que exporte el LAS de cada pozo`
   * `@mio automatizar la presentación powerpoint de las muestras con porosidad mayor que 15`
   * `@mio script del diagrama ternario de Dickinson`
   * `@mio script de las muestras sin porosidad`
   * `@mio script que ejecute el flujo del lab en todas las imágenes`
3. Mio responde con el nombre del script y las condiciones que leyó ("muestras: diagenetic.constituent"), y el script
   se abre en la ventana de scripts como un script nuevo llamado "Mio — …".
4. Lea el encabezado: repite la petición y dice qué cambiar. La línea `CRITERIA = [...]` contiene las muestras de la
   petición como criterios del Explorer; la lista vacía significa todas las descripciones.
5. Pulse **Ejecutar** (o F5). La salida lista cada archivo escrito. Marque **Botón** para que el script aparezca en el
   menú Scripts de la cinta y se ejecute con un clic la próxima vez.

### Cambiar un script

Los valores que suele cambiar están al comienzo del cuerpo del script: la carpeta, el formato (`FMT = 'docx'`), las
clasificaciones, las curvas del LAS, la ruta del archivo. Cámbielos y ejecute de nuevo. Guarde el script en el
proyecto para el equipo.

## Opciones

Las tareas que Mio sabe escribir (cada una ejecutada en el proyecto de ejemplo por las pruebas):

| Tarea | Palabras que la llaman | Lo que hace el script |
|---|---|---|
| Informe de cada descripción | informe | un PDF, Word, Excel o HTML por descripción, en una carpeta |
| Tabla de totales y clasificaciones | clasificación, totales, Folk, Dickinson, tabla | una fila por descripción, en CSV |
| Resultado de la consulta en hoja de cálculo | hoja, excel, csv | la tabla de un concepto del Explorer en XLSX o CSV |
| Archivo LAS de cada pozo | LAS, Petrel, curvas | un LAS 2.0 por pozo con las curvas elegidas |
| Páginas HTML | html, página | una página por descripción y un índice |
| Archivos de intercambio | xml, copia | un archivo de intercambio por descripción |
| Presentación PowerPoint | presentación, powerpoint, diapositivas | la presentación de una consulta |
| Diagrama ternario | ternario, diagrama | las muestras en un diagrama (Folk, McBride, Dickinson…) |
| Secuencia paragenética | paragenética, secuencia | la figura de cada descripción |
| Conteo por pozo o facies | contar, cuántas, resumen | cuántas muestras por pozo (o facies) |
| Valores que faltan | falta, sin, vacío | las descripciones sin un valor (la porosidad, por defecto) |
| Flujo del Lab | flujo, segmentar, imágenes | un flujo sobre todas las imágenes, tabla por muestra |
| Porosidad de los volúmenes | volumen, micro-CT, tomografía | la porosidad de cada volumen segmentado, en CSV |
| Imágenes con anotaciones | fotos, imágenes, anotaciones | las imágenes exportadas con sus anotaciones |

Formatos reconocidos en la petición: PDF, Word, Excel, HTML, CSV. Clasificaciones: Folk, McBride, Dickinson (QtFL y
QmFLt), Dunham, Embry & Klovan, Wright, Grabau, Bramkamp & Powers. Idioma del informe: "en inglés", "en español",
"en portugués".

## Cómo funciona

Mio no inventa código. Elige la receta por las palabras de la petición, llena sus parámetros (formato,
clasificación, archivo) y lee las muestras pedidas con las mismas reglas de la búsqueda en lenguaje natural — por eso
la línea `CRITERIA` dice exactamente lo que entendió. Cada receta la ejecutan las pruebas automáticas de RockFace en
el proyecto ILUSTRATIVO de ejemplo, así que el script que Mio escribe funciona. Si ninguna receta sirve, dice cuáles
sabe escribir.

Para tareas que las recetas no cubren, un asistente mayor conectado a RockFace por el [servidor MCP](mcp_server.md)
puede escribir scripts nuevos con la referencia completa de la interfaz de programación.

## Desde un script

```python
s = prj.mio_script("informe en Word de cada descripción con calcita", lang="es")
print(s.recipe, s.params, s.criteria)
print(s.code)                                   # el script, listo para ejecutar
exec(compile(s.code, "<mio>", "exec"), {"rf": rf, "project": prj})

for r in rf.script_recipes():                   # las tareas que Mio sabe escribir
    print(r["key"], r["title"], r["params"])
s = prj.mio_script("tabla", recipe="table_classifications", classifications=["folk1980", "mcbride1963"])
```

## Límites y problemas comunes

* "Aún no tengo un script para eso": la tarea no tiene receta; pida una de las tareas de la tabla o parta de un
  script parecido.
* Una petición sin la palabra script es una pregunta común: "informe de cada descripción" pregunta; "script del
  informe de cada descripción" escribe el script.
* Si la línea `CRITERIA` no contiene las muestras que quería, corríjala a mano o pida de nuevo con los términos de la
  nomenclatura ("con calcita", "del pozo ILLUSTRATIVE-1", "porosidad mayor que 15").
* Un script escribe archivos en la carpeta actual del programa; use rutas completas para otra carpeta.

## Cobertura

Etapa 0.30 del ROADMAP (pedido del propietario del 13/11/2026: Mio prepara scripts Python para tareas
repetitivas).
