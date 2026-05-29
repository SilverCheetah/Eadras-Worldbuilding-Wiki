#!/usr/bin/env python3
"""Generate wiki/ai-index.md — an AI navigation index for the Eadras wiki.

The GitHub archive serves wiki pages with Obsidian [[wikilinks]] intact, which
GitHub renders as dead literal text. This script produces ONE committed file,
wiki/ai-index.md, that an AI agent (or human) can land on and navigate from:

  - It takes your curated wiki/index.md and rewrites every [[wikilink]] into a
    real, absolute GitHub URL, preserving all your categories and descriptions.
  - It appends a "Complete page manifest": every canon page name -> URL, so any
    [[name]] reference an agent meets mid-page resolves by lookup.

Design decisions to match the repo's governance (CLAUDE.md / system-governance):
  - SOURCE IS NEVER MODIFIED. Only wiki/ai-index.md is written.
  - _sealed/ is excluded (one-way-linking rule); templates/ and log.md too,
    mirroring bundle_for_ai.py's exclusions.
  - Links are ABSOLUTE blob URLs, so the file is robust to being moved/viewed
    anywhere (blob view, raw, API, pasted into chat).
  - Wikilink parsing uses a BOUNDED regex (character classes that cannot match
    ']'), so there is no runaway-expansion risk — in the spirit of the no-`sed`
    / no-regex-runaway rule, while still handling alias/heading forms cleanly.

Usage:
    python make_ai_index.py [--dry-run]

Run it after editing index.md (or on each push). It prints a ready-to-paste
log.md entry; per governance, append that to the TOP of wiki/log.md.
"""

import os
import re
import sys
import urllib.parse
from collections import defaultdict
from datetime import date
from pathlib import Path

# --- Repo coordinates (edit if the repo is renamed/moved) -------------------
GH_USER   = "SilverCheetah"
GH_REPO   = "Eadras-Worldbuilding-Wiki"
GH_BRANCH = "main"

ROOT     = Path(__file__).resolve().parent
WIKI     = ROOT / "wiki"
INDEX    = WIKI / "index.md"
OUTPUT   = WIKI / "ai-index.md"

BLOB_BASE = f"https://github.com/{GH_USER}/{GH_REPO}/blob/{GH_BRANCH}/wiki"

# Excluded from being linkable targets AND from the manifest.
EXCLUDE_DIRS  = {"_sealed", "templates"}          # sealed = one-way only
EXCLUDE_FILES = {"log.md", "ai-index.md"}          # log = not canon; don't self-list

# Bounded wikilink matcher: target/alias char classes forbid ']' '|' '#',
# so the match can never run past a single link. Handles:
#   [[t]] [[t|a]] [[t#h]] [[t#h|a]] [[t#^block]] and the ![[...]] embed form.
WIKILINK = re.compile(
    r"!?\[\["
    r"(?P<target>[^\]\|#]+)"
    r"(?P<sub>#\^?[^\]\|]+)?"
    r"(?:\|(?P<alias>[^\]]+))?"
    r"\]\]"
)


def gh_url(rel_within_wiki: str, anchor: str = "") -> str:
    parts = rel_within_wiki.replace("\\", "/").split("/")
    enc = "/".join(urllib.parse.quote(p) for p in parts)
    return f"{BLOB_BASE}/{enc}{anchor}"


def heading_anchor(heading: str) -> str:
    """GitHub heading anchor: lowercase, drop punctuation, spaces->hyphens."""
    h = heading.strip().lower()
    h = re.sub(r"[^\w\s-]", "", h)
    h = re.sub(r"\s+", "-", h)
    return "#" + h if h else ""


def build_page_index():
    """Return (by_key, all_pages, ambiguous).

    by_key maps a lowercased lookup key -> wiki-relative posix path.
    Keys: bare filename stem, and full relative path without extension.
    all_pages: sorted list of (display_name, rel_path) for the manifest.
    ambiguous: dict of stem -> [paths] where a bare name is non-unique.
    """
    by_key = {}
    stem_hits = defaultdict(list)
    all_pages = []

    for dirpath, dirnames, filenames in os.walk(WIKI):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            if not fn.endswith(".md") or fn in EXCLUDE_FILES:
                continue
            rel = Path(dirpath, fn).relative_to(WIKI).as_posix()
            stem = Path(fn).stem
            relnoext = rel[:-3]  # strip ".md"
            stem_hits[stem.lower()].append(rel)
            by_key[relnoext.lower()] = rel          # path-style key (unique)
            all_pages.append((stem, rel))

    # Bare-stem keys: register; first sorted path wins on collision.
    ambiguous = {}
    for stem_l, hits in stem_hits.items():
        hits_sorted = sorted(hits)
        by_key.setdefault(stem_l, hits_sorted[0])
        if len(hits) > 1:
            ambiguous[stem_l] = hits_sorted

    all_pages.sort(key=lambda t: t[0].lower())
    return by_key, all_pages, ambiguous


