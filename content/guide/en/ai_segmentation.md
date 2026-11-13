# RockFace AI: segmenting with models, training, fine-tuning and validating

## What it is for

A neural network trained on many examples segments a picture, a whole thin section, a micro-CT volume or an image
log in one click, and gives the area of every class with how confident it is. When a model does not fit your
material — another resin, another stain, another scanner — you **paint a few examples** and **fine-tune** it: the
new version learns your material, and its accuracy is measured on part of your annotation it never saw. This is the
annotation → training → validation → application → retraining cycle. The **unsupervised** segmentation splits a
picture into its textures with no annotation at all, and the **instance segmenter** of image logs finds the holes of
sidewall coring and the vugs as separate objects.

## Before you start

* RockFace AI installed (see [RockFace AI: installation, device and the model hub](ai_setup_hub.md)). Training also needs the extra
  `ai-train`.
* A thin section with a picture (Lab), or a grey volume or an image log (MC).

## Step by step

### Lab — a picture or a whole thin section

1. Open the section in **Lab**, open the picture and go to the **AI** tab.
2. **Apply**: select a model of the task *Segmentation 2D* (e.g. `rockface-thinsection-pores`) and click **Segment
   the picture (whole section, block by block)**. The picture is classified at full resolution, block by block, and
   kept as a segmentation map; the result shows the area of every class, the porosity and the mean confidence. A
   model of the task *Objects (instances) 2D* trained on pictures gives an object map instead, with one number per
   grain, measured in the **Measurements** tab.
3. **Train or fine-tune**:
   * **Annotation**: *Strokes of the Segmentation tab* (paint examples of each segment there, as for the random forest) or
     a segmentation map of the picture (made by any method, corrected by hand), or *Objects: …* — an object map of the
     picture (grains or pores split in the **Edit and objects** tab and corrected by hand) to train an **instance
     model** that separates touching grains (the textural instance model);
   * tick **Fine-tune the selected model** to start from the model selected in the table (the classes must match);
   * choose the **Network size** (small, standard, large), **Epochs**, **Steps per epoch**, the share **Held out for
     validation** and a **Model name**, and click **Train**. The result shows the accuracy, mean IoU and Dice of each
     class on the held-out part; the model is kept in the project.
4. **Validate**: choose a **Reference map** that was not used in training (of this or another picture) and click
   **Validate**: the metrics of the selected model against it. Classes are matched by name.
5. **Without annotation**: set **At most / At least segments**, **Iterations** and the **Working size**, and click
   **Segment without annotation**. The map's segments are named *Segment 1…k* by decreasing area; rename and merge
   them in the **Edit and objects** tab.

### MC — a volume or an image log

1. Open a grey volume and go to the **AI** tab.
2. **Apply**: select a model (e.g. `rockface-microct-pores`; a 2D model runs slice by slice) and click **Segment the
   volume**: a labels volume with the fractions, the porosity and the mean confidence.
3. **Train, fine-tune and validate**: choose the **Grey volume** and the **Annotation (labels volume)** — painted in
   the **Random forest** tab or a segmentation corrected by hand — the **Network** (2D slice by slice, or 3D), and
   click **Train**. In 2D, a share of the annotated slices is held out; in 3D, blocks of the volume. **Validate**
   measures the selected model against a segmented volume of the same grid.
4. **Image logs**: open an amplitude log; select a model of the task *Objects (instances) 2D* (e.g.
   `rockface-imagelog-instances`), choose the **Transit time** log of the same well when the model takes it, and
   click **Apply to the image log**: an object log with the table of the objects (sizes, depths, azimuths), editable
   with the log editor of 0.23. A *Segmentation 2D* model gives a labels log instead.

## Options

| Field | What it changes |
|---|---|
| Network size | small (8 filters in the first layer), standard (16), large (32): larger learns more, needs more memory and time |
| Epochs, Steps per epoch | How long the training lasts; the network with the best held-out accuracy is kept |
| Held out for validation | The share of the annotation kept out of training to measure the model (blocks of 64 px in 2D, slices or blocks of 32 voxels in MC) |
| Fine-tune the selected model | Start from that model (learning rate ×0.3); the new version has it as parent |
| At most / At least segments | The bounds of the unsupervised segmentation |
| Smallest object | Objects of the instance segmenter below this area are dropped |

## How it works

* **Network**: a U-Net (Ronneberger, Fischer & Brox 2015) of four levels with batch normalisation, in 2D or 3D;
  loss = class-weighted cross-entropy plus Dice on the annotated pixels only (Milletari, Navab & Ahmadi 2016);
  AdamW (Loshchilov & Hutter 2019) with a cosine schedule; random flips and rotations of 90°.
* **Metrics** (on held-out data): accuracy, intersection over union and Dice per class, the confusion matrix.
* **Large pictures and volumes**: tiles with a margin, reflected at the borders, classified in batches; the margin
  limits the seams between tiles.
* **Unsupervised**: a small network trained on the picture itself, its classes made constant on SLIC superpixels
  and spatially continuous (Kanezaki 2018; Kim, Kanezaki & Tanaka 2020; Achanta et al. 2012); the number of classes
  falls as the network merges them.
* **Instances**: the network classifies background, inside and edge of objects; the insides are the seeds of a
  watershed over the objects, across the 0°/360° seam of the log.

## From a script

```python
pic = prj.image("ILLUSTRATIVE mosaic PP")
seg, fr, por, conf = pic.ai_segment("rockface-thinsection-pores")          # whole section, block by block
model, met = pic.ai_train(map=seg, base="rockface-thinsection-pores", epochs=10)   # fine-tune, held-out metrics
print(pic.ai_validate(model, "reference map"))
seg2, fr2 = pic.ai_unsupervised(max_segments=8)
grains, n = pic.ai_objects(pic.ai_train_objects("grain objects")[0])          # the textural instance model
vol = prj.volume("plug scan")
labels, fr, por, conf = vol.ai_segment("rockface-microct-pores")
model, met = vol.ai_train("painted slices", base="rockface-microct-pores")
objects, table, n = prj.log("AMP").ai_instances("rockface-imagelog-instances", transit_time="TT")
```

## Limits and common problems

* "The annotation has k classes and the model m": fine-tuning keeps the model's classes; paint the same segments.
* "No class of the reference matches a class of the model by name": rename the segments of the reference map.
* A model applied to pictures of another magnification: the shipped thin-section model was trained at about the
  resolution of the GO-Forward images; fine-tune it on a few strokes of your pictures.
* Training on a processor takes minutes for a picture and can take hours for a 3D network; run long trainings on a
  graphics card or as a job (MC → Multiscale → Jobs: *AI: train a volume segmenter*).

## Coverage

GT18 (pretrained segmenters, thin section), GV19 (pretrained volume segmenters), GI11 (instance segmenter of image
logs), GT20 (unsupervised segmentation), L7 (whole-section quantification by ML), L11 (annotation → ML → validation →
extrapolation → retraining, for mineralogy and texture).
