"""Sweep padded table-cell wikilinks the main sweep missed.

Pattern: '[[<old> ' (slug + ONE trailing space) -> '[[<new>' (no space).
The replacement consumes exactly one space, preserving the +1 char from
slug pluralization, so markdown table column widths stay identical.

Pure str.replace; no regex.
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


def sweep(text: str) -> tuple[str, dict[str, int]]:
    counts = {}
    for old, new in RENAMES:
        old_pat = f'[[{old} '   # one trailing space
        new_pat = f'[[{new}'    # no space, +1 char on slug = same width
        n = text.count(old_pat)
        if n:
            counts[old_pat] = n
            text = text.replace(old_pat, new_pat)
    return text, counts


def main():
    args = sys.argv[1:]
    wiki = Path(args[0]) if args else Path('wiki')
    dry_run = '--dry-run' in args

    total_files = 0
    total_repls = 0
    for md in sorted(wiki.rglob('*.md')):
        if md.name == 'log.md':
            continue
        original = md.read_text(encoding='utf-8')
        new, counts = sweep(original)
        if counts:
            total_files += 1
            total_repls += sum(counts.values())
            print(f'  {sum(counts.values()):3d}  {md.relative_to(wiki)}  ::  {counts}')
            if not dry_run:
                md.write_text(new, encoding='utf-8')
    mode = 'DRY RUN ' if dry_run else ''
    print(f'{mode}files affected: {total_files}, replacements: {total_repls}')


if __name__ == '__main__':
    main()
