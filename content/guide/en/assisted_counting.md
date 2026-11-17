# Point counting assisted by AI

## What it is for

Most of the points of a count are easy: the same quartz, the same pore resin, again and again. The AI assistant
learns them from the points you count and proposes the line of the next point; you confirm with **Enter** or count
another line. Each confirmation or correction teaches the model at once, so after a few dozen points most proposals
are right and the count goes faster — while every point is still decided by you.

## Before you start

* A **grid** on the count's **image** (Point count → Image and calibration: *Section image…*, then *Make grid*).
* Optionally the **crossed-polarized image** of the same field, same size and framing (*Crossed-polars image…*): the
  model then also learns the interference colours.
* The program's AI libraries (`rockface[lab]`, in both installers' editions).

## Step by step

1. Count the first points as usual — at least **15 points of two lines or more**.
2. Tick **Propose the constituent (AI)**. Under the count buttons you see the proposal for the current point:
   *AI: Monocrystalline quartz — 92 %*, and the next lines with their probabilities.
3. Press **Enter** (or *Accept*) when the proposal is right; count another line (keyboard, list, voice) when it is
   not. The model learns again after every point.
4. **Blind check**: about one point in ten shows *Blind check: count this point without a proposal*. These points
   are always the same; on them you count without seeing the proposal, so the agreement measured there is honest.
5. Tick **Most uncertain points first** to let the model choose the next point: the one where it is least sure.
   It learns fastest there. **Count every point** of the grid afterwards — a count stopped half way after this is
   not a random sample of the section, and the tab says so.
6. Read the line below: the model's points and its out-of-bag accuracy, your **agreement** with the proposals and
   the agreement on the **blind** points with its 95 % interval.

**Mio**: *"how did the AI do in the count of ILL-TS-002?"* gives the agreement, the blind one and the most frequent
corrections.

## How it works

* **What the model sees.** Around every point, three windows of the image: the cross-hair (3 × 3 pixels), the grain
  under it (30 µm) and its surroundings (90 µm). In each: the mean and spread of red, green and blue, saturation,
  brightness, hue, the 10th, 50th and 90th percentiles of the brightness, the mean gradient (texture, relief) and how
  blue it is (pore resin) — 45 numbers, 90 with the crossed-polarized image.
* **The model** is a random forest (Breiman 2001), the same as RockFace Lab's, trained on the counted points; the
  share of its trees that vote for a line is the proposal's probability. It is trained again whenever the counted
  points change — a fraction of a second.
* **Active learning.** The *margin* between the two most probable lines measures the doubt; *most uncertain first*
  visits the point of the smallest margin (uncertainty sampling, Settles 2009).
* **Measured on an ILLUSTRATIVE textured section** (the synthetic rock of the guide, PP and XP, 300 points): after
  15 counted points the proposals were right on 54 % of the points still to count; after 60 more, 81 % visiting the
  grid in order and **91 % visiting the most uncertain points first**. On the example's flat-coloured section
  (ILL-TS-002), trained on 100 points, 94.5 % of the other 200 were right.
* **Why blind points.** People follow automated advice even when it is wrong (*automation bias*, Goddard et al.
  2012); agreement measured on points whose proposal you saw is inflated by that. The blind points, with the
  proposal hidden, measure the model as it is. Every counted point keeps what was proposed, its probability and
  whether it was blind.

## From a script

```python
d = prj["ILL-TS-002"]
r = d.assist(top=10)              # the ten most uncertain points not yet counted
r["ready"], r["trained_on"], r["oob"]
[(q["index"], q["uid"], round(q["p"], 2)) for q in r["proposals"]]
d.set_crossed_image("ILL-TS-002-xpl.png")    # the same field under crossed polars
d.ai_agreement()                  # {"proposed", "agreed", "rate", "blind", "blind_rate", "interval", ...}
```

Scripts only read the proposals: counting stays with the petrographer.

## Limits and common problems

* The model knows only this section and the lines counted in it: it learns afresh in every count, so the first
  points are always counted by hand. A rare constituent seen once or twice is seldom proposed — count it yourself.
* Proposals depend on the image: out of focus, uneven light or a different magnification from the counted points
  make them worse. Points outside the image get no proposal.
* The image must be calibrated (µm per pixel) so the windows have their real size.
* Visiting uncertain points first changes the order, not the grid: use it only when you will count every point.
* The model is not shipped and is not pretrained on other rocks; the LITHOS benchmark (Chacón et al. 2025, 25 mineral
  classes) is non-commercial and was used only to read about the state of the art.

## Coverage

O8 (the owner's request of 2026-11-17: the innovations, the fourth one).

References: Breiman (2001), https://doi.org/10.1023/A:1010933404324; Settles (2009), Active learning literature
survey, Univ. Wisconsin–Madison TR 1648; Tang, Milliken & Spikes (2020), https://doi.org/10.1016/j.marpetgeo.2020.104518;
Chacón et al. (2025), Towards automated petrography, arXiv:2511.00328; Goddard, Roudsari & Wyatt (2012),
https://doi.org/10.1136/amiajnl-2011-000089.
