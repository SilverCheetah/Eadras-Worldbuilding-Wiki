"""
Phase 1, Step 2 — Escape unescaped pipes in wikilinks inside markdown tables
=============================================================================

Adds backslash escapes to wikilink alias-pipes that sit inside markdown table 
cells, where the unescaped pipe breaks the table's column structure.

WHAT IT FIXES
-------------
Markdown tables use `|` as the column-separator. When a wikilink containing 
an alias-pipe sits inside a table cell:

    | Race   | Creator | Notes |
    | ---    | ---     | ---   |
    | [[arathi|Arathi]] | ...

...the markdown parser splits the wikilink across two cells. The row above 
becomes 4 cells (`[[arathi`, `Arathi]]`, ...) instead of 3.

Per Obsidian docs, the fix is to escape the alias-pipe:

    | [[arathi\\|Arathi]] | ...

The wikilink parser handles `\|` correctly: it still resolves to `arathi` 
with display text `Arathi`, and the table parser correctly counts cells.

SCOPE OF THIS FIX
-----------------
Targets ONLY wikilinks of the form `[[slug|Display]]` that:
  1. Appear inside a markdown table row (a line whose first non-whitespace 
     character is `|` and which contains ≥3 pipes).
  2. Use an UNESCAPED alias-pipe.

PROSE WIKILINKS ARE LEFT ALONE. There are 8,696 of them in the wiki; they 
must not be touched.

NOTE ON peoples-of-eadras.md
-----------------------------
This file has a 6-column-header / variable-cell table that is structurally 
malformed beyond pipe-escaping. This script will fix the pipe-escapes but 
the table will still need manual rebuilding (see issue #4 in the register, 
and the companion script `04-rebuild-peoples-of-eadras-table.py`).

USAGE
-----
    python 02-escape-pipes-in-table-wikilinks.py            # dry run
    python 02-escape-pipes-in-table-wikilinks.py --write   # apply

DEPENDENCIES
------------
None beyond Python 3.10+ stdlib.
"""

import argparse
import re
import sys
from pathlib import Path


# A wikilink with an unescaped pipe (i.e., not preceded by backslash).
# Captures: target | display
WIKILINK_WITH_PIPE = re.compile(
    r'\[\[([^\[\]\\\|]+?)\|([^\[\]\\]+?)\]\]'
)


def find_repo_root(start: Path) -> Path:
    p = start.resolve()
    for parent in [p] + list(p.parents):
        if (parent / 'wiki' / 'system-governance.md').exists():
            return parent
    raise SystemExit(f"Could not find repo root from {start}.")


def is_table_row(line: str) -> bool:
    """A markdown table row starts with | (after stripping) and has ≥3 pipes total."""
    stripped = line.strip()
    return stripped.startswith('|') and stripped.count('|') >= 3


def fix_line(line: str) -> tuple[str, int]:
    """Escape alias-pipes inside wikilinks. Returns (new_line, num_fixes)."""
    fixes = [0]
    def repl(m):
        fixes[0] += 1
        return f'[[{m.group(1)}\\|{m.group(2)}]]'
    new_line = WIKILINK_WITH_PIPE.sub(repl, line)
    return new_line, fixes[0]


def fix_file(path: Path, write: bool, verbose: bool) -> tuple[int, list[tuple[int, str, str]]]:
    """Fix one file. Returns (total_fixes, sample_diffs)."""
    text = path.read_text(encoding='utf-8')
    lines = text.split('\n')
    new_lines = []
    total_fixes = 0
    sample_diffs = []
    
    for i, ln in enumerate(lines):
        if is_table_row(ln) and '[[' in ln:
            new_ln, n = fix_line(ln)
            if n:
                total_fixes += n
                if verbose and len(sample_diffs) < 3:
                    sample_diffs.append((i+1, ln.strip()[:160], new_ln.strip()[:160]))
            new_lines.append(new_ln)
        else:
            new_lines.append(ln)
    
    if write and total_fixes:
        path.write_text('\n'.join(new_lines), encoding='utf-8')
    
    return total_fixes, sample_diffs


def main():
    parser = argparse.ArgumentParser(description="Escape pipes in table-cell wikilinks")
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--repo', type=Path, default=None)
    args = parser.parse_args()
    
    repo = args.repo or find_repo_root(Path(__file__).parent)
    print(f"Repo root: {repo}")
    print(f"Mode: {'WRITE' if args.write else 'DRY RUN'}\n")
    
    files = []
    for path in sorted(repo.glob('wiki/**/*.md')):
        if '_sealed' in path.parts or 'templates' in path.parts:
            continue
        files.append(path)
    
    total = 0
    affected_files = 0
    for path in files:
        rel = path.relative_to(repo)
        n, diffs = fix_file(path, args.write, args.verbose)
        if n:
            affected_files += 1
            total += n
            print(f"  {n:3d}  {rel}")
            if args.verbose:
                for ln, a, b in diffs:
                    print(f"    L{ln}- {a}")
                    print(f"    L{ln}+ {b}")
                print()
    
    print()
    print(f"Files modified: {affected_files}")
    print(f"Total wikilinks escaped: {total}")
    
    if args.write:
        print()
        print("Suggested commit:")
        print('  git add -A')
        print('  git commit -m "Escape pipes in table-cell wikilinks (186 fixes)"')
    else:
        print("\nDRY RUN — re-run with --write to apply.")


if __name__ == '__main__':
    main()
