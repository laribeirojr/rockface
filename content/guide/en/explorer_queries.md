# RockFace Explorer: queries, result tables and exports

## What it is for

RockFace Explorer asks questions of a whole collection: *which samples have barite?*, *which samples of well X have
U-Pb dating?*, *the grainstones with porosity above 15 % and permeability above 100 mD*. A query can use any concept
of a description — identification, texture, composition with its attributes, pore system, petrophysics, analyses,
classifications, totals, the diagenetic interpretation, images, spot analyses, mineral maps — and gives the
descriptions found, a table of any concept for them with their photos, and exports.

## Before you start

* A project with descriptions. To try Explorer: Help → **Open the ILLUSTRATIVE collection** (48 descriptions).
* A question can also be typed in plain language in the search box at the top (page [Mio: questions in plain language and the local language model](mio.md)).

## Step by step

### Opening Explorer

**Home → Collection → Explorer** (Ctrl+Shift+E), or `rockface explorer project.rockface`. The **Query** tab opens.

### A simple query

1. **Attributes**: an attribute of the identification (well, field, formation, zone, facies, rock type, depths,
   sample type, uses…).
2. **Values (descriptions)** lists its values with the number of descriptions that have each. Tick or select one or
   more.
3. For a number, give the **Numeric range**: **From** and **To** (either end may stay empty); "Found: … to …" shows
   the range in the collection.
4. **Add to the criteria**. The criterion appears in **Selection criteria (Del removes)**.
5. Add more criteria: a description must meet all of them. "N of M descriptions meet every criterion."

### An advanced query

1. **Advanced** shows the **Concepts**: Identification, Macroscopic and Microscopic texture, Primary composition,
   Diagenetic composition, Pores in the composition, Pore system, Petrophysics, Laboratory analyses,
   Classifications, Totals, Diagenetic interpretation, Images, Spot analyses, Mineral maps.
2. Choose a concept, then an attribute and its values or range, and **Add to the criteria**.
3. Within one concept, the criteria must be met by **the same row**: "diagenetic constituent = calcite" and "habit
   = poikilotopic" find the samples with poikilotopic calcite, not those with some calcite and something
   poikilotopic.

### The result table

1. **Descriptions found** lists them; pick some to see only them in the table and to export them (none picked:
   all).
2. **Table of**: the concept to show — for example Petrophysics, or Diagenetic composition with each line's share.
   **Every row** shows all the rows of the descriptions found, not only those that meet the criteria.
3. The **Photos** column gives the number of images of each thin section; select a row to see the photo,
   double-click it to open the description in RockFace Petro.
4. Click a column header to sort.

### Saving and exporting

* **Save query…** (give it a name), **Open query…**, **New query**; the **Saved queries** dialog also **Load**s and
  **Delete**s them. Queries are kept in the project.
* **Export**:
  * **Result table to Excel or CSV…** — numbers stay numbers;
  * **Descriptions found (HTML, Excel, PDF, Word)…** — through the report dialog (page [Reports](reports.md));
  * **Descriptions selected in the table to HTML…** or **to XML…** (an exchange file, page [Exporting and importing descriptions](exchange.md));
  * **Wells to LAS (Petrel)…** and **Presentation of the query (.pptx)…** (page [Groups, figures and presentations](groups_figures.md)).
* **Read again** reloads the descriptions after changes made in Petro.

## Options

| Option | What it changes |
|---|---|
| Advanced | Every concept instead of the identification only. |
| Every row | All rows of the descriptions found, not only the rows that meet the criteria. |
| Descriptions found (picked) | Limit the table and the exports to them. |

## How it works

Every description is read into *facts*, by concept: one row per composition line, per analysis, per spot, per map
phase… A description meets the query when, for each concept named, one and the same row meets all the criteria of
that concept, and every concept is met. Facts are read in about 8 ms per description and a query is answered in
about 1 ms on 480 descriptions. Templates are left out.

## From a script

```python
with rf.open("collection.rockface") as prj:
    print([d.name for d in prj.query(("diagenetic", "constituent", "barite"))])          # which samples have barite?
    print([d.name for d in prj.query(("spots", "system", "U-Pb"), well="ILLUSTRATIVE-A2")])   # dated, in well A2
    good = prj.query(("petrophysics", "porosity", 15, None), ("petrophysics", "permeability", 100, None))
    prj.save_query("Good reservoir", ("petrophysics", "porosity", 15, None))
    header, rows = prj.query_table("petrophysics", facies="Grainstone")
    prj.export_table("good.xlsx", "petrophysics", ("petrophysics", "porosity", 15, None))
```

## Limits and common problems

* "Tick or select at least one value." / "Type numbers for the range (either end may stay empty)."
* "The query has no criteria yet." / "Give the query a name."
* "Nothing to export: no description found or selected."

## Coverage

Q1 (simple query), Q2 (advanced query on every concept), Q3 (numeric ranges), Q4 (criteria list), Q5 (result
table), Q6 (saved queries), Q7 (export to Excel), Q8 (descriptions found to HTML, Excel and PDF), Q9 (selected
descriptions to HTML and XML), Q10 (export configuration), Q11 (photos column), L1 (search: "which samples have
barite?").
