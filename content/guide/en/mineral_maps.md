# Mineral maps: registration, overlay, composite and quantification

## What it is for

A mineral map from QEMSCAN, MLA, TIMA, a µXRF phase map or any classified image tells which mineral is at each
pixel. RockFace Atlas registers it on the optical image of the same thin section, lays it over the image with any
opacity, makes a **composite image** (the map blended over the photograph, with its legend and scale), and
**quantifies** each phase over the whole map or over any region — comparing the map with the point count.

## Before you start

* A saved description whose thin section has (ideally) a whole-slide optical image in Atlas.
* The map as PNG or TIFF (a palette image, a grey image of phase numbers or an RGB image of phase colours) and its
  legend: CSV or TXT (with or without a header, e.g. `Mineral,R,G,B`) or a 3D Slicer colour table.

## Step by step

### Importing the map

1. In RockFace Atlas, **Mineral map…**.
2. In **Import a mineral map**, choose the map, its **Legend** (by default the legend file found beside the map),
   the **Colour tolerance** (how far a colour of an RGB map may be from the legend's) and the **µm per pixel**.
3. RockFace reads the phases ("… pixels, N phases"). In the **Map** tab, check every phase:
   * **Phase** name and **Colour**;
   * **Role**: Mineral, Pore, Background or Unclassified;
   * **Concepts**: codes of constituents, groups or kinds of the nomenclature, separated by commas (e.g.
     `quartz, quartz_dia`; `pore`) — they link the map to the nomenclature and to the point count;
   * **Show** to hide or show a phase; **Show all**, **Hide all**; **Merge** joins selected phases.
4. **Save phases**.

### Registering the map on the optical image

1. **Register…** opens the two images side by side.
2. Click a point on the optical image (left), then the same point on the map (right): a grain corner, a pore, a
   scratch. Repeat. Two pairs are enough for a **similarity** (rotation, scale, shift), three for an **affine**
   transform; spread them over the map and add a few more.
3. The table gives each **Pair** with its **Residual**; **Remove pair**, **Remove all**.
4. Choose the **Transform** and **Apply**. RockFace reports the RMS of the pairs and the **leave-one-out error**
   (each pair predicted by the others), the scale and the rotation.
5. The map is now drawn in the frame of the section, over every image of it: in the viewer, choose it in **Over
   it:** and set the opacity. **Side by side** shows the two images with **Move both views together**. **Remove**
   undoes the registration (the map goes back to its scale at the origin of the section).

### Quantifying

1. In **Quantification**, choose the **Region**: **Whole map**, **Area on screen**, or an annotation (a box or a
   contour drawn on any image of the section).
2. Choose a description in **Compare with** to put its point count beside the map.
3. **Quantify**. The table gives each phase with its **Map %**, **Area (mm²)**, **Count %** and **Difference**, and
   the summary: area analysed, the share of minerals and pores, porosity. Background and unclassified pixels are
   left out of the %.
4. **Export CSV…** writes the table.

### The composite image

1. **Composite…** opens **Composite image**.
2. **Optical image** (by default the plane-polarized slide), **Map drawn as** (colours blended over the image, or
   phase outlines), opacity, **Width**, **Region** (whole image or the area on screen).
3. **Legend with the % of each phase, and scale bar**; **Also add it to the image library**.
4. **OK** and save the picture.

## Options

| Option | What it changes |
|---|---|
| Colour tolerance | RGB distance within which a map colour is taken as a legend colour. |
| Role | Background and unclassified are left out of the %; pores give the porosity. |
| Concepts | The link to the composition lines for the comparison with the count. |
| Transform | Similarity (≥ 2 pairs) or affine (≥ 3 pairs). |

## How it works

The registration is a least-squares fit of the landmark pairs; the leave-one-out error is a conservative estimate of
the real error (about twice it, on test cases with a known answer: six pairs picked to the nearest pixel give
2.9 µm RMS on a 10 µm map). The map's tiles hold phase numbers drawn through a colour table, so phases are shown,
hidden or recoloured at once. A map can also be aligned on a segmentation without landmarks (page [A mineral map aligned without landmarks; effects on big volumes](map_alignment_big_volumes.md)).

## From a script

```python
d = prj["TS-9"]
qem = d.add_map("TS-9_qemscan.tif", legend="TS-9_qemscan.csv", um_per_px=10)
pp = prj.image("TS-9 PP")
fit = qem.register([((140, 120), (380, 288)), ((1250, 90), (1860, 314)), ((700, 520), (1102, 854)),
                    ((180, 880), (390, 1304))], model="similarity", target=pp)
print(f"RMS {fit.rms_um:.1f} µm, leave-one-out {fit.loo_um:.1f} µm")
for row in qem.compare(d):
    print(row["phase"], round(row["map"], 1), row["count"])
qem.composite("TS-9_composite.png", base=pp, opacity=0.5)
```

## Limits and common problems

* "No mineral map on this thin section. Import one with Mineral map…"
* "N pairs: at least … are needed."
* "Not registered and without scale: register it on the optical image."
* An RGB map with colours far from the legend: raise the colour tolerance, or give a legend with the exact colours.

## Coverage

GT2 (QEMSCAN maps), GT5 (registration with landmark pairs), L9 (overlay of the optical image and the mineralogical
map → composite image).
