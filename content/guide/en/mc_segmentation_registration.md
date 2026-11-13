# RockFace MC: segmentation, porosity and registration of volumes

## What it is for

The **Segmentation** tab cuts the grey values of a micro-CT volume into segments — pore and solid, or more phases —
by typed cuts or by Otsu's method, limited to the cylinder of a plug when needed, and measures the porosity, its
profile along an axis, the connectivity of the pore space and its two-point correlation. The **Registration** tab
aligns two volumes of the same sample, and finds where a thin-section image lies in a volume, adding the matching
slice to the thin section.

## Before you start

A volume in RockFace MC (page [RockFace MC: micro-CT volumes — import, views and processing](mc_volumes.md)), filtered if noisy.

## Step by step

### Segmenting

1. Open **Segmentation** and select the grey volume.
2. **Cuts**: type them, or leave empty for Otsu (**empty: Otsu**); **Segments (Otsu)** gives the number of segments;
   **Find the cuts (Otsu)** shows them on the histogram.
3. **Region**: the **whole volume**, the **cylinder of the plug** (found automatically), or **inside** another
   segmented volume.
4. **Segment**. "Segmented: porosity … %." The darkest segment is the pore. The segmented volume appears under the
   sample, and can be laid over the grey one with **Overlay**.

### Analyses of the segmented volume

* **Porosity** — the porosity of the region, and the porosity of every slice along an axis (**slice along x, y, z**).
* **Connectivity** — along an axis: connected and isolated porosity, the number of pore clusters, and whether the
  pore space crosses the volume.
* **Two-point** — the two-point correlation of the pores along x, y and z, and the correlation length of each.

Effects on the segments (grow, shrink, smooth, logical operations with another segment) are in **Effects on the
segmented volume** (page [Volume tools: filters, shading, segment editor effects, objects, registration, analyses](volume_tools.md)).

### Registering two volumes

1. Open **Registration**. In **Two volumes of the sample**, choose the **Fixed** and the **Moving** volume.
2. **Find the shift (3D phase correlation)**: "Shift found: x, y, z voxels", kept on the moving volume. Tick **Find
   the rotation too (no landmarks)** for a rotated scan (page [Volume tools: filters, shading, segment editor effects, objects, registration, analyses](volume_tools.md)).
3. **Resample the moving volume on the fixed one** writes it on the fixed grid, voxel for voxel.

### A thin-section image in the volume

1. Under **A thin-section image in the volume**, choose the **Image** (a photo or slide of one of the sample's thin
   sections) and **Slices across** (the axis).
2. **Locate the image**. RockFace looks for the slice that shows the image, with its rotation, scale and shift:
   "Slice z = …; rotation …°, … voxels per pixel; ECC …".
3. **Add the matching slice to the thin section**: the slice of the volume is added to the section's images in
   Atlas, laid over the image — the link between the thin section and the tomography.

## Options

| Option | What it changes |
|---|---|
| Cuts / Segments (Otsu) | Where the grey values are cut, typed or by multi-level Otsu. |
| Region | Whole volume, the plug's cylinder, or inside a segmented volume. |
| Slices across | The axis along which the thin section was cut from the plug. |

## How it works

* The porosity of the Berea sandstone of Imperial College London (400³ voxels, 5.345 µm) is 19.645 % against the
  published 19.6 %; a grey scan simulated from it and segmented by Otsu gave 19.54–21.06 %.
* The shift between two volumes is found by 3D phase correlation (a known shift found exactly); landmarks fit a
  rigid, similarity or affine transform.
* A thin-section image is located by a search of slice, angle and scale, refined by the enhanced correlation
  coefficient: pictures of a slice at other pixel sizes and angles (20° to 137°) were placed on the right slice
  within 0.01–0.83 voxel.

## From a script

```python
ct = prj.volume("ILLUSTRATIVE plug")
pores = ct.filter(("median", {"size": 3})).segment(roi="cylinder")          # Otsu, two segments
print(pores.porosity()["porosity"], pores.connectivity("z")["percolates"])
print(pores.profile("z")[:5], pores.two_point()["length_x"])
other = prj.volume("ILLUSTRATIVE plug, second scan")
other.register(ct)                                                           # the automatic shift
aligned = other.resample_on(ct)
found = prj["TS-9"].images("photo")[0].locate_in(ct, axis="z", add_slice=True)
```

## Limits and common problems

* "Choose two different volumes."
* A thin-section image is found only if the volume holds that slice: give the axis across which the section was cut.
* A plug's cylinder is found from the air around it: on a crop without air, use the whole volume or a region.

## Coverage

GV6 (segmentation), GV7 (registration), L2 (links from samples to tomography), L13 in part (2D image → tomography).
