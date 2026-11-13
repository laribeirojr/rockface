# Sistema poroso

## Para qué sirve

La pestaña **Sistema poroso** registra la porosidad visual de la lámina y los tipos de poro que la componen, cada uno
con su fracción, tamaño y modificador. Los tipos de poro son los de Choquette y Pray (1970) para carbonatos y los de
las clasificaciones de poros de areniscas, tomados de la base de conocimiento.

## Antes de empezar

Una descripción abierta. La porosidad de la resina azul medida en una imagen (RockFace Lab) o los puntos contados
(pestaña Conteo de puntos) pueden servir de porosidad visual.

## Paso a paso

1. Abra la pestaña **Sistema poroso**.
2. **Porosidad** — escriba la **Porosidad visual (%)**. La suma de los tipos se muestra al lado.
3. **Tipos de poro** — hasta ocho filas. Para cada una:
   * **Tipo** — los poros selectivos de fábrica de Choquette y Pray (interpartícula, intrapartícula, intercristalino,
     móldico, fenestral, de abrigo, de armazón de crecimiento), los no selectivos de fábrica (fractura, canal,
     vúgulo, caverna) y los que pueden ser una u otra cosa (brecha, perforación, madriguera, contracción), y los poros
     de areniscas (intergranular primario y secundario, disolución intragranular, sobredimensionado,
     microporosidad);
   * **%** — su fracción del volumen de la roca;
   * **mm** — un tamaño típico, o la clase de **Tamaño de poro** (la clase sigue a un tamaño escrito);
   * **Modificador** — un modificador de la base de conocimiento que se aplica a poros.
4. **Notas** y luego **Guardar** (Ctrl+S).

## Opciones

| Campo | Regla |
|---|---|
| Porosidad visual | 0–100 %. |
| Tipos de poro | Como máximo ocho, sin repetir; cada uno 0–100 %. |
| Suma de los tipos | Comparada con la porosidad visual: más o menos que ella da un aviso. |

## Cómo funciona

Los tipos de poro y sus modificadores son términos de RockFace tomados de la literatura publicada (Choquette y Pray
1970 para carbonatos; los tipos de poro de areniscas según Schmidt y McDonald 1979 y Pettijohn et al. 1987). Las
clases de tamaño de poro son los microporos (< 1/16 mm), mesoporos pequeños y grandes (hasta 4 mm) y megaporos
pequeños y grandes (hasta 256 mm) de Choquette y Pray. Los tipos de poro contados como puntos en la composición (tipo
*poro*) son un registro aparte: el Sistema poroso es la síntesis del petrógrafo.

## Desde un script

```python
from rockface.core import texture as tx
d = prj["TS-9"]
d.pores.total_porosity = 18.0
d.pores.pores = [tx.Pore("interparticle", 12.0, size_mm=0.15), tx.Pore("moldic", 6.0)]
d.save()
```

## Límites y problemas comunes

* "Los tipos de poro suman … %, más que la porosidad visual (… %)." — un aviso: revise las fracciones.
* "… debe estar entre 0 y 100 %."
* Un código de tipo de poro o de modificador desconocido (de un script o de un archivo antiguo) se rechaza con "Valor
  desconocido …".

## Cobertura

P17 (descripción del sistema poroso).
