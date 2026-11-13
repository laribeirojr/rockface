# RockFace AI: generative model of a volume (SinGAN) and the spot cycle

## What it is for

**Generating rock images.** From one training volume — a segmented micro-CT volume or a grey one — a generative
network learns its texture and makes as many new volumes as you want, of the same size or larger, with the same
porosity and pore sizes, for simulations that need several realizations or a volume larger than the scan. It sits
beside the MPS generation of 0.25 (Multiscale tab).

**The spot cycle.** When some spot analyses of a project (microprobe, LA-ICP-MS, EDS…) have their constituent named
by the petrographer, a classifier learns the constituent from the measured values, tells how often it is right on
thin sections it did not see, and proposes a constituent with its probability for the spots not yet named. You
accept, correct or reject each proposal; the next training uses them.

## Before you start

* SinGAN: RockFace AI with training (extra `ai-train`); a graphics card for 3D training of useful size.
* Spot cycle: spot analyses with values (Atlas → Spots, or imported from CSV), at least 6 named spots of at least 2
  constituents; the constituents are nomenclature terms.

## Step by step

### Generative model (MC → AI)

1. Open the training volume (segmented or grey).
2. In **Generative model (SinGAN)**, set the **Iterations** per scale and the **Training volume up to** size (the
   volume is read at the level that fits it), and click **Train on the volume**. The result compares 4 volumes
   generated from new noise with the training volume: porosity, two-point probability (S2) and correlation length.
   The model is kept in the project with its card.
3. Select the model in the table (task *Generation 3D*), set **Volumes**, **Size × training** (1.5 makes each side
   1.5 times longer) and **Seed**, and click **Generate volumes**: they are added to the sample, as labels volumes
   with the legend of the training volume when it was segmented.
4. For large volumes run the training as a job: **Multiscale → Jobs**, calculation *AI: train a generative model
   (SinGAN)*, here or on a remote computer with a graphics card; **Bring the results back** adds the model.

### Spot cycle (Lab → AI)

1. Choose the **Spots** kind and **From** *this thin section* or *the whole project*, and click **Learn**. The result
   shows the accuracy and the per-class scores by cross-validation in folds by thin section (a section is never both
   in training and in validation).
2. Choose the **Classifier** and **Propose from probability** (e.g. 0.6), and click **Propose**: the table lists the
   unnamed spots with the proposed constituent and its probability.
3. Untick what you reject, type over a constituent to correct it, and click **Accept checked**: the constituents are
   written into the spots, each with the model and the probability in its record (so you can always tell a name
   given by hand from an accepted proposal).
4. Learn again: the new classifier uses the accepted spots too.

## Options

| Field | What it changes |
|---|---|
| Iterations | Training steps per scale of the pyramid |
| Training volume up to | The largest training volume (voxels per side); the level of the volume that fits is used |
| Volumes, Size × training, Seed | How many volumes, how large, and which noise |
| Propose from probability | Proposals below it are not listed |

## How it works

* **SinGAN** (Shaham, Dekel & Michaeli 2019), in 3D as in GeoSlicer's RockSinGAN module: a pyramid of small
  convolutional generators and patch discriminators trained coarse to fine on the one training volume; each scale is
  trained with the Wasserstein loss and gradient penalty (Gulrajani et al. 2017) plus the reconstruction of the
  training volume from a fixed noise; the noise of each finer scale is scaled by the reconstruction error of the
  scale below. The whole pyramid is one ONNX graph, so generation runs on any device.
* **Comparison**: porosity, the two-point probability S2(h) along x and the length where S2 has fallen 1/e of the way
  to φ² (Torquato 2002).
* **Spot classifier**: the random forest of 0.23 on the values (below the detection limit = 0; missing = median of
  the training spots), cross-validated in folds grouped by thin section.

## From a script

```python
vol = prj.volume("plug segmentation")
model, comparison = vol.ai_generator(iterations=300, max_voxels=32 ** 3)
new = vol.ai_generate(model, n=4, scale=1.5)
rid, metrics = prj.ai_spots_train(kind="geochemistry")
props = prj.ai_spots_propose(rid, kind="geochemistry", min_probability=0.6)
prj.ai_spots_accept(props, rid)
```

## Limits and common problems

* A 3D generator trains in minutes on a graphics card and in hours on a processor; start with a small training size
  and few iterations to check the result, then run the full training as a job.
* A generator learns one texture: a training volume with a trend (a layer, a fracture) is reproduced as texture, not
  as a trend; use MPS with hard data when the layout matters.
* Spot proposals are only as good as the named spots: name examples of every constituent you expect, from more than
  one thin section.

## Coverage

GM5 (image generation: the generative network RockSinGAN), L11 (annotation → ML → validation → extrapolation →
retraining, for spot geochemistry).
