# Exporting and importing descriptions

## What it is for

A **RockFace exchange file** (`.rfx`, XML) carries descriptions from one project to another: to send a study to a
colleague, to gather the work of several petrographers, or to keep an archive in an open format. It keeps
everything of a description — identification, parts, composition, point count, classification, diagenesis — and the
analyses, requests and pictures of its sample; optionally the Atlas images of its thin section.

## Before you start

* A project with saved descriptions (to export), or an exchange file (to import).
* On a server, importing needs the petrographer level or above.

## Step by step

### Exporting

1. **Home → Reports and exchange → Export…** (Ctrl+E).
2. Tick the **Descriptions** to export.
3. Choose:
   * **Include the pictures** — the pictures of analyses, requests and counted points;
   * **Include the Atlas images of the thin sections** — every tile of their pyramids goes into the file
     (whole-slide images of several gigabytes are better moved with **Save project as…**);
   * **One file per description, in a folder**.
4. **Export…** and choose the file (or the folder). "N descriptions exported to …".

### Importing

1. **Home → Reports and exchange → Import…** (Ctrl+I).
2. **Files…** or **Folder…** (every `.rfx` and `.xml` in it).
3. The list shows each **Description**, its **File** and whether it is **In this project** (*new* or *name already
   used*). Tick those to import.
4. **Names already in the project**:
   * **Import with a new name: (2), (3)…**
   * **Skip them**
   * **Replace the descriptions of the project** (asks for a confirmation).
5. **Import**. The result names what was imported, renamed or not imported, and why.

## Options

| Option | What it changes |
|---|---|
| Include the pictures | Attachments go into the file (base64). |
| Include the Atlas images | The images of the thin sections, with their annotations, maps and spots. |
| One file per description | A folder of files instead of one file. |
| Names already in the project | Rename, skip or replace. |

## How it works

The file is checked before anything is imported (format version, codes known to this RockFace, totals of the
project). Wells, samples and thin sections are matched by name and numbers, so two descriptions of the same thin
section stay together; identifiers are mapped to the new project; the summaries (totals, classifications) are worked
out again. Files written by any earlier RockFace are read. Custom totals of the exporting project travel with the
file.

XML of other programs is read through a mapping (Home → **Import XML with a mapping…**, page [Sample catalogue, Touchstone-ready table and XML by mapping](catalogue_exchange.md)).

## From a script

```python
with rf.open("study.rockface") as prj:
    prj.export("for-the-lab.rfx", names=["TS-9", "TS-10"], images=True)
    prj.export_folder("archive", names=None)               # one file per description
with rf.create("copy.rockface") as other:
    for r in other.import_file("for-the-lab.rfx", policy="skip"):
        print(r["name"], r["action"], r["as"], r["messages"])
print(rf.read_exchange("for-the-lab.rfx").names())         # read without importing
```

## Limits and common problems

* "No descriptions in the files chosen."
* "…: not imported — …": the reason (unknown code, a file written by a newer RockFace…).
* Replacing cannot be undone.

## Coverage

P2 (Export, Import), P36 (XML generator for batches), P37 (XML importer: files or folders, name conflicts).
