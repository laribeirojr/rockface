# Microporosity: porosity maps, Darcy permeability and the Microtom simulations

## What it is for

A micro-CT volume resolves the large pores but not the pores smaller than its voxel: a voxel of microporous cement or
clay is grey, between the pore and the grain. The **Microporosity** tab of RockFace MC turns the volume into a
**porosity map** (each voxel 0 = solid … 1 = resolved pore, the microporosity in between), computes the **Darcy
permeability** of that map, and runs the **Microtom** simulations on a segmentation: pore-size distributions,
mercury intrusion and capillary drainage, imbibition, and the absolute permeability by lattice Boltzmann.

## Before you start

* A grey micro-CT volume and its segmentation on the same grid (tab Segmentation), with a segment for the resolved
  pores, one for the microporous phase and one for the grains.
* For the method from saturation: a dry scan and a scan of the same plug saturated with a contrast fluid, registered
  on the same grid (tab Registration), and the segmentation.
* The Microtom simulations work on a segmentation with the role "pore" on its pore segments.

## Step by step

### Make a porosity map

1. Open the grey volume and go to the **Microporosity** tab.
2. In **Porosity map**, choose **From**: *a segmentation* or *a dry and a saturated scan*.
3. Choose the **Grey volume** (or the **Dry scan** and the **Saturated scan**) and the **Segmentation**.
4. Check the **Role of each segment**, written as `Segment=role; …`: `macro` (resolved pore, porosity 1), `micro`
   (microporous: porosity from the attenuation), `solid` (porosity 0) and `high` (dense minerals, porosity 0). The
   proposal comes from the segment names and roles; type over it to change it.
5. Keep **Pore and solid attenuations from the medians of their segments**, or untick it and type the
   **Attenuation of pore / solid**.
6. Click **Make the porosity map**. The map is a new volume (category *porosity*); the table gives the total
   porosity, the resolved part and the microporosity.

### Darcy permeability of the map

1. Open the porosity map.
2. In **Darcy permeability of the map**, choose the **Permeability of a voxel**: *power law k = a·φ^b* (type a in
   mD and b) or *Kozeny–Carman* (type the **Grain diameter**). The resolved pores get the permeability of a tube as
   wide as the voxel.
3. Click **Calculate the permeability of the current map**: K along x, y and z.

### Microtom simulations

1. Open the segmentation.
2. Choose the **Simulation** and its options, and click **Simulate on the current segmentation**. A map made by the
   simulation (pore radius, entry radius) is kept as a new volume; the chart and the table show the curve.

## Options

| Field | What it changes |
|---|---|
| Simulation | *Pore-size distribution (local thickness)*: the radius of the largest ball that holds each pore voxel, as a cumulative curve. *Pore-size distribution (non-overlapping spheres)*: balls placed largest first without overlap (a hierarchical count). *Mercury intrusion (MICP)*: σ 0.485 N/m, θ 140°, from one face. *Capillary drainage*: the same with your σ and θ. *Imbibition* and *Imbibition with trapping (Sor)*: the wetting fluid comes back from the small pores; with trapping, the oil cut off from the outlet stays (Sor). *Absolute permeability (lattice Boltzmann)* and its *REV* on cubes of growing edge |
| Direction of invasion | The face the fluid enters from (x, y or z) |
| Radius steps | Number of radii of the curves |
| Interfacial tension / contact angle | σ and θ of drainage and imbibition |
| Relaxation time / tolerance | τ of the lattice-Boltzmann model (1.5 by default) and the relative change of the mean velocity at which the flow is steady |
| At most (voxels) | The simulation runs on the finest level of the pyramid with at most this number of voxels |

## How it works

* **Porosity from the attenuation**: in the microporous phase φ = (I_solid − I) / (I_solid − I_pore), clipped to
  0…1; the resolved pores are 1, the solid 0. From a dry and a saturated scan, φ = (Δ − Δ_solid) / (Δ_pore − Δ_solid)
  with Δ = I_saturated − I_dry, the difference of the two scans relative to those of a resolved pore and of the solid.
  Both are linear mixing models of the attenuation.
* **Darcy permeability of the map**: each voxel gets k(φ) and the pressure equation ∇·(k ∇p) = 0 is solved with a
  finite-volume scheme (harmonic means between voxels), pressure fixed on two opposite faces; K = Q L / (A Δp). Exact
  on layered maps (arithmetic and harmonic means).
* **Pore sizes**: local thickness (Hildebrand & Rüegsegger 1997) from the Euclidean distance map.
* **Drainage and MICP**: morphological invasion (Hilpert & Miller 2001): at the radius r the non-wetting fluid fills
  the balls of radius r whose centres connect to the inlet face; P = 2σ|cos θ| / r (Washburn 1921).
* **Lattice Boltzmann**: D3Q19, two-relaxation-time collision (Ginzburg, Verhaeghe & d'Humières 2008) with the magic parameter 1/8 that
  places the bounce-back wall half-way between the nodes; a body force drives the flow and K = ν ⟨u⟩ / g. The sample
  is joined to its mirror image along the flow, so the boundaries are periodic. Checked on plane Poiseuille flow
  (exact) and on arrays of spheres against Sangani & Acrivos (1982).

## From a script

```python
grey, seg = prj.volume("plug grey"), prj.volume("plug segmentation")
phi, info = grey.porosity_map(seg, {1: "macro", 2: "micro", 3: "solid"})
k = phi.darcy(model="power", a_md=50, b=3)
psd = seg.microtom("psd")
lbm = seg.lbm_permeability(axes=("x", "y", "z"))
```

## Limits and common problems

* The attenuation of the microporous phase must lie between those of the pore and the solid; a dense mineral in the
  microporous segment reads as solid. Give such minerals their own segment with the role `high`.
* The lattice-Boltzmann run grows with the number of pore voxels: a 128³ cube of a sandstone takes about an hour on
  two processor cores. Send it as a job (Multiscale tab → Jobs) or reduce **At most (voxels)**.
* Below about 4 voxels across, a throat is not resolved by the lattice Boltzmann model; the voxel size sets the
  smallest pore that flows.

## Coverage

GV9 (microporosity), GV10 (Microtom), GV11 (flow modelling and permeability).
