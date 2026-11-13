# Editar la segmentación de un perfil y sus objetos

## Para qué sirve

Una segmentación automática de un perfil de imagen nunca es perfecta: un vúgulo queda fuera, el borde de un patín se
toma por vúgulo, dos vúgulos se juntan. Aquí usted corrige la segmentación con un pincel y revisa los objetos
(vúgulos, manchas) uno a uno: rechaza los falsos, une los pedazos de un mismo objeto, conserva solo los que tienen
medidas con sentido.

## Antes de empezar

Un perfil segmentado (pestaña Perfiles → Segmentación, objetos y tamaños de poro → Segmentar) o un perfil de objetos
(… → Objetos), abierto en las pistas de RockFace MC.

## Paso a paso

### Corregir una segmentación

1. Abra el perfil segmentado. En **Pincel y objetos**, elija qué **Pintar** (un segmento, o **— borrador —**) y el
   **Radio del pincel** en milímetros de la pared del pozo.
2. Pulse **Pintar en la pista** y arrastre el ratón sobre la pista. Un trazo cruza la costura 0/360° por el lado más
   corto.
3. **Deshacer** quita el último trazo.

### Revisar los objetos

1. Abra el perfil de objetos. La tabla lista cada objeto: profundidad (tope, base, centro), azimut, área, diámetro
   equivalente, altura, ancho, y si toca el tope o la base del perfil.
2. Escriba un filtro (`area_mm2 > 50 and not touches_edge`): la tabla muestra los objetos que pasan; el histograma
   muestra la columna elegida.
3. Elija objetos en la tabla y pulse **Rechazar los elegidos** o **Unir los elegidos**, o pulse **Conservar solo las
   filas mostradas** para rechazar todos los objetos que el filtro oculta.
4. Para añadir un objeto, elija **Un objeto nuevo** en **Pintar** y píntelo; **Hacer crecer el objeto elegido** y
   **Recortar el objeto elegido** cambian el objeto elegido en la tabla.

## Cómo funciona

El pincel es un disco del radio dado sobre la pared desenrollada (paso de profundidad × ancho de la columna, en mm).
Las filas tocadas se reescriben en su lugar, con su pirámide de niveles. Las medidas se recalculan a partir de los
objetos después de cada cambio.

## Desde un script

```python
perfil = prj.log("Vúgulos (ILLUSTRATIVE)")
patch = perfil.paint([(120.0, 2510.30), (126.0, 2510.32)], radius_mm=8, value=2)
perfil.undo(patch)
objetos = prj.log("Vúgulos (ILLUSTRATIVE) (objects)")
tabla = objetos.instances()
rechazados = objetos.keep_only("area_mm2 > 50 & touches_edge == 0")
nuevo = objetos.paint_instance([(200.0, 2511.0)], radius_mm=10)
```

## Límites y problemas comunes

* **"Elija primero un objeto en la tabla."** Hacer crecer y recortar necesitan un objeto elegido.
* La pintura nueva nunca cubre otro objeto; recortar solo quita píxeles del objeto elegido.
* El segmentador de instancias entrenado de GeoSlicer llega en la etapa 0.26.

## Cobertura

GI8 (Segment Editor de los perfiles de imagen, Instance Segmenter Editor).
