# Exporting wells to WITSML and samples to OSDU

## What it is for

* **WITSML** (Energistics) is the format of well data that reservoir-modelling and well-data programs read. It lets
  the petrography of the samples, and the image logs and curves of RockFace MC, sit beside the other logs of a well.
* **OSDU** is the open data platform of the energy industry. Its manifest lets the wells, samples, thin sections,
  descriptions, laboratory analyses and images of a project be ingested into an OSDU data platform, including the
  Rock and Fluid Sample service.

## Before you start

* **For WITSML:** the samples need a well and a depth. The curves are those of Explorer's LAS export.
* **For OSDU:** ask the platform's data manager for the **data partition** and the **legal tag** to use.

## Step by step

### WITSML

1. In RockFace Petro, choose **Home → Reports and exchange → Export WITSML**.
2. Choose a folder. RockFace writes, for each well:
   * `<well>_well.xml` and `<well>_wellbore.xml`: the well and its wellbore;
   * `<well>_samples_log.xml`: one row per sample depth, with core porosity, permeability, grain density, visual
     porosity and facies;
   * one `<well>_<log>_log.xml` for each well log of RockFace MC. Image logs become array curves, one value per
     azimuth.
3. Load the files into the target program as WITSML 1.4.1.1 well, wellbore and log objects.

### OSDU

1. Choose **Home → Reports and exchange → Export OSDU manifest**.
2. Choose the file name, then type the **data partition** and the **legal tag**. An empty legal tag writes a
   placeholder, to be replaced before ingestion.
3. Give the JSON file to the platform's manifest ingestion.

## Options

From a script or the command line you can choose:

* the descriptions;
* the curves of the samples' log and the depth used (measured, corrected, adjusted);
* whether to include the MC logs and the image logs;
* for OSDU, the access groups and the countries.

## How it works

* **WITSML.** RockFace writes WITSML 1.4.1.1 with its own code. The element order follows the WITSML 1.4.1.1
  schema. The index is the measured depth in metres; missing values are left empty, with `-999.25` as the null
  value.
* **OSDU.** Wells and wellbores become `master-data--Well` and `master-data--Wellbore`. Samples and thin sections
  become `master-data--Sample` (a thin section is a child sample of its sample). Descriptions and laboratory
  analyses become `work-product-component--SamplesAnalysis`, and images `work-product-component--SampleImage`.
  * The petrography — composition with percentages, classifications, the codes of RockFace's nomenclature — goes
    in `ExtensionProperties.RockFace`, because OSDU has no petrography schema yet.
  * The mapping table is in `docs/SERVER.md`.

## From a script

```python
import rockface.api as rf
with rf.open("project.rockface") as prj:
    prj.export_witsml("witsml_folder")
    prj.export_osdu("manifest.json", partition="my-partition", legal_tag="my-partition-legal")
```

Or: `rockface export witsml project.rockface folder` and `rockface export osdu project.rockface manifest.json
--partition my-partition --legal-tag my-partition-legal`.

## Limits and common problems

* **WITSML validation.** The files were checked by reading them back, not against the official schema files.
  Please report any program that refuses them, using the feedback form.
* **OSDU schema versions.** The versions used are written in the manifest. If the platform uses others, the data
  manager may need to adjust them.
* **Images.** OSDU image records describe the images; the image files stay in RockFace. Export the images from
  Atlas to attach them as datasets.

## Coverage

P38 (WITSML export), L13 (OSDU).
