#!/usr/bin/env python3
"""Build the PDF user guide of RockFace Suite from the same Markdown pages as the website.

    python scripts/build_manual.py            # the three languages → site/downloads/RockFace-User-Guide-<lang>.pdf
    python scripts/build_manual.py pt         # one language (en, pt, es)

Needs pandoc (≥ 2.19) and XeLaTeX with the KOMA-Script classes, TeX Gyre Pagella and DejaVu fonts. The parts and
chapters follow content/guide/contents.json; each page's screenshot follows its first paragraph; links between pages
become links inside the PDF. Adapted from the SciVelyx Suite manual builder.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
GUIDE = ROOT / "content" / "guide"
CONFIG = tomllib.loads((ROOT / "site.toml").read_text(encoding="utf-8"))
OUT = SITE / "downloads"

TEXT = {
    "en": {"lang": "en-GB", "subtitle": "User guide", "slogan": "From the thin section to the database.",
           "version": "Version", "contents": "Contents", "web": "",
           "intro": "Petro, Atlas, Explorer, Lab and MC, with RockFace AI and Mio. Every example uses ILLUSTRATIVE "
                    "data; every picture comes from the real program.",
           "site": "This guide is also on the web, where it is updated with each version:",
           "shot": "In the program:"},
    "pt": {"lang": "pt-BR", "subtitle": "Guia do usuário", "slogan": "Da lâmina ao banco de dados.",
           "version": "Versão", "contents": "Sumário", "web": "pt-br/",
           "intro": "Petro, Atlas, Explorer, Lab e MC, com o RockFace AI e a Mio. Todos os exemplos usam dados "
                    "ILUSTRATIVOS; todas as imagens vêm do programa real.",
           "site": "Este guia também está na internet, onde é atualizado a cada versão:",
           "shot": "No programa:"},
    "es": {"lang": "es-ES", "subtitle": "Guía del usuario", "slogan": "De la lámina a la base de datos.",
           "version": "Versión", "contents": "Índice", "web": "es/",
           "intro": "Petro, Atlas, Explorer, Lab y MC, con RockFace AI y Mio. Todos los ejemplos usan datos "
                    "ILUSTRATIVOS; todas las imágenes vienen del programa real.",
           "site": "Esta guía también está en internet, donde se actualiza con cada versión:",
           "shot": "En el programa:"},
}


def site_url() -> str:
    base = CONFIG["site"]["base_path"].strip("/")
    return CONFIG["site"]["origin"].rstrip("/") + "/" + (base + "/" if base else "")


def picture(lang: str, slug: str, tmp: Path) -> Path | None:
    f = SITE / "assets" / "guide" / lang / f"{slug}.webp"
    if not f.exists():
        return None
    jpg = tmp / f"{lang}-{slug}.jpg"
    im = Image.open(f).convert("RGB")
    if im.width > 1400:
        im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
    im.save(jpg, quality=82, optimize=True)
    return jpg


def chapter(lang: str, slug: str, text: str, tmp: Path, slugs: set) -> str:
    """One page of the guide → one chapter of the PDF."""
    lines = text.split("\n")
    title = lines[0][2:].strip()
    lines[0] = f"# {title} {{#ch-{slug}}}"
    text = "\n".join(lines)

    def link(m):
        label, target, frag = m.group(1), m.group(2), m.group(3) or ""
        return f"[{label}](#ch-{target})" if target in slugs else label
    text = re.sub(r"(?<!!)\[([^\]]+)\]\(([a-z0-9_]+)\.md(#[^)]*)?\)", link, text)
    # code blocks without a language are highlighted as shell, so that their long lines break like the others
    out, inside = [], False
    for ln in text.split("\n"):
        if ln.startswith("```"):
            if not inside and ln.strip() == "```":
                ln = "```bash"
            inside = not inside
        out.append(ln)
    text = "\n".join(out)
    pic = picture(lang, slug, tmp)
    if pic is not None:                 # after the first paragraph of the first section
        m = re.search(r"\n## [^\n]+\n\n.+?\n\n", text, re.S)
        fig = f"![{TEXT[lang]['shot']} {title}]({pic.as_posix()})\n\n"
        text = text[:m.end()] + fig + text[m.end():] if m else text + "\n\n" + fig
    return text


PREAMBLE = r"""
\usepackage{fontspec}
\setmainfont{TeX Gyre Pagella}
\setsansfont{DejaVu Sans}[Scale=0.9]
\setmonofont{DejaVu Sans Mono}[Scale=0.8]
\newfontfamily\fallbackfont{DejaVu Serif}[Scale=0.92]
\usepackage{newunicodechar}
FALLBACKS
\usepackage{xcolor}
\definecolor{svnavy}{HTML}{002050}
\definecolor{svcyan}{HTML}{0BBAF4}
\addtokomafont{disposition}{\color{svnavy}}
\addtokomafont{chapter}{\sffamily\bfseries}
\addtokomafont{part}{\sffamily\bfseries}
\usepackage{graphicx}
\setkeys{Gin}{width=\linewidth,height=0.42\textheight,keepaspectratio}
\usepackage{float}
\floatplacement{figure}{H}
\usepackage[font=small,labelformat=empty]{caption}
\usepackage{scrlayer-scrpage}
\pagestyle{scrheadings}
\clearpairofpagestyles
\ohead{\small\sffamily RockFace Suite}
\ihead{\small\sffamily\leftmark}
\ofoot*{\small\sffamily\pagemark}
\setlength{\emergencystretch}{3em}
\usepackage{etoolbox}
\AtBeginEnvironment{longtable}{\small}
\usepackage{fvextra}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,breakanywhere,commandchars=\\\{\},fontsize=\small}
"""

COVER = r"""
\begin{titlepage}
\centering
\vspace*{2.2cm}
\includegraphics[width=3.2cm]{@@LOGO@@}\par
\vspace{1.2cm}
{\fontsize{40}{46}\selectfont\color{svnavy} RockFace Suite\par}
\vspace{0.35cm}
{\Large\sffamily @@SUBTITLE@@\par}
\vspace{0.8cm}
{\large\itshape @@SLOGAN@@\par}
\vspace{0.4cm}
{\color{svcyan}\rule{6cm}{1.2pt}\par}
\vspace{1.4cm}
\begin{minipage}{0.78\textwidth}\centering\normalsize @@INTRO@@\end{minipage}
\vfill
{\sffamily @@VERSIONLABEL@@ @@VERSION@@ \textbullet{} @@DATE@@\par}
\vspace{0.3cm}
{\small @@SITETEXT@@\par\url{@@SITEURL@@}\par}
\end{titlepage}
"""


def fallbacks(text: str) -> str:
    """Characters that TeX Gyre Pagella lacks are printed with DejaVu Serif (XeLaTeX has no automatic fallback)."""
    from fontTools.ttLib import TTFont
    pag = subprocess.run(["kpsewhich", "texgyrepagella-regular.otf"], capture_output=True, text=True).stdout.strip()
    cmap = TTFont(pag).getBestCmap()
    skip = set("\\{}$&#^_%~")
    chars = sorted({c for c in text if ord(c) > 127 and ord(c) not in cmap and c not in skip})
    return "\n".join(f'\\newunicodechar{{{c}}}{{{{\\fallbackfont\\char"{ord(c):04X}\\relax}}}}' for c in chars)


def build(lang: str) -> Path:
    T = TEXT[lang]
    parts = json.loads((GUIDE / "contents.json").read_text(encoding="utf-8"))["parts"]
    slugs = {p for part in parts for p in part["pages"]}
    version = CONFIG["rockface"]["version"]
    tmp = Path(tempfile.mkdtemp(prefix="guide-"))
    chunks = []
    for part in parts:
        chunks.append("```{=latex}\n\\part{" + part["title"].get(lang, part["title"]["en"]) + "}\n```")
        for slug in part["pages"]:
            text = (GUIDE / lang / f"{slug}.md").read_text(encoding="utf-8")
            chunks.append(chapter(lang, slug, text, tmp, slugs))
    md = "\n\n".join(chunks)
    (tmp / "guide.md").write_text(md, encoding="utf-8")
    values = {"LOGO": (SITE / "assets" / "apple-touch-icon.png").as_posix(), "SUBTITLE": T["subtitle"],
              "SLOGAN": T["slogan"], "INTRO": T["intro"], "VERSIONLABEL": T["version"], "VERSION": version,
              "DATE": dt.date.today().isoformat(), "SITETEXT": T["site"], "SITEURL": site_url() + T["web"] + "guide/"}
    cover = re.sub(r"@@([A-Z]+)@@", lambda m: values[m.group(1)], COVER)
    pre = PREAMBLE.replace("FALLBACKS", fallbacks(md))
    (tmp / "preamble.tex").write_text(pre + "\\AtBeginDocument{\\hypersetup{pdftitle={RockFace Suite — "
                                      + T["subtitle"] + "}, pdfauthor={RockFace Suite}}}\n", encoding="utf-8")
    (tmp / "cover.tex").write_text(cover, encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    pdf = OUT / f"RockFace-User-Guide-{lang}.pdf"
    cmd = ["pandoc", str(tmp / "guide.md"), "-f", "markdown+raw_attribute", "-o", str(pdf),
           "--pdf-engine=xelatex", "--top-level-division=chapter", "--toc", "--toc-depth=1",
           "-V", "documentclass=scrreprt", "-V", "classoption=oneside", "-V", "papersize=a4", "-V", "fontsize=11pt",
           "-V", "geometry:margin=2.2cm", "-V", f"lang={T['lang']}", "-V", f"toc-title={T['contents']}",
           "-V", "colorlinks=true", "-V", "linkcolor=svnavy", "-V", "urlcolor=svnavy", "-V", "toccolor=black",
           "-M", "pagetitle=RockFace Suite", "--include-in-header", str(tmp / "preamble.tex"),
           "--include-before-body", str(tmp / "cover.tex"), "--highlight-style=tango",
           "-V", "microtypeoptions=protrusion=false"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-4000:])
        raise SystemExit(f"pandoc failed for {lang}")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"{pdf.relative_to(ROOT)}  {pdf.stat().st_size // 1024} kB")
    return pdf


if __name__ == "__main__":
    for lg in sys.argv[1:] or list(TEXT):
        build(lg)
