# Importar descripciones de otro programa (XML)

## Para qué sirve

Las descripciones de láminas hechas en otro programa de petrografía pueden entrar en RockFace sin escribirlas de
nuevo, cuando ese programa graba cada descripción como un archivo XML cuyo elemento raíz es
`ThinPetrographicDescription`. RockFace lee la identificación, la grava, la arena y el lodo, la composición con sus
puntos y porcentajes y el ambiente diagenético interpretado, y lo añade todo al proyecto como descripciones de
RockFace.

## Antes de empezar

* **En el programa de origen**, exporte las descripciones como archivos XML (un archivo por descripción). El idioma
  de la exportación no importa.
* **Este archivo no:** una exportación para Touchstone (Geocosm) también es XML, pero no es una descripción.
  RockFace la reconoce y lo avisa.
* **En RockFace**, abra el proyecto que recibirá las descripciones.

## Paso a paso

1. En RockFace Petro, elija **Inicio → Informes e intercambio → Importar descripciones de otro programa (XML)…**.
2. Elija **Archivos…** (uno o más XML) o **Carpeta…** (todos los archivos de descripción de la carpeta).
3. La tabla de arriba lista las descripciones encontradas, con el número de líneas de composición y si el nombre ya
   existe en el proyecto. Desmarque las que no quiera.
4. La tabla de abajo lista los **números sin correspondencia**: cada término del otro programa tiene un número.
   Para cada fila, elija el término de RockFace correspondiente, o deje **(no importar: guardar como texto)**.
5. Deje marcado **Recordar estas correspondencias en este proyecto**, para que los próximos archivos no necesiten
   nada.
6. Elija qué hacer con un nombre que ya existe en el proyecto (renombrar, omitir, reemplazar) y pulse **Importar**.

## Opciones

| Opción | Qué hace |
|---|---|
| Recordar estas correspondencias | Los números que usted asoció quedan en el proyecto y valen para las próximas importaciones |
| Nombre ya en el proyecto | **Renombrar** añade "(2)", **Omitir** mantiene la existente, **Reemplazar** la borra e importa de nuevo |
| (no importar: guardar como texto) | La línea no se importa; va, con nombre, número y cantidad, a las notas de la composición |

## Cómo funciona

* **Los números.** Cada término del archivo tiene un nombre, en el idioma de la exportación, y un número
  que no cambia con el idioma. RockFace lleva los números a sus propios términos. Vienen listos solo los números cuyo
  significado se comprobó igual en los dos programas. Los demás se asocian una vez.
* **Nada se adivina.** Una línea cuyo término no tiene correspondencia queda como texto en las notas de la
  composición. Un atributo (localización, hábito, modificador, relación paragenética) sin correspondencia, o que el
  término de RockFace no acepta, sale de la línea y también va a las notas. Asocie el número e importe de nuevo con
  **Reemplazar**.
* **Identificación.** Descripción, lámina, testigo, caja, plug, pozo o afloramiento, profundidades de tope y base,
  campo, unidad, cuenca, país, estado, institución, petrógrafo, observación y usos van a sus campos. Lugar, proyecto,
  digitador, fechas de edición, clase de roca, soporte y el ambiente interpretado no tienen campo en RockFace: se
  graban, tal como están, en un bloque de las observaciones con el título "[Importado de XML (ThinPetrographicDescription)]".
* **Puntos y porcentajes.** Cuando la descripción fue contada, se importan los puntos y RockFace calcula los
  porcentajes. Si no, se importan los porcentajes. Los totales grabados en el archivo no se importan: RockFace calcula
  los suyos.
* RockFace guarda solo los números del otro programa y sus propios términos. No copia nombres, definiciones ni
  reglas de ese programa.

## Desde un script

```python
import rockface.api as rf

print(rf.read_tpd("D-01.xml")["lines"])
with rf.open("proyecto.rockface") as prj:
    res = prj.import_tpd(["exportaciones/"])
    print(res["unknown"])                      # números para asociar una vez
    prj.save_tpd_mapping({"constituent": {"115": "quartz_mono"}})
    prj.import_tpd(["exportaciones/"], on_conflict="replace")
```

## Límites y problemas comunes

* **Las imágenes y las coordenadas de los puntos** no están en esos archivos XML.
* **Líneas en las notas.** Asocie sus números en la tabla de abajo e importe de nuevo con **Reemplazar**.
* **Otras versiones del formato.** Los archivos leídos hasta ahora se grabaron con la versión 3.3.0 del
  formato. Otras versiones se leen del mismo modo. Por favor, informe por el formulario de opinión un archivo que no
  se lea.
* **El otro sentido** — archivos grabados por RockFace para el otro programa y para Touchstone — vendrá en una versión
  posterior, cuando estén los archivos necesarios para comprobarlo.

## Cobertura

P37 (importador de XML; los archivos del propio programa de origen leídos desde la 0.32).
