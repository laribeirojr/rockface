# Pore system

## What it is for

The **Pore system** tab records the visual porosity of the thin section and the pore types that make it up, each
with its share, size and modifier. The pore types are those of Choquette & Pray (1970) for carbonates and of the
sandstone pore classifications, from the knowledge base.

## Before you start

A description open. Blue-resin porosity measured on an image (RockFace Lab) or counted points (Point count tab)
can be used as the visual porosity.

## Step by step

1. Open the **Pore system** tab.
2. **Porosity** — type the **Visual porosity (%)**. The **Sum of the types** is shown beside it.
3. **Pore types** — up to eight rows. For each:
   * **Type** — the fabric-selective pores of Choquette & Pray (interparticle, intraparticle, intercrystalline,
     moldic, fenestral, shelter, growth-framework), the pores not fabric-selective (fracture, channel, vug, cavern)
     and those that may be either (breccia, boring, burrow, shrinkage), and the sandstone pores (primary and
     secondary intergranular, intragranular dissolution, oversized, microporosity);
   * **%** — its share of the rock volume;
   * **mm** — a typical size, or the **Pore size** class (the class follows a typed size);
   * **Modifier** — a modifier of the knowledge base that applies to pores.
4. **Notes**, then **Save** (Ctrl+S).

## Options

| Field | Rule |
|---|---|
| Visual porosity | 0–100 %. |
| Pore types | At most eight, no repeats; each 0–100 %. |
| Sum of the types | Compared with the visual porosity: more or less than it gives a warning. |

## How it works

The pore types and their modifiers are RockFace terms from the published literature (Choquette & Pray 1970 for
carbonates; sandstone pore types after Schmidt & McDonald 1979 and Pettijohn et al. 1987). The pore-size classes
are Choquette & Pray's micropores (< 1/16 mm), small and large mesopores (to 4 mm) and small and large megapores
(to 256 mm). Pore types counted as points in the composition (kind *pore*) are a
separate record: the Pore system is the petrographer's synthesis.

## From a script

```python
from rockface.core import texture as tx
d = prj["TS-9"]
d.pores.total_porosity = 18.0
d.pores.pores = [tx.Pore("interparticle", 12.0, size_mm=0.15), tx.Pore("moldic", 6.0)]
d.save()
```

## Limits and common problems

* "The pore types add up to … %, more than the visual porosity (… %)." — a warning: check the shares.
* "… must be between 0 and 100 %."
* An unknown pore type or modifier code (from a script or an old file) is refused with "Unknown value …".

## Coverage

P17 (pore-system description).
