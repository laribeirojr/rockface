# Projects and descriptions

## What it is for

A **project** holds a collection: its wells and outcrops, samples, thin sections, descriptions, images, analyses,
volumes and logs. A **description** is the petrographer's record of one thin section. This page covers creating and
opening projects, and creating, loading, saving, copying, deleting and using descriptions as templates.

## Before you start

RockFace Petro open (page [Getting started](getting_started.md)).

## Step by step

### A project

1. **Home → Project → New project** (Ctrl+Shift+N): choose a folder and a name. The file ends in `.rockface`.
2. **Open project…** (Ctrl+O) opens an existing one; the **Recent** list of the start page keeps the last ones.
3. **Save project as…** writes a copy of the whole project under a new name and goes on in the copy.
4. **Close project** returns to the start page.

A project on a team server is opened with **Connect to server** instead (page [Working together on a server](server.md)).

### A new description

1. **Home → Description → New description** (Ctrl+N).
2. Type the **Name of the new description** and choose its **Thin section**:
   * a new thin section, or
   * an existing one, when several petrographers (or several studies) describe the same section. The identification
     then starts from what is known of that section: well, depths, sample, numbers.
3. The **Identification** tab opens. Fill it in (page [Identification of a sample](identification.md)) and the other tabs as needed.
4. **Save** (Ctrl+S). Every tab is checked together: any error blocks the whole save, and the first tab with an
   error is shown, with the field marked.

In the **Project** panel, a double click on a thin section also starts a new description on it.

### Loading, saving and copying

* **Load description…** (Ctrl+L) lists the descriptions with their well, depth and thin section; type in **Filter…**
  to narrow the list. A double click in the **Project** panel does the same.
* **Save** (Ctrl+S) writes the description open. If you load another one or close the project with changes not
  saved, RockFace asks first.
* **Save as…** (Ctrl+Shift+S) writes a copy under a new name (**Name of the copy**). The name of a saved description
  cannot be changed: use Save as and delete the old one.
* **Delete** removes the description open, with its parts and point count, after a confirmation. It cannot be
  undone. When it was the last description of a thin section, the section goes too, unless it has Atlas images or
  spot analyses, or its sample has analyses or requests: those are never thrown away. The well always stays.
* **Home → Form → Clear** empties the tab shown, to start it again.

### Templates

A template is a description kept as a starting point: a usual list of constituents, the petrographer and
institution, a standard set of uses.

1. Open a description that is a good start, then **Save as…**.
2. Tick **Mark the copy as a template**.
3. Templates appear with the label *template* in the panel and are left out of the count of descriptions and of
   the queries of Explorer; an export includes them only when asked.
4. To use one: load it, **Save as…** under the new sample's name (without the tick), then change what differs.

## Options

| Field | What it changes |
|---|---|
| Thin section (New description) | New section, or a section already in the project: several descriptions of one section share its images, point count frame and analyses. |
| Mark the copy as a template | The copy is a template: kept apart from the collection. |

## How it works

The data model follows the rock: basin → field → well (or outcrop) → core → sample → thin section → description,
with the images, analyses, volumes and logs attached to the sample or the thin section. Every change is written in
the project's audit table (who, when, what). A description is saved as one transaction: identification and all its
parts, or nothing.

## From a script

```python
import rockface.api as rf
with rf.create("study.rockface") as prj:                  # a new, empty project
    d = prj.new("TS-9", well_name="ILLUSTRATIVE W-1", top_depth=2501.3, thin_section_no="9")
    prj.copy("TS-9", "TS-9 template", template=True)     # a template
    print([x.name for x in prj], len(prj.descriptions(templates=True)))
with rf.open("study.rockface") as prj:
    prj.delete("TS-9")
```

## Limits and common problems

* "A description named … already exists in this project": names are unique in a project.
* "The name of a saved description cannot be changed; use Save as."
* "Not saved: …" in the status bar names the field to correct; the tab with the error is shown.
* On a server, descriptions written by someone else open read-only for a petrographer (page [Working together on a server](server.md)).

## Coverage

P1 (main window), P2 (New, Load, Save, Save as, templates, Delete), P6 (thin section chosen for a description), P9
(Load description).
