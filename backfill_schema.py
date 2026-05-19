#!/usr/bin/env python3
"""Backfill the canonical CLAUDE.md frontmatter schema across the wiki.

Strategy:
  - Parse each .md file's frontmatter as text (find first --- block).
  - For each missing schema field, add it with a sensible default.
  - Special-case the carve-outs (log.md, index.md, _sealed/, rpg/, reference pages).
  - Add the show-properties toggle to the body if not already present.
  - Do NOT add the axes-block — that requires per-page judgment (which
    pages depict agents with meaningful axes positions).
  - Pure str manipulation; no regex sed-style sweeps.
  - Always dry-run-first; reports every proposed change.

Defaults (when fields are missing):
  - canon_status: [established]
  - perspective: [tome-neutral]   (or [tome-sealed] in _sealed/, [ooc] in rpg/, [reference] for known reference pages)
  - historical_horizon: [all]     (safe default; means "spans multiple eras")
  - knowledge_access: [common]    (or [sealed] for _sealed/, [meta] for reference pages)
  - cssclasses: [hide-props]      (added if missing; existing classes preserved)

Usage:
  python backfill_schema.py wiki [--dry-run] [--limit N]
"""
import sys
from pathlib import Path

SKIP_EXACT = {'log.md', 'index.md'}
REFERENCE_PAGES = {
    'tags.md', 'naming-conventions.md', 'eadras-timeline.md',
    'open-questions.md', 'worldbuilding-needs.md', 'axes-of-creation.md',
    'inspirations.md',
}

SHOW_PROPS_TOGGLE = '<label class="show-props-label"><input type="checkbox" class="show-props-toggle"> Show properties</label>'


def classify(rel_path: str) -> dict:
    """Decide defaults for canon_status/perspective/horizon/access based on path."""
    parts = rel_path.replace('\\', '/').split('/')
    name = parts[-1]
    is_sealed = '_sealed' in parts
    is_rpg = 'rpg' in parts
    is_reference = name in REFERENCE_PAGES

    if is_sealed:
        return {
            'canon_status': '[established]',
            'perspective': '[tome-sealed]',
            'historical_horizon': '[all]',
            'knowledge_access': '[sealed]',
        }
    if is_rpg:
        return {
            'canon_status': '[pending]',
            'perspective': '[ooc]',
            'historical_horizon': '[all]',
            'knowledge_access': '[meta]',
        }
    if is_reference:
        return {
            'canon_status': '[established]',
            'perspective': '[reference]',
            'historical_horizon': '[all]',
            'knowledge_access': '[meta]',
        }
    return {
        'canon_status': '[established]',
        'perspective': '[tome-neutral]',
        'historical_horizon': '[all]',
        'knowledge_access': '[common]',
    }


def parse_frontmatter(text: str) -> tuple[str | None, str, str]:
    """Return (frontmatter_block, body, leading_blank).

    Frontmatter block does not include the surrounding --- lines.
    Returns (None, text, '') if no frontmatter detected.
    """
    # Strip optional leading BOM, then optional leading blank line.
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
    # find next ---
    nl = '\r\n' if work.startswith('---\r\n') else '\n'
    end_marker = f'{nl}---{nl}'
    end_pos = work.find(end_marker, len(f'---{nl}'))
    if end_pos < 0:
        return None, text, ''
    fm = work[len(f'---{nl}'):end_pos]
    body = work[end_pos + len(end_marker):]
    return fm, body, leading


def has_field(fm: str, field: str) -> bool:
    """Check if frontmatter has a given top-level field."""
    for line in fm.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(f'{field}:'):
            return True
    return False


def add_field(fm: str, field: str, value: str) -> str:
    """Append a field to the frontmatter if absent."""
    if has_field(fm, field):
        return fm
    if not fm.endswith('\n'):
        fm += '\n'
    return fm + f'{field}: {value}\n'


