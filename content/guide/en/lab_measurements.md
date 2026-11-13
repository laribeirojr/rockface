# RockFace Lab: measurements and size distributions

## What it is for

The **Measurements** tab measures every object of an object map — each grain or pore: area, perimeter, Feret
diameters, the fitted ellipse, shape factors, orientation, brightness and colour — and, for pores, the throats
between them and the coordination number. It gives the size classes (Udden–Wentworth for grains, Choquette & Pray
for pores), the Folk & Ward statistics, tables with computed columns and filters, charts, and the exports.

## Before you start

An object map (page [RockFace Lab: editing maps and objects](lab_editing_objects.md)), ideally with its scale.

## Step by step

### Measuring

1. Open **Measurements** and choose the **Object map**.
2. **Size measure** (the column used for the sizes: largest Feret diameter, equivalent diameter…) and
   **Distribution by**: **number of objects** or **area (as a point count)**.
3. **Leave out objects cut by the edge**; **Objects of at least** N pixels.
4. **Measure**. "N objects measured: …".
5. The summary: "Size: mean … µm (class); D10, D50, D90", "Folk & Ward (φ): mean, sorting (class), skewness,
   kurtosis", "Shape: mean aspect ratio, mean circularity", and for pores "Mean coordination number … (N throats)".

### The table

* One row per object with its **Area**, **Perimeter**, **Perimeter / area**, **Equivalent diameter**, **Largest**,
  **Smallest** and **Mean Feret diameter**, **Angle of the largest Feret**, **Aspect ratio**, **Elongation**,
  **Ellipse major** and **minor axis**, **Orientation (ellipse)**, **Eccentricity**, **Form factor**, **Circularity**,
  **Solidity**, **Convexity**, **γ (perimeter / circle)**, **Centre x, y** (px and mm), **On the edge**, the
  **Coordination number** of pores, and the brightness and colour of the picture under the object.
* **Filter**, e.g. `area_um2 > 500 & aspect_ratio < 0.6`, then **Apply the filter** ("Objects shown: n of N").
* **New column** with a **Formula**, e.g. `feret_max_um / feret_min_um`, then **Add the column**.
* The table can be sorted, filtered by column, exported to CSV or XLSX, and shown as a histogram.

### Classes and charts

1. **Classes**: **Grain size (Udden–Wentworth)** (14 classes from clay to boulder), **Pore size (Choquette &
   Pray)**, or **Groups of similar area** — with the count, % by number and % by area of each.
2. Chart: **Size histogram (φ)** with its cumulative curve, **Crossplot with histograms**, **Rose diagram of
   orientations**, **Size classes**, or **Transitions between phases (stacked bars)** (page [Transitions between phases](transitions.md)). **Draw the chart**; save it as PNG.
3. Export the tables (CSV, XLSX) and the objects in colour (PNG).

## Options

| Option | What it changes |
|---|---|
| Size measure | The diameter used for classes and statistics. |
| Distribution by area | Each object weighs its area, as a point count would. |
| Leave out objects cut by the edge | Objects touching the image border are not counted. |

## How it works

* Perimeter by the Crofton formula; Feret diameters from the convex hull of the sub-pixel outline; the ellipse of
  the same second moments; shape factors after ISO 9276-6.
* Throats: the length of the boundary between two touching pores; the coordination number is the number of pores
  each touches.
* Checked on shapes of known size at random positions and angles: from 20 px across, area, perimeter, Feret
  diameters and ellipse within about 2 %, orientation within a fraction of a degree; coordination 4 and 6 in square
  and hexagonal packings; the Folk & Ward measures of 517 discs of a known log-normal law equal to those of the drawn
  diameters.

## From a script

```python
grains = prj.image("ILLUSTRATIVE mosaic PP").segment("resin").objects(2, "watershed", min_px=40)
m = grains.measure()
print(m.summary(exclude_edge=True))                       # Folk & Ward, D10/D50/D90, shape, coordination
t = m.table.filter("touches_edge == 0")
t.add_column("ratio", "feret_max_um / feret_min_um")
print(rf.measure.class_table(t, "feret_max_um", "wentworth"))
rf.measure.chart("rose", t, "orientations.png", x="ellipse_angle")
rf.measure.to_xlsx("grains.xlsx", {"grains": t})
```

## Limits and common problems

* "The map has no scale: lengths are in pixels." — give the image its scale in Atlas.
* Objects of one or two pixels have meaningless shapes: raise **Objects of at least**.
* The Crofton perimeter is 5–7 % low on long straight sides.

## Coverage

GT11 (per-object metrics), GT12 (2D throats and coordination), GT13 (size classes; groups by similar area), GT14
(outputs: XLSX tables, coloured objects), GT19 (tables, filter, charts).
