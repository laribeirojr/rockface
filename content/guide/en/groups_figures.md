# Groups, figures and presentations

## What it is for

RockFace Explorer draws several **groups** of samples together on a ternary classification — the samples of each
well on Folk's QFR, each facies on Dickinson's QtFL — with their markers and colours. Its **figure generator**
makes publication figures from any attribute of the collection (crossplots, histograms, bars, box plots, curves
against depth by well, ternary diagrams), sized for a journal, and exports them also as a SciVelyx Graphs project. A
**presentation** gathers figures, tables and image galleries into a PowerPoint file.

## Before you start

A project with descriptions; saved queries help (page [RockFace Explorer: queries, result tables and exports](explorer_queries.md)).

## Step by step

### Groups on a ternary classification

1. Open the **Groups** tab of Explorer.
2. **Classification method**: the **Ternary classification** (Folk 1980, McBride 1963, Dickinson QtFL and QmFLt,
   or one of the project) and, if wanted, **Original composition (restored)**.
3. **Add group** (up to ten). For each group, in **Groups of descriptions**:
   * the descriptions: **Query of the Query tab**, **Criteria of the group**, or a saved query; **Picked by hand**
     adds others ("Those found by the query are fixed; tick others to add them by hand");
   * **Point marker**, **Fill colour**, **Border colour**; **Show the group**; **Remove the group**.
4. **Classify** draws every group, with the legend. "N points in G groups; M descriptions without a point in this
   classification."
5. In the diagram: **Point size**, **Without colours**, **Names of all points (or click a point)**, **Zoom in**,
   **Zoom out**; the hover box gives the name and the vertex values; "Field under the pointer: …".
6. **Export picture…**; **Save groups…** and **Open groups…** keep the sets in the project.

### A figure

1. Open the **Figures** tab.
2. **Kind**: **Crossplot**, **Histogram**, **Bars (number of samples)**, **Box plot by category**, **Against depth,
   by well** or **Ternary with groups**.
3. **Attribute (X)** and **Attribute (Y)** — any attribute of any concept (for example Petrophysics › Porosity,
   Totals › Qt); **Colour by** an attribute or **Groups (Groups tab)**; **Bins** for histograms; **Depth** (measured,
   corrected, adjusted) for curves against depth.
4. **Logarithmic X**, **Logarithmic Y**, **Names of the samples**, **Legend**, **Only the descriptions of the query**.
5. **Title**; **Journal size** (Nature, Elsevier, AAPG, ACS one or two columns, a 16:9 slide) or **Free size** with
   **Width (mm)**, **Height (mm)** and **Font size (pt)**.
6. **Export…** writes PNG, TIFF, JPEG, SVG, PDF, the plotted data as CSV, or a SciVelyx Graphs project
   (`.scivelyx.json`) to finish the figure there.
7. **Save figure…** keeps it in the project; **Open figure…** draws a saved one again from the latest records.

### A presentation

1. Under **Presentation**, add slides: **+ Figure** (the figure shown), **+ Table** (the result table of a
   concept), **+ Images** (a gallery of the thin sections).
2. **Write presentation (.pptx)…**. The deck is 16:9, opens with a title slide and the query's criteria.
3. Or, in the Query tab, **Export → Presentation of the query (.pptx)…** writes one at once.

## Options

| Option | What it changes |
|---|---|
| Original composition (restored) | The groups are placed with the composition before diagenesis. |
| Journal size | Width, height and fonts of the journal's column (or of a slide). |
| Where a description has several rows | The mean is used, except when X and Y are of the same concept (one point per row). |

## How it works

Groups and figures are recomputed from the saved descriptions every time they are drawn, so a saved figure always
shows the latest data. Figures are drawn with Matplotlib at 600 dpi by default; the SciVelyx Graphs project carries
the same data and styles, so the figure can be finished in SciVelyx Graphs.

## From a script

```python
wells = [rf.Group(w, rf.Query([rf.Criterion("identification", "well", [w])])) for w in ("ILLUSTRATIVE-A1", "ILLUSTRATIVE-A2")]
prj.figure("qfr.pdf", kind="ternary", scheme="folk1980", groups=wells, colour_by="groups")
phik = prj.figure("phi_k.png", kind="crossplot", x="petrophysics.porosity", y="petrophysics.permeability",
                  log_y=True, colour_by="identification.facies", preset="elsevier-1col")
prj.figure("phi_k.scivelyx.json", phik)                      # open it in SciVelyx Graphs
prj.save_figure("Porosity and permeability", phik)
prj.presentation("barite.pptx", ("diagenetic", "constituent", "barite"), figures_=[phik])
```

## Limits and common problems

* "At most 10 groups."
* "No figures saved in this project yet." / "No groups saved in this project yet."
* "Add slides first." — a presentation needs at least one slide.
* PowerPoint presentations need the `explorer` extra (python-pptx), installed with `.[all]`.

## Coverage

M1 (up to 10 groups from saved queries), M2 (marker, fill and border colour per group), M3 (classification methods
recomputed from the latest data), M4 (legend, hover box, labels, zoom, export), L5 (figure generator and
presentations).
