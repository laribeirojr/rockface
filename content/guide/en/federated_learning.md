# Federated learning between laboratories

## What it is for

Several laboratories train **one model of the point count together**, and each keeps its pictures, points and
descriptions. Only the model's numbers leave a laboratory, in a file it can read before sending. The shared model
then helps every laboratory's counts: with the **AI proposals** of the point count (1.0.0rc7) it proposes the
constituent under a point **from the first point**, before a new count has the 15 points its own model needs.

## Before you start

* Counts with their picture (Point count tab → the section's image), counted points, and lines whose constituent is
  in RockFace's knowledge base. The crossed-polarized picture is needed only if the federation asks for it.
* At least 50 counted points in the counts you send (fewer points are easier to recover from an update).
* One laboratory **coordinates**: it creates the federation and combines the updates. Any laboratory can do it.
* A way to exchange small files (about 55 kB each): e-mail, a shared folder, a disk — whatever each institution
  allows. Nothing is sent by RockFace itself.

## Step by step

**The coordinator — create the federation.** Tools → **Federated learning** → *Coordinate*. Give it a name, the
number of rounds (20), the local passes per round (2), the largest update (5) and, if wanted, noise (see below).
**Create the federation…** writes `<name>-r1.rffed`. Send it to the laboratories.

**Each laboratory — take part.** *Take part* → **Open a federation…** → the `.rffed` received. Type the name the
others will see (e.g. *Lab A*), tick the counts to use, and click **Prepare my update**. RockFace shows
**what leaves this computer — the whole file**: the federation, the round, your laboratory's name, the number of
points, the change of the model's weights (some ten thousand numbers), its size, and how the shared model did on 20 %
of your own points kept aside, before and after your passes. Below it, **what stays here**: your points by
constituent. **Save the update…** and send the `.rfupd` to the coordinator.

**The coordinator — the next round.** *Coordinate* → **Open a federation…** (the current `.rffed`) → **Add the
laboratories' updates…** → **Combine into the next round…** writes `<name>-r2.rffed`. The history shows each round:
the laboratories with their points, and how many of their held-out points the shared model got right before and
after. Send the new file to the laboratories, and repeat.

**Everybody — use it in the count.** *Use in the count* → **Choose the shared model…** (the latest `.rffed`). In the
Point count tab tick **Propose the constituent (AI)** and **Shared model**: the proposals come from the first point, marked *(shared
model)*; as you count, your own model learns and the two are mixed — the shared model weighs as much as 30 of your
points, then less and less (*this count and the shared model*). Nothing is counted for you: Enter accepts a
proposal, as in 1.0.0rc7, and blind points still measure the agreement honestly.

**Mio**: *"como está a federação?"* (*"status of the federated model?"*, *"¿cómo va la federación?"*) gives the shared
model in use, its rounds, the laboratories of the last round and its accuracy on their held-out points.

## How it works

* **The model.** A network of one hidden layer on the same 45 features of the count's assistant (colour, spread,
  saturation, hue, brightness percentiles, edges and blue resin in windows of 3 × 3 pixels, 30 µm and 90 µm around the
  point; 90 with the crossed-polarized picture). Its classes are **every constituent of the built-in knowledge base**
  (106): a fixed list, so the list tells nothing about anyone's rocks.
* **Each picture standardized by itself.** Before the model sees a point, each feature is standardized by the mean
  and spread of that feature at all the grid points of the same picture, counted or not. That takes out each
  laboratory's stain, lamp and camera, and needs no statistics from anyone — the idea of keeping the normalization
  local (FedBN, Li et al. 2021).
* **Federated averaging.** In each round every laboratory starts from the shared weights, makes a few passes over its
  own points and sends the change; the coordinator adds the average of the changes, each weighted by its number of
  points (FedAvg, McMahan et al. 2017; FedProx's proximal term is available for scripts, Li et al. 2020). Rounds by
  files are how two oil companies and a university ran a federated test on digital rocks: the weights went by file
  transfer, and the federated models beat every participant's own model (Chang et al. 2024).
* **Checks.** An update of another federation, of another round, made from another version of the model, of a
  laboratory already in the round, with a field that should not be there, or with numbers that are not finite, is
  refused. Every file carries a fingerprint; a changed file is refused.
* **What it protects, and what it does not.** Pictures, points, coordinates, names and the constituents counted never
  leave. But a model's numbers can still say something about the data it learned from: gradients can be inverted
  (Zhu et al. 2019) and membership guessed (Shokri et al. 2017). An update of hundreds of points after several passes
  is far harder to invert than one gradient; the **largest update** cuts big updates down, and **noise** makes any
  update harder still — at a price: with two laboratories, noise 0.01 cost about 1 point of accuracy, 0.02 six, 0.05
  fifteen (the trial below). This is **not a formal differential-privacy guarantee** per point (that needs clipping
  per point and a privacy accountant, Abadi et al. 2016), and the coordinator sees each laboratory's update (secure
  aggregation, Bonawitz et al. 2017, is not implemented). Choose a coordinator all the laboratories trust.

