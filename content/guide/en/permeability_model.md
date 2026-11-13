# Permeability model of image logs

## What it is for

A continuous permeability curve along the well from a **segmented image log** (e.g. vugs, microporous matrix and
tight matrix on an acoustic amplitude log), a **porosity curve** and the **plug permeabilities** measured in the
laboratory. It is meant for dual-porosity carbonates, where the vugs seen on the image carry much of the flow.

## Before you start

* A segmented image log (Well logs tab → Segmentation), with a segment for the macropores (vugs).
* A porosity curve of the same well (imported from LAS, CSV…; in fraction or in %).
* The plug permeabilities: depth (m) and K (mD), at least two inside the image.

## Step by step

1. Open the segmented image log and go to the **Well logs** tab, group **Permeability model (image log)**.
2. Choose the **Segmented image log** and the **Porosity curve**.
3. Choose the **Macropore segment** (its porosity exponent is fixed at 1) and, if needed, an **Ignored segment** (an
   uncertainty class, or a bad-image class).
4. Set the **Depth window** over which the fractions of the segments are counted (0: every row of the image).
5. Paste the **Plugs**, one per line: depth and K (spaces, tabs or semicolons).
6. Optionally type **Forced points (Kds)** the same way: depths and K the curve must pass near, to correct a zone of
   interest.
7. Click **Fit and write the permeability curve**. The curve (unit mD) is added to the well, and the fit is shown:
   number of plugs, misfit of log10 K, R², and A and B of each segment.

## Options

| Field | What it changes |
|---|---|
| Macropore segment | The segment whose term is A·F·Φ (exponent 1) |
| Ignored segment | Pixels left out of the fractions |
| Depth window | Rows gathered into one depth of the curve |
| Forced points (Kds) | Extra points of the fit with ten times the weight of a plug |

## How it works

At every depth (Menezes de Jesus, Compan & Surmas 2016):

K = A1·F1·Φ^B1 + A2·F2·Φ^B2 + … + An·Fn·Φ^Bn + Am·Fm·Φ

where Fn is the fraction of segment n in the rows at that depth, Φ the porosity curve interpolated to the image
depths, Fm the fraction of the macropore segment. A ≥ 0 and 0 ≤ B ≤ 8 are fitted to the plugs by least squares on
log10 K (permeability spans decades), from several starting exponents (trust-region reflective). Synthetic plugs
made with known A and B are recovered exactly.

## From a script

```python
seg = prj.log("AMP (segmentation)")
k, fit = seg.permeability_model("PHIT", [(2510.35, 120.0), (2512.10, 8.5), (2515.80, 300.0)], macro="Pore",
                                window_m=0.1)
print(fit["A"], fit["B"], fit["rms_log10"])
```

## Limits and common problems

* With few plugs, the terms of the classes with little influence can come out as 0; check the A and B shown and
  their misfit.
* The model uses only the image and the porosity; the plugs must sample the classes of the image for the fit to
  hold elsewhere.

## Coverage

GI10 (permeability modelling).
