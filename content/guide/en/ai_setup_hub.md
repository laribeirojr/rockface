# RockFace AI: installation, device and the model hub

## What it is for

RockFace AI adds neural networks to Lab and MC: models that segment pictures, whole thin sections, micro-CT volumes
and image logs, that you can train and fine-tune on your own annotations, and a generative model of rock images. It
is an **option**: RockFace without AI has every other function, and nothing else changes when you add it. This page
shows how to install it for the computer you have, how to choose where the models run (the processor or a graphics
card), and how the models are kept, shared and compared in the **model hub**.

## Before you start

* RockFace installed (0.26 or later).
* For a graphics card: the card's own driver (NVIDIA, AMD or Intel). The rest comes with the packages.

## Step by step

### Installing: the computer is detected, you choose

1. In a terminal, run `rockface ai setup`. RockFace lists what it found — system, processor, cores, vector
   instructions, memory, graphics cards, and the AI packages already installed — and the options for this computer:

   | Option | When |
   |---|---|
   | RockFace without AI | Nothing more to install |
   | AI on the processor | Any computer; applying a model takes seconds to minutes, training minutes to hours |
   | AI on the NVIDIA graphics card (CUDA) | An NVIDIA card: the fastest for applying and for training |
   | AI on the graphics card (DirectML) | Windows with any DirectX 12 card (NVIDIA, AMD, Intel): models are applied on the card, training runs on the processor |
   | AI on Apple silicon (Core ML and MPS) | A Mac with an M processor |

   The recommended option is marked; **you decide**. Type its number (or press Enter for the recommended one).
2. RockFace shows the installation command (`python -m pip install …`) and asks before running it. With
   `--option cuda --yes` it chooses and installs without asking; with `--dry-run` it only shows the command.
3. The same dialog is in the program: **Lab → AI** or **MC → AI**, button **Hardware and device…**. It shows the
   hardware, the options with the recommended one in bold, and the command that installs the one you select (with a
   **Copy** button). **OK** keeps your choice.

`rockface ai info` shows the hardware and the device in use; `rockface ai models [project]` lists the models.

### The model hub

The table **Models** of the AI tab lists every model RockFace knows for that tab, from three places:

* **RockFace** — the models shipped with the program (see *How it works*);
* **Hub folder** — a folder shared by the team (a network drive, a synchronised folder), chosen the first time you
  click **Publish to hub**, or given by the variable `ROCKFACE_AI_HUB`;
* **Project** — the models trained in, or imported into, the project.

Select a row and use:

* **Card…** — what the model is: task, inputs, classes, the data it was trained on and their licences, the metrics
  on held-out data, its parent model (when it was fine-tuned) and its lineage, and the SHA-256 of the network;
* **Import… / Export…** — a model as one `.rfai` file, to send to a colleague or keep;
* **Publish to hub** — the model written to the hub folder as `<name>/<version>.rfai`, with an `index.json` of the
  hub; a version is never overwritten;
* **Delete** — a model of the project (with a line in the audit);
* **Compare** — the cards of the selected rows side by side (metrics, data, parent).

## Options

| Field | What it changes |
|---|---|
| Option (setup) | Which packages are installed and which device runs the models |
| `ROCKFACE_AI_DEVICE` | The device without the interface (`cpu`, `cuda`, `directml`, `coreml`) — for scripts and jobs |
| `ROCKFACE_AI_HUB` | The hub folder without the interface |

## How it works

* **Two layers, installed apart.** Applying a model uses ONNX Runtime (MIT licence; extra `ai`), whose execution
  providers run the same network on the processor, on CUDA, on DirectML or on Core ML; the processor is always the
  fallback. Training uses PyTorch (BSD licence; extra `ai-train`) on the processor, CUDA or Apple's MPS.
* **A model is data, never code.** An `.rfai` file is a zip with `model.onnx` (the network, ONNX format) and
  `card.json` (its card). The card holds the SHA-256 of the network, checked on every load: a changed file is
  refused. Models are never pickled Python objects.
* **Versions and lineage.** Each model has a name and a version; fine-tuning a model makes the next version with the
  model it came from as its parent; the same name and version cannot be kept twice.
* **The models shipped** were trained only on data whose licence allows it — RockFace's synthetic data (exact truth)
  and open data under CC BY 4.0 or ODC-BY — and each card states the data and the metrics measured on data the model
  did not see. Data under non-commercial or share-alike licences are used only for internal tests, never to train a
  model that ships.

## From a script

```python
info = prj.ai_hardware()              # hardware, options (recommended one marked), device, packages installed
for m in prj.ai_models():             # every model: source, name, version, task, licence, held-out metrics
    print(m["name"], m["version"], m["metrics"])
m = prj.ai_model("rockface-thinsection-pores")      # the newest version, wherever it is
prj.ai_export(m, "pores.rfai"); rid = prj.ai_import("pores.rfai")
prj.ai_publish(rid, "//server/rockface-hub"); print(prj.ai_lineage(rid))
```

## Limits and common problems

* "RockFace AI is not installed": run `rockface ai setup` (or `pip install -e ".[ai]"` from the source).
* "Training needs the extra ai-train": applying models works; training needs PyTorch (`pip install -e ".[ai-train]"`).
* On Linux, the PyTorch package from PyPI brings the CUDA libraries (about 3 GB). For a processor-only computer,
  install it from the PyTorch CPU index (`pip install torch --index-url https://download.pytorch.org/whl/cpu`).
* A card not listed: update its driver; on Windows the DirectML option works with any DirectX 12 card.

## Coverage

L13 (model hub), GT18 / GV19 (the pretrained models and the choice of the model for the hardware found), and the
AI installation of the ROADMAP stage 0.26.
