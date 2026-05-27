"""
Phase 2, Step 6 — Sweep references to deprecated stub pages
============================================================

Three pages were correctly set to `canon_status: [deprecated]` on 2026-05-14:
    - wiki/dashar.md
    - wiki/heart-of-the-goddess.md
    - wiki/weavespinners.md

Per system-governance §4, after deprecation: "Redirect wikilinks from other 
pages to the new canonical target." This was not done. References to the 
three stubs fall into four categories:

A. CLEAN RELATED-LIST ITEMS — auto-fixable.
   Lines like `- [[dashar]]` standing alone in a Related-pages list. The 
   script removes these (deprecated page shouldn't be in active Related lists).

B. META / AUDIT PAGES — intentionally preserved.
   `open-questions.md`, `worldbuilding-needs.md`, `index.md`, `inspirations.md`, 
   and `log.md` all reference the deprecated pages on purpose: they document 
   the deprecation history, list the deprecated pages explicitly, or preserve 
   the OOC inspiration trail. Skipped.

C. PLACE-NAME BODY-TEXT — flagged for authorial decision.
   Several active canon pages use "Heart of the Goddess" as a metaphysical 
   PLACE that characters interact with (Lirra's eyes appear there; players 
   can walk into it). The 2026-05-14 deprecation retired the mechanism by 
   which sorcerers transmuted into Da'shar there — but the place itself 
   was never declared retired. This needs an authorial call.

D. MECHANISM BODY-TEXT — flagged for authorial decision.
   `lirra.md` L116 has a table row describing Lirra's relationship with 
   Da'shar as a category — the actual deprecated mechanism. Authorial 
   call: keep with a "(formerly)" annotation, or remove the row.

USAGE
-----
    python 06-sweep-deprecated-refs.py            # dry run, full report
    python 06-sweep-deprecated-refs.py --write    # apply category A only
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


DEPRECATED_SLUGS = ['dashar', 'heart-of-the-goddess', 'weavespinners']

META_SKIP_FILES = {
    'open-questions.md',
    'worldbuilding-needs.md',
    'index.md',
    'inspirations.md',
    'log.md',
}


def remove_list_item_link(text: str, slug: str) -> tuple[str, int]:
    pat = re.compile(
        r'^[ \t]*-[ \t]+\[\[' + re.escape(slug) + r'\]\][ \t]*\n',
        re.MULTILINE,
    )
    matches = pat.findall(text)
    new_text = pat.sub('', text)
    return new_text, len(matches)


def find_body_text_refs(repo: Path) -> dict:
    result = {slug: [] for slug in DEPRECATED_SLUGS}
    for path in repo.glob('wiki/**/*.md'):
        if '_sealed' in path.parts or 'templates' in path.parts:
            continue
        if path.name in META_SKIP_FILES:
            continue
        if path.stem in DEPRECATED_SLUGS:
            continue
        text = path.read_text(encoding='utf-8')
        lines = text.split('\n')
        for slug in DEPRECATED_SLUGS:
            for m in re.finditer(
                r'\[\[' + re.escape(slug) + r'(?:#[^\]\|]*)?(?:\\?\|[^\]]+)?\]\]',
                text
            ):
                line_no = text[:m.start()].count('\n') + 1
                line = lines[line_no - 1].strip()
                if re.match(
                    r'^-[ \t]+\[\[' + re.escape(slug) + r'\]\][ \t]*$',
                    line
                ):
                    continue
                result[slug].append((path, line_no, line))
    return result


def classify_body_ref(line: str) -> str:
    if line.strip().startswith('|'):
        return 'table'
    if 'heart-of-the-goddess' in line.lower() and any(
        kw in line.lower() for kw in ['in the', 'walk into', 'step into', 'inside']
    ):
        return 'place'
    return 'other'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--repo', type=Path, default=None)
    args = parser.parse_args()
    
    repo = args.repo or find_repo_root(Path(__file__).parent)
    print(f"Repo root: {repo}")
    print(f"Mode: {'WRITE' if args.write else 'DRY RUN'}\n")
    
    # === A. Clean Related-list removals ===
    print("=" * 60)
    print("A. Related-list item removals (AUTO-FIXED)")
    print("=" * 60)
    
    file_changes = {}
    total_a = 0
    for path in repo.glob('wiki/**/*.md'):
        if '_sealed' in path.parts or 'templates' in path.parts:
            continue
        if path.name in META_SKIP_FILES:
            continue
        if path.stem in DEPRECATED_SLUGS:
            continue
        text = path.read_text(encoding='utf-8')
        original = text
        for slug in DEPRECATED_SLUGS:
            text, n = remove_list_item_link(text, slug)
            if n:
                print(f"  {path.relative_to(repo)}: removed {n}x `- [[{slug}]]`")
                total_a += n
        if text != original:
            file_changes[path] = text
    
    print(f"\n  Total Related-list removals: {total_a}")
    
    # === B. Meta-page skips (informational) ===
    print()
    print("=" * 60)
    print("B. Meta-page references (PRESERVED — historical record)")
    print("=" * 60)
    print()
    for fname in sorted(META_SKIP_FILES):
        path = repo / 'wiki' / fname
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        for slug in DEPRECATED_SLUGS:
            cnt = len(list(re.finditer(
                r'\[\[' + re.escape(slug) + r'(?:#[^\]\|]*)?(?:\\?\|[^\]]+)?\]\]',
                text
            )))
            if cnt:
                print(f"  wiki/{fname}: {cnt}x [[{slug}]]  — preserved")
    
    # === C & D. Body-text refs (manual review) ===
    body_refs = find_body_text_refs(repo)
    
    print()
    print("=" * 60)
    print("C. Place-name body-text references (AUTHORIAL DECISION)")
    print("=" * 60)
    print()
    print("These reference 'Heart of the Goddess' as a metaphysical place")
    print("that characters interact with. The 2026-05-14 deprecation retired")
    print("the sorcerer-transmutation MECHANISM, not the place itself.")
    print()
    print("DECISION: For each, choose one of:")
    print("  (a) Keep the place-name, mark the mechanism as historical")
    print("  (b) Rename to a new canonical location")
    print("  (c) Remove the sentence entirely")
    print()
    
    place_refs = []
    for slug, refs in body_refs.items():
        for path, ln, line in refs:
            if classify_body_ref(line) == 'place':
                place_refs.append((path, ln, slug, line))
    
    for path, ln, slug, line in sorted(place_refs):
        print(f"  {path.relative_to(repo)}:{ln}  ({slug})")
        print(f"    {line[:180]}")
        print()
    
    print()
    print("=" * 60)
    print("D. Mechanism / table body-text references (AUTHORIAL DECISION)")
    print("=" * 60)
    print()
    
    mech_refs = []
    for slug, refs in body_refs.items():
        for path, ln, line in refs:
            kind = classify_body_ref(line)
            if kind != 'place':
                mech_refs.append((path, ln, slug, line))
    
    for path, ln, slug, line in sorted(mech_refs):
        print(f"  {path.relative_to(repo)}:{ln}  ({slug})")
        print(f"    {line[:180]}")
        print()
    
    print(f"Total body-text refs needing decision: {len(place_refs) + len(mech_refs)}")
    print(f"  Place references:     {len(place_refs)}")
    print(f"  Mechanism references: {len(mech_refs)}")
    
    if args.write and file_changes:
        for path, text in file_changes.items():
            path.write_text(text, encoding='utf-8')
        print()
        print("✓ Applied category-A fixes.")
        print()
        print("Suggested commit:")
        print('  git add -A')
        print('  git commit -m "Sweep deprecated-stub references from Related lists"')
    elif not args.write:
        print()
        print("DRY RUN — re-run with --write to apply category-A fixes.")
        print("Categories B/C/D are informational only and require manual decisions.")


if __name__ == '__main__':
    main()
