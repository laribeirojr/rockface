# Consistencia entre escalas

## Para qué sirve

La misma muestra se mide en varias escalas: la lámina en el microscopio, el tapón en el laboratorio, el volumen de
micro-CT, el perfil del pozo a su profundidad. Cada uno ve la roca de una manera, y todos deberían contar una
historia coherente — junto con la secuencia paragenética que escribió el petrógrafo. La pestaña **Consistencia** las
compara y dice, para cada verificación, si los números concuerdan, si difieren como la descripción lo explica o si se
contradicen — y qué revisar.

## Antes de empezar

Las verificaciones usan lo que el proyecto ya tiene; cada una solo se ejecuta con sus datos:

* la **composición** (porosidad, IGV, cementos, arcillas) — Petro → Composición;
* la **porosidad y la permeabilidad del tapón** — Petro → Análisis, *Petrofísica convencional*;
* un **volumen de micro-CT segmentado** de la muestra con su porosidad, o un mapa de microporosidad — RockFace MC;
* una **curva de porosidad** (PHIT, PHIE, NPHI, DPHI…) del pozo de la muestra que cubra su profundidad — RockFace MC
  → perfiles;
* el **tamaño de grano y la selección** — Petro → Microscópica (o Macroscópica);
* la **secuencia paragenética** con sus regímenes — Petro → Diagénesis.

## Paso a paso

1. Abra una descripción y la pestaña **Consistencia** (la última).
2. Lea la tabla: cada verificación, su resultado y la explicación. Pase el ratón sobre la explicación para ver sus
   referencias.
   * **Consistente** — los números concuerdan;
   * **Explicado** — difieren como la descripción dice que deberían (el tapón ve la microporosidad de las arcillas
     descritas, por ejemplo);
   * **A revisar** — una diferencia que nada en la descripción explica;
   * **Inconsistente** — los datos se contradicen;
   * **Sin datos** — lo que falta para ejecutar la verificación.
3. **Verificar de nuevo** después de editar la descripción (la pestaña sigue la composición y la descripción
   microscópica en pantalla).
4. **Preguntar a Mio** envía *"¿La muestra … es consistente?"* a Mio; también responde *"¿qué muestras son
   inconsistentes?"* para todo el proyecto.
5. Los **informes** tienen la sección *Consistencia* con las verificaciones que tienen datos y sus referencias.

## Las verificaciones

| Verificación | Qué compara | Resultado |
|---|---|---|
| Porosidad: lámina × tapón | La porosidad del conteo (con su incertidumbre) y la del tapón | Lámina por encima del tapón más allá de la incertidumbre: *inconsistente* (poros hechos en la preparación, otra lámina, tapón y lámina de lugares distintos). Tapón más de 5 puntos por encima: *explicado* si se describen arcillas, matriz, micrita o microporosidad, *a revisar* si no (Halley 1978) |
| Porosidad: micro-CT | La porosidad resuelta de un volumen segmentado (o el total de un mapa de microporosidad) y el tapón — la lámina si no hay tapón | Más de 3 puntos por encima: *inconsistente* (umbral de segmentación); más de 5 por debajo: *explicado* (poros menores que el vóxel; Andrä et al. 2013) |
| Porosidad: perfil de pozo | La curva de porosidad a la profundidad de la muestra y el tapón (o la lámina) | Más de 5 puntos de diferencia: *a revisar* (desfase de profundidad, capas finas, correcciones del perfil) |
| Volumen intergranular (IGV) | El IGV de una arenisca | Más de 45 %: *inconsistente* — más que la arena recién depositada (Beard & Weyl 1973; Lundegard 1992). Menos de 26 %: *explicado* por 10 % o más de granos dúctiles o por contactos cóncavo-convexos o suturados, *a revisar* si no (Paxton et al. 2002; Pittman & Larese 1991) |
| Cemento temprano × compactación | Cemento eodiagenético e IGV | 10 % o más de cemento temprano con IGV menor de 28 %: *inconsistente*; IGV de 35 % o más sin cemento temprano ni matriz: *a revisar* |
| Secuencia paragenética | Relaciones y regímenes de las fases | Relaciones contradictorias, o un régimen posterior antes de uno anterior: *inconsistente* |
| Permeabilidad × textura | La permeabilidad del tapón y la estimación de Berg (1970) por la porosidad, el tamaño de grano mediano y la selección | Dentro de un factor 10: *consistente*; 10 veces menor: *explicado* por arcillas, cementos o microporosidad, *a revisar* si no; 10 veces mayor: *explicado* por fracturas, *a revisar* si no |

## Cómo funciona

* La porosidad de la lámina lleva la incertidumbre del conteo de los puntos contados (vea *Qué tan seguro es el
  conteo de puntos*): una diferencia dentro de ella nunca se llama inconsistente.
* Estimación de Berg (1970): k (mD) = 1000 × 5,1×10⁻⁶ φ^5,1 d² e^(−1,385 p), con φ en %, d el tamaño de grano mediano
  en mm y p = P90 − P10 = 2,563 σ (selección de Folk & Ward, unidades φ). Si la selección no está descrita se supone
  una arena moderadamente seleccionada (σ = 0,85) y se dice.
* Una roca se trata como carbonática cuando sus granos carbonáticos y su lodo calcáreo superan a los granos
  extracuencales: las verificaciones de IGV no se aplican.
* El valor del perfil es la muestra de la curva más cercana a la profundidad corregida (o al tope); una curva en v/v
  se lee en %.

## Desde un script

```python
rep = prj["ILL-TS-001"].consistency()
rep["status"]                                   # "ok", "explained", "check", "inconsistent" o "no_data"
[(c["code"], c["status"]) for c in rep["checks"]]
for r in prj.consistency():                     # todas las descripciones, primero las que piden atención
    print(r["name"], r["status"])
rf.berg_permeability(19.4, 0.18, 0.42)          # 138 mD
```

## Límites y problemas comunes

* Los umbrales son reglas prácticas de la literatura, no leyes: un *a revisar* es una pregunta al petrógrafo, no un
  error.
* La ecuación de Berg se dedujo para arenas limpias de 30 a 40 % de porosidad; para areniscas cementadas léala como
  un orden de magnitud — de ahí el factor 10.
* La DRX de roca total no se compara con el conteo (porcentajes en peso y en volumen, y las fases finas que el
  microscopio no resuelve, difieren demasiado para una regla simple).
* Los límites del IGV son para areniscas de granos rígidos; las rocas muy gruesas, muy mal seleccionadas o ricas en
  matriz parten de una porosidad deposicional menor.

## Cobertura

O8 (pedido del propietario del 17/11/2026: las innovaciones, la segunda).

Referencias: Halley (1978), https://doi.org/10.1306/212F7504-2B24-11D7-8648000102C1865D; Andrä et al. (2013),
https://doi.org/10.1016/j.cageo.2012.09.005; Beard & Weyl (1973); Lundegard (1992),
https://doi.org/10.1306/D42678D4-2B26-11D7-8648000102C1865D; Paxton et al. (2002); Pittman & Larese (1991),
https://doi.org/10.1306/0C9B292F-1710-11D7-8645000102C1865D; Berg (1970); Nelson (1994).
