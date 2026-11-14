# Mio writes scripts for repetitive tasks

## What it is for

Every task you repeat — the report of each description, the classification table of a well, the LAS of each well,
the figures of all the samples, a Lab flow over every picture — can become a **Python script** that runs in seconds.
You need not write it: ask Mio. She writes the script from the request, already with the samples you described, and
opens it in the script window. You read it, change it if you wish and run it. Nothing runs by itself.

## Before you start

* A project open.
* No knowledge of Python is needed to use the script Mio writes; to change it, the page
  [Python scripting](scripting.md) explains the programming interface.

## Step by step

### Ask for a script

1. Open Mio's panel (Mio button, or Ctrl+Alt+M).
2. Ask with the word **script** (or **automate**, **routine**, **python**) and say the task and the samples:
   * `@mio write a script that makes the Word report of each description with calcite`
   * `@mio script for the Folk and McBride classification table`
   * `@mio script that exports the LAS of each well`
   * `@mio automate the powerpoint presentation of the samples with porosity above 15`
   * `@mio script for the Dickinson ternary diagram`
   * `@mio script for the samples without porosity`
   * `@mio script that runs the lab flow on all the images`
3. Mio answers with the script's name and the conditions she read ("samples: diagenetic.constituent"), and the
   script opens in the script window as a new script named "Mio — …".
4. Read the header: it repeats the request and says what to change. The line `CRITERIA = [...]` holds the samples of
   the request as Explorer criteria; an empty list means every description.
5. Click **Run** (or F5). The output lists each file written. Tick **Button** for the script to appear in the Scripts
   menu of the ribbon and run with one click next time.

### Change a script

The values you usually change are at the top of the script's body: the folder, the format (`FMT = 'docx'`), the
classifications, the LAS curves, the file path. Change them and run again. Save the script in the project for the
team.

## Options

The tasks Mio can write (each one run on the example project by the tests):

| Task | Words that call it | What the script does |
|---|---|---|
| Report of every description | report | one PDF, Word, Excel or HTML per description, in a folder |
| Table of totals and classifications | classification, totals, Folk, Dickinson, table | one row per description, as CSV |
| Query result as a spreadsheet | spreadsheet, excel, csv | the table of an Explorer concept as XLSX or CSV |
| LAS file of every well | LAS, Petrel, curves | one LAS 2.0 per well with the curves chosen |
| HTML pages | html, page | one page per description and an index |
| Exchange files | xml, backup | one exchange file per description |
| PowerPoint presentation | presentation, powerpoint, slides | the presentation of a query |
| Ternary diagram | ternary, diagram | the samples on a diagram (Folk, McBride, Dickinson…) |
| Paragenetic sequence | paragenesis, sequence | the figure of each description |
| Count by well or facies | count, summary | how many samples per well (or facies) |
| Missing values | missing, without, empty | the descriptions without a value (porosity by default) |
| Lab flow | flow, segment, images | a flow over every picture, a table per sample |
| Porosity of the volumes | volume, micro-CT | the porosity of each segmented volume, as CSV |
| Pictures with annotations | photos, pictures, annotations | the pictures exported with their annotations |

Formats recognized in the request: PDF, Word, Excel, HTML, CSV. Classifications: Folk, McBride, Dickinson (QtFL and
QmFLt), Dunham, Embry & Klovan, Wright, Grabau, Bramkamp & Powers. Report language: "in English", "in Spanish", "in
Portuguese".

## How it works

Mio does not invent code. She picks the recipe by the words of the request, fills its parameters (format,
classification, file) and reads the samples asked for with the same rules as the plain-language search — that is why
the `CRITERIA` line says exactly what she understood. Every recipe is run by RockFace's automatic tests on the
ILLUSTRATIVE example project, so the script Mio writes works. When no recipe fits, she says which ones she can write.

For tasks the recipes do not cover, a larger assistant linked to RockFace through the [MCP server](mcp_server.md) can
write new scripts with the full reference of the programming interface.

## From a script

```python
s = prj.mio_script("Word report of each description with calcite", lang="en")
print(s.recipe, s.params, s.criteria)
print(s.code)                                   # the script, ready to run
exec(compile(s.code, "<mio>", "exec"), {"rf": rf, "project": prj})

for r in rf.script_recipes():                   # the tasks Mio can write
    print(r["key"], r["title"], r["params"])
s = prj.mio_script("table", recipe="table_classifications", classifications=["folk1980", "mcbride1963"])
```

## Limits and common problems

* "I have no script for that yet": the task has no recipe; ask for one of the tasks above or start from a similar
  script.
* A request without the word script is an ordinary question: "report of each description" asks; "script for the
  report of each description" writes the script.
* If the `CRITERIA` line does not hold the samples you meant, correct it by hand or ask again with the terms of the
  nomenclature ("with calcite", "of well ILLUSTRATIVE-1", "porosity above 15").
* A script writes files in the program's current folder; use full paths for another folder.

## Coverage

ROADMAP stage 0.30 (owner's request of 2026-11-13: Mio prepares Python scripts for repetitive tasks).
