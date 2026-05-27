"""
Phase 1, Step 4 — Commit the cleaned unicorns.md
=================================================

The live repo's wiki/unicorns.md has a six-line section block duplicated 
262 times (corruption residue from the 2026-05-10 sed-script incident).
The file is 2,400 lines / 411KB when the real content is ~280 lines / ~17KB.

A cleaned 312-line version was prepared on 2026-05-27 but never committed.

This script:
  1. Verifies that the cleaned version exists at the path you specify.
  2. Pre-processes it through the mojibake fixer, line-ending normalizer,
     AND the table-cell-wikilink-pipe-escape transform (so it lands in 
     the repo in clean form whether or not those scripts have already run).
  3. Writes it to wiki/unicorns.md.
  4. Cleans the Sources line: removes triplicated source references 
     (issue #6 in the register — the 2026-05-27 cleaned version still has 
     "DragonsAndUnicorns_01_InWorld_Facts.txt; user direction 2026-05-13" 
     repeated 3 times on the Sources line).

USAGE
-----
    # Show what would happen
    python 04-fix-unicorns.py --cleaned /path/to/unicorns-cleaned.md

    # Apply
    python 04-fix-unicorns.py --cleaned /path/to/unicorns-cleaned.md --write

DEPENDENCIES
------------
- ftfy (used by 01-fix-mojibake.py logic)
- Safe to run BEFORE or AFTER scripts 01, 02, 03 — the script applies all 
  three transforms to the upload internally so the result is always clean.
"""

import argparse
import re
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    p = start.resolve()
    for parent in [p] + list(p.parents):
        if (parent / 'wiki' / 'system-governance.md').exists():
            return parent
    raise SystemExit(f"Could not find repo root from {start}.")


def dedupe_sources_line(text: str) -> tuple[str, int]:
    """
    Strip exact-duplicate source tokens from the **Sources** line, preserving 
    order of first occurrence. Returns (new_text, duplicates_removed).
    """
    def fix_sources(match):
        prefix = match.group(1)  # "**Sources**: "
        body = match.group(2)
        # Split on ; - this is the Eadras Sources convention
        parts = [p.strip() for p in body.split(';') if p.strip()]
        seen = set()
        unique = []
        removed = 0
        for p in parts:
            if p in seen:
                removed += 1
                continue
            seen.add(p)
            unique.append(p)
        if removed:
            fix_sources.removed += removed
        return prefix + '; '.join(unique)
    
    fix_sources.removed = 0
    new_text = re.sub(
        r'^(\*\*Sources\*\*:\s*)(.+)$',
        fix_sources,
        text,
        count=1,
        flags=re.MULTILINE,
    )
    return new_text, fix_sources.removed


def escape_pipes_in_table_wikilinks(text: str) -> tuple[str, int]:
    """
    Apply script 02's transform: in table rows, escape unescaped alias-pipes 
    in wikilinks. Returns (new_text, num_fixed).
    """
    wikilink_re = re.compile(
        r'\[\[([^\[\]\\\|]+?)\|([^\[\]\\]+?)\]\]'
    )
    fixed = 0
    new_lines = []
    for ln in text.split('\n'):
        stripped = ln.strip()
        if stripped.startswith('|') and stripped.count('|') >= 3 and '[[' in ln:
            def repl(m):
                nonlocal fixed
                fixed += 1
                return f'[[{m.group(1)}\\|{m.group(2)}]]'
            new_lines.append(wikilink_re.sub(repl, ln))
        else:
            new_lines.append(ln)
    return '\n'.join(new_lines), fixed


def main():
    parser = argparse.ArgumentParser(description="Replace wiki/unicorns.md with the cleaned version")
    parser.add_argument('--cleaned', type=Path, required=True,
                        help='Path to the cleaned unicorns.md (e.g., the 2026-05-27 upload)')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--repo', type=Path, default=None)
    args = parser.parse_args()
    
    if not args.cleaned.exists():
        raise SystemExit(f"Cleaned file not found: {args.cleaned}")
    
    repo = args.repo or find_repo_root(Path(__file__).parent)
    target = repo / 'wiki' / 'unicorns.md'
    
    if not target.exists():
        raise SystemExit(f"Target not found: {target}")
    
    print(f"Repo root: {repo}")
    print(f"Cleaned source: {args.cleaned}")
    print(f"Target: {target}")
    print(f"Mode: {'WRITE' if args.write else 'DRY RUN'}\n")
    
    # Sanity check the original
    original = target.read_text(encoding='utf-8')
    print(f"Original target stats:")
    print(f"  Size:                {len(original)} chars")
    print(f"  Lines:               {original.count(chr(10)) + 1}")
    print(f"  Mojibake markers:    {original.count('â€')}")
    print(f"  'The unicorn mythic voice' headers: {original.count('## The unicorn mythic voice')}")
    
    # Load cleaned, fix line endings + mojibake + sources dedup
    raw = args.cleaned.read_bytes()
    # Normalize line endings
    raw = raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    text = raw.decode('utf-8')
    
    # ftfy pass
    try:
        import ftfy
    except ImportError:
        raise SystemExit("ftfy is required. pip install ftfy --break-system-packages")
    
    moji_before = text.count('â€')
    text = ftfy.fix_text(text)
    moji_after = text.count('â€')
    
    # Dedupe sources
    text, dupes_removed = dedupe_sources_line(text)
    
    # Escape table-wikilink pipes (so this file is clean even if script 02 ran before)
    text, pipes_escaped = escape_pipes_in_table_wikilinks(text)
    
    print(f"\nCleaned source after processing:")
    print(f"  Size:                {len(text)} chars")
    print(f"  Lines:               {text.count(chr(10)) + 1}")
    print(f"  Mojibake markers:    {moji_before} → {moji_after}")
    print(f"  Sources duplicates removed:    {dupes_removed}")
    print(f"  Table-wikilink pipes escaped:  {pipes_escaped}")
    print(f"  'The unicorn mythic voice' headers: {text.count('## The unicorn mythic voice')}")
    
    if args.write:
        target.write_text(text, encoding='utf-8')
        print(f"\n✓ Wrote {len(text)} chars to {target}")
        print("\nSuggested commit:")
        print('  git add wiki/unicorns.md')
        print('  git commit -m "Replace unicorns.md with cleaned version (resolves 262x section duplication)"')
    else:
        print("\nDRY RUN — re-run with --write to apply.")


if __name__ == '__main__':
    main()
