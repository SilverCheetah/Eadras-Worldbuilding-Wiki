"""Find table-cell wikilinks like [[rathar           |Rathar]] where the
sweep missed because of whitespace padding between slug and pipe."""
from pathlib import Path

OLD = ['rathar', 'taran', 'aetherin', 'grug', 'orug']
TERMS = ('|', '\\')

for md in sorted(Path('wiki').rglob('*.md')):
    if md.name == 'log.md':
        continue
    text = md.read_text(encoding='utf-8')
    for slug in OLD:
        needle = f'[[{slug}'
        i = 0
        while True:
            i = text.find(needle, i)
            if i < 0:
                break
            tail = text[i + len(needle):]
            j = 0
            while j < len(tail) and tail[j] == ' ':
                j += 1
            if j > 0 and j < len(tail) and tail[j] in TERMS:
                line_no = text[:i].count('\n') + 1
                snippet = text[i:i + 80].replace('\n', '\\n')
                print(f'{md.relative_to("wiki")}:{line_no}  {snippet}')
            i += 1
