# Mio: preguntas en lenguaje natural y el modelo de lenguaje local

## Para qué sirve

**Mio** es la asistente de RockFace. Usted pregunta sobre las descripciones del proyecto con sus propias palabras —
"¿qué muestras tienen barita?", "¿cuántas muestras del pozo B tienen porosidad mayor que 20 %?", "permeabilidad media
de las muestras con caolinita", "¿qué falta antes del estudio?", "¿cómo segmento una lámina con IA?" — y ella responde
desde la base de datos: las descripciones que coinciden, cuántas, mínimo, media y máximo de un número, los valores de
un campo, los datos principales de una muestra, las descripciones sin un valor, la página de esta guía que explica
una tarea. Cada respuesta muestra las condiciones que leyó, para que vea exactamente qué se preguntó a la base.

En el Explorer la misma lectura funciona como **búsqueda en lenguaje natural**: escriba la pregunta en el cuadro de
búsqueda de la barra de herramientas y la consulta aparece en la lista de criterios, lista para refinar, guardar o
exportar.

Mio funciona sin modelo de lenguaje (sus reglas entienden las palabras de la nomenclatura de RockFace en español,
inglés y portugués, números — también en palabras — y comparaciones). Un **modelo de lenguaje local** — un modelo abierto pequeño que
funciona en su computadora, en el procesador o en la tarjeta gráfica — le permite entender preguntas más libres:
otras grafías ("baryte", "caolín"), sinónimos ("romboedros de dolomita"), palabras fuera de la nomenclatura.

## Antes de empezar

* Un proyecto abierto con descripciones.
* Para el modelo de lenguaje: RockFace con el extra `llm` (`pip install "rockface-suite[llm]"`, que instala
  llama-cpp-python), o un servidor local ya en marcha (Ollama, LM Studio o llama-server). No hace falta tarjeta
  gráfica.

## Paso a paso

### Preguntar a Mio

1. Haga clic en **Mio** en la barra de herramientas (en Petro: **Herramientas → Mio**) o pulse **Ctrl+Alt+M**. El
   panel de Mio se abre a la derecha.
2. Escriba la pregunta y pulse **Enter** (o **Preguntar**). El `@mio` al principio es opcional en el panel.
3. Lea la respuesta y la línea **Condiciones leídas**. **Palabras no usadas** lista las palabras que no convirtió en
   condición — reformule si alguna importaba.
4. Cuando la respuesta es una búsqueda, **Abrir en Explorer** la muestra como consulta del Explorer.

En cualquier cuadro de búsqueda que habla con Mio (el del Explorer), un texto que empieza con **@mio** va al panel.

### Búsqueda en lenguaje natural en el Explorer

1. **Explorer** → escriba en el cuadro *Buscar en lenguaje natural…* (por ejemplo *muestras con barita y porosidad
   mayor que 20 %*) y pulse **Enter**.
2. Los criterios aparecen en la lista y las descripciones encontradas debajo. Una pregunta que no es una sola
   consulta ("calcita o dolomita") selecciona las descripciones en la lista.

### Elegir el modelo de lenguaje

1. En el panel de Mio, haga clic en **Modelo de lenguaje…**.
2. El diálogo muestra esta computadora (memoria, hilos, tarjetas gráficas, si llama.cpp puede usar la tarjeta) y los
   modelos que caben en ella, con tamaño, licencia, dónde funcionaría y el **recomendado** marcado. Usted elige:
   * **El modelo seleccionado en la lista** — se descarga una vez (pregunta antes, con el tamaño y la licencia) y queda
     en `~/.rockface/llm`;
   * **Un archivo GGUF en esta computadora** — cualquier modelo en formato GGUF que ya tenga;
   * **Un servidor local** — la dirección de Ollama (`http://localhost:11434`), LM Studio o llama-server, y el nombre
     del modelo en el servidor.
3. **Ejecutar en**: procesador o tarjeta gráfica. **OK** guarda la elección; el modelo se carga con la primera
   pregunta.
4. **Usar el modelo de lenguaje** (panel) lo enciende y apaga; **Respuestas fluidas** deja que el modelo reescriba la
   respuesta (se conserva solo si sus números son exactamente los de la base).

En la línea de comandos: `rockface llm setup` (la misma elección, con el recomendado marcado), `rockface llm use
<archivo.gguf | http://localhost:11434>`, `rockface llm info` y `rockface llm ask <proyecto> "<pregunta>"`.

## Opciones

