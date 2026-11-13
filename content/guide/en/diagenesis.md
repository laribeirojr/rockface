# Diagenesis: environments, paragenetic sequence and knowledge graph

## What it is for

The **Diagenesis** tab interprets the diagenetic environments the rock went through — marine, meteoric, arid,
alkaline lacustrine, burial, hot fluids, uplift — from the features of its description, each conclusion with the
rules and sources behind it. It also builds the **paragenetic sequence**: the diagenetic phases in the order they
formed, with their regime (eo-, meso- or telodiagenesis). The petrographer confirms or rejects each environment,
and can reorder the sequence by hand.

## Before you start

A description whose composition has diagenetic constituents, ideally with their habits, locations and paragenetic
relations (covers, replaces, postdates…) (page [Composition](composition.md)).

## Step by step

### The environments

1. Open the **Diagenesis** tab.
2. **Diagenetic environments** lists every **Environment** with its **Regime** and the **Result**:
   * *interpreted* — one indicative rule or two different supporting rules were found;
   * *some evidence* — one supporting rule;
   * empty — "No evidence of this environment in the description."
3. Select an environment to see the rules **Found**: the feature of the description, the rule and its source.
4. In **Petrographer**, **confirm** or **reject** it; your decision wins over the automatic result. Write a **Note
   on this environment** if needed.
5. **Diagenetic interpretation — notes**: the overall interpretation in your words.

### The paragenetic sequence

1. **Paragenetic sequence** shows the phases in order, each with its **Step**, **Phase** (precipitation or
   dissolution of a constituent) and **Regime**, and the chart of the sequence.
2. The order comes from the paragenetic relations of the composition; the regime from the rules. Contradictions
   are reported: "Contradictory relations between … and …: left out of the order", "… comes before … but belongs to
   a later regime".
3. **Up** and **Down** move a phase; the regime can be changed in its cell. **Automatic** brings back the order
   worked out by RockFace.
4. **Export picture…** saves the chart.
5. **Save** (Ctrl+S): the interpretation is part of the description.

### The knowledge graph

1. **Knowledge graph…** (in the tab, or Tools → Knowledge base → **Knowledge graph**).
2. The graph links the features of a description → the rules → the environments → the regimes. Solid lines are
   indicative rules, dashed lines supporting rules; the rules found in the open description are in blue.
3. In **Environment**, choose one to see only its part of the graph, or **(all environments)**. **Export picture…**
   saves it.

## Options

| Field | What it changes |
|---|---|
| Petrographer | Confirmed or rejected: replaces the automatic result in reports, queries and figures. |
| Up, Down, regime cell | The sequence set by hand (kept with the description). |
| Automatic | Back to the order and regimes found by RockFace. |

## How it works

* The rules are RockFace's own, each from the published literature: Morad et al. (2000, 2010), Worden & Burley
  (2003), Longman (1980), Flügel (2010), Scholle & Ulmer-Scholle (2003), Radke & Mathis (1980), Tosca & Wright
  (2018), Paxton et al. (2002), Schmidt & McDonald (1979), Taylor (1950), Park & Schot (1968).
* An environment is *interpreted* with one indicative rule or two different supporting rules, and has *some
  evidence* with one supporting rule. The aggregation is stated in the program and in `docs/NOMENCLATURE.md`; the
  petrographer's decision always wins.
* The order of the phases is a topological sort of the relations; relations that contradict each other are left
  out and reported.
* RockFace Explorer draws the paragenetic evolution of several samples together (page [Paragenetic evolution and the stratigraphic column](evolution_column.md)).

## From a script

```python
d = prj["TS-9"]
for code, r in d.interpret().items():
    print(code, r["status"], r["regime"], r["rules"])          # e.g. meso_burial interpreted meso ['albitization']
d.diagenesis.decisions["eo_marine"] = "confirmed"
d.save()
for step in d.paragenesis():
    print(step["step"], step["phase"], step["kind"], step["regime"])
rf.paragenesis_figure("sequence.png", d)
rf.knowledge_graph("graph.svg", environment="meso_burial")      # also .png, or .dot for the whole graph
```

## Limits and common problems

* "No diagenetic phases in the composition." — add diagenetic constituents first.
* Without paragenetic relations, the phases have no order: give the relations in the composition (covers,
  replaces, postdates, fills dissolution of…).
* The DOT file of the knowledge graph (for Graphviz) is written for the whole graph only.

## Coverage

P33 (diagenetic environment interpretation), P40 (knowledge graph), L8 (paragenetic sequence generator).
