# Mio looks at the picture

## What it is for

Mio can look at a photomicrograph of the section and propose the fields of the microscopic description and of the
pore system — sorting, roundness, sphericity, grain size, fabric, contacts, visible porosity and pore types — each
with **how many of its answers agree**. A model on your own computer does the looking; nothing is ticked and nothing
is written until you tick what you see yourself in the picture, apply it to the form and save the description.

## Before you start

* A **vision model** on this computer (*Mio looks* → *Vision models…*):
  * with an **NVIDIA RTX card of 12 GB** (RTX 3060 and up): **Qwen2.5-VL 7B** (Q5_K_M), 6.8 GB to download;
  * with a card of **24–32 GB** (RTX 5090): **Qwen2.5-VL 32B** (Q4_K_H), 19.3 GB;
  * with an 8 GB card or none: the smaller 7B (Q4_K_M) — on the processor it takes minutes a picture.

  The window marks the model that fits the card it finds. Each model comes as two files, the language model and its
  image projector; both are Apache-2.0. **llama-cpp-python** reads them (built with CUDA to use the card; the
  installers bring it built for the processor). Or use a **local server** that already has the model — Ollama (`ollama pull qwen2.5vl:7b`),
  LM Studio or llama-server — by giving its address (`http://localhost:11434/v1`) and model name.
* A **picture** of the section: a photograph or slide in the Atlas, the point count's image, or a file. The
  crossed-polarized picture of the same field helps (interference colours, extinction).

## Step by step

1. Open the description and click **Mio looks** (Home tab).
2. Choose the **picture**. Atlas photographs in plane-polarized light come first; their **crossed-polarized pair** is
   found by place on the section or by name (`… PP` / `… XP`) and shown beside it. For a whole slide, the central
   2 mm (one field of view) is shown. The **field width** comes from the picture's scale; type it if it is unknown —
   it lets the model judge the grain size.
3. Choose how many **answers** (3 by default) and click **Look**. The model is asked that many times; each answer is
   one line per field, with the words of RockFace's vocabulary in your language.
4. Read the table: the field, the **value** most answers gave (the others said are in its list, with how many gave
   them), the amount (the median, with the range said), **Answers that agree** (2/3, 3/3…) and the model's own line.
5. Look at the picture and **tick** only what you see yourself. *Tick where all answers agree* ticks the 3/3 lines —
   untick any you disagree with.
6. **Apply**, then save the description as usual. *Answers of the model* shows the full answers.

**Mio**: *"what do you see in ILL-TS-001?"* (*"o que você vê na …?"*, *"¿qué ves en la imagen de …?"*) looks at the
first plane-polarized picture of the sample and lists the proposals with their agreement; it writes nothing.

## How it works

* **The model.** Qwen2.5-VL (Bai et al. 2025) reads the picture at up to 1024 pixels on its longer side and answers
  a fixed form: one line per field, “not visible” when the picture does not let it judge. Its words go through the
  same reader as dictation (1.0.0rc6), so the proposals use RockFace's terms; the field named at the start of a line
  decides which proposals of that line are kept.
* **How sure.** A model's own words about its certainty are poorly calibrated (Xiong et al. 2024). Instead the model
  is asked several times at a temperature of 0.7 and the answers are compared: the confidence of a value is the
  share of answers that gave it (self-consistency, Wang et al. 2023). Amounts agree when they are within 2 percentage
  points or 25 % of the median (30 % for a size in mm). With one answer, the agreement says nothing.
* **Nothing ticked.** People follow automated advice even when it is wrong (automation bias, Goddard et al. 2012):
  every proposal starts unticked and is written only when you apply it.
* **Local only.** The pictures never leave the computer; a server address on another computer is refused unless
  `vision.allow_remote` is set on purpose.
* **What has been measured.** Not yet on real sections: this version was tested with scripted answers, not with the
  model running. Published work on describing thin sections with vision-language models — ThinGPT (Luo et al. 2025)
  and a carbonate model trained on 57 000 pictures (Atolagbe & Koeshidayatullah 2026) — used models trained on
  labelled sections; the general Qwen2.5-VL used here is not, so expect it to be surer of texture than of
  mineralogy, and check every proposal.
* **Not in this version.** Searching the library for the most similar sections and proposing from their
  descriptions waits for the owner's decision on two patents (US 12,688,615 B2; US 2022/0207079 A1).

## From a script

```python
d = prj["ILL-TS-001"]
r = d.look(samples=3)               # the first PP picture of the section in the Atlas, and its XP pair
[(f["target"], f["code"], f["value"], f["confidence"]) for f in r["findings"]]
r["answers"]                        # what the model wrote, answer by answer
d.look(image="field.png", xpl="field_xp.png", width_mm=1.3, apply=True, at_least=1.0)  # writes the 3/3 ones
rf.look("field.png", lang="pt")    # without a project
rf.vision_models(); rf.vision_status()
```

## Limits and common problems

* A general model, not a petrographer: it may mistake cement for grains or plucked grains for pores, or call every
  rock moderately sorted. Agreement between its answers measures its consistency, not its accuracy.
* Mineral composition is not proposed — the point count does that (with the AI assistant of 1.0.0rc7).
* Numbers win over words: a description with a measured sorting (φ) or grain size keeps the class that follows the
  number when the proposal is applied, and the save says so.
* A picture without scale: type the field width, or the grain size will be guessed from nothing.
* On the processor the 7B model takes minutes for three answers; the 32B needs a 24–32 GB card.
* “This llama-cpp-python cannot read Qwen2.5-VL pictures”: update llama-cpp-python, or use a local server.

## Coverage

O8 (the owner's request of 2026-11-17: the innovations, the fifth one).

References: Bai et al. (2025), Qwen2.5-VL technical report, arXiv:2502.13923; Wang et al. (2023), Self-consistency
improves chain of thought reasoning in language models, ICLR 2023, arXiv:2203.11171; Xiong et al. (2024), Can LLMs
express their uncertainty?, ICLR 2024, arXiv:2306.13063; Goddard, Roudsari & Wyatt (2012),
https://doi.org/10.1136/amiajnl-2011-000089; Luo et al. (2025), ThinGPT, Petroleum Science,
https://doi.org/10.1016/j.petsci.2025.09.009; Atolagbe & Koeshidayatullah (2026), Vision-language models for automated
carbonate petrography and depositional environment interpretation, Artificial Intelligence in Geosciences 7(3)
100230, https://doi.org/10.1016/j.aiig.2026.100230.
