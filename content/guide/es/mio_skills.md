# Skills de Mio

## Para qué sirve

Una **skill** es una pequeña receta que Mio ejecuta cada vez que una pregunta la pide: varias de sus herramientas,
una tras otra, con los valores tomados de la pregunta. "Resumen del pozo ILLUSTRATIVE-B" cuenta las muestras del
pozo, lista sus facies, da porosidad y permeabilidad y dice qué descripciones no tienen porosidad — en una sola
respuesta. RockFace trae ocho skills, activas desde el principio, para usar y copiar; usted escribe las suyas y las
guarda para sí o en el proyecto, para todo el equipo.

## Antes de empezar

* Un proyecto abierto. Escribir una skill no requiere programar: es un texto JSON corto editado en el diálogo
  **Skills**.

## Paso a paso

### Usar una skill

1. En el panel de Mio escriba una de sus frases ("resumen del pozo ILLUSTRATIVE-B", "huecos en los datos", "mejores
   reservorios", "cómo hago …") o su nombre tras una barra: `/well-summary ILLUSTRATIVE-B`.
2. Si la skill necesita un valor que la pregunta no dio (el pozo, una muestra), Mio lo pide.

Las skills que trae RockFace:

| Skill | Se llama con (ejemplos) | Qué hace |
|---|---|---|
| `well-summary` | resumen del pozo · well summary · resumo do poço | conteo, facies, porosidad, permeabilidad, porosidad faltante de un pozo |
| `formation-summary` | resumen de la formación · formation summary | conteo, pozos, facies, porosidad, cemento de una formación |
| `reservoir-quality` | mejores reservorios · calidad de reservorio | muestras con porosidad ≥ 15 % y permeabilidad ≥ 100 mD, y sus pozos |
| `cement-overview` | panorama de los cementos · cementación | cemento total y carbonático; muestras con calcita, dolomita, crecimientos de cuarzo |
| `dated-samples` | muestras datadas · dataciones | muestras con puntos de datación y sus pozos |
| `data-gaps` | huecos en los datos · datos faltantes · control de calidad | descripciones sin profundidad, porosidad o permeabilidad |
| `sample-report` | ficha de la muestra · sample report | los datos principales de una descripción y las sugerencias de sus mapas |
| `how-to` | cómo hago · how do I · como faço | las páginas de esta guía que explican una tarea |

### Escribir una skill

1. Panel de Mio → **Skills…**. La lista muestra todas las skills con su origen: *RockFace*, *mía* (su carpeta),
   *proyecto*.
2. Seleccione una para verla, o haga clic en **Nueva** para una plantilla.
3. Edite el JSON (campos abajo) y haga clic en **Guardar para mí** (su carpeta) o **Guardar en el proyecto** (todos
   los que abren el proyecto). La skill se verifica antes de guardar; los problemas aparecen bajo el editor.
4. **Activa** apaga una skill sin eliminarla. Una skill guardada con el nombre de otra la reemplaza (una skill del
   proyecto llamada `how-to` reemplaza la de RockFace); **Eliminar** trae la otra de vuelta.

## Opciones

```json
{
 "name": "kaolinite-by-well",
 "title": {"en": "Kaolinite by well", "pt": "Caulinita por poço", "es": "Caolinita por pozo"},
 "description": {"en": "…", "pt": "…", "es": "Cuántas muestras de un pozo tienen caolinita, y su porosidad."},
 "triggers": ["kaolinite by well", "caulinita por poço", "caolinita por pozo"],
 "inputs": {"well": {"field": "well"}},
 "steps": [
  {"tool": "count", "question": "samples of well {well} with kaolinite"},
  {"tool": "stats", "number": "petrophysics.porosity", "question": "samples of well {well} with kaolinite"}
 ],
 "active": true
}
```

| Campo | Qué es |
|---|---|
| `name` | minúsculas, dígitos y guiones; también el `/nombre` que llama la skill |
| `title`, `description` | mostrados en la lista, en inglés, portugués y español |
| `triggers` | frases que llaman la skill (los acentos y las mayúsculas no importan) |
| `inputs` | valores leídos de la pregunta: `{"field": "well"}` (cualquier campo de la identificación: pozo, formación, facies, campo, cuenca, zona…) o `{"field": "sample"}` (el nombre de una descripción); `{question}` siempre está disponible |
| `steps` | las herramientas, en orden: `search`, `count` (`question`), `stats` (`number`, `question`; 0.31: `statistic` y `group`, p. ej. `facies`), `values` (`field`, `question`), `missing` (`number`, `question`), `describe` (`sample`), `suggest` (`sample`), `guide` (`question`), `ages` (`question`, 0.31) |

`number` es `concepto.atributo` como en el Explorer: `petrophysics.porosity`, `petrophysics.permeability`,
`petrophysics.grain_density`, `identification.top_depth`, `totals.cement`, `totals.carbonate_cement`…

## Cómo funciona

Las skills son datos, nunca código: una skill solo puede llamar a las herramientas de Mio, y cada herramienta solo lee
el proyecto. Las skills vienen de tres lugares, leídos en este orden (una posterior con el mismo nombre reemplaza a la
anterior): la carpeta de RockFace `rockface/mio_skills`, su carpeta (`~/.rockface/mio/skills`, o el ajuste
`mio.skills`, o `ROCKFACE_MIO_SKILLS`) y el proyecto (guardada en el proyecto con una línea de auditoría, así un
proyecto en servidor comparte sus skills con el equipo).

## Desde un script

```python
for s in prj.mio_skills():
    print(s.name, s.source, s.triggers)
prj.save_mio_skill({"name": "barite-count", "triggers": ["barita por favor"],
                    "steps": [{"tool": "count", "question": "samples with barite"}]})
print(prj.mio(lang="es").ask("/barite-count").text)
prj.delete_mio_skill("barite-count")
```

## Límites y problemas comunes

* "La skill no se puede usar: …": la verificación lista qué corregir (una herramienta que no existe, una entrada usada
  pero no declarada, un `stats` sin número).
* Una frase que también es una pregunta común ("muestras con calcita") hace que toda pregunta así ejecute la skill —
  elija frases que digan qué es la skill.
* Las skills que escriben en el proyecto (aplicar una sugerencia, ejecutar un script) no se permiten en esta versión:
  Mio propone, el usuario decide.

## Cobertura

El asistente que llama a las herramientas del programa de la etapa 0.27 del ROADMAP; el pedido del propietario del
13/11/2026 (skills creadas por el usuario, ejemplos activos desde el principio).