| Campo | Qué cambia |
|---|---|
| Usar el modelo de lenguaje | Apagado: las reglas responden solas. Encendido: el modelo lee las preguntas en que las reglas dejan palabras |
| Respuestas fluidas | El modelo reescribe la respuesta; una reescritura con cualquier número cambiado se descarta |
| Ejecutar en | Procesador o tarjeta gráfica (la tarjeta requiere llama.cpp compilado con CUDA, Metal o Vulkan) |
| `ROCKFACE_LLM_PATH`, `ROCKFACE_LLM_URL`, `ROCKFACE_LLM_DEVICE` | El modelo sin la interfaz (scripts, trabajos) |
| `ROCKFACE_LLM_DIR` | Dónde se guardan los modelos descargados |

Los modelos ofrecidos (todos con licencias permisivas, cuantización Q4_K_M):

| Modelo | Archivo | Licencia | Para |
|---|---|---|---|
| Qwen2.5 0.5B Instruct | 0,40 GB | Apache-2.0 | cualquier computadora |
| Qwen3 1.7B | 1,28 GB | Apache-2.0 | portátiles (recomendado con menos de 8 hilos) |
| Qwen3 4B · Phi-4 mini | 2,5 GB | Apache-2.0 · MIT | 8 hilos o más, 8 GB de memoria |
| Qwen2.5 7B Instruct · Qwen3 8B | 4,7–5,0 GB | Apache-2.0 | una tarjeta gráfica |

## Cómo funciona

* **Responde la base, nunca el modelo.** La pregunta se lee en criterios del Explorer (los mismos que usted arma a
  mano) y las descripciones las encuentra el Explorer en los registros. Al modelo solo se le pide convertir las
  palabras que las reglas no entendieron en frases del vocabulario de RockFace, con números; sus frases se verifican
  contra el vocabulario (una frase que no está en él se descarta o se cambia por la más cercana) y se leen de nuevo
  con las reglas, así que cada condición es una que el usuario ve. La respuesta restringida a un esquema JSON
  (gramática de llama.cpp) impide que el modelo escriba otra cosa.
* **Las reglas.** El vocabulario es la base de conocimiento del proyecto (constituyentes, grupos, hábitos,
  ubicaciones, modificadores en tres idiomas), los valores de la identificación (pozos, formaciones, facies…), los
  análisis (porosidad, permeabilidad, profundidad, totales) y los análisis puntuales; las palabras se comparan sin
  acentos ni plurales, con tolerancia de una letra en las palabras largas; los números se unen a la palabra numérica
  más cercana, los hábitos al constituyente más cercano.
* **Las herramientas.** `search`, `count`, `stats`, `values`, `describe`, `missing`, `suggest`, `guide` — todas solo
  leen. Las **skills** de Mio las encadenan (página *Skills de Mio*).
* **Privacidad.** El modelo funciona en la computadora; una dirección de servidor en otra computadora se rechaza salvo
  que usted la permita expresamente, porque las preguntas y los registros mostrados al modelo saldrían de la
  computadora.
* **Aceptación en un conjunto de prueba.** Un proyecto ILUSTRATIVO de 48 descripciones inventadas de contenido
  conocido y 41 preguntas en español, inglés y portugués: 41 correctas por las reglas. Quince paráfrasis más
  difíciles: 8 correctas solo con las reglas, 13 con Qwen2.5 0.5B en un procesador sin tarjeta gráfica (2 hilos;
  3–14 s, mediana de 5 s, en las preguntas que llaman al modelo) — `docs/LLM.md`.

## Desde un script

```python
a = prj.ask("muestras con barita y porosidad mayor que 20 %")      # solo las reglas
print(a.count, a.names, a.explanation, a.unknown)
q = a.query()                                                      # la consulta del Explorer, cuando es una
mio = prj.mio(model=True, lang="es")                               # con el modelo de lenguaje configurado
r = mio.ask("@mio ¿cuántas muestras del pozo ILLUSTRATIVE-B tienen caolinita?")
print(r.tool, r.text, r.data)
from rockface.api import llm
m = llm.LlamaModel("Qwen2.5-0.5B-Instruct-Q4_K_M.gguf", device="cpu")   # o llm.ServerModel("http://localhost:11434", "qwen2.5:0.5b")
print(prj.ask("muestras con baritina", model=m).names)
```

## Límites y problemas comunes

* "Sin modelo de lenguaje": elija uno en **Modelo de lenguaje…** o con `rockface llm setup`; Mio sigue respondiendo
  con sus reglas.
* Una palabra ignorada: aparece en **Palabras no usadas**; use el término de la nomenclatura o encienda el modelo.
* La primera pregunta con modelo tarda unos segundos más (el modelo se carga una vez por sesión).
* En un proyecto en servidor el panel responde en el hilo de la ventana (la ventana espera mientras el modelo lee).
* Mio no cambia el proyecto: herramientas y skills solo leen; las sugerencias se escriben solo cuando usted las acepta.

## Cobertura

L1 (búsqueda en lenguaje natural en la base de datos), el asistente que llama a las herramientas del programa y la
elección del procesador o de la tarjeta gráfica de la etapa 0.27 del ROADMAP.
