# RockFace Lab: edición de mapas y objetos

## Para qué sirve

Una segmentación rara vez es perfecta: un grano pintado como cemento, burbujas en la resina tomadas por poros, una
raya. La pestaña **Edición y objetos** corrige un mapa a mano sobre su imagen — pincel, borrador, polígono, tijeras,
trazado por nivel, islas — y separa uno de sus segmentos en **objetos**: cada grano o cuerpo de poro por separado, para
poder medirlo. Los objetos se pueden unir, dividir, cortar y borrar. Todo cambio se puede deshacer.

## Antes de empezar

Un mapa de la lámina: una segmentación (página [RockFace Lab: segmentación y porosidad](lab_segmentation.md)) o un mapa mineralógico ("La lámina aún no tiene
mapas: segmente primero una imagen.").

## Paso a paso

### Corregir un mapa

1. Abra **Edición y objetos** y elija el **Mapa**; ajuste su **Opacidad** sobre la imagen.
2. Marque **Editar el mapa** y elija el **Segmento escrito**.
3. Elija una herramienta:
   * **Pincel** — arrastre sobre la imagen para pintar el segmento elegido (**Radio del pincel**);
   * **Borrador** — arrastre para borrar (sin clasificar);
   * **Polígono** — haga clic en las esquinas; un doble clic o Enter lo rellena;
   * **Tijeras** — dibuje un polígono: su interior (o, con **Tijeras: fuera del polígono**, su exterior) recibe el
     segmento elegido;
   * **Trazado por nivel** — haga clic en un punto: los píxeles conectados de color parecido (**Tolerancia de color
     (ΔE*ab)**) reciben el segmento elegido.
4. **Islas menores que** y **Quitar las islas**: los trozos pequeños se dan a su entorno.
5. **Deshacer** y **Rehacer** — "Cambios que se pueden deshacer: …; rehacer: …".

Cada edición se escribe en el mapa a resolución completa y en todos los niveles de zoom a la vez.

### Objetos

1. En **Objetos**, elija el **Segmento a separar** (los granos, o los poros).
2. **Separación**:
   * islas — cada trozo conectado es un objeto;
   * watershed — los granos que se tocan se separan en sus gargantas: **Distancia mínima entre centros** y **Suavizado
     del mapa de distancias (σ)**;
   * SNOW — el watershed sobresegmentado de Gostick (2017), para cuerpos de poro.
3. **Objetos menores que (descartados)**.
4. **Separar en objetos**. "N objetos guardados: …". Los objetos se dibujan cada uno con su color.
5. Edítelos con las herramientas:
   * **Unir** — haga clic en los objetos y luego en **Unir los objetos marcados** ("Objetos marcados: n (al menos
     2)");
   * **Dividir** — haga clic en un objeto para dividirlo por watershed;
   * **Cortar** — haga clic en los dos extremos de una línea de corte;
   * **Borrar** — haga clic en un objeto para borrarlo.
   **Deshacer** y **Rehacer** como para el mapa.

## Opciones

| Opción | Qué cambia |
|---|---|
| Tolerancia de color (ΔE*ab) | Cuánto puede diferir un color y seguir siendo trazado. |
| Distancia mínima entre centros | Mayor: menos objetos, más grandes. |
| Suavizado del mapa de distancias | Mayor: menos división excesiva de granos irregulares. |
| Objetos menores que | Los objetos pequeños se descartan (ruido). |

## Cómo funciona

Las ediciones se escriben en su lugar, en las teselas del mapa, con todos los niveles de la pirámide rehechos; cada
edición devuelve un "parche" para deshacer, de modo que deshacer devuelve exactamente el mapa anterior (comprobado con
mapas escritos de nuevo). Los objetos se guardan como un mapa de objetos: cada píxel guarda el número de su objeto. En
láminas de verdad exacta, los granos separados por watershed y SNOW se encontraron con exhaustividad de 0,78–0,83 y
precisión de 0,96–0,98; con los colores del XP la exhaustividad subió a 0,87–0,89 (página [RockFace Lab: medidas y distribuciones de tamaño](lab_measurements.md)).

## Desde un script

```python
seg = prj.image("ILLUSTRATIVE mosaic PP").segment("resin")      # un mapa de segmentación
patch = seg.paint([(100, 100), (300, 120)], 15, 1)      # pincel a lo largo de una línea, radio 15 px, segmento 1
seg.undo(patch)
seg.level_trace(420, 380, tolerance=8, phase=2)
seg.remove_islands(30)
grains = seg.objects(2, "watershed", min_distance=6, sigma=1.0, min_px=40)
print(grains.object_count())
grains.merge_objects([(1421, 842), (1422, 842)])       # un punto en cada uno de dos objetos que se tocan
grains.cut_objects((600, 300), (640, 360))
```

## Límites y problemas comunes

* "Objetos marcados: 1 (al menos 2)." — haga clic en un segundo objeto antes de unir.
* Separar un mapa muy grande tarda: separe antes un recorte para elegir los parámetros.
* Las tijeras también se alcanzan por script para cualquier polígono (`img.scissors`).

## Cobertura

GT7 (segmentación manual: pintar, borrar, tijeras, trazado por nivel, islas), GT9 (particionado: islas, watershed,
SNOW), GT10 (editor de objetos: unir, dividir, cortar, borrar).
