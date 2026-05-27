"""
Phase 1, Step 3 — Normalize line endings and clean leading-frontmatter garbage
==============================================================================

Two related cleanups:

1. NORMALIZE LINE ENDINGS to LF (\n)
   Repository policy: every wiki file should use LF. As of audit, 1 file 
   (wiki/celestia.md) uses CRLF and all others use LF. This drifts further 
   any time files are edited in Windows tools without LF-enforcement.
   
   Optional: also write a .gitattributes file at repo root to enforce LF 
   on all wiki markdown going forward (--write-gitattributes).

2. STRIP LEADING WHITESPACE BEFORE FRONTMATTER
   Two files have whitespace before their opening `---`:
   - wiki/aramet.md: 1 leading newline
   - wiki/celestia.md: 193 bytes of CR characters (the corruption residue)
   
   YAML frontmatter must begin on line 1 of the file. Anything before it 
   is illegal per system-governance §1 and breaks some markdown processors.

USAGE
-----
    python 03-normalize-line-endings.py                       # dry run
    python 03-normalize-line-endings.py --write              # apply
    python 03-normalize-line-endings.py --write-gitattributes # also add .gitattributes
"""

import argparse
from pathlib import Path


GITATTRIBUTES_CONTENT = """\
# Normalize line endings to LF for all wiki markdown.
# Set by 03-normalize-line-endings.py per audit recommendation.
*.md text eol=lf
"""


def find_repo_root(start: Path) -> Path:
    p = start.resolve()
    for parent in [p] + list(p.parents):
        if (parent / 'wiki' / 'system-governance.md').exists():
            return parent
    raise SystemExit(f"Could not find repo root from {start}.")


def fix_file(path: Path, write: bool) -> dict:
    """
    Fixes line endings (CRLF → LF) and strips leading whitespace before 
    frontmatter. Returns a dict describing what was changed.
    """
    raw = path.read_bytes()
    report = {
        'crlf_count': raw.count(b'\r\n'),
        'lone_cr_count': raw.count(b'\r') - raw.count(b'\r\n'),
        'leading_ws_stripped': 0,
        'changed': False,
    }
    
    # Normalize line endings: CRLF → LF, lone CR → LF
    fixed = raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    
    # Strip BOM if present
    if fixed.startswith(b'\xef\xbb\xbf'):
        fixed = fixed[3:]
        report['bom_stripped'] = True
    
    # Strip leading whitespace before frontmatter
    # Files exempt from frontmatter requirement (per governance §1): 
    # index.md, log.md, naming-conventions.md
    name = path.name
    if name not in ('index.md', 'log.md', 'naming-conventions.md'):
        # Find first non-whitespace
        stripped = fixed.lstrip(b' \t\n\r')
        if stripped.startswith(b'---'):
            leading_len = len(fixed) - len(stripped)
            if leading_len > 0:
                report['leading_ws_stripped'] = leading_len
                fixed = stripped
    
    if fixed != raw:
        report['changed'] = True
        if write:
            path.write_bytes(fixed)
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Normalize line endings and clean frontmatter prefixes")
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--write-gitattributes', action='store_true',
                        help='Also write .gitattributes file at repo root')
    parser.add_argument('--repo', type=Path, default=None)
    args = parser.parse_args()
    
    repo = args.repo or find_repo_root(Path(__file__).parent)
    print(f"Repo root: {repo}")
    print(f"Mode: {'WRITE' if args.write else 'DRY RUN'}\n")
    
    affected = []
    for path in sorted(repo.glob('wiki/**/*.md')):
        if '_sealed' in path.parts or 'templates' in path.parts:
            continue
        report = fix_file(path, args.write)
        if report['changed']:
            affected.append((path, report))
    
    for path, report in affected:
        rel = path.relative_to(repo)
        notes = []
        if report['crlf_count']:
            notes.append(f"{report['crlf_count']} CRLF")
        if report['lone_cr_count']:
            notes.append(f"{report['lone_cr_count']} lone CR")
        if report['leading_ws_stripped']:
            notes.append(f"{report['leading_ws_stripped']}b leading whitespace stripped")
        if report.get('bom_stripped'):
            notes.append("BOM stripped")
        print(f"  {rel}: {'; '.join(notes)}")
    
    print(f"\nFiles modified: {len(affected)}")
    
    if args.write_gitattributes:
        gitattr = repo / '.gitattributes'
        if gitattr.exists():
            print(f"\n.gitattributes already exists; not overwriting. Current contents:")
            print(gitattr.read_text())
        else:
            if args.write:
                gitattr.write_text(GITATTRIBUTES_CONTENT)
                print(f"\nWrote {gitattr}")
            else:
                print(f"\nWould write to {gitattr}:")
                print(GITATTRIBUTES_CONTENT)
    
    if args.write:
        print("\nSuggested commit:")
        print('  git add -A')
        print('  git commit -m "Normalize line endings to LF; strip leading garbage from celestia.md and aramet.md"')
    else:
        print("\nDRY RUN — re-run with --write to apply.")


if __name__ == '__main__':
    main()
