# U-Pb dating on the Tera-Wasserburg diagram

## What it is for

The U-Pb spots of a diagenetic mineral (a calcite cement, a dolomite) measured on several samples are dated
together: RockFace Explorer plots them on the **Tera-Wasserburg diagram**, fits the York regression line, and gives
the age at its lower intercept with the concordia, with its uncertainty, the MSWD and the probability of fit. The age
is kept in the project with the phase it dates, and placed in the paragenetic evolution and in the stratigraphic
column.

## Before you start

* U-Pb spot analyses on the thin sections (page [Spot analyses: geochemistry, dating and fluid inclusions](spot_analyses.md)): kind *dating* (or system "U-Pb") with ²³⁸U/²⁰⁶Pb
  and ²⁰⁷Pb/²⁰⁶Pb, their uncertainties and the error correlation (rho).
* A query in Explorer that finds the samples to date together (for example one formation).

## Step by step

1. In RockFace Explorer, open the **U-Pb dating** tab.
2. **Descriptions with U-Pb spots (of the query)** lists the samples found that have U-Pb spots.
3. **Mineral dated**: the constituent (or group) whose spots are used, or **Every mineral**.
4. **Regression**:
   * **Free (York)** — the line through the points;
   * **Anchored to Stacey & Kramers (1975) common Pb** — the initial ²⁰⁷Pb/²⁰⁶Pb from the model at the age found;
   * **Anchored to a given initial ²⁰⁷Pb/²⁰⁶Pb** — type the **Initial ²⁰⁷Pb/²⁰⁶Pb** and the **Error of the anchor**.
5. The table lists every spot; untick **Spot (used)** to leave a spot out of the regression (it stays on the
   diagram, marked).
6. The diagram shows the points with their error ellipses, the concordia with its ages, the regression line and the
   result: "Age = … ± … Ma (2σ)", "± … Ma (95 % conf.)", the MSWD, n, and the initial ²⁰⁷Pb/²⁰⁶Pb.
7. **Export diagram…** saves it (PNG, SVG, PDF).
8. **Save age…**: give it a name; it is kept with the phase it dates (mineral and habit). **Ages of the project
   (double-click opens)** lists the saved ages; **Delete age**.

## Options

| Option | What it changes |
|---|---|
| Mineral dated | Which spots are used. |
| Regression | Free, anchored on Stacey & Kramers common lead, or anchored on a given value with its error. |
| Spot (used) | Leaves an outlier out of the fit. |

## How it works

* York regression with correlated errors in both coordinates (York et al. 2004); the age is the lower intercept of
  the line with the Tera-Wasserburg concordia (decay constants of Jaffey et al. 1971, ²³⁸U/²³⁵U of Hiess et al.
  2012). The anchored fit forces the
  line through the initial ²⁰⁷Pb/²⁰⁶Pb (Stacey & Kramers 1975, or the value given).
* The uncertainty is given as 2σ (analytical) and as the 95 % interval: t(n−2) × σ × √MSWD when MSWD > 1, else
  1.96σ (Ludwig 2003); decay-constant errors are not included. MSWD = χ²/(n − 2) (Wendt & Carl 1991), with the
  probability of fit.
* Checked against published values: Pearson's data with York's weights give the published slope, intercept and
  errors; on 800 synthetic data sets the 95 % interval holds the true age 97.2 % (free) and 97.5 % (anchored) of the
  time.

## From a script

```python
d = prj.date(formation="Example Formation", constituent="calcite_dia", anchor="stacey_kramers", figure="tw.pdf")
print(f"{d.age:.1f} ± {d.age_2s:.1f} Ma (2σ), MSWD {d.mswd:.2f}, n = {d.n}")
prj.save_age("Sandstone calcite", ("identification", "formation", "Example Formation"),
             constituent="calcite_dia", habit="poikilotopic", anchor="stacey_kramers")
print(prj.ages())
```

## Limits and common problems

* "No age: …" — too few spots, or "The line does not cut the concordia."
* "No age to save: date some spots first."
* Spots without rho are taken as uncorrelated (rho = 0).

## Coverage

L12 (dating U-Pb, Tera-Wasserburg; ages in the stratigraphy).
