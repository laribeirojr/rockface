# Un mapa mineral alineado sin puntos de control; efectos en volúmenes grandes

## Para qué sirve

Dos detalles encontrados por la auditoría de 0.23 y cerrados en 0.28. **Un mapa mineral alineado sobre una
segmentación de la imagen** sin marcar pares de puntos (el Thin Section Auto Registration de GeoSlicer). **Los
efectos del editor de segmentos en volúmenes grandes** — margen, suavizado, eliminación de bordes y expansión — a
resolución completa, por bloques de cortes, en lugar de en un nivel reducido (los efectos Big Image de GeoSlicer).

## Antes de empezar

* Alineación: una segmentación de la imagen (Lab → Segmentación) y el mapa mineral de la misma lámina, ambos con una
  fase de poro (papel de la fase "Poro"), o con fases que muestren los mismos bordes.
* Efectos: un volumen segmentado en MC.

## Paso a paso

1. **Lab → Registro**: elija la segmentación como *Imagen fija* y el mapa mineral (marcado "mapa") como *Imagen
   móvil*; **Automático** (con *Búsqueda (automática)* "traslación", "cualquier giro" o "giro y escala" cuando los dos no
   tienen un marco de la lámina en común); **Guardar el registro**. El mapa queda superpuesto a la imagen en Atlas y
   en Lab.
2. **MC → Segmentación → Efectos sobre el volumen segmentado**: nada cambia para el usuario — un volumen demasiado grande para tenerlo entero en
   memoria ahora se edita a resolución completa, unos pocos cortes a la vez.

## Cómo funciona

* Alineación: los poros de cada mapa (o, sin poros, los bordes entre dos fases cualesquiera) se convierten en una
  imagen en gris; las dos se alinean por ECC sobre sus gradientes en una pirámide (Evangelidis & Psarakis 2008),
  partiendo de los marcos de la lámina o de la búsqueda, como Lab alinea dos imágenes (0.17).
* Efectos: cada bloque de cortes se lee con el margen en z que necesita el efecto (el margen o el ancho más un corte,
  el tamaño del suavizado más uno) y se recorta después del efecto — el mismo resultado que en el volumen entero. En
  la *expansión* el segmento más cercano se busca en el bloque y en 16 cortes alrededor (`halo`).

## Desde un script

```python
t = prj.image("Mapa mineral").register_on("Segmentación", search="shift")   # dos mapas: por sus poros
rf.lab.register_map(prj.raw, seg_id, map_id, fixed_phases=[1], map_phases=[3])
rf.vol_tools.edit_labels(prj.raw, labels_id, "boundary_removal", width=2)   # volúmenes grandes: por bloques
```

## Límites y problemas comunes

* Las fases elegidas deben ser lo mismo en los dos mapas (los poros de la imagen y la porosidad del mapa); con
  conjuntos de fases muy distintos use pares de puntos.
* Islas, operaciones lógicas, crecer desde semillas y trazado de nivel siguen en un nivel reducido en volúmenes muy
  grandes: necesitan el volumen entero a la vez.

## Cobertura

Filas de la auditoría de 0.23 ThinSectionAutoRegistration (GT5), BoundaryRemovalBigImage y ExpandSegmentsBigImage
(GV6, GV8).
