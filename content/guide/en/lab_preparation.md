# RockFace Lab: crop, filters and the sample mask

## What it is for

RockFace Lab prepares the images of a thin section for analysis. **Crop** cuts every image of the section to the
same rectangle, keeping its place in the section. **Filters** improve an image — brightness and contrast,
saturation, gamma, levels, histogram equalization, shading correction, smoothing, sharpening — with a preview. The
**Sample mask** finds the useful area of the section (the rock, without the glass and the borders) and splits it
into fragments.

## Before you start

* A thin section with images in RockFace Atlas (page [RockFace Atlas: whole slides, detail photos and the image library](atlas_viewer.md)).
* Open Lab: **Home → Images → Lab** (Ctrl+Shift+L) in RockFace Petro, or `rockface lab project.rockface`.

## Step by step

### The window

* **Thin section:** at the top chooses the section; **Images of the section** lists its images (originals and those
  made by Lab, with what made them).
* The viewer shows the image selected: **Fit**, **1:1**, **Zoom in**, **Zoom out**.
* The tabs on the right: **Crop**, **Filters**, **Sample mask**, **Registration**, **Calculator**, **Segmentation**,
  **Edit and objects**, **Measurements**, **Flows**, **AI**.

Every tool writes a **new image** of the section; the original is never changed.

### Crop

1. Open **Crop**. Give the rectangle in the section frame: **Left (mm)**, **Top (mm)**, **Right (mm)**, **Bottom
   (mm)**, or:
   * **Draw on the image** — drag a rectangle;
   * **Whole image**; **Box of the sample mask**;
   * a rectangle from **Saved regions** or **Last used**.
2. **Name of the region** and **Save region** keep it for the next sections; **Delete region**.
3. In **Images to crop**, check the images (PP, XP, a map…). Each is cropped to the part it covers.
4. **Crop the checked images**. "N cropped image(s) added to the section."

### Filters

1. Open **Filters** and choose the image.
2. **Add** a filter to the list:
   * **Brightness and contrast**, **Saturation**, **Gamma**;
   * **Automatic levels** (**Low** and **High percentile**, channels joint or each);
   * **Histogram equalization**;
   * **Shading correction** (uneven lighting: **Reference** resin, bright, all, mask or flat; **Surface degree**;
     **Largest gain**);
   * **Gaussian smoothing** (**Sigma (px)**), **Median filter** (**Size (px)**), **Unsharp mask (sharpen)**
     (**Sigma**, **Amount**);
   * **Paint outside the sample** (with a mask **Image** and its **Fill**).
3. The filters run in order: **Up**, **Down**, **Remove**, **Undo**, **Redo**. The viewer shows the result at
   once; **Show the original** compares.
4. **Name of the new image**, then **Write as a new image**. "Filtered image added: …".

### Sample mask

1. Open **Sample mask**. The mask is found **by colour (blue resin)** or **by samples drawn on the image**: **Draw
   rock sample** and **Draw resin sample** on the image ("Samples: N rock pixels, M resin pixels").
2. **Split into fragments** by the resin between them: **Resin wider than**, **Keep the largest** (N fragments, or
   all), **Smoothing**, **Smallest area**.
3. **Find the sample**. "Sample: …% of the image, N fragment(s)". "No glass or border found: the whole image is the
   sample." when the image is all rock.
4. **Name of the mask**, then **Keep the mask**. The mask is used by Crop (**Box of the sample mask**), by **Paint
   outside the sample**, by the segmentation and by the measurements.

## Options

| Option | What it changes |
|---|---|
| Shading correction — Reference | What should be even: the resin, the bright areas, all of the image, a mask, or a flat-field image. |
| Automatic levels — Channels | Stretch the three channels together (keeps the colours) or each apart. |
| Resin wider than | The narrowest resin gap that separates two fragments (fraction of the shorter side). |

## How it works

* Brightness, contrast and saturation give exactly what Pillow's ImageEnhance gives, and the histogram equalization
  of the luminance exactly what OpenCV gives (checked on 26 images, 20 of them real thin-section patches).
* Filters are applied block by block, so a whole section of any size is filtered with little memory, and the result
  is the same as filtering the whole image at once.
* The shading correction fits a polynomial surface to the reference (the resin by default) and divides it out: an
  unevenness of 0.086–0.130 was brought back to 0.021 on test sections.
* The sample mask finds the glass and the borders by colour and texture; on PP and XP sections it matched the true
  mask with IoU 0.97–0.9996.

## From a script

```python
pp, xp = prj.image("ILLUSTRATIVE mosaic PP"), prj.image("ILLUSTRATIVE mosaic XP")
pp_c, xp_c = prj.crop([pp, xp], roi=(2.0, 2.0, 8.0, 6.0))          # mm of the section frame
better = pp_c.filter(["shading", ("brightness_contrast", {"contrast": 20}), ("unsharp", {"sigma": 1.5})])
mask = pp.sample_mask(split=True, n_largest=2)
print(mask.areas_mm2())
prj.save_roi("Centre", (2.0, 2.0, 8.0, 6.0))
```

## Limits and common problems

* "Give a rectangle to crop." / "Check at least one image."
* "The section has no sample mask yet (Sample mask tab)."
* On a section without blue resin, find the mask **by samples drawn on the image**.

## Coverage

GT3 (crop), GT4 (enhancement filters), GT6 (sample foreground: useful area, fragments, keep the N largest).
