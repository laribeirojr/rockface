# Claude en RockFace

## Para qué sirve

Claude, el asistente de IA de Anthropic, puede trabajar **junto con** RockFace, como lo hace en un procesador de
textos o una hoja de cálculo: lee las muestras del proyecto, encuentra las páginas de esta guía, mira las imágenes de
las láminas y la ventana, abre una descripción y una pestaña y propone campos de la descripción microscópica y del
sistema poroso. Llega a RockFace de tres formas, que pueden usarse juntas:

1. **El panel de Claude**, dentro de cada programa de RockFace (junto a Mio): usted conversa con Claude sin salir de
   RockFace.
2. **Claude Desktop**, con la **extensión de RockFace** (un doble clic la instala): usted conversa con Claude en su
   propia app y él trabaja en RockFace.
3. **La ventana en vivo**: sea cual sea la forma de conversar, Claude trabaja en la ventana de RockFace que está
   abierta — la descripción en la que usted está, la pestaña que ve, las imágenes de su lámina.

Las tres usan las mismas herramientas, las mismas reglas y la misma auditoría: lo que Claude hace desde Claude
Desktop es lo que hace desde el panel.

Mio sigue igual: local, gratuita y sin internet. Claude es una opción para quien quiere un modelo más fuerte y acepta
que la conversación vaya a Anthropic.

## Antes de empezar

* Para el **panel**: una **clave de la API de Claude**. Se crea en la Claude Console (platform.claude.com → API keys)
  y se paga por uso; una suscripción a las apps de Claude (Pro, Max, Team) no la incluye. Péguela en los ajustes del
  panel: queda en un archivo de su carpeta de usuario que solo usted puede leer, nunca en un proyecto. Una clave en
  la variable `ANTHROPIC_API_KEY` se usa primero.
* Para **Claude Desktop**: la app Claude Desktop, con su cuenta. No hace falta clave de la API — Claude Desktop usa su
  plan de Claude.
* **Sus datos.** Lo que Claude lee — la pregunta, las respuestas de las herramientas, las imágenes que mira — se envía
  a Anthropic. Datos públicos, bien; **datos privados, no use Claude**: use Mio, que funciona en este equipo. RockFace
  pregunta antes de la primera conversación, y de nuevo en cada sesión en un proyecto marcado como confidencial
  (*Herramientas → Conectores*).

## Paso a paso

### Conversar con Claude en RockFace (el panel)

1. Haga clic en **Claude** (Inicio → Herramientas, o `Ctrl+Alt+K`). El panel se abre a la derecha.
2. La primera vez, haga clic en el botón de **ajustes** del panel, pegue la clave de la API y haga clic en
   **Guardar**. Elija el modelo:
   * **Claude Sonnet 5.5** (predeterminado) — rápido y capaz; US$ 2 / 10 por millón de tokens (entrada / salida);
   * **Claude Opus 5.5** — el más capaz para trabajos largos; US$ 4 / 20;
   * **Claude Haiku 5.5** — el más rápido y económico; desde US$ 0,10 / 0,50;
   * **Claude Fable 5.2** — las tareas de investigación más difíciles; US$ 8 / 40.
3. Pregunte, en su idioma. Por ejemplo:
   * "¿Qué muestras del proyecto tienen cemento de calcita por encima del 10 %? Haga una tabla con su porosidad."
   * "Abra ILL-TS-001, mire la imagen y proponga la selección, la redondez y los poros."
   * "¿Cómo hago un diagrama ternario del conteo de puntos?"
4. El panel muestra cada herramienta que Claude usó (líneas ⚙) y su respuesta. **Detener** termina un turno largo;
   **Nueva conversación** empieza de nuevo. Los tokens gastados aparecen debajo del modelo.

### Claude propone, usted decide

* **Propuestas.** Cuando Claude propone campos de la descripción, una ventana los lista **sin marcar**: el campo, el
  valor y las palabras que usó Claude. Marque lo que usted mismo ve, haga clic en **Aplicar las marcadas** y
  **guarde** la descripción como siempre. Nada se escribe antes.
* **Scripts.** Si activa **Dejar que Claude proponga scripts** (ajustes), Claude puede escribir un script de Python
  para una tarea; se muestra en una ventana y solo se ejecuta al hacer clic en **Ejecutar**. Una descripción con
  cambios sin guardar no se toca.
* **Navegación.** Claude puede abrir una descripción y mostrar una pestaña; no deja una descripción con cambios sin
  guardar.

### Claude Desktop trabaja en RockFace (la extensión)

1. En los ajustes del panel de Claude, haga clic en **Instalar en Claude Desktop…**. RockFace escribe
   `RockFace-Suite.mcpb` (en su carpeta de usuario, `.rockface/claude`), lo abre y activa la ventana en vivo.
