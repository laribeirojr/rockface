# Consistency between scales

## What it is for

The same sample is measured at several scales: the thin section under the microscope, the plug in the laboratory,
the micro-CT volume, the well log at its depth. Each sees the rock differently, and they should tell a coherent
story — together with the paragenetic sequence the petrographer wrote. The **Consistency** tab compares them and
says, for each check, whether the numbers agree, differ in the way the description explains, or contradict each
other — and what to look at.

## Before you start

The checks use what the project already has; each one runs only with its data:

* the **composition** (porosity, IGV, cements, clays) — Petro → Composition;
* the **plug's porosity and permeability** — Petro → Analyses, *Conventional petrophysics*;
* a **segmented micro-CT volume** of the sample with its porosity, or a microporosity map — RockFace MC;
* a **porosity curve** (PHIT, PHIE, NPHI, DPHI…) of the sample's well covering its depth — RockFace MC → logs;
* the **grain size and sorting** — Petro → Microscopic (or Macroscopic);
* the **paragenetic sequence** with its regimes — Petro → Diagenesis.

## Step by step

1. Open a description and the **Consistency** tab (the last one).
2. Read the table: each check, its result and the explanation. Hover over an explanation to see its references.
   * **Consistent** — the numbers agree;
   * **Explained** — they differ the way the description says they should (the plug sees the microporosity of the
     clays described, for example);
   * **To check** — a difference nothing in the description explains;
   * **Inconsistent** — the data contradict each other;
   * **No data** — what is missing to run the check.
3. **Check again** after editing the description (the tab follows the composition and the microscopic description
   on screen).
4. **Ask Mio** sends *"Is the sample … consistent?"* to Mio; she also answers *"which samples are inconsistent?"* for
   the whole project.
5. **Reports** have a *Consistency* section with the checks that have data and their references.

## The checks

| Check | Compared | Result |
|---|---|---|
| Porosity: thin section × plug | Point-count porosity (with its counting uncertainty) and the plug's | Thin section above the plug beyond the uncertainty: *inconsistent* (pores made in preparation, another lamina, plug and thin section from different places). Plug more than 5 points above: *explained* when clays, matrix, micrite or microporosity are described, *to check* otherwise (Halley 1978) |
| Porosity: micro-CT | Resolved porosity of a segmented volume (or the total of a microporosity map) and the plug — the thin section when there is no plug | More than 3 points above: *inconsistent* (segmentation threshold); more than 5 below: *explained* (pores below the voxel size; Andrä et al. 2013) |
| Porosity: well log | The porosity curve at the sample's depth and the plug (or the thin section) | More than 5 points apart: *to check* (depth shift, thin beds, log corrections) |
| Intergranular volume (IGV) | IGV of a sandstone | Above 45 %: *inconsistent* — more than freshly deposited sand (Beard & Weyl 1973; Lundegard 1992). Below 26 %: *explained* by 10 % or more ductile grains or by concavo-convex or sutured contacts, *to check* otherwise (Paxton et al. 2002; Pittman & Larese 1991) |
| Early cement × compaction | Eodiagenetic cement and IGV | 10 % or more early cement with IGV below 28 %: *inconsistent*; IGV 35 % or more with neither early cement nor matrix: *to check* |
| Paragenetic sequence | Relations and regimes of the phases | Contradicting relations, or a later regime before an earlier one: *inconsistent* |
| Permeability × texture | The plug's permeability and Berg's (1970) estimate from the porosity, the median grain size and the sorting | Within a factor of 10: *consistent*; 10 times lower: *explained* by clays, cements or microporosity, *to check* otherwise; 10 times higher: *explained* by fractures, *to check* otherwise |

## How it works

* The thin-section porosity carries the counting uncertainty of the points counted (see *How sure the point count
  is*): a difference inside it is never called inconsistent.
* Berg's (1970) estimate: k (mD) = 1000 × 5.1×10⁻⁶ φ^5.1 d² e^(−1.385 p), with φ in %, d the median grain size in
  mm and p = P90 − P10 = 2.563 σ (Folk & Ward sorting, φ units). When the sorting is not described a moderately
  sorted sand (σ = 0.85) is assumed and said so.
* A rock is treated as a carbonate when its carbonate grains and lime mud outweigh the extrabasinal grains: the IGV
  checks are then not applied.
* The log value is the curve's sample nearest to the corrected depth (or the top depth); a curve in v/v is read in %.

## From a script

```python
rep = prj["ILL-TS-001"].consistency()
rep["status"]                                   # "ok", "explained", "check", "inconsistent" or "no_data"
[(c["code"], c["status"]) for c in rep["checks"]]
for r in prj.consistency():                     # every description, the ones to look at first
    print(r["name"], r["status"])
rf.berg_permeability(19.4, 0.18, 0.42)          # 138 mD
```

## Limits and common problems

* The thresholds are rules of thumb from the literature, not laws: a *to check* is a question to the petrographer,
  not an error.
* Berg's equation was derived for clean sands of 30 to 40 % porosity; for cemented sandstones read it as an order
  of magnitude — hence the factor of 10.
* The whole-rock XRD is not compared with the point count (weight and volume percentages, and the fine phases the
  microscope cannot resolve, differ too much for a simple rule).
* The IGV limits are for rigid-grain sandstones; very coarse, very poorly sorted or matrix-rich rocks start from a
  lower depositional porosity.

## Coverage

O8 (the owner's request of 2026-11-17: the innovations, the second one).

References: Halley (1978), https://doi.org/10.1306/212F7504-2B24-11D7-8648000102C1865D; Andrä et al. (2013),
https://doi.org/10.1016/j.cageo.2012.09.005; Beard & Weyl (1973); Lundegard (1992),
https://doi.org/10.1306/D42678D4-2B26-11D7-8648000102C1865D; Paxton et al. (2002); Pittman & Larese (1991),
https://doi.org/10.1306/0C9B292F-1710-11D7-8645000102C1865D; Berg (1970); Nelson (1994).