def add_cssclass(fm: str, cls: str) -> str:
    """Add a cssclass to the cssclasses field; create the field if absent."""
    lines = fm.splitlines()
    out = []
    found = False
    for ln in lines:
        stripped = ln.lstrip()
        if stripped.startswith('cssclasses:'):
            found = True
            # Compact form: cssclasses: [a, b]
            after = stripped[len('cssclasses:'):].strip()
            if after.startswith('[') and after.endswith(']'):
                contents = after[1:-1].strip()
                items = [i.strip() for i in contents.split(',')] if contents else []
                if cls not in items:
                    items.append(cls)
                ln = f'cssclasses: [{", ".join(items)}]'
            elif after == '' or after.startswith('-'):
                # YAML list form (multi-line) — leave alone; flag as anomaly
                pass
            else:
                # Unknown form — leave alone
                pass
        out.append(ln)
    result = '\n'.join(out)
    if not found:
        if not result.endswith('\n'):
            result += '\n'
        result += f'cssclasses: [{cls}]\n'
    return result


def ensure_show_props(body: str) -> tuple[str, bool]:
    """Insert the show-properties toggle before the H1 if missing."""
    if 'show-props-toggle' in body:
        return body, False
    # find first H1 line
    lines = body.split('\n')
    for i, ln in enumerate(lines):
        if ln.startswith('# '):
            # Insert toggle + blank line before this H1
            insert = [SHOW_PROPS_TOGGLE, '']
            lines = lines[:i] + insert + lines[i:]
            return '\n'.join(lines), True
    return body, False


def process(md_path: Path, wiki_root: Path) -> dict:
    rel = str(md_path.relative_to(wiki_root))
    if md_path.name in SKIP_EXACT:
        return {'rel': rel, 'action': 'skip-carveout'}

    text = md_path.read_text(encoding='utf-8')
    fm, body, leading = parse_frontmatter(text)
    if fm is None:
        return {'rel': rel, 'action': 'no-frontmatter'}

    defaults = classify(rel)
    changes = []
    new_fm = fm
    for field, value in defaults.items():
        if not has_field(new_fm, field):
            new_fm = add_field(new_fm, field, value)
            changes.append(f'+{field}={value}')
    if not has_field(new_fm, 'cssclasses'):
        new_fm = add_cssclass(new_fm, 'hide-props')
        changes.append('+cssclasses=[hide-props]')
    else:
        # Add hide-props to existing cssclasses if missing
        new_fm_after = add_cssclass(new_fm, 'hide-props')
        if new_fm_after != new_fm:
            new_fm = new_fm_after
            changes.append('+hide-props in cssclasses')

    new_body, body_changed = ensure_show_props(body)
    if body_changed:
        changes.append('+show-props-toggle')

    if not changes:
        return {'rel': rel, 'action': 'already-conforms'}

    nl = '\n'
    new_text = leading + f'---{nl}{new_fm}{"" if new_fm.endswith(nl) else nl}---{nl}{new_body}'
    return {'rel': rel, 'action': 'change', 'changes': changes, 'new_text': new_text}


def main():
    args = sys.argv[1:]
    wiki = Path(args[0]) if args else Path('wiki')
    dry_run = '--dry-run' in args
    limit = None
    for a in args:
        if a.startswith('--limit'):
            limit = int(a.split('=')[-1]) if '=' in a else None
    counts = {'change': 0, 'already-conforms': 0, 'skip-carveout': 0, 'no-frontmatter': 0}
    rows = []
    for md in sorted(wiki.rglob('*.md')):
        result = process(md, wiki)
        counts[result['action']] = counts.get(result['action'], 0) + 1
        if result['action'] == 'change':
            rows.append(result)
            if not dry_run:
                md.write_text(result['new_text'], encoding='utf-8')
        if limit and counts['change'] >= limit:
            break

    mode = 'DRY RUN ' if dry_run else ''
    print(f'{mode}Backfill summary:')
    for k, v in counts.items():
        print(f'  {k}: {v}')
    print()
    if rows:
        print('Per-file changes:')
        for r in rows[:50]:
            print(f"  {r['rel']}  ::  {', '.join(r['changes'])}")
        if len(rows) > 50:
            print(f'  ... and {len(rows) - 50} more')


if __name__ == '__main__':
    main()
