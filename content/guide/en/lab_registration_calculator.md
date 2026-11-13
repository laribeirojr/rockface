# RockFace Lab: registration and the image calculator

## What it is for

**Registration** aligns one image of a section on another — the crossed-polars image on the plane-polarized one, a
cathodoluminescence image, a second scan — by landmark pairs and/or automatically, and writes it on the pixel grid
of the fixed image, so the two can be used together pixel by pixel. The **Calculator** combines the images of a
section with a formula, pixel by pixel: a mask of the dark pixels of XP, the difference of two lights, a threshold
of the hue.

## Before you start

Two images of the same thin section in RockFace Lab (page [RockFace Lab: crop, filters and the sample mask](lab_preparation.md)).

## Step by step

### Registration

1. Open the **Registration** tab.
2. **Fixed image** (usually PP) and **Moving image** (XP, CL…).
3. **Transform**: **translation**, **similarity (turn, scale, shift)**, **affine** or **thin-plate spline**.
4. Either:
   * **Landmark pairs…** — click a point on the fixed image (left), then the same point on the moving image
     (right); the fit is made after every pair, with the **Residual** of each and "RMS … px, leave-one-out … px";
     **Remove pair**, **Remove all**; or
   * **Automatic** — the correlation of the grain outlines (ECC), started from the section frames or from the pairs.
     **Search (automatic)**: from the section frames, **shift**, **any rotation**, or **rotation and scale**.
5. The result: "…: rotation …°, scale …, shift … px", the correlation of the outlines, the landmark errors.
6. Check it: **Moving over fixed** blends the two; **Flicker** alternates them.
7. **Save the registration** keeps it on the moving image; **Write on the grid of the fixed image** writes the
   moving image resampled pixel for pixel on the fixed one ("Image added on the fixed grid: …").

### Calculator

1. Open the **Calculator** tab. The images of the section are listed; double-click a name to insert it.
2. Write the **Formula**, with `{image name}` and a channel: `.r .g .b`, `.l` (luminance), `.h .s .v`. Examples:
   * `{XP}.l < 40` — the dark pixels of XP (a mask);
   * `({PP}.v − {XP}.v)/2 + 128` — a grey image;
   * `where({PP}.h > 190, 255, 0)`.
   Numbers, `+ − * / **`, comparisons, `& | ~`, and `abs sqrt log log10 exp min max where clip round`.
3. **Reference image** — the grid of the result (the other images are taken on it through their registrations).
4. **Result**: **by the formula** (a comparison gives a mask, a number a grey image), **mask** or **grey image**.
   **Stretch the values** with the **Value shown black** and **Value shown white**.
5. **Name of the result**, then **Calculate**. "Uses: …" lists the images used. "Result added: …".

## Options

| Option | What it changes |
|---|---|
| Transform | Translation, similarity, affine (≥ 3 pairs) or thin-plate spline (non-linear, many pairs). |
| Search (automatic) | How far the automatic search looks: none, shift, any rotation, rotation and scale. |
| Result | Mask (a map of 0/1) or grey image. |

## How it works

* Landmark fits are least squares; the leave-one-out error predicts each pair from the others. The automatic
  registration maximizes the enhanced correlation coefficient (ECC) of the grain outlines, after a search of shift,
  rotation and scale.
* Checks: XP on PP recovered within 0.017 px for any rotation and ±8 % scale; a scan placed 6 px off corrected to
  0.15 px; a thin-plate spline 0.06 px on a non-linear warp; on real thin-section pairs the common offset was found
  in 52 and 59 of 60 patches.
* The calculator works block by block on the grid of the reference image.

## From a script

```python
pp_c, xp_c = prj.image("ILLUSTRATIVE mosaic PP (crop)"), prj.image("ILLUSTRATIVE mosaic XP (crop)")
t = xp_c.register_on(pp_c, search="rotation")            # automatic, from the section frames
print(t.rotation_deg, t.scale, t.ecc)
xp_on_pp = xp_c.resample_on(pp_c)                        # on the grid of the PP image
dark = prj.calculate("{%s}.l < 60" % xp_on_pp.name, pp_c, name="dark in XP")
print(dark.areas_mm2())
```

## Limits and common problems

* "Choose two different images of the section."
* "N pairs: at least … are needed." — 1 for a translation, 2 for a similarity, 3 for an affine transform, 4 for a
  thin-plate spline.
* The automatic registration needs images with grains in common; on very different lights (CL on PP), give a few
  landmark pairs first.

## Coverage

GT5 (registration PP ↔ XP with landmark pairs, automatic registration), GT19 (Volume Calculator of the "More tools").
