# Talking with Mio

## What it is for

Mio is a conversation, as with a chat assistant: you write the way you would to a colleague — *how do I export the
wells to LAS?*, *and the trajectory too?*, *what is poikilotopic calcite?*, *how many samples of this project have
pyrite?* — and she answers in a few sentences, in your language, and keeps the thread of the conversation. You do not
need to learn commands or key words.

She answers from what RockFace says about itself — the user guide, the manuals and the website — and from the project
open in the window. Each answer names the pages it came from, as links that open the guide at the right section. The
numbers about your project are computed by RockFace's tools, as before; any number in an answer that is not in what
Mio read is shown as one to check.

The language model runs on your computer only. It is downloaded once; after that, Mio works without internet and
nothing you ask leaves the computer.

## Before you start

* RockFace 1.0.0rc3 or later, installed with the installer (both editions bring llama.cpp, the engine that runs the
  model). From the Python source: `pip install "rockface-suite[llm]"`.
* For the recommended model, about 4 GB of free memory and 2.5 GB of disk space; the internet once, to download it.
  No graphics card is needed.
* A project open, for questions about the project; questions about the program need none.

## Step by step

### Download the model (the first time)

1. Open Mio's panel: the **Mio** button of the toolbar (in Petro, **Tools → Mio**) or **Ctrl+Alt+M**.
2. When there is no model yet, the panel offers the one recommended for this computer — for instance *Qwen3 4B
   Instruct 2507 (2.5 GB, runs on the processor)*. Click **Download Qwen3 4B Instruct 2507**. A progress window shows
   the download; **Cancel** stops it.
3. **Other models…** opens the list of the models that fit this computer, a GGUF file you already have, or a local
   server (Ollama, LM Studio). **Not now** hides the offer until the program is opened again; Mio then answers with
   her rules and the guide's passages.
4. When the download ends, Mio says the model is ready. The first answer loads it (a few seconds); later answers start
   at once.

### Talk

1. Write in the box at the bottom and press **Enter** or **Ask**.
2. The answer appears word by word. **Stop** ends it early.
3. Go on with the conversation: *and with porosity above 10?*, *explain the second step*, *and in Spanish?*. A short
   follow-up is completed with the earlier questions before Mio looks things up (for a project question, the
   complete question is the one the tools answer).
4. **New conversation** starts again: Mio forgets the conversation (the model stays loaded).

The picture shows an answer written by Qwen3 4B Instruct 2507 on a processor, recorded in the evaluation of
2026-11-15 (`tools/mio_eval`).

### Sources and checked numbers

* Below each answer, **Sources** lists the passages the answer cites ([1], [2]…). A guide passage opens **Help → Help contents** (F1) at its section; a manual opens its PDF on the website.
* For a question about the project, the answer is written from the result of the tool (count, average, values,
  summary of a sample, a term of the nomenclature, the U-Pb ages). **Open in Explorer** shows a search as an Explorer
  query.
* *Check these numbers…* below an answer lists the numbers of the answer that are not in the passages or the
  project's results Mio was given.
* Scripts (*write a script that…*), connector calls (*find Folk 1980 in Crossref*) and skills called by their name
  (*/well-summary A*) work as before.

## Options

| Field | What it changes |
|---|---|
| Use the language model | Off: Mio answers with her rules, and a question about the program gets the best passages of the guide |
| Language model… | The model: one of the list (the recommended one marked), a GGUF file, or a local server; processor or graphics card |
| `llm.context` (settings) | How many tokens the model reads at once (8192 by default): longer conversations keep more of their beginning |
| `ROCKFACE_LLM_PATH`, `ROCKFACE_LLM_URL`, `ROCKFACE_LLM_DIR` | The model without the interface (scripts, the terminal) |

The models (permissive licences, Q4_K_M quantization; the recommended one depends on the memory, the threads and the
graphics card found):

