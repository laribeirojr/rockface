# Identification of a sample

## What it is for

The **Identification** tab says what the description is about: its name and uses, the well or outcrop, the sample
and its depths, the thin section, the petrographer, and the important observations. Every query, report, figure and
LAS file reads these fields.

## Before you start

A description open or just created (page [Projects and descriptions](projects_descriptions.md)).

## Step by step

1. Open the **Identification** tab (the first one).
2. **Description**
   * **Description name** — required and unique in the project. After the first save it is locked (use **Save
     as…** for another name).
   * **Selected use of the description** — up to three uses (reservoir characterization, reservoir quality,
     diagenesis, provenance, depositional environment, petrophysical calibration, geochemistry and dating,
     teaching, other), without repeats.
3. **Well or outcrop**
   * **Name** — type a new one or choose one already in the project; choosing an existing well fills in its basin,
     field, country, state and position.
   * **Kind** (well or outcrop), **Basin**, **Field**, **Country**, **State / province**, **Latitude (°)**,
     **Longitude (°)**.
4. **Sample**
   * **Sample type** (core plug, whole core, sidewall core, cuttings, outcrop sample, other), **Stratigraphic
     unit**, **Zone**.
   * **Top depth (m)** and **Base depth (m)**; **Corrected depth (m)** (core-to-log correction) and **Adjusted
     depth (m)** (the final depth used in models).
   * **Core no.**, **Box no.**, **Plug no.**, **Thin-section no.** and **Facies** (the team's code or name).
5. **Petrographer** — **Name** and **Institution**. **First edition** and **Last edition** are filled in by RockFace.
6. **Important observations** — a free summary of what matters most in the sample.
7. **Save** (Ctrl+S).

## Options

| Field | Rule |
|---|---|
| Description name | Required; unique; locked after the first save. |
| Selected use | At most three, no repeats. |
| Depths | 0 to 9999.99 m; the base cannot be shallower than the top. |
| Latitude, longitude | −90° to 90°; −180° to 180°. |
| Facies | Free text: the code or name the team uses (Explorer's dashboard groups by it). |

## How it works

Wells, samples and thin sections are shared records: two descriptions of the same thin section show the same
well, depths and numbers, and changing them in one changes them for both. The values stored are language-neutral
codes (for example the sample type), so the project reads the same in English, Spanish and Portuguese. The well's
directional survey, when there is one, gives the true vertical depth and the position of each sample (page [Well trajectory](well_trajectory.md)).

## From a script

```python
with rf.open("study.rockface") as prj:
    d = prj["TS-9"]
    print(d.identification.well_name, d.identification.top_depth)
    d.update(base_depth=2501.6, facies="F3", uses=["reservoir", "diagenesis"])   # checked as in the form, then saved
```

`d.update()` raises `rf.ScriptError` with the messages when a value breaks a rule, and nothing is written.

## Limits and common problems

* "The description name is required." / "… already exists in this project."
* "Top depth (m) must be between 0 and 9999.99 m."
* "The base depth (… m) is shallower than the top depth (… m)."
* "At most three uses can be selected." / "A use of the description is selected twice."
* Warnings (not errors): "No well or outcrop given.", "The thin section has no number." The description is saved,
  but queries by well or by thin section will not find it.

## Coverage

P4 (identification fields), P5 (selected uses), P7 (important observations), P8 (position and depths).
