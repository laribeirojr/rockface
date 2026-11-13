# Transitions between phases

## What it is for

Which minerals touch which: does the dolomite border the pores, is the quartz surrounded by calcite cement? The
transition table of a mineral map or a segmentation says, for every phase, how its neighbouring pixels are shared
among the other phases. The stacked bar chart shows it at a glance.

## Before you start

A mineral map or a segmentation of a thin section in RockFace Lab.

## Step by step

1. Open the section in RockFace Lab and go to the **Measurements** tab.
2. In **Transitions between the phases of**, choose the map and press **Compute**.
3. The table (in place of the size classes) has one column per phase: the % of its neighbouring pixels that belong to
   each phase (the rows). The chart shows one bar per phase, stacked by the phases it touches.
4. **Chart (PNG)** keeps the chart as a PNG file.

## How it works

Each pixel is compared with its 8 neighbours over the whole map at full resolution; the contacts of a phase with
itself are left out; each column is divided by its total (GeoSlicer's "transition analysis" of the Segment
Inspector).

## From a script

```python
seg = prj.image("ILLUSTRATIVE mosaic PP (segmentation)")
table = seg.transitions()                 # rf.Table: "phase" and one column per phase, in %
print(table.rows())
```

## Limits and common problems

* "This needs a segmentation or a mineral map": the transitions are computed on maps, not on pictures.
* Phases that do not occur in the map are left out.

## Coverage

GT19 (Segment Inspector: transition analysis; Charts: transition).
