# Conversar con Mio

## Para qué sirve

Mio es una conversación, como con un asistente de chat: usted escribe como le escribiría a un colega — *¿cómo exporto
los pozos a LAS?*, *¿y también la trayectoria?*, *¿qué es la calcita poiquilotópica?*, *¿cuántas muestras de este
proyecto tienen pirita?* — y ella responde en pocas frases, en su idioma, y sigue el hilo de la conversación. No hace
falta aprender comandos ni palabras clave.

Responde con lo que RockFace dice de sí mismo — la guía del usuario, los manuales y el sitio web — y con el proyecto
abierto en la ventana. Cada respuesta indica las páginas de donde salió, como enlaces que abren la guía en la sección
correcta. Los números de su proyecto los calculan las herramientas de RockFace, como antes; un número de la respuesta
que no está en lo que Mio leyó aparece para verificarlo.

El modelo de lenguaje se ejecuta solo en su computadora. Se descarga una vez; después, Mio funciona sin internet y
nada de lo que pregunte sale de la computadora.

## Antes de empezar

* RockFace 1.0.0rc3 o posterior, instalado con el instalador (las dos ediciones traen llama.cpp, el motor que ejecuta
  el modelo). Desde el código Python: `pip install "rockface-suite[llm]"`.
* Para el modelo recomendado, unos 4 GB de memoria libre y 2,5 GB de disco; internet una vez, para descargarlo. No hace
  falta tarjeta gráfica.
* Un proyecto abierto, para las preguntas sobre el proyecto; las preguntas sobre el programa no lo necesitan.

## Paso a paso

### Descargar el modelo (la primera vez)

1. Abra el panel de Mio: el botón **Mio** de la barra de herramientas (en Petro, **Herramientas → Mio**) o
   **Ctrl+Alt+M**.
2. Cuando todavía no hay modelo, el panel ofrece el recomendado para esta computadora — por ejemplo *Qwen3 4B Instruct
   2507 (2,5 GB, se ejecuta en el procesador)*. Haga clic en **Descargar Qwen3 4B Instruct 2507**. Una ventana muestra
   el progreso de la descarga; **Cancelar** la detiene.
3. **Otros modelos…** abre la lista de los modelos que caben en esta computadora, un archivo GGUF que ya tenga o un
   servidor local (Ollama, LM Studio). **Ahora no** oculta la oferta hasta que el programa se abra de nuevo; Mio
   responde entonces con sus reglas y los fragmentos de la guía.
4. Cuando termina la descarga, Mio avisa que el modelo está listo. La primera respuesta lo carga (unos segundos); las
   siguientes empiezan enseguida.

### Conversar

1. Escriba en el cuadro de abajo y pulse **Enter** o **Preguntar**.
2. La respuesta aparece palabra por palabra. **Detener** la interrumpe.
3. Siga la conversación: *¿y con porosidad mayor que 10?*, *explique el segundo paso*, *¿y en portugués?*. Una
   continuación corta se completa con las preguntas anteriores antes de que Mio busque la respuesta (en una pregunta
   sobre el proyecto, la pregunta completa es la que responden las herramientas).
4. **Nueva conversación** empieza de nuevo: Mio olvida la conversación (el modelo sigue cargado).

La figura muestra una respuesta escrita por Qwen3 4B Instruct 2507 en un procesador, registrada en la evaluación
del 15/11/2026 (`tools/mio_eval`).

### Fuentes y números verificados

* Debajo de cada respuesta, **Fuentes** lista los fragmentos que la respuesta cita ([1], [2]…). Un fragmento de la
  guía abre **Ayuda → Contenido de la ayuda** (F1) en su sección; un manual abre su PDF en el sitio web.
* En una pregunta sobre el proyecto, la respuesta se escribe con el resultado de la herramienta (conteo, promedio,
  valores, resumen de una muestra, un término de la nomenclatura, las edades U-Pb). **Abrir en Explorer** muestra una
  búsqueda como consulta de Explorer.
* *Verifique estos números…* debajo de una respuesta lista los números de la respuesta que no están en los fragmentos
  ni en los resultados del proyecto que Mio recibió.
* Los scripts (*escriba un script que…*), las llamadas a conectores (*busque Folk 1980 en Crossref*) y las skills
  llamadas por su nombre (*/well-summary A*) funcionan como antes.

## Opciones

| Campo | Qué cambia |
|---|---|
| Usar el modelo de lenguaje | Apagado: Mio responde con sus reglas, y una pregunta sobre el programa recibe los mejores fragmentos de la guía |
| Modelo de lenguaje… | El modelo: uno de la lista (el recomendado marcado), un archivo GGUF o un servidor local; procesador o tarjeta gráfica |
| `llm.context` (configuración) | Cuántos tokens lee el modelo de una vez (8192 por defecto): las conversaciones largas guardan más de su inicio |
| `ROCKFACE_LLM_PATH`, `ROCKFACE_LLM_URL`, `ROCKFACE_LLM_DIR` | El modelo sin la interfaz (scripts, la terminal) |

Los modelos (licencias permisivas, cuantización Q4_K_M; el recomendado depende de la memoria, los hilos y la tarjeta
gráfica encontrados):

