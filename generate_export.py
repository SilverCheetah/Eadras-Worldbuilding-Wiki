#!/usr/bin/env python3
"""Generate concatenated wiki exports at the repository root.

By default every run produces **two** files:

    wiki-export-YYYY-MM-DD.md          -- full export. Includes everything under
                                          wiki/ (canon, _sealed/, rpg/, all
                                          reference/meta pages, log.md). For
                                          trusted users and the canonical
                                          backup. One per day; re-runs through
                                          the day silently overwrite the day's
                                          snapshot.
    wiki-export-YYYY-MM-DD-public.md   -- public export. Strips administrative
                                          and sealed material so the file is
                                          safe to hand to an external AI.

Public-export exclusion rules (locked 2026-05-11):

    Prefix-stripped:
      wiki/_sealed/         -- plot-spine secrets; never leaves the vault.

    Exact-path-stripped:
      wiki/log.md           -- operational changelog; ~4000 lines of dates.
      wiki/index.md         -- table of contents; redundant for an external AI
                               that receives the whole text.
      wiki/inspirations.md  -- real-world / fictional touchstones; OOC.

Kept in the public export (these describe canon and are useful context for
an external collaborator): wiki/tags.md, wiki/naming-conventions.md,
wiki/open-questions.md, wiki/worldbuilding-needs.md, and the entire
wiki/rpg/ subfolder (OOC mechanics, but useful for game-design discussion).

Stripping happens at export-generation time, not at share time -- so the
public copy is always ready to go and there is no "remember to strip" step.
Do not solve the sharing problem by excluding sealed material from the full
export; the full export remains the canonical backup.

Format (matching the existing 2026-05-09 / 2026-05-07 exports):

    # Eadras Wiki — Export YYYY-MM-DD                  (full)
    # Eadras Wiki — Public Export YYYY-MM-DD           (public)

    Concatenated export of ... wiki pages as of YYYY-MM-DD.

    **Includes** / **Excludes**: ...

    ---

    ## Table of Contents

    - `wiki/<name>.md` — <title>
    - ...

    ---

    ===============================================
    FILE: wiki/<name>.md
    ===============================================

    <page content>

    ...

Usage:
  python generate_export.py [--root <path>] [--full-only | --public-only]

  --force is accepted for backward compatibility but no longer required;
  same-day re-runs always overwrite.
"""
import re
import sys
from datetime import date
from pathlib import Path


DELIM = '=' * 47

# Public-export strip rules.
PUBLIC_STRIP_PREFIXES = ('wiki/_sealed/',)
PUBLIC_STRIP_EXACT = frozenset({
    'wiki/log.md',
    'wiki/index.md',
    'wiki/inspirations.md',
})


def is_public_excluded(rel: str) -> bool:
    if rel in PUBLIC_STRIP_EXACT:
        return True
    return any(rel.startswith(p) for p in PUBLIC_STRIP_PREFIXES)


def extract_title(text: str) -> str:
    """Pull the YAML title field, or fall back to the first H1."""
    m = re.search(r'^title:\s*(.+?)$', text, re.MULTILINE)
    if m:
        title = m.group(1).strip()
        if title.startswith('"') and title.endswith('"'):
            title = title[1:-1]
        if title.startswith("'") and title.endswith("'"):
            title = title[1:-1]
        return title
    m = re.search(r'^# (.+?)$', text, re.MULTILINE)
    return m.group(1).strip() if m else '(untitled)'


