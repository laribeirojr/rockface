# RockFace MC: whole cores and core-box photographs

## What it is for

The **Cores** tab processes the whole-core CT scans of a well in a batch: each core is found in its liner and
centred, given its well and depth, oriented (by the bedding of the first core or by an image log of the well), moved
and turned, unwrapped as an image of its outer surface, laid as one well unwrap and as a CT log, its fractures
filled, and exported. Core-box photographs are cut into their cores and laid by depth as one strip of the well.

## Before you start

* The CT scans imported as grey volumes of a sample of the well (page [RockFace MC: micro-CT volumes — import, views and processing](mc_volumes.md)).
* The top depth of the first core and the core diameter; optionally a table of the top and base of each core (CSV).
* For orientation by an image log: the image log of the well (page [RockFace MC: image logs](mc_image_logs.md)).

## Step by step

### Processing the scans

1. Open **Cores**. Under **Scans of the sample**, check the scans.
2. **Well**, **Top of the first core**, **Core diameter**; **Boundaries (CSV)** (optional: top and base of each core,
   in m).
3. **Correct the radial attenuation (beam hardening)** if the core is brighter at its rim.
4. **Process the cores**. "Finding and centring the cores…", then "N core(s) processed". Each core shows "Core of
   …: top–base m, … mm, rotation …°, shift … m".

### Orientation and position

1. **Orient by**: **bedding of the first core** (the others turned to follow it), or **an image log of the well**
   (choose the **Image log**).
2. **Orient the checked cores**. "Rotations: …".
3. By hand: **Depth shift** and **Rotation**, then **Move and turn the core**.

### Unwrap and logs

1. **Radial depth** (how far inside the surface the unwrap is read), then **Unwrap the core**: an image of the outer
   surface, depth down, azimuth across, laid in the well's logs.
2. **Well diameter** and **Well unwrap**: the checked cores as one unwrap of the well, at the well's diameter.
3. **CT log**: the mean CT value by depth, as a curve of the well.

### Inpainting, export, flow

* **Fractures (segmented volume)** and **Fill the fractures**: the fractures of a segmented core filled slice by
  slice.
* **Export the checked cores…**: an HTML summary, the CSV matrix and the Techlog form with depth, the PNG unwrap, the
  TIFF volume. "N files written in …".
* **Core flow: core → segmentation**: import → core → crop → segmentation and porosity, in one go.

### Core-box photographs

1. Under **Core box photographs**, **Add photographs…** and give each its **Top (m)** and **Base (m)**.
2. **Channels per box** (rows of cores in a box), or **automatic**.
3. **Make the strip**: the rows of cores are found by the background colour, cut, and laid end to end by depth as
   one strip of the well.

## Options

| Option | What it changes |
|---|---|
| Correct the radial attenuation | Removes the beam-hardening brightening of the rim. |
| Orient by | The bedding of the first core, or an image log. |
| Radial depth | Depth inside the surface at which the unwrap is read (mm). |
| Channels per box | The number of rows of cores in each box photograph. |

## How it works

* The liner and the core are found as circles in the slices; on the ILLUSTRATIVE well the core radius was found at
  49.6–49.7 mm for 50 mm, and on a real whole-core CT (internal test) the core inside the liner at 130.4 mm.
* Orientation by the bedding fits the dominant sinusoid of each core's unwrap; by an image log, it correlates the
  depth gradients of the unwrap and the log: within 0.1° and 2 mm on the ILLUSTRATIVE well.
* Core-box photographs made a strip exactly on the ILLUSTRATIVE well.

## From a script

```python
scans = prj["TS-9"].volumes()                                 # the CT scans of the sample, top to base
cores = [prj.process_core(v, 2500.0 + 0.9 * k, 100.0, well="W-1") for k, v in enumerate(scans)]
print(cores[0].core["diameter_mm"], cores[0].core["top_m"])
prj.orient_cores(cores, "sinusoid")                            # or "image_log", log=prj.log("AMP")
unwrap = cores[0].unwrap(radial_depth_mm=1.0)
well_unwrap = prj.well_unwrap(cores, well_diameter_mm=216)
ct = prj.ct_log(cores)
prj.export_cores(cores, "cores_out")
strip = prj.load_core_photos("W-1", [("box1.jpg", 2500.0, 2503.0), ("box2.jpg", 2503.0, 2506.0)])
```

## Limits and common problems

* "Check at least one scan or core."
* "Give the top and base depth of every photograph."
* A core touching its liner may be found as the liner: check the diameter shown, and give the core diameter.

## Coverage

GC1 (multicore), GC2 (core photograph loader), GC3 (crop), GC4 (multicore transformations), GC5 (segmentation),
GC6 (core inpainting), GC7 (export), GC8 (flows), GI2 (unwraps of processed cores).