| Modelo | Archivo | Licencia | Para |
|---|---|---|---|
| Qwen3 4B Instruct 2507 | 2,5 GB | Apache-2.0 | la conversación (recomendado con 8 hilos o más) |
| Qwen3 1.7B | 1,3 GB | Apache-2.0 | portátiles con menos de 8 hilos (más rápido, respuestas más simples) |
| Qwen2.5 0.5B Instruct | 0,4 GB | Apache-2.0 | computadoras con poca memoria (respuestas cortas) |
| Qwen2.5 7B Instruct · Qwen3 8B | 4,7–5,0 GB | Apache-2.0 | una tarjeta gráfica |

## Cómo funciona

* **Lo que dice RockFace.** La guía (español, inglés y portugués), los siete manuales (en portugués, por ahora) y los
  textos del sitio web se cortan en unos 2000 fragmentos que acompañan al programa. Para cada mensaje, los fragmentos
  que mejor lo responden se encuentran por estadística de palabras (BM25, sin acentos ni plurales; siglas como LAS
  conservadas), primero en el idioma del mensaje. Cuatro de ellos van con el mensaje, numerados.
* **Lo que dice el proyecto.** Las preguntas sobre el proyecto las responden las herramientas de Mio (búsqueda, conteo,
  estadística, valores, resumen, faltantes, nomenclatura, edades), las mismas de las versiones anteriores; el resultado
  va con el mensaje.
* **La respuesta.** El modelo recibe quién es Mio y la instrucción de tomar los hechos sobre el programa solo de los
  fragmentos, y los números del proyecto solo de los resultados, citando los fragmentos que usa. La conversación va con
  cada mensaje; cuando ya no cabe, los turnos más antiguos se acortan primero.
* **Verificado.** Cada número de la respuesta se busca en lo que el modelo recibió; los demás se listan para verificar.
  Una pregunta que responden las herramientas del proyecto va al modelo solo con su resultado, y una respuesta cuyos
  números no coinciden con ese resultado se reemplaza por la frase de la propia herramienta (con un aviso).
* **Medido.** Un conjunto de evaluación de 150 preguntas escritas como las hacen los usuarios (70 en portugués, 40 en
  inglés, 40 en español, una o más sobre cada página de la guía), más preguntas sobre el proyecto, conversación y
  continuaciones (`tools/mio_eval`): los fragmentos de una página esperada están entre los cuatro dados al modelo en
  9 de cada 10 preguntas. Las respuestas del modelo real las mide el flujo "Mio evaluation" del repositorio de
  descargas: con Qwen3 4B Instruct 2507 en un procesador, todas las respuestas llegaron en el idioma de la pregunta,
  136 de las 150 respuestas sobre el programa citaron un fragmento de la página que responde y las 10 preguntas sobre
  el proyecto dieron los números de las herramientas (15/11/2026).
* **Privacidad.** El modelo se ejecuta en RockFace (llama.cpp) o en un servidor de esta computadora; un servidor en
  otra computadora se rechaza, salvo que usted lo permita explícitamente.

## Desde un script

```python
import rockface.api as rf

c = rf.chat(lang="es", model=True)                  # el modelo de la configuración; model=None: reglas y fragmentos
r = c.ask("¿Cómo exporto los pozos a LAS?", on_token=print)
print(r.text, r.cited, [s["title"] for s in r.sources])
r = c.ask("¿Y también la trayectoria?")             # la conversación sigue
prj = rf.open("proyecto.rockface")
print(prj.chat(model=True).ask("¿Cuántas muestras tienen pirita?").text)
print(rf.docs_search("porosidad de micro-CT", "es", n=3))
```

En una terminal: `rockface llm chat` (una conversación; `--project archivo.rockface` para las preguntas del proyecto,
`/new` empieza de nuevo) o `rockface llm chat --no-model --lang es cómo instalo un complemento?` para una respuesta.

## Límites y problemas comunes

* "Esta instalación no puede ejecutar un modelo de lenguaje por sí misma": una instalación anterior a 1.0.0rc3 —
  instale la actual o elija un servidor local en **Modelo de lenguaje…**.
* Respuestas lentas: en el procesador, las primeras palabras tardan de unos segundos a unos treinta segundos, según la
  computadora y el largo de los fragmentos; elija **Qwen3 1.7B** en **Modelo de lenguaje…** para respuestas más
  rápidas, o una tarjeta gráfica.
* La descarga falla detrás de un proxy: la descarga usa la configuración de proxy del sistema; descargue el archivo
  GGUF con el navegador y elíjalo en **Modelo de lenguaje… → Un archivo GGUF en esta computadora**.
* Una respuesta sin fuentes: la guía no tiene nada sobre eso, o la pregunta es general (geología, conversación). Mio
  dice cuando la guía no responde; verifique lo que dice con la guía.
* Un modelo local es más pequeño que los asistentes de internet: puede entender mal una pregunta. Las fuentes y los
  números verificados están para comprobar la respuesta.
* Mio no modifica el proyecto: sus herramientas solo leen; las sugerencias se escriben solo cuando usted las acepta.

## Cobertura

Pedido del dueño del 15/11/2026: Mio como una conversación en lenguaje natural, como los asistentes basados en
modelos de lenguaje, respondiendo con las guías del usuario, los manuales y el sitio web; el modelo solo local,
descargado en el primer uso (ROADMAP 1.0.0rc3).
