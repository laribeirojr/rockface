#!/usr/bin/env python3
"""Assemble the RockFace Suite website into ``_site/`` and check it.

The home page is ``site/index.html`` filled with the texts of ``content/strings.toml`` in English (at the root),
Portuguese (``pt-br/``) and Spanish (``es/``). The user guide is Markdown in ``content/guide/<en|pt|es>/``, in the
order and parts of ``content/guide/contents.json``, with the screenshots of ``site/assets/guide/<lang>/``; both come
from the RockFace source (``tools/export_site.py`` there) and are not edited here.

The build fails on a broken local link, a missing image, an image whose width/height attributes do not match the
file, invalid JSON-LD, a third-party resource, a page above the size budget, a guide page missing in a language, or
a word of the confidentiality list (``scripts/banned.txt``, if present, one regular expression per line).

    python scripts/build_site.py            # build and check
    python scripts/build_site.py --serve    # … then serve _site/ on http://localhost:8000/

Environment (optional outside CI):
    SITE_ORIGIN     https://laribeirojr.github.io
    SITE_BASE_PATH  /rockface   (empty for a custom domain)

Design adapted from MDraft (MIT, LICENSE-MDraft.txt), through the SciVelyx Suite site.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import os
import re
import shutil
import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path

import markdown
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
CONTENT = ROOT / "content"
GUIDE = CONTENT / "guide"
OUT = ROOT / "_site"
CONFIG = tomllib.loads((ROOT / "site.toml").read_text(encoding="utf-8"))
STRINGS = tomllib.loads((CONTENT / "strings.toml").read_text(encoding="utf-8"))

ORIGIN = os.environ.get("SITE_ORIGIN", CONFIG["site"]["origin"]).rstrip("/")
BASE = os.environ.get("SITE_BASE_PATH", CONFIG["site"]["base_path"]).strip()
BASE = "" if BASE in ("", "/") else "/" + BASE.strip("/")
SITE_URL = f"{ORIGIN}{BASE}/"
PAGE_BUDGET = 450_000            # bytes of HTML + CSS + JS + images referenced by one page (lazy images excluded)
VERSION = CONFIG["rockface"]["version"]
FEEDBACK_URL = CONFIG["rockface"].get("feedback_url", "").strip()

# site language → (URL prefix, html lang, og locale, guide folder)
LANGS = {
    "en": ("", "en", "en_US", "en"),
    "pt-br": ("pt-br/", "pt-BR", "pt_BR", "pt"),
    "es": ("es/", "es", "es_ES", "es"),
}

failures: list[str] = []


def check(ok: bool, msg: str, quiet: bool = False) -> bool:
    if not ok or not quiet:
        print(("  PASS  " if ok else "  FAIL  ") + msg)
    if not ok:
        failures.append(msg)
    return ok


def pdf_name(lang: str) -> str:
    return f"RockFace-User-Guide-{lang}.pdf"


def partial(name: str) -> str:
    return (SITE / "_partials" / f"{name}.html").read_text(encoding="utf-8")


def fill(text: str, values: dict) -> str:
    """{{> partial}} includes, then {{KEY}} values (repeated until stable, so partials may use values)."""
    for _ in range(5):
        text = re.sub(r"\{\{>\s*([\w-]+)\s*\}\}", lambda m: partial(m.group(1)), text)
        new = re.sub(r"\{\{([A-Z_0-9]+)\}\}", lambda m: str(values.get(m.group(1), m.group(0))), text)
        if new == text:
            break
        text = new
    left = sorted(set(re.findall(r"\{\{[^}]+\}\}", text)))
    check(not left, f"no unfilled placeholder {left}" if left else "placeholders filled", quiet=not left)
    return text


def common_values(lang: str, rel_root: str, url_path: str, title: str, description: str, nav: str,
                  aroot: str) -> dict:
    """``rel_root``: from the page to the root of its language; ``aroot``: to the site root (assets)."""
    prefix, html_lang, locale, glang = LANGS[lang]
    S = STRINGS[lang]
    return {
        **{k: v for k, v in S.items() if isinstance(v, str)},
        "AROOT": aroot, "ROOT": rel_root, "HTML_LANG": html_lang, "OG_LOCALE": locale, "IMG_LANG": glang,
        "GUIDE_PDF": pdf_name(glang), "VERSION": VERSION,
        "URL_EN": (aroot + url_path) or "./", "URL_PT": aroot + "pt-br/" + url_path, "URL_ES": aroot + "es/" + url_path,
        "CUR_EN": str(lang == "en").lower(), "CUR_PT": str(lang == "pt-br").lower(),
        "CUR_ES": str(lang == "es").lower(),
        "ABS_EN": SITE_URL + url_path, "ABS_PT": SITE_URL + "pt-br/" + url_path, "ABS_ES": SITE_URL + "es/" + url_path,
        "SITE_URL": SITE_URL, "CANONICAL": SITE_URL + prefix + url_path,
        "TITLE": html.escape(title), "DESCRIPTION": html.escape(description),
        "OG_IMAGE": SITE_URL + "assets/og.png", "YEAR": str(_dt.date.today().year), "NAV": nav,
    }


def nav_links(items) -> str:
    return "\n".join(f'          <a href="{href}">{html.escape(label)}</a>' for label, href in items)


# ------------------------------------------------------------------ the guide
def contents() -> list[dict]:
    return json.loads((GUIDE / "contents.json").read_text(encoding="utf-8"))["parts"]


def guide_pages(glang: str) -> list[dict]:
    """The pages of one language in the order of contents.json, each with its part."""
    out = []
    for part in contents():
        for slug in part["pages"]:
            src = GUIDE / glang / f"{slug}.md"
            if not check(src.exists(), f"{glang}: guide page {slug}.md exists", quiet=True):
                src = GUIDE / "en" / f"{slug}.md"
            text = src.read_text(encoding="utf-8")
            m = re.match(r"^# (.+)$", text, re.M)
            out.append({"slug": slug, "title": m.group(1).strip() if m else slug, "text": text,
                        "part": part["title"].get(glang, part["title"]["en"])})
    return out


def doc_nav(items, current: str, rel_root: str) -> str:
    """The parts of the guide, each with its pages."""
    out, part = [], None
    for g in items:
        if g["part"] != part:
            if part is not None:
                out.append("        </ol>")
            part = g["part"]
            out.append(f"        <h3>{html.escape(part)}</h3>\n        <ol class=\"part\">")
        cur = ' aria-current="page"' if g["slug"] == current else ""
        out.append(f'          <li><a href="{rel_root}guide/{g["slug"]}/"{cur}>{html.escape(g["title"])}</a></li>')
    out.append("        </ol>")
    return "\n".join(out)


def shot_html(glang: str, slug: str, title: str, aroot: str, lang: str) -> str:
    f = SITE / "assets" / "guide" / glang / f"{slug}.webp"
    if not f.exists():
        return ""
    with Image.open(f) as pic:
        w, h = pic.size
    src = f"{aroot}assets/guide/{glang}/{slug}.webp"
    S = STRINGS[lang]
    alt = html.escape(f"{S['T_SCREENSHOT']}: {title}")
    cap = html.escape(title)
    return (f'<figure class="manual-figure"><a class="shot" href="{src}" data-full="{src}" data-caption="{cap}" '
            f'data-gallery="guide"><img src="{src}" width="{w}" height="{h}" loading="lazy" decoding="async" '
            f'alt="{alt}" /></a><figcaption>{S["T_IN_PROGRAM"]} {cap}</figcaption></figure>')


def nested_lists(text: str) -> str:
    """The guide is CommonMark (sub-items indented by 2–3 spaces); Python-Markdown wants 4 for a nested list."""
    out, in_list, fence = [], False, False
    for ln in text.split("\n"):
        if ln.startswith("```"):
            fence = not fence
        if not fence:
            m = re.match(r"^( {1,3})([*+-]|\d+\.) ", ln)
            if m and in_list:
                ln = "    " + ln[len(m.group(1)):]
            if re.match(r"^([*+-]|\d+\.) ", ln):
                in_list = True
            elif not ln.strip():
                pass
            elif not ln.startswith(" "):
                in_list = False
        out.append(ln)
    return "\n".join(out)


def render_guide(g: dict, items: list, k: int, lang: str) -> tuple[str, str]:
    prefix, _, _, glang = LANGS[lang]
    rel = "../../"
    aroot = rel + ("../" if lang != "en" else "")
    url = f"guide/{g['slug']}/"
    text = nested_lists(g["text"])
    text = re.sub(r"\]\(([a-z0-9_]+)\.md(#[^)]*)?\)", lambda m: f"](../{m.group(1)}/{m.group(2) or ''})", text)
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "attr_list", "sane_lists"],
                           extension_configs={"toc": {"permalink": False}})
    body = md.convert(text)
    fig = shot_html(glang, g["slug"], g["title"], aroot, lang)
    if fig:                        # the picture after the first paragraph of "What it is for"
        m = re.search(r"</h2>\s*<p>.*?</p>", body, re.S)
        body = body[:m.end()] + "\n" + fig + body[m.end():] if m else fig + body
    first = re.search(r"\n## [^\n]+\n\n(.+?)(\n\n|$)", g["text"], re.S)
    desc = re.sub(r"\s+", " ", re.sub(r"[*`]|\[([^\]]*)\]\([^)]*\)", r"\1", first.group(1)))[:180] if first else ""
    prev_ = items[k - 1] if k > 0 else None
    next_ = items[k + 1] if k + 1 < len(items) else None
    S = STRINGS[lang]

    def link(it, label):
        if it is None:
            return "<span></span>"
        return f'<a class="text-link" href="{rel}guide/{it["slug"]}/">{label}: {html.escape(it["title"])}</a>'
    nav = nav_links([(lbl, rel + h) for lbl, h in S["NAV"]])
    page = fill(partial("doc"), {
        **common_values(lang, rel, url, f"{g['title']} — {S['T_GUIDE']} · RockFace", desc, nav, aroot),
        "DOC_NAV": doc_nav(items, g["slug"], rel), "DOC_BODY": body,
        "DOC_PAGER": link(prev_, S["T_PREV"]) + link(next_, S["T_NEXT"])})
    return prefix + url + "index.html", page


def render_guide_index(items: list, lang: str) -> tuple[str, str]:
    prefix, _, _, glang = LANGS[lang]
    rel = "../"
    aroot = rel + ("../" if lang != "en" else "")
    S = STRINGS[lang]
    parts, part = [], None
    for g in items:
        if g["part"] != part:
            if part is not None:
                parts.append("</ol></section>")
            part = g["part"]
            parts.append(f'<section class="guide-part"><h2>{html.escape(part)}</h2><ol>')
        parts.append(f'<li><a href="{rel}guide/{g["slug"]}/">{html.escape(g["title"])}</a></li>')
    parts.append("</ol></section>")
    body = (f"<h1>{html.escape(S['T_GUIDE'])} — RockFace {VERSION}</h1>\n<p class=\"lead\">{html.escape(S['T_GUIDE_INTRO'])}"
            f"</p>\n<p><a class=\"btn btn-ghost\" href=\"{aroot}downloads/{pdf_name(glang)}\">{S['T_GUIDE_PDF']}</a></p>\n"
            f'<div class="guide-parts">{"".join(parts)}</div>')
    nav = nav_links([(lbl, rel + h) for lbl, h in S["NAV"]])
    page = fill(partial("doc"), {
        **common_values(lang, rel, "guide/", f"{S['T_GUIDE']} — RockFace Suite", S["T_GUIDE_INTRO"][:180], nav,
                        aroot),
        "DOC_NAV": doc_nav(items, "", rel), "DOC_BODY": body, "DOC_PAGER": "<span></span>"})
    return prefix + "guide/index.html", page


# ------------------------------------------------------------------ checks
class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.imgs, self.scripts, self.jsonld, self._json = [], [], [], [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.refs.append(a["href"])
        if tag == "link" and a.get("href") and a.get("rel") not in ("canonical", "alternate"):
            self.refs.append(a["href"])
            if a.get("rel") == "stylesheet" and a["href"].startswith("http"):
                self.scripts.append(a["href"])
        if tag == "img":
            self.imgs.append(a)
            if a.get("src"):
                self.refs.append(a["src"])
        if tag == "script":
            if a.get("src"):
                self.refs.append(a["src"])
                if a["src"].startswith("http"):
                    self.scripts.append(a["src"])
            if a.get("type") == "application/ld+json":
                self._json = []

    def handle_data(self, data):
        if self._json is not None:
            self._json.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._json is not None:
            self.jsonld.append("".join(self._json))
            self._json = None


def validate(pages: dict[str, str]) -> None:
    ids = {rel: set(re.findall(r'\sid="([^"]+)"', text)) for rel, text in pages.items()}
    n_ok = 0
    for rel, text in pages.items():
        s = Scan()
        s.feed(text)
        here = (OUT / rel).parent
        broken = []
        for ref in s.refs:
            if not ref or ref.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, frag = ref.partition("#")
            path = path.split("?")[0]
            if not path:
                if frag and frag not in ids[rel]:
                    broken.append(ref)
                continue
            target = (here / path).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                broken.append(ref)
            elif frag:
                key = str(target.relative_to(OUT.resolve()))
                if key in ids and frag not in ids[key]:
                    broken.append(ref)
        ok1 = check(not broken, f"{rel}: local links resolve" + (f" — broken {broken}" if broken else ""), quiet=True)
        bad = []
        size = len(text.encode())
        for im in s.imgs:
            src = im.get("src", "")
            if not src:
                continue
            if src.startswith("http"):
                bad.append(f"{src} (remote)")
                continue
            f = (here / src.split("?")[0]).resolve()
            if not f.exists():
                continue
            if im.get("loading") != "lazy":
                size += f.stat().st_size
            if "width" not in im or "height" not in im:
                bad.append(f"{src} without width/height")
                continue
            with Image.open(f) as pic:
                if (int(im["width"]), int(im["height"])) != pic.size:
                    bad.append(f"{src} is {pic.size}, attributes say {im['width']}×{im['height']}")
            if "alt" not in im:
                bad.append(f"{src} without alt")
        ok2 = check(not bad, f"{rel}: images exist with true sizes and alt text" + (f" — {bad}" if bad else ""),
                    quiet=True)
        ok3 = check(not s.scripts, f"{rel}: no third-party script or stylesheet {s.scripts}", quiet=True)
        ok4 = True
        for block in s.jsonld:
            try:
                json.loads(block)
            except json.JSONDecodeError:
                ok4 = check(False, f"{rel}: JSON-LD is valid JSON")
        for asset in ("styles.css", "site.js"):
            if asset in text:
                size += (OUT / asset).stat().st_size
        ok5 = check(size <= PAGE_BUDGET, f"{rel}: {size / 1000:.0f} kB within the {PAGE_BUDGET // 1000} kB budget",
                    quiet=True)
        n_ok += all((ok1, ok2, ok3, ok4, ok5))
    check(n_ok == len(pages), f"{n_ok} of {len(pages)} pages: links, images, scripts, JSON-LD and size budget")


def confidentiality(pages: dict[str, str]) -> None:
    """Nothing of the confidential lists ever goes into the public site."""
    banned = ROOT / "scripts" / "banned.txt"
    pats = [ln.strip() for ln in banned.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.startswith("#")] if banned.exists() else []
    rx = re.compile("|".join(pats), re.I) if pats else None
    hits = []
    if rx:
        for rel, text in pages.items():
            plain = re.sub(r"<[^>]+>", " ", text)
            if rx.search(plain):
                hits.append(f"{rel}: {rx.search(plain).group(0)}")
        for md in GUIDE.rglob("*.md"):
            m = rx.search(md.read_text(encoding="utf-8"))
            if m:
                hits.append(f"{md.relative_to(ROOT)}: {m.group(0)}")
    check(not hits, f"confidentiality list: {len(pats)} patterns, no page matches" + (f" — {hits}" if hits else ""))


def same_pages() -> None:
    names = {g: sorted(p.stem for p in (GUIDE / g).glob("*.md")) for _, _, _, g in LANGS.values()}
    listed = sorted(p for part in contents() for p in part["pages"])
    check(all(n == listed for n in names.values()),
          f"every guide page in the three languages and in contents.json ({len(listed)} pages)")


# ------------------------------------------------------------------ build
def feedback_block(lang: str) -> str:
    S = STRINGS[lang]
    if FEEDBACK_URL:
        return (f'          <div class="actions"><a class="btn btn-primary" href="{html.escape(FEEDBACK_URL)}">'
                f'{S["H_FB_BUTTON"]}</a></div>\n          <p class="fineprint">{S["H_FB_INPROGRAM"]}</p>')
    return f'          <p class="notice">{S["H_FB_PENDING"]}</p>'


def build() -> int:
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir()
    for item in SITE.iterdir():
        if item.name.startswith("_") or item.suffix == ".html":
            continue
        (shutil.copytree if item.is_dir() else shutil.copy2)(item, OUT / item.name)
    shutil.copy2(ROOT / "LICENSE-MDraft.txt", OUT / "assets" / "LICENSE-MDraft.txt")
    same_pages()
    pages: dict[str, str] = {}
    n_pages = len([p for part in contents() for p in part["pages"]])
    home_title = {"en": ("RockFace Suite — petrography from the thin section to the database",
                         "RockFace Suite: description, images, queries, image analysis and micro-CT of sedimentary "
                         "rocks, in five programs that share one project. User guide in English, Portuguese and "
                         "Spanish."),
                  "pt-br": ("RockFace Suite — petrografia da lâmina ao banco de dados",
                            "RockFace Suite: descrição, imagens, consultas, análise de imagens e micro-CT de rochas "
                            "sedimentares, em cinco programas que compartilham um projeto. Guia em inglês, "
                            "português e espanhol."),
                  "es": ("RockFace Suite — petrografía de la lámina a la base de datos",
                         "RockFace Suite: descripción, imágenes, consultas, análisis de imágenes y micro-CT de rocas "
                         "sedimentarias, en cinco programas que comparten un proyecto. Guía en inglés, portugués y "
                         "español.")}
    for lang, (prefix, *_r) in LANGS.items():
        S = STRINGS[lang]
        aroot = "./" if lang == "en" else "../"
        vals = common_values(lang, "./" if lang == "en" else "./", "", *home_title[lang],
                             nav_links([(lbl, h) for lbl, h in S["NAV"]]), aroot)
        vals.update({"FEEDBACK_BLOCK": feedback_block(lang), "PAGES": str(n_pages)})
        for key, name in (("HERO", "atlas_viewer"), ("DASH", "explorer_dashboard")):
            with Image.open(SITE / "assets" / "guide" / LANGS[lang][3] / f"{name}.webp") as pic:
                vals[f"{key}_W"], vals[f"{key}_H"] = pic.size
        if lang == "en":
            vals["URL_EN"] = "./"
        pages[prefix + "index.html"] = fill((SITE / "index.html").read_text(encoding="utf-8"), vals)
        items = guide_pages(LANGS[lang][3])
        dst, text = render_guide_index(items, lang)
        pages[dst] = text
        for k, g in enumerate(items):
            dst, text = render_guide(g, items, k, lang)
            pages[dst] = text
    # 404: served from any depth, so absolute paths under the base
    S = STRINGS["en"]
    r = f"{BASE}/"
    vals = common_values("en", r, "404.html", "Page not found — RockFace Suite", "This page does not exist.",
                         nav_links([(lbl, r + h) for lbl, h in S["NAV"]]), r)
    pages["404.html"] = fill((SITE / "404.html").read_text(encoding="utf-8"), vals)
    for dst, text in pages.items():
        (OUT / dst).parent.mkdir(parents=True, exist_ok=True)
        (OUT / dst).write_text(text, encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n")
    urls = [SITE_URL + d.removesuffix("index.html") for d in pages if d != "404.html"]
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{html.escape(u)}</loc></url>\n" for u in urls) + "</urlset>\n")
    print(f"Built {len(pages)} pages into {OUT.relative_to(ROOT)}/ for {SITE_URL}")
    for _, _, _, g in LANGS.values():
        check((OUT / "downloads" / pdf_name(g)).exists(), f"downloads/{pdf_name(g)} exists")
    validate({k: v for k, v in pages.items() if k != "404.html"})
    confidentiality(pages)
    if failures:
        print(f"\n{len(failures)} check(s) failed")
        return 1
    print("\nall checks passed")
    return 0


def serve() -> None:
    import functools
    import http.server
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
    print("Serving _site/ on http://localhost:8000/ (Ctrl+C stops)")
    http.server.ThreadingHTTPServer(("", 8000), handler).serve_forever()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true")
    args = ap.parse_args()
    code = build()
    if args.serve and code == 0:
        serve()
    sys.exit(code)
