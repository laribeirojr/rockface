# Composition

## What it is for

The **Composition** tab is the table of what the rock is made of: primary constituents, diagenetic constituents
and pore types, each with its attributes (location, habit, modifier, paragenetic relation) and its amount — counted
points, a manual percentage or a visual estimate. Totals, classifications, the diagenetic interpretation, reports
and queries are all worked out from it.

## Before you start

A description open. The constituents and attributes come from the knowledge base (page [Nomenclature, scales and references (the knowledge base)](nomenclature_knowledge_base.md)).

## Step by step

### Adding lines

1. Open the **Composition** tab.
2. **Add…** (Ins). In the **Composition line** dialog, choose the **Constituent** from the grouped lists (primary
   constituents, diagenetic constituents, pores); type in the filter to find it in any language.
3. Give the attributes its kind allows:
   * primary — **Location**, **Modifier**;
   * diagenetic — **Habit**, **Location**, **Modifier**, **Relation** (paragenetic), **Related constituent** and
     **Its location**;
   * pore — **Location**, **Modifier**, **Relation**, **Related constituent**.
4. Give the amount, one of:
   * **Points** — counted points;
   * **Manual %** — a percentage measured elsewhere;
   * **Nominal amount** — a visual estimate on the comparison-chart steps (trace, 1, 2, 3, 5, 7, 10, 15, 20, 25,
     30, 40, 50 %).
5. **Observation** — a note about this line. **OK**.

The same constituent can appear on several lines with different attributes (for example calcite as a poikilotopic
intergranular cement and as a replacement of feldspar).

### Counting by clicks and keys

* A **double click** on the Points cell of a line adds a point; **Alt + double click** takes one away.
* **Keys…** gives lines to the keys 1–0 and Ctrl+1–0 (twenty keys): pressing a key adds a point to its line.
* The line under the table shows the points and the shares: "… points · primary … % · diagenetic … % · pores … %
  · total … %".
* **Clear points** sets every count to zero and keeps the lines.

For counting on the image of the section, with each point's position kept, use the **Point count** tab (page
[Point counting](point_counting.md)).

### Editing the table

| Button | Key | Does |
|---|---|---|
| Attributes… | Enter | Edits the selected line. F2 edits a single cell. |
| Delete | Del | Deletes the selected lines. |
| Copy, Paste | Ctrl+C, Ctrl+V | Copies lines, also into another description. |
| Up, Down | Ctrl+Up, Ctrl+Down | Moves the selected lines. |
| Group, Ungroup | Ctrl+G, Ctrl+U | Gathers lines under a named group, or undoes it; **Grouped view** shows the groups. |
| Colour of the selected lines… | | A colour for the lines (also used in the point count and the reports). |
| Undo, Redo | Ctrl+Z, Ctrl+Y | Every change of the table. |
| Template… | | Loads the composition of a template: replace the lines, or add the missing ones. |
| Preferences… | | **Double clicks per point** and **Remind me to save every** N points. |

**Save** (Ctrl+S) when done; the reminder appears after the number of points set in the preferences.

## Options

| Option | What it changes |
|---|---|
| Double clicks per point | How many double clicks make one point (at least 1). |
| Remind me to save every | A reminder in the status bar after N points (0 = never). |
| Grouped view | Lines shown under their groups, or as one list. |

## How it works

* Lines with a manual % or a nominal amount keep that value ("fixed lines"); the counted lines share what is left,
  100 − fixed, in proportion to their points. Without any counted point the percentages are the fixed values. A line
  with points and a % counts by its points (with a warning).
* The nominal steps follow the comparison charts of Terry & Chilingar (1955); a trace counts as 0 %.
* The attributes a constituent may take come from the knowledge base ("Applies to"), so a habit is never given to a
  primary grain.

## From a script

```python
d = prj["TS-9"]
d.add_line("quartz_mono", points=112, location="framework")
d.add_line("calcite_dia", points=24, habit="poikilotopic", location="ig_pore_filling")
d.add_line("kaolinite", nominal="3", habit="booklet", location="intragranular_replacive",
           relation="replaces", related="k_feldspar")
for line in d.lines():
    print(line["constituent"], round(line["share"], 2))      # quartz_mono 79.88, calcite_dia 17.12, kaolinite 3.0
d.save()
```

## Limits and common problems

* "… does not apply to …": an attribute that the constituent's kind does not take.
* "… appears twice with the same attributes (see line …)": merge the two lines.
* "The manual and nominal percentages add up to … %, more than 100 %."
* "…: no location given." — a warning for diagenetic constituents.
* "A location of the related constituent was given without the constituent."

## Coverage

P18 (composition table), P19 (attributes), P20 (points, manual %, nominal amount, observation), P21 (groups and
colours), P22 (copy, paste, move, undo), P23 (keys), P24 (clear points, template, preferences, save reminder).
