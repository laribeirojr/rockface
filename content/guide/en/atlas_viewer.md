# RockFace Atlas: whole slides, detail photos and the image library

## What it is for

RockFace Atlas keeps the images of each thin section: whole-slide images of any size (a scanner's multi-gigapixel
slide, a microscope mosaic) in several lights, and detail photos placed at their exact position on the section,
with the stage position where they were taken. The **image library** finds any image of the project by its name,
caption, well, section, kind, light or objective, and the viewer zooms from the whole section to full resolution at
once.

## Before you start

* A **saved** description: images belong to its thin section ("Save a description first: images belong to its
  thin section.").
* Image files: PNG, JPEG, TIFF, BigTIFF, OME-TIFF, BMP, GIF, WebP; scanner formats (SVS, NDPI, MRXS, SCN) with
  OpenSlide installed; Zeiss CZI with the `czi` extra.

## Step by step

### Opening Atlas

**Home → Images → Atlas** (Ctrl+Shift+A) in RockFace Petro opens Atlas on the same project and thin section; or
`rockface atlas project.rockface`.

### Importing a whole slide

1. **Import…** (Ctrl+I) and choose the files.
2. In **Import images**, check the **Thin section**, the **Kind** (whole slide), the **Category** (microscope
   mosaic, slide scanner, photomicrograph, macroscopic photo, other) and the **Light / signal** (plane-polarized,
   crossed polars, reflected, cathodoluminescence, ultraviolet, fluorescence, SEM, other).
3. Scale: **µm per pixel** — from the file when it carries it, else typed, else from the **Objective** and the
   table of **Objectives…**.
4. **Tiles**: **JPEG** (photographs; smaller) or **PNG** (lossless; maps).
5. **OK**. "Building the image pyramid…" shows the progress; a very large image takes a while, once.

### Detail photos

1. **Detail photo…**: choose the photo, its **Objective**, light, and, when known, its **Position x, y (mm)** on the
   section and the **Stage x, y (mm)** where it was taken.
2. Or place it afterwards: select it under **Detail photos**, choose the tool **Place photo**, and click where it
   is on the whole slide.
3. **Show on the slide** frames the photo's field; **Open** shows the photo itself; **Stage to this field** sends
   the stage (or the simulator) back to where it was taken.
4. **Retake…** adds a new photo of the same field, with the same position, stage position and objective, linked to
   the first ("N photos of this field").

### The viewer

* Drag to pan; the mouse wheel zooms. **Fit**, **1:1**, **Zoom in**, **Zoom out**.
* **Over it:** lays another image of the section over the one open (XP over PP, CL, a mineral map), with the
  **Opacity of the image laid over**.
* Show or hide **Photos** (the fields of the detail photos, numbered), the **Scale bar**, the **Overview** map and
  the **Round section** outline.
* **Counted points of:** shows the points counted in a description, coloured by constituent (page [Point counting](point_counting.md)).
* **Tools**: **Measure** (click two points: the distance in µm), **Calibrate** (click two points and give their
  distance: sets the scale), **Place photo**, **Spot** (page [Spot analyses: geochemistry, dating and fluid inclusions](spot_analyses.md)).
* **Export view…** saves what is shown, or the whole image, as PNG, JPEG or TIFF.

### The image library

1. The **Image library** lists every image of the project. Type in **Search names, captions, wells, sections…**.
2. **Filters**: kind, category, light, objective and **Well or outcrop**; **Only this thin section**.
3. **By concept** finds images by what their annotations show (page [Atlas annotations and the search by concept](atlas_annotations.md)).
4. Select an image to see and edit its **Name**, kind, category, light, objective, scale and **Caption**; **Save
   changes**. **Read scale bar** finds the scale bar burnt into a picture and reads its length (OCR).
5. **Delete image** removes the image and its tiles from the project.

## Options

| Field | What it changes |
|---|---|
| Objectives… | µm per pixel of the camera for each objective, measured once on a stage micrometer. |
| Tiles | JPEG (smaller, for photographs) or PNG (lossless, for maps and labels). |
| Position x, y (mm) | Where the photo lies on the section (its centre), in the section frame. |
| Stage x, y (mm) | Where the stage was when the photo was taken (to come back to it). |

## How it works

Each image is stored in the project as a pyramid of tiles: only the tiles on the screen are read, at the level that
matches the zoom, so a 2-gigapixel section opens in a fraction of a second and pans without waiting. Every image
has its place in the section frame (millimetres), shared with the point count, the annotations, the mineral maps
and the spot analyses: what is at a point on one image is at the same point on the others.

## From a script

```python
d = prj["TS-9"]
slide = d.add_image("TS-9_PP.tif", category="scanner", modality="pp")
photo = d.add_photo("field1.jpg", x_mm=4.2, y_mm=3.6, magnification=10, stage_x_mm=31.2, stage_y_mm=24.6)
slide.overview("TS-9_fields.png", width=2400)               # the slide with the photo fields numbered
crop = slide.region(*slide.to_px(4.0, 3.4), 400, 300)      # a NumPy array at full resolution
for img in prj.images(kind="photo", modality="xp", well="ILLUSTRATIVE W-1"):
    print(img.name, img.um_per_px, img.x_mm, img.y_mm)
prj.objectives = {"10": 0.65, "20": 0.325}                 # µm per pixel for each objective
```

## Limits and common problems

* "This thin section has no whole-slide image." — photos can still be imported, and placed later.
* "The stage position of this photo is not known." — Stage to this field needs the stage position.
* "A scale needs two different points and a length above zero."
* Moving several gigabytes of images to another project: **Save project as…** is faster than an exchange file.

## Coverage

R1 (database of photomicrographs with fast queries), GT1 (thin-section images with scale), GT21 (CZI and the scale
bar), L6 (photos taken again at the same referenced position).
