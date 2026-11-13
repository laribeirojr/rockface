# RockFace Explorer: the dashboard of a collection

## What it is for

The **Dashboard** tab shows a collection at a glance: the samples by facies, porosity against permeability, the
grain density, the depths sampled in each well, the sample types, and galleries of the images (PP and XP mosaics,
scanner slides, detail photos, mineral maps). Filters by field, formation, zone, well, facies and image category
narrow every chart at once.

## Before you start

A project with descriptions, ideally with petrophysics (Analyses tab, page [Analyses and analysis requests](analyses_requests.md)) and
images (RockFace Atlas).

## Step by step

1. In RockFace Explorer, open the **Dashboard** tab.
2. The charts:
   * **Samples by facies (click to filter)** — a treemap; click a facies to keep only it;
   * **Porosity × permeability (mD)** — one point per sample, coloured by facies, permeability on a log axis;
   * **Grain density** — a histogram;
   * **Depths by well** — the **Measured (top)**, **Corrected** and **Adjusted** depths of the samples of each
     well;
   * **Sample types** — plugs, whole cores, sidewall cores, cuttings, outcrop samples.
3. **Filters**: tick values of **Field**, **Formation**, **Zone**, **Well**, **Facies** and **Image category**; every
   chart and gallery follows. "N of M samples". **Clear filters** removes them.
4. **Only the descriptions of the query** limits the dashboard to the descriptions found in the Query tab.
5. **Galleries**: **Mosaic PP**, **Mosaic XP**, **Scanner**, **Detail photos**, **Mineralogy (maps)**. Double-click
   an image to open it in RockFace Atlas.

## Options

| Option | What it changes |
|---|---|
| Filters | Every chart and gallery shows only the samples that match. |
| Only the descriptions of the query | The dashboard of the query's result. |

## How it works

The dashboard reads the same facts as the queries: petrophysics comes from the conventional-petrophysics analyses
of each sample, the facies, field, formation, zone and well from the identification, the galleries from the Atlas
images of each thin section (by category and light). The treemap is squarified (each rectangle's area is the number
of samples).

## From a script

```python
board = prj.dashboard(field="Example Field A")
print(board.facies())                    # samples by facies
for phi, k, facies, did in board.phi_k():
    print(phi, k, facies)
print(board.grain_density(10), board.depths(), board.sample_types())
print(board.gallery("mosaic_pp"))        # image ids
```

## Limits and common problems

* "No data for the descriptions shown." — no petrophysics or no images among the samples filtered.
* A sample without facies is shown under "—".

## Coverage

L1 (dashboards), Q2 (concepts of petrophysics in the collection).
