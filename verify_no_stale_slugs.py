"""Verify no stale [[rathar/taran/aetherin/grug/orug + terminator]] wikilinks remain
outside log.md. Pure literal scan — no regex."""
from pathlib import Path

OLD_SLUGS = ['rathar', 'taran', 'aetherin', 'grug', 'orug']
TERMINATORS = [']', '|', '#', '\\']

total = 0
for md in sorted(Path('wiki').rglob('*.md')):
    if md.name == 'log.md':
        continue
    text = md.read_text(encoding='utf-8')
    for slug in OLD_SLUGS:
        for term in TERMINATORS:
            pat = f'[[{slug}{term}'
            n = text.count(pat)
            if n:
                print(f'{n:3d}  {md.relative_to("wiki")}  -- pattern {pat!r}')
                total += n
print(f'\nTOTAL stale wikilinks: {total}')
