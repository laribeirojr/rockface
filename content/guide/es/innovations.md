# Las seis innovaciones

## Para qué sirve

Además de las funciones de los programas de referencia, RockFace trae seis innovaciones de método, una por versión de
la 1.0.0rc4 a la 1.0.0rc9, de la más simple a la más audaz. Esta página dice qué hace cada una, dónde está en los
programas y cómo se verificó; cada una tiene su página.

| # | Innovación | Versión · dónde | Qué le da al petrógrafo |
|---|---|---|---|
| 1 | [Qué tan seguro es el conteo de puntos](counting_uncertainty.md) | 1.0.0rc4 · Petro | El intervalo de 95 % de cada constituyente contado, la probabilidad de cada campo de las clasificaciones, la región de confianza en el diagrama ternario y cuántos puntos faltan |
| 2 | [Consistencia entre escalas](consistency.md) | 1.0.0rc5 · Petro, MC, Lab | Siete verificaciones entre lámina, plug, micro-CT, perfil y secuencia paragenética, cada contradicción explicada con su fuente |
| 3 | [Dictado en el microscopio](dictation.md) | 1.0.0rc6 · Petro, Mio | Dictar la descripción y contar por voz sin dejar el ocular; reconocimiento en la propia computadora |
| 4 | [Conteo de puntos asistido por IA](assisted_counting.md) | 1.0.0rc7 · Petro | Un modelo que aprende de los puntos contados y propone los siguientes, los más inciertos primero, con una coincidencia honesta |
| 5 | [Mio mira la imagen](mio_vision.md) | 1.0.0rc8 · Mio, Atlas | Un modelo de visión en la tarjeta gráfica del laboratorio propone la textura y el sistema poroso a partir de una fotomicrografía, cada propuesta con cuántas respuestas coinciden |
| 6 | [Aprendizaje federado entre laboratorios](federated_learning.md) | 1.0.0rc9 · Petro | Laboratorios entrenan juntos un modelo del conteo; solo los números del modelo salen de cada uno |

## Paso a paso

1. **Qué tan seguro es el conteo**: Composición → la columna *Intervalo de 95 %*; Clasificación → *Probabilidad*; el
   diagrama ternario → *Región de confianza*; la pestaña Conteo de puntos dice cuándo la clasificación es estable.
2. **Consistencia**: la pestaña *Consistencia* de una descripción, o Mio: *"¿es consistente ILL-TS-001?"*.
3. **Dictado**: Inicio → **Dictar**; en la pestaña Conteo de puntos, el botón del micrófono.
4. **Conteo asistido**: pestaña Conteo de puntos → **Proponer el constituyente (IA)**; Enter acepta.
5. **Mio mira**: Inicio → **Mio mira** (un modelo de visión en la computadora, elegido en *Modelos de visión…*).
6. **Aprendizaje federado**: Herramientas → **Aprendizaje federado**; en la pestaña Conteo de puntos, **Modelo
   compartido**.

## Cómo funciona

Las seis siguen los mismos principios:

* **Local.** Todo corre en la computadora del usuario — las estadísticas, el reconocimiento de voz, el modelo de
  visión, el modelo del conteo; en una federación solo salen los números del modelo, en un archivo que el laboratorio
  lee antes.
* **El petrógrafo decide.** El programa propone y dice qué tan seguro está; nada se graba hasta que el petrógrafo lo
  acepta, y los puntos a ciegas miden la coincidencia sin el sesgo de ver la propuesta antes.
* **Medido.** Cada innovación tiene criterio de aceptación y pruebas automáticas: los intervalos cubren el 95 % por
  simulación; todos los ejemplos de la guía del dictado se entienden en los tres idiomas; 91 % de los puntos
  restantes correctos tras 75 contados por los más inciertos, contra 81 % en el orden de la malla; un modelo federado
  acierta 83 % en un laboratorio que no participó, contra 79 % de cada laboratorio solo (datos ILLUSTRATIVE).
* **Con fuentes.** Cada versión empezó con un relevamiento de la literatura y de las patentes; las referencias están
  en cada página, las notas de patentes en la auditoría de licencias. La búsqueda de láminas parecidas en una
  biblioteca (innovación 5) quedó fuera por decisión del propietario, hasta una consulta de patentes.

## Desde un script

```python
d = prj["ILL-TS-002"]
d.uncertainty()                 # 1 · intervalos y probabilidades
d.consistency()                 # 2 · las verificaciones entre escalas
d.dictate("moderadamente seleccionado, granos subredondeados", "es")   # 3 · propuestas a partir de texto
d.assist(top=5)                 # 4 · propuestas de la IA del conteo
d.look(samples=3)               # 5 · lo que propone el modelo de visión
prj.federated_update("fed-r1.rffed", "lab.rfupd", site="Lab A")   # 6 · la actualización de este laboratorio
```

## Límites y problemas comunes

* Las propuestas de 3 a 6 son propuestas: cada página dice cómo se midieron y dónde pueden fallar.
* El modelo de visión (5) se probó con respuestas guionadas; su acierto en láminas reales aún se medirá.
* El aprendizaje federado (6) protege los datos, no todo rastro de ellos en el modelo: su página dice qué hacen y qué
  no hacen el recorte y el ruido.

## Cobertura

O8 (pedido del propietario del 2026-11-17: "Gostei de todas elas. Podemos implementar da mais simples para a mais
ousada?").
