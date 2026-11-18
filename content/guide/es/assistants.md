# ChatGPT y Gemini en RockFace

## Para qué sirve

El panel del asistente de IA de RockFace conversa con **Claude** (Anthropic), **ChatGPT** (OpenAI) o **Gemini**
(Google), según elija. Los tres usan las mismas herramientas de RockFace y siguen las mismas reglas que Claude (vea
[Claude en RockFace](claude.md)): leen las muestras del proyecto, encuentran las páginas de esta guía, miran las
imágenes de la lámina y la ventana, abren una descripción y una pestaña y proponen campos de la descripción
microscópica y del sistema poroso — siempre **sin marcar**, para que usted decida.

Las apps de escritorio también trabajan en RockFace, mediante el servidor MCP de RockFace: **Claude Desktop**, la
**app de escritorio de ChatGPT** (y Codex, que comparte su configuración) y **Google Antigravity**, en el escritorio y
en la línea de comandos, donde trabaja Gemini.

## Antes de empezar

* **Para el panel**, la clave de la API de la empresa cuyo asistente usa. Las claves de la API se pagan por uso y no
  forman parte de la suscripción a las apps de ChatGPT o de Gemini:
  * ChatGPT — OpenAI Platform, platform.openai.com → API keys (o la variable `OPENAI_API_KEY`);
  * Gemini — Google AI Studio, aistudio.google.com → Get API key (o `GEMINI_API_KEY`, o `GOOGLE_API_KEY`);
  * Claude — Claude Console (o `ANTHROPIC_API_KEY`).
  Cada clave queda en un archivo de su carpeta de usuario que solo usted puede leer, nunca en un proyecto.
* **Para una app de escritorio**, la app instalada y con su cuenta: ahí no hace falta clave de la API.
* **Sus datos.** Lo que un asistente lee — la pregunta, las respuestas de las herramientas, las imágenes que mira — va
  a su empresa. Datos públicos, bien; **datos privados, no los use**: use Mio, que funciona en este equipo. RockFace
  pregunta antes de la primera conversación con cada asistente, y de nuevo en cada sesión en un proyecto marcado como
  confidencial.

## Paso a paso

### Elegir el asistente del panel

1. Haga clic en **Asistente de IA** (Inicio → Herramientas, o `Ctrl+Alt+K`).
2. En el panel, elija **Claude**, **ChatGPT** o **Gemini** y luego el modelo:
   * ChatGPT: **GPT-6.1 Sol** (predeterminado; US$ 2 / 10 por millón de tokens, entrada / salida), **GPT-6 Astra** (el
     más capaz; US$ 10 / 50), **GPT-6.1 Terra** (US$ 1 / 5), **GPT-6 Luna** (el más rápido y económico;
     US$ 0,10 / 0,50);
   * Gemini: **Gemini 4 Argon** (predeterminado; US$ 2 / 10 hasta el 30 de noviembre de 2026, luego US$ 4 / 20),
     **Gemini 3.8 Flash** (más rápido y económico; US$ 0,75 / 3,75, precio de lanzamiento), **Gemini 3.1 Pro
     (preview)** (US$ 2 / 12).
   Cada asistente guarda su modelo; cambiar de asistente empieza una conversación nueva.
3. La primera vez, haga clic en el botón de **ajustes**, elija el asistente en **Claves y modelos de**, pegue la clave
   y haga clic en **Guardar**.
4. Pregunte, en su idioma, como con Claude: "Abra ILL-TS-001, mire la imagen y proponga la selección y los poros." Las
   propuestas llegan en una ventana, sin marcar; marque lo que usted ve y haga clic en **Aplicar las marcadas**.

### Dejar que una app de escritorio trabaje en RockFace

En los ajustes del panel:

* **Escribir en la app de escritorio de ChatGPT** añade RockFace a `~/.codex/config.toml`, que comparten la app de
  escritorio de ChatGPT, Codex y su extensión para editores (se guarda una copia fechada del archivo anterior). En la
  app de ChatGPT, abra Settings → MCP servers y reinicie las extensiones; RockFace aparece ahí. (También puede
  añadirlo a mano ahí: STDIO, con el comando que muestra `rockface assistant config chatgpt`.)
