# Suggest description: from a segmentation map to the description

## What it is for

A segmentation map already says how much of the section each mineral and the pores cover. **Suggest description**
turns it into proposals for the description of the thin section — a composition line for each constituent with its
points, the visual porosity, and, from an object map of grains, the main grain-size mode and the sorting — and writes
only what you tick. It saves typing what the map already measured and keeps the petrographer in charge.

## Before you start

* In Lab, a thin section with a segmentation map: made in **Lab → Segmentation**, by an AI model in **Lab → AI**, or
  imported as a mineral map in Atlas.
* A description of that thin section (created in Petro).
* The phases of the map named with concepts of the nomenclature (the map's legend; Atlas → mineral map → phases).

## Step by step

1. **Lab** → choose the thin section; open the map (or keep any image: the last map of the section is used).
2. Click **Suggest description** in the toolbar. If the section has several descriptions, choose one.
3. The dialog shows the suggestion as a sentence and one checkbox per item:
   * each constituent with its share of the counted area and its points of a 300-point count — when the map's
     phase allows several constituents (a phase named "quartz"), the others are listed (*or …*) to check;
   * the visual porosity (the pore phases);
   * the grain-size mode and the sorting, when an object map of grains is given (script).
4. Untick what you do not want and click **Write the ticked items**. Each line written says in its observation that
   it was suggested from the map.

In the Mio panel, `@mio sugira a descrição de ILL-NL-003` (or the skill *sample report*) shows the same suggestion
as text, without writing anything.

## Options

| Item | Written into |
|---|---|
| Composition line | the composition: a new line with the points, or the points of the same constituent replaced |
| Visual porosity | the pore system: total porosity |
| Grain size | the thin-section texture: main mode (mm and Wentworth class) |
| Sorting | the thin-section texture: sorting class and σI |

## How it works

* The map is quantified with the background and unclassified phases left out (as in Atlas → mineral map); the share
  of each phase becomes points of a 300-point count, rounded (a share below one point is listed but not applicable).
* A phase's concepts give the constituent: the first constituent named, or the first constituent of a group named;
  its kind (primary, diagenetic, pore) comes from the knowledge base.
* Grain size and sorting are the graphic measures of Folk & Ward (1957) of the maximum Feret diameters of the grain
  objects, classed by Wentworth (1922) and Folk & Ward's sorting terms.
* The sentence is written from a template in English, Portuguese or Spanish, so every number is a number of the map;
  a language model may rephrase it, and the rephrasing is kept only with exactly the same numbers.

## From a script

```python
d = prj["ILL-NL-003"]
s = d.suggestion()                                   # the last map of its thin section
print(rf.suggest.text(s, "pt", prj.kb))
print([(i.key, i.percent, i.points) for i in s.items])
d.apply_suggestion(s, accept=["porosity", "line:calcite_dia"])
s = prj.suggest_description("my map", objects="my grains")      # with grain size and sorting
```

## Limits and common problems

* "This thin section has no segmentation map": make one in Lab → Segmentation or Lab → AI.
* A phase named only by a kind ("Cement") is listed but not applicable: name it with a constituent in the map's legend.
* The points replace those of the same constituent in the composition (without habit or location); lines with a
  habit or a location are left as they are.

## Coverage

"Segmentation turned into description suggestions" of the ROADMAP stage 0.27; L7 (whole-section quantification)
carried into the description.
