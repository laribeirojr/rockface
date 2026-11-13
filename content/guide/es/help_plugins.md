# Ayuda, soporte, complementos y actualizaciones

## Para qué sirve

**Contenido de la ayuda** (F1) abre esta guía dentro del programa, con contenido, índice y búsqueda. **Soporte**
prepara lo que hay que enviar al pedir ayuda. **Complementos y actualizaciones** instala extensiones escritas en
Python y avisa cuando existe un RockFace más nuevo.

## Antes de empezar

Nada, para la ayuda. Para complementos: un `.zip` de complemento (una carpeta con `plugin.json` y su código) o la
dirección de un servidor de complementos.

## Paso a paso

1. **Ayuda → Contenido de la ayuda** (F1). *Contenido*: páginas y secciones; *Índice*: todos los títulos, con filtro;
   *Buscar*: palabras e Intro — las mejores secciones primero.
2. **Ayuda → Soporte…**: las versiones de RockFace, Python, las bibliotecas y los complementos, para copiar o guardar;
   escriba a la dirección de soporte que definió su equipo (preferencia `support/contact`).
3. **Ayuda → Complementos y actualizaciones…**: *Instalar desde un archivo…* muestra el nombre, el autor y el SHA-256
   del archivo antes de instalar; *Instalar desde un repositorio Git…* clona el repositorio (añada `@rama` o
   `@etiqueta` a la dirección para una versión) y muestra el commit antes de instalar; marque *Activo* para activarlo (en el próximo inicio); *Quitar*. *Servidor*: vacío
   para el catálogo de RockFace o la dirección de otro `index.json`; *Listar los complementos del servidor* y doble
   clic para instalar; *Buscar una versión más nueva de RockFace*.

## Opciones

| Campo de `plugin.json` | Significado |
|---|---|
| name, version, description, author, licence | se muestran en la lista |
| requires | la versión más antigua de RockFace con la que funciona |
| module | el archivo Python con `register(app)` |

## Cómo funciona

* La guía es el mismo Markdown del sitio, indexado cuando se arma el programa; la búsqueda ordena las secciones por
  BM25 sobre sus palabras, como Mio.
* Los complementos están en `~/.rockface/plugins`; un complemento empieza desactivado y solo se carga después de que
  el usuario lo activa; un archivo con rutas fuera de su carpeta se rechaza; un complemento que falla al inicio se
  informa, sin detener el programa.
* El índice del servidor lista el RockFace más reciente (versión, instalador, SHA-256, notas) y los complementos; una
  descarga solo se guarda si su SHA-256 coincide. RockFace nunca instala una actualización por sí mismo.

## Desde un script

```python
rf.plugins.install_zip("herramienta.zip"); rf.plugins.enable("herramienta")
rf.plugins.install_git("https://example.org/team/tool.git", "v1.0")
rf.plugins.check_update("https://example.org/rockface/index.json")
```

## Límites y problemas comunes

* Un complemento se ejecuta con sus permisos: instale solo lo que sea de confianza.
* El catálogo por defecto se publicará con los instaladores (desde la 1.0); hasta entonces use un servidor del equipo.

## Cobertura

P40 (contenido de la ayuda, soporte), P41 (gestor de complementos y actualizador); Counterledge C6.
