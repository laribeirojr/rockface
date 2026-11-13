# Atlas annotations and the search by concept

## What it is for

Annotations mark what an image shows — an arrow on a kaolinite booklet, a box around a dissolved feldspar, a
contour of a pore, a label — and tie each mark to the nomenclature as a **feature**: a constituent with its habit,
location, modifier and relation, as in the composition. RockFace writes the **automatic caption** of the image from
them, exports figures with or without the marks, and finds images by what they show: rock type → concept →
attribute → value.

## Before you start

An image open in RockFace Atlas (page [RockFace Atlas: whole slides, detail photos and the image library](atlas_viewer.md)).

## Step by step

### Drawing

1. Open the **Annotations** tab of the panel **Image, annotations and map**.
2. Choose a tool:
   * **Arrow** — click where it starts, then where it points;
   * **Box** — click two opposite corners; **Ellipse** — two corners of the box around it;
   * **Contour** — click the points; double-click, Enter or the first point closes it;
   * **Label** — click where the text goes, then type it.
3. **Select** — click an annotation to choose it, drag it to move it, Delete removes it.
4. **Colour**, **Line** width and **Text** size; **Apply look** gives them to the selected annotation.

### Saying what it shows

1. Select an annotation and press **Feature…**. In **What the annotation shows**, choose the constituent and its
   habit, location, modifier and relation (the same lists as the composition).
2. **Text…** changes the text of a label or adds a text to any annotation.
3. Annotations that say something are lettered A, B, C… in the order they were drawn; the letters are drawn on the
   image and used by the caption.

### The note and the caption

1. **Note of the image** — a text about the whole image, with **Add a feature…** for what the whole image shows;
   **Save the note**.
2. **Automatic caption** — the name, kind and light, objective, sample, depth and thin section, the position on the
   section, the note, "(A) …; (B) …" and the scale. **Copy** it, or **Use as the caption** of the image.

### Exporting figures

1. **Export images…**
2. **Images**: **The image open**, **Every image of its thin section** or **The images listed in the library**.
3. **Annotations**: **With annotations**, **Without annotations** or **Both (two files each)**.
4. **Longer side at most** (pixels) and **A caption file (.txt) next to each image**.
5. Choose the folder.

### Finding images by concept

1. In the **Image library**, open **By concept**.
2. **Look in**: **the annotations of the images**, **the compositions of the descriptions**, or **annotations and
   compositions**.
3. Open the tree **Rock type › concept › attribute › value** — for example *Subarkose › Kaolinite › Habit ›
   Booklet* — and select a node: the library shows the images found, with **Found in: …** (the letters, the note or
   the description). **Show every image** clears the search.

## Options

| Option | What it changes |
|---|---|
| Colour, Line, Text | Look of the annotation (also in exported figures). |
| Feature | What the annotation shows, with the nomenclature of RockFace. |
| Look in | Search the annotations, the compositions of the thin sections, or both. |

## How it works

Annotations are stored in the full-resolution pixels of their image, so they stay in place at any zoom and in any
export. The features use the codes of the knowledge base, so a caption is written in the language of the interface
(or of the export) and the search finds an image whatever language it was annotated in. The rock type of an image is
the classification of the descriptions of its thin section.

## From a script

```python
img = prj.image("Field B — kaolinite booklets")
img.annotate("rect", [[820, 410], [1260, 760]], features=[rf.Feature("kaolinite", habit="booklet")])
img.annotate("label", [[1300, 420]], text="Kln")
img.note("Kaolinite booklets fill the pores.", [{"constituent": "kaolinite"}])
print(img.caption_auto("en"))
for found, reasons in prj.search_images(concept="kaolinite", attribute="habit", value="booklet"):
    found.export(f"{found.name}.png", max_side=3000, annotated=True, caption_file=True)
prj.export_images("figures", annotated=True, caption_file=True, lang="pt")
```

## Limits and common problems

* A feature with a code unknown to the knowledge base is refused.
* Only one note per image: a new note replaces it.
* "Delete this annotation?" — deleting cannot be undone; the letters of the others follow.

## Coverage

R2 (hierarchical search: rock type → concept → attribute → value), R3 (image editor: arrows, contours, letters,
notes; features with the nomenclature).
