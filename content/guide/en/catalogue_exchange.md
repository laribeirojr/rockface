# Sample catalogue, Touchstone-ready table and XML by mapping

## What it is for

**Sample catalogue** browses the wells and samples of a corporate catalogue and imports the chosen files.
**Touchstone-ready table** writes the petrographic quantities that diagenetic modelling uses. **Import XML with a
mapping** reads descriptions written by another program.

## Before you start

* Catalogue: a shared folder `<well>/<sample>/` (optionally a `sample.json` with `top_m`, `base_m`, `type`), or an
  OSDU platform with a token in `ROCKFACE_OSDU_TOKEN`.
* XML import: the XML file and a mapping (JSON) that says where things are in it.

## Step by step

1. **Petro → Home → Sample catalogue…**: choose *Shared folder* or *OSDU platform*, the address, **Connect**; search
   a well; tick the files of its samples; **Import the checked files**. Pictures go to Atlas, volumes to MC, LAS
   files to the well's logs, PDF reports to the sample's analyses.
2. **Petro → Home → Touchstone-ready table…**: choose where to save the CSV.
3. **Petro → Home → Import XML with a mapping…**: choose the XML, then the mapping. Codes without a match are listed.

## Options

| Mapping key (XML) | Meaning |
|---|---|
| description | path of a description element (e.g. `.//description`) |
| name, well, top_depth, thin_section | paths inside it (`@attr`, `child`, `child/@attr`) |
| line, code, percent, points | the composition lines and their fields |
| codes | the other program's codes → RockFace constituents |

The Touchstone mapping lists the columns: each a field (name, well, depth, grain size, sorting) or a sum of totals
or constituents.

## How it works

* The catalogue uses connectors with the same three questions (wells, samples, a file): a folder, or the OSDU
  Search service (`POST /api/search/v2/query`). The well and the sample are found or created by name and depth.
* The Touchstone input format is not published: the table carries the quantities of the published model (Lander &
  Walderhaug 1999; Lander et al. 2008) and says in its first line that it is not that format.
* Mapped XML: every code must match a constituent of the nomenclature; nothing is guessed.

## From a script

```python
cat = rf.catalogue.FolderConnector("//share/catalogue")
s = cat.samples("ILL-WELL-A")[0]
rf.catalogue.import_items(prj.raw, cat, s, s.items)
prj.touchstone_table("touchstone.csv")
prj.import_mapped_xml("descriptions.xml", mapping)
```

## Limits and common problems

* A connector to a corporate sample catalogue will be added when its interface is documented to RockFace.
* An XML of another program and the "Touchstone format" will be named so only after real files have been read.

## Coverage

GV16 (catalogue browser; corporate connector pending), P35 (Touchstone; final with a real file), P37 (XML importer).
