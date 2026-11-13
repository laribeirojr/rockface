# RockFace Lab: segmentación y porosidad

## Para qué sirve

La **segmentación** separa los píxeles de una imagen de lámina en segmentos — poro, granos, cemento, matriz… — y
guarda el resultado como un **mapa** sobre la imagen. Su segmento de poro da la **porosidad**. RockFace Lab ofrece los
métodos clásicos: la resina azul, umbrales de un canal (también Otsu de varios niveles), un rango de color, un
clasificador bayesiano aprendido de muestras dibujadas en la imagen, k-medias (también sobre superpíxeles), semillas
que crecen por watershed, y un bosque aleatorio entrenado con ejemplos pintados.

## Antes de empezar

Una imagen de la lámina en RockFace Lab, de preferencia recortada y filtrada (página [RockFace Lab: recorte, filtros y la máscara de la muestra](lab_preparation.md)). Una máscara
de la muestra limita la segmentación a la roca.

## Paso a paso

1. Abra la pestaña **Segmentación** y seleccione una imagen (no un mapa).
2. **Método**:
   * **Resina azul (poro / sólido)** — la resina epoxi azul es poro. En CIELAB la resina se encuentra por su azul
     (b*), con el corte elegido automáticamente (Otsu) o escrito, y el **Croma mínimo**; o por el **Ángulo de tono
     CIELAB**. La resina puede separarse por su claridad: **no: toda la resina es poro**, **poro abierto = resina clara
     (Otsu)**, o **poro abierto = L* como mínimo…** — la parte oscura, teñida por la resina, es entonces
     microporosidad.
   * **Umbrales de un canal** — elija el **Canal** (luminancia, rojo, verde, azul, tono, saturación y valor HSV, L*,
     a*, b*, croma y ángulo de tono CIELAB) y los cortes; vacío: automático (Otsu de varios niveles).
   * **Rango de color (HSV)** — los rangos de tono, saturación y valor de un segmento.
   * **Clasificador bayesiano (muestras)** — **Dibujar una muestra del segmento elegido** para cada segmento (al menos
     8 píxeles cada una); el clasificador aprende sus colores.
   * **K-medias (no supervisado)** — el número de **Grupos**, sobre píxeles o sobre **Superpíxeles**.
   * **Crecer desde semillas (watershed)** — **Pintar semillas del segmento elegido** con el **Radio del pincel**.
   * **Bosque aleatorio (ejemplos pintados)** — página [Segmentar por ejemplos pintados (bosque aleatorio)](random_forest.md).
3. **Segmentos**: **Añadir segmento**, **Quitar segmento**; cada uno con su nombre, color y **Papel** (poro, sólido,
   sin clasificar).
4. Región: la imagen entera, o una máscara de la muestra.
5. **Segmentar**. La vista previa muestra el mapa sobre la imagen y la "Parte del área contada" de cada segmento, la
   **Porosidad (poro / poro + sólido)** y los umbrales usados.
6. Limpie el mapa: **Islas menores que** (píxeles dados a su entorno) y **Suavizado (mayoría)**.
7. **Nombre del mapa** y luego **Guardar la segmentación como mapa**. "Segmentación guardada: … (porosidad … %)."

El mapa puede corregirse a mano y separarse en objetos (página [RockFace Lab: edición de mapas y objetos](lab_editing_objects.md)), y luego medirse (página
[RockFace Lab: medidas y distribuciones de tamaño](lab_measurements.md)).

## Opciones

| Opción | Qué cambia |
|---|---|
| Resina azul — la separación por L* | Toda la resina es poro, o solo la resina clara (poro abierto); la resina oscura es microporosidad. |
| Canal, cortes | Qué canal se corta, y dónde (vacío: Otsu). |
| Superpíxeles (k-medias) | Agrupar superpíxeles SLIC en vez de píxeles: segmentos más suaves. |
| Papel | Poro y sólido hacen la porosidad; sin clasificar queda fuera de ella. |

## Cómo funciona

* Los colores se convierten a CIELAB (dentro de 0,0049 de scikit-image en 100 000 colores) y a HSV; se ofrecen 12
  canales.
* En tres láminas ILUSTRATIVAS de verdad exacta (22,3–25,6 % de porosidad), la resina azul, el Otsu de b* y el
  clasificador bayesiano fueron exactos en imágenes limpias y quedaron dentro de 0,5 puntos (IoU ≥ 0,95) con
  desenfoque, ruido y resina más fina a la vez.
* En las 20 láminas carbonáticas de GO-Forward D2.1 (CC BY 4.0), cuyos valores publicados son la porosidad abierta de
  una segmentación SLIC + k-medias, la resina por ángulo de tono con la separación por L* sigue esos valores con una
  correlación de 0,97; contar toda la resina da la porosidad óptica total.
* El mapa es una imagen en teselas como las demás, en el sistema de la lámina, por lo que se superpone a todas las
  imágenes de la lámina en Atlas y en Lab.

## Desde un script

```python
pp = prj.image("ILLUSTRATIVE mosaic PP")
seg = pp.segment("resin", post=[("islands", {"min_px": 20})])
print(f"porosidad {seg.porosity():.2f} %")
km = pp.segment("kmeans", k=4, superpixels=5000, save=False)          # un vistazo, no se escribe nada
otsu = pp.segment("thresholds", channel="b", classes=3, name="Otsu de b*")
```

## Límites y problemas comunes

* "Elija una imagen de la lámina (no un mapa) para segmentar."
* "Dibuje una muestra (de al menos 8 píxeles) de cada segmento." / "Pinte semillas de al menos un segmento."
* La vista previa se calcula en un nivel reducido en imágenes grandes ("Calculado en el nivel …"); el mapa guardado
  está a resolución completa.
* Láminas sin resina azul: use umbrales, un rango de color, el clasificador o el bosque aleatorio.

## Cobertura

GT7 (segmentación manual y por umbrales), GT8 (poro / no poro por inferencia bayesiana), L7 en parte (cuantificación de
la lámina entera, clásica).
