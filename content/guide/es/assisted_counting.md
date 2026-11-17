# Conteo de puntos asistido por IA

## Para qué sirve

La mayor parte de los puntos de un conteo es fácil: el mismo cuarzo, la misma resina de los poros, una y otra vez. El
asistente de IA los aprende de los puntos que usted cuenta y propone la línea del punto siguiente; usted confirma con
**Enter** o cuenta otra línea. Cada confirmación o corrección enseña al modelo al instante, así que tras unas decenas
de puntos la mayoría de las propuestas son correctas y el conteo avanza más rápido — y cada punto lo sigue decidiendo
usted.

## Antes de empezar

* Una **malla** sobre la **imagen** del conteo (Conteo de puntos → Imagen y calibración: *Imagen de la lámina…*, luego *Crear malla*).
* Si quiere, la **imagen con nícoles cruzados** del mismo campo, del mismo tamaño y encuadre (*Imagen con nícoles
  cruzados…*): el modelo aprende también los colores de interferencia.
* Las bibliotecas de IA del programa (`rockface[lab]`, en las dos ediciones de los instaladores).

## Paso a paso

1. Cuente los primeros puntos como siempre — al menos **15 puntos de dos líneas o más**.
2. Marque **Proponer el constituyente (IA)**. Bajo los botones del conteo aparece la propuesta para el punto actual:
   *IA: Cuarzo monocristalino — 92 %*, y las líneas siguientes con sus probabilidades.
3. Pulse **Enter** (o *Aceptar*) cuando la propuesta sea correcta; cuente otra línea (teclado, lista, voz) cuando no
   lo sea. El modelo aprende de nuevo tras cada punto.
4. **Verificación a ciegas**: más o menos un punto de cada diez muestra *Verificación a ciegas: cuente este punto sin
   propuesta*. Son siempre los mismos puntos; en ellos usted cuenta sin ver la propuesta, y la concordancia medida
   allí es honesta.
5. Marque **Primero los puntos más inciertos** para que el modelo elija el punto siguiente: aquel en que está menos
   seguro. Allí aprende más rápido. **Cuente después todos los puntos** de la malla — un conteo detenido a medias así
   no es una muestra aleatoria de la lámina, y la pestaña lo avisa.
6. Lea la línea de abajo: los puntos del modelo y su exactitud fuera de bolsa, su **concordancia** con las propuestas
   y la concordancia en los puntos **a ciegas**, con su intervalo del 95 %.

**Mio**: *"¿qué tal la IA en el conteo de ILL-TS-002?"* da la concordancia, la de los puntos a ciegas y las
correcciones más frecuentes.

## Cómo funciona

* **Lo que ve el modelo.** Alrededor de cada punto, tres ventanas de la imagen: el retículo (3 × 3 píxeles), el grano
  bajo él (30 µm) y su entorno (90 µm). En cada una: media y dispersión del rojo, verde y azul, saturación, brillo,
  matiz, los percentiles 10, 50 y 90 del brillo, el gradiente medio (textura, relieve) y cuán azul es (resina de los
  poros) — 45 números, 90 con la imagen de nícoles cruzados.
* **El modelo** es un bosque aleatorio (Breiman 2001), el mismo de RockFace Lab, entrenado con los puntos contados; la
  fracción de sus árboles que vota por una línea es la probabilidad de la propuesta. Se entrena de nuevo cada vez que
  cambian los puntos contados — una fracción de segundo.
* **Aprendizaje activo.** El *margen* entre las dos líneas más probables mide la duda; *primero los más inciertos*
  visita el punto de menor margen (muestreo por incertidumbre, Settles 2009).
* **Medido en una lámina ILLUSTRATIVE con textura** (la roca sintética de la guía, PP y XP, 300 puntos): con 15 puntos
  contados las propuestas acertaban el 54 % de los puntos aún por contar; con 60 más, el 81 % visitando la malla en
  orden y el **91 % visitando primero los más inciertos**. En la lámina de colores lisos del ejemplo (ILL-TS-002),
  entrenada con 100 puntos, el 94,5 % de los otros 200 eran correctos.
* **Por qué puntos a ciegas.** Las personas siguen consejos automáticos aun cuando son erróneos (*sesgo de
  automatización*, Goddard et al. 2012); la concordancia medida en puntos cuya propuesta usted vio queda inflada por
  ello. Los puntos a ciegas, con la propuesta oculta, miden el modelo tal como es. Cada punto contado guarda lo que se
  propuso, su probabilidad y si era a ciegas.

## Desde un script

```python
d = prj["ILL-TS-002"]
r = d.assist(top=10)              # los diez puntos aún no contados más inciertos
r["ready"], r["trained_on"], r["oob"]
[(q["index"], q["uid"], round(q["p"], 2)) for q in r["proposals"]]
d.set_crossed_image("ILL-TS-002-xpl.png")    # el mismo campo con nícoles cruzados
d.ai_agreement()                  # {"proposed", "agreed", "rate", "blind", "blind_rate", "interval", ...}
```

Los scripts solo leen las propuestas: quien cuenta es el petrógrafo.

## Límites y problemas comunes

* El modelo conoce solo esta lámina y las líneas contadas en ella: aprende desde cero en cada conteo, así que los
  primeros puntos siempre se cuentan a mano. Un constituyente raro, visto una o dos veces, rara vez se propone —
  cuéntelo usted.
* Las propuestas dependen de la imagen: desenfocada, con luz desigual o con un aumento distinto del de los puntos
  contados, empeoran. Los puntos fuera de la imagen no tienen propuesta.
* La imagen debe estar calibrada (µm por píxel) para que las ventanas tengan su tamaño real.
* Visitar primero los puntos inciertos cambia el orden, no la malla: úselo solo si va a contar todos los puntos.
* El modelo no viene listo ni preentrenado con otras rocas; el banco LITHOS (Chacón et al. 2025, 25 clases de
  minerales) es no comercial y se usó solo para leer sobre el estado del arte.

## Cobertura

O8 (pedido del dueño del 2026-11-17: las innovaciones, la cuarta).

Referencias: Breiman (2001), https://doi.org/10.1023/A:1010933404324; Settles (2009), Active learning literature
survey, Univ. Wisconsin–Madison TR 1648; Tang, Milliken y Spikes (2020), https://doi.org/10.1016/j.marpetgeo.2020.104518;
Chacón et al. (2025), Towards automated petrography, arXiv:2511.00328; Goddard, Roudsari y Wyatt (2012),
https://doi.org/10.1136/amiajnl-2011-000089.
