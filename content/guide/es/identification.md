# Identificación de una muestra

## Para qué sirve

La pestaña **Identificación** dice de qué trata la descripción: su nombre y usos, el pozo o afloramiento, la muestra y
sus profundidades, la lámina, el petrógrafo y las observaciones importantes. Todas las consultas, informes, figuras y
archivos LAS leen estos campos.

## Antes de empezar

Una descripción abierta o recién creada (página [Proyectos y descripciones](projects_descriptions.md)).

## Paso a paso

1. Abra la pestaña **Identificación** (la primera).
2. **Descripción**
   * **Nombre de la descripción** — obligatorio y único en el proyecto. Tras el primer guardado queda bloqueado (use
     **Guardar como…** para otro nombre).
   * **Uso de la descripción** — hasta tres usos (caracterización de reservorio, calidad de reservorio, diagénesis,
     proveniencia, ambiente deposicional, calibración petrofísica, geoquímica y datación, docencia, otro), sin
     repetir.
3. **Pozo o afloramiento**
   * **Nombre** — escriba uno nuevo o elija uno que ya está en el proyecto; elegir un pozo existente completa su
     cuenca, campo, país, estado y posición.
   * **Tipo** (pozo o afloramiento), **Cuenca**, **Campo**, **País**, **Estado / provincia**, **Latitud (°)**,
     **Longitud (°)**.
4. **Muestra**
   * **Tipo de muestra** (plug de testigo, testigo entero, testigo lateral, recortes de perforación, muestra de
     afloramiento, otro), **Unidad estratigráfica**, **Zona**.
   * **Profundidad del tope (m)** y **Profundidad de la base (m)**; **Profundidad corregida (m)** (corrección
     testigo–perfil) y **Profundidad ajustada (m)** (la profundidad final usada en los modelos).
   * **Testigo n.º**, **Caja n.º**, **Plug n.º**, **Lámina n.º** y **Facies** (el código o nombre del equipo).
5. **Petrógrafo** — **Nombre** e **Institución**. **Primera edición** y **Última edición** las completa RockFace.
6. **Observaciones importantes** — un resumen libre de lo que más importa en la muestra.
7. **Guardar** (Ctrl+S).

## Opciones

| Campo | Regla |
|---|---|
| Nombre de la descripción | Obligatorio; único; bloqueado tras el primer guardado. |
| Uso de la descripción | Como máximo tres, sin repetir. |
| Profundidades | 0 a 9999,99 m; la base no puede ser menos profunda que el tope. |
| Latitud, longitud | −90° a 90°; −180° a 180°. |
| Facies | Texto libre: el código o nombre que usa el equipo (el panel de Explorer agrupa por él). |

## Cómo funciona

Pozos, muestras y láminas son registros compartidos: dos descripciones de la misma lámina muestran el mismo pozo,
profundidades y números, y cambiarlos en una los cambia para las dos. Los valores guardados son códigos neutros
respecto al idioma (por ejemplo el tipo de muestra), por lo que el proyecto se lee igual en inglés, español y
portugués. El levantamiento direccional del pozo, cuando existe, da la profundidad vertical verdadera y la posición de
cada muestra (página [Trayectoria del pozo](well_trajectory.md)).

## Desde un script

```python
with rf.open("estudio.rockface") as prj:
    d = prj["TS-9"]
    print(d.identification.well_name, d.identification.top_depth)
    d.update(base_depth=2501.6, facies="F3", uses=["reservoir", "diagenesis"])   # comprobado como en el formulario y guardado
```

`d.update()` lanza `rf.ScriptError` con los mensajes cuando un valor rompe una regla, y no se escribe nada.

## Límites y problemas comunes

* "El nombre de la descripción es obligatorio." / "Ya existe una descripción llamada … en este proyecto."
* "Profundidad del tope (m) debe estar entre 0 y 9999,99 m."
* "La profundidad de la base (… m) es menor que la del tope (… m)."
* "Se pueden elegir como máximo tres usos." / "Un uso de la descripción está repetido."
* Avisos (no errores): "No se indicó pozo ni afloramiento.", "La lámina no tiene número." La descripción se guarda,
  pero las consultas por pozo o por lámina no la encontrarán.

## Cobertura

P4 (campos de la identificación), P5 (usos elegidos), P7 (observaciones importantes), P8 (posición y profundidades).
