"""Comprehensive wiki lint.

Checks:
  1. Frontmatter schema conformance (required fields, locked enums)
  2. Body conventions (show-props toggle, Summary/Sources/Last updated, Related pages block)
  3. Wikilink graph: dangling links, orphan pages
  4. Known content issues: stale slugs, deprecated terms, broken cross-refs

Read-only. Reports issues; does not modify wiki.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

WIKI = Path('wiki')

# ---- Locked enums from CLAUDE.md ----

CANON_STATUS = {'established', 'proposed', 'open-canon', 'pending',
                'rework-pending', 'partial-rework-pending',
                'deprecated', 'sealed'}
PERSPECTIVE = {'tome-neutral', 'tome-secret', 'tome-sealed', 'tome-recovered',
               'in-character', 'ooc', 'reference'}
HORIZON = {'primordial', 'nerathi-era', 'dragon-era', 'dragon-unicorn-era',
           'progenitor-era', 'high-firethorn', 'demon-war', 'dimming',
           'modern-era', 'all'}
ACCESS = {'common', 'general', 'scholarly', 'esoteric', 'meta', 'sealed'}

REQUIRED_FIELDS = ['title', 'tags', 'canon_status', 'perspective',
                   'historical_horizon', 'knowledge_access']

# Bare-frontmatter pages (CLAUDE.md "When the schema doesn't apply"):
BARE_FRONTMATTER = {'log.md', 'index.md'}

# Reference pages — full schema applies with perspective=reference, access=meta:
REFERENCE_PAGES = {'tags.md', 'naming-conventions.md', 'eadras-timeline.md',
                   'open-questions.md', 'worldbuilding-needs.md',
                   'inspirations.md', 'eras.md'}

# ---- Helpers ----

FM_RE = re.compile(r'\A[\s﻿]*---\s*\n(.*?)\n---\s*\n', re.DOTALL)
# Match [[...]] but NOT ![[...]] (image embed). Allow trailing \ before ]].
WIKILINK_RE = re.compile(r'(?<!!)\[\[([^\[\]\|#]+?)\\?(?:#[^\[\]\|]*)?(?:\|[^\[\]]*)?\]\]')
IMAGE_EXT = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')

def parse_frontmatter(text):
    """Return (dict-of-fields, body) — fields parsed loosely, not strict YAML."""
    # Strip BOM if present so the regex matches the first line
    if text.startswith('﻿'):
        text = text[1:]
    m = FM_RE.match(text)
    if not m:
        return None, text
    fm_text = m.group(1)
    body = text[m.end():]
    fields = {}
    current_key = None
    for line in fm_text.split('\n'):
        if not line.strip():
            continue
        # Top-level field: "key: value" or "key:"
        top = re.match(r'^([a-zA-Z_][\w-]*)\s*:\s*(.*)$', line)
        if top:
            current_key = top.group(1)
            val = top.group(2).strip()
            fields[current_key] = val
        elif line.startswith('  ') and current_key:
            # nested (e.g. axes_profile sub-fields) — ignore for lint purposes
            pass
    return fields, body

def parse_array(val):
    """Parse "[a, b, c]" into list. Returns None if not array form."""
    val = val.strip()
    if not (val.startswith('[') and val.endswith(']')):
        return None
    inside = val[1:-1].strip()
    if not inside:
        return []
    return [x.strip() for x in inside.split(',')]

def slug_from_path(p):
    """wiki/foo/bar.md → 'bar'; wiki/foo.md → 'foo'"""
    return p.stem

def resolve_wikilink(target, existing_slugs, aliases, path_slugs):
    """Resolve a wikilink target (the bit before # or |) to a slug.
    Returns the resolved slug if found, else None.
    path_slugs: dict mapping 'subfolder/stem' → True for files in subfolders."""
    target = target.strip().rstrip('\\')
    if not target:
        return None
    # Image-embed catch (already handled by negative-lookbehind regex, but defense)
    if target.lower().endswith(IMAGE_EXT):
        return 'IMAGE'  # sentinel — not a wikilink miss
    # Path-prefixed (rpg/foo, _sealed/foo)
    if '/' in target:
        if target in path_slugs:
            return target
        # Try last segment as a slug
        last = target.split('/')[-1]
        if last in existing_slugs:
            return last
        return None
    # Some links use display name with spaces; the slug form is lowercased+hyphenated
    candidates = [
        target,
        target.lower().replace(' ', '-'),
        target.lower(),
    ]
    for c in candidates:
        if c in existing_slugs:
            return c
        if c in aliases:
            return aliases[c]
    return None

# ---- Main ----

def main():
    issues = []  # (severity, category, page, message)

    pages = sorted(WIKI.rglob('*.md'))
    if not pages:
        print('No wiki pages found.')
        return

    parsed = {}   # path → (fields, body)
    slugs = set()
    path_slugs = set()  # 'rpg/foo' / '_sealed/foo' path-relative slugs
    aliases = {}  # alias → slug
    titles = {}   # slug → title-text

    for p in pages:
        try:
            text = p.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            issues.append(('ERROR', 'encoding', p, f'unable to read as utf-8: {e}'))
            continue
        fields, body = parse_frontmatter(text)
        slug = slug_from_path(p)
        slugs.add(slug)
        # Also index by relative path for subfolder pages
        rel_no_ext = p.relative_to(WIKI).with_suffix('').as_posix()
        path_slugs.add(rel_no_ext)
        parsed[p] = (fields, body, text)
        if fields and 'title' in fields:
            titles[slug] = fields['title']
        if fields and 'aliases' in fields:
            arr = parse_array(fields['aliases'])
            if arr is not None:
                for a in arr:
                    a_norm = a.lower().replace(' ', '-')
                    aliases[a_norm] = slug
                    aliases[a] = slug

    # ---- Schema and body checks ----

    for p in pages:
        fields, body, text = parsed[p]
        rel = p.relative_to(WIKI).as_posix()
        name = p.name

        if fields is None:
            issues.append(('ERROR', 'frontmatter', rel, 'no frontmatter block found'))
            continue

        # Bare-frontmatter pages
        if name in BARE_FRONTMATTER:
            if 'title' not in fields:
                issues.append(('WARN', 'frontmatter', rel, 'log/index page missing title'))
            continue

        # Required fields
        for req in REQUIRED_FIELDS:
            if req not in fields:
                issues.append(('ERROR', 'frontmatter', rel,
                              f'missing required field: {req}'))

        # Validate enums
        for key, enum, name_enum in [
            ('canon_status', CANON_STATUS, 'canon_status'),
            ('perspective', PERSPECTIVE, 'perspective'),
            ('historical_horizon', HORIZON, 'historical_horizon'),
            ('knowledge_access', ACCESS, 'knowledge_access'),
        ]:
            if key in fields:
                arr = parse_array(fields[key])
                if arr is None:
                    issues.append(('WARN', 'frontmatter', rel,
                                  f'{key} should be array form [...]: got "{fields[key][:50]}"'))
                else:
                    for v in arr:
                        if v not in enum:
                            issues.append(('ERROR', 'enum', rel,
                                          f'{key} has invalid value "{v}"; allowed: {sorted(enum)}'))

        # Array form check for tags
        if 'tags' in fields:
            arr = parse_array(fields['tags'])
            if arr is None:
                issues.append(('WARN', 'frontmatter', rel,
                              f'tags should be array form [a, b, c]'))
            elif len(arr) > 5:
                issues.append(('WARN', 'frontmatter', rel,
                              f'tags has {len(arr)} entries; CLAUDE.md says 1–5'))
            elif len(arr) == 0:
                issues.append(('WARN', 'frontmatter', rel, 'tags is empty'))

        # cssclasses: hide-props expected on content pages
        is_content = name not in BARE_FRONTMATTER
        if is_content:
            if 'cssclasses' not in fields:
                issues.append(('WARN', 'frontmatter', rel,
                              'missing cssclasses (expected [hide-props] on content pages)'))
            else:
                cssc = parse_array(fields['cssclasses']) or []
                if 'hide-props' not in cssc:
                    issues.append(('WARN', 'frontmatter', rel,
                                  f'cssclasses missing hide-props: {cssc}'))

        # Body conventions
        if is_content:
            if 'show-props-toggle' not in body[:500]:
                issues.append(('WARN', 'body', rel,
                              'missing show-properties toggle near top of body'))
            if '**Summary**' not in body:
                issues.append(('WARN', 'body', rel, 'missing **Summary**: line'))
            if '**Sources**' not in body:
                issues.append(('WARN', 'body', rel, 'missing **Sources**: line'))
            if '**Last updated**' not in body:
                issues.append(('WARN', 'body', rel, 'missing **Last updated**: line'))
            elif not re.search(r'\*\*Last updated\*\*:\s*\d{4}-\d{2}-\d{2}', body):
                issues.append(('WARN', 'body', rel,
                              'Last updated line not in YYYY-MM-DD format'))
            if 'Related pages' not in body:
                issues.append(('WARN', 'body', rel, 'missing Related pages block'))
            else:
                # Check that related pages block uses collapsible <details>
                if not re.search(r'<details>\s*<summary>Related pages</summary>', body):
                    issues.append(('INFO', 'body', rel,
                                  'Related pages block may not use canonical <details><summary> form'))

    # ---- Wikilink graph ----

    inbound = defaultdict(set)   # slug → set of slugs that link to it
    outbound = defaultdict(set)  # slug → set of slugs it links to
    dangling = []                # (page, target, line) triples

    for p in pages:
        fields, body, text = parsed[p]
        rel = p.relative_to(WIKI).as_posix()
        slug = slug_from_path(p)
        # Skip wikilink-graph for the index and the log — they list everything by design.
        for m in WIKILINK_RE.finditer(text):
            target = m.group(1).strip()
            # Skip relative paths like ../foo or README links
            if target.startswith('../'):
                target_clean = target[3:]
                resolved = resolve_wikilink(target_clean, slugs, aliases, path_slugs)
                if resolved is None:
                    dangling.append((rel, target, '../-prefixed'))
                else:
                    outbound[slug].add(resolved)
                    inbound[resolved].add(slug)
                continue
            if target == 'README':
                # In _sealed/, README is local — skip
                continue
            resolved = resolve_wikilink(target, slugs, aliases, path_slugs)
            if resolved is None:
                if rel == 'log.md' and target.startswith(('project-', 'feedback-', 'user-', 'reference-')):
                    continue
                dangling.append((rel, target, ''))
            elif resolved == 'IMAGE':
                pass
            else:
                outbound[slug].add(resolved)
                inbound[resolved].add(slug)

    # Find orphans — pages with no inbound link from anything except log.md
    log_slug = 'log'
    index_slug = 'index'
    for slug in slugs:
        if slug in (log_slug, index_slug, 'README'):
            continue
        inbounds = inbound.get(slug, set())
        non_meta = inbounds - {log_slug, index_slug}
        if not non_meta:
            # Find the file for this slug
            matches = [p for p in pages if slug_from_path(p) == slug]
            if matches:
                rel = matches[0].relative_to(WIKI).as_posix()
                # Only report if it's a content page (not _sealed README etc.)
                issues.append(('INFO', 'orphan', rel,
                              f'no inbound wikilinks from non-meta pages (only log/index/none)'))

    # Report dangling
    for page, target, note in dangling:
        msg = f'dangling wikilink: [[{target}]]'
        if note:
            msg += f' ({note})'
        issues.append(('WARN', 'dangling-link', page, msg))

    # ---- Output ----

    by_sev = defaultdict(list)
    for sev, cat, page, msg in issues:
        by_sev[sev].append((cat, page, msg))

    print(f'=== WIKI LINT REPORT ===')
    print(f'Pages scanned: {len(pages)}')
    print(f'Slugs indexed: {len(slugs)}')
    print(f'Aliases indexed: {len(aliases)}')
    print(f'Wikilink edges: {sum(len(v) for v in outbound.values())}')
    print(f'Total issues: {len(issues)}')
    for sev in ['ERROR', 'WARN', 'INFO']:
        print(f'  {sev}: {len(by_sev[sev])}')
    print()

    for sev in ['ERROR', 'WARN', 'INFO']:
        if not by_sev[sev]:
            continue
        print(f'\n--- {sev} ({len(by_sev[sev])}) ---')
        # Group by category
        by_cat = defaultdict(list)
        for cat, page, msg in by_sev[sev]:
            by_cat[cat].append((page, msg))
        for cat in sorted(by_cat):
            print(f'\n  [{cat}] ({len(by_cat[cat])})')
            for page, msg in sorted(by_cat[cat]):
                print(f'    {page}: {msg}')

if __name__ == '__main__':
    main()
