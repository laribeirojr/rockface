# Mio: questions in plain language and the local language model

## What it is for

**Mio** is RockFace's assistant. You ask her about the descriptions of the project in your own words — "which
samples have barite?", "quantas amostras do poço B têm porosidade acima de 20 %?", "average permeability of the
samples with kaolinite", "what is missing before the study?", "how do I segment a section with AI?" — and she answers
from the database: the descriptions that match, how many, minimum, mean and maximum of a number, the values of a field,
the main facts of one sample, the descriptions without a value, the page of this guide that explains a task. Every
answer shows the conditions she read, so you see exactly what was asked of the database.

In the Explorer the same reading works as a **plain-language search**: type the question in the search box of the
toolbar and the query appears in the criteria list, ready to refine, save or export.

Mio works without a language model (her rules understand the words of RockFace's nomenclature in English,
Portuguese and Spanish, numbers — also written in words — and comparisons). A **local language model** — a small open model that runs on your
computer, on the processor or the graphics card — lets her understand freer questions: other spellings ("baryte",
"kaolin"), synonyms ("dolomite rhombs"), words outside the nomenclature.

## Before you start

* A project open with descriptions.
* For the language model: RockFace with the extra `llm` (`pip install "rockface-suite[llm]"`, which installs
  llama-cpp-python), or a local server already running (Ollama, LM Studio or llama-server). No graphics card is needed.

## Step by step

### Asking Mio

1. Click **Mio** in the toolbar (in Petro: **Tools → Mio**), or press **Ctrl+Alt+M**. The Mio panel opens on the right.
2. Type the question and press **Enter** (or **Ask**). `@mio` at the start is optional in the panel.
3. Read the answer and the line **Conditions read**. **Words not used** lists words she did not turn into a
   condition — rephrase if one of them mattered.
4. When the answer is a search, **Open in Explorer** shows it as an Explorer query.

In any search box that talks to Mio (the Explorer's), a text that starts with **@mio** goes to the panel.

### Plain-language search in the Explorer

1. **Explorer** → type in the box *Search in plain language…* (for example *samples with barite and porosity above
   20 %*) and press **Enter**.
2. The criteria appear in the list and the descriptions found below them. A question that is not a single query
   ("calcite or dolomite") selects the descriptions in the list instead.

### Choosing the language model

1. In the Mio panel, click **Language model…**.
2. The dialog shows this computer (memory, threads, graphics cards, whether llama.cpp can use the card) and the
   models that fit it, with size, licence, where it would run and the **recommended** one marked. You choose:
   * **The model selected in the list** — downloaded once (it asks first, with the size and licence) and kept in
     `~/.rockface/llm`;
   * **A GGUF file on this computer** — any model in GGUF format you already have;
   * **A local server** — the address of Ollama (`http://localhost:11434`), LM Studio or llama-server, and the model
     name on the server.
3. **Run on**: the processor or the graphics card. **OK** keeps the choice; the model loads with the first question.
4. **Use the language model** (panel) switches it on and off; **Fluent answers** lets the model rephrase the answer
   (kept only when its numbers are exactly those of the database).

From the command line: `rockface llm setup` (the same choice, with the recommended one marked), `rockface llm use
<file.gguf | http://localhost:11434>`, `rockface llm info`, and `rockface llm ask <project> "<question>"`.

## Options

| Field | What it changes |
|---|---|
| Use the language model | Off: the rules answer alone. On: the model reads the questions the rules leave words of |
| Fluent answers | The model rephrases the answer; a rephrasing with any number changed is discarded |
| Run on | Processor or graphics card (the card needs llama.cpp built with CUDA, Metal or Vulkan) |
| `ROCKFACE_LLM_PATH`, `ROCKFACE_LLM_URL`, `ROCKFACE_LLM_DEVICE` | The model without the interface (scripts, jobs) |
| `ROCKFACE_LLM_DIR` | Where downloaded models are kept |

The models offered (all with permissive licences, Q4_K_M quantization):

| Model | File | Licence | For |
|---|---|---|---|
| Qwen2.5 0.5B Instruct | 0.40 GB | Apache-2.0 | any computer |
| Qwen3 1.7B | 1.28 GB | Apache-2.0 | laptops (recommended with fewer than 8 threads) |
| Qwen3 4B · Phi-4 mini | 2.5 GB | Apache-2.0 · MIT | 8 threads or more, 8 GB of memory |
| Qwen2.5 7B Instruct · Qwen3 8B | 4.7–5.0 GB | Apache-2.0 | a graphics card |

## How it works

* **The database answers, never the model.** The question is read into criteria of the Explorer (the same criteria
  you build by hand) and the descriptions are found by the Explorer in the records. The model is only asked to turn
  the words the rules did not understand into phrases of RockFace's vocabulary, with numbers; its phrases are checked
  against the vocabulary (a phrase that is not in it is dropped or replaced by the closest one) and read again by the
  rules, so every condition is one the user sees. The answer constrained to a JSON schema (llama.cpp grammar) keeps
  the model from writing anything else.
* **The rules.** The vocabulary is the project's knowledge base (constituents, groups, habits, locations, modifiers
  in three languages), the values of the identification (wells, formations, facies…), the analyses (porosity,
  permeability, depth, totals) and the spot analyses; words are compared without accents and plurals, with one
  letter of tolerance for long words; numbers attach to the nearest number word, habits to the nearest constituent.
* **The tools.** `search`, `count`, `stats`, `values`, `describe`, `missing`, `suggest`, `guide` — all read only.
  Mio's **skills** chain them (*Mio's skills* page).
* **Privacy.** The model runs on the computer; a server address on another computer is refused unless you allow it
  explicitly, because the questions and the records shown to the model would leave the computer.
* **Accepted on a test set.** An ILLUSTRATIVE project of 48 invented descriptions of known content and 41 questions
  in English, Portuguese and Spanish: 41 right by the rules. Fifteen harder paraphrases: 8 right by the rules
  alone, 13 with Qwen2.5 0.5B on a processor without a graphics card (2 threads; 3–14 s, median 5 s, for the
  questions that call the model) — `docs/LLM.md`.

## From a script

```python
a = prj.ask("amostras com barita e porosidade acima de 20 %")      # rules only
print(a.count, a.names, a.explanation, a.unknown)
q = a.query()                                                      # the Explorer query, when it is one
mio = prj.mio(model=True, lang="pt")                               # with the language model configured
r = mio.ask("@mio quantas amostras do poço ILLUSTRATIVE-B têm caulinita?")
print(r.tool, r.text, r.data)
from rockface.api import llm
m = llm.LlamaModel("Qwen2.5-0.5B-Instruct-Q4_K_M.gguf", device="cpu")   # or llm.ServerModel("http://localhost:11434", "qwen2.5:0.5b")
print(prj.ask("plugs containing baryte", model=m).names)
```

## Limits and common problems

* "No language model": choose one with **Language model…** or `rockface llm setup`; Mio still answers with her rules.
* A word ignored: it is listed under **Words not used**; use the term of the nomenclature or switch the model on.
* The first question with a model takes a few seconds more (the model is loaded once per session).
* On a server project the panel answers in the window's thread (the window waits while the model reads).
* Mio does not change the project: tools and skills only read; suggestions are written only when you accept them.

## Coverage

L1 (natural-language search of the database), the assistant that calls the program's tools and the choice of the
processor or the graphics card of the ROADMAP stage 0.27.
