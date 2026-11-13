# Totals

## What it is for

A **total** adds up the composition lines of one kind: all the quartz, the feldspars, the intergranular cement, the
dissolution porosity, the bioclasts… RockFace has 50 built-in totals and the compaction measures IGV, COPL, CEPL and
ICOMPACT, worked out on the present composition and on the **original** one (before diagenesis). A project can add
its own totals. The classifications, figures, queries and LAS curves use them.

## Before you start

A description with its composition (page [Composition](composition.md)).

## Step by step

### Reading the totals

1. Open the **Classification** tab. The **Totals** table is on the left.
2. Each row gives a total in % of the rock volume, in two columns:
   * **Present** — from the composition as described;
   * **Original** — from the composition before diagenesis: the share of each replacive or dissolution line is
     given back to the constituent it replaced or dissolved.
3. The totals are written automatically with the description: no button to press.

### A custom total

1. **Custom totals…** opens **Custom totals of the project**.
2. **New**, then give the total a **Code** and a name.
3. Add **Conditions**: a line is picked when it matches every column of one condition — kind, group, constituent,
   location, habit, modifier, relation. Double-click a cell to choose codes: checked means *include*, partly
   checked means *exclude*; an empty cell (*any*) accepts anything. **Add condition**, **Remove condition**.
4. **In this description: … %** shows the result at once.
5. **OK**. The total appears, marked *custom*, in every description of the project.

## Options

The built-in totals include:

| Group | Totals |
|---|---|
| Whole rock | volume, primary, diagenetic, porosity, framework grains |
| Origin | extrabasinal, intrabasinal, non-carbonate intrabasinal (Zuffa 1980) |
| Provenance | Qm, Qp, chert, quartz, Qt, feldspars, K-feldspars, plagioclase, rock fragments by kind, L, Lt (Dickinson 1985) |
| Others | micas, heavy minerals, matrix, depositional matrix |
| Carbonates | non-skeletal grains, bioclasts, pre-salt constituents, allochems, lime mud, dolomite, carbonates, evaporites |
| Diagenesis | cements (all, intergranular, silica, carbonate, clay, sulphate), diagenetic feldspar, replacive, displacive |
| Pores | intergranular, intragranular and moldic, dissolution, fracture, microporosity |
| Compaction | IGV, COPL, CEPL, ICOMPACT |

## How it works

* A total sums the percentages of the lines picked by any of its conditions.
* IGV = intergranular porosity + intergranular cement + depositional matrix (Paxton et al. 2002).
* COPL = Pi − ((100 − Pi) × IGV) / (100 − IGV) and CEPL = (Pi − COPL) × C / IGV, with Pi = 40 % (Lundegard 1992);
  ICOMPACT = COPL / (COPL + CEPL) (Ehrenberg 1995).
* The list of every total, with its conditions and sources, is in `docs/NOMENCLATURE.md` of the source code.

## From a script

```python
d = prj["TS-9"]
t = d.totals()                       # every total in % of the rock
print(t["qt"], t["intergranular_cement"], t["igv"], d.totals(original=True)["feldspar"])
prj.add_total("kaolinite_all", "Kaolinite (all)", rf.Selector(constituents=["kaolinite"]))
rows = prj.table(totals=["volume", "igv", "kaolinite_all"])
prj.to_csv("totals.csv", rows)
```

## Limits and common problems

* A custom total with a code already used is refused.
* IGV, COPL and CEPL were defined for sandstones; RockFace works them out for any rock, so read them with care in
  carbonates.
* The original composition is only as good as the paragenetic relations given in the composition (replaces,
  dissolution of…).

## Coverage

P26 (total table, custom totals, saved automatically), P27 (more than 30 automatic totals), P28 (custom totals
editor).
