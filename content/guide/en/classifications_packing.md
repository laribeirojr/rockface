# McBride, Bramkamp & Powers and the packing classes

## What it is for

Three classifications that the reference programs offer and RockFace now has, each from its published source:
**McBride (1963)** for sandstones, **Bramkamp & Powers (1958)** for carbonates — with its reservoir-rock symbol
(for example *21BD*) — and the **packing classes** loose, normal and tight of the packing proximity of Kahn (1956).

## Before you start

* A description with its composition (Petro → Composition).
* For Bramkamp & Powers: the carbonate inputs that the composition cannot give (below).
* For the packing class: the grain contacts counted on a traverse, or the contact types in %.

## Step by step

1. **Petro → Classification tab.** McBride appears beside Folk (1980) with its present and original field;
   **Diagram…** draws the triangle.
2. For a carbonate rock, fill in the **carbonate inputs** at the bottom right:
   * *Original texture (Bramkamp & Powers)*: not visibly altered, moderately altered, strongly altered (still
     recognizable) or obliterated;
   * *Visual porosity*: A porous or poorly cemented, B compact, C dense;
   * *Altered by*: from the dolomite (default), anhydrite (A), silica (S) or changes not understood (X);
   * *Facies*, *Group* and *Dolomite %* come from the composition and can be overridden;
   * *Special rock type*: 14AX/14BX, 31BX or 51BX when the voids replace grains.
3. The row *Carbonates — Bramkamp & Powers (1958)* shows the name, the facies and the symbol;
   **Possibilities…** lists the 28 classes with their criteria.
4. **Petro → Microscopic tab → Contacts and packing.** Type the grain-to-grain and the total contacts of a
   traverse, or the contact types with their %: the proximity and the class appear at once. **Packing help…** shows
   three ILLUSTRATIVE packs, one per class, each with its proximity counted.

## Options

| Field | Values |
|---|---|
| McBride poles | Q = quartz, quartzite and chert; F = feldspars; R = other rock fragments (plutonic and carbonate fragments included) |
| Bramkamp & Powers group | 1 fine-grained limestone, 2 calcarenitic limestone, 3 calcarenite, 5 coarse clastic carbonate; 4 crystalline dolomite (obliterated) |
| Symbol | group · degree (1 moderate, 2 strong, 3 relic) · porosity (A, B, C) · alteration (R, D, A, S, X) |
| Packing classes | loose P < 40 %, normal 40–55 % (both limits included), tight P > 55 % |

## How it works

* **McBride (1963)** places the point by the boundaries of Folk (1954): quartzarenite above 95 % Q; the lines
  F = 25 % and R = 25 % from the 75 % points of the sides, and F = 10 %, R = 10 % from the 10 % points of the base;
  lithic subarkose where both F and R are 10–25 %; F:R = 1:1 splits the rest (McBride 1963, fig. 1 and p. 666–667).
* **Bramkamp & Powers (1958)**: group 1 when the sand-size or coarser clastic carbonate fragments are below 10 %;
  group 2 above it with at least 10 % of the original fine matrix; groups 3 and 5 below 10 % matrix, split by the
  fragments coarser than sand. The alteration columns of their Table 2: < 10 % dolomite recrystallized, > 10 %
  porphyroblastic dolomite (moderate), 10–75 % dolomitic and > 75 % relic (strong); obliterated is group 4. The
  facies: impure with clay and silt, sandy with detrital grains (from 1 % of the solids). Percentages are of the
  solids.
* **Packing**: Kahn's packing proximity P = grain-to-grain contacts ÷ all contacts of the grains crossed × 100
  (Kahn 1956); without counts, the same ratio from the contact types (every type but "floating"). The class limits
  are those of Bocardi (2005, p. 31) and Menezes Filho (2015, p. 40). The help pictures are computed by RockFace:
  a pack of round grains whose radii are scaled until the proximity, counted on horizontal traverses as Kahn
  describes, falls in the class.

## From a script

```python
d = prj["ILL-TS-001"]
d.classify("mcbride1963", label=True)                 # 'Subarkose'
c = prj["ILL-CB-001"]
c.carbonate.bp_texture, c.carbonate.bp_porosity = "moderate", "B"
c.save()
c.classify("bramkamp_powers1958", label=True), c.symbol()   # (…, '21BD')
d.packing()                                           # {'proximity': 62.0, 'density': …, 'class': 'tight'}
rf.packing_class(47)                                  # 'normal'
```

## Limits and common problems

* McBride does not say where coarse plutonic fragments go: RockFace counts them as rock fragments (Folk 1980 counts
  them as feldspar), and says so beside the diagram.
* The visual porosity A/B/C of Bramkamp & Powers has no numbers in the paper: choose it by their criteria (the
  tooltip summarizes them). Until it is chosen the symbol shows "?".
* Bramkamp & Powers applies when carbonates are more than half of the solids.

## Coverage

P14 (packing classes and visual help), P29 and M3 (McBride), P32 (Bramkamp & Powers).
