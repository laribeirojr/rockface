# Diagénesis: ambientes, secuencia paragenética y grafo de conocimiento

## Para qué sirve

La pestaña **Diagénesis** interpreta los ambientes diagenéticos por los que pasó la roca — marino, meteórico, árido,
lacustre alcalino, soterramiento, fluidos calientes, levantamiento — a partir de los rasgos de su descripción, cada
conclusión con las reglas y fuentes que la sostienen. También arma la **secuencia paragenética**: las fases
diagenéticas en el orden en que se formaron, con su régimen (eo-, meso- o telodiagénesis). El petrógrafo confirma o
rechaza cada ambiente y puede reordenar la secuencia a mano.

## Antes de empezar

Una descripción cuya composición tenga constituyentes diagenéticos, de preferencia con sus hábitos, localizaciones y
relaciones paragenéticas (cubre, reemplaza, posterior a…) (página [Composición](composition.md)).

## Paso a paso

### Los ambientes

1. Abra la pestaña **Diagénesis**.
2. **Ambientes diagenéticos** lista cada **Ambiente** con su **Régimen** y el **Resultado**:
   * *Interpretado* — se encontró una regla indicativa o dos reglas de apoyo distintas;
   * *Alguna evidencia* — una regla de apoyo;
   * vacío — "Ninguna evidencia de este ambiente en la descripción."
3. Seleccione un ambiente para ver las reglas **Encontrado**: el rasgo de la descripción, la regla y su fuente.
4. En **Petrógrafo**, **confirme** o **rechace**; su decisión prevalece sobre el resultado automático. Escriba una
   **Nota sobre este ambiente** si hace falta.
5. **Interpretación diagenética — notas**: la interpretación general en sus palabras.

### La secuencia paragenética

1. **Secuencia paragenética** muestra las fases en orden, cada una con su **Paso**, **Fase** (precipitación o
   disolución de un constituyente) y **Régimen**, y el gráfico de la secuencia.
2. El orden viene de las relaciones paragenéticas de la composición; el régimen, de las reglas. Las contradicciones se
   informan: "Relaciones contradictorias entre … y …: quedan fuera del orden", "… viene antes que … pero pertenece a
   un régimen posterior".
3. **Subir** y **Bajar** mueven una fase; el régimen se puede cambiar en su celda. **Automático** devuelve el orden
   calculado por RockFace.
4. **Exportar imagen…** guarda el gráfico.
5. **Guardar** (Ctrl+S): la interpretación forma parte de la descripción.

### El grafo de conocimiento

1. **Grafo de conocimiento…** (en la pestaña, o en Herramientas → Base de conocimiento → **Grafo de conocimiento**).
2. El grafo une los rasgos de una descripción → las reglas → los ambientes → los regímenes. Las líneas continuas son
   reglas indicativas, las discontinuas reglas de apoyo; las reglas encontradas en la descripción abierta están en
   azul.
3. En **Ambiente**, elija uno para ver solo su parte del grafo, o **(todos los ambientes)**. **Exportar imagen…** lo
   guarda.

## Opciones

| Campo | Qué cambia |
|---|---|
| Petrógrafo | Confirmado o rechazado: reemplaza el resultado automático en informes, consultas y figuras. |
| Subir, Bajar, celda del régimen | La secuencia fijada a mano (guardada con la descripción). |
| Automático | Vuelve al orden y a los regímenes encontrados por RockFace. |

## Cómo funciona

* Las reglas son propias de RockFace, cada una tomada de la literatura publicada: Morad et al. (2000, 2010), Worden y
  Burley (2003), Longman (1980), Flügel (2010), Scholle y Ulmer-Scholle (2003), Radke y Mathis (1980), Tosca y Wright
  (2018), Paxton et al. (2002), Schmidt y McDonald (1979), Taylor (1950), Park y Schot (1968).
* Un ambiente es *interpretado* con una regla indicativa o dos reglas de apoyo distintas, y tiene *alguna evidencia*
  con una regla de apoyo. Esa agregación está declarada en el programa y en `docs/NOMENCLATURE.md`; la decisión del
  petrógrafo siempre prevalece.
* El orden de las fases es un ordenamiento topológico de las relaciones; las relaciones que se contradicen quedan
  fuera y se informan.
* RockFace Explorer dibuja la evolución paragenética de varias muestras juntas (página [Evolución paragenética y la columna estratigráfica](evolution_column.md)).

## Desde un script

```python
d = prj["TS-9"]
for code, r in d.interpret().items():
    print(code, r["status"], r["regime"], r["rules"])          # p. ej. meso_burial interpreted meso ['albitization']
d.diagenesis.decisions["eo_marine"] = "confirmed"
d.save()
for step in d.paragenesis():
    print(step["step"], step["phase"], step["kind"], step["regime"])
rf.paragenesis_figure("secuencia.png", d)
rf.knowledge_graph("grafo.svg", environment="meso_burial")      # también .png, o .dot para el grafo entero
```

## Límites y problemas comunes

* "Ninguna fase diagenética en la composición." — añada primero constituyentes diagenéticos.
* Sin relaciones paragenéticas las fases no tienen orden: dé las relaciones en la composición (cubre, reemplaza,
  posterior a, rellena disolución de…).
* El archivo DOT del grafo de conocimiento (para Graphviz) se escribe solo para el grafo entero.

## Cobertura

P33 (interpretación de los ambientes diagenéticos), P40 (grafo de conocimiento), L8 (generador de la secuencia
paragenética).
