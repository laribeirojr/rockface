# Reports

## What it is for

A **report** writes one or many descriptions as a document: PDF to print or archive, Word (DOCX) or Excel (XLSX) to
edit, or HTML pages to read in a browser — in English, Spanish or Portuguese, whatever the language of the
interface. It holds the sections you choose: identification, description, composition, totals, classifications with
their ternary diagrams, diagenesis with the paragenetic chart, analyses, requests, the images of the thin section
and its spot analyses.

## Before you start

The descriptions saved: unsaved changes are not in the report.

## Step by step

1. **Home → Reports and exchange → Report…** (Ctrl+P).
2. **Descriptions**: tick those to write (**All**, **None**). The description open is ticked.
3. **Format**: PDF, Word, Excel or HTML.
4. **Language of the report**: English, Español or Português.
5. **Sections**: Identification, Macroscopic, Microscopic, Pore system, Composition, Totals, Classifications,
   Diagenesis, Analyses, Requests, Images of the thin section, Spot analyses.
6. Layout:
   * **Width of the pictures (mm)** and **Width of the ternary diagrams (mm)**;
   * **Figures**: **In their sections** or **All at the end**;
   * **Also the original composition (before diagenesis)**.
7. For HTML, tick **HTML: one page per description, with an index page** and choose the **Folder for the HTML
   pages**: each description gets its page, and `index.html` links them.
8. **Open the file when written**, then **Write report…** and choose where to save it.

"Word, Excel and HTML files can be edited after export."

## Options

| Option | What it changes |
|---|---|
| Format | PDF (A4), DOCX, XLSX (a sheet listing the descriptions and one sheet per description) or HTML. |
| Language of the report | Independent of the interface language. |
| Sections | Only the sections ticked are written. |
| Width of the pictures / ternary diagrams | Size of the figures in the document, in mm. |
| Figures | Inside their sections, or all gathered at the end. |
| Original composition | Adds the composition before diagenesis and its totals and classifications. |

## How it works

The report is built from the same records the forms show (codes translated into the language of the report);
numbers are written with the decimal separator of that language. Ternary diagrams and the paragenetic chart are
drawn as in the program. Explorer writes reports of the descriptions found by a query through the same dialog (page
[RockFace Explorer: queries, result tables and exports](explorer_queries.md)).

## From a script

```python
with rf.open("study.rockface") as prj:
    prj["TS-9"].report("TS-9.pdf", lang="pt")
    prj.report("well-1.docx", names=["TS-9", "TS-10"], lang="en",
               sections=["identification", "composition", "classification"], figure_mm=120, figures="end")
    prj.html_pages("site", lang="es")                  # one page per description and index.html
```

## Limits and common problems

* "No description chosen."
* Word and Excel need the `reports` extra (python-docx, openpyxl), installed with `.[all]`.
* Very large whole-slide images are written reduced to the picture width chosen.

## Coverage

P10 (reports in English, Portuguese and Spanish), P34 (reports: PDF, Excel, HTML, Word; language; configuration),
P36 (HTML generator for batches).
