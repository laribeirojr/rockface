# Getting started

## What it is for

RockFace Suite describes, images, queries and measures sedimentary rocks, from the thin section to the database.
It is five programs that open the same project and the same thin section, so what one writes the others read at
once:

| Program | For | Opens with |
|---|---|---|
| **RockFace Petro** | the description of a thin section: identification, composition, point count, classifications, diagenesis, reports | `rockface-petro` |
| **RockFace Atlas** | whole-slide images and detail photos at their place on the section, annotations, mineral maps, spot analyses | Home → **Atlas** (Ctrl+Shift+A) or `rockface-atlas` |
| **RockFace Explorer** | queries over a collection, the dashboard, groups, figures, presentations, LAS, dating, paragenetic evolution | Home → **Explorer** (Ctrl+Shift+E) or `rockface-explorer` |
| **RockFace Lab** | image analysis of a section: crop, filters, registration, segmentation, objects, measurements | Home → **Lab** (Ctrl+Shift+L) or `rockface-lab` |
| **RockFace MC** | micro-CT volumes, whole cores and image logs of a well | Home → **MC** (Ctrl+Shift+M) or `rockface-mc` |

## Before you start

* RockFace installed on your computer with the installer the RockFace team gave you (public downloads start with version 1.0). RockFace AI and
  the local language model are installed apart (pages [RockFace AI: installation, device and the model hub](ai_setup_hub.md) and [Mio: questions in plain language and the local language model](mio.md)).
* Nothing else: the first project can be the ILLUSTRATIVE example.

## Step by step

### The start page

1. Open **RockFace Petro**. The start page shows **New project**, **Open project…**, **Connect to server** and
   **Open the illustrative example**, the **Recent** projects, and the five programs of **The RockFace Suite**.
2. Choose **Open the illustrative example** to look around first. It writes a small project with invented samples
   (every name is marked ILLUSTRATIVE) and opens it.
3. Or drag a `.rockface` file onto the window to open it.

### The window

* The **ribbon** at the top has four tabs:
  * **Home** — the groups **Project**, **Server**, **Description**, **Images** (Atlas, Lab, MC), **Collection**
    (Explorer), **Reports and exchange** and **Form**;
  * **View** — **Dark theme** and the **Language**;
  * **Tools** — the **Knowledge base** (Nomenclature, Scales, References, Knowledge graph), **Python** (Scripts) and
    **Mio**;
  * **Help** — **Help contents** (F1), **About RockFace**, **Licence**, **Support…**, **Plug-ins and updates…**, the
    knowledge graph and the two ILLUSTRATIVE projects.
* The **Project** panel on the left lists the wells, their thin sections and the descriptions of each section.
* The **description tabs** in the middle: Identification, Macroscopic, Microscopic, Composition, Point count, Pore
  system, Classification, Diagenesis, Analyses and Requests.
* The **status bar** at the bottom gives the result of every action; on the right, the number of descriptions and
  the project's name.

### Language and theme

1. **View → Language**: English, Español or Português. Every window changes at once, and the choice is kept for the
   next start.
2. **View → Dark theme** switches between the light and the dark theme.

The project does not depend on the language: a project written in Portuguese opens, and reports, in English or
Spanish. Only the labels change; the stored values are the same codes.

### Help inside the program

* **Help → Help contents** (F1) opens this guide in the interface language, with **Contents**, **Index** and
  **Search**.
* **Mio**, RockFace's assistant, answers "how do I…" questions with the page of this guide that explains it (page
  [Mio: questions in plain language and the local language model](mio.md)).
* **Help → Support…** gathers the versions of RockFace and its libraries to send with a question (no file names and
  no project content).

### The ILLUSTRATIVE collection

**Help → Open the ILLUSTRATIVE collection** writes a project of 48 invented descriptions from four wells, with
images, analyses, U-Pb spots and a stratigraphic table. It is meant for trying RockFace Explorer.

## Options

| Where | What it changes |
|---|---|
| View → Language | The interface language (English, Spanish, Portuguese) of every program. |
| View → Dark theme | Light or dark windows. Diagrams and figures are always drawn on paper colours. |
| Help → Plug-ins and updates… | Plug-ins installed and the check for a newer RockFace (page [Help, support, plug-ins and updates](help_plugins.md)). |

## How it works

A project is one `.rockface` file (an SQLite database) or a database on a PostgreSQL server shared by a team (page
[Working together on a server](server.md)). Every image, counted point and spot analysis is stored in the coordinate frame of
its thin section (millimetres), never only in image pixels, so the five programs agree on where things are. Files
written by an older version are upgraded when opened; a file written by a newer version is refused with a message.

## From a script

```python
import rockface.api as rf
with rf.example("demo.rockface") as prj:           # the ILLUSTRATIVE example project
    print(len(prj), [d.name for d in prj])
```

From a terminal:

```
rockface example demo.rockface        # writes the ILLUSTRATIVE example project
rockface collection coll.rockface     # writes the ILLUSTRATIVE collection (48 descriptions)
rockface petro demo.rockface          # opens it in RockFace Petro (also atlas, explorer, lab, mc)
```

## Limits and common problems

* "This project was written by a newer RockFace": update RockFace to open it.
* "… is not a RockFace project": the file is not a RockFace database (or is damaged).
* The preferences (language, theme, recent projects) belong to your user on this computer, not to the project.

## Coverage

P1 (main window), P3 (status bar), P10 (interface in English, Portuguese and Spanish), P40 (help contents), O1
(scripting).
