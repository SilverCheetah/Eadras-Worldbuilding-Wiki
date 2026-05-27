"""
Phase 2, Step 5 — Finalize system-governance.md Section 6
==========================================================

Cleanup tasks:

1. REMOVE the stale "## 6. Backups and Exports" header (it was left in place 
   when the section body was replaced; both `## 6.` headers are currently 
   stacked back-to-back).

2. REMOVE the [#anchor](#anchor) self-anchor lines under each subheading in 
   Section 6 — they are inconsistent with the rest of the document (no other 
   section uses this convention).

3. UPDATE the `Last updated:` date to today (or a date passed in).

This script operates on the local repo's wiki/system-governance.md. If you 
have a refreshed version sitting in another location, pass --source to point 
at it; the script will apply the cleanup to that version and write the result 
to the repo.

USAGE
-----
    # Use the in-repo version as input
    python 05-fix-governance-section-6.py            # dry run
    python 05-fix-governance-section-6.py --write   # apply

    # Use an external source (e.g., uploaded refresh)
    python 05-fix-governance-section-6.py --source /path/to/system-governance.md --write

    # Specify the Last-updated date
    python 05-fix-governance-section-6.py --date 2026-05-27 --write

SAFETY
------
- Dry run by default.
- Idempotent: removes the duplicate header and anchor lines if present; 
  no-op if already cleaned.
- Asserts that exactly one ## 6. header remains after cleanup.
"""

import argparse
import re
from datetime import date
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    p = start.resolve()
    for parent in [p] + list(p.parents):
        if (parent / 'wiki' / 'system-governance.md').exists():
            return parent
    raise SystemExit(f"Could not find repo root from {start}.")


def clean_governance(text: str, new_date: str) -> tuple[str, list[str]]:
    """Apply the three cleanups. Returns (new_text, list_of_actions_taken)."""
    actions = []
    
    # 1. Remove "## 6. Backups and Exports" header if it sits immediately above "## 6. Backups and Recovery"
    pat_double_header = re.compile(
        r'## 6\. Backups and Exports\s*\n\s*\n## 6\. Backups and Recovery',
        re.MULTILINE
    )
    if pat_double_header.search(text):
        text = pat_double_header.sub('## 6. Backups and Recovery', text)
        actions.append("Removed stale '## 6. Backups and Exports' header")
    
    # 2. Remove [#anchor](#anchor) self-anchor lines that immediately follow headers
    # Pattern: a line like "[#xxx](#xxx)" (just the bracketed link, possibly with surrounding blank lines)
    pat_anchor = re.compile(
        r'\n\[#([a-z0-9-]+)\]\(#\1\)\n',
        re.MULTILINE
    )
    matches = list(pat_anchor.finditer(text))
    if matches:
        text = pat_anchor.sub('\n', text)
        actions.append(f"Removed {len(matches)} self-anchor [#x](#x) line(s)")
    
    # 3. Update Last-updated date
    pat_date = re.compile(r'^\*\*Last updated\*\*:\s*\d{4}-\d{2}-\d{2}', re.MULTILINE)
    if pat_date.search(text):
        text = pat_date.sub(f'**Last updated**: {new_date}', text)
        actions.append(f"Updated Last-updated to {new_date}")
    
    # Sanity check: exactly one ## 6. header
    section_6_count = len(re.findall(r'^## 6\.', text, re.MULTILINE))
    if section_6_count != 1:
        raise SystemExit(
            f"Sanity check failed: expected exactly one '## 6.' header after cleanup, "
            f"got {section_6_count}. Aborting."
        )
    
    return text, actions


def main():
    parser = argparse.ArgumentParser(description="Finalize system-governance.md Section 6")
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--source', type=Path, default=None,
                        help='External source file (default: wiki/system-governance.md in repo)')
    parser.add_argument('--date', default=None,
                        help='Last-updated date in YYYY-MM-DD format (default: today)')
    parser.add_argument('--repo', type=Path, default=None)
    args = parser.parse_args()
    
    repo = args.repo or find_repo_root(Path(__file__).parent)
    target = repo / 'wiki' / 'system-governance.md'
    source = args.source or target
    new_date = args.date or date.today().isoformat()
    
    print(f"Repo root: {repo}")
    print(f"Source:    {source}")
    print(f"Target:    {target}")
    print(f"Date:      {new_date}")
    print(f"Mode:      {'WRITE' if args.write else 'DRY RUN'}\n")
    
    text = source.read_text(encoding='utf-8')
    new_text, actions = clean_governance(text, new_date)
    
    if not actions:
        print("Nothing to do — Section 6 already clean.")
        return
    
    print("Actions taken:")
    for a in actions:
        print(f"  ✓ {a}")
    
    print(f"\nSize: {len(text)} → {len(new_text)} chars")
    
    if args.write:
        target.write_text(new_text, encoding='utf-8')
        print(f"\n✓ Wrote {target}")
        print("\nSuggested commit:")
        print('  git add wiki/system-governance.md')
        print('  git commit -m "Finalize system-governance §6 (git workflow; closes 2026-05-15 todo)"')
    else:
        print("\nDRY RUN — re-run with --write to apply.")


if __name__ == '__main__':
    main()
