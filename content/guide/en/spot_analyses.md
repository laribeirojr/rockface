# Spot analyses: geochemistry, dating and fluid inclusions

## What it is for

A **spot analysis** is a measurement made at one point of the thin section: a laser-ablation or microprobe analysis,
a U-Pb date, a fluid-inclusion microthermometry. RockFace Atlas keeps each spot at its place in the section frame,
with its values and uncertainties, the mineral analysed and a photo of the area, so the spot is drawn at the same
place on every image of the section, can be found again under the instrument, and is reached from a query or a
figure.

## Before you start

* A saved description whose thin section is in Atlas, with a calibrated image.
* For laboratory tables: a CSV file with a spot name, x and y, and the value columns.

## Step by step

### Adding a spot by hand

1. In RockFace Atlas, choose the tool **Spot** and click where the analysis was made — or **New…** in the **Spots**
   tab.
2. In **Spot analysis**, give the **Kind** (geochemistry, dating, fluid inclusion, other), the **Spot** name
   (given in order — G01, D01, FI01… — when left empty), the **Position (x, y)**, the **Spot size**, **Method**,
   **Laboratory**, **Date** and **Analyst**.
3. The **Mineral** analysed and its **Location**, from the nomenclature.
4. **Values**: **Add value** for each — **Name**, **Value**, **±**, **Level** (1s, 2s), **Unit**, **< DL** (below the
   detection limit). **Usual fields of the kind** fills in the usual names (U-Pb ratios, Th and Tm ice…).
5. **Metadata** (**Add metadata**) for anything else; **Photo of the area** links a detail photo; **Notes**. **OK**.

### Importing a laboratory table

1. In the **Spots** tab, **Import table…**.
2. Choose the CSV and the **Coordinates in the table**: section frame (mm or µm), pixels of a calibrated image, or
   an instrument frame (below).
3. **Kind (when the table has none)**.
4. RockFace reads the rows ("N rows; M with errors will be left out") and shows each **Line** with its **Problems**.
   Value columns such as `Sr (ppm)` take their unit from the header; the uncertainty follows in a column `±`, `2s`,
   `err` or named `Sr 2s`; `<0.5` is below the detection limit; text columns become metadata.
5. **OK**.

### Instrument frames: finding a spot again

1. **Frames…** opens **Instrument frames of the section**. Give the **Instrument** name and **Its unit**.
2. Read the same marks — fiducials, scratches, grain corners — on the instrument (**Instrument x, y**, or **Read the
   stage**) and on the image of the section (**Section x, y (mm)**). **Add mark** for each; two marks are enough for
   a similarity, three for an affine transform, a fourth checks the others.
3. **Fit**: the RMS of the marks and the leave-one-out error.
4. Then **Stage to the spot** sends the stage to a selected spot, in the instrument's own coordinates. Calibrate
   again after the slide is put back in the holder.

### Looking at the spots

* The **Spots** tab lists them by kind (**Show**: **All kinds** or one), with their values. **Show** centres the
  viewer on a spot; **On the image** draws them; **Edit…**, **Delete**.
* **Photo of the area…** adds or opens the photo of the spot's area.
* **Export CSV…** — one row per spot, one column per value with its uncertainty.
* **Figure of the spots** — the section with the spots labelled, the **Counted points of:** a description, and
  **With the mineral map (when registered)**; **Save figure…**.

## Options

| Field | What it is |
|---|---|
| Level | The uncertainty's level: 1s or 2s. |
| < DL | Below the detection limit (the value is the limit). |
| Coordinates in the table | mm, µm, pixels of an image, or an instrument frame. |

## How it works

Spots are stored in millimetres of the section frame, never only in the instrument's coordinates: an instrument
frame is a transform (similarity or affine) fitted on marks, so the same spot is found on any instrument that has
its frame. Some values are derived and shown (never stored), each with its source: the salinity of a fluid
inclusion from Tm ice (Bodnar 1993) and the ²⁰⁶Pb/²³⁸U age from ²³⁸U/²⁰⁶Pb (Jaffey et al. 1971 decay constant, no
common-Pb correction). U-Pb spots are dated together in RockFace Explorer (page [U-Pb dating on the Tera-Wasserburg diagram](dating.md)).

## From a script

```python
d = prj["TS-9"]
d.calibrate_frame("LA-ICP-MS stage", [((41250, 18630), (1.0, 1.0)), ((57240, 18965), (17.0, 1.0)),
                                      ((41020, 29380), (1.0, 11.75))], unit="um")
d.import_spots("TS-9_U-Pb.csv", coords="frame", frame="LA-ICP-MS stage", kind="dating")
fi = d.add_spot("fluid_inclusion", 4.184, 3.488, values=[rf.Value("Th", 118.5, 1.0, "°C", "1s"),
                                                         rf.Value("Tm ice", -12.3, 0.2, "°C", "1s")],
                method="microthermometry", constituent="quartz_dia")
print(rf.spots.derived(fi))                              # salinity 16.24 wt% NaCl eq. (Bodnar 1993)
print(d.to_frame("LA-ICP-MS stage", fi.x_mm, fi.y_mm))   # where it is on the instrument
d.spot_figure("TS-9_spots.png")
```

## Limits and common problems

* "No instrument frame for this section: add one with Frames… (fiducial marks)."
* A name already used in the section is refused; implausible values (a negative ppm, rho outside −1…1) only warn.
* The derived U-Pb age has no common-lead correction: use the dating of Explorer for ages.

## Coverage

L3 (links to spot analyses with photos of the analysed areas), L12 in part (spot analyses with detail images and
dating).
