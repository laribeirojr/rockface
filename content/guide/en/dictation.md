# Dictation at the microscope

## What it is for

At the microscope the eyes are on the eyepieces and the hands on the stage. With dictation the petrographer speaks
instead of typing: the **description fields** ("moderately sorted, subrounded, primary intergranular porosity 12
percent, concavo-convex contacts") and the **point count** ("monocrystalline quartz", "three", "undo"). Speech is
recognised **on this computer** — the audio is neither kept nor sent anywhere — and nothing is written before the
petrographer sees what was understood.

![The Dictate window with the words heard and the proposals read from them](../img/en/dictation.webp)

## Before you start

* Install the voice libraries once: `pip install rockface[voice]` (whisper.cpp, Vosk and the microphone library;
  all MIT or Apache-2.0).
* Open **Dictate → Voice models…** and download:
  * **Whisper base** (142 MB) for dictating descriptions — or *Whisper small* (466 MB) with 8 GB of memory, or
    *Whisper large-v3 turbo* (547 MB) with an NVIDIA RTX card and a CUDA build of pywhispercpp;
  * the **Vosk small** model of your language (31–40 MB) for counting by voice.
* Choose the microphone in the same window. A headset microphone keeps the noise of the room out.

## Step by step

**Dictating the description**

1. Open a description and click **Dictate** (Home tab).
2. Click **Listen** and speak. Pause after each phrase: every pause sends what you said, and it appears in the text
   box. You can also type or paste the words and click **Interpret**.
3. Read the table: each proposal shows the field, the value, the % or mm, and **the words it came from**.
   * A word that fits several types (*intergranular*: primary or secondary?) comes **unticked** with a list to
     choose from.
   * A negated phrase (*no fractures*, *sem cimento*, *sin porosidad móldica*) is shown as **said absent** and never
     adds anything.
   * Saying a field twice keeps the last one: "well sorted… no, moderately sorted" gives *moderately sorted*.
4. Tick what is right and click **Apply the ticked ones**. The values go to the Microscopic and Pore system tabs;
   **save the description** to keep them (the usual checks run then).
5. What was not understood can go to the notes of the microscopic description (tick the box below the table).

**Counting by voice**

1. In the **Count** tab, make the grid as usual and click **Count by voice**.
2. At each point say the constituent's name (*monocrystalline quartz*), part of it when only one line has it
   (*feldspar*), or the number of its keyboard shortcut (*three*, *number three*).
3. Commands: **undo**, **back**, **skip**, **stop** (*desfazer, voltar, pular, parar*; *deshacer, volver, saltar,
   detener*).
4. The line under the button says what was heard and what was done. A word not understood, or one that fits two
   lines (*quartz* with mono- and polycrystalline quartz), counts nothing: the program beeps and you say it again.
5. **The stage is never moved by voice**: move it with the keyboard, the controller or by hand.

**Asking Mio**

* The microphone button next to Mio's question box listens for one question and puts it in the box; read it and
  send it.
* *"Note: moderately sorted, porosity 12 percent"* (*anote:*, *dicta:*) makes Mio read the fields from the words —
  she only shows them; the Dictate window writes them.

## Fields understood

| Field | Examples |
|---|---|
| Sorting | *well sorted*, *moderately sorted*, *bem selecionado*, *seleção moderada*, *mal seleccionado* |
| Roundness and its modifiers | *subrounded*, *angular*, *subarredondado*, *embayed grains* |
| Sphericity | *high sphericity*, *esfericidade baixa*, *elongate* |
| Main grain-size mode | *medium sand*, *areia fina*, *main mode 0.25 mm*, *moda principal zero vírgula dois cinco milímetros* |
| Fabric | *grain supported*, *matrix supported*, *imbricated* |
| Intergranular contacts (with %) | *concavo-convex contacts 40 percent*, *contatos suturados*, *point contacts* |
| Total visual porosity | *total porosity 18 percent*, *porosidade 12 %*, *no visible porosity* (0 %) |
| Pore types (with %) | *primary intergranular 12*, *moldic porosity 3 percent*, *microporosity*, *vugs* |

Numbers may be digits or words in the three languages (*twenty five*, *vinte e cinco*, *veinticinco*;
*zero point two five*).

## How it works

* **Two recognisers, both local.** Whisper (whisper.cpp, MIT) writes free dictation and is steered toward the
  petrographic vocabulary by a short prompt with the description terms and the constituents of the composition
  (contextual biasing, Lall & Liu 2024). Vosk (Apache-2.0) recognises the closed vocabulary of counting — the lines,
  the numbers and the commands — at once, so a word outside it is refused rather than guessed.
* **Only speech is heard.** The sound is cut into utterances by its loudness (a pause of 0.6 s ends one), so the
  recogniser never hears silence: Whisper invents phrases on silence (*Careless Whisper*, Koenecke et al. 2024).
  Known invented phrases ("thanks for watching", "obrigado por assistir") and phrases repeated in a loop are removed.
* **Every proposal shows its words.** Speech recognition errors read well, and dropping or adding a "no" is the
  classic one (Basma et al. 2011): hence the words heard, the unticked ambiguous types and the negations that never
  become presences.
* **The vocabulary is the knowledge base's**: the labels of the terms and scales in English, Spanish and Portuguese,
  with the genders and plurals of Portuguese and Spanish (*selecionado/selecionada*).

## From a script

```python
d = prj["ILL-TS-001"]
r = d.dictate("subangular, sutured contacts", "en")                 # proposals only
[(p["target"], p["code"], p["value"]) for p in r["proposals"]]
d.dictate("subangular, sutured contacts", "en", apply=True)         # written and saved (the usual checks)
prj["ILL-TS-002"].voice_count("three", "en")                         # {"kind": "count", "slot": 3, ...}
rf.dictation("bem selecionado, porosidade 12 %", "pt")               # without a project
rf.speech_models(); rf.speech_status()
rf.transcribe("note.wav", "pt")                                      # a 16-bit WAV file, recognised locally
```

## Limits and common problems

* **No microphone found**: install `rockface[voice]` (sounddevice brings PortAudio) and check the system's input
  device; choose it in *Voice models…*.
* Whisper base on an old processor takes a second or two per phrase; short phrases with pauses work best. With an
  RTX card, *large-v3 turbo* is both faster and more accurate.
* Free dictation understands the fields above; the composition is counted by voice, not dictated as percentages.
* The small Vosk Portuguese model is weak at free speech (about 33 % word errors on Common Voice) but reliable on the
  closed vocabulary of counting, which is what it is used for.
* Some Vosk models are AGPL or non-commercial; only the Apache-2.0 ones are offered.

## Coverage

O8 (the owner's request of 2026-11-17: the innovations, the third one).

References: Radford et al. (2023), Whisper, PMLR 202; Koenecke et al. (2024), https://doi.org/10.1145/3630106.3658996;
Basma et al. (2011), https://doi.org/10.2214/AJR.11.6691; Lall & Liu (2024), arXiv:2410.18363; Povey et al. (2011),
Kaldi; Al-Dhubaib et al. (2008), US 7,319,961 (voice capture of petrographic data and point counts; expired).
