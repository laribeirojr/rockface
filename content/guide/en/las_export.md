# Wells to LAS

## What it is for

The descriptions of a well, written as a **LAS 2.0** file — one per well — so that reservoir-modelling programs such
as Petrel, Techlog or Geolog read the petrography as curves against depth: porosity and permeability, totals,
classifications, facies… Text attributes become discrete curves with their code tables.

## Before you start

* Descriptions with a well and a depth.
* Optional: a query in Explorer, to write only the descriptions found.

## Step by step

1. In RockFace Explorer, **Export → Wells to LAS (Petrel)…**. The **Wells to LAS 2.0** dialog opens.
2. **Depth of the samples**: measured (top), corrected or adjusted.
3. **Company** — written in the header.
4. **Only the N descriptions found by the query**, or every description.
5. **Curves (one value per sample depth)**: tick the attributes to write (porosity, permeability, grain density,
   totals, classifications, facies, zone…). Each has its mnemonic and unit.
6. **First file** shows the beginning of the first file, to check.
7. **Write…** and choose the folder. "N LAS files written in …".

## Options

| Option | What it changes |
|---|---|
| Depth of the samples | Which depth of the identification is the DEPT curve. |
| Curves | Numeric curves, or discrete curves for text attributes (integer codes with their table). |

## How it works

* One LAS 2.0 file per well, with an irregular depth step (`STEP 0`) and `NULL -999.25`.
* Text attributes (facies, a classification) become discrete curves of integer codes; the code table is written in
  the Parameter and Other sections.
* Two samples at the same depth are merged.
* The files were checked with two independent readers (lasio and W. Weckesser's LASReader): every value equals the
  record, the required header items are present and lasio gives no warning.

## From a script

```python
prj.export_las("las", ("identification", "formation", "Example Carbonate Unit"),
               curves=["petrophysics.porosity", "petrophysics.permeability", rf.Curve("totals.qt", "QT", "%"),
                       "identification.facies"],
               depth="corrected_depth", company="ILLUSTRATIVE")
las = rf.las.read("las/ILLUSTRATIVE-A1.las")             # read a LAS 2.0 file back
```

## Limits and common problems

* "No sample with this depth." — the depth chosen is empty for these samples (for example no adjusted depth).
* Samples without a well are left out.
* For image logs and curves of RockFace MC, see [RockFace MC: image logs](mc_image_logs.md) (LAS, CSV, DLIS, NetCDF) and the WITSML export (page
  [Exporting wells to WITSML and samples to OSDU](exports.md)).

## Coverage

P38 (export to LAS for reservoir-modelling software), L4 (LAS exporter to Petrel).