2. Claude Desktop muestra la instalación: haga clic en **Install**. (O abra Claude Desktop → Settings → Extensions y
   arrastre el archivo allí.) En sus opciones puede elegir un **proyecto** — usado cuando no hay una ventana de
   RockFace abierta — y **Dejar que Claude proponga scripts**.
3. En Claude Desktop, pregunte como en el panel: "En RockFace, ¿qué está abierto ahora?", "Mire la imagen de esta
   muestra y proponga la descripción."

Si su Claude Desktop no acepta extensiones, haga clic en **Escribir en la configuración de Claude Desktop**: RockFace
se añade a `claude_desktop_config.json` (guardando una copia fechada del archivo anterior); reinicie Claude Desktop.

### La ventana en vivo

**Dejar que Claude trabaje en esta ventana** (ajustes) abre un canal solo en este equipo (127.0.0.1, un puerto al azar
y un secreto en un archivo que solo usted puede leer). Activado, Claude Desktop trabaja en la ventana que usted tiene
abierta; desactivado, trabaja en el proyecto elegido en la extensión, o en nada. Sigue activado en las próximas
sesiones hasta que lo desactive; se cierra con la ventana.

## Cómo funciona

* **Un solo conjunto de herramientas.** `search`, `table`, `ask` (Mio), `describe`, `guide`, `write_script`,
  `api_reference`, `description_fields` y, en una ventana, `window_state`, `open_description`, `show_tab`,
  `list_pictures`, `look_at` (una imagen, o la propia ventana, reducida a 1 568 píxeles), `propose_description` y,
  cuando se permite, `run_script`. En el panel, Claude las llama con la API Messages de Claude y el uso de
  herramientas; desde Claude Desktop, con el servidor MCP de RockFace (`rockface mcp serve --live`), que pasa cada
  llamada a la ventana abierta.
* **Las propuestas usan las palabras de RockFace.** `propose_description` lee líneas "Campo: valor" con el mismo
  lector del dictado y de *Mio mira*; solo las palabras del vocabulario de RockFace se vuelven propuestas, y empiezan
  sin marcar — las personas siguen consejos automáticos aun cuando están equivocados (sesgo de automatización), así
  que usted decide cada campo.
* **Imágenes.** Solo las dos últimas imágenes quedan en la conversación; las anteriores se reemplazan por una nota, lo
  que mantiene bajo el costo.
* **Auditoría.** Cada llamada de herramienta se escribe en la auditoría del proyecto, con su origen (`panel:` o
  `mcp:`).
* **Ningún paquete nuevo.** El panel habla con la API con el cliente HTTP del propio Python; la extensión es un ZIP
  hecho en su equipo, que apunta a su RockFace.

## Desde un script

```python
rf.claude_models()                                   # los modelos, con sus precios
rf.claude_ask("¿Cuántas muestras tienen calcita?", prj)  # necesita ANTHROPIC_API_KEY o la clave del panel
rf.claude_extension()                                # el archivo .mcpb para Claude Desktop
rf.claude_desktop_config(install=True)               # o escribir la configuración de Claude Desktop
rf.live_windows()                                    # las ventanas que dejan trabajar a Claude
rf.mcp_config(live=True)                             # la entrada mcpServers para otro asistente
```

Desde la línea de comandos: `rockface claude extension`, `rockface claude config`, `rockface claude ask
proyecto.rockface "pregunta"`, `rockface claude windows` y `rockface mcp serve --live`.

## Límites y problemas comunes

* "Aún no hay clave de la API": el panel necesita una clave de la Claude Console; Claude Desktop no.
* "La clave de la API fue rechazada" (401) o "La clave no tiene permiso para esto" (403, a menudo falta de crédito):
  revise la clave en la Claude Console. "Demasiadas solicitudes por ahora" (429) o "Claude está ocupado ahora" (529):
  espere un poco y pregunte de nuevo.
* Claude Desktop dice que ninguna ventana de RockFace lo deja trabajar: abra RockFace y active **Dejar que Claude
  trabaje en esta ventana**, o elija un proyecto en las opciones de la extensión.
* La extensión apunta al RockFace del equipo que la creó; tras reinstalar RockFace en otra carpeta, créela de nuevo.
* Claude es un modelo general, no un petrógrafo: compare cada propuesta con la imagen, como en *Mio mira*.
* Sin internet, use Mio.

## Cobertura

O9 (el pedido del propietario del 2026-11-18: Claude operando RockFace, como en las apps de Word, Excel y PowerPoint —
el panel, la ventana en vivo y la extensión de Claude Desktop juntos).

Referencias: Anthropic, API Messages de Claude y uso de herramientas, https://docs.claude.com; Model Context Protocol,
https://modelcontextprotocol.io; MCP Bundles (.mcpb), https://github.com/modelcontextprotocol/mcpb; Goddard, Roudsari &
Wyatt (2012), sesgo de automatización, https://doi.org/10.1136/amiajnl-2011-000089.
