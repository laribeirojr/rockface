# Self-test of an installation

## What it is for

The self-test checks, in about a minute, that RockFace works on this computer: what depends on the computer rather
than on the program — its libraries, the reports in every format, the files, the figures, the image and volume
pipelines, the AI models, Mio and the five windows on the real screen. Run it after installing and whenever
something behaves strangely; its report is what the RockFace team asks for when you report a problem.

## Before you start

* Nothing to prepare. The self-test makes its own ILLUSTRATIVE data in a temporary folder and never opens, changes
  or saves your projects or your preferences.

## Step by step

1. In RockFace Petro: **Help → Run the self-test…**.
2. The window lists each check as it ends. The five programs open and close by themselves: do not click them.
3. At the end, **Open the report** shows `report.html` in the browser, with the pictures it made; **Open the
   folder** shows the folder with `report.html`, `report.json` and `selftest.zip`.
4. If a check failed, send `selftest.zip` with your report (see [Sending your opinion](feedback.md)).

## Options

| Where | What it does |
|---|---|
| `rockface selftest` | The same checks from a terminal, without the windows |
| `--gui` | Also opens and photographs the five windows (Help → Run the self-test… does it) |
| `--quick` | Only the HTML report among the report formats |
| `-o FOLDER` | The folder of the report (default: a new temporary folder) |
| `--open` | Opens `report.html` when done |

## How it works

| Part | What is checked |
|---|---|
| Installation | Version, system, edition (with or without AI), the licence files |
| Numerics | numpy, SciPy, scikit-image and scikit-learn, with a threshold of known answer |
| Projects | The ILLUSTRATIVE example project written, closed and opened again; totals and the Folk (1980) classification |
| Reports | The report of a description in HTML, Word, Excel and PDF |
| Exchange | The descriptions exported to a `.rfx` file and imported into a new project |
| Figures | A ternary diagram |
| Images | A synthetic thin section with blue resin of known porosity: filter and segmentation; the porosity found must be within 3 points of the porosity drawn |
| Volumes | A synthetic micro-CT volume of known porosity: import and Otsu segmentation, within 2 points |
| AI | The shipped thin-section model applied to the synthetic section (AI edition; "not applicable" in the other), the device and whether training is available |
| Mio | A question in plain language read by the rules |
| Server | The PostgreSQL driver of server mode |
| Interface | The five windows, the screen size and scale |

Each check is independent: one failure never stops the others. A check that does not apply to the installation
(the AI models in the edition without AI) is marked "not applicable", not failed.

## From a script

```python
import rockface.api as rf

res = rf.selftest(gui=False, quick=True)
print(res["summary"], res["folder"])     # {'passed': 13, 'skipped': 0, 'failed': 0} and the folder of report.html
```

## Limits and common problems

* **The windows check on a computer without a screen.** Run `rockface selftest` without `--gui`, or set
  `QT_QPA_PLATFORM=offscreen`.
* **It takes longer the first time.** The operating system and the antivirus check the program's files on the first
  start.

## Coverage

1.0 (self-test of the installation; ROADMAP).
