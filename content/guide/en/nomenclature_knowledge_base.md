# Nomenclature, scales and references (the knowledge base)

## What it is for

Every list of RockFace — constituents, habits, locations, modifiers, paragenetic relations, structures, contacts,
pore types — comes from its **knowledge base**: 257 built-in terms in English, Spanish and Portuguese, each with its
published source. The knowledge-base editor shows them, and lets a project add its own terms, hide terms it does
not use and put the lists in its preferred order. It also shows the numeric **scales** (grain size, sorting,
roundness, crystal size, pore size) and the **references** cited.

## Before you start

* A project open, to change anything. Without a project the built-in nomenclature is shown read-only.
* On a server, changing the knowledge base needs the manager level.

## Step by step

### Looking up a term

1. **Tools → Knowledge base → Nomenclature** (Ctrl+K).
2. Choose the **Category** (constituent, group, habit, location, modifier, relation, structure, contact…).
3. Type in **Filter (any language)…**: "quartzo", "cuarzo" and "quartz" find the same term; accents are ignored.
4. Select a term to see its code, its labels in the three languages, its group, kind, rock family, what it applies
   to, and its **Sources**.

### Adding a term of the project

1. Choose the category, then **Add term…**.
2. Fill in **Code** (lower case, letters, digits and `_`; it never changes afterwards), the labels in **English**
   (required), **Spanish** and **Portuguese** (a warning when missing), and, as the category asks, **Group** and
   **Rock family** (constituents), **Kind** (groups), **Applies to** (locations and modifiers) and **Inverse
   relation** (relations).
3. In **Sources**, give the full reference of the source (author, year, title, publication). Every built-in term
   carries its literature source; a project term without one is saved with a warning.
4. **Apply**, then **Save in the project**.

### Hiding, ordering, undoing

* **Hide** takes a built-in term out of the lists of this project (descriptions that use it keep it). Tick **Show
  hidden terms** to see them, and **Show** to bring one back.
* **Up** and **Down** change the order in which the terms appear in the lists of the forms.
* **Remove** deletes a term of the project (built-in terms can only be hidden).
* **Undo** cancels the last change; **Restore defaults** brings back the built-in order and every hidden term (the
  project's own terms are kept).
* **Save in the project** writes the changes, with a line in the audit; **Close** asks first if something is not
  saved.

### Scales

1. **Tools → Knowledge base → Scales**.
2. Choose the **Scale**: grain size (Udden–Wentworth, with φ of Krumbein), sorting (Folk & Ward σI), roundness
   (Powers), crystal size (Folk 1962) or pore size. The table gives each class with **From**, **To (exclusive)** and
   φ.
3. **Check a value against a class**: type a **Value**, choose a **Class**; RockFace answers "Consistent" or "Not
   consistent: … is …, not …". The description forms use the same check (page [Macroscopic and microscopic description](macro_micro_description.md)).

### References

**Tools → Knowledge base → References** lists every reference with its **Key**, the full **Reference** and **Cited
by** (how many terms, rules, totals and classifications cite it).

## Options

| Field | What it is |
|---|---|
| Code | The value stored in the project; never translated, never changed. |
| Group, Kind | Where the term goes in the composition lists (e.g. diagenetic carbonate). |
| Rock family | Siliciclastic, carbonate or both: the lists of a description show the family that applies. |
| Applies to | For locations and modifiers: the kinds of constituent they can describe. |
| Inverse relation | For paragenetic relations: the relation read the other way (e.g. *replaces* ↔ *replaced by*). |

## How it works

The built-in nomenclature is RockFace's own, built from the published literature;
none of it comes from the ontology of a commercial program. The project keeps only its differences — its own terms,
hidden terms and order — so a newer RockFace with more built-in terms still opens it. The full list, with the
sources, is `docs/NOMENCLATURE.md` of the source code.

## From a script

```python
with rf.open("study.rockface") as prj:
    for t in prj.search("caulinita"):                 # any language, accents ignored
        print(t.category, t.code, t.labels["en"], t.citations())
    print(prj.term("constituent", "kaolinite").labels)
from rockface.core import scales
print(scales.classify("grain_size", 0.3))            # 'medium_sand'
```

## Limits and common problems

* "Open a project to add, hide or reorder terms; the built-in nomenclature is shown."
* A code already used, or a code with capitals or spaces, is refused; so is a constituent without its group and
  rock family.
* Hiding a term does not change the descriptions that already use it.

## Coverage

P39 (knowledge-base tools: attribute editors with and without consistency intervals, item order, add, update,
remove, undo).
