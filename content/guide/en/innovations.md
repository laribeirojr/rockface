# The six innovations

## What it is for

Beyond the functions of the reference programs, RockFace brings six innovations of method, one per version from
1.0.0rc4 to 1.0.0rc9, from the simplest to the boldest. This page says what each one does, where it is in the
programs, and how it was checked; each has its own page.

| # | Innovation | Version · where | What it gives the petrographer |
|---|---|---|---|
| 1 | [How sure the point count is](counting_uncertainty.md) | 1.0.0rc4 · Petro | The 95 % interval of every counted constituent, the probability of each field of the classifications, the confidence region on the ternary diagram, and how many points are still needed |
| 2 | [Consistency between scales](consistency.md) | 1.0.0rc5 · Petro, MC, Lab | Seven checks between thin section, plug, micro-CT, well log and paragenetic sequence, each contradiction explained with its source |
| 3 | [Dictation at the microscope](dictation.md) | 1.0.0rc6 · Petro, Mio | Speaking the description and counting by voice without leaving the eyepiece; recognition on the computer |
| 4 | [Point counting assisted by AI](assisted_counting.md) | 1.0.0rc7 · Petro | A model that learns from the points counted and proposes the next ones, the most uncertain first, with an honest agreement |
| 5 | [Mio looks at the picture](mio_vision.md) | 1.0.0rc8 · Mio, Atlas | A vision model on the laboratory's graphics card proposes the texture and the pore system from a photomicrograph, each proposal with how many answers agree |
| 6 | [Federated learning between laboratories](federated_learning.md) | 1.0.0rc9 · Petro | Laboratories train one model of the count together; only the model's numbers leave each one |

## Step by step

1. **How sure the count is**: Composition → the column *95 % interval*; Classification → *Probability*; the ternary
   diagram → *Confidence region*; the Point count tab says when the classification is stable.
2. **Consistency**: the tab *Consistency* of a description, or Mio: *"is ILL-TS-001 consistent?"*.
3. **Dictation**: Home → **Dictate**; in the Point count tab, the microphone button.
4. **Assisted counting**: Point count tab → **Propose the constituent (AI)**; Enter accepts.
5. **Mio looks**: Home → **Mio looks** (a vision model on the computer, chosen in *Vision models…*).
6. **Federated learning**: Tools → **Federated learning**; in the Point count tab, **Shared model**.

## How it works

The six follow the same principles:

* **Local.** Everything runs on the user's computer — the statistics, the speech recognition, the vision model, the
  count's model; in a federation only the model's numbers leave, in a file the laboratory reads first.
* **The petrographer decides.** The program proposes and says how sure it is; nothing is written until the
  petrographer accepts it, and blind points measure the agreement without the bias of seeing the proposal first.
* **Measured.** Each innovation has an acceptance criterion and automatic tests: the intervals cover 95 % by
  simulation; every example of the dictation guide is understood in three languages; 91 % of the remaining points
  right after 75 counted uncertain-first, against 81 % in grid order; a federated model 83 % right at a laboratory
  that took no part, against 79 % for each laboratory alone (ILLUSTRATIVE data).
* **With sources.** Each version began with a survey of the literature and of the patents; the references are on each
  page, the patent notes in the licence audit. The search for similar thin sections in a library (innovation 5) was
  left out by the owner until a patent consultation.

## From a script

```python
d = prj["ILL-TS-002"]
d.uncertainty()                 # 1 · intervals and probabilities
d.consistency()                 # 2 · the checks between scales
d.dictate("moderately sorted, subrounded grains", "en")   # 3 · proposals from text
d.assist(top=5)                 # 4 · proposals of the count's AI
d.look(samples=3)               # 5 · what the vision model proposes
prj.federated_update("fed-r1.rffed", "lab.rfupd", site="Lab A")   # 6 · this laboratory's update
```

## Limits and common problems

* The proposals of 3–6 are proposals: each page says how they were measured and where they can fail.
* The vision model (5) was tested with scripted answers; its accuracy on real sections is still to be measured.
* Federated learning (6) protects the data, not every trace of them in the model: its page says what clipping and
  noise do and do not do.

## Coverage

O8 (the owner's request of 2026-11-17: "Gostei de todas elas. Podemos implementar da mais simples para a mais
ousada?").
