# Superficies 3D, guardar en un archivo NetCDF existente y el paquete para Geolog

## Para qué sirve

Tres herramientas de intercambio de la pestaña **Multiescala** de RockFace MC:

* **Superficies 3D**: los modelos de fotogrametría de testigos, plugs y afloramientos (Wavefront OBJ con sus
  materiales MTL y las imágenes de textura) guardados en el proyecto y mostrados en 3D, y la superficie de un segmento
  de un volumen creada y escrita como OBJ.
* **Guardar en un archivo NetCDF existente**: los volúmenes hechos en RockFace escritos como nuevas variables del
  archivo NetCDF del que vinieron los datos, que conserva todo lo que tenía (atributos, dimensiones y otras variables).
* **Geolog (archivos)**: los perfiles de un pozo escritos como un paquete que Geolog carga con sus propios cargadores de
  LAS y DLIS, y los archivos que Geolog escribe leídos de vuelta, con sus valores nulos.

## Antes de empezar

* Una superficie: un archivo `.obj` (con su `.mtl` y las imágenes en la misma carpeta), o un volumen segmentado.
* NetCDF: un archivo NetCDF clásico existente (o NetCDF-4, con h5py instalado) y el volumen a guardar.
* Geolog: los perfiles de un pozo (pestaña Perfiles de pozo); los archivos DLIS se escriben cuando `dliswriter` está
  instalado y se leen cuando `dlisio` está instalado; LAS siempre.

## Paso a paso

### Superficies 3D

1. En **Superficies 3D**, escriba los **mm por unidad del archivo OBJ** (1 si el modelo está en mm; 1000 en metros) y
   pulse **Importar OBJ…**. La superficie queda con la muestra actual y se muestra: arrastre para girar, rueda del
   ratón para ampliar.
2. Para crear una a partir de un volumen, abra una segmentación, elija el **Segmento** y pulse **A partir del
   segmento**.
3. **Exportar OBJ…** escribe el OBJ, su MTL y las texturas en PNG; **Eliminar la superficie** la quita.

### Guardar en un archivo NetCDF

1. Abra el volumen a guardar y, en **Guardar en un archivo NetCDF existente**, elija el **Archivo NetCDF**.
2. Marque **Reemplazar una variable del mismo nombre** para sobrescribirla; si no, se da un nombre nuevo (`_2`, `_3`…).
3. Pulse **Guardar el volumen actual en el archivo**. Un volumen con la misma forma que una variable del archivo toma
   sus dimensiones, de modo que queda alineado con la imagen de la que vino.

### Geolog

1. En **Geolog (archivos)** elija el **Pozo** y pulse **Escribir un paquete para Geolog…**, y luego una carpeta: un LAS
   por perfil de imagen, un LAS por malla de profundidad para las curvas, un DLIS con todos los perfiles,
   `rockface_geolog.json` y `README_geolog.txt`.
2. Para leer los archivos de Geolog, escriba los **Valores nulos** (−999,25; −999; −9999; −99999 por defecto) y el
   **Diámetro** del pozo, y pulse **Leer archivos de Geolog…** sobre la carpeta (o un archivo).

## Opciones

| Campo | Qué cambia |
|---|---|
| mm por unidad del archivo OBJ | Escala de los vértices a mm |
| Reemplazar una variable del mismo nombre | Sobrescribir en vez de añadir un sufijo |
| Valores nulos | Valores leídos como faltantes en los archivos LAS y DLIS, además del NULL de cada LAS |
| Diámetro | Diámetro del pozo asignado a los perfiles de imagen leídos |

## Cómo funciona

* **OBJ/MTL**: vértices (con colores por vértice opcionales), coordenadas de textura, normales, caras de cualquier
  número de lados divididas en triángulos, índices negativos, `usemtl` y `mtllib`; materiales con `Kd`, `d` y
  `map_Kd`. Un vértice usado con dos coordenadas de textura pasa a ser dos vértices. La vista dibuja las caras de atrás
  hacia delante (algoritmo del pintor) con el color de la textura en su centro y sombreado de Lambert; las mallas
  pesadas se reducen para la vista agrupando vértices (Rossignac & Borrel 1993). A partir de un volumen, la superficie
  se hace por marching cubes (Lorensen & Cline 1987) tras un ligero suavizado gaussiano de la máscara (área de una
  esfera dentro del 0,5 %).
* **NetCDF**: un archivo clásico se reescribe mediante un archivo temporal con todo lo que tenía más las nuevas
  variables, y luego se reemplaza; un NetCDF-4 recibe las variables en el propio archivo y se enlazan las escalas de
  dimensión de la variable correspondiente.
* **Geolog**: mnemónicos en mayúsculas, letras, dígitos y guion bajo, como máximo 32 caracteres, únicos; el manifiesto
  guarda lo que LAS no guarda (tipos, leyendas de los segmentos, azimuts, diámetro), para que el paquete vuelva entero
  a RockFace.

## Desde un script

```python
s = prj.import_surface("core_box.obj", sample, scale_mm=1000)
s.render("core_box.png")
prj.volume("plug segmentation").save_into_netcdf("plug.nc")
prj.geolog_export("Well A", "to_geolog")
logs = prj.geolog_import("from_geolog", "Well A", nulls=(-999.25, -9999))
```

## Límites y problemas comunes

* La vista muestra un color por cara; las texturas muy finas sobre caras grandes se ven planas (el OBJ escrito conserva
  la textura entera).
* Los archivos NetCDF clásicos de más de 2 GB necesitan el formato de offset de 64 bits, que la reescritura conserva;
  NetCDF-4 necesita h5py.
* RockFace no abre por sí mismo un proyecto de Geolog: el intercambio es por archivos, que Geolog carga y escribe.

## Cobertura

GV18 (superficies 3D texturizadas), GV15 (guardar en un archivo NetCDF existente), GM1 (integración con Geolog), GM2
(herramientas de importación y exportación).
