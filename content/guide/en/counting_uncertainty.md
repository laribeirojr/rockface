# How sure the point count is

## What it is for

A point count of 300 points does not give the composition, it estimates it: counted again, the same thin section
would give slightly different percentages, and a rock near a boundary of a classification could fall in the field
next door. RockFace shows this **counting uncertainty** where the numbers are used:

* the **95 % interval** of every counted line in the composition;
* the **probability** of the field of each ternary classification (Folk, McBride, Dickinson);
* the **confidence region** of the point on the ternary diagram;
* while counting, whether the classification is already **stable** or **how many more points** it needs.

## Before you start

* A description with **counted points** (Petro → Point count, or points typed in the Composition tab). Lines with a
  manual % or a nominal amount have no counting uncertainty and are taken as they are.
* For the probabilities: a sandstone (or any rock) that a ternary classification places.

## Step by step

1. **Petro → Composition.** The column **95 % interval** gives, for each counted line, the range of percentages of
   the rock that the count supports; the tooltip says how it was computed.
2. **Petro → Point count.** Under the counted points, a line such as *Folk (1980): Subarkose 97 % — stable* or
   *… 81 % — about 240 more points for 95 %* tells you whether to stop counting. *Near a boundary* means that more
   points will not settle the field: the rock really is between two fields.
3. **Petro → Classification.** The column **Probability** gives the probability of the field shown; select a
   ternary classification to read every field's probability, and whether it is stable or how many points it needs.
4. **Diagram…** draws the **confidence region**: the shaded area where the point may be with 95 % confidence (a band
   along a side when a pole is empty). **Confidence region** switches it off.
5. **Reports** give the probabilities under the classifications and draw the regions on the diagrams; the report
   dialog's **Counting uncertainty of the classifications** leaves them out.

## Options

| Item | Value |
|---|---|
| Confidence of the intervals and the region | 95 % |
| A classification is *stable* when | its most probable field has at least 95 % |
| Points needed | counted again with the same proportions, up to 5,000 more points |
| Draws of the probabilities | 4,000 (the same count always gives the same numbers) |

From a script the confidence, the stability level and the draws can be changed.

## How it works

* **Intervals.** A counted line is a proportion of the counted points; its interval is the Wilson (1927) score
  interval, which stays between 0 and 100 % and keeps its 95 % coverage for rare constituents, unlike the ± 2σ of
  the classical chart of Van der Plas & Tobi (1965) (Agresti & Coull 1998; Howarth 1998; Weltje 2002). The interval
  is scaled to the share of the rock that the counted lines hold.
* **Probabilities.** The counts are a multinomial sample of the rock (Chayes 1956). Given the counts, the true
  proportions follow a Dirichlet distribution (Jeffreys' prior, counts + ½; Vermeesch 2005). RockFace draws 4,000
  compositions from it, computes the totals and the point of each classification exactly as for the description,
  and counts the field each point falls in.
* **Region.** The drawn points, in additive log-ratios (Aitchison 1982; Weltje 2002), give a bivariate normal
  region at 95 %, drawn back on the triangle — an ellipse in log-ratios, curved near the corners. When one pole is
  empty in every draw the region is the interval along the side.
* **Points needed.** The same proportions counted with more points (1.25 to 30 times as many) until the most
  probable field reaches 95 %.

## From a script

```python
d = prj["ILL-TS-001"]
u = d.uncertainty()                          # confidence=0.95, stable=0.95, draws=4000
u["schemes"]["folk1980"]["probabilities"]    # {'subarkose': 0.97, 'arkose': 0.02, …}
u["schemes"]["folk1980"]["needed"]           # 0: already stable; None: near a boundary
u["lines"][0]                                # {'constituent': 'quartz_mono', 'share': 48.1, 'low': 42.5, 'high': 53.8, …}
rf.wilson_interval(21, 295)                  # (4.7, 10.6) in % of the counted points
rf.ternary_figure("folk.png", "folk1980", prj.descriptions(), regions=True)
```

Mio answers too: *"a classificação da ILL-TS-001 é confiável?"*, *"how sure is the classification of ILL-TS-002?"*,
*"quantos pontos faltam na ILL-TS-002?"*.

## Limits and common problems

* **Counting uncertainty only.** The sampling error between thin sections of the same rock (Bayly 1965), the
  identification errors of the petrographer and the uncertainty of manual and nominal amounts are not included.
* The model assumes points farther apart than the largest grain (Van der Plas & Tobi 1965); a grid finer than the
  grains counts the same grain twice and makes the intervals look narrower than they are.
* The original composition (before diagenesis) has no probabilities yet.
* A carbonate rock gets the intervals of its lines; the rule classifications (Dunham, Embry & Klovan…) have no
  probabilities.

## Coverage

O8 (the owner's request of 2026-11-17: the innovations, the first one).

References: Chayes (1956); Van der Plas & Tobi (1965), https://doi.org/10.2475/ajs.263.1.87; Bayly (1965); Wilson
(1927); Agresti & Coull (1998); Howarth (1998), https://doi.org/10.2475/ajs.298.7.594; Aitchison (1982); Weltje
(2002), https://doi.org/10.1016/S0012-8252(01)00076-9; Vermeesch (2005), https://doi.org/10.1029/2004JB003479;
Vermeesch (2018), https://doi.org/10.1016/j.epsl.2018.08.019.
