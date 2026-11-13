# RockFace Lab: registro y la calculadora de imágenes

## Para qué sirve

El **Registro** alinea una imagen de una lámina sobre otra — la imagen de nícoles cruzados sobre la de luz polarizada
plana, una imagen de catodoluminiscencia, un segundo escaneo — por pares de puntos y/o automáticamente, y la escribe
sobre la malla de píxeles de la imagen fija, para que las dos puedan usarse juntas píxel a píxel. La **Calculadora**
combina las imágenes de una lámina con una fórmula, píxel a píxel: una máscara de los píxeles oscuros del XP, la
diferencia de dos luces, un umbral del tono.

## Antes de empezar

Dos imágenes de la misma lámina en RockFace Lab (página [RockFace Lab: recorte, filtros y la máscara de la muestra](lab_preparation.md)).

## Paso a paso

### Registro

1. Abra la pestaña **Registro**.
2. **Imagen fija** (normalmente la PP) e **Imagen móvil** (XP, CL…).
3. **Transformación**: **traslación**, **semejanza (giro, escala, traslación)**, **afín** o **spline de placa
   delgada**.
4. O bien:
   * **Pares de puntos…** — haga clic en un punto de la imagen fija (izquierda) y luego en el mismo punto de la móvil
     (derecha); el ajuste se hace tras cada par, con el **Residuo** de cada uno y "RMS … px, dejando uno fuera … px";
     **Quitar par**, **Quitar todos**; o
   * **Automático** — la correlación de los contornos de los granos (ECC), partiendo del marco de las láminas o de los
     pares. **Búsqueda (automática)**: desde el marco de la lámina, **traslación**, **cualquier giro** o **giro y
     escala**.
5. El resultado: "…: giro …°, escala …, traslación … px", la correlación de los contornos, los errores de los pares.
6. Compruebe: **Móvil sobre fija** mezcla las dos; **Parpadeo** las alterna.
7. **Guardar el registro** lo guarda en la imagen móvil; **Escribir sobre la malla de la fija** escribe la imagen móvil
   remuestreada píxel a píxel sobre la fija ("Imagen añadida sobre la malla fija: …").

### Calculadora

1. Abra la pestaña **Calculadora**. Se listan las imágenes de la lámina; haga doble clic en un nombre para insertarlo.
2. Escriba la **Fórmula**, con `{nombre de la imagen}` y un canal: `.r .g .b`, `.l` (luminancia), `.h .s .v`.
   Ejemplos:
   * `{XP}.l < 40` — los píxeles oscuros del XP (una máscara);
   * `({PP}.v − {XP}.v)/2 + 128` — una imagen en gris;
   * `where({PP}.h > 190, 255, 0)`.
   Números, `+ − * / **`, comparaciones, `& | ~`, y `abs sqrt log log10 exp min max where clip round`.
3. **Imagen de referencia** — la malla del resultado (las demás imágenes se toman sobre ella mediante sus registros).
4. **Resultado**: **según la fórmula** (una comparación da una máscara, un número una imagen en gris), **máscara** o
   **imagen en gris**. **Estirar los valores** con el **Valor en negro** y el **Valor en blanco**.
5. **Nombre del resultado** y luego **Calcular**. "Usa: …" lista las imágenes usadas. "Resultado añadido: …".

## Opciones

| Opción | Qué cambia |
|---|---|
| Transformación | Traslación, semejanza, afín (≥ 3 pares) o spline de placa delgada (no lineal, muchos pares). |
| Búsqueda (automática) | Hasta dónde busca el registro automático: ninguna, traslación, cualquier giro, giro y escala. |
| Resultado | Máscara (un mapa de 0/1) o imagen en gris. |

## Cómo funciona

* Los ajustes de pares de puntos son de mínimos cuadrados; el error dejando uno fuera predice cada par con los demás.
  El registro automático maximiza el coeficiente de correlación mejorado (ECC) de los contornos de los granos, tras
  una búsqueda de traslación, giro y escala.
* Comprobaciones: XP sobre PP recuperado dentro de 0,017 px para cualquier giro y ±8 % de escala; un escaneo
  desplazado 6 px corregido a 0,15 px; una spline de placa delgada a 0,06 px en una deformación no lineal; en pares
  reales de láminas, el desplazamiento común se encontró en 52 y 59 de 60 recortes.
* La calculadora trabaja bloque a bloque sobre la malla de la imagen de referencia.

## Desde un script

```python
pp_c, xp_c = prj.image("ILLUSTRATIVE mosaic PP (crop)"), prj.image("ILLUSTRATIVE mosaic XP (crop)")
t = xp_c.register_on(pp_c, search="rotation")            # automático, desde el marco de las láminas
print(t.rotation_deg, t.scale, t.ecc)
xp_on_pp = xp_c.resample_on(pp_c)                        # sobre la malla de la imagen PP
oscuro = prj.calculate("{%s}.l < 60" % xp_on_pp.name, pp_c, name="oscuro en XP")
print(oscuro.areas_mm2())
```

## Límites y problemas comunes

* "Elija dos imágenes distintas de la lámina."
* "N pares: se necesitan al menos …." — 1 para una traslación, 2 para una semejanza, 3 para una transformación afín,
  4 para una spline de placa delgada.
* El registro automático necesita imágenes con granos en común; en luces muy distintas (CL sobre PP), dé antes algunos
  pares de puntos.

## Cobertura

GT5 (registro PP ↔ XP con pares de puntos, registro automático), GT19 (Volume Calculator de las "More tools").
