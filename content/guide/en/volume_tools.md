# Volume tools: filters, shading, segment editor effects, objects, registration, analyses

## What it is for

The tools of RockFace MC that prepare a micro-CT volume, correct its segmentation and measure it: an edge-preserving
filter, the correction of the shading (beam hardening), the effects of a segment editor, the separation of the pore
space into objects, the registration of two scans turned with respect to each other, and the variogram, the
representative elementary volume and the attributes of a volume.

## Before you start

A volume open in RockFace MC. Every tool writes a **new** volume; the original is never changed.

## Step by step

### Anisotropic diffusion (Volume tab)

1. **Volume → Filters**, choose **Anisotropic diffusion (edge-preserving)**.
2. Set **Conductance** (lower keeps more edges) and **Iterations** (more smooths more), press **Add**, then
   **Apply**.

### Shading correction (Volume tab)

1. **Shading correction (slice by slice)**: choose where the background is fitted — **The whole slice**, the
   cylinder of the plug, or inside a segmented volume.
2. Optional: **Smoothing along the slices** (in slices).
3. Press **Correct the shading**.

### Effects on the segmented volume (Segmentation tab)

Open a segmented volume. In **Effects on the segmented volume** choose the **Effect**, the **Segment** and, when
asked, the **Other segment**, the **Voxels / size / tolerance** or the **Region or grey volume**, then **Apply the
effect (new volume)**:

* **Margin** grows (positive voxels) or shrinks (negative) a segment;
* **Smoothing** removes the roughness of a segment;
* **Islands** removes the pieces smaller than the size given;
* **Logical operators** add, subtract, intersect, copy, invert or clear segments;
* **Mask** keeps only what is inside another segmented volume;
* **Expand segments** fills the voxels at 0 with the nearest segment;
* **Boundary removal** empties the voxels where two segments touch;
* **Grow from seeds** grows the painted voxels of an annotation over a grey volume;
* **Level tracing from the crosshair** takes the connected voxels of a grey volume close to the value under the
  crosshair.

### Objects of the pore space (Analyses tab)

1. Open a segmented volume. In **Objects of the pore space** choose **Separated by**: *Watershed of the distance map*
   (touching pores are split) or *Connected pieces*.
2. Set **Smallest distance between centres** and **Smallest object**, press **Separate into objects**.
3. The table lists every object: voxels, volume, equivalent diameter, axes, centroid, the radius of the largest
   inscribed sphere, and whether it touches the border.

### Registration with rotation (Registration tab)

Choose the **Fixed** and **Moving** volumes, tick **Find the rotation too (no landmarks)** and press **Find the shift
(3D phase correlation)**. The rotation (about x, y, z) and the shift are kept on the moving volume; **Resample the
moving volume on the fixed one** writes it on the fixed grid.

### Variogram, REV and attributes (Analyses tab)

* **Variogram (x, y, z, all directions)**: the semivariogram of a grey volume, or of the pores of a segmented one,
  with the fitted model (range, sill, nugget) in the table.
* **Representative elementary volume**: the standard deviation of the mean of random cubes of growing edge; the REV
  is where the curve levels off.
* **Report (HTML)…** writes the plots and tables in one page.
* **Show the attributes** lists size, voxel, values, history; **Import a PCR file…** adds the reconstruction
  parameters of the scanner (the Min and Max of the grey scale).

The **Table** of the tab is filtered by an expression (`voxels > 100 and not border`), exported to CSV or Excel, and
shows the histogram of the chosen column.

## How it works

* Anisotropic diffusion: Perona & Malik (1990); the conductance is scaled by the root mean square of the gradient,
  as in ITK's gradient anisotropic diffusion. Computed block by block, the same as the whole volume.
* Shading: on each slice, a second-degree polynomial f(x, y) is fitted to random points of the mask and the slice
  becomes s / f · M (M the mean of the mask).
* Objects: the watershed (Vincent & Soille 1991) of the smoothed distance map, one marker per local maximum.
* Rotation: a search of the angle about z with the 3D phase correlation of the shift, then the six parameters
  refined by the normalized cross-correlation.
* Variogram: Matheron (1963); spherical model; with a region, only the pairs with both ends inside it count.

## From a script

```python
vol = prj.volume("Plug A")
smooth = vol.filter(("anisotropic", {"conductance": 1.0, "iterations": 5}))
flat = vol.shading_correction("cylinder")
seg = flat.segment()
objects = seg.partition(min_distance=4)
rows = objects.objects()
t = prj.volume("Plug A, second scan").register_rigid(vol)
v = seg.variogram()
seg.variogram_report("variogram.html")
bigger = seg.edit("margin", segment=1, voxels=2)
```

## Limits and common problems

* The effects and the objects work on the whole volume in memory: above 64 million voxels they work at a reduced
  level of the volume.
* The rotation search assumes the same voxel size in both volumes.
* The Gabor, Minkowski and variogram-range features of GeoSlicer's segmenter are not offered.

## Coverage

GV4, GV6, GV7, GV14 (Filters, Polynomial Shading Correction, Segment Editor, Segment Inspector, Register, Variogram
Analysis, Attribute Tools, Tables).
