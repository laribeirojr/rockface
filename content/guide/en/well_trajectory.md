# Well trajectory

## What it is for

A deviated well puts a sample at a measured depth (MD) that is not its true vertical depth (TVD), nor straight
under the well head. **Well trajectory** reads the directional survey of the well and gives every sample its TVD,
its depth below sea level, its offsets north and east and its latitude and longitude.

## Before you start

* The well in the project (Identification), with its head latitude and longitude for the geographic position.
* A survey file: measured depth, inclination and azimuth (CSV, text or LAS).

## Step by step

1. **Petro → Home → Well trajectory…**
2. Choose the well; type the elevation of the depth datum above sea level and the north reference.
3. **Read a survey…** and choose the file. The stations appear with TVD, north, east and dogleg severity.
4. **Samples**: every sample of the well on the trajectory. **Plan and section**: the plan view and the vertical
   section, samples in red.

## Options

| Field | Meaning |
|---|---|
| Depth datum | elevation of the datum (kelly bushing, rotary table) above sea level: TVDSS = TVD − datum |
| North reference | true, grid or magnetic, as the survey gives the azimuths (recorded, not converted) |
| Columns | MD / Depth / Prof., Inc / Incl / Devi, Azi / Azim / Hazi, any order; comma, semicolon, tab or spaces |

## How it works

Minimum curvature (Bourgoyne et al. 1986; Sawaryn & Thorogood 2005): between two stations the well follows the arc
of a circle; ΔN, ΔE and ΔTVD are the half sums of the direction cosines times ΔMD, times the ratio factor
RF = (2/β)·tan(β/2), β the dogleg. A sample between stations lies on the same arc. Latitude and longitude come
from the head by the WGS 84 radii of curvature (local tangent plane).

## From a script

```python
st = prj.survey("ILL-WELL-1", "survey.csv", datum_elevation_m=25.0)
st[-1].tvd, st[-1].north, st[-1].east
rf.trajectory.sample_position(prj.raw, sample_id)     # {'tvd': …, 'tvdss': …, 'latitude': …, …}
```

## Limits and common problems

* Above the first station the well is taken vertical; below the last it keeps the last direction (marked
  *extrapolated*).
* Magnetic azimuths are not corrected for declination: convert them first or choose the reference that matches.

## Coverage

P8 (sample location: geographic position, well depth and trajectory).
