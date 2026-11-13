# A mineral map aligned without landmarks; effects on big volumes

## What it is for

Two details found by the 0.23 audit and closed in 0.28. **A mineral map aligned on a segmentation of the picture**
without clicking landmark pairs (GeoSlicer's Thin Section Auto Registration). **The effects of the segment editor on
big volumes** — margin, smoothing, boundary removal and expand — at full resolution, slab by slab, instead of on a
reduced level (GeoSlicer's Big Image effects).

## Before you start

* Alignment: a segmentation of the picture (Lab → Segmentation) and the mineral map of the same thin section, both
  with a pore phase (phase role "Pore"), or with phases that show the same boundaries.
* Effects: a segmented volume in MC.

## Step by step

1. **Lab → Registration**: choose the segmentation as *Fixed image* and the mineral map (marked "map") as *Moving
   image*; **Automatic** (with *Search (automatic)* "shift", "any rotation" or "rotation and scale" when the two have no common
   section frame); **Save the registration**. The map is then laid over the picture in Atlas and Lab.
2. **MC → Segmentation → Effects on the segmented volume**: nothing changes for the user — a volume too big to be held whole is now edited at
   full resolution, a few planes at a time.

## How it works

* Alignment: the pores of each map (or, without pores, the boundaries between any two phases) become a grey image;
  the two are aligned by ECC on their gradients over a pyramid (Evangelidis & Psarakis 2008), starting from the
  section frames or from the search, as Lab aligns two pictures (0.17).
* Effects: each slab of planes is read with the margin in z the effect needs (the margin or the width plus one
  plane, the smoothing size plus one) and cut back after the effect — the same result as on the whole volume. For
  *expand* the nearest segment is looked for within the slab and 16 planes around it (`halo`).

## From a script

```python
t = prj.image("Mineral map").register_on("Segmentation", search="shift")    # two maps: by their pores
rf.lab.register_map(prj.raw, seg_id, map_id, fixed_phases=[1], map_phases=[3])
rf.vol_tools.edit_labels(prj.raw, labels_id, "boundary_removal", width=2)    # big volumes: slab by slab
```

## Limits and common problems

* The phases chosen must be the same thing in both maps (pores of the picture and the porosity of the map); with
  very different phase sets use landmark pairs.
* Islands, logical operations, grow from seeds and level tracing still work on a reduced level of very big volumes:
  they need the whole volume at once.

## Coverage

0.23 audit rows ThinSectionAutoRegistration (GT5), BoundaryRemovalBigImage and ExpandSegmentsBigImage (GV6, GV8).
