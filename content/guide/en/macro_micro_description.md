# Macroscopic and microscopic description

## What it is for

The **Macroscopic** tab records what is seen in the hand sample or the core: structures, texture, colour and
fabric. The **Microscopic** tab records what is seen in the thin section: structures, the grain-size interval and
its modes, sorting, grain shape, fabric, the intergranular contacts and the packing. RockFace checks every value
against its scale, so the text and the numbers of a description never disagree.

## Before you start

A description open (page [Projects and descriptions](projects_descriptions.md)). The lists come from the knowledge base (page [Nomenclature, scales and references (the knowledge base)](nomenclature_knowledge_base.md)).

## Step by step

### Macroscopic

1. Open the **Macroscopic** tab.
2. **Structures** — up to three (**Structure 1–3**), each with its **Extent (%)** of the sample.
3. **Texture** — **Modal grain size** (Udden–Wentworth), **Crystal size** (Folk 1962, for crystalline rocks),
   **Sorting**, **Roundness** (Powers) and **Sphericity**.
4. **Colour** — the **Munsell code** (for example `5YR 6/4` or `N7`) and the **Colour name**.
5. **Fabric** — **Orientation** and **Support**.
6. **Notes**, then **Save** (Ctrl+S).

### Microscopic

1. Open the **Microscopic** tab.
2. **Structures** — up to three, with their extent.
3. **Grain size**
   * **Grain-size interval**: the **Finest** and the **Coarsest** class.
   * **Modes**: the **Main mode** and up to three more (**Second**, **Third**, **Fourth mode**), each as a class or a
     size in **mm**. When a size is typed, its class is filled in.
   * **Gravel (%)**, **Sand (%)** and **Mud (%)**, with their total shown beside them.
4. **Sorting and grain shape** — **Sorting** as a class or as **σI (φ)** (Folk & Ward 1957); **Roundness**, the
   **Roundness range** and the **Roundness modifiers**; **Sphericity**; **Crystal size**; **Orientation** and
   **Support**.
5. **Contacts and packing**
   * **Contacts, most abundant first (%)** — up to five contact types (point, long, concavo-convex, sutured,
     floating) with their percentage.
   * For Kahn's (1956) packing: count, along a traverse, the **All contacts on the traverse** of the grains crossed
     and how many are **Grain-to-grain contacts**; RockFace shows the **Packing proximity (Kahn)** and its class
     (loose, normal, tight). Measure the **Grain intercepts (mm)** and the **Traverse length (mm)** for the
     **Packing density (Kahn)**.
   * **Packing help…** opens the visual help of the packing classes (page [McBride, Bramkamp & Powers and the packing classes](classifications_packing.md)).
6. **Notes**, then **Save**.

## Options

| Field | Rule |
|---|---|
| Structures | At most three, no repeats; an extent needs a structure; 0–100 %. |
| Modes | At most four; the main mode first; each inside the grain-size interval. |
| Grain-size interval | The finest end first. |
| σI (φ), modal sizes | A number wins over the class: when they disagree, the class is updated, with a message. |
| Gravel + sand + mud | Should total 100 % (saved anyway, with a warning). |
| Contacts | At most five, no repeats, total at most 100 %. |
| Grain-to-grain contacts | Not more than all the contacts. |

## How it works

* Grain size follows the Udden–Wentworth scale (Wentworth 1922) with the φ of Krumbein (1934); sorting the
  inclusive graphic standard deviation of Folk & Ward (1957); roundness the classes of Powers (1953); crystal size
  Folk (1962).
* "Numbers win": a value in millimetres or φ is the measurement, and the class is derived from it.
* Packing proximity P = grain-to-grain contacts ÷ all contacts × 100; packing density = total grain intercept ÷
  traverse length × 100 (Kahn 1956). Classes: loose below 40, normal 40–55, tight above 55.

## From a script

```python
d = prj["TS-9"]
d.micro.sorting_phi = 0.62               # Folk & Ward σI; the class follows on save
d.micro.grain_contacts, d.micro.total_contacts = 38, 80
print(d.micro.packing_proximity, d.micro.packing_class)       # 47.5 normal
d.macro.colour_code = "5Y 7/2"
d.save()                                 # checked exactly as in the forms
```

## Limits and common problems

* "“…” is not in Munsell notation (for example 5YR 6/4 or N7)."
* "Grain-size interval: the first end is coarser than the second."
* "Secondary modes were given without the main mode." / "… is outside the interval given."
* "Modal grain size: 0.3 corresponds to medium sand; the number wins and the class was updated." — a message, not
  an error.

## Coverage

P11 (macroscopic description), P12 (microscopic structures and grain size), P13 (sorting and shape), P14 (contacts
and packing).
