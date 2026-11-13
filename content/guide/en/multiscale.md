# Multiscale: image generation (MPS), comparison of the realizations and the two-scale pore network

## What it is for

A plug scanned at high resolution covers a few millimetres; an image log or a core scan covers metres at a coarser
resolution. The **Multiscale** tab of RockFace MC joins the scales: it **generates 3D images** of the fine scale
with the statistics of a training volume, conditioned by what is known at the coarse scale (hard data, or an image
log wrapped on the borehole wall), **compares** the realizations with the training image, and extracts a
**two-scale pore network** from a porosity map, where the microporous voxels become unresolved pores.

## Before you start

* For MPS: a training volume (a segmentation, for a categorical simulation, or a grey or porosity volume, for a
  continuous one). Optionally a hard-data volume on the grid of the simulation (0 or empty = no datum) or an image log
  of the well.
* For the two-scale network: a porosity map (tab Microporosity).

## Step by step

### Generate images (MPS)

1. Go to the **Multiscale** tab; in **Image generation (MPS)** choose the **Training volume**.
2. Optionally choose **Hard data (volume)** or **Hard data (image log on a cylinder)**: the log's columns are laid on
   the wall of a vertical cylinder of the grid, one row per slice.
3. Type the **Grid (z y x)** of the simulation (empty: the grid of the training volume), the number of
   **Realizations** and the **seed**.
4. Set the **Neighbours / search radius / distance threshold** of the direct sampling, and click **Simulate**.
   Each realization is a new volume of the sample (category *simulation*).

### Compare the realizations

Click **Compare the realizations**: the chart shows the porosity of every slice of each realization against the
training image, and the table the mean pore radius of each (pore-size distribution by local thickness).

### Two-scale pore network

1. In **Two-scale pore network** choose the **Porosity map**.
2. Choose the **Radius of the unresolved pores**: *fixed* (type it), *Leverett J (from k)*, or *from a MICP curve*,
   and the **tortuosity** and the **block** size (voxels of microporosity gathered into one unresolved pore).
3. Click **Extract and calculate the permeability**. The network is kept in the project (tab Pore network, where all
   the simulations of 0.24 run on it) with its permeability along x, y and z.

## Options

| Field | What it changes |
|---|---|
| Neighbours | Number of informed nodes nearest to the node simulated that make its pattern (24 by default) |
| Search radius | How far the neighbours are looked for (voxels) |
| Distance threshold | The training image is scanned until a pattern differs by less than this fraction (0.05: at most one neighbour of twenty in another class) |
| Radius of the unresolved pores | *fixed*: one radius; *Leverett*: r = √(8k/φ) from a permeability k of the microporous phase; *MICP*: radii drawn from a mercury curve, the largest to the most porous blocks |
| Tortuosity / block | τ of the capillary-bundle model of the microporous plugs; the edge of the cubes of microporous voxels that make one unresolved pore |

## How it works

* **Direct sampling** (Mariethoz, Renard & Straubhaar 2010): the nodes are visited in a random order; for each one the
  pattern of its informed neighbours is compared with patterns at random places of the training image, and the value
  of the first place close enough (or of the closest one scanned) is pasted. Hard data are informed from the start
  and kept.
* **The two-scale network** (after Bultreys et al. 2015): the resolved pores (φ = 1) are extracted by SNOW as in 0.24;
  the microporous voxels are gathered into cubes that become unresolved pores, of volume Σφ and radius given by the
  subscale model. A conduit that touches an unresolved pore is a porous plug of permeability k = φ r² / (8 τ) (a
  bundle of capillaries of radius r and tortuosity τ), conductance k A / L. A binary map gives exactly the network of
  0.24; a uniform microporous block gives exactly k of the plug.

## From a script

```python
seg = prj.volume("plug segmentation")
reals = seg.mps(realizations=5, shape=(64, 128, 128), log=prj.log("AMP image log"), seed=3)
net = prj.volume("plug porosity map").multiscale_network({"kind": "fixed", "radius_um": 0.5}, tortuosity=2.0)
print(net.kabs())
```

## Limits and common problems

* Direct sampling slows down with large training images and strict thresholds: start with a small grid, a threshold of
  0.1 and the scanned fraction 0.05 (``fraction`` in a script), then refine. Long runs can go as jobs.
* The generative network (RockSinGAN) of the reference program is an AI model; it comes with the AI stage (0.26).
* The subscale models are simple: the microporous plugs are capillary bundles; use a MICP curve of the
  microporous phase when the laboratory has one.

## Coverage

GV13 (multiscale), GM5 (image generation — MPS; the generative network in 0.26), GM6 (post-processing), GM7 (pore
network across scales), GM3 (image-log preprocessing: the log on a cylinder), GM4 and GM8 (preprocessing and
segmentation of the scales, with the tools of 0.20–0.23).
