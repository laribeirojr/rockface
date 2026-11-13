# Mapas mineralógicos: registro, superposición, compuesto y cuantificación

## Para qué sirve

Un mapa mineralógico de QEMSCAN, MLA, TIMA, un mapa de fases de µXRF o cualquier imagen clasificada dice qué mineral
hay en cada píxel. RockFace Atlas lo registra sobre la imagen óptica de la misma lámina, lo superpone a la imagen con
cualquier opacidad, genera una **imagen compuesta** (el mapa mezclado sobre la fotografía, con su leyenda y escala) y
**cuantifica** cada fase sobre todo el mapa o sobre cualquier región — comparando el mapa con el conteo de puntos.

## Antes de empezar

* Una descripción guardada cuya lámina tenga (de preferencia) una imagen óptica de la lámina entera en Atlas.
* El mapa en PNG o TIFF (una imagen de paleta, una imagen gris de números de fase o una imagen RGB de los colores de
  las fases) y su leyenda: CSV o TXT (con o sin encabezado, por ejemplo `Mineral,R,G,B`) o una tabla de colores de 3D
  Slicer.

## Paso a paso

### Importar el mapa

1. En RockFace Atlas, **Mapa mineralógico…**.
2. En **Importar un mapa mineralógico**, elija el mapa, su **Leyenda** (por defecto el archivo de leyenda encontrado
   junto al mapa), la **Tolerancia de color** (cuánto puede alejarse un color de un mapa RGB del de la leyenda) y el
   **µm por píxel**.
3. RockFace lee las fases ("… píxeles, N fases"). En la pestaña **Mapa**, revise cada fase:
   * nombre de la **Fase** y **Color**;
   * **Papel**: Mineral, Poro, Fondo o Sin clasificar;
   * **Conceptos**: códigos de constituyentes, grupos o tipos de la nomenclatura, separados por comas (por ejemplo
     `quartz, quartz_dia`; `pore`) — ligan el mapa a la nomenclatura y al conteo de puntos;
   * **Ver** oculta o muestra una fase; **Ver todas**, **Ocultar todas**; **Fusionar** une las fases seleccionadas.
4. **Guardar fases**.

### Registrar el mapa sobre la imagen óptica

1. **Registrar…** abre las dos imágenes lado a lado.
2. Haga clic en un punto de la imagen óptica (izquierda) y luego en el mismo punto del mapa (derecha): una esquina de
   grano, un poro, una raya. Repita. Dos pares bastan para una **semejanza** (rotación, escala, traslación), tres para
   una transformación **afín**; repártalos por el mapa y añada algunos más.
3. La tabla da cada **Par** con su **Residuo**; **Quitar par**, **Quitar todos**.
4. Elija la **Transformación** y **Aplicar**. RockFace informa el RMS de los pares y el **error dejando uno fuera**
   (cada par predicho por los demás), la escala y la rotación.
5. El mapa se dibuja ahora en el sistema de la lámina, sobre todas sus imágenes: en el visor, elíjalo en **Encima:** y
   ajuste la opacidad. **Lado a lado** muestra las dos imágenes con **Mover las dos vistas juntas**. **Quitar**
   deshace el registro (el mapa vuelve a su escala en el origen de la lámina).

### Cuantificar

1. En **Cuantificación**, elija la **Región**: **Todo el mapa**, **Área en pantalla**, o una anotación (un rectángulo o
   contorno dibujado en cualquier imagen de la lámina).
2. Elija una descripción en **Comparar con** para poner su conteo de puntos junto al mapa.
3. **Cuantificar**. La tabla da cada fase con el **% mapa**, el **Área (mm²)**, el **% conteo** y la **Diferencia**, y
   el resumen: área analizada, la parte de minerales y poros, porosidad. Los píxeles de fondo y sin clasificar quedan
   fuera de los %.
4. **Exportar CSV…** guarda la tabla.

### La imagen compuesta

1. **Composición…** abre **Imagen compuesta**.
2. **Imagen óptica** (por defecto la lámina en luz polarizada plana), **Mapa dibujado como** (colores mezclados sobre
   la imagen, o contornos de las fases), opacidad, **Ancho**, **Región** (imagen entera o el área en pantalla).
3. **Leyenda con el % de cada fase, y barra de escala**; añadirla también a la biblioteca de imágenes.
4. **Aceptar** y guarde la imagen.

## Opciones

| Opción | Qué cambia |
|---|---|
| Tolerancia de color | Distancia RGB dentro de la cual un color del mapa se toma como un color de la leyenda. |
| Papel | Fondo y sin clasificar quedan fuera de los %; los poros dan la porosidad. |
| Conceptos | El enlace con las líneas de la composición para la comparación con el conteo. |
| Transformación | Semejanza (≥ 2 pares) o afín (≥ 3 pares). |

## Cómo funciona

El registro es un ajuste de mínimos cuadrados de los pares de puntos de control; el error dejando uno fuera es una
estimación conservadora del error real (alrededor del doble, en casos de prueba con respuesta conocida: seis pares
marcados al píxel más cercano dan 2,9 µm de RMS en un mapa de 10 µm). Las teselas del mapa guardan números de fase
dibujados mediante una tabla de colores, por lo que las fases se muestran, ocultan o recolorean al instante. Un mapa
también puede alinearse sobre una segmentación sin puntos de control (página [Un mapa mineral alineado sin puntos de control; efectos en volúmenes grandes](map_alignment_big_volumes.md)).

## Desde un script

```python
d = prj["TS-9"]
qem = d.add_map("TS-9_qemscan.tif", legend="TS-9_qemscan.csv", um_per_px=10)
pp = prj.image("TS-9 PP")
fit = qem.register([((140, 120), (380, 288)), ((1250, 90), (1860, 314)), ((700, 520), (1102, 854)),
                    ((180, 880), (390, 1304))], model="similarity", target=pp)
print(f"RMS {fit.rms_um:.1f} µm, dejando uno fuera {fit.loo_um:.1f} µm")
for row in qem.compare(d):
    print(row["phase"], round(row["map"], 1), row["count"])
qem.composite("TS-9_compuesto.png", base=pp, opacity=0.5)
```

## Límites y problemas comunes

* "Esta lámina no tiene mapa mineralógico. Importe uno con Mapa mineralógico…"
* "N pares: se necesitan al menos …."
* "Sin registrar y sin escala: regístrelo sobre la imagen óptica."
* Un mapa RGB con colores lejos de la leyenda: aumente la tolerancia de color, o dé una leyenda con los colores exactos.

## Cobertura

GT2 (mapas QEMSCAN), GT5 (registro con pares de puntos de control), L9 (superposición de la imagen óptica y del mapa
mineralógico automatizado → imagen compuesta).
