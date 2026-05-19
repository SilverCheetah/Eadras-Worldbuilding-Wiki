#!/usr/bin/env python3
"""Sweep Sarathim → Amunorian rename (2026-05-12).

Replaces wikilink slugs, frontmatter tags, and body prose forms. All
replacements are pure str.replace; no regex, so no chance of runaway
expansion.

Body-prose rules are ordered: specific plural-collective phrases run
BEFORE the general "Sarathim X → Amunorian X" rule, so phrases like
"the Sarathim themselves" become "the Amunorians themselves" rather
than "the Amunorian themselves".

The user-chosen convention (2026-05-12) is:
  - Adjective: "Sarathim X" → "Amunorian X"  (X = any noun)
  - Plural collective: "the Sarathim" / "Modern Sarathim survive" → Amunorians
  - Singular indefinite: "A Sarathim smiles..." → "An Amunorian smiles..."
  - Tag/lineage modifier: "sarathim" → "amunorian"

Does NOT touch:
  - `Sarathis` (the capital city — canon-preserved)
  - `log.md` historical entries (preserved as-written by default;
    Obsidian aliases on amunorians.md handle wikilink resolution)
  - raw/ source filenames (e.g., sarathim-revision-2026-05-11.txt)

Usage:
  python sweep_sarathim_to_amunorian.py <wiki_root> [--dry-run] [--include-log]
"""
import sys
from pathlib import Path


# Order matters. Specific phrases first; general fallthrough last.
RENAMES: list[tuple[str, str]] = [
    # === 1. Wikilink slugs ===
    ('[[sarathim]]', '[[amunorians]]'),
    ('[[sarathim|', '[[amunorians|'),
    ('[[sarathim#', '[[amunorians#'),

    # === 2. Frontmatter tag references ===
    (', sarathim,', ', amunorian,'),
    (', sarathim]', ', amunorian]'),
    ('[sarathim,', '[amunorian,'),

    # === 3. Quoted sayings (article must change: "A" → "An" before vowel) ===
    ('"A Sarathim smiles', '"An Amunorian smiles'),
    ('*A Sarathim smiles', '*An Amunorian smiles'),

    # === 4. Specific plural-collective phrases (must precede general rule) ===
    # "the Sarathim" + verb / pronoun → "the Amunorians"
    ('the Sarathim themselves', 'the Amunorians themselves'),
    ('the Sarathim alone', 'the Amunorians alone'),
    ('the Sarathim are', 'the Amunorians are'),
    ('the Sarathim were', 'the Amunorians were'),
    ('the Sarathim consciously', 'the Amunorians consciously'),
    ('the Sarathim viewed', 'the Amunorians viewed'),
    ('the Sarathim distinguished', 'the Amunorians distinguished'),
    ('the Sarathim treated', 'the Amunorians treated'),
    ('the Sarathim lost', 'the Amunorians lost'),
    ('The Sarathim are', 'The Amunorians are'),
    ('The Sarathim were', 'The Amunorians were'),
    ('The Sarathim themselves', 'The Amunorians themselves'),

    # "Modern Sarathim" + verb → "Modern Amunorians"
    ('Modern Sarathim survive', 'Modern Amunorians survive'),
    ('Modern Sarathim live', 'Modern Amunorians live'),

    # "diaspora Sarathim" as plural noun
    ('diaspora Sarathim as', 'diaspora Amunorians as'),

    # === 5. General Sarathim → Amunorian (adjective + noun catch-all) ===
    ('Sarathim ', 'Amunorian '),

    # === 6. Trailing-punctuation forms ===
    ("Sarathim's", "Amunorian's"),
    ('Sarathim.', 'Amunorian.'),
    ('Sarathim,', 'Amunorian,'),
    ('Sarathim;', 'Amunorian;'),
    ('Sarathim:', 'Amunorian:'),
    ('Sarathim)', 'Amunorian)'),
    ('Sarathim]', 'Amunorian]'),
]


def sweep(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for old, new in RENAMES:
        n = text.count(old)
        if n:
            counts[old] = n
            text = text.replace(old, new)
    return text, counts


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    wiki = Path(args[0])
    dry_run = '--dry-run' in args
    include_log = '--include-log' in args

    total_files = 0
    total_repls = 0
    rows: list[tuple[str, dict[str, int]]] = []

    for md in sorted(wiki.rglob('*.md')):
        rel = md.relative_to(wiki).as_posix()
        if not include_log and rel == 'log.md':
            continue
        original = md.read_text(encoding='utf-8')
        new, counts = sweep(original)
        if counts:
            rows.append((rel, counts))
            total_files += 1
            total_repls += sum(counts.values())
            if not dry_run and new != original:
                md.write_text(new, encoding='utf-8')

    mode = 'DRY RUN ' if dry_run else ''
    log_note = '(log.md included)' if include_log else '(log.md skipped)'
    print(f'{mode}files affected: {total_files}, replacements: {total_repls} {log_note}')
    print()
    for rel, counts in rows:
        per_file = sum(counts.values())
        details = ', '.join(f'{n}×"{p}"' for p, n in sorted(counts.items()))
        print(f'  {per_file:3d}  {rel}  ::  {details}')


if __name__ == '__main__':
    main()
