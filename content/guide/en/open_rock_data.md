# Open rock data: public micro-CT images

## What it is for

To try RockFace MC, compare methods or teach, without images of your own: public micro-CT images of sandstones and
carbonates, downloaded and imported into a sample with their licence and citation.

## Before you start

* A project with at least one sample (a description), and an Internet connection.
* Room on the disk: an image of 1000³ voxels takes about 1 GB, and the 2015 Imperial College archive several GB.

## Step by step

1. In RockFace MC, tab **Import**, click **Open rock data (public images)…**.
2. Choose an image in the table (collection, rock, image, size, licence). Below the table: the citation, the licence,
   the size of the download and the page of the source. **Read the licence before using the data, and cite the
   source.**
3. Choose the **Sample** that receives the volume and the **Download folder**.
4. Click **Download and import**. The file is downloaded once (a second import reuses it) and imported as a volume of
   the sample; its caption holds the citation and the licence.

## Options

* **Eleven Sandstones** (Digital Rocks Portal): eleven sandstones at 2.25 µm, 1000³ voxels, in three forms — grey,
  filtered and binary. Licence ODC-BY 1.0.
* **ICL sandstones and carbonates 2009** (Imperial College London): binary images of Berea, the S and LV60 sandstones
  and carbonates, in 7-Zip archives (the package `py7zr` is needed to open them).
* **ICL micro-CT 2015** (Imperial College London): Bentheimer, Doddington, Estaillades and Ketton, 1000³, grey, in one
  archive of several gigabytes.

## How it works

The list of images, addresses, sizes and voxel sizes follows the `drd` library of L. Mosser (Apache 2.0), which
GeoSlicer uses; the files are downloaded through a temporary `.part` file and imported out of core, a block at a time.

## From a script

```python
for e in rf.ProjectAPI.rock_data()[:3]:
    print(e.id, e.rock, e.licence)
v = prj.download_rock_data("eleven/Berea/binary", prj.descriptions()[0], folder="data")
```

## Limits and common problems

* **"The download … failed"** — no connection, or the source moved the file; try again later or download it from the
  page of the source and import it with **Import** (RAW, 1000 × 1000 × 1000, 8 bits).
* **"This archive is in the 7-Zip format"** — install `py7zr` (`pip install py7zr`).
* The binary images are imported as grey volumes with two values: segment them with a threshold (tab Segmentation).

## Coverage

GV17 (Open Rock Data).
