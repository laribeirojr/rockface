# Segmenting by painted examples (random forest)

## What it is for

Some phases cannot be told apart by a colour or a grey value: a cement with the colour of the grains, vugs with the
mean grey of the matrix. You paint a few pixels (or voxels) of every segment, and the program learns from the image
**around** them — smoothness, texture, edges — and classifies the whole picture or volume. Each new stroke trains it
again and the preview changes at once, so you correct it where it is wrong.

It works in **RockFace Lab** on thin-section pictures and in **RockFace MC** on micro-CT volumes.

## Before you start

* Lab: a picture of a thin section (a crossed-polarized picture of the same section can be added as a second
  picture, if it is registered on the first or both have the section frame).
* MC: a grey volume. For a large volume, crop a representative part first (**Volume → Crop**) to paint and preview
  quickly; the model can then be applied to the whole volume.

## Step by step

### In Lab (pictures)

1. Open the picture and go to the **Segmentation** tab.
2. In **Method**, choose **Random forest (painted examples)**. Two segments are proposed (pore and solid): rename
   them, add more with **Add segment**.
3. Zoom on a representative part of the picture: the preview is computed on the part on screen.
4. Select a segment in the table, press **Paint examples of the selected segment** and paint a few strokes on it.
   Do the same for every segment. Paint the boundaries and the places that are easy to confuse.
5. With **Update the preview after every stroke** ticked, the preview follows each stroke. Look where it is wrong
   and paint there.
6. Press **Apply to the whole image** to classify the whole picture at the pixel size you trained on, block by
   block, or **Keep the segmentation as a map** to keep only the part computed.

### In MC (volumes)

1. Open the grey volume and go to the **Random forest** tab.
2. Type the segments in **Segments (separated by ;)** (for example `Vug; Matrix`) and press **New annotation on this
   volume**. The annotation is shown over the slices.
3. Choose the segment in **Paint with**, the **Brush radius**, and press **Paint on the slices**. Drag the mouse on
   any of the three slice views. **— eraser —** removes paint; **Undo** takes back the last stroke. Tick **Ball** to
   paint the neighbouring slices too.
4. Paint a few voxels of every segment, on several slices.
5. **Train and preview (current z slice)** shows the result on a window of the current slice; with **Train again and
   preview after every stroke**, it follows each stroke.
6. Press **Apply to the whole volume**. The result is a new segmented volume, with its porosity.

## Options

* **Features** — what the forest looks at, as in GeoSlicer's Interactive Segmenter:
  * *Sharp*: the value, Gaussian σ 1 and 2, local variance 5 × 5 — fine details;
  * *Balanced*: the value, Gaussian 1, 2, 4, variance 5 and 9 — a good start;
  * *Smooth* and *Extra smooth*: larger scales, smoother segments;
  * *Complete*: all of them, plus the gradient and the Laplacian.
* **Trees** — more trees, a steadier result (32 is enough most of the time).
* **Second picture / Second volume** — more channels on the same grid (the XP picture of a section).
* **Method** (MC) — *Random forest* or *Bayesian inference (Gaussian)* (each segment a normal distribution of the
  features).
* **Model** — *Train on the painted examples*, or a model kept in the project. Every model applied is kept in the
  project; **Export model…** writes it to a `.rfmodel` file, **Import model…** reads one (from a colleague, say).

## How it works

* For every pixel or voxel, the features of the chosen set are computed on each channel (L\*, a\*, b\* of a colour
  picture; the grey value of a volume). A random forest (Breiman 2001) of decision trees learns from the painted
  points which features tell the segments apart; every point gets the segment most trees vote for.
* A feature depends only on the points within a margin around it, so the image is classified block by block with
  that margin: the result is the same as the whole image at once, however large.
* A model is kept as plain numbers (the nodes of the trees), never as program code: a model received from someone
  else is safe to open.
* Source: L. Breiman (2001), *Random forests*, Machine Learning 45, 5–32; the presets follow the GeoSlicer manual.

## From a script

```python
import rockface.api as rf
prj = rf.open("project.rockface")
pp = prj.image("ILLUSTRATIVE mosaic PP")
seg, forest = pp.forest(strokes=[(1, [(120, 80), (140, 90)], 6), (2, [(600, 420)], 6)],
                        segments=["Pore", "Solid"], preset="balanced")
whole, fractions, porosity = pp.apply_forest(forest)
vol = prj.volume("Plug A")
ann = vol.new_annotation(["Vug", "Matrix"])
ann.paint("z", 40, [(30, 30), (36, 30)], 2.0, 1)
f3 = vol.train_forest(ann, name="Vugs")
seg3 = vol.apply_forest(f3)
```

## Limits and common problems

* **"Paint examples of at least two segments."** Every segment needs a few strokes.
* **The preview is good but the whole image is not.** The strokes came from one part only; paint other parts too.
* **"The model was trained on … channels"**: a model trained with a second picture needs one now.
* In Lab, the preview and the training use the strokes on screen; strokes outside the part on screen are kept for
  later.
* The pretrained networks of GeoSlicer (U-Net) come in stage 0.26.

## Coverage

GV6, GT7, GT8 (Interactive Segmenter, Segmenter — random forest and Bayesian methods).
