# Importing descriptions from another program (XML)

## What it is for

Thin-section descriptions made in another petrography program can be brought into RockFace without typing them
again, when that program writes each description as an XML file whose root element is `ThinPetrographicDescription`. RockFace reads the identification, the gravel, sand and mud, the composition with its
points and percentages, and the interpreted diagenetic environment, and adds them to the project as RockFace
descriptions.

## Before you start

* **In the program of origin**, export the descriptions as XML files (one file per description). The language of
  the export does not matter.
* **Not this file:** an export for Touchstone (Geocosm) is also XML, but it is not a description. RockFace
  recognises it and says so.
* **In RockFace**, open the project that will receive the descriptions.

## Step by step

1. In RockFace Petro, choose **Home → Reports and exchange → Import descriptions from another program (XML)…**.
2. Choose **Files…** (one or more XML files) or **Folder…** (every description file in the folder).
3. The upper table lists the descriptions found, with the number of composition lines and whether the name is
   already in the project. Untick the ones you do not want.
4. The lower table lists the **numbers without a match**: each term of the other program has a number. For each
   row, choose the RockFace term it becomes, or leave **(do not import: keep as text)**.
5. Keep **Remember these matches in this project** ticked, so the next files need nothing.
6. Choose what to do with a name already in the project (rename, skip, replace) and click **Import**.

## Options

| Option | What it does |
|---|---|
| Remember these matches | The numbers you mapped are kept in the project and used by every later import |
| Name already in the project | **Rename** adds "(2)", **Skip** leaves the existing one, **Replace** deletes it and imports again |
| (do not import: keep as text) | The line is not imported; it is written, with its name, number and amount, in the composition notes |

## How it works

* **The numbers.** Every term in the file has a name, in the language of the export, and a number that does
  not change with the language. RockFace carries the numbers to its own terms. Only the numbers whose meaning was
  checked to be the same in both programs are built in. You add the others once.
* **Nothing is guessed.** A line whose term has no match is kept as text in the composition notes. An attribute
  (location, habit, modifier, paragenetic relation) without a match, or one the RockFace term does not take, is left
  out of the line and written in the notes too. Map the number and import again with **Replace**.
* **Generic terms.** When the other program records quartz, feldspar, silica or carbonate without saying
  which kind, the line becomes RockFace's undifferentiated term (Folk 1980): it counts in the totals of quartz,
  feldspar, silica or carbonate, and the QmFLt diagram says it cannot place a sample with quartz of no told kind.
* **Identification.** Description, thin section, core, box, plug, well or outcrop, top and base depths, field, unit,
  basin, country, state, institution, petrographer, observation and uses go to their fields. Place, project, typist,
  edition dates, rock class, support and the interpreted environment have no field in RockFace: they are written,
  word for word, in a block of the observations headed "[Imported from XML (ThinPetrographicDescription)]".
* **Points and percentages.** When the description was counted, the points are imported and RockFace computes the
  percentages. Otherwise the percentages are imported. The totals written in the file are not imported: RockFace
  computes its own.
* RockFace keeps only the other program's numbers and its own terms. It does not copy that program's names,
  definitions or rules.

## From a script

```python
import rockface.api as rf

print(rf.read_tpd("D-01.xml")["lines"])
with rf.open("project.rockface") as prj:
    res = prj.import_tpd(["exports/"])
    print(res["unknown"])                      # numbers to map once
    prj.save_tpd_mapping({"constituent": {"115": "quartz_mono"}})
    prj.import_tpd(["exports/"], on_conflict="replace")
```

## Limits and common problems

* **Images and point coordinates** are not in these XML files.
* **Lines in the notes.** Map their numbers in the lower table, then import again with **Replace**.
* **Other versions of the format.** The files read so far were written with format version 3.3.0. Other
  versions are read the same way. Please report any file that is not read, using the feedback form.
* **The other direction** — files written by RockFace for the other program and for Touchstone — will come in a
  later version, when the files needed to check it are available.

## Coverage

P37 (XML importer; the program of origin's own files read since 0.32).
