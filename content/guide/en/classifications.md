# Classifications and ternary diagrams

## What it is for

The **Classification** tab names the rock: sandstones by Folk (1980) and McBride (1963), provenance by Dickinson
(QtFL and QmFLt), texture by Folk's gravel–sand–mud classes, carbonates by Dunham, Embry & Klovan, Wright, Grabau
and Bramkamp & Powers. Each classification is worked out from the composition, on the present and on the original
composition, and the ternary ones are drawn in a diagram window. A project can add its own ternary classifications.

## Before you start

* A description with its composition (and, for the texture, the gravel, sand and mud % of the Microscopic tab).
* For carbonates: the carbonate inputs that the composition cannot give (below).

## Step by step

### Reading the classifications

1. Open the **Classification** tab. **Classifications** lists every classification with its **Present** and
   **Original** result.
2. "no data" means the composition does not have what the classification needs; "outside the fields" that the
   point falls outside every field; "Near the boundary with: …" that it lies within the tolerance of another field.
3. **Observations** — a note on the classification.

### The ternary diagram

1. Select a ternary classification and press **Diagram…**.
2. The **Ternary diagram** window shows the fields, the point of the description and, with **Original point**, the
   point of the original composition.
3. **Values (% of the three poles)** gives each **Pole** and the **Result**; **Under the cursor** names the field
   under the mouse.
4. **Fit**, **Zoom in**, **Zoom out**; **Point size**; **Colours** (fields coloured or not); **Names** (field names
   on or off).
5. **Export picture…** saves the diagram as PNG or SVG.

### Carbonate rocks

1. When carbonates are more than half of the solids, fill in **Carbonate rocks: what the composition does not
   tell**:
   * **Fabric support** (as in the Microscopic tab, or set here); **Organically bound at deposition** (no; yes, mode
     not known; baffling; encrusting and binding; rigid framework);
   * **Grains larger than 2 mm (% of the grains)** and their **Support**;
   * **Microstylolitic grain contacts**, **Cement is the main component**, **Diagenesis obliterated the fabric**;
   * **Crystal size (µm)** and **Dominant grain size (mm)**;
   * the Bramkamp & Powers inputs (page [McBride, Bramkamp & Powers and the packing classes](classifications_packing.md)).
2. **Possibilities…** lists every class of the selected classification with its criteria, the one found marked.
   **Missing: …** names the inputs still needed.

### A classification of the project

1. **Manage classifications…** (in the tab or in the diagram window) opens **Ternary classifications of the
   project**.
2. **New**; give the **Code** and the name.
3. **Poles**: three poles, each with a **Symbol** and the **Totals added up** (codes of totals separated by commas).
4. **Fields**: **Add field**, its name and its **Vertices** — three percentages per vertex in the order of the
   poles, vertices separated by semicolons (for example `100 0 0; 50 50 0; 50 0 50`).
5. **Apply**. The classification appears in every description of the project, in Explorer's groups and in the
   figures.

## Options

| Classification | Inputs |
|---|---|
| Folk (1980), McBride (1963) — QFR | quartz, feldspars and rock fragments of the composition |
| Dickinson QtFL, QmFLt | Gazzi–Dickinson counting assumed; plutonic fragments are not plotted |
| Folk (1954) gravel–sand–mud | gravel, sand and mud % of the Microscopic tab |
| Dunham (1962), Embry & Klovan (1971) | support, grains, mud, organic binding, grains > 2 mm |
| Wright (1992) | also cement, microstylolites, obliteration, crystal size |
| Grabau (1904) | dominant grain size of the carbonate grains |
| Bramkamp & Powers (1958) | group, texture, porosity, alteration, dolomite |

## How it works

* A ternary point is the three poles' totals normalised to 100; the field is found by point-in-polygon on the
  published boundaries (Folk 1980; McBride 1963; Dickinson et al. 1983 and Dickinson 1985).
* The QmFLt recycled-orogen subfields come from one digitization of the published figure and are marked
  "Boundaries to be checked against the original figure."
* The carbonate classes follow the criteria of their papers, shown in **Possibilities…**. They apply when
  carbonates are above 50 % of the solids ("Carbonates are … % of the solids; the carbonate classifications apply
  above 50 %").

## From a script

```python
d = prj["TS-9"]
print(d.classify("folk1980", label=True), d.point("folk1980"))
print(d.classify("dunham1962"), d.classify("folk1980", original=True))
d.carbonate.support = "grain_supported"               # carbonate inputs, then save
d.save()
rf.ternary_figure("qtfl.svg", "dickinson_qtfl", [d], original=False)   # several descriptions may be given
```

## Limits and common problems

* "no data": the composition lacks the poles (e.g. no feldspar and no rock fragments is still a point; no framework
  grain at all is not).
* Custom fields with vertices that do not add up to 100: "Vertices not understood".
* A classification of the project with a code already used is refused.

## Coverage

P29 (siliciclastic classifications, present and original), P30 (Dickinson provenance), P31 (ternary diagram window),
P32 (carbonate classifications and the table of possibilities), M3 (classifications recomputed from the latest
data).