def resolve(target: str, by_key: dict):
    t = target.strip()
    if t.lower().endswith(".md"):
        t = t[:-3]
    return by_key.get(t.lower()) or by_key.get(Path(t).name.lower())


def strip_frontmatter(text: str) -> str:
    text = text.lstrip("\ufeff")  # BOM
    if text.lstrip().startswith("---"):
        body = text.lstrip()
        end = body.find("\n---", 3)
        if end != -1:
            nl = body.find("\n", end + 1)
            return body[nl + 1:] if nl != -1 else ""
    return text


def convert_links(text: str, by_key: dict, report: dict) -> str:
    def repl(m):
        target = m.group("target")
        sub = m.group("sub")
        alias = m.group("alias")
        rel = resolve(target, by_key)

        anchor, head_label = "", ""
        if sub:
            if sub.startswith("#^"):
                report["blockrefs"] += 1          # block refs have no GH anchor
            else:
                head_label = f" › {sub[1:].strip()}"
                anchor = heading_anchor(sub[1:])

        label = (alias or (target.strip() + head_label)).strip()

        if rel is None:
            report["unresolved"].append(target.strip())
            return label                           # readable text, never a dead [[...]]
        report["converted"] += 1
        return f"[{label}]({gh_url(rel, anchor)})"

    return WIKILINK.sub(repl, text)


ORIENTATION = (
    "> **For AI agents and external readers.** This is a generated navigation "
    "index for the Eadras worldbuilding wiki. The source pages use Obsidian "
    "`[[wikilinks]]`, which GitHub does not render as clickable links — so every "
    "link below is a direct GitHub URL instead. To follow a `[[name]]` reference "
    "you find *inside* any page, look that name up in the **Complete page "
    "manifest** at the bottom of this file. Sealed and template pages are "
    "intentionally omitted. Generated by `make_ai_index.py` — do not hand-edit; "
    "regenerate instead.\n"
)


def build_output(converted_body: str, all_pages, report) -> str:
    parts = [
        "---\n",
        "title: Eadras Wiki — AI Navigation Index\n",
        "tags: [meta]\n",
        "---\n\n",
        "# Eadras Wiki — AI Navigation Index\n\n",
        ORIENTATION,
        "\n---\n\n",
        converted_body.strip(),
        "\n\n---\n\n",
        "## Complete page manifest\n\n",
        f"Every canon page ({len(all_pages)}), for resolving any `[[name]]` by lookup.\n\n",
    ]
    seen = set()
    for name, rel in all_pages:
        if rel in seen:
            continue
        seen.add(rel)
        parts.append(f"- [{name}]({gh_url(rel)})\n")
    return "".join(parts)


def main():
    dry = "--dry-run" in sys.argv[1:]
    if not WIKI.is_dir() or not INDEX.is_file():
        sys.exit(f"Run from the repo root; expected {INDEX} to exist.")

    by_key, all_pages, ambiguous = build_page_index()
    report = {"converted": 0, "unresolved": [], "blockrefs": 0}

    src = INDEX.read_text(encoding="utf-8")
    converted_body = convert_links(strip_frontmatter(src), by_key, report)
    output = build_output(converted_body, all_pages, report)

    if dry:
        print("[DRY RUN] not writing.\n")
    else:
        OUTPUT.write_text(output, encoding="utf-8")
        print(f"Wrote {OUTPUT.relative_to(ROOT)}")

    print(f"  links converted : {report['converted']}")
    print(f"  pages in manifest: {len(set(r for _, r in all_pages))}")
    print(f"  block refs (no anchor): {report['blockrefs']}")

    if report["unresolved"]:
        uniq = sorted(set(report["unresolved"]))
        print(f"  UNRESOLVED (left as plain text): {len(uniq)}")
        for t in uniq:
            print(f"      [[{t}]]")
    if ambiguous:
        print(f"  AMBIGUOUS bare names (first match used): {len(ambiguous)}")
        for stem, hits in sorted(ambiguous.items()):
            print(f"      '{stem}': {hits}")

    # Ready-to-paste log entry (append to TOP of wiki/log.md per governance).
    print("\n--- log.md entry (paste newest-first at top of wiki/log.md) ---")
    print(f"## {date.today():%Y-%m-%d} — Regenerated ai-index.md")
    print(f"Regenerated `wiki/ai-index.md` from `index.md`: "
          f"{report['converted']} links converted, "
          f"{len(set(report['unresolved']))} unresolved.\n")


if __name__ == "__main__":
    main()