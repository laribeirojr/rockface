# Qué tan seguro es el conteo de puntos

## Para qué sirve

Un conteo de 300 puntos no da la composición, la estima: contada de nuevo, la misma lámina daría porcentajes un
poco distintos, y una roca cerca de un límite de clasificación podría caer en el campo vecino. RockFace muestra esta
**incertidumbre del conteo** donde se usan los números:

* el **intervalo de 95 %** de cada línea contada de la composición;
* la **probabilidad** del campo de cada clasificación ternaria (Folk, McBride, Dickinson);
* la **región de confianza** del punto en el diagrama ternario;
* durante el conteo, si la clasificación ya es **estable** o **cuántos puntos más** necesita.

## Antes de empezar

* Una descripción con **puntos contados** (Petro → Conteo de puntos, o puntos escritos en la pestaña Composición).
  Las líneas con % manual o cantidad nominal no tienen incertidumbre del conteo y entran como están.
* Para las probabilidades: una arenisca (o cualquier roca) que una clasificación ternaria ubique.

## Paso a paso

1. **Petro → Composición.** La columna **Intervalo 95 %** da, para cada línea contada, el rango de porcentajes de la
   roca que el conteo sostiene; la ayuda emergente dice cómo se calculó.
2. **Petro → Conteo de puntos.** Bajo los puntos contados, una línea como *Folk (1980): Subarcosa 97 % — estable* o
   *… 81 % — unos 240 puntos más para 95 %* dice si ya se puede dejar de contar. *Cerca de un límite* significa que
   más puntos no decidirán el campo: la roca está de verdad entre dos campos.
3. **Petro → Clasificación.** La columna **Probabilidad** da la probabilidad del campo mostrado; seleccione una
   clasificación ternaria para leer la probabilidad de cada campo, y si es estable o cuántos puntos faltan.
4. **Diagrama…** dibuja la **región de confianza**: el área sombreada donde puede estar el punto con 95 % de
   confianza (una franja a lo largo de un lado cuando un polo está vacío). **Región de confianza** la apaga.
5. Los **informes** dan las probabilidades bajo las clasificaciones y dibujan las regiones en los diagramas; la
   opción **Incertidumbre del conteo de las clasificaciones** del diálogo de informe las deja fuera.

## Opciones

| Ítem | Valor |
|---|---|
| Confianza de los intervalos y de la región | 95 % |
| Una clasificación es *estable* cuando | su campo más probable tiene al menos 95 % |
| Puntos necesarios | contados de nuevo con las mismas proporciones, hasta 5000 puntos más |
| Sorteos de las probabilidades | 4000 (el mismo conteo da siempre los mismos números) |

Desde un script se pueden cambiar la confianza, el nivel de estabilidad y los sorteos.

## Cómo funciona

* **Intervalos.** Una línea contada es una proporción de los puntos contados; su intervalo es el intervalo score de
  Wilson (1927), que queda entre 0 y 100 % y mantiene su cobertura de 95 % para constituyentes raros, a diferencia
  del ± 2σ del ábaco clásico de Van der Plas & Tobi (1965) (Agresti & Coull 1998; Howarth 1998; Weltje 2002). El
  intervalo se escala a la parte de la roca que ocupan las líneas contadas.
* **Probabilidades.** Los conteos son una muestra multinomial de la roca (Chayes 1956). Dados los conteos, las
  proporciones verdaderas siguen una distribución de Dirichlet (a priori de Jeffreys, conteos + ½; Vermeesch 2005).
  RockFace sortea 4000 composiciones de ella, calcula los totales y el punto de cada clasificación exactamente como
  para la descripción y cuenta en qué campo cae cada punto.
* **Región.** Los puntos sorteados, en razones logarítmicas aditivas (Aitchison 1982; Weltje 2002), dan una región
  normal bivariada de 95 %, dibujada de vuelta en el triángulo — una elipse en razones logarítmicas, curva cerca de
  los vértices. Cuando un polo está vacío en todos los sorteos, la región es el intervalo a lo largo del lado.
* **Puntos necesarios.** Las mismas proporciones contadas con más puntos (de 1,25 a 30 veces) hasta que el campo más
  probable llegue a 95 %.

## Desde un script

```python
d = prj["ILL-TS-001"]
u = d.uncertainty()                          # confidence=0.95, stable=0.95, draws=4000
u["schemes"]["folk1980"]["probabilities"]    # {'subarkose': 0.97, 'arkose': 0.02, …}
u["schemes"]["folk1980"]["needed"]           # 0: ya estable; None: cerca de un límite
u["lines"][0]                                # {'constituent': 'quartz_mono', 'share': 48.1, 'low': 42.5, 'high': 53.8, …}
rf.wilson_interval(21, 295)                  # (4.7, 10.6) en % de los puntos contados
rf.ternary_figure("folk.png", "folk1980", prj.descriptions(), regions=True)
```

Mio también responde: *"¿qué tan segura es la clasificación de ILL-TS-002?"*, *"how sure is the classification of
ILL-TS-001?"*, *"quantos pontos faltam na ILL-TS-002?"*.

## Límites y problemas comunes

* **Solo la incertidumbre del conteo.** El error de muestreo entre láminas de la misma roca (Bayly 1965), los
  errores de identificación del petrógrafo y la incertidumbre de las cantidades manuales y nominales no se incluyen.
* El modelo supone puntos más separados que el grano mayor (Van der Plas & Tobi 1965); una malla más fina que los
  granos cuenta el mismo grano dos veces y hace que los intervalos parezcan más estrechos de lo que son.
* La composición original (antes de la diagénesis) todavía no tiene probabilidades.
* Una roca carbonática recibe los intervalos de sus líneas; las clasificaciones por reglas (Dunham, Embry & Klovan…)
  no tienen probabilidades.

## Cobertura

O8 (pedido del propietario del 17/11/2026: las innovaciones, la primera).

Referencias: Chayes (1956); Van der Plas & Tobi (1965), https://doi.org/10.2475/ajs.263.1.87; Bayly (1965); Wilson
(1927); Agresti & Coull (1998); Howarth (1998), https://doi.org/10.2475/ajs.298.7.594; Aitchison (1982); Weltje
(2002), https://doi.org/10.1016/S0012-8252(01)00076-9; Vermeesch (2005), https://doi.org/10.1029/2004JB003479;
Vermeesch (2018), https://doi.org/10.1016/j.epsl.2018.08.019.
