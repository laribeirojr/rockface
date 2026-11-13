# Modelo de permeabilidad de perfiles de imagen

## Para qué sirve

Una curva continua de permeabilidad a lo largo del pozo a partir de un **perfil de imagen segmentado** (p. ej. vúgulos,
matriz microporosa y matriz cerrada en un perfil de amplitud acústica), de una **curva de porosidad** y de las
**permeabilidades de plugs** medidas en el laboratorio. Está pensado para carbonatos de doble porosidad, en los que los
vúgulos vistos en la imagen llevan buena parte del flujo.

## Antes de empezar

* Un perfil de imagen segmentado (pestaña Perfiles de pozo → Segmentación), con un segmento para los macroporos
  (vúgulos).
* Una curva de porosidad del mismo pozo (importada de LAS, CSV…; en fracción o en %).
* Las permeabilidades de plugs: profundidad (m) y K (mD), al menos dos dentro de la imagen.

## Paso a paso

1. Abra el perfil de imagen segmentado y vaya a la pestaña **Perfiles de pozo**, grupo **Modelo de permeabilidad
   (perfil de imagen)**.
2. Elija el **Perfil de imagen segmentado** y la **Curva de porosidad**.
3. Elija el **Segmento de macroporos** (su exponente de porosidad es fijo en 1) y, si hace falta, un **Segmento
   ignorado** (una clase de incertidumbre o de imagen mala).
4. Ajuste la **Ventana de profundidad** en la que se cuentan las fracciones de los segmentos (0: cada fila de la
   imagen).
5. Pegue los **Plugs**, uno por línea: profundidad y K (espacios, tabulaciones o punto y coma).
6. Opcionalmente escriba **Puntos forzados (Kds)** del mismo modo: profundidades y K cerca de los cuales debe pasar la
   curva, para corregir una zona de interés.
7. Pulse **Ajustar y escribir la curva de permeabilidad**. La curva (unidad mD) se añade al pozo, y se muestra el
   ajuste: número de plugs, desajuste de log10 K, R² y A y B de cada segmento.

## Opciones

| Campo | Qué cambia |
|---|---|
| Segmento de macroporos | El segmento cuyo término es A·F·Φ (exponente 1) |
| Segmento ignorado | Píxeles dejados fuera de las fracciones |
| Ventana de profundidad | Filas reunidas en una profundidad de la curva |
| Puntos forzados (Kds) | Puntos adicionales del ajuste, con diez veces el peso de un plug |

## Cómo funciona

En cada profundidad (Menezes de Jesus, Compan & Surmas 2016):

K = A1·F1·Φ^B1 + A2·F2·Φ^B2 + … + An·Fn·Φ^Bn + Am·Fm·Φ

donde Fn es la fracción del segmento n en las filas de esa profundidad, Φ la curva de porosidad interpolada en las
profundidades de la imagen, Fm la fracción del segmento de macroporos. A ≥ 0 y 0 ≤ B ≤ 8 se ajustan a los plugs por
mínimos cuadrados en log10 K (la permeabilidad varía por décadas), a partir de varios exponentes iniciales (región de
confianza reflectiva). Plugs sintéticos hechos con A y B conocidos se recuperan exactamente.

## Desde un script

```python
seg = prj.log("AMP (segmentation)")
k, fit = seg.permeability_model("PHIT", [(2510.35, 120.0), (2512.10, 8.5), (2515.80, 300.0)], macro="Pore",
                                window_m=0.1)
print(fit["A"], fit["B"], fit["rms_log10"])
```

## Límites y problemas comunes

* Con pocos plugs, los términos de las clases de poca influencia pueden salir 0; revise los A y B mostrados y el
  desajuste.
* El modelo usa solo la imagen y la porosidad; los plugs deben muestrear las clases de la imagen para que el ajuste
  valga en otros tramos.

## Cobertura

GI10 (modelado de permeabilidad).
