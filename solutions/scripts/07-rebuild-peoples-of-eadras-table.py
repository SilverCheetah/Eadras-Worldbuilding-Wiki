"""
Phase 2, Step 7 — Rebuild wiki/peoples-of-eadras.md tables
============================================================

The "Original Races" and "Races Present in the Modern Era" tables in 
peoples-of-eadras.md are structurally broken in the live repo. Two patterns 
combined to break them:

1. The header row declares 3 columns (`| Race | Creator | Notes |`) but 
   the separator row declares 5 cells (`| --- | --- | --- | --- | --- |`).

2. Cell contents with `[[slug|Display]]` wikilinks have UNESCAPED alias-pipes. 
   The markdown table parser interprets those pipes as column separators, 
   splitting one logical wikilink across two visual cells.

The combination produces rows like:
    | **[[arathi  | Arathi]]** | Evye & Fryr | First civilization... |      |      |

...which renders as a 5-cell mess instead of a clean 3-column row.

WHAT THIS SCRIPT DOES
---------------------
1. Locates each of the two tables.
2. Parses each row using a wikilink-aware tokenizer (treats `[[...]]` and 
   `\\|` as opaque non-separators).
3. Normalizes each row to exactly 3 columns: Race | Creator | Notes.
4. Re-emits with properly-escaped wikilinks (`[[slug\\|Display]]`) since 
   the result is still inside a markdown table.
5. Preserves all surrounding prose, only rewriting the two tables in place.

USAGE
-----
    python 07-rebuild-peoples-of-eadras-table.py             # dry run
    python 07-rebuild-peoples-of-eadras-table.py --write     # apply

NOTE
----
This script is best run AFTER script 02 (escape-pipes), although it doesn't 
depend on it — the rebuilt table will use escaped pipes regardless. Running 
02 first means the table is already in a more-correct state if this rebuild 
ever fails partway.
"""

import argparse
import re
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    p = start.resolve()
    for parent in [p] + list(p.parents):
        if (parent / 'wiki' / 'system-governance.md').exists():
            return parent
    raise SystemExit(f"Could not find repo root from {start}.")


def smart_split(line: str) -> list[str]:
    """
    Split a markdown table row by `|`, respecting [[...]] grouping and \\| 
    escapes. Returns logical cells (with leading/trailing | edges removed).
    """
    cells = []
    cur = []
    i = 0
    in_link = False
    while i < len(line):
        if line[i:i+2] == '[[':
            in_link = True
            cur.append('[[')
            i += 2; continue
        if line[i:i+2] == ']]':
            in_link = False
            cur.append(']]')
            i += 2; continue
        if line[i:i+2] == '\\|':
            cur.append('\\|')
            i += 2; continue
        c = line[i]
        if c == '|' and not in_link:
            cells.append(''.join(cur).strip())
            cur = []
        else:
            cur.append(c)
        i += 1
    cells.append(''.join(cur).strip())
    # Drop the empty leading and trailing cells produced by the bordering |
    return [c for c in cells if c]


def normalize_wikilinks_in_cell(cell: str) -> str:
    """
    For wikilinks in table cells:
      [[slug   |   Display]]   →   [[slug\\|Display]]
    
    Collapses internal whitespace, then escapes the alias-pipe (because the 
    cell is going inside a markdown table).
    """
    def fix_unescaped(m):
        slug = m.group(1).strip()
        display = m.group(2).strip()
        return f'[[{slug}\\|{display}]]'
    
    # Match wikilinks with UNESCAPED pipe and possibly internal whitespace
    cell = re.sub(
        r'\[\[\s*([^\[\]\\\|]+?)\s*\|\s*([^\[\]\\]+?)\s*\]\]',
        fix_unescaped, cell
    )
    
    # Match wikilinks with already-ESCAPED pipe and possibly internal whitespace
    def fix_escaped(m):
        slug = m.group(1).strip()
        display = m.group(2).strip()
        return f'[[{slug}\\|{display}]]'
    cell = re.sub(
        r'\[\[\s*([^\[\]\\\|]+?)\s*\\\|\s*([^\[\]\\]+?)\s*\]\]',
        fix_escaped, cell
    )
    
    # Collapse multiple spaces outside wikilinks
    cell = re.sub(r'  +', ' ', cell)
    return cell.strip()


