# MC → More: cups, distance map, folder watch, reconstruction, upscaling and two-phase flow

## What it is for

Tools found by the audit of the GeoSlicer source: calibrate grey values with **reference cups**, measure the
**distance** to the edge of a segment, import scans from a **folder** while the scanner writes them, **reconstruct**
a SkyScan acquisition, carry core measurements to the **LAS** depth samples and plug measurements **along the
core**; on image logs, segment a **depth range** and trace a level across the 0/360° seam; simulate **two-phase flow** on a segmented volume with LBPM.

## Before you start

A sample with volumes (MC), or a well with image logs.

## Step by step

1. **MC → More → Reference cups**: open the scan with its plug and the Teflon, quartz and aluminium cups; **Find the
   cups around the plug**; type the values they should have; **Remap the grey values** (a new volume).
2. **Distance map**: on a segmented volume choose the segment; **Distance to the edge of the segment (µm)**.
3. **Watch a folder**: choose the scanner's output folder; **Start watching**: every scan that stopped growing is
   imported; numbered names make a time sequence.
4. **Reconstruction (FDK)**: a SkyScan folder (projections and `.log`); **Reconstruct**.
5. **Two-phase flow (LBPM)**: open a segmented volume; give the segments of fluid A (LBPM label 1) and fluid B
   (label 2), the solid components that wet differently, the wetting affinity of the solid and the process grid;
   **Write the case** (the folder, the command and a SLURM script `run_lbpm.sh`), or **Run here as a job** /
   **Run on the remote computer** (the computer of MC → Multiscale → Jobs (batch and remote));
   **Read the results** shows the end points and the curves.
6. Upscaling, plug to core and the log tools are in the API (below).

## How it works

* Cups: the plug's cylinder is found, the voxels around it split by a four-class Otsu (air and three references)
  and 1-D k-means; the remap is the least-squares line through the references.
* Distance: the Euclidean distance transform with the voxel size of each axis.
* Folder watch: a dataset is imported when its size and time are the same on two looks.
* Reconstruction: Feldkamp–Davis–Kress for a cone beam on a circular orbit (Feldkamp et al. 1984; Kak & Slaney
  1988) and filtered back-projection for a parallel beam, in NumPy (GeoSlicer's uses ASTRA, GPL, which RockFace
  cannot ship); attenuation in 1/mm.
* Upscaling to LAS: the mean of the core values inside each LAS sample window; plug to core: a random forest (or a
  linear fit) of the plug values on the core's CT features, checked leave-one-out before use.
* Logs: a depth range written as a segment; level tracing grows the region of similar values from a seed, connected
  across the seam of a full-turn log.
* Two-phase flow: LBPM (McClure et al. 2021; GPL-3.0, so RockFace does not contain it — it runs the user's own
  installation). The case: the volume as LBPM's 8-bit RAW (x fastest) and `input.db`, its `Domain` written to match
  — size, process grid and sub-domains, voxel length in µm, the segments mapped to 0 (solid), 1, 2 and negative
  labels for the solid components with their `ComponentAffinity`; the other sections from LBPM's documentation
  (colour model, fractional-flow protocol). The results: `timelog.csv` (relative permeability against the
  saturation) and `subphase.csv` (saturation from the connected and disconnected phase volumes, capillary pressure
  pn − pw, interfacial area, Euler characteristic), as GeoSlicer's Pore Scale Modelling reads them.

## From a script

```python
c = rf.gs_tools.cups(prj.raw, vol_id); rf.gs_tools.remap(prj.raw, vol_id, c.medians, {"teflon": 1000, "aluminium": 3000})
rf.gs_tools.distance_map(prj.raw, labels_id, 1)
vol, voxel_um = rf.gs_tools.reconstruct_skyscan("acquisition_folder")
rf.gs_tools.upscale_to_las(depth, porosity, "well.las", "out.las", compare="PHIT")
rf.gs_tools.plug_to_core(core_depth, features, plug_depth, plug_porosity)
rf.log_edit.fill_depth_range(prj.raw, log_id, 1001.0, 1001.2, 2)
rf.log_edit.level_trace(prj.raw, grey_id, labels_id, azimuth=10, depth=1000.5, tolerance=10, value=3)
res = prj.lbpm(labels_id, {1: "fluid_a", 2: "fluid_b"}, "lbpm-case", nproc=(2, 2, 1))   # needs LBPM installed
prj.lbpm(labels_id, {1: "fluid_a"}, "lbpm-case", run=False)       # only the case and its command
```
`rockface notebook project.rockface` writes a Jupyter notebook that opens the project with the API.

## Limits and common problems

* The reconstruction expects flat-corrected projections (as SkyScan writes them) and a centred rotation axis.
* Plug to core needs plugs that span the range of the core; the leave-one-out error says how far to trust it.
* LBPM must be installed where the job runs (here, the remote computer or the cluster); each size of the volume must
  divide by the process grid. The pressures are in lattice units.

## Coverage

GeoSlicer audit of 0.28 (GV20–GV28, GI12–GI13).
