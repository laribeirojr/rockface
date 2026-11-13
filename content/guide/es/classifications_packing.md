# McBride, Bramkamp & Powers y las clases de empaquetamiento

## Para qué sirve

Tres clasificaciones que ofrecen los programas de referencia y que RockFace ahora tiene, cada una con su fuente
publicada: **McBride (1963)** para areniscas, **Bramkamp & Powers (1958)** para carbonatos — con su símbolo de roca
reservorio (por ejemplo *21BD*) — y las **clases de empaquetamiento** suelto, normal y cerrado de la proximidad de
empaquetamiento de Kahn (1956).

## Antes de empezar

* Una descripción con su composición (Petro → Composición).
* Para Bramkamp & Powers: los datos carbonáticos que la composición no da (abajo).
* Para la clase de empaquetamiento: los contactos de los granos contados en una traversa, o los tipos de contacto en %.

## Paso a paso

1. **Petro → pestaña Clasificación.** McBride aparece junto a Folk (1980), con el campo actual y el original;
   **Diagrama…** dibuja el triángulo.
2. En una roca carbonática, complete los **datos carbonáticos** abajo a la derecha:
   * *Textura original (Bramkamp & Powers)*: no alterada visiblemente, moderadamente alterada, fuertemente alterada
     (aún reconocible) u obliterada;
   * *Porosidad visual*: A porosa o poco cementada, B compacta, C densa;
   * *Alterada por*: por la dolomita (por defecto), anhidrita (A), sílice (S) o cambios poco comprendidos (X);
   * *Facies*, *Grupo* y *Dolomita %* vienen de la composición y se pueden cambiar;
   * *Tipo especial de roca*: 14AX/14BX, 31BX o 51BX cuando los huecos reemplazan granos.
3. La fila *Carbonatos — Bramkamp & Powers (1958)* muestra el nombre, la facies y el símbolo; **Posibilidades…**
   lista las 28 clases con sus criterios.
4. **Petro → pestaña Microscópica → Contactos y empaquetamiento.** Escriba los contactos grano–grano y el total de una
   traversa, o los tipos de contacto con sus %: la proximidad y la clase aparecen enseguida. **Ayuda de
   empaquetamiento…** muestra tres empaquetamientos ILUSTRATIVOS, uno por clase, cada uno con su proximidad contada.

## Opciones

| Campo | Valores |
|---|---|
| Polos de McBride | Q = cuarzo, cuarcita y chert; F = feldespatos; R = otros fragmentos de roca (incluidos los plutónicos y los carbonáticos) |
| Grupo de Bramkamp & Powers | 1 caliza de grano fino, 2 caliza calcarenítica, 3 calcarenita, 5 carbonato clástico grueso; 4 dolomía cristalina (obliterada) |
| Símbolo | grupo · grado (1 moderado, 2 fuerte, 3 relicto) · porosidad (A, B, C) · alteración (R, D, A, S, X) |
| Clases de empaquetamiento | suelto P < 40 %, normal 40–55 % (ambos límites incluidos), cerrado P > 55 % |

## Cómo funciona

* **McBride (1963)** usa los límites de Folk (1954): cuarzoarenita por encima de 95 % de Q; las líneas F = 25 % y
  R = 25 % salen de los puntos de 75 % de los lados, y F = 10 %, R = 10 % de los puntos de 10 % de la base; subarcosa
  lítica donde F y R están ambos entre 10 y 25 %; F:R = 1:1 divide el resto (McBride 1963, fig. 1 y p. 666–667).
* **Bramkamp & Powers (1958)**: grupo 1 cuando los fragmentos carbonáticos clásticos de tamaño arena o mayores son
  menos de 10 %; grupo 2 por encima con al menos 10 % de matriz fina original; grupos 3 y 5 con menos de 10 % de
  matriz, separados por los fragmentos mayores que arena. Las columnas de alteración de su Tabla 2: < 10 % de
  dolomita recristalizado, > 10 % de dolomita porfiroblástica (moderado), 10–75 % dolomítico y > 75 % relicto
  (fuerte); obliterado es el grupo 4. La facies: impura con arcilla y limo, arenosa con granos detríticos (desde 1 %
  de los sólidos). Los porcentajes son de los sólidos.
* **Empaquetamiento**: proximidad de Kahn P = contactos grano–grano ÷ todos los contactos de los granos cruzados × 100
  (Kahn 1956); sin conteo, la misma razón por los tipos de contacto (todos menos "flotante"). Los límites de las
  clases son los de Bocardi (2005, p. 31) y Menezes Filho (2015, p. 40). Las figuras de la ayuda las calcula
  RockFace: un empaquetamiento de granos redondos cuyos radios crecen hasta que la proximidad, contada en traversas
  horizontales como describe Kahn, cae en la clase.

## Desde un script

```python
d = prj["ILL-TS-001"]
d.classify("mcbride1963", label=True)
c = prj["ILL-CB-001"]
c.carbonate.bp_texture, c.carbonate.bp_porosity = "moderate", "B"
c.save()
c.classify("bramkamp_powers1958", label=True), c.symbol()   # (…, '21BD')
d.packing()                                           # {'proximity': 62.0, 'density': …, 'class': 'tight'}
rf.packing_class(47)                                  # 'normal'
```

## Límites y problemas comunes

* McBride no dice dónde van los fragmentos plutónicos gruesos: RockFace los cuenta como fragmentos de roca (Folk 1980
  los cuenta como feldespato) y lo indica junto al diagrama.
* La porosidad visual A/B/C de Bramkamp & Powers no tiene números en el artículo: elíjala por sus criterios (la ayuda
  del campo los resume). Mientras no se elija, el símbolo muestra "?".
* Bramkamp & Powers se aplica cuando los carbonatos son más de la mitad de los sólidos.

## Cobertura

P14 (clases de empaquetamiento y ayuda visual), P29 y M3 (McBride), P32 (Bramkamp & Powers).
