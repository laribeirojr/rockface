# RockFace MC: image logs

## What it is for

The **Well logs** tab keeps the image logs of a well — acoustic amplitude and transit time, resistivity,
conductivity, core unwraps, CT logs — with its curves, on one depth axis. It imports and exports the usual formats,
crops and processes them (eccentricity, spiral filter, quality and heterogeneity, azimuth shift, CLAHE), fills their
gaps (inpainting), segments them into vugs with their sizes by depth, fits the sinusoids of planar features, and lays
core unwraps on the image log.

## Before you start

* The log files: LAS 2.0 (with stacked image curves), CSV (matrix, Techlog, long form; also gzipped), NetCDF or GMT
  grids, DLIS (with the optional `dlis` extra), a picture with its top and base depths, or a folder of core
  unwraps.
* The well's name; the hole diameter, for lengths in millimetres.

## Step by step

### Importing

1. Open **Well logs**. **File or folder** (LAS, CSV, NetCDF/grd, DLIS, picture, folder of unwraps).
2. **Well**, **Hole diameter**, **Measurement** (acoustic amplitude, transit time, resistivity, conductivity, CT,
   photograph, other); for a picture, its **Picture top and base**.
3. **Import**. "N log(s) imported." The wells and their logs appear in the left panel; the tracks are shown side by
   side on one depth axis, with a **Palette**.

### Crop and processing

1. **Depths** and **Crop**.
2. **Process** — choose one, with its parameters, then **Apply**:
   * **Eccentricity** — corrects the amplitude of a tool off the centre of the hole, using the **Transit-time log**;
   * **Spiral filter** — removes the spiral pattern of the tool (**Shortest** and **Longest wavelength (m)**);
     "Filtered: …% of the image changed";
   * **Quality indicator** and **Heterogeneity index** — curves by depth (**Window (m)**);
   * **Azimuth shift** — turns the image by an **Azimuth deviation curve**;
   * **CLAHE** — local contrast (**Clip limit**).

### Unwrap registration and inpainting

1. **Core unwrap** and **Largest depth shift**, then **Lay the unwrap on the image log**: "Unwrap moved … m and
   turned …° (correlation …)".
2. **Inpainting**: **linear (row by row)**, **harmonic (smooth)** or **biharmonic**; **Also fill (segmented log)**
   for a mask; **Fill the gaps** — the pad gaps of the tool and the masked areas are filled.

### Segmentation, objects and pore sizes

1. **Cuts** (empty: Otsu), then **Segment**.
2. **Objects**: the vugs as objects across the 0/360° seam (**Smallest object**): "N objects; equivalent diameter
   mean … mm, largest … mm", with their table.
3. **Pore sizes**: the local thickness of the pore space in mm and its histograms by **Depth interval**.

### Planar features

1. **Pick points**: click at least three points of a bedding plane or fracture on the image track.
2. **Fit the sinusoid**: "Plane at … m: dip …° toward …°".
3. **Dominant fabric**: the dominant sinusoid of the depths on screen.

### Export

**Export…** writes LAS, CSV (matrix or Techlog), NetCDF, PNG/TIFF or DLIS (with the optional dliswriter).

## Options

| Option | What it changes |
|---|---|
| Measurement | What the log is; amplitude and transit time go together for the eccentricity. |
| Inpainting | Linear (fast), harmonic (smooth), biharmonic (follows gradients). |
| Smallest object | Vugs smaller than this are left out. |

## How it works

* Logs are stored by depth with a pyramid, so long wells are shown at once.
* On the ILLUSTRATIVE well (dipping beds and vugs of known truth): dominant fabric 25.0°/120.0° exact; a hidden pad
  filled with RMSE 0.043–0.050 against 0.083 for the row mean; 38 of 40 vugs found.
* On a real FMI log (internal test): a hidden pad filled with RMSE 14.97 (linear) against 29.07 for the row mean;
  two passes matched within 0.8 mm.
* Editing log segmentations by brush and reviewing objects: page [Editing a log segmentation and its objects](log_editing.md); permeability model
  of segmented logs: page [Permeability model of image logs](permeability_model.md).

## From a script

```python
amp, tt = prj.import_log("amplitude.las", "W-1", diameter_mm=216)[:2]
(fixed, tau, _), = amp.eccentricity(tt)
clean, changed = fixed.inpaint(method="biharmonic").spiral_filter(4, 20)
print(clean.dominant_sinusoid(2501, 2510).dip_deg)
vugs, table = clean.segment().objects(min_px=6)
table.to_csv("vugs.csv")
clean.export("clean.las")
```

## Limits and common problems

* "Choose a file or folder."
* "No log to show." — the well has no log yet, or none in the depths shown.
* DLIS needs the `dlis` extra (dlisio, LGPL, loaded only when used).

## Coverage

GI1 (import), GI2 (unwrap), GI3 (export), GI4 (crop), GI5 (processing), GI6 (unwrap registration), GI7
(inpainting), GI8 (segmentation, planar features), GI9 (pore-size distribution).
