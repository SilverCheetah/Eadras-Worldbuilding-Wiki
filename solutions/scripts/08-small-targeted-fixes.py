"""
Phase 2, Step 8 — Targeted small fixes
========================================

Catches the small, locatable issues that don't justify their own scripts:

1. TYPO WIKILINKS
   Sweep specific known-typo wikilinks to their correct targets:
       [[velrathi-tea-tradition]]                            → [[velrathi-tea-culture]]
       [[flesh-crafters]]                                    → [[flesh-eaters]]
       [[mythic-retellings-of-the-cataclysm-and-demon-war]]  → [[mythic-recitations]]
       [[ascended-mortal-deities-mechanism]]                 → [[apotheosis]]
   
   These are pages that DO exist under a slightly different slug. The 
   broken links can be redirected mechanically.

2. WIKI-PAGE-1 / WIKI-PAGE-2 PLACEHOLDER LEAK
   wiki/inspirations.md contains `[[wiki-page-1]]` and `[[wiki-page-2]]` 
   placeholders that escaped a template. These are reported (but not 
   auto-fixed — authorial intent needed to know what they should be).

3. DWARVES.MD DUPLICATE `## Naming`
   wiki/dwarves.md has two `## Naming` H2 sections covering different 
   topics. The first (L21) is about race etymology (Shada'din vs 
   Dwarves); the second (L139) is about personal naming conventions. 
   Renames the first to `## Etymology` to disambiguate.

4. ORDER-SWORN-SORCERERS REFERENCES
   `wiki/inspirations.md` references `[[order-sworn-sorcerers]]` — the 
   page was renamed to `[[order-sworn-netharim]]` in the magic-system 
   rework. Sweep the rename.
   
   (`wiki/log.md` also has these; left alone as historical record.)

USAGE
-----
    python 08-small-targeted-fixes.py            # dry run
    python 08-small-targeted-fixes.py --write    # apply
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


# (old_slug, new_slug)
TYPO_REDIRECTS = [
    ('velrathi-tea-tradition',                            'velrathi-tea-culture'),
    ('flesh-crafters',                                    'flesh-eaters'),
    ('mythic-retellings-of-the-cataclysm-and-demon-war',  'mythic-recitations'),
    ('ascended-mortal-deities-mechanism',                 'apotheosis'),
]

# (old_slug, new_slug) — apply only to specified files; skip log.md (history)
RENAME_REDIRECTS = [
    ('order-sworn-sorcerers', 'order-sworn-netharim'),
]
RENAME_SKIP_FILES = {'log.md'}  # historical record


def redirect_wikilink(text: str, old_slug: str, new_slug: str) -> tuple[str, int]:
    """
    Replace [[old_slug]] or [[old_slug|Display]] or [[old_slug#anchor|Display]] etc.
    with the equivalent pointing at new_slug. Returns (new_text, num_replaced).
    """
    pat = re.compile(
        r'\[\[' + re.escape(old_slug) + r'(\#[^\]\|]*)?(\\?\|[^\]]+)?\]\]'
    )
    matches = pat.findall(text)
    new_text = pat.sub(
        lambda m: f'[[{new_slug}{m.group(1) or ""}{m.group(2) or ""}]]',
        text
    )
    return new_text, len(matches)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--repo', type=Path, default=None)
    args = parser.parse_args()
    
    repo = args.repo or find_repo_root(Path(__file__).parent)
    print(f"Repo root: {repo}")
    print(f"Mode: {'WRITE' if args.write else 'DRY RUN'}\n")
    
    file_changes = {}  # path -> new_text
    
    def load(path):
        if path not in file_changes:
            file_changes[path] = path.read_text(encoding='utf-8')
        return file_changes[path]
    
    # 1. Typo redirects across all files (skip log.md as historical record)
    TYPO_SKIP_FILES = {'log.md'}
    print("=== Typo wikilink redirects ===")
    for old, new in TYPO_REDIRECTS:
        total = 0
        for path in repo.glob('wiki/**/*.md'):
            if '_sealed' in path.parts or 'templates' in path.parts:
                continue
            if path.name in TYPO_SKIP_FILES:
                continue
            text = load(path)
            new_text, n = redirect_wikilink(text, old, new)
            if n:
                total += n
                file_changes[path] = new_text
                print(f"  {path.relative_to(repo)}: {n}x [[{old}]] → [[{new}]]")
        if total == 0:
            print(f"  (no instances of [[{old}]] found outside skip-list)")
    
    # 2. Rename redirects (skip historical files)
    print("\n=== Rename redirects ===")
    for old, new in RENAME_REDIRECTS:
        total = 0
        for path in repo.glob('wiki/**/*.md'):
            if '_sealed' in path.parts or 'templates' in path.parts:
                continue
            if path.name in RENAME_SKIP_FILES:
                continue
            text = load(path)
            new_text, n = redirect_wikilink(text, old, new)
            if n:
                total += n
                file_changes[path] = new_text
                print(f"  {path.relative_to(repo)}: {n}x [[{old}]] → [[{new}]]")
        if total == 0:
            print(f"  (no instances of [[{old}]] found outside skip-list)")
    
    # 3. Dwarves.md duplicate ## Naming → first becomes ## Etymology
    print("\n=== dwarves.md ## Naming → ## Etymology ===")
    dwarves_path = repo / 'wiki' / 'dwarves.md'
    if dwarves_path.exists():
        text = load(dwarves_path)
        # The first ## Naming covers race-etymology; rename it to ## Etymology
        # We do this by finding the FIRST occurrence and replacing only that
        # (not the second one, which is about personal names)
        first = text.find('\n## Naming\n')
        if first >= 0:
            new_text = text[:first] + '\n## Etymology\n' + text[first + len('\n## Naming\n'):]
            file_changes[dwarves_path] = new_text
            print(f"  Renamed first '## Naming' (L{text[:first].count(chr(10))+2}) to '## Etymology'")
        else:
            print("  (No '## Naming' found; already renamed?)")
    
    # 4. Report (don't auto-fix) the inspirations.md template-leak — but skip
    #    placeholders that are inside HTML comment blocks (intentional templates).
    print("\n=== Manual-review items ===")
    print()
    insp_path = repo / 'wiki' / 'inspirations.md'
    if insp_path.exists():
        text = load(insp_path)
        # Strip HTML comments to find placeholders that ARE in live prose
        live_text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
        found_any = False
        for marker in ['[[wiki-page-1]]', '[[wiki-page-2]]']:
            if marker in live_text:
                # Find line number in original text (not comment-stripped)
                for i, ln in enumerate(text.split('\n')):
                    if marker in ln:
                        # Check this specific line isn't inside a comment
                        line_pos = sum(len(l)+1 for l in text.split('\n')[:i])
                        before = text[:line_pos]
                        # Inside comment if last <!-- is later than last -->
                        if before.rfind('<!--') > before.rfind('-->'):
                            continue  # inside a comment
                        found_any = True
                        print(f"  wiki/inspirations.md:{i+1} contains placeholder {marker}")
                        print(f"    {ln.strip()[:180]}")
                        print(f"    → Replace with the actual influences being documented.")
                        print()
                        break
        if not found_any:
            print("  inspirations.md placeholders found only inside HTML comments (intentional template);")
            print("  no action required.")
            print()
    
    # Apply
    if args.write:
        for path, new_text in file_changes.items():
            path.write_text(new_text, encoding='utf-8')
        print(f"\n✓ Wrote {len(file_changes)} files")
        print("\nSuggested commit:")
        print('  git add -A')
        print('  git commit -m "Sweep typo wikilinks; rename order-sworn-sorcerers→netharim outside log; clean dwarves Naming dup"')
    else:
        print(f"\nDRY RUN — would write {sum(1 for p, t in file_changes.items() if t != p.read_text(encoding='utf-8'))} files")
        print("Re-run with --write to apply.")


if __name__ == '__main__':
    main()
