#!/usr/bin/env python3
"""Sweep wikilinks for the May 10 race renames.

Replaces five slug prefixes inside wikilinks ONLY when followed by a
wikilink terminator: ']', '|', '#', or '\\' (the backslash form used
inside markdown tables). All replacements are pure str.replace; no
regex, so no chance of runaway expansion.

Usage:
  python sweep_wikilinks.py <wiki_root> [--dry-run] [--include-log]
"""
import sys
from pathlib import Path

RENAMES = [
    ('rathar', 'rathari'),
    ('taran', 'tarans'),
    ('aetherin', 'aetherins'),
    ('grug', 'grugi'),
    ('orug', 'orugi'),
]
TERMINATORS = [']', '|', '#', '\\']


def sweep(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for old, new in RENAMES:
        for term in TERMINATORS:
            old_pat = f'[[{old}{term}'
            new_pat = f'[[{new}{term}'
            n = text.count(old_pat)
            if n:
                counts[old_pat] = n
                text = text.replace(old_pat, new_pat)
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
