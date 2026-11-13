# Point counting

## What it is for

The **Point count** tab counts the composition on a grid of points laid over the thin section — for example 300
points — on the section image or with a motorized stage. Every point keeps its position in millimetres of the
section frame, so a recount lands on the same points, any counted point can be visited again, and the map of the
counted points shows the composition of the section. The counts fill the Points column of the composition.

## Before you start

* A description with its composition lines (page [Composition](composition.md)): you count *as* one of the lines.
* Saved at least once: from then on every counted point is written to the project at once, so no point is ever
  lost ("Save the description to keep the count…").
* Optional: an image of the section (**Section image…**), or the whole-slide image of RockFace Atlas.

## Step by step

### The grid

1. Open the **Point count** tab. Leave **Mode** on **Grid**.
2. Either type **Points wanted** (e.g. 300) and the **Area w × h (mm)** and press **Spread N points**, or give the
   grid yourself: **Origin x, y (mm)**, **Step x, y (mm)** and **Columns × rows**.
3. **Path**: **Serpentine** (back and forth) or **Row by row**. Tick **Round section** to keep only the points inside
   a round section.
4. **Make grid**. The map on the left shows the points.

### The section image

1. **Section image…** loads a picture of the section; under **Image and calibration** give its **µm per pixel** and
   the **Image origin x, y (px)** (the pixel at 0, 0 mm).
2. The points are drawn over the image. Without an image the points are drawn on their own.

### Counting

1. **Initiate** goes to the first point. With **Track** on, each count moves to the next point not yet counted.
2. Choose the line in **Count as** and press **Count**, or press the line's key (1–0 and Ctrl+1–0, set in the
   Composition tab's **Keys…**).
3. **Step over** skips a point (on resin out of the section, a hole…); **Uncount** takes back the count of the
   current point; **Back** returns to the previous point.
4. **Observation at the point** and **Pictures at the point…** keep a note and photos for the point under the
   cross-hairs.
5. The counter shows "N of M points counted"; the composition's points follow at once.

### Moving around

* Click a point on the map to go to it; **Go to point…** by its number.
* **Fit**, **Zoom in**, **Zoom out**, the mouse wheel; **Only the map** hides the panel.
* The path followed, the current point and the stage position are drawn on the map, the counted points coloured
  by their line.

### With a motorized stage (free mode)

1. Choose the **Stage** (**Simulator (no hardware)** for practice) and press **Controller…** to move it with the
   numeric pad: 8, 2, 4, 6 and the diagonals 7, 9, 1, 3.
2. **Mode → Free**: give the **Counting axis**, the **Step (mm)**, the **Traverse spacing (mm)** and **Reverse x ·
   y** for a stage mounted the other way. Each count moves the stage one step; at the end of the area it moves to
   the next traverse.

### Coordinates

* **Coordinates…** lists the points counted as each constituent, with x and y in mm; **Export CSV…** writes them.
* **Import points…** reads points from a CSV file (x, y and the line label), in mm or in pixels with their size.
* **Clear count** forgets every counted point and keeps the grid.

## Options

| Field | What it changes |
|---|---|
| Points wanted, Area | Spread N points: square steps over the area, exactly N points. |
| Path | Serpentine or row by row. |
| Round section | Only the points inside the ellipse inscribed in the grid area. |
| Track | Move to the next point not counted after each count. |
| Counting axis, Step, Traverse spacing | Free mode with a stage. |

## How it works

The same grid parameters always give the same points (request L10: positions never lost,
reproducible). A grid cannot be changed once points are counted ("… points are already counted: the grid stays");
clear the count first. The composition lines the count uses get exactly the number of points counted as them;
other lines keep their own points. The counted points also appear in RockFace Atlas over the whole-slide image
and in the figures of the section.

## From a script

```python
d = prj["TS-9"]
q = d.add_line("quartz_mono")
c = d.add_line("calcite_dia", habit="poikilotopic", location="ig_pore_filling")
d.count.set_grid(rf.ct.grid_for(300, 20.0, 30.0))       # 300 points on a 20 × 30 mm area
d.count.assign(q.uid)                                    # the current point counted as quartz; moves on
d.count.assign(c.uid)
rf.ct.sync_points(d.composition, d.count)                # the composition's points follow the count
d.save()
print(d.count.counted, d.count.coordinates_by_line())
```

## Limits and common problems

* "No points yet: make a grid, or count in free mode."
* "Every point is counted or skipped." — the count is complete.
* RockFace ships the stage simulator; a motorized stage of a given make needs its driver, written on the `Stage`
  interface of `rockface.core.counting` (for example as a plug-in).

## Coverage

P25 (stage buttons: Initiate, Track, Step over, Controller), S1 (free mode), S2 (movement log, return to points,
go to a point, zoom, colours per constituent), S3 (map of the counted points, percentages, return to any point),
L10 (a grid of points with coordinates on each thin section).
