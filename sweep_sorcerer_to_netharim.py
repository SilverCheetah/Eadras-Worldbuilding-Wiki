"""Sweep deprecated sorcerer/Weavespinner terminology to the new Netharim/Windspeaker canon.

Replacements:
  Sorcerer Crusade   → Anti-Magic Crusade
  sorcerer-crusade   → anti-magic-crusade   (wikilink slug)
  Weavespinners      → Windspeakers
  Weavespinner       → Windspeaker
  weavespinners      → windspeakers
  weavespinner       → windspeaker
  Sorcerers          → Netharim
  Sorcerer           → Netharim
  sorcerers          → Netharim
  sorcerer           → Netharim
  Sorcery            → Netharim practice
  sorcery            → Netharim practice
  Sorcerous          → Netharim
  sorcerous          → Netharim

EXCLUSIONS:
  - log.md (append-only history, preserves the change record)
  - inspirations.md (catalogs Galloway's "Sorcerer apparatus" as historical influence)
  - tags.md (canonical tag taxonomy; check separately)
  - The stub pages (dashar.md, order-sworn-sorcerers.md, weavespinners.md,
    heart-of-the-goddess.md) explain what they WERE; leave their terminology
    in place where it describes the deprecated concept

ORDER MATTERS: do the multi-word phrases first ("Sorcerer Crusade" before "Sorcerer"),
and do the wikilink form before the prose form so we don't corrupt slugs.

Read-only by default; pass --apply to actually write.
"""
import sys
from pathlib import Path

WIKI = Path('wiki')

EXCLUDED_FILES = {
    'log.md',
    'inspirations.md',
    'tags.md',
    'dashar.md',
    'order-sworn-sorcerers.md',
    'weavespinners.md',
    'heart-of-the-goddess.md',
    # The two newly-rewritten pages already use the new canon and reference
    # the old terms only in their sources-line metadata; skip to preserve those:
    'anti-magic-crusade.md',
    'order-sharanel.md',
    'magic-in-eadras.md',
    'windspeakers.md',
    # Stubs that document the deprecation:
}

# Order matters — phrases first, then individual words
REPLACEMENTS = [
    # Wikilink slugs first (longest first to avoid corruption)
    ('[[sorcerer-crusade|', '[[anti-magic-crusade|'),
    ('[[sorcerer-crusade]]', '[[anti-magic-crusade]]'),
    ('[[sorcerer-crusade#', '[[anti-magic-crusade#'),
    ('[[weavespinners|', '[[windspeakers|'),
    ('[[weavespinners]]', '[[windspeakers]]'),
    ('[[weavespinners#', '[[windspeakers#'),
    # Multi-word phrases
    ('Sorcerer Crusade', 'Anti-Magic Crusade'),
    ('sorcerer crusade', 'anti-magic crusade'),
    ('Sorcerer-Crusade', 'Anti-Magic-Crusade'),
    # Weavespinner → Windspeaker (plural and singular)
    ('Weavespinners', 'Windspeakers'),
    ('Weavespinner', 'Windspeaker'),
    ('weavespinners', 'windspeakers'),
    ('weavespinner', 'windspeaker'),
    # sorcery/sorcerous → Netharim practice / Netharim
    ('Sorcery', 'Netharim practice'),
    ('sorcery', 'Netharim practice'),
    ('Sorcerous', 'Netharim'),
    ('sorcerous', 'Netharim'),
    # Plain noun (capitalized variants and plural before singular)
    ('Sorcerers', 'Netharim'),
    ('sorcerers', 'Netharim'),
    ('Sorcerer', 'Netharim'),
    ('sorcerer', 'Netharim'),
]

def sweep(apply_changes=False):
    pages = sorted(WIKI.rglob('*.md'))
    total_subs = 0
    files_touched = 0

    for p in pages:
        rel = p.relative_to(WIKI).as_posix()
        if p.name in EXCLUDED_FILES:
            continue
        # Don't touch _sealed/README.md or other meta
        if rel.startswith('_sealed/'):
            # Allow sweeps inside _sealed/ EXCEPT the README (which has special structure)
            if p.name == 'README.md':
                continue
        try:
            text = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            print(f'SKIP (encoding): {rel}')
            continue
        original = text
        per_file_subs = 0
        for old, new in REPLACEMENTS:
            count = text.count(old)
            if count > 0:
                text = text.replace(old, new)
                per_file_subs += count
        if per_file_subs > 0:
            files_touched += 1
            total_subs += per_file_subs
            print(f'  {rel}: {per_file_subs} replacement(s)')
            if apply_changes:
                p.write_text(text, encoding='utf-8')

    print()
    print(f'=== Summary ===')
    print(f'Files touched: {files_touched}')
    print(f'Total substitutions: {total_subs}')
    if not apply_changes:
        print(f'(dry-run; pass --apply to write changes)')


if __name__ == '__main__':
    apply = '--apply' in sys.argv
    sweep(apply_changes=apply)