def render_export(today: str, pages, *, is_public: bool) -> str:
    """Assemble one export file from a (rel, text, title) page list."""
    parts = []
    if is_public:
        parts.append(f'# Eadras Wiki — Public Export {today}\n\n')
        parts.append(f'Concatenated public export of canon wiki pages as of {today}. '
                     f'Safe to share with external AI collaborators.\n\n')
        parts.append('**Excludes**: `wiki/_sealed/*` (plot-spine secrets), '
                     '`wiki/log.md` (operational changelog), '
                     '`wiki/index.md` (table of contents), '
                     '`wiki/inspirations.md` (OOC real-world touchstones).\n\n')
        parts.append('**Includes**: all in-universe canon pages plus the in-project '
                     'reference pages (`tags.md`, `naming-conventions.md`, '
                     '`open-questions.md`, `worldbuilding-needs.md`) and the entire '
                     '`wiki/rpg/` OOC splatbook subfolder.\n\n')
    else:
        parts.append(f'# Eadras Wiki — Export {today}\n\n')
        parts.append(f'Concatenated full export of all wiki pages as of {today}.\n\n')
        parts.append('**Includes**: `wiki/`, `wiki/_sealed/`, `wiki/rpg/`, and all '
                     'reference/meta pages. This is the canonical backup; do **not** '
                     'share externally as-is — use the `-public.md` companion file '
                     'instead (it is generated alongside this one).\n\n')
    parts.append(f'**Total pages**: {len(pages)}.\n\n')
    parts.append('---\n\n## Table of Contents\n\n')
    for rel, _text, title in pages:
        parts.append(f'- `{rel}` — {title}\n')
    parts.append('\n---\n\n')
    for rel, text, _title in pages:
        parts.append(f'\n{DELIM}\nFILE: {rel}\n{DELIM}\n\n')
        # Ensure the page text ends with exactly one newline before next delimiter
        parts.append(text.rstrip('\n') + '\n')
    return ''.join(parts)


def main():
    args = sys.argv[1:]
    root = Path('.')
    full_only = '--full-only' in args
    public_only = '--public-only' in args
    if full_only and public_only:
        print('ERROR: --full-only and --public-only are mutually exclusive.',
              file=sys.stderr)
        sys.exit(2)
    for i, a in enumerate(args):
        if a == '--root' and i + 1 < len(args):
            root = Path(args[i + 1])

    today = date.today().isoformat()  # YYYY-MM-DD
    full_path = root / f'wiki-export-{today}.md'
    public_path = root / f'wiki-export-{today}-public.md'

    wiki_root = root / 'wiki'
    if not wiki_root.is_dir():
        print(f'ERROR: {wiki_root} is not a directory.', file=sys.stderr)
        sys.exit(1)

    # Collect every .md under wiki/ in sorted order, recording (rel, text, title).
    all_pages = []
    for md in sorted(wiki_root.rglob('*.md')):
        rel = md.relative_to(root).as_posix()
        text = md.read_text(encoding='utf-8')
        # Strip any leading BOM for the export (it can interfere with re-import)
        if text.startswith('﻿'):
            text = text[1:]
        all_pages.append((rel, text, extract_title(text)))

    if not all_pages:
        print('ERROR: no wiki pages found.', file=sys.stderr)
        sys.exit(1)

    public_pages = [p for p in all_pages if not is_public_excluded(p[0])]
    excluded = [p[0] for p in all_pages if is_public_excluded(p[0])]

    # Write full export (everything).
    if not public_only:
        full_path.write_text(render_export(today, all_pages, is_public=False),
                             encoding='utf-8')
        size_kb = full_path.stat().st_size / 1024
        print(f'Wrote {full_path} ({len(all_pages)} pages, {size_kb:.1f} KB) [full]')

    # Write public export (sealed + administrative stripped).
    if not full_only:
        public_path.write_text(render_export(today, public_pages, is_public=True),
                               encoding='utf-8')
        size_kb = public_path.stat().st_size / 1024
        print(f'Wrote {public_path} ({len(public_pages)} pages, {size_kb:.1f} KB) [public]')
        if excluded:
            print(f'  Stripped {len(excluded)} page(s) from public: '
                  f'{", ".join(excluded[:6])}'
                  + (f', +{len(excluded) - 6} more' if len(excluded) > 6 else ''))


if __name__ == '__main__':
    main()
