# RockFace Suite — website and user guide

The public site of **RockFace Suite** (petrography from the thin section to the database: RockFace Petro, Atlas,
Explorer, Lab and MC, with RockFace AI and Mio), published with GitHub Pages at
<https://laribeirojr.github.io/rockface/>, in English (root), Portuguese (`pt-br/`) and Spanish (`es/`).

| Folder | What it holds |
|---|---|
| `site/` | The home page template (`index.html`), the partials, styles, script, fonts, logo and the PDF guides (`downloads/`) |
| `content/strings.toml` | The words of the home page, header, footer and guide pages in the three languages |
| `content/guide/` | The user guide: one Markdown page per function in `en/`, `pt/`, `es/`, and `contents.json` (parts and order) |
| `site/assets/guide/` | The screenshots of each guide page, per language, taken from the real program |
| `scripts/build_site.py` | Builds `_site/` and checks it (links, images and their sizes, no third-party resources, size budget, the same pages in every language) |
| `scripts/build_manual.py` | Builds the PDF guides from the same pages (pandoc + XeLaTeX) |

The guide pages, `contents.json`, the screenshots, the logo and the Open Graph image are **not edited here**: they come
from the RockFace source at each version (`tools/export_site.py` there, which also refuses any page with a
confidential name). Every example uses ILLUSTRATIVE data.

    python -m pip install -r requirements.txt
    python scripts/build_manual.py      # the three PDFs (needs pandoc, XeLaTeX, TeX Gyre Pagella, DejaVu, fontTools)
    python scripts/build_site.py        # build and check; --serve shows it on http://localhost:8000/

GitHub Pages must be enabled once in the repository settings with "Source: GitHub Actions"; the workflow
`.github/workflows/pages.yml` then builds and publishes the site at every push to `main`.

The testers' feedback form is set in `site.toml` (`feedback_url`); while it is empty the site says that the form is
being prepared.

Design adapted from [MDraft](https://bgeneto.github.io/MDraft/) (MIT, `LICENSE-MDraft.txt`), through the SciVelyx
Suite site. EB Garamond and IBM Plex Mono under the SIL Open Font License (`site/assets/fonts/`).
