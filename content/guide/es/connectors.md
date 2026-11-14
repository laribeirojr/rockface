# Conectores de Mio: Google, Microsoft 365, referencias, datos geológicos y tareas

## Para qué sirve

Los **conectores** llevan el trabajo de RockFace a los servicios que el equipo ya usa y traen de ellos lo que ayuda a
la descripción. Con ellos Mio puede:

* enviar la tabla de las muestras de una consulta a una **hoja de cálculo** de Google Sheets o de Excel;
* escribir un **documento** (Google Docs, Word) o armar una **presentación** con el resultado;
* preparar un **correo** (Gmail, Outlook) para la dirección que usted dé, o poner un **evento** en el calendario;
* crear una **tarea** o una tarjeta (Trello, Jira, Google Tasks, Planner);
* encontrar una **referencia** y su DOI en Crossref o en su biblioteca Zotero;
* traer los datos de un **mineral** de Mindat y de una **unidad estratigráfica** de Macrostrat;
* abrir un informe de problema (**issue**) en GitHub.

Los conectores de Google, Microsoft 365, Trello y Jira usan el **Model Context Protocol (MCP)**, el estándar abierto
con el que los asistentes de IA hablan con servicios externos. Crossref, Zotero, Mindat, Macrostrat y GitHub se llaman
directamente desde RockFace.

## Antes de empezar

* Un proyecto abierto.
* Para Google, Microsoft 365 y Jira: el servidor MCP correspondiente instalado en el equipo. Estos servidores no son
  parte de RockFace; el catálogo solo sabe cómo iniciarlos. El de Google necesita `uv` (el comando `uvx`) y una
  credencial OAuth "Aplicación de escritorio" creada en Google Cloud; el de Microsoft 365 necesita `Node.js` (el
  comando `npx`) e inicia la sesión de la cuenta la primera vez.
* Para Mindat, Zotero y GitHub: la clave de API o el token de su cuenta. Crossref y Macrostrat son abiertos.
* Para los servidores remotos (el servidor de Drive del propio Google, el de GitHub, Trello): el token de la cuenta.

## Paso a paso

### Activar un conector en el proyecto

1. En el panel de Mio pulse **Conectores** (o, en Petro, en la pestaña Ayuda, **Conectores…**).
2. La tabla muestra cada conector: grupo, tipo (integrado o MCP, con cómo se inicia), lo que hace y, entre
   corchetes, las claves que aún faltan en este equipo.
3. Marque **Activo en este proyecto** en la fila del conector. Todos empiezan apagados; activar vale solo para este
   proyecto.
4. Seleccione la fila y pulse **Claves y tokens…** para dar las claves (guardadas solo en este equipo) y los ajustes
   del conector (el id de usuario de Zotero, el repositorio de GitHub, el correo de contacto de Crossref).
5. Pulse **Probar**: RockFace inicia el servidor y lista sus herramientas, sin enviar datos del proyecto.

### Pedir a Mio

Escriba en el panel de Mio, como en una conversación. Ejemplos:

* `@mio busque la referencia Folk 1980 petrology en crossref`
* `@mio datos del mineral dolomita en mindat` — Mio traduce el nombre por la nomenclatura (Dolomite)
* `@mio unidad estratigráfica Barreirinhas en macrostrat`
* `@mio envíe las muestras con calcita a una hoja de Google`
* `@mio cree un documento en Word con las muestras del pozo ILLUSTRATIVE-1`
* `@mio agende en el calendario la revisión de las láminas del pozo ILLUSTRATIVE-2`
* `@mio cree una tarea en Trello: recontar la lámina TS-002`
* `@mio abra una issue en github: la exportación LAS omite muestras sin profundidad`

Mio hace la parte de RockFace (las muestras pedidas, la tabla, el texto), elige el conector activo y la herramienta
del servicio que sirve, y **prepara** la llamada. Una ventana muestra el conector, la herramienta, los argumentos y si
salen datos del proyecto del equipo. Solo **Confirmar y ejecutar** envía; **Cancelar** no envía nada. El resultado
aparece en el panel (en Crossref, ya como lista de referencias).

### Proyecto confidencial

Marque **Proyecto confidencial** en el diálogo de los conectores. En ese proyecto toda llamada que lleve datos del
proyecto fuera pide una segunda confirmación, con aviso; las consultas que solo llevan las palabras escritas (una
referencia, un mineral) siguen la regla normal.

### Un servidor MCP de su elección

**Añadir un servidor MCP…** pide un nombre corto y un comando (`uvx mi-servidor`, `python servidor.py`) o una
dirección (`https://…`). El servidor entra apagado en la tabla y funciona como los del catálogo.

## Opciones

