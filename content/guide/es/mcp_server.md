# RockFace como servidor MCP para otros asistentes de IA

## Para qué sirve

Además de llamar a servicios externos, RockFace puede ser llamado por ellos. El comando `rockface mcp serve` abre un
proyecto como **servidor MCP** (Model Context Protocol): un asistente de IA que habla MCP — Claude Desktop, un editor
de código, un agente corporativo — puede consultar las muestras, leer tablas, encontrar páginas de la guía y escribir
scripts para RockFace, conversando en lenguaje natural con el usuario. Es el camino para tareas mayores que las
recetas de Mio: el asistente lee la referencia de la interfaz de programación y escribe el script, que usted ejecuta
en RockFace.

## Antes de empezar

* RockFace instalado en el equipo y un proyecto.
* Un asistente que acepte servidores MCP. Usted es responsable de lo que el asistente envía fuera: si corre en la
  nube, las respuestas de RockFace llegan a su servicio. Para un proyecto confidencial use un asistente local, o no
  use este recurso.

## Paso a paso

### Conectar RockFace al asistente

1. Genere la configuración: `rockface mcp config proyecto.rockface`. Sale una entrada JSON `mcpServers` con el
   comando que inicia el servidor.
2. Pegue esa entrada en el archivo de configuración MCP del asistente (en Claude Desktop, el archivo de configuración
   de las herramientas de desarrollador) y reinicie el asistente.
3. Pregunte al asistente, por ejemplo:
   * "En RockFace, ¿cuántas muestras tienen calcita y en qué pozos?"
   * "Muestre la tabla de petrofísica de las muestras con porosidad mayor que 15 %."
   * "¿Cómo hago el conteo de puntos con platina motorizada en RockFace?"
   * "Escriba un script de RockFace que, para cada pozo, exporte el LAS y una tabla de clasificaciones de Folk."

### Dejar que el asistente ejecute scripts

Con `rockface mcp config proyecto.rockface --allow-scripts` el servidor ofrece también `run_script`: el asistente
ejecuta scripts en el proyecto y ve su salida. Úselo solo en un proyecto de trabajo, con copia de seguridad, y con un
asistente de confianza.

### Servir por HTTP

`rockface mcp serve proyecto.rockface --http 8765` sirve lo mismo por HTTP (Streamable HTTP) en `127.0.0.1:8765`,
solo en este equipo.

## Opciones

| Herramienta del servidor | Lo que da al asistente |
|---|---|
| `ask` | la respuesta de Mio a una pregunta (conteos, listas, estadísticas, valores, faltantes, una descripción) |
| `search` | las descripciones de una pregunta y las condiciones leídas |
| `describe` | una descripción en palabras |
| `table` | un concepto en tabla (identificación, composición, petrofísica, totales, clasificaciones…), opcionalmente solo de las descripciones de una pregunta |
| `guide` | las páginas de esta guía que responden a una pregunta |
| `write_script` | un script escrito por las recetas de Mio (devuelto, no ejecutado) |
| `api` | la referencia de la interfaz de programación (`rf`) |
| `run_script` | solo con `--allow-scripts`: ejecuta un script en el proyecto |

Recursos: `rockface://api` (la referencia) y `rockface://guide/<página>` (las páginas de la guía). Opciones del
comando: `--lang es|pt|en` (idioma de las respuestas), `--allow-scripts`, `--http PUERTO`.

## Cómo funciona

El servidor usa el SDK oficial de MCP en Python (licencia MIT). Cada llamada del asistente deja una fila en la
auditoría del proyecto (`mcp`) con la herramienta y el texto pedido. Las herramientas, salvo `run_script`, solo leen
el proyecto. Las respuestas vienen de la base de datos y de las recetas probadas; el asistente puede reformularlas,
pero los números son los de RockFace.

## Desde un script

```python
cfg = rf.mcp_config("proyecto.rockface")         # la entrada mcpServers
print(cfg)
print(rf.api_reference()[:2000])                 # lo que devuelve la herramienta api
```

## Límites y problemas comunes

* El asistente no ve RockFace: revise la ruta del proyecto en la entrada `mcpServers` y reinicie el asistente.
* Respuestas en otro idioma: inicie con `--lang es`.
* No aparece `run_script`: falta `--allow-scripts`.
* El proyecto está abierto en RockFace al mismo tiempo: las lecturas funcionan; las escrituras de `run_script` y del
  programa pueden cruzarse — cierre uno de ellos para escribir.

## Cobertura

Etapa 0.30 del ROADMAP (las herramientas de Mio ofrecidas también como servidor MCP).