* **Escribir en Google Antigravity (Gemini)** añade RockFace a `~/.gemini/config/mcp_config.json`, que comparten la
  app de escritorio Antigravity y su línea de comandos (`agy`). Ejecute `/mcp` ahí para ver las herramientas de
  RockFace.
* **Instalar en Claude Desktop…** y **Escribir en la configuración de Claude Desktop**: vea
  [Claude en RockFace](claude.md).

Cada uno de estos botones también activa **Dejar que los asistentes de IA trabajen en esta ventana**, para que la app
trabaje en la ventana que tiene abierta (y en el archivo del proyecto, cuando no hay una ventana abierta, si eligió
uno).

## Cómo funciona

* **Un solo conjunto de herramientas, tres conversaciones.** Las herramientas, las reglas y la auditoría son las de
  Claude en RockFace. El panel habla con ChatGPT mediante la Responses API de OpenAI (`store: false`: OpenAI no guarda
  la conversación; el razonamiento del modelo vuelve cifrado entre turnos) y con Gemini mediante la API de Gemini
  (`generateContent` con declaraciones de funciones; cada turno del modelo vuelve como llegó, con su firma de
  razonamiento). Las imágenes van a ChatGPT en un mensaje después de las respuestas de las herramientas y a Gemini
  junto con ellas; solo las dos últimas quedan en la conversación.
* **La ventana de las propuestas** dice qué asistente las hizo ("Propuestas de Gemini"); cuando llama una app de
  escritorio, dice "un asistente de IA", porque RockFace no sabe qué app es.
* **Auditoría.** Cada llamada de herramienta se escribe en la auditoría del proyecto con su origen: `panel:` para el
  panel, `mcp:` para una app de escritorio.
* **Las versiones web de ChatGPT y de Gemini** no alcanzan un programa de su equipo; RockFace no se abre a internet.
  Use las apps de escritorio.

## Desde un script

```python
rf.assistants()                                     # los asistentes, si hay clave, los modelos y los precios
rf.assistant_ask("¿Qué facies tiene la mayor porosidad?", prj, assistant="gemini")
rf.assistant_ask("¿Cuántas muestras tienen calcita?", prj, assistant="chatgpt", model="gpt-6-luna")
rf.assistant_config("chatgpt")                      # la tabla [mcp_servers.rockface], como texto
rf.assistant_config("gemini", install=True)         # escrita en la configuración de Antigravity
```

Desde la línea de comandos: `rockface assistant list`, `rockface assistant ask proyecto.rockface "pregunta" --with
chatgpt`, `rockface assistant config chatgpt|gemini|claude`.

## Límites y problemas comunes

* "La clave de la API fue rechazada": la clave de una empresa no sirve para otra; revise que la clave en los ajustes
  esté en el asistente correcto.
* "La clave no tiene permiso para esto (crédito o modelo)": la cuenta no tiene crédito o no tiene acceso a ese modelo —
  las claves de ChatGPT y de Gemini necesitan la facturación activada para estos modelos.
* La app de ChatGPT no muestra RockFace: reinicie sus extensiones (Settings → MCP servers) o la app.
* Antigravity no muestra RockFace: revise `/mcp`; un Gemini CLI antiguo lee `~/.gemini/settings.json` (añada ahí, en
  `mcpServers`, la entrada que muestra `rockface mcp config --live`).
* Los modelos y los precios cambian a menudo; RockFace muestra los de noviembre de 2026.
* Sin internet, o con datos privados, use Mio.

## Cobertura

O10 (el pedido del propietario del 2026-11-18: ChatGPT y Gemini trabajando en RockFace como Claude).

Referencias: OpenAI, Responses API y llamada de funciones, https://platform.openai.com/docs; OpenAI, Model Context
Protocol en la app de escritorio de ChatGPT y en Codex, https://learn.chatgpt.com/docs/extend/mcp; Google, llamada de
funciones en la API de Gemini, https://ai.google.dev/gemini-api/docs; Google Antigravity, migración desde Gemini CLI,
https://antigravity.google/docs/cli/gcli-migration.
