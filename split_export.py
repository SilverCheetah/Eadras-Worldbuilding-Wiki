#!/usr/bin/env python3
"""Split a wiki concatenated export into individual files.

Usage:
  python split_export.py <export_file> <output_root> [--only-sealed] [--fix-mojibake]

Each export contains blocks of the form:

    ============================  (>=5 = signs)
    FILE: wiki/<path>
    ============================

followed by file content until the next such block (or EOF).

This script:
  - parses by that pattern (any number of '=' signs >= 5)
  - writes each page to <output_root>/<rel_path>
  - preserves UTF-8 encoding
  - optionally repairs double-encoded UTF-8 (latin-1 -> utf-8 round-trip)
  - optionally restricts to wiki/_sealed/* files
  - reports counts and any anomalies
"""
import re
import sys
from pathlib import Path


def fix_mojibake(text: str) -> str:
    """Reverse double-encoded UTF-8.

    If the original UTF-8 bytes were decoded as Latin-1 then re-encoded as
    UTF-8 (the classic mojibake pattern), this round-trip restores them.
    Returns the original text if the fix isn't applicable.
    """
    try:
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def split_export(
    export_path: Path,
    output_root: Path,
    only_sealed: bool = False,
    fix_encoding: bool = False,
    dry_run: bool = False,
) -> tuple[int, int, list[str]]:
    raw = export_path.read_bytes()
    text = raw.decode('utf-8')

    # Border line of >=5 '=' chars, then FILE: wiki/..., then another border.
    pattern = re.compile(
        r'^={5,}\r?\nFILE: (wiki/[^\r\n]+)\r?\n={5,}\r?\n',
        re.MULTILINE,
    )
    matches = list(pattern.finditer(text))
    if not matches:
        print(f'ERROR: no FILE: headers found in {export_path}', file=sys.stderr)
        return 0, 0, []

    written = 0
    skipped = 0
    anomalies: list[str] = []

    for i, m in enumerate(matches):
        rel_path = m.group(1).strip()
        if only_sealed and not rel_path.startswith('wiki/_sealed/'):
            skipped += 1
            continue

        content_start = m.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[content_start:content_end].rstrip() + '\n'

        if fix_encoding:
            content = fix_mojibake(content)

        if len(content.strip()) < 50:
            anomalies.append(f'  short page ({len(content)} chars): {rel_path}')

        out_path = output_root / rel_path
        if not dry_run:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(content.encode('utf-8'))
        written += 1

    return written, skipped, anomalies


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    export_file = Path(args[0])
    output_root = Path(args[1])
    only_sealed = '--only-sealed' in args
    fix_encoding = '--fix-mojibake' in args
    dry_run = '--dry-run' in args

    if not export_file.is_file():
        print(f'ERROR: not a file: {export_file}', file=sys.stderr)
        sys.exit(1)

    written, skipped, anomalies = split_export(
        export_file, output_root, only_sealed, fix_encoding, dry_run
    )

    mode = 'DRY RUN ' if dry_run else ''
    print(f'{mode}{export_file.name}: wrote {written}, skipped {skipped}')
    if anomalies:
        print('Anomalies:')
        for a in anomalies:
            print(a)


if __name__ == '__main__':
    main()
