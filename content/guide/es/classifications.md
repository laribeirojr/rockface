# Clasificaciones y diagramas ternarios

## Para qué sirve

La pestaña **Clasificación** da nombre a la roca: areniscas por Folk (1980) y McBride (1963), proveniencia por
Dickinson (QtFL y QmFLt), textura por las clases grava–arena–lodo de Folk, carbonatos por Dunham, Embry y Klovan,
Wright, Grabau y Bramkamp y Powers. Cada clasificación se calcula a partir de la composición, sobre la composición
actual y la original, y las ternarias se dibujan en una ventana de diagrama. Un proyecto puede añadir sus propias
clasificaciones ternarias.

## Antes de empezar

* Una descripción con su composición (y, para la textura, los % de grava, arena y lodo de la pestaña Microscópica).
* Para carbonatos: los datos de rocas carbonáticas que la composición no da (abajo).

## Paso a paso

### Leer las clasificaciones

1. Abra la pestaña **Clasificación**. **Clasificaciones** lista cada clasificación con su resultado **Actual** y
   **Original**.
2. "sin datos" significa que la composición no tiene lo que la clasificación necesita; "fuera de los campos", que el
   punto cae fuera de todos los campos; "Cerca del límite con: …", que está dentro de la tolerancia de otro campo.
3. **Observaciones** — una nota sobre la clasificación.

### El diagrama ternario

1. Seleccione una clasificación ternaria y pulse **Diagrama…**.
2. La ventana **Diagrama ternario** muestra los campos, el punto de la descripción y, con **Punto original**, el punto
   de la composición original.
3. **Valores (% de los tres polos)** da cada **Polo** y el **Resultado**; **Bajo el cursor** nombra el campo bajo el
   ratón.
4. **Ajustar**, **Acercar**, **Alejar**; **Tamaño del punto**; **Colores** (campos coloreados o no); **Nombres**
   (nombres de los campos activados o no).
5. **Exportar imagen…** guarda el diagrama en PNG o SVG.

### Rocas carbonáticas

1. Cuando los carbonatos son más de la mitad de los sólidos, complete **Rocas carbonáticas: lo que la composición no
   indica**:
   * **Soporte de la fábrica** (como en la pestaña Microscópica, o fijado aquí); **Ligada orgánicamente en la
     depositación** (no; sí, modo desconocido; organismos deflectores; organismos incrustantes que ligan; armazón
     rígido);
   * **Granos mayores que 2 mm (% de los granos)** y su soporte;
   * **Contactos microestilolíticos**, **El cemento es el componente principal**, **La diagénesis obliteró la
     fábrica**;
   * **Tamaño de cristal (µm)** y el tamaño de grano dominante (mm);
   * los datos de Bramkamp y Powers (página [McBride, Bramkamp & Powers y las clases de empaquetamiento](classifications_packing.md)).
2. **Posibilidades…** lista todas las clases de la clasificación seleccionada con sus criterios, marcando la
   encontrada. **Falta: …** nombra los datos que aún faltan.

### Una clasificación del proyecto

1. **Gestionar clasificaciones…** (en la pestaña o en la ventana del diagrama) abre **Clasificaciones ternarias del
   proyecto**.
2. **Nueva**; dé el **Código** y el nombre.
3. **Polos**: tres polos, cada uno con un **Símbolo** y los **Totales sumados** (códigos de totales separados por
   comas).
4. **Campos**: **Añadir campo**, su nombre y sus **Vértices** — tres porcentajes por vértice en el orden de los polos,
   vértices separados por punto y coma (por ejemplo `100 0 0; 50 50 0; 50 0 50`).
5. **Aplicar**. La clasificación aparece en todas las descripciones del proyecto, en los grupos de Explorer y en las
   figuras.

## Opciones

| Clasificación | Datos |
|---|---|
| Folk (1980), McBride (1963) — QFR | cuarzo, feldespatos y fragmentos de roca de la composición |
| Dickinson QtFL, QmFLt | supone el conteo Gazzi–Dickinson; los fragmentos plutónicos no se grafican |
| Folk (1954) grava–arena–lodo | % de grava, arena y lodo de la pestaña Microscópica |
| Dunham (1962), Embry y Klovan (1971) | soporte, granos, lodo, ligazón orgánica, granos > 2 mm |
| Wright (1992) | también cemento, microestilolitos, obliteración, tamaño de cristal |
| Grabau (1904) | tamaño de grano dominante de los granos carbonáticos |
| Bramkamp y Powers (1958) | grupo, textura, porosidad, alteración, dolomita |

## Cómo funciona

* Un punto ternario son los totales de los tres polos normalizados a 100; el campo se encuentra por punto-en-polígono
  sobre los límites publicados (Folk 1980; McBride 1963; Dickinson et al. 1983 y Dickinson 1985).
* Los subcampos del orógeno reciclado del QmFLt vienen de una sola digitalización de la figura publicada y están
  marcados "Límites por verificar con la figura original."
* Las clases de carbonatos siguen los criterios de sus artículos, mostrados en **Posibilidades…**. Se aplican cuando
  los carbonatos superan el 50 % de los sólidos ("Los carbonatos son … % de los sólidos; las clasificaciones de
  carbonatos se aplican por encima del 50 %").

## Desde un script

```python
d = prj["TS-9"]
print(d.classify("folk1980", label=True), d.point("folk1980"))
print(d.classify("dunham1962"), d.classify("folk1980", original=True))
d.carbonate.support = "grain_supported"               # datos de carbonatos, luego guardar
d.save()
rf.ternary_figure("qtfl.svg", "dickinson_qtfl", [d], original=False)   # se pueden dar varias descripciones
```

## Límites y problemas comunes

* "sin datos": a la composición le faltan los polos (ningún feldespato y ningún fragmento sigue siendo un punto;
  ningún grano del armazón no lo es).
* Campos personalizados con vértices que no suman 100: "Vértices no entendidos".
* Se rechaza una clasificación del proyecto con un código ya usado.

## Cobertura

P29 (clasificaciones siliciclásticas, actual y original), P30 (proveniencia de Dickinson), P31 (ventana del diagrama
ternario), P32 (clasificaciones de carbonatos y la tabla de posibilidades), M3 (clasificaciones recalculadas con los
datos más recientes).
