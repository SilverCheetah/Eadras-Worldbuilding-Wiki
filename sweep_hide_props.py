"""
Sweep script: remove the broken show-properties toggle and the paired
`hide-props` cssclass from every wiki page.

The custom toggle never worked as intended; replaced by Obsidian's built-in
property folding (2026-05-16). This is a one-shot cleanup.

Two transformations:

1. **Toggle line removal.** Every page carries (verbatim, single line):

       <label class="show-props-label"><input type="checkbox" class="show-props-toggle"> Show properties</label>

   plus a blank line on each side. The script removes the toggle line AND
   the single blank line immediately following it, so the page goes from:

       ---
       <blank>
       <toggle>
       <blank>
       # Title

   to:

       ---
       <blank>
       # Title

2. **`hide-props` removal from cssclasses arrays.** Three variants in the
   wild:

   - `cssclasses: [hide-props]`             -> entire line removed
   - `cssclasses: [hide-props, axes-unset]` -> becomes `cssclasses: [axes-unset]`
   - `cssclasses: [axes-unset, hide-props]` -> becomes `cssclasses: [axes-unset]`

Usage:
    python sweep_hide_props.py --dry-run    # report counts, no writes
    python sweep_hide_props.py              # apply

Only files under wiki/ are touched. CLAUDE.md is intentionally NOT touched
by this script (its convention text needs a careful manual rewrite, not a
mechanical string replace). log.md may carry historical-text references to
the toggle inside log entries — those are inside prose, not at the page
header, and they will not match the standalone-line pattern. They survive.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
WIKI = REPO_ROOT / "wiki"

TOGGLE_LINE = '<label class="show-props-label"><input type="checkbox" class="show-props-toggle"> Show properties</label>'

# Pattern: toggle line on its own line, with a trailing newline, plus a
# following blank line. We remove both.
TOGGLE_BLOCK = re.compile(
    r"^" + re.escape(TOGGLE_LINE) + r"\n\n",
    re.MULTILINE,
)

# cssclasses array variants. We intentionally only match the three known
# shapes. If something exotic surfaces, the dry-run will flag it.
CSSCLASSES_ONLY = re.compile(r"^cssclasses: \[hide-props\]\n", re.MULTILINE)
CSSCLASSES_PAIRED = re.compile(
    r"^cssclasses: \[(?:hide-props, ([^\]]+)|([^\]]+), hide-props)\]\n",
    re.MULTILINE,
)


def sweep(text: str) -> tuple[str, dict[str, int]]:
    """Return (new_text, counts) where counts reports what was changed."""
    counts = {"toggle": 0, "cssclasses_only": 0, "cssclasses_paired": 0}

    new_text, n = TOGGLE_BLOCK.subn("", text)
    counts["toggle"] = n

    new_text, n = CSSCLASSES_ONLY.subn("", new_text)
    counts["cssclasses_only"] = n

    def paired_repl(match: re.Match) -> str:
        remainder = match.group(1) or match.group(2)
        return f"cssclasses: [{remainder}]\n"

    new_text, n = CSSCLASSES_PAIRED.subn(paired_repl, new_text)
    counts["cssclasses_paired"] = n

    return new_text, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would change without writing.",
    )
    args = parser.parse_args()

    files = sorted(WIKI.rglob("*.md"))
    total = {"toggle": 0, "cssclasses_only": 0, "cssclasses_paired": 0}
    changed_files: list[Path] = []

    for path in files:
        text = path.read_text(encoding="utf-8")
        new_text, counts = sweep(text)
        if new_text == text:
            continue
        changed_files.append(path)
        for k, v in counts.items():
            total[k] += v
        if not args.dry_run:
            path.write_text(new_text, encoding="utf-8")

    mode = "Would change" if args.dry_run else "Changed"
    print(f"{mode} {len(changed_files)} files.")
    print(f"  toggle-line removals:           {total['toggle']}")
    print(f"  cssclasses [hide-props] (sole): {total['cssclasses_only']}")
    print(f"  cssclasses paired:              {total['cssclasses_paired']}")

    # Sanity check: there should be NO orphan toggle lines (toggle without
    # the following blank), and no `hide-props` strings left.
    orphans_toggle = 0
    orphans_hide = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        if TOGGLE_LINE in text:
            orphans_toggle += 1
        if "hide-props" in text:
            orphans_hide += 1

    if args.dry_run:
        # During dry-run the files haven't been touched; orphans counts are
        # the current state.
        print(f"  (pre-sweep) pages still containing toggle line: {orphans_toggle}")
        print(f"  (pre-sweep) pages still containing hide-props:  {orphans_hide}")
    else:
        print(f"  pages still containing toggle line: {orphans_toggle} (should be 0)")
        print(f"  pages still containing hide-props:  {orphans_hide} (should be 0)")
        if orphans_toggle or orphans_hide:
            print("  WARNING: residual instances found. Inspect manually.")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
