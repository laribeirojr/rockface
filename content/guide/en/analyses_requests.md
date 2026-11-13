# Analyses and analysis requests

## What it is for

The **Analyses** tab keeps the laboratory results of the sample — petrophysics, XRD, SEM, isotopes, chemistry,
biostratigraphy — with their pictures. The **Requests** tab asks the laboratory for new analyses and follows them
until they are done. Both belong to the **sample**: every description of the sample's thin sections shows them.

## Before you start

A **saved** description: analyses and requests belong to its sample ("Save the description first: analyses and
requests belong to its sample.").

## Step by step

### Adding an analysis

1. Open the **Analyses** tab. Its heading names the sample.
2. **Add analysis…**
3. Choose the **Analysis**: conventional petrophysics, special petrophysics, XRD (whole rock or clay fraction), SEM
   (secondary or backscattered electrons), stable isotopes (C, O), strontium isotopes, chemistry or
   biostratigraphy.
4. Fill in the **Laboratory**, the **Date (yyyy-mm-dd)** and the results. The fields follow the kind:
   * conventional petrophysics — **Porosity** (%), **Permeability** (mD), **Grain density** (g/cm³);
   * stable isotopes — **δ13C** and **δ18O** (‰ VPDB); strontium — **87Sr/86Sr**;
   * XRD — a table of **Mineral** and **%** (**Add row**, **Remove row**);
   * chemistry — a table of **Element or compound**, **Value** and **Unit**;
   * special petrophysics — the **Method**; biostratigraphy — **Biozone**, **Age** and **Fossils**;
   * **Notes** for anything else.
5. Under **Pictures and files**, **Add picture…** (SEM images, diffractograms, chromatograms); **Export…** saves one
   back to a file.
6. **OK**. The list shows the kind, laboratory, date, a summary of the results and the number of pictures. **Edit…**
   and **Delete** act on the selected analysis.

### Requesting an analysis

1. Open the **Requests** tab, then **New request…**
2. Choose the **Analysis**. The **Tip** says what a good objective states for that kind.
3. Write the **Objective** (required): what question the analysis should answer.
4. **Status**: Requested, In progress, Done or Cancelled. Change it as the work goes on.
5. **Notes** and pictures (for example a photo of the area to sample), then **OK**.

The list shows the kind, objective, status, when it was requested and by whom.

## Options

| Field | Rule |
|---|---|
| Date | yyyy-mm-dd, yyyy-mm or yyyy. |
| Porosity, permeability, grain density | 0–100 %, 0–100 000 mD, 1.5–5.0 g/cm³. |
| δ13C, δ18O | −50 to 50 ‰ VPDB; 87Sr/86Sr 0.69–0.80. |
| XRD rows | Each mineral named; the percentages should total 100 (saved anyway, with a warning). |

## How it works

Analyses and requests are stored with the sample, so a plug's porosity is entered once and shown in every
description of that plug. They go into the reports, the exchange files, the queries of Explorer (petrophysics,
isotopes, XRD) and its dashboard (porosity × permeability, grain density). Pictures are kept inside the project.
Routine core analyses of a laboratory report in PDF can be read into the samples of a well by depth (Home →
**Import lab report (PDF)…**, page [Files of the reference programs](file_formats.md)).

## From a script

```python
d = prj["TS-9"]
d.add_analysis("conventional_petrophysics", laboratory="ILLUSTRATIVE lab", date="2026-03-02",
               values={"porosity": 18.2, "permeability": 245.0, "grain_density": 2.65})
d.add_analysis("xrd_whole_rock", rows=[{"mineral": "Quartz", "percent": 71}, {"mineral": "Calcite", "percent": 29}],
               pictures=["xrd.png"])
d.add_request("stable_isotopes", "δ13C and δ18O of the calcite cement, to date its water source")
for a in d.analyses():
    print(a["kind"], a["values"], a["rows"])
print([r["status"] for r in d.requests()])
```

## Limits and common problems

* "Choose the kind of analysis." / "State the objective of the request."
* "… must be between … and …": a value outside the plausible range of its kind.
* "The analysis has no results yet." — a warning: the analysis is saved empty.
* Pictures larger than the project's limit for attachments are refused.

## Coverage

P15 (additional analyses), P16 (analysis requests with pictures).
