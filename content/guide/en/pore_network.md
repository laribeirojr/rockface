# Pore network: extraction, permeability, mercury intrusion, relative permeability, production

## What it is for

The pore space of a micro-CT volume turned into a network of pores (the bodies) joined by throats (the
constrictions), on which the flow is computed: the absolute permeability along x, y and z, the mercury intrusion
curve (MICP) to compare with the laboratory, the relative permeability curves of oil and water (drainage then
imbibition), the oil recovery of a waterflood, and how all of these change with the wettability.

## Before you start

* A segmented volume of the sample in RockFace MC (tab Segmentation), with the pore segments marked with the role
  "pore" — or an objects volume (tab Analyses → Objects of the pore space), whose objects become the pores.
* Or a network in the Statoil format (the four files `*_node1.dat`, `*_node2.dat`, `*_link1.dat`, `*_link2.dat` of
  pnextract and pnflow, as the Imperial College networks).
* A large volume is extracted at the finest level of its pyramid under 64 million voxels; crop it first (Volume →
  Crop) to work at full resolution.

## Step by step

### Extract the network

1. Open the segmented volume and go to the **Pore network** tab.
2. In **Extraction (SNOW)**, keep **Smoothing of the distance map** 0.40 and **Radius of the peak search** 4 voxels
   (the values of the SNOW algorithm), give a **Name** if you wish, and click **Extract the network of this volume**.
3. The network appears in **Network** with its numbers (pores, throats, mean coordination number, isolated pores, mean
   radii, porosity of the network), drawn in 3D: drag to turn, wheel to zoom; **Colour of the pores** by radius or by
   coordination number. The regions of the pores are kept as an objects volume.
4. **Import Statoil…** reads a network made elsewhere; **Export Statoil…** writes the current one (flow along the
   axis chosen in **Flow along**); **Delete the network** removes it from the project.

### Run a simulation

Choose the **Simulation**, its parameters, and click **Run**. The chart and the table show the result; every result
is kept with the network.

* **Absolute permeability (one phase)** — K along x, y, z (or one axis) in mD and m².
* **Mercury intrusion (MICP)** — the mercury saturation against the pressure (log), with the throat radius of each
  step in the table.
* **Relative permeability (two phases)** — drainage (oil into the water-filled rock) then imbibition (water back):
  krw and kro against Sw, Pc of each step; Swi, Sor and the end points in the status bar.
* **Sensitivity test** — the two-phase run repeated for every value of one parameter (**Vary**, values separated by
  `;`): the cloud of curves and its mean, the table of the results of each run and the correlations of the parameter
  with each result.
* **Kabs REV** — the volume cut into centred cubes of growing edge, each extracted again, and the permeability of each
  size: where it stops changing, the volume is representative.

### After a two-phase run

* **Animate the cycles** — the pores coloured by their fluid at each step (oil red, water blue); the slider chooses
  the step.
* **Production prediction** — the waterflood of the imbibition curve (Buckley–Leverett): oil recovered against the
  pore volumes of water injected; after a sensitivity test, every curve and the pessimistic, neutral and optimistic
  predictions (P10, P50, P90).
* **Reference curve (CSV)…** — a measured krel curve (columns `Sw`, `krw`, `kro`) drawn with the simulated one.
* **Report (HTML)…** — one page with the network, the permeability, MICP, krel, production and REV.

## Options

* **Mercury**: surface tension 0.485 N/m and contact angle 140° by default.
* **Oil–water interfacial tension** (0.03 N/m), **viscosities** of water and oil.
* **Receding contact angle** (drainage) — its centre and **range** (the angles of the elements spread uniformly over
  the range); **Advancing − receding angle**: the advancing angle of imbibition. Below 90° the rock is water-wet,
  above 90° oil-wet.
* **Sw step** — the saturation between two computed points; **Minimum Swi** — where drainage stops.
* **Lower / upper plane of the box** — the saturation and the flow are computed between these planes (0.1 and 0.9 of
  the length by default, as pnflow's calculation box): the pores beyond them hold the pressures.

## How it works

* **Extraction**: the distance map of the pore space, smoothed, its maxima as markers (a marker nearer to a higher
  one than to the solid dropped), the watershed: each region a pore, each contact of two regions a throat (Gostick
  2017). Pore radius: the largest distance in the region; throat radius: the largest on the contact; shape factor of
  a throat G = r² / (4 A) from its area A.
* **Flow**: each conduit (half pore, throat, half pore) three ducts in series, g = k G A² / μ (k = 3/5 triangle,
  0.5623 square, 1/2 circle; Patzek & Silin 2001); the pressures of the pores solved; K = Q μ L / (A ΔP).
* **MICP**: mercury enters from every face, an element at P = −2 σ cos θ / r (Washburn 1921) if a neighbour is
  already filled.
* **Two phases**: drainage by invasion percolation from the inlet face, water kept in the corners; imbibition by
  snap-off in throats, σ (cos θ − sin θ tan β) / r, and piston-like filling, 2 σ cos θ / r, oil trapped when it loses
  its path to the outlet; kr from the conductances of each phase (Valvatne & Blunt 2004, simplified).
* **Production**: the fractional flow, the Welge tangent and the recovery (Buckley & Leverett 1942; Welge 1952).

## From a script

```python
seg = prj.volume("ILLUSTRATIVE sphere pack")
net = seg.extract_network(name="ILLUSTRATIVE network")
print(net.stats()["coordination_mean"])
k = net.kabs()                         # {"x": {"K_mD": …}, …, "mean_mD"}
m = net.micp()
kr = net.two_phase(theta_r=30, separation=20, swi_min=0.2)
pr = net.production(kr, mu_w=1e-3, mu_o=5e-3)
runs = net.sensitivity({"theta_r": [20, 40, 60]})
net.export_statoil("pack")             # pack_node1.dat …
net.report("network.html")
berea = prj.import_statoil("Berea_node1.dat")
```

## Limits and common problems

* **"Nothing flows from face to face"** — the pores do not connect the two faces along that axis: try another axis,
  or the segmentation misses the small pores.
* The two-phase model is a simplified one: no cooperative pore filling, no oil layers, no film swelling; in a strongly
  water-wet rock snap-off dominates and kro falls early. Compare with measured curves (Reference curve) before using
  the values.
* The extracted radii come from the distance map at voxel centres: throats one voxel wide are not resolved.
* Extracting 64 million voxels (400³) takes about 1.5 minutes and 3.5 GB of memory.
* Microporosity (unresolved pores) and multiscale networks come in stage 0.25.

## Coverage

GV12 (Pore Network: Extraction, Simulation — one phase, two phases, mercury injection —, Kabs REV, Krel EDA,
Production Prediction, Cycles Visualization, PNM report).