| Model | File | Licence | For |
|---|---|---|---|
| Qwen3 4B Instruct 2507 | 2.5 GB | Apache-2.0 | the conversation (recommended with 8 threads or more) |
| Qwen3 1.7B | 1.3 GB | Apache-2.0 | notebooks with fewer than 8 threads (faster, simpler answers) |
| Qwen2.5 0.5B Instruct | 0.4 GB | Apache-2.0 | computers with little memory (short answers) |
| Qwen2.5 7B Instruct · Qwen3 8B | 4.7–5.0 GB | Apache-2.0 | a graphics card |

## How it works

* **What RockFace says.** The guide (English, Portuguese and Spanish), the seven manuals (in Portuguese for now) and the website's texts are
  cut into about 2,000 passages shipped with the program. For each message, the passages that best answer it are found
  by word statistics (BM25, without accents and plurals; acronyms such as LAS kept), in the language of the message
  first. Four of them go with the message, numbered.
* **What the project says.** Questions about the project are answered by Mio's tools (search, count, statistics,
  values, summary, missing values, nomenclature, ages), the same as in her earlier versions; their result goes with
  the message.
* **The answer.** The model is told who Mio is and to take facts about the program only from the passages, and
  numbers about the project only from the results, citing the passages it uses. The conversation goes with each
  message; when it no longer fits, the oldest turns are shortened first.
* **Checked.** Every number of the answer is looked for in what the model was given; the others are listed to check.
  A question the project's tools answer goes to the model with their result only, and an answer whose numbers do not
  match that result is replaced by the tool's own sentence (with a note saying so).
* **Measured.** An evaluation set of 150 questions written as users ask them (70 in Portuguese, 40 in English, 40 in
  Spanish, one or more on every page of the guide), plus project questions, small talk and follow-ups
  (`tools/mio_eval`): the passages of an expected page are among the four given to the model for 9 questions in 10.
  The answers of the real model are measured by the downloads repository's workflow "Mio evaluation": with Qwen3 4B
  Instruct 2507 on a processor, every answer came in the language of the question, 136 of the 150 documentation
  answers cited a passage of the page that answers, and the 10 project questions gave the tools' numbers
  (2026-11-15).
* **Privacy.** The model runs in RockFace (llama.cpp) or on a server on this computer; a server on another computer is
  refused unless you allow it explicitly.

## From a script

```python
import rockface.api as rf

c = rf.chat(lang="en", model=True)                  # the model of the settings; model=None: rules and passages
r = c.ask("How do I export the wells to LAS?", on_token=print)
print(r.text, r.cited, [s["title"] for s in r.sources])
r = c.ask("And the trajectory too?")                # the conversation goes on
prj = rf.open("project.rockface")
print(prj.chat(model=True).ask("How many samples have pyrite?").text)
print(rf.docs_search("micro-CT porosity", "en", n=3))
```

In a terminal: `rockface llm chat` (a conversation; `--project file.rockface` for the project's questions, `/new`
starts again) or `rockface llm chat --no-model how do I install a plug-in?` for one answer.

## Limits and common problems

* "This installation cannot run a language model by itself": an installation older than 1.0.0rc3 — install the
  current one, or choose a local server in **Language model…**.
* Slow answers: on the processor, the first words take from a few seconds to about half a minute, depending on the
  computer and on the length of the passages; choose **Qwen3 1.7B** in **Language model…** for faster answers, or a
  graphics card.
* The download fails behind a proxy: the download uses the system's proxy settings; download the GGUF file with the
  browser and choose it in **Language model… → A GGUF file on this computer**.
* An answer without sources: the guide has nothing on that, or the question is general (geology, small talk). Mio says
  when the guide does not answer; check what she says against the guide.
* A local model is smaller than the assistants on the internet: it can misread a question. The sources and the
  checked numbers are there to verify the answer.
* Mio does not change the project: her tools only read; suggestions are written only when you accept them.

## Coverage

Owner's request of 2026-11-15: Mio as a conversation in natural language, like the assistants based on language
models, answering from the user guides, the manuals and the website; the model local only, downloaded on first use
(ROADMAP 1.0.0rc3).
