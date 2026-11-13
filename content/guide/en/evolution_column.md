# Paragenetic evolution and the stratigraphic column

## What it is for

The **paragenetic evolution** puts the diagenetic phases of several samples — a formation, a field, a query — in
one chart: the events in order, their regime (eo-, meso-, telodiagenesis), the water source of each, the mean amount
and the number of samples, the U-Pb ages, and photos of the phases. The **stratigraphic column** places the
formations with their depositional ages and the U-Pb ages of the samples, to show that each cement is younger than
the rock that holds it.

## Before you start

* Descriptions with their composition and paragenetic relations (page [Diagenesis: environments, paragenetic sequence and knowledge graph](diagenesis.md)).
* For the ages: dated phases (page [U-Pb dating on the Tera-Wasserburg diagram](dating.md)).
* For the column: the formations with their depositional ages (below).

## Step by step

### The evolution

1. In RockFace Explorer, open the **Evolution** tab, then **Paragenetic evolution**.
2. The descriptions are those of the query of the Query tab (**Only the descriptions of the query**), or all.
3. The table lists the **Events (phases)** in order, with their **Regime**, **Water source**, **Mean % (n)** and
   **U-Pb age**. "N samples, P phases, C relations in contradiction between samples."
4. Change the **Regime** or the **Water source** of a phase in its cell (Marine, Meteoric, Evaporitic, Alkaline
   lake, Near-surface pore water, Basinal (burial), Hydrothermal, Not interpreted): your choice is kept in the project.
5. **Photos of the phases** adds photos of each phase to the chart: the photos of its dated spots, then the Atlas
   images annotated with its constituent.
6. **Evolution chart…** saves the chart (PNG, SVG, PDF); **Events (CSV)…** the table.

### The stratigraphic column

1. Open **Ages in the stratigraphy**.
2. In **Formations, top to base (depositional ages, Ma)**, **Add formation** and give its **Formation** name, **Top
   (Ma)**, **Base (Ma)** and **Colour**. **Save formations**.
3. The column shows each formation with its age range and, beside it, the U-Pb ages saved for its samples.
4. **Stratigraphic column…** saves it.

## Options

| Option | What it changes |
|---|---|
| Only the descriptions of the query | The evolution of the samples found, or of all. |
| Regime, Water source | Set by hand for a phase (cleared with an empty value). |
| Photos of the phases | Photos in the chart. |

## How it works

Each phase is a constituent with its habit and its kind (precipitation or dissolution), gathered across the
samples. The events are ordered by regime, then by the paragenetic relations of all the samples together, then by
their place in each sample's own sequence; relations that contradict each other between samples are counted and left
out. The regime comes from the diagenetic rules (a phase without one takes the regime of the phases before it), the
water source from the environments interpreted, unless set by hand. Ages are placed on the phase they date (mineral and
habit of the saved age).

## From a script

```python
evo = prj.evolution(formation="Example Formation", path="evolution.png")
for ph in evo.phases:
    print(ph.event, ph.label, ph.regime, ph.water, ph.share_mean, ph.ages)
prj.set_phase(evo.phases[-1].key, water="hydrothermal")
prj.stratigraphy = [{"name": "Example Formation", "top": 100.0, "base": 108.0, "colour": "#E9D7A5"}]
prj.strat_column("column.pdf")
```

## Limits and common problems

* A phase without paragenetic relations in any sample is placed by its regime and its place in each sample's
  sequence only.
* The column needs the depositional ages of the formations (base older than top).

## Coverage

L8 (paragenetic sequence of several samples), L12 (ages in the stratigraphy; paragenetic evolution of several
samples with quantification and photos).