| Conector | Grupo | Cómo funciona | Necesita |
|---|---|---|---|
| Google Workspace | google | servidor MCP de la comunidad en el equipo (`uvx workspace-mcp --tool-tier core`): Sheets, Docs, Slides, Drive, Calendar, Gmail, Tasks | `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET` y su cuenta `USER_GOOGLE_EMAIL` |
| Google Drive (servidor de Google) | google | servidor remoto del propio Google (Developer Preview) | `TOKEN` |
| Microsoft 365 | microsoft | servidor de la comunidad (`npx -y @softeria/ms-365-mcp-server`): Outlook, Calendario, OneDrive, Excel, Word, To Do, OneNote, Teams, SharePoint | el inicio de sesión de Microsoft la primera vez |
| Microsoft 365 (CLI) | microsoft | la CLI for Microsoft 365 de la comunidad PnP: SharePoint, Teams, Planner, OneDrive | el inicio de sesión |
| Crossref | references | directo, abierto | opcional: `mailto` |
| Zotero | references | directo | `API_KEY` y el ajuste `user_id` |
| Mindat | geodata | directo | `API_KEY` (gratuita) |
| Macrostrat | geodata | directo, abierto | — |
| GitHub | dev | directo (issues) | `TOKEN` y, si quiere, el ajuste `repo` |
| GitHub (servidor de GitHub) | dev | servidor remoto de GitHub | `TOKEN` |
| Trello | dev | servidor remoto de Atlassian | `TOKEN` |
| Jira y Confluence | dev | servidor de la comunidad (`uvx mcp-atlassian`) | `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN` |

Las claves también pueden venir de variables de entorno `ROCKFACE_<CONECTOR>_<NOMBRE>` (por ejemplo
`ROCKFACE_GITHUB_TOKEN`), que prevalecen sobre el archivo.

## Cómo funciona

* **Apagados por defecto.** La lista de conectores activos se guarda en el proyecto; las claves, solo en el equipo,
  en `~/.rockface/connectors.json` (permisos 600), nunca en el proyecto ni en la auditoría.
* **Se muestra antes de ejecutar.** Toda llamada se prepara primero; nada sale sin su confirmación.
* **Auditoría.** Toda llamada — hecha, rechazada, cancelada o fallida — deja una fila en la auditoría del proyecto
  (`connector`), con la herramienta y un resumen criptográfico de los argumentos; el diálogo muestra las últimas.
* **La herramienta correcta.** Los servidores MCP dicen qué herramientas tienen. Para enviar una tabla, Mio busca la
  herramienta cuyo nombre y descripción hablan de hoja de cálculo y de crear, y pone la tabla en el parámetro de datos
  (`values`, `rows`, `data`…). Nunca propone una herramienta que borre. Usted ve la herramienta elegida antes de
  confirmar.
* **Lo que lleva la herramienta (0.31).** Entre las herramientas que sirven, Mio prefiere la que lleva el contenido:
  una hoja importada de CSV en lugar de una hoja vacía, un documento importado de Markdown (con título y tabla) en
  lugar de texto corrido. Las herramientas como `manage_event` y `manage_task` reciben la acción `create`; la lista
  de tareas por defecto es `@default`. La fecha y la hora de un evento vienen de la frase (*mañana a las 10*, *el
  02/12 a las 14h*, *tomorrow at 3pm*), con una hora de duración. Un correo solo se prepara con la dirección escrita
  en el pedido.
* **Su cuenta.** Los servidores que piden la cuenta en cada llamada (el de Google pide `user_google_email`) la reciben
  del secreto `USER_GOOGLE_EMAIL` de este equipo; sin él, Mio dice lo que falta en lugar de adivinar.
* **Seguridad.** Los documentos y correos que vuelven de un servicio pueden contener instrucciones escritas por otras
  personas; Mio no las sigue: solo muestra el resultado.

## Desde un script

```python
prj.enable_connector("crossref")
r = prj.connector_call("crossref", "search_works", {"query": "Folk 1980 petrology"}, confirm=True)
for item in r.data:
    print(rf.connectors.reference_text(item))

prj.enable_connector("google")
header, rows = prj.query_table("identification", ("diagenetic", "constituent", "calcite_dia"))
call = prj.connector_plan("google", "export_table", {"title": "Muestras con calcita", "rows": [header] + rows})
print(call.preview("es"))                        # lo que va a salir
res = prj.connector_run(call, confirm=True)      # usted escribió la llamada: confirm=True
print(res.ok, res.text)
print(prj.connector_calls()[-1])                 # la fila de la auditoría
```

En la línea de comandos: `rockface connectors list proyecto.rockface`, `rockface connectors enable
proyecto.rockface crossref`, `rockface connectors secret github TOKEN`, `rockface connectors test proyecto.rockface
google`, `rockface connectors call proyecto.rockface crossref search_works '{"query": "Folk 1980"}'`.

## Límites y problemas comunes

* "El conector … está apagado": actívelo en la tabla, para este proyecto.
* "missing …": dé las claves en **Claves y tokens…**.
* La prueba no responde: el servidor no está instalado (`uvx`, `npx` no encontrados) o la cuenta no inició sesión.
* Servidores distintos nombran distinto sus herramientas; si Mio elige mal, use **Desde un script** con la
  herramienta correcta (`prj.connector_tools("google")` las lista) o pida de otra forma.
* El servidor remoto de Gmail del propio Google crea borradores, no envía: el envío es suyo. El servidor de la
  comunidad en el nivel `core` solo tiene la herramienta de **enviar**: revise el destinatario en la ventana de
  confirmación.

## Cobertura

Etapa 0.30 del ROADMAP (pedido del propietario del 13/11/2026: los conectores MCP de Mio, primero las herramientas
de Google; y, por su elección, Microsoft 365, referencias y datos geológicos, GitHub y tareas).