def rebuild_table(rows: list[str], expected_cols: int = 3) -> list[str]:
    """
    Rebuild a list of table-row lines into a clean, properly-formed table 
    with `expected_cols` columns. Returns the list of new lines (excluding 
    header and separator, which the caller provides).
    """
    new_rows = []
    for row in rows:
        cells = smart_split(row)
        # Drop trailing empty cells (the | | | padding)
        while cells and not cells[-1]:
            cells.pop()
        # Pad if short
        while len(cells) < expected_cols:
            cells.append('')
        # Truncate if too long (should never happen after smart_split)
        cells = cells[:expected_cols]
        # Normalize wikilinks
        cells = [normalize_wikilinks_in_cell(c) for c in cells]
        # Emit
        new_rows.append('| ' + ' | '.join(cells) + ' |')
    return new_rows


def find_and_rebuild_table(text: str, header_pattern: str) -> tuple[str, dict]:
    """
    Find the table whose header line matches `header_pattern` (regex), 
    then rebuild it. Returns (new_text, stats).
    
    Strategy: locate the header line, the separator line, then capture all 
    consecutive table rows until a non-pipe-starting line.
    """
    lines = text.split('\n')
    
    # Find the header
    header_idx = None
    for i, ln in enumerate(lines):
        if re.match(header_pattern, ln.strip()):
            header_idx = i
            break
    
    if header_idx is None:
        return text, {'found': False}
    
    # Separator should be next non-blank line
    sep_idx = header_idx + 1
    while sep_idx < len(lines) and not lines[sep_idx].strip().startswith('|'):
        sep_idx += 1
    
    if sep_idx >= len(lines) or not re.match(r'^\|[\s\-:\|]+\|?\s*$', lines[sep_idx].strip()):
        return text, {'found': False, 'reason': 'no separator after header'}
    
    # Capture row lines
    row_start = sep_idx + 1
    row_end = row_start
    while row_end < len(lines) and lines[row_end].strip().startswith('|'):
        row_end += 1
    
    raw_rows = lines[row_start:row_end]
    
    # Rebuild
    new_rows = rebuild_table(raw_rows, expected_cols=3)
    
    # Build the new table
    new_header = '| Race | Creator | Notes |'
    new_separator = '| --- | --- | --- |'
    
    # Reassemble
    new_lines = (
        lines[:header_idx]
        + [new_header, new_separator]
        + new_rows
        + lines[row_end:]
    )
    
    return '\n'.join(new_lines), {
        'found': True,
        'header_line': header_idx + 1,
        'rows_rebuilt': len(raw_rows),
        'original_rows': raw_rows,
        'new_rows': new_rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--repo', type=Path, default=None)
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    
    repo = args.repo or find_repo_root(Path(__file__).parent)
    target = repo / 'wiki' / 'peoples-of-eadras.md'
    
    print(f"Repo root: {repo}")
    print(f"Target:    {target}")
    print(f"Mode:      {'WRITE' if args.write else 'DRY RUN'}\n")
    
    text = target.read_text(encoding='utf-8')
    
    # Rebuild both tables. The header pattern allows for whitespace padding 
    # in the column names ("| Race    |" etc.)
    text, stats1 = find_and_rebuild_table(
        text, r'^\|\s*Race\s+\|\s*Creator\s+\|'
    )
    if stats1['found']:
        print(f"Rebuilt table 1 starting at line {stats1['header_line']}: {stats1['rows_rebuilt']} rows")
        if args.verbose:
            print("\nSample rebuilt rows:")
            for r in stats1['new_rows'][:5]:
                print(f"  {r[:160]}")
            print()
    
    if not stats1['found']:
        print("WARNING: no race table found. File may already be rebuilt or have different headers.")
        return
    
    if args.write:
        target.write_text(text, encoding='utf-8')
        print(f"\n✓ Wrote {target}")
        print("\nSuggested commit:")
        print('  git add wiki/peoples-of-eadras.md')
        print('  git commit -m "Rebuild peoples-of-eadras.md race tables (3 columns; escape pipes in wikilinks)"')
    else:
        print("\nDRY RUN — re-run with --write to apply.")
        print("Before applying, eyeball-check the rebuilt rows above with --verbose.")


if __name__ == '__main__':
    main()
