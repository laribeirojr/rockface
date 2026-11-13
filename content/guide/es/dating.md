# Datación U-Pb en el diagrama de Tera-Wasserburg

## Para qué sirve

Los puntos U-Pb de un mineral diagenético (un cemento de calcita, una dolomita) medidos en varias muestras se datan
juntos: RockFace Explorer los grafica en el **diagrama de Tera-Wasserburg**, ajusta la recta de la regresión de York y
da la edad en su intercepto inferior con la concordia, con su incertidumbre, el MSWD y la probabilidad del ajuste. La
edad queda en el proyecto con la fase que data, y se ubica en la evolución paragenética y en la columna estratigráfica.

## Antes de empezar

* Análisis puntuales U-Pb en las láminas (página [Análisis puntuales: geoquímica, datación e inclusiones fluidas](spot_analyses.md)): tipo *datación* (o sistema "U-Pb") con
  ²³⁸U/²⁰⁶Pb y ²⁰⁷Pb/²⁰⁶Pb, sus incertidumbres y la correlación de los errores (rho).
* Una consulta en Explorer que encuentre las muestras a datar juntas (por ejemplo, una formación).

## Paso a paso

1. En RockFace Explorer, abra la pestaña **Datación U-Pb**.
2. **Descripciones con puntos U-Pb (de la consulta)** lista las muestras encontradas que tienen puntos U-Pb.
3. **Mineral datado**: el constituyente (o grupo) cuyos puntos se usan, o **Todos los minerales**.
4. **Regresión**:
   * **Libre (York)** — la recta por los puntos;
   * **Anclada al Pb común de Stacey & Kramers (1975)** — el ²⁰⁷Pb/²⁰⁶Pb inicial del modelo a la edad encontrada;
   * **Anclada a un ²⁰⁷Pb/²⁰⁶Pb inicial dado** — escriba el **²⁰⁷Pb/²⁰⁶Pb inicial** y el **Error del ancla**.
5. La tabla lista todos los puntos; desmarque **Punto (usado)** para sacar un punto de la regresión (queda en el
   diagrama, marcado).
6. El diagrama muestra los puntos con sus elipses de error, la concordia con sus edades, la recta de la regresión y el
   resultado: "Edad = … ± … Ma (2σ)", "± … Ma (conf. 95 %)", el MSWD, n y el ²⁰⁷Pb/²⁰⁶Pb inicial.
7. **Exportar diagrama…** lo guarda (PNG, SVG, PDF).
8. **Guardar edad…**: dé un nombre; queda con la fase que data (mineral y hábito). **Edades del proyecto (doble clic
   abre)** lista las edades guardadas; **Eliminar edad**.

## Opciones

| Opción | Qué cambia |
|---|---|
| Mineral datado | Qué puntos se usan. |
| Regresión | Libre, anclada al plomo común de Stacey & Kramers, o anclada a un valor dado con su error. |
| Punto (usado) | Saca un punto anómalo del ajuste. |

## Cómo funciona

* Regresión de York con errores correlacionados en las dos coordenadas (York et al. 2004); la edad es el intercepto
  inferior de la recta con la concordia de Tera-Wasserburg (constantes de decaimiento de Jaffey et al. 1971,
  ²³⁸U/²³⁵U de Hiess et al. 2012). El ajuste anclado fuerza la recta por el ²⁰⁷Pb/²⁰⁶Pb inicial (Stacey & Kramers
  1975, o el valor dado).
* La incertidumbre se da en 2σ (analítica) y como intervalo del 95 %: t(n−2) × σ × √MSWD cuando MSWD > 1, si no 1,96σ
  (Ludwig 2003); no se incluyen los errores de las constantes de decaimiento. MSWD = χ²/(n − 2) (Wendt y Carl 1991),
  con la probabilidad del ajuste.
* Comprobado con valores publicados: los datos de Pearson con los pesos de York dan la pendiente, el intercepto y los
  errores publicados; en 800 conjuntos sintéticos el intervalo del 95 % contiene la edad verdadera el 97,2 % (libre) y
  el 97,5 % (anclada) de las veces.

## Desde un script

```python
d = prj.date(formation="Example Formation", constituent="calcite_dia", anchor="stacey_kramers", figure="tw.pdf")
print(f"{d.age:.1f} ± {d.age_2s:.1f} Ma (2σ), MSWD {d.mswd:.2f}, n = {d.n}")
prj.save_age("Calcita de la arenisca", ("identification", "formation", "Example Formation"),
             constituent="calcite_dia", habit="poikilotopic", anchor="stacey_kramers")
print(prj.ages())
```

## Límites y problemas comunes

* "Sin edad: …" — pocos puntos, o "La recta no corta la concordia."
* "Ninguna edad que guardar: date puntos primero."
* Los puntos sin rho se toman como no correlacionados (rho = 0).

## Cobertura

L12 (datación U-Pb, Tera-Wasserburg; edades en la estratigrafía).
