# RockFace Lab: editing maps and objects

## What it is for

A segmentation is rarely perfect: a grain painted as cement, resin bubbles taken as pores, a scratch. The **Edit and
objects** tab corrects a map by hand over its image — brush, eraser, polygon, scissors, level tracing, islands — and
splits one of its segments into **objects**: each grain or pore body on its own, so that it can be measured. Objects
can be merged, split, cut and deleted. Every change can be undone.

## Before you start

A map of the section: a segmentation (page [RockFace Lab: segmentation and porosity](lab_segmentation.md)) or a mineral map ("The section
has no map yet: segment an image first.").

## Step by step

### Correcting a map

1. Open **Edit and objects** and choose the **Map**; set its **Opacity** over the image.
2. Tick **Edit the map** and choose the **Segment written**.
3. Choose a tool:
   * **Brush** — drag over the image to paint the chosen segment (**Brush radius**);
   * **Eraser** — drag to erase (not classified);
   * **Polygon** — click the corners; double-click or Enter fills it;
   * **Scissors** — draw a polygon: its inside (or, with **Scissors: outside the polygon**, its outside) is set to
     the chosen segment;
   * **Level tracing** — click a point: the connected pixels of a similar colour (**Colour tolerance (ΔE*ab)**) take
     the chosen segment.
4. **Islands smaller than** and **Remove the islands**: small pieces are given to their surroundings.
5. **Undo** and **Redo** — "Changes that can be undone: …; redone: …".

Every edit is written into the map at full resolution and at every zoom level at once.

### Objects

1. Under **Objects**, choose the **Segment to separate** (the grains, or the pores).
2. **Separation**:
   * islands — each connected piece is an object;
   * watershed — touching grains are split at their necks: **Minimum distance between centres** and **Smoothing of
     the distance map (σ)**;
   * SNOW — the over-segmented watershed of Gostick (2017), for pore bodies.
3. **Objects smaller than (dropped)**.
4. **Separate into objects**. "N objects kept: …". The objects are drawn each in its colour.
5. Edit them with the tools:
   * **Merge** — click the objects, then **Merge the objects clicked** ("Objects clicked: n (at least 2)");
   * **Split** — click an object to split it by watershed;
   * **Cut** — click the two ends of a cutting line;
   * **Delete** — click an object to delete it.
   **Undo** and **Redo** as for the map.

## Options

| Option | What it changes |
|---|---|
| Colour tolerance (ΔE*ab) | How different a colour may be and still be traced. |
| Minimum distance between centres | Larger: fewer, bigger objects. |
| Smoothing of the distance map | Larger: less over-splitting of irregular grains. |
| Objects smaller than | Small objects are dropped (noise). |

## How it works

Edits are written in place in the tiles of the map, every level of the pyramid rebuilt; each edit returns an undo
patch, so undoing gives back exactly the map before (checked against maps written anew). Objects are kept as an
object map: every pixel holds the number of its object. On sections of exact truth, grains separated by watershed
and SNOW were found with recall 0.78–0.83 and precision 0.96–0.98; with the XP colours the recall rose to 0.87–0.89
(page [RockFace Lab: measurements and size distributions](lab_measurements.md)).

## From a script

```python
seg = prj.image("ILLUSTRATIVE mosaic PP").segment("resin")      # a segmentation map
patch = seg.paint([(100, 100), (300, 120)], 15, 1)      # brush along a line, radius 15 px, segment 1
seg.undo(patch)
seg.level_trace(420, 380, tolerance=8, phase=2)
seg.remove_islands(30)
grains = seg.objects(2, "watershed", min_distance=6, sigma=1.0, min_px=40)
print(grains.object_count())
grains.merge_objects([(1421, 842), (1422, 842)])       # a point in each of two touching objects
grains.cut_objects((600, 300), (640, 360))
```

## Limits and common problems

* "Objects clicked: 1 (at least 2)." — click a second object before merging.
* Separating a very large map takes time: separate a crop first to choose the parameters.
* The scissors are reached from scripts for any polygon (`img.scissors`).

## Coverage

GT7 (manual segmentation: paint, erase, scissors, level tracing, islands), GT9 (partitioning: islands, watershed,
SNOW), GT10 (object editor: merge, split, cut, delete).
