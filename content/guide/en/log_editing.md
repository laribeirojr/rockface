# Editing a log segmentation and its objects

## What it is for

An automatic segmentation of an image log is never perfect: a vug is missed, a pad edge is taken for a vug, two vugs
are joined. Here you correct the segmentation with a brush, and review the objects (vugs, spots) one by one: decline
the false ones, merge the pieces of one object, keep only those whose measurements make sense.

## Before you start

A segmented log (Well logs tab → Segmentation, objects and pore sizes → Segment) or a log of objects (… → Objects),
open in the tracks of RockFace MC.

## Step by step

### Correcting a segmentation

1. Open the segmented log. In **Brush and objects**, choose what to **Paint** (a segment, or **— eraser —**) and the
   **Brush radius** in millimetres of the borehole wall.
2. Press **Paint on the track** and drag the mouse on the track. A stroke crosses the 0/360° seam the short way.
3. **Undo** takes back the last stroke.

### Reviewing the objects

1. Open the log of objects. The table lists every object: depth (top, base, centre), azimuth, area, equivalent
   diameter, height, width, and whether it touches the top or base of the log.
2. Type a filter (`area_mm2 > 50 and not touches_edge`): the table shows the objects that pass; the histogram shows
   the chosen column.
3. Select objects in the table and press **Decline selected** or **Merge selected**, or press **Keep only the rows
   shown** to decline every object the filter hides.
4. To add an object, choose **A new object** in **Paint** and paint it; **Grow the selected object** and **Trim the
   selected object** change the object selected in the table.

## How it works

The brush is a disc of the given radius on the unrolled wall (depth step × column width in mm). The rows touched are
rewritten in place with their pyramid of levels. The measurements are recomputed from the objects after every
change.

## From a script

```python
log = prj.log("Vugs (ILLUSTRATIVE)")
patch = log.paint([(120.0, 2510.30), (126.0, 2510.32)], radius_mm=8, value=2)
log.undo(patch)
objects = prj.log("Vugs (ILLUSTRATIVE) (objects)")
table = objects.instances()
declined = objects.keep_only("area_mm2 > 50 & touches_edge == 0")
new_label = objects.paint_instance([(200.0, 2511.0)], radius_mm=10)
```

## Limits and common problems

* **"Select an object in the table first."** Grow and trim need an object selected.
* New paint never covers another object; trim only removes pixels of the selected object.
* The trained instance segmenter of GeoSlicer comes in stage 0.26.

## Coverage

GI8 (Segment Editor of image logs, Instance Segmenter Editor).
