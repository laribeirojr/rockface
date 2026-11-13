# Exportar e importar descripciones

## Para qué sirve

Un **archivo de intercambio de RockFace** (`.rfx`, XML) lleva descripciones de un proyecto a otro: para enviar un
estudio a un colega, reunir el trabajo de varios petrógrafos o guardar un archivo en un formato abierto. Guarda todo de
una descripción — identificación, partes, composición, conteo de puntos, clasificación, diagénesis — y los análisis,
solicitudes e imágenes de su muestra; opcionalmente las imágenes Atlas de su lámina.

## Antes de empezar

* Un proyecto con descripciones guardadas (para exportar), o un archivo de intercambio (para importar).
* En un servidor, importar requiere el nivel de petrógrafo o superior.

## Paso a paso

### Exportar

1. **Inicio → Informes e intercambio → Exportar…** (Ctrl+E).
2. Marque las **Descripciones** a exportar.
3. Elija:
   * **Incluir las imágenes** — las imágenes de análisis, solicitudes y puntos contados;
   * **Incluir las imágenes Atlas de las láminas** — todas las teselas de sus pirámides van al archivo (las imágenes de
     láminas enteras de varios gigabytes se llevan mejor con **Guardar proyecto como…**);
   * **Un archivo por descripción, en una carpeta**.
4. **Exportar…** y elija el archivo (o la carpeta). "N descripciones exportadas a …".

### Importar

1. **Inicio → Informes e intercambio → Importar…** (Ctrl+I).
2. **Archivos…** o **Carpeta…** (todos los `.rfx` y `.xml` que contiene).
3. La lista muestra cada **Descripción**, su **Archivo** y si está **En este proyecto** (*nueva* o *nombre ya
   usado*). Marque las que va a importar.
4. **Nombres ya presentes en el proyecto**:
   * **Importar con otro nombre: (2), (3)…**
   * **Omitirlas**
   * **Reemplazar las descripciones del proyecto** (pide confirmación).
5. **Importar**. El resultado dice qué se importó, se renombró o no se importó, y por qué.

## Opciones

| Opción | Qué cambia |
|---|---|
| Incluir las imágenes | Los adjuntos van al archivo (en base64). |
| Incluir las imágenes Atlas | Las imágenes de las láminas, con sus anotaciones, mapas y puntos. |
| Un archivo por descripción | Una carpeta de archivos en vez de un solo archivo. |
| Nombres ya presentes en el proyecto | Renombrar, omitir o reemplazar. |

## Cómo funciona

El archivo se comprueba antes de importar nada (versión del formato, códigos conocidos por este RockFace, totales del
proyecto). Pozos, muestras y láminas se reconocen por nombre y números, de modo que dos descripciones de la misma
lámina siguen juntas; los identificadores se reasignan en el nuevo proyecto; los resúmenes (totales,
clasificaciones) se recalculan. Se leen los archivos escritos por cualquier RockFace anterior. Los totales
personalizados del proyecto que exportó viajan con el archivo.

El XML de otros programas se lee mediante un mapeo (Inicio → **Importar XML con un mapeo…**, página
[Catálogo de muestras, tabla para Touchstone y XML por mapeo](catalogue_exchange.md)).

## Desde un script

```python
with rf.open("estudio.rockface") as prj:
    prj.export("para-el-lab.rfx", names=["TS-9", "TS-10"], images=True)
    prj.export_folder("archivo", names=None)               # un archivo por descripción
with rf.create("copia.rockface") as otro:
    for r in otro.import_file("para-el-lab.rfx", policy="skip"):
        print(r["name"], r["action"], r["as"], r["messages"])
print(rf.read_exchange("para-el-lab.rfx").names())         # lee sin importar
```

## Límites y problemas comunes

* "Ninguna descripción en los archivos elegidos."
* "…: no importada — …": el motivo (código desconocido, archivo escrito por un RockFace más nuevo…).
* Reemplazar no se puede deshacer.

## Cobertura

P2 (Exportar, Importar), P36 (generador de XML por lotes), P37 (importador de XML: archivos o carpetas, conflictos de
nombres).
