#!/usr/bin/env python3
"""Convert YAML list-form frontmatter fields to compact array form.

Per CLAUDE.md schema: every array field uses compact form `field: [a, b, c]`,
never YAML list form `field:\n  - a\n  - b`. The single exception is
`axes_profile:` which is a dict, not an array, and is left alone.

Pure str manipulation; processes only the frontmatter block of each page.
"""
import sys
from pathlib import Path

ARRAY_FIELDS = [
    'tags', 'canon_status', 'perspective', 'historical_horizon',
    'knowledge_access', 'aliases', 'cssclasses',
]


def parse_frontmatter(text: str) -> tuple[str | None, str, str]:
    leading = ''
    work = text
    if work.startswith('﻿'):
        leading += '﻿'
        work = work[1:]
    if work.startswith('\n'):
        leading += '\n'
        work = work[1:]
    elif work.startswith('\r\n'):
        leading += '\r\n'
        work = work[2:]
    if not work.startswith('---\n') and not work.startswith('---\r\n'):
        return None, text, ''
    nl = '\r\n' if work.startswith('---\r\n') else '\n'
    end_marker = f'{nl}---{nl}'
    end_pos = work.find(end_marker, len(f'---{nl}'))
    if end_pos < 0:
        return None, text, ''
    fm = work[len(f'---{nl}'):end_pos]
    body = work[end_pos + len(end_marker):]
    return fm, body, leading


def compact_listform(fm: str) -> tuple[str, list[str]]:
    """Find any `field:\n  - value` patterns and convert to `field: [value]`."""
    lines = fm.split('\n')
    out = []
    changes = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # Find field-name lines with empty value, followed by indented dash list
        matched = False
        for fname in ARRAY_FIELDS:
            prefix = f'{fname}:'
            if stripped == prefix or stripped == prefix + ' ':
                # Look ahead for indented '- value' lines
                items = []
                j = i + 1
                while j < len(lines):
                    nxt = lines[j]
                    if nxt.startswith('  - ') or nxt.startswith('- '):
                        item = nxt.lstrip()[2:].strip()
                        items.append(item)
                        j += 1
                    elif nxt.strip() == '':
                        break
                    else:
                        break
                if items:
                    out.append(f'{fname}: [{", ".join(items)}]')
                    changes.append(f'{fname} ({len(items)} items)')
                    i = j
                    matched = True
                    break
        if not matched:
            out.append(line)
            i += 1
    return '\n'.join(out), changes


def main():
    args = sys.argv[1:]
    wiki = Path(args[0]) if args else Path('wiki')
    dry_run = '--dry-run' in args
    rows = []
    for md in sorted(wiki.rglob('*.md')):
        text = md.read_text(encoding='utf-8')
        fm, body, leading = parse_frontmatter(text)
        if fm is None:
            continue
        new_fm, changes = compact_listform(fm)
        if not changes:
            continue
        nl = '\n'
        new_text = leading + f'---{nl}{new_fm}{"" if new_fm.endswith(nl) else nl}---{nl}{body}'
        rows.append((md.relative_to(wiki), changes))
        if not dry_run:
            md.write_text(new_text, encoding='utf-8')
    mode = 'DRY RUN ' if dry_run else ''
    print(f'{mode}Compacted {len(rows)} pages:')
    for rel, changes in rows:
        print(f'  {rel}: {", ".join(changes)}')


if __name__ == '__main__':
    main()
