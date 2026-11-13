# Nomenclatura, escalas y referencias (la base de conocimiento)

## Para qué sirve

Todas las listas de RockFace — constituyentes, hábitos, ubicaciones, modificadores, relaciones paragenéticas,
estructuras, contactos, tipos de poro — vienen de su **base de conocimiento**: 257 términos incorporados en inglés,
español y portugués, cada uno con su fuente publicada. El editor de la base de conocimiento los muestra y permite que
un proyecto añada sus propios términos, oculte los que no usa y ponga las listas en el orden que prefiera. Muestra
también las **escalas** numéricas (granulometría, selección, redondez, tamaño de cristal, tamaño de poro) y las
**referencias** citadas.

## Antes de empezar

* Un proyecto abierto, para cambiar algo. Sin proyecto, la nomenclatura incorporada se muestra solo para lectura.
* En un servidor, cambiar la base de conocimiento requiere el nivel de gerente.

## Paso a paso

### Consultar un término

1. **Herramientas → Base de conocimiento → Nomenclatura** (Ctrl+K).
2. Elija la **Categoría** (constituyente, grupo, hábito, ubicación, modificador, relación, estructura, contacto…).
3. Escriba en **Filtrar (cualquier idioma)…**: "cuarzo", "quartzo" y "quartz" encuentran el mismo término; se ignoran
   los acentos.
4. Seleccione un término para ver su código, sus etiquetas en los tres idiomas, su grupo, tipo, familia de roca, a qué
   se aplica, y sus **Fuentes**.

### Añadir un término del proyecto

1. Elija la categoría y luego **Añadir término…**.
2. Complete el **Código** (minúsculas, letras, dígitos y `_`; nunca cambia después), las etiquetas en **Inglés**
   (obligatoria), **Español** y **Portugués** (un aviso si faltan) y, según la categoría, **Grupo** y **Familia de
   roca** (constituyentes), **Tipo** (grupos), **Se aplica a** (ubicaciones y modificadores) y **Relación inversa**
   (relaciones).
3. En **Fuentes**, dé la referencia completa de la fuente (autor, año, título, publicación). Todo término incorporado
   lleva su fuente de la literatura; un término del proyecto sin fuente se guarda con un aviso.
4. **Aplicar** y luego **Guardar en el proyecto**.

### Ocultar, ordenar, deshacer

* **Ocultar** saca un término incorporado de las listas de este proyecto (las descripciones que lo usan lo
  conservan). Marque **Mostrar términos ocultos** para verlos, y **Mostrar** para traer uno de vuelta.
* **Subir** y **Bajar** cambian el orden en que aparecen los términos en las listas de los formularios.
* **Quitar** borra un término del proyecto (los términos incorporados solo se pueden ocultar).
* **Deshacer** cancela el último cambio; **Restaurar valores** devuelve el orden incorporado y todos los términos
  ocultos (los términos propios del proyecto se conservan).
* **Guardar en el proyecto** escribe los cambios, con una línea en la auditoría; **Cerrar** pregunta antes si algo no
  se guardó.

### Escalas

1. **Herramientas → Base de conocimiento → Escalas**.
2. Elija la **Escala**: granulometría (Udden–Wentworth, con el φ de Krumbein), selección (σI de Folk y Ward),
   redondez (Powers), tamaño de cristal (Folk 1962) o tamaño de poro. La tabla da cada clase con **Desde**, **Hasta
   (exclusive)** y φ.
3. **Comprobar un valor con una clase**: escriba un **Valor**, elija una **Clase**; RockFace responde "Coherente" o
   "Incoherente: … es …, no …". Los formularios de la descripción usan la misma comprobación (página
   [Descripción macroscópica y microscópica](macro_micro_description.md)).

### Referencias

**Herramientas → Base de conocimiento → Referencias** lista cada referencia con su **Clave**, la **Referencia**
completa y **Citada por** (cuántos términos, reglas, totales y clasificaciones la citan).

## Opciones

| Campo | Qué es |
|---|---|
| Código | El valor guardado en el proyecto; nunca se traduce, nunca cambia. |
| Grupo, Tipo | Dónde va el término en las listas de la composición (por ejemplo, carbonato diagenético). |
| Familia de roca | Siliciclástica, carbonática o ambas: las listas de una descripción muestran la familia que corresponde. |
| Se aplica a | Para ubicaciones y modificadores: los tipos de constituyente que pueden describir. |
| Relación inversa | Para relaciones paragenéticas: la relación leída al revés (por ejemplo *reemplaza* ↔ *reemplazado por*). |

## Cómo funciona

La nomenclatura incorporada es propia de RockFace, construida a partir de la literatura publicada; nada de ella viene
de la ontología de un programa comercial. El proyecto guarda solo sus diferencias — sus términos, los términos
ocultos y el orden —, por lo que un RockFace más nuevo, con más términos incorporados, todavía lo abre. La lista
completa, con las fuentes, está en `docs/NOMENCLATURE.md` del código fuente.

## Desde un script

```python
with rf.open("estudio.rockface") as prj:
    for t in prj.search("caolinita"):                 # cualquier idioma, sin acentos
        print(t.category, t.code, t.labels["es"], t.citations())
    print(prj.term("constituent", "kaolinite").labels)
from rockface.core import scales
print(scales.classify("grain_size", 0.3))            # 'medium_sand'
```

## Límites y problemas comunes

* "Abra un proyecto para añadir, ocultar o reordenar términos; se muestra la nomenclatura incorporada."
* Se rechaza un código ya usado, o con mayúsculas o espacios; también un constituyente sin su grupo y familia de roca.
* Ocultar un término no cambia las descripciones que ya lo usan.

## Cobertura

P39 (herramientas de la base de conocimiento: editores de atributos con y sin intervalos de coherencia, orden de los
ítems, añadir, actualizar, quitar, deshacer).