**The trial (ILLUSTRATIVE).** Two invented laboratories, each with three counted sections of about 260 points, its
own colour cast, and most of one constituent left uncounted (A seldom counted feldspar, B seldom cement); 20 rounds of
2 passes; the accuracy on sections never seen (mean of three repetitions, `tools/bench_federated.py`):

| Model | Lab A | Lab B | Lab C (took no part) |
|---|---|---|---|
| Federated | 80 % | 83 % | 83 % |
| All points pooled (possible only with invented data) | 81 % | 84 % | 86 % |
| Lab A alone | 76 % | 74 % | 79 % |
| Lab B alone | 76 % | 78 % | 79 % |

A new count at Lab C with the shared model: 83 % of the proposals right from the first point; without it, no
proposal before 15 points, 42 % at 15, 71 % at 30, 79 % at 60 (and 83 % at 60 with both).

## From a script

```python
rf.federation_create("sandstones-r1.rffed", "Sandstones", rounds=20)          # the coordinator
r = prj.federated_update("sandstones-r1.rffed", "lab-a.rfupd", site="Lab A")    # each laboratory
r["fields"]                                   # every field of the file that would leave
r["by_class"]                                 # what stays: points by constituent
rf.federation_aggregate("sandstones-r1.rffed", ["lab-a.rfupd", "lab-b.rfupd"], "sandstones-r2.rffed")
rf.federation("sandstones-r2.rffed")["history"]
prj["ILL-TS-002"].assist(top=5, shared="sandstones-r2.rffed")   # proposals with the shared model
```

The module `rockface.core.federated` has the parts: `create`, `site_data`, `site_update`, `inspect`,
`check_update`, `aggregate`, `simulate`, `centralized`, `local_only`.

## Limits and common problems

* The model is as good as the counts behind it: a constituent nobody counts is never proposed, and one counted with
  different names in two laboratories confuses it. The classes are the knowledge base's constituents.
* Very different rocks (a carbonate federation and a sandstone count) give poor proposals; the history's *Right
  before* column shows how the shared model does on each laboratory's own points before it learns from them.
* A count without a picture, or without the crossed-polarized picture when the federation asks for it, is left out.
* "Only N points can teach the model": tick more counts, or count more points.
* The proposals of the shared model are proposals: the petrographer counts, and Enter only accepts what he sees.
* *Patents.* Google holds patents on federated learning (e.g. US 10,402,469 B2, US 11,120,102 B2, US 10,657,461 B2).
  RockFace averages updates exchanged as files and uses no compressed or sketched updates and no adaptive server
  optimizer; this is a design note, not a legal opinion (`docs/LICENSE_AUDIT.md`).

## Coverage

O8 (the owner's request of 2026-11-17: the innovations, the sixth one).

References: McMahan et al. (2017), Communication-efficient learning of deep networks from decentralized data,
AISTATS, arXiv:1602.05629; Li et al. (2020), Federated optimization in heterogeneous networks (FedProx), MLSys,
arXiv:1812.06127; Li et al. (2021), FedBN, ICLR, arXiv:2102.07623; McMahan et al. (2018), Learning differentially
private recurrent language models, ICLR, arXiv:1710.06963; Abadi et al. (2016), Deep learning with differential
privacy, CCS, https://doi.org/10.1145/2976749.2978318; Zhu, Liu & Han (2019), Deep leakage from gradients, NeurIPS,
arXiv:1906.08935; Shokri et al. (2017), Membership inference attacks, IEEE S&P,
https://doi.org/10.1109/SP.2017.41; Bonawitz et al. (2017), Practical secure aggregation, CCS,
https://doi.org/10.1145/3133956.3133982; Kairouz et al. (2021), Advances and open problems in federated learning,
https://doi.org/10.1561/2200000083; Chang et al. (2024), Federated learning test for collaborative machine
learning, SCA2024-1036; RahimiZadeh et al. (2025), FTA-FTL: federated transfer learning for lithology microscopic
images, arXiv:2501.03349.
