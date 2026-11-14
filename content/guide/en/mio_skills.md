# Mio's skills

## What it is for

A **skill** is a small recipe that Mio runs whenever a question asks for it: several of her tools one after the
other, with the values taken from the question. "Well summary ILLUSTRATIVE-B" counts the samples of the well, lists
its facies, gives porosity and permeability and says which descriptions lack porosity — in one answer. RockFace ships
eight skills, active from the start, to use and to copy; you write your own and keep them for yourself or in the
project, for the whole team.

## Before you start

* A project open. Writing a skill needs no programming: it is a short JSON text edited in the **Skills** dialog.

## Step by step

### Using a skill

1. In the Mio panel type one of its phrases ("resumo do poço ILLUSTRATIVE-B", "data gaps", "melhores
   reservatórios", "how do I …"), or its name after a slash: `/well-summary ILLUSTRATIVE-B`.
2. If the skill needs a value the question did not give (the well, a sample), Mio asks for it.

The skills shipped with RockFace:

| Skill | Called by (examples) | What it does |
|---|---|---|
| `well-summary` | well summary · resumo do poço · resumen del pozo | count, facies, porosity, permeability, missing porosity of a well |
| `formation-summary` | formation summary · resumo da formação | count, wells, facies, porosity, cement of a formation |
| `reservoir-quality` | reservoir quality · melhores reservatórios | samples with porosity ≥ 15 % and permeability ≥ 100 mD, and their wells |
| `cement-overview` | cement overview · cimentação | total and carbonate cement; samples with calcite, dolomite, quartz overgrowths |
| `dated-samples` | dated samples · amostras datadas | samples with dating spots and their wells |
| `data-gaps` | data gaps · lacunas · control de calidad | descriptions without depth, porosity or permeability |
| `sample-report` | sample report · ficha da amostra | the main facts of a description and the suggestions of its maps |
| `how-to` | how do I · como faço · cómo hago | the pages of this guide that explain a task |

### Writing a skill

1. Mio panel → **Skills…**. The list shows every skill with where it comes from: *RockFace*, *mine* (your folder),
   *project*.
2. Select one to see it, or click **New** for a template.
3. Edit the JSON (fields below) and click **Save for me** (your folder) or **Save in the project** (everyone who
   opens the project). The skill is checked before it is saved; problems are listed under the editor.
4. **Active** switches a skill off without deleting it. A skill saved with the name of another replaces it (a project
   skill named `how-to` replaces RockFace's); **Delete** brings the other back.

## Options

```json
{
 "name": "kaolinite-by-well",
 "title": {"en": "Kaolinite by well", "pt": "Caulinita por poço", "es": "Caolinita por pozo"},
 "description": {"en": "How many samples of a well have kaolinite, and their porosity.", "pt": "…", "es": "…"},
 "triggers": ["kaolinite by well", "caulinita por poço", "caolinita por pozo"],
 "inputs": {"well": {"field": "well"}},
 "steps": [
  {"tool": "count", "question": "samples of well {well} with kaolinite"},
  {"tool": "stats", "number": "petrophysics.porosity", "question": "samples of well {well} with kaolinite"}
 ],
 "active": true
}
```

| Field | What it is |
|---|---|
| `name` | lower case, digits and hyphens; also the `/name` that calls the skill |
| `title`, `description` | shown in the list, in English, Portuguese and Spanish |
| `triggers` | phrases that call the skill (accents and capitals do not matter) |
| `inputs` | values read from the question: `{"field": "well"}` (any identification field: well, formation, facies, field, basin, zone…) or `{"field": "sample"}` (a description's name); `{question}` is always available |
| `steps` | the tools, in order: `search`, `count` (`question`), `stats` (`number`, `question`; 0.31: `statistic` and `group`, e.g. `facies`), `values` (`field`, `question`), `missing` (`number`, `question`), `describe` (`sample`), `suggest` (`sample`), `guide` (`question`), `ages` (`question`, 0.31) |

`number` is `concept.attribute` as in the Explorer: `petrophysics.porosity`, `petrophysics.permeability`,
`petrophysics.grain_density`, `identification.top_depth`, `totals.cement`, `totals.carbonate_cement`…

## How it works

Skills are data, never code: a skill can only call Mio's tools, and every tool only reads the project. Skills come
from three places, read in this order (a later one with the same name replaces an earlier one): RockFace's folder
`rockface/mio_skills`, your folder (`~/.rockface/mio/skills`, or the setting `mio.skills`, or `ROCKFACE_MIO_SKILLS`)
and the project (kept in the project with an audit line, so a server project shares its skills with the team).

## From a script

```python
for s in prj.mio_skills():
    print(s.name, s.source, s.triggers)
prj.save_mio_skill({"name": "barite-count", "triggers": ["barite please"],
                    "steps": [{"tool": "count", "question": "samples with barite"}]})
print(prj.mio(lang="en").ask("/barite-count").text)
prj.delete_mio_skill("barite-count")
```

## Limits and common problems

* "The skill cannot be used: …": the check lists what to fix (a tool that does not exist, an input used but not
  declared, a `stats` without a number).
* A trigger that is also a normal question ("samples with calcite") makes every such question run the skill — choose
  phrases that say what the skill is.
* Skills that write to the project (apply a suggestion, run a script) are not allowed in this version: Mio proposes,
  the user decides.

## Coverage

The assistant that calls the program's tools of the ROADMAP stage 0.27; the owner's request of 2026-11-13 (skills
created by the user, examples active from the start).
