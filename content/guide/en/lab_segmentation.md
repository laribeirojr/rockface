# RockFace Lab: segmentation and porosity

## What it is for

**Segmentation** sorts the pixels of a thin-section image into segments — pore, grains, cement, matrix… — and keeps
the result as a **map** over the image. Its pore segment gives the **porosity**. RockFace Lab offers the classical
methods: the blue resin, thresholds of a channel (also multi-level Otsu), a colour range, a Bayesian classifier
learnt from samples drawn on the image, k-means (also on superpixels), seeds grown by watershed, and a random forest
trained on painted examples.

## Before you start

An image of the section in RockFace Lab, ideally cropped and filtered (page [RockFace Lab: crop, filters and the sample mask](lab_preparation.md)). A sample mask limits the segmentation to the rock.

## Step by step

1. Open the **Segmentation** tab and select a picture (not a map).
2. **Method**:
   * **Blue resin (pore / solid)** — the blue epoxy is pore. In CIELAB the resin is found by its blue (b*), the cut
     chosen automatically (Otsu) or typed, with **Chroma at least**; or by the **CIELAB hue angle**. The resin can
     be split by its lightness: **no: all resin is pore**, **open pore = bright resin (Otsu)**, or **open pore = L*
     at least…** — the dark, resin-tinted part is then microporosity.
   * **Thresholds of a channel** — choose the **Channel** (luminance, red, green, blue, HSV hue, saturation, value,
     CIELAB L*, a*, b*, chroma, hue angle) and the cuts; empty: automatic (multi-level Otsu).
   * **Colour range (HSV)** — the ranges of hue, saturation and value of a segment.
   * **Bayesian classifier (samples)** — **Draw a sample of the selected segment** for every segment (at least 8
     pixels each); the classifier learns their colours.
   * **K-means (unsupervised)** — the number of **Clusters**, on pixels or on **Superpixels**.
   * **Grow from seeds (watershed)** — **Paint seeds of the selected segment** with the **Brush radius**.
   * **Random forest (painted examples)** — page [Segmenting by painted examples (random forest)](random_forest.md).
3. **Segments**: **Add segment**, **Remove segment**; each with its name, colour and **Role** (pore, solid,
   unclassified).
4. Region: the whole image, or a sample mask.
5. **Segment**. The preview shows the map over the image and "Share of the counted area" of each segment, the
   **Porosity (pore / pore + solid)** and the thresholds used.
6. Clean the map: **Islands smaller than** (pixels given to their surroundings) and **Smoothing (majority)**.
7. **Name of the map**, then **Keep the segmentation as a map**. "Segmentation kept: … (porosity … %)."

The map can be corrected by hand and split into objects (page [RockFace Lab: editing maps and objects](lab_editing_objects.md)), then
measured (page [RockFace Lab: measurements and size distributions](lab_measurements.md)).

## Options

| Option | What it changes |
|---|---|
| Blue resin — the split by L* | All resin is pore, or only the bright resin (open pore); the dark resin is microporosity. |
| Channel, cuts | Which channel is cut, and where (empty: Otsu). |
| Superpixels (k-means) | Cluster SLIC superpixels instead of pixels: smoother segments. |
| Role | Pore and solid make the porosity; unclassified is left out of it. |

## How it works

* Colours are converted to CIELAB (within 0.0049 of scikit-image on 100 000 colours) and to HSV; 12 channels are
  offered.
* On three ILLUSTRATIVE sections of exact truth (22.3–25.6 % porosity), the blue resin, Otsu of b* and the Bayesian
  classifier were exact on clean images and within 0.5 points (IoU ≥ 0.95) when blurred, noisy and with thinner
  resin together.
* On the 20 carbonate sections of GO-Forward D2.1 (CC BY 4.0), whose published values are the open porosity of a
  SLIC + k-means segmentation, the hue-angle resin with the L* split follows them with a correlation of 0.97; counting
  all the resin gives the total optical porosity.
* The map is a tiled image like the others, in the frame of the section, so it is laid over every image of the
  section in Atlas and Lab.

## From a script

```python
pp = prj.image("ILLUSTRATIVE mosaic PP")
seg = pp.segment("resin", post=[("islands", {"min_px": 20})])
print(f"porosity {seg.porosity():.2f} %")
km = pp.segment("kmeans", k=4, superpixels=5000, save=False)          # a look, nothing written
otsu = pp.segment("thresholds", channel="b", classes=3, name="Otsu of b*")
```

## Limits and common problems

* "Choose a picture of the section (not a map) to segment."
* "Draw a sample (of at least 8 pixels) for every segment." / "Paint seeds of at least one segment."
* The preview is computed at a reduced level on large images ("Computed at level …"); the map kept is at full
  resolution.
* Sections without blue resin: use thresholds, a colour range, the classifier or the random forest.

## Coverage

GT7 (manual and threshold segmentation), GT8 (pore / non-pore by Bayesian inference), L7 in part (quantification of
the whole section, classical).
