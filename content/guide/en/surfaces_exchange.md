# 3D surfaces, saving into an existing NetCDF file and the Geolog package

## What it is for

Three exchange tools of the **Multiscale** tab of RockFace MC:

* **3D surfaces**: the photogrammetry models of cores, plugs and outcrops (Wavefront OBJ with its MTL materials and
  texture pictures) kept in the project and shown in 3D, and the surface of a segment of a volume made and written as
  OBJ.
* **Save into an existing NetCDF file**: the volumes made in RockFace written as new variables of the NetCDF file the
  data came from, which keeps everything it held (its attributes, dimensions and other variables).
* **Geolog (files)**: the logs of a well written as a package that Geolog loads with its own LAS and DLIS loaders, and
  the files that Geolog writes read back, with their null values.

## Before you start

* A surface: an `.obj` file (with its `.mtl` and pictures in the same folder), or a segmented volume.
* NetCDF: an existing classic NetCDF file (or a NetCDF-4 file, with h5py installed) and the volume to save.
* Geolog: the logs of a well (Well logs tab); DLIS files are written when `dliswriter` is installed and read when
  `dlisio` is installed; LAS always.

## Step by step

### 3D surfaces

1. In **3D surfaces**, type the **mm per unit of the OBJ file** (1 when the model is in mm; 1000 when in metres) and
   click **Import OBJ…**. The surface is kept with the current sample and shown: drag to turn, wheel to zoom.
2. To make one from a volume, open a segmentation, choose the **Segment** and click **From the segment**.
3. **Export OBJ…** writes the OBJ, its MTL and the textures as PNG; **Delete the surface** removes it.

### Save into a NetCDF file

1. Open the volume to save, and in **Save into an existing NetCDF file** choose the **NetCDF file**.
2. Tick **Replace a variable of the same name** to overwrite one; otherwise a new name is given (`_2`, `_3`…).
3. Click **Save the current volume into the file**. A volume of the same shape as a variable of the file takes its
   dimensions, so it lines up with the image it came from.

### Geolog

1. In **Geolog (files)** choose the **Well** and click **Write a package for Geolog…**, then a folder: one LAS per
   image log, one LAS per depth grid for the curves, a DLIS with every log, `rockface_geolog.json` and
   `README_geolog.txt`.
2. To read Geolog's files, type the **Null values** (−999.25; −999; −9999; −99999 by default) and the hole
   **Diameter**, and click **Read files from Geolog…** on the folder (or a file).

## Options

| Field | What it changes |
|---|---|
| mm per unit of the OBJ file | Scale of the vertices to mm |
| Replace a variable of the same name | Overwrite instead of adding a suffix |
| Null values | Values read as missing in the LAS and DLIS files, besides the NULL of each LAS file |
| Diameter | Hole diameter set on the image logs read |

## How it works

* **OBJ/MTL**: vertices (with optional per-vertex colours), texture coordinates, normals, faces of any number of
  sides split into triangles, negative indices, `usemtl` and `mtllib`; materials with `Kd`, `d` and `map_Kd`. A
  vertex used with two texture coordinates becomes two vertices. The view draws the faces from the back (painter's
  algorithm) with the colour of the texture at their centre and Lambert shading; heavy meshes are reduced for the view
  by vertex clustering (Rossignac & Borrel 1993). From a volume, the surface is made by marching cubes (Lorensen &
  Cline 1987) after a light Gaussian smoothing of the mask (area of a sphere within 0.5 %).
* **NetCDF**: a classic file is rewritten through a temporary file with all it held plus the new variables, then
  replaced; a NetCDF-4 file is appended in place and the dimension scales of the matching variable are attached.
* **Geolog**: mnemonics upper case, letters, digits and underscore, at most 32 characters, unique; the manifest keeps
  what LAS cannot (kinds, segment legends, azimuths, diameter) so the package comes back to RockFace whole.

## From a script

```python
s = prj.import_surface("core_box.obj", sample, scale_mm=1000)
s.render("core_box.png")
prj.volume("plug segmentation").save_into_netcdf("plug.nc")
prj.geolog_export("Well A", "to_geolog")
logs = prj.geolog_import("from_geolog", "Well A", nulls=(-999.25, -9999))
```

## Limits and common problems

* The view shows one colour per face; very fine textures on large faces look flat (the OBJ written keeps the texture
  whole).
* Classic NetCDF files above 2 GB need the 64-bit offset format, which the rewrite keeps; NetCDF-4 needs h5py.
* RockFace does not open a Geolog project itself: the exchange is by files, which Geolog loads and writes.

## Coverage

GV18 (textured 3D surfaces), GV15 (saving into an existing NetCDF file), GM1 (Geolog integration), GM2 (import and
export tools).
