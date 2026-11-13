# Files of the reference programs

## What it is for

RockFace opens the files that GeoSlicer and the laboratories hand over, so nothing has to be converted first:
micro-CT volumes from Amira/Avizo, HDF5, DICOM series and TESCAN reconstructions; Zeiss CZI thin-section scans;
GeoSlicer scenes and segmentations; the tables of laboratory reports in PDF; and the scale bar burnt into a
microscope picture.

## Before you start

* A project with a sample (volumes) or a thin section (images).
* Optional packages, installed once: `pip install rockface[formats]` (HDF5, DICOM, PDF, OCR) and, for CZI,
  `pip install rockface[czi]`. OCR also needs the Tesseract program.

## Step by step

1. **Volumes — MC → Import.** Choose the file or folder: `.am`, `.h5`/`.hdf5`, a `.dcm` file or a DICOM folder, a
   TESCAN folder (with `*.acq.1.xml` and `recon/`), or a GeoSlicer scene `.mrml` or segmentation `.seg.nrrd`. Click
   **Import**.
2. **Volumes out — MC → Volume → Export** now also writes `.am`, `.h5` and, for a segmentation, `.seg.nrrd`.
3. **CZI — Atlas → Import** a `.czi` like any slide.
4. **Lab report — Petro → Home → Import lab report (PDF)…**: choose the PDF, the well and the depth tolerance;
   each row becomes a conventional petrophysics analysis of the sample at that depth.
5. **Scale bar — Atlas → image properties → Read scale bar**: the bar is found and its length read; if the text
   cannot be read, type the length.

## Options

| Format | What RockFace reads |
|---|---|
| Amira `.am` | binary (little or big endian) or ASCII; byte to double; raw, HxByteRLE or HxZip; voxel from BoundingBox and Units |
| HDF5 | any 3D dataset (the largest by default); voxel from `voxel_um`, `spacing` + `units`, `element_size_um` |
| DICOM | the largest series of a folder, slices ordered along their normal, Hounsfield units; no patient fields kept |
| TESCAN | the slices of `recon/`, voxel = VoxelSize (mm) of `*.rec.1.xml`, origin from `*.acq.1.xml` |
| `_NNNNNnm` in a name | voxel size in nanometres when the file gives none |
| CZI | the first scene, RGB or grey, µm per pixel from the scaling |
| `.mrml`, `.seg.nrrd` | volumes, label maps and segmentations (3D or layered) with their segment names and colours |
| Lab report PDF | depth, diameter, length, mass, permeability, porosity, grain density (PT, EN, ES headings; comma or point) |

## How it works

* Each reader turns the file into a volume source read slab by slab, so large files stay out of memory; the
  voxel size comes from the file, else from the name, else from the import form.
* Lab reports: ruled tables are read by their lines; tables of aligned text by the columns of the numbers; the
  headings are matched by their words (*Profundidade*, *Permeabilidade*, *Massa específica*…).
* Scale bar: the longest solid horizontal bar that contrasts with its surroundings, then the text next to it read
  by Tesseract ("500 µm", "0.5 mm"); µm per pixel = length ÷ bar pixels.

## From a script

```python
src = rf.volume.open_volume("scan.am")                        # or .h5, a DICOM or TESCAN folder
v = rf.volume.add_volume(prj.raw, src, sample_id)
rf.volume.export(prj.raw, v.id, "out.seg.nrrd")               # a labels volume for GeoSlicer
rf.geoslicer.import_scene(prj.raw, "project.mrml", sample_id)
prj.import_lab_report("rca.pdf", "ILL-WELL-1", tolerance_m=0.1)
rf.atlas.read_scale_bar(prj.raw, image_id)                    # Scale(bar, text, value_um, um_per_px)
```

## Limits and common problems

* CZI needs pylibCZIrw (LGPL-3.0, optional, like OpenSlide for other slide formats).
* A lab report whose table is an image (a scan) has no text: run OCR on the PDF first.
* Without units, an Amira bounding box is guessed from the voxel size (metres, millimetres or micrometres); the
  guess is written in the volume's history.

## Coverage

GV1 and GT1 formats (0.28), GC1 DICOM, GI lab-report tables, GT scale bar; GeoSlicer audit of 0.28.
