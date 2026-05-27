"""
Phase 1, Step 1 — Mojibake sweep
=================================

Fixes UTF-8 → cp1252 → UTF-8 round-trip corruption across the wiki.
Uses ftfy library (the de-facto standard for this fix).

WHAT IT FIXES
-------------
Signature byte triplet `â€` (0xc3 0xa2 0xe2 0x82 0xac) and its variants:
    â€"   →  —    (em dash)
    â€"   →  –    (en dash)
    â€™   →  '    (right single quote)
    â€˜   →  '    (left single quote)
    â€œ   →  "    (left double quote)
    â€\x9d →  "    (right double quote)
    â€¦   →  …    (ellipsis)
    â†'   →  →    (right arrow)
    â†'   →  ←    (left arrow)
    â†•   →  ↕    (up-down arrow)
    â†"   →  ↑    (up arrow)
    â†"   →  ↓    (down arrow)
    â‰¥   →  ≥    (greater-equal)
    â‰¤   →  ≤    (less-equal)
    â‰ ́   →  ≠    (not-equal)
    â‚‚   →  ₂    (subscript 2 etc.)
    â€¢   →  •    (bullet)

WHY NOT A NAIVE encode('latin-1').decode('utf-8') APPROACH
----------------------------------------------------------
Files contain a MIX of correctly-encoded UTF-8 (real em dashes, accents)
and mojibaked UTF-8. The naive approach crashes on legitimate UTF-8.
ftfy detects and fixes only the corrupted runs and leaves correct UTF-8 alone.

USAGE
-----
    # Dry run (default) — shows what would change without writing
    python 01-fix-mojibake.py

    # Apply changes
    python 01-fix-mojibake.py --write

    # Show full diffs (not just counts)
    python 01-fix-mojibake.py --verbose

    # Limit to specific files (relative paths from repo root)
    python 01-fix-mojibake.py --files wiki/unicorns.md wiki/inspirations.md

SAFETY
------
- Default mode is DRY RUN. Nothing is written unless --write is passed.
- The script is idempotent: running it twice has the same effect as running it once.
- ftfy is conservative: if it can't confidently fix a sequence, it leaves it alone.
- After running, do `git diff --stat` to see scope, `git diff` to spot-check,
  and commit only when satisfied. Git's history is the safety net per
  system-governance §6.

REPO PATH
---------
Default repo root is auto-detected: looks for `wiki/system-governance.md` 
starting from the script's directory and walking up. Override with --repo.
"""

import argparse
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    """Walk up from start looking for the marker file."""
    p = start.resolve()
    for parent in [p] + list(p.parents):
        if (parent / 'wiki' / 'system-governance.md').exists():
            return parent
    raise SystemExit(
        f"Could not find wiki/system-governance.md walking up from {start}. "
        f"Pass --repo explicitly."
    )


def collect_files(repo: Path, filter_paths: list[str] | None) -> list[Path]:
    """Collect all .md files to process, excluding _sealed and templates."""
    if filter_paths:
        return [repo / p for p in filter_paths if (repo / p).exists()]
    
    files = []
    for path in sorted(repo.glob('wiki/**/*.md')):
        # Skip sealed and templates per governance §4 and §1
        if '_sealed' in path.parts or 'templates' in path.parts:
            continue
        files.append(path)
    return files


def fix_file(path: Path, write: bool, verbose: bool) -> tuple[int, int, list[tuple[str, str]]]:
    """
    Fix a single file. Returns (mojibake_before, mojibake_after, sample_diffs).
    """
    try:
        import ftfy
    except ImportError:
        raise SystemExit(
            "ftfy is required. Install with: pip install ftfy --break-system-packages"
        )
    
    text = path.read_text(encoding='utf-8')
    
    # Count mojibake markers in the original
    moji_before = text.count('â€') + text.count('â†') + text.count('â‚') + text.count('â‰')
    
    if moji_before == 0:
        return (0, 0, [])
    
    fixed = ftfy.fix_text(text)
    moji_after = fixed.count('â€') + fixed.count('â†') + fixed.count('â‚') + fixed.count('â‰')
    
    # Collect sample diffs (up to 3 changed lines)
    sample_diffs = []
    if verbose:
        for a, b in zip(text.split('\n'), fixed.split('\n')):
            if a != b:
                sample_diffs.append((a[:160], b[:160]))
                if len(sample_diffs) >= 3:
                    break
    
    if write and text != fixed:
        path.write_text(fixed, encoding='utf-8')
    
    return (moji_before, moji_after, sample_diffs)


def main():
    parser = argparse.ArgumentParser(description="Sweep mojibake from the Eadras wiki")
    parser.add_argument('--write', action='store_true',
                        help='Actually write changes (default: dry run)')
    parser.add_argument('--verbose', action='store_true',
                        help='Show before/after sample for each changed file')
    parser.add_argument('--repo', type=Path, default=None,
                        help='Path to repo root (default: auto-detect)')
    parser.add_argument('--files', nargs='+', default=None,
                        help='Specific files to process (paths relative to repo root)')
    args = parser.parse_args()
    
    repo = args.repo or find_repo_root(Path(__file__).parent)
    print(f"Repo root: {repo}")
    print(f"Mode: {'WRITE' if args.write else 'DRY RUN (no files will be modified)'}")
    
    files = collect_files(repo, args.files)
    print(f"Auditing {len(files)} files\n")
    
    total_before = 0
    total_after = 0
    files_changed = 0
    
    for path in files:
        rel = path.relative_to(repo)
        before, after, diffs = fix_file(path, args.write, args.verbose)
        if before > 0:
            files_changed += 1
            total_before += before
            total_after += after
            print(f"  {before:5d} → {after:3d}  {rel}")
            if args.verbose and diffs:
                for a, b in diffs:
                    print(f"      - {a}")
                    print(f"      + {b}")
                print()
    
    print()
    print(f"Files with mojibake: {files_changed}")
    print(f"Total mojibake markers: {total_before} → {total_after}")
    
    if args.write:
        print()
        print("Changes written. Next steps:")
        print("  1. cd into the repo")
        print("  2. git diff --stat   (verify scope matches)")
        print("  3. git diff wiki/some-file.md   (spot-check a representative file)")
        print("  4. git add -A && git commit -m 'Sweep mojibake from 227 wiki files (ftfy)'")
        print("  5. git push")
    else:
        print()
        print("DRY RUN — no files were modified.")
        print("Re-run with --write to apply changes.")


if __name__ == '__main__':
    main()
