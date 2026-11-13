# Colour of the selected lines (composition)

## What it is for

Counterledge lets the petrographer colour lines of the composition table to find them at a glance while counting.
In RockFace the selected lines take a colour through their group.

## Step by step

1. **Petro → Composition**: select one or more lines.
2. **Colour of the selected lines…** and choose the colour.

## How it works

The lines share a group (the one they already share, or a new one) and the group's colour paints them; ungrouping
removes it. The colour is saved with the composition.

## From a script

```python
d = prj["ILL-TS-001"]; d.composition.groups   # {"g1": {"name": …, "colour": "#123456"}}
```

## Coverage

Counterledge C2 (Configure Selected Row Color).
