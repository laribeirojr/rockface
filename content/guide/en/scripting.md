# Python scripts

## What it is for

Every RockFace program can be driven by Python scripts through one public API, `rockface.api`: to fill in many
descriptions at once, to write the tables and figures of a study, to check a whole collection, or to automate any
task of Atlas, Explorer, Lab and MC. Scripts are kept in the project, can be listed as buttons of the ribbon, and also
run without the interface, from a terminal or a Jupyter notebook.

## Before you start

* A project open, to keep scripts in it ("Open a project to keep scripts in it.").
* Basic Python. The **API…** button and `docs/SCRIPTING.md` of the source code list every call.

## Step by step

### The script window

1. **Tools → Python → Scripts** (Ctrl+Shift+P). The **Python scripts** window opens.
2. **Scripts of the project** on the left: **New**, **Delete**, **Import .py…**, **Export .py…**.
3. Give the script a **Name**. Tick **Button** to list it under the arrow of the **Scripts** button of the ribbon.
4. Write the script in the editor (line numbers, Python highlighting). In a script:
   * `rf` — the API; `project` — the open project; `current` — the description open in the interface;
   * `ui.message(text)` writes in the status bar; `ui.open(name)` opens a description after the script ends.
5. **Run** (F5 or Ctrl+Shift+J) runs the whole script; **Run selection** (Ctrl+J) runs the selected lines or the
   current line.
6. **Output** shows what the script prints and its errors, the line of an error marked in the editor ("The script
   stopped with an error at line …").
7. The **console** under the output evaluates one line in the same namespace as the last run — Enter runs it.
8. **Save in the project** (Ctrl+S).

If the open description has unsaved changes, RockFace asks to save it before the run, and reloads it after.

### A first script

```python
for d in project:
    t = d.totals()
    print(d.name, round(t["porosity"], 1), d.classify("folk1980", label=True))
rows = project.table(totals=["volume", "qt", "feldspar", "igv"], classifications=["folk1980"])
project.to_csv("summary.csv", rows)
ui.message(f"{len(rows)} descriptions written")
```

### Without the interface

```
rockface script my_script.py --project study.rockface -- arg1 arg2
```

In Jupyter or any Python program:

```python
import rockface.api as rf
with rf.open("study.rockface") as prj:
    print(len(prj))
```

`rockface notebook study.rockface` writes a notebook that opens the project (page [MC → More: cups, distance map, folder watch, reconstruction, upscaling and two-phase flow](mc_more_tools.md)).

### The example scripts

The ILLUSTRATIVE example project holds the example scripts: a summary table, a provenance figure, a custom total, a
check of every description, the diagenesis summary, reports in batch, the Atlas overview, annotated figures, mineral
maps, spot analyses, Explorer queries and figures, dating and evolution, and the Lab and MC examples.

## Options

| Option | What it does |
|---|---|
| Button | Lists the script under the Scripts button of the ribbon (Tools tab). |
| Run selection | Runs only the selected lines, or the current line. |

## How it works

* **Same checks.** A script cannot store what the forms would refuse: `d.save()` validates exactly as the forms and
  raises `rf.ScriptError` with the messages, writing nothing.
* **Audit.** Writes made by a script are recorded under the user's name followed by ` [script]`.
* **Scripts written by others.** A script kept in a project and written by someone else runs only after a
  confirmation ("A script can read and change the project and the files of this computer. Run it?").
* **Stability.** `rf.API_VERSION` follows semantic versioning: within 1.x names are only added.
* **Licence.** Scripts that use the API are the user's own work: writing, running and sharing them is allowed.

## From a script

This page is about scripts; the "From a script" section of every other page of this guide shows the calls for that
function.

## Limits and common problems

* "The script stopped with an error at line …": the traceback in the output shows only the script's own lines.
* A script runs with your rights on the computer: run only scripts you trust.
* A long script blocks the window while it runs; for long calculations of MC use jobs (page [Jobs: batch and remote computing](jobs.md)).

## Coverage

O1 (Python scripting in every RockFace application).
