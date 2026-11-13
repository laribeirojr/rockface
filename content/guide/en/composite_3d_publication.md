# From the 2D composite to the 3D composite, and publishing

## What it is for

The mineral map of a thin section says what every grain is; the micro-CT of the plug shows the grains in 3D but not
what they are. **3D composite** carries the map's phases into the whole volume, and gives each phase its
properties. **Publication** sends the project — samples, descriptions, analyses, images — to the corporate data
environment on a schedule, only what changed.

## Before you start

* A micro-CT volume of the sample and a mineral map (or a segmentation) of its thin section.
* The map located in the volume: **MC → Register → Locate the image** (or both images calibrated in the section
  frame when another image of the same section was located).
* For publishing: a folder watched by the platform's ingestion, or the address of an OSDU platform and a token.

## Step by step

1. Locate the map (or the optical picture) in the volume; save the placement.
2. In a script or the script window: `prj.composite_3d(map, volume)` — the map's phases on the slice train a model
   on the grey volume, a quarter of the slice is held out to measure the agreement, and the whole volume is
   classified.
3. Give the phases their properties: `rf.composite3d.property_volume(...)` makes a float volume per property.
4. Publishing: `rockface publish project.rockface --folder <path> --period 24` (or `--url <platform>`), then
   `rockface publish project.rockface --if-due` from the system's scheduler (`--schedule` prints the lines).

## Options

| Setting | Meaning |
|---|---|
| hold_out | share of the slice kept out of training to measure the agreement (default 0.25) |
| method | random forest or Gaussian Bayesian model |
| target | `folder` (manifest files) or `rafs` (OSDU Storage + RAFS DDMS) |
| period_hours | how often `--if-due` publishes |
| token_env | the environment variable with the access token (ROCKFACE_OSDU_TOKEN); never stored |
| analysis_type, content_version | RAFS content type and schema version of the routine core analyses |

## How it works

* The map is sampled at every voxel of the placed slice through the placement matrix; background phases do not
  train. The model is the random forest of MC with the features of the grey volume.
* Publication builds the OSDU manifest of the project, compares each record with the SHA-256 of what was sent, and
  sends only the changed ones: to a folder (a numbered JSON written atomically) or to the platform — wells and
  wellbores by `PUT /api/storage/v2/records`, samples by `POST /api/rafs-ddms/v2/masterdata`, descriptions and
  analyses by `POST /api/rafs-ddms/v2/samplesanalysis`, and the routine core analyses as content data
  (`/samplesanalysis/{id}/data/{type}`), with the headers `Authorization` and `data-partition-id`.

## From a script

```python
c = prj.composite_3d(map_img, vol)                    # Composite3D(labels_id, held_out={'accuracy': …}, …)
pv = rf.composite3d.property_volume(prj.raw, c.labels_id, {"Calcite": 2.71, "Quartz": 2.65}, "Grain density",
                                    "g/cm³")
prj.publication(target="folder", folder="//share/osdu-inbox", period_hours=24)
prj.publish()                                         # {'sent': …, 'unchanged': …, 'file': …}
```

## Limits and common problems

* The 3D composite is as good as the contrast of the phases in the CT: phases with the same attenuation (calcite
  and dolomite at low energy) are told apart only with a second volume (another energy) as an extra channel.
* Check the RAFS content schema of the platform (`GET /api/rafs-ddms/v2/samplesanalysis/{type}/data/schema`) before
  the first publication; the petrography travels in ExtensionProperties until RAFS has a schema for it.

## Coverage

L13 (2D composite → tomography → 3D composite with properties; containers, model hub, periodic incorporation, OSDU
RAFS DDMS).
