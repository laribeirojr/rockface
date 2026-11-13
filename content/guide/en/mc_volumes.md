# RockFace MC: micro-CT volumes — import, views and processing

## What it is for

RockFace MC keeps the micro-CT volumes of each sample — a plug, a whole core, a cuttings pot — next to its thin
sections and descriptions. It imports the usual formats, stores volumes of any size out of core, shows them in three
slices and in 3D, and crops, filters, resamples, combines and exports them. Every operation writes a new volume with
its history; the original is never changed.

## Before you start

* A saved description: a volume belongs to the description's sample (and may be tied to one of its thin sections).
* Open MC: **Home → Images → MC** (Ctrl+Shift+M) in RockFace Petro, or `rockface mc project.rockface`.

## Step by step

### The window

* **Volumes** on the left, by sample (and the wells with their logs, page [RockFace MC: image logs](mc_image_logs.md)); select one to show it.
* Three slice views (x, y, z) and the **3D view** (**maximum projection**, **mean projection**, or **off**). Click in
  a slice to move the others; the status shows "Voxel x, y, z: value".
* **Window** (grey levels shown) and **Automatic window**; **Overlay** lays a segmented volume over the grey one.
* The tabs: **Import**, **Volume**, **Segmentation**, **Registration**, **Cores**, **Well logs**, **Random forest**,
  **Analyses**, **Pore network**, **Microporosity**, **Multiscale**, **AI**, **More**.

### Importing a volume

1. Open **Import**. **File…** or **Folder…**: a folder of slices, a TESCAN or DICOM folder, a multi-page TIFF, RAW,
   MetaImage (.mhd/.mha), NRRD, NetCDF, HDF5, Amira (.am) or Imperial ASCII (.dat).
2. For RAW: **Size (RAW)** in voxels, **Type (RAW)**, **Byte order (RAW)** (little- or big-endian) and **Header to
   skip (RAW)**. The other formats say it in their header.
3. **Voxel size** (from the file, or typed in µm).
4. **Content**: **grey values** or **segmented**; for a segmented volume, **Values and segments** maps each value of
   the file to a segment.
5. **Sample** and, optionally, the **Thin section**; the **Name**.
6. **Import**. "… imported: nx × ny × nz voxels."

Public micro-CT images can be downloaded with their licence: **Open rock data (public images)…** (page [Open rock data: public micro-CT images](open_rock_data.md)).

### Processing (the Volume tab)

* **Crop (voxels, from – to)** for x, y and z, then **Crop**.
* **Filters**: **Filter** (Gaussian, median, mean, unsharp mask, window to 8 bits, invert, anisotropic diffusion)
  with its parameters, **Add** to the list, **Clear**, **Apply**. Filters run block by block.
* **Shading correction (slice by slice)** — page [Volume tools: filters, shading, segment editor effects, objects, registration, analyses](volume_tools.md).
* **Resample**: **New voxel size**, **Interpolation** (nearest, linear, cubic), **Resample**.
* **Volume calculator**: a **Formula** over the volumes of the same size (listed in "Volumes of this size:"), e.g.
  `(a − b) / 2` or `a > 120` (a condition gives a segmented 0/1 volume); **Calculate**.
* **Export**: **Export…** to .mhd (+ .raw), .mha, .nrrd, .tif or .nc, with the voxel size.
* **Delete volume** (it cannot be undone).

## Options

| Option | What it changes |
|---|---|
| Content | Grey values, or segmented (labels with their segments). |
| Interpolation | Nearest for segmented volumes; linear or cubic for grey values. |
| Window | Only the display; the stored values are not changed. |

## How it works

Volumes are stored in the project as compressed chunks of 64³ voxels with a pyramid of halved levels, so the views
read only what they show and a volume larger than the memory is processed a block at a time: 403 million voxels
were imported and segmented with about 1 GB of memory. Filters block by block equal the whole volume at once; five
formats were read back identical.

## From a script

```python
d = prj["TS-9"]
ct = d.import_volume("plug.mhd")                               # or prj.import_volume(path, d, voxel_um=5.0)
small = ct.crop((0, 400, 0, 400, 0, 400)).resample(factor=0.5)  # box (z0, z1, y0, y1, x0, x1) in voxels
smooth = ct.filter(("median", {"size": 3}), ("gaussian", {"sigma": 0.8}))
diff = prj.calculate_volumes("a - b", {"a": ct, "b": smooth}, name="residual")
print(ct.shape, ct.voxel_um)                                    # (nz, ny, nx), µm
smooth.export("plug_smooth.nrrd")
```

## Limits and common problems

* "Choose a file or folder and a sample."
* A RAW file read with the wrong size or type looks like noise: check the size, type and byte order.
* Very large imports take time; the progress shows and the work can be cancelled.

## Coverage

GV1 (import), GV2 (export), GV3 (crop), GV4 (filters), GV5 (resample), GV8 (large images out of core), GV14 (volume
calculator), L2 (links from samples to tomography).
