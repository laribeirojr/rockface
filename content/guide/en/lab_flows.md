# RockFace Lab: flows, the whole section and NetCDF

## What it is for

A **flow** runs the whole chain — segmentation, separation into objects, measurement — on one image or on many
(every image of a section, or of the project) in one go, and gives a table with one row per sample and LAS files of
the pore sizes by depth for each well. **Whole section** segments a full thin-section image at full resolution,
block by block. **Import and export** reads and writes label images and NetCDF files to exchange maps with other
programs.

## Before you start

Images of the sections in RockFace Lab; for the PP/XP flow, the XP image of each section; for LAS, descriptions with
a well and a depth.

## Step by step

### A flow

1. Open the **Flows** tab.
2. **Flow**:
   * **PP: pores and grains** — blue-resin segmentation, pores and grains separated and measured;
   * **PP/XP: grains separated by the XP colours** — grains told apart by their extinction colours in crossed
     polars (**XP: merge colours closer than (ΔE*ab)**);
   * **Mineral map (QEMSCAN…): objects of every phase**.
3. **Images of**: **this thin section** or **the whole project**; check the images to use.
4. **Pore separation** (watershed, SNOW, islands), **Minimum distance between centres**, **Objects smaller than
   (dropped)**, **Also separate the grains**.
5. **Run the flow on the checked images**. "Running the flow: image k of n…", then "Flow done on N images (M with
   errors)".
6. The table has one row per sample: well, depth, thin section, porosity, the fractions of the phases, and the
   size statistics. Export it (CSV, XLSX).
7. **LAS curve of the pores** (the size column) and **LAS by depth**: one LAS file per well with the maximum, mean,
   median, minimum and standard deviation of the column and the porosity at each sample depth.

### The whole section

1. Under **Whole section (without machine learning)**, select a picture.
2. **Quantify the whole section** segments it at full resolution, block by block, with the method of the
   Segmentation tab (pixel-by-pixel methods; blue resin otherwise). "…: N pixels counted", with the porosity and
   the share of each segment.

For the whole section segmented by a neural network, see [RockFace AI: segmenting with models, training, fine-tuning and validating](ai_segmentation.md).

### Import and export

* **Import a label image…** (PNG, TIFF) — **Labels as a segmentation map** or **Labels as an object map**.
* **Export the map as labels (TIFF)…**
* **Import NetCDF…** and **Export the section as NetCDF…** — the images and maps of the section with their scale,
  origin and phases (classic NetCDF; NetCDF-4 read).

## Options

| Option | What it changes |
|---|---|
| Flow | PP, PP/XP or mineral map. |
| Images of | One thin section or the whole project. |
| XP: merge colours closer than | Grains whose XP colours differ less than this are one grain. |
| LAS curve of the pores | The size column written to the LAS files. |

## How it works

* The flows use the same functions as the tabs, so a flow gives the result the tabs would give one step at a time.
* Grains separated with the XP colours were found with recall 0.87–0.89, against 0.46–0.51 from PP alone, on
  sections of known grains.
* The whole section is processed block by block with overlapping margins: on a 27 Mpx section the result was
  identical to the whole image at once, and the porosity equal to the truth.
* NetCDF and label TIFF round trips are identical.

## From a script

```python
pp = prj.image("ILLUSTRATIVE mosaic PP")
r = pp.run_flow("pp")
pores, grains = r.measurements
print(r.porosity, grains.summary(exclude_edge=True)["d50_mm"])
results = prj.run_flow(prj.images(kind="slide", modality="pp"), flow="pp")
prj.flow_table(results).to_csv("by_sample.csv")
prj.las_by_depth(results, "las", column="feret_max_um")
seg, fractions, porosity = pp.quantify_whole("resin")
prj.export_netcdf([pp, seg], "section.nc")
```

## Limits and common problems

* "Check at least one image."
* "The section has no XP picture for this image." — the PP/XP flow needs both lights.
* Samples without a well or a depth are in the table but not in the LAS files.

## Coverage

GT14 (LAS per depth, NetCDF), GT15 (predefined flows PP, PP/XP, QEMSCAN), GT16 (multi-image analysis), GT17 (export
and import of standard sources), L7 (quantification of the whole thin section, classical).
