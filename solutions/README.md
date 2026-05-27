# Eadras Wiki Cleanup — Phase 1 & 2 Solutions

Solutions to Phase 1 and Phase 2 of the 2026-05-27 Eadras Worldbuilding Wiki audit.

## What's in here

- **`RUNBOOK.md`** — Step-by-step instructions for running all 8 scripts in order against your local repo. Start here.
- **`scripts/`** — 8 Python scripts implementing every fix. All scripts:
  - Default to **dry-run mode** — no files written unless `--write` is passed.
  - Auto-detect the repo root by looking for `wiki/system-governance.md`.
  - Print a summary of changes and a suggested commit message.
  - Are idempotent — safe to re-run.

## Quick start

```
cd "D:\Worldbuilding\Worldbuilding LLM Wiki"
pip install ftfy
git checkout -b cleanup/phases-1-and-2
```

Then follow `RUNBOOK.md` step-by-step. Each script has its own `--help` for reference.

## Script inventory

| # | Script | Phase | Fixes | Expected impact |
|---|---|---|---|---|
| 01 | `01-fix-mojibake.py` | 1 | UTF-8→cp1252→UTF-8 corruption | 227 files, ~6,556 chars |
| 02 | `02-escape-pipes-in-table-wikilinks.py` | 1 | Wikilink pipes in table cells | 34 files, 186 fixes |
| 03 | `03-normalize-line-endings.py` | 1 | CRLF/CR + leading frontmatter garbage | `celestia.md`, `aramet.md` |
| 04 | `04-fix-unicorns.py` | 1 | 262× section duplication | `unicorns.md` 411KB→27KB |
| 05 | `05-fix-governance-section-6.py` | 2 | Stacked `## 6.` headers, stale date | `system-governance.md` |
| 06 | `06-sweep-deprecated-refs.py` | 2 | Deprecated stub references (auto + flag) | 4 auto-fixes + report |
| 07 | `07-rebuild-peoples-of-eadras-table.py` | 2 | Broken markdown race table | `peoples-of-eadras.md` |
| 08 | `08-small-targeted-fixes.py` | 2 | Typo wikilinks, dwarves dup, rename | 4 small surgical fixes |

## What this does NOT do

These scripts handle every Phase 1 and Phase 2 item that is *mechanically determinable*. They do not address:

- **Content development** (Phase 4) — the 87 development items in the 2026-05-24 Issues Register.
- **Authorial decisions** (Phase 3) — should `demonfall-gate` be a page? How should Heart of the Goddess as a place be handled now that the mechanism is deprecated? Where should image assets live?

Script 06 explicitly *reports* the authorial-decision items without trying to auto-resolve them.

## Verification

After running all 8 scripts and committing, you can verify the cleanup with:

```
grep -c "â€" wiki/*.md wiki/rpg/*.md wiki/protocols/*.md | grep -v ":0$"
ls -lh wiki/unicorns.md
grep "^## 6" wiki/system-governance.md
git log --oneline cleanup/phases-1-and-2
```

The grep should return nothing, `unicorns.md` should be ~17 KB, `system-governance.md` should have exactly one `## 6.` header, and the log should show 8–9 cleanup commits.

## Safety notes

- **Dry-run first, always.** Every script defaults to dry-run; you must pass `--write` explicitly.
- **Commit between scripts.** Each step's commit can be independently reverted if a problem emerges.
- **The `--write` flag is required for changes.** Without it, scripts only report what they *would* do.
- **Run on a branch.** The runbook recommends `cleanup/phases-1-and-2` so you can review the full set of changes before merging to main.
- **Per `system-governance.md` §6**, git provides the safety net. If a script's effect is wrong, `git checkout HEAD -- <file>` reverts that file; `git reset --hard HEAD~1` reverts the last commit if not pushed.
- **`sed -i` and `awk -i` are not used anywhere in these scripts** — per governance §6 and the load-bearing 2026-05-10 lesson. All edits are Python sweeps with explicit write steps.

## Files generated

After running everything, you should have:

- ~236 modified `wiki/**.md` files.
- Optional new `.gitattributes` if `--write-gitattributes` was passed in Step 3.
- 8–9 commits on the cleanup branch.

## If something goes wrong

For any single script:

```
# Revert just that file from the last commit
git checkout HEAD -- wiki/<file>.md

# Revert the most recent commit entirely (before pushing)
git reset --hard HEAD~1

# Compare current state to baseline
git diff 857a096 -- wiki/<file>.md
```

If you discover a bug mid-stream:

1. Stop running scripts.
2. Either commit what's good or `git reset` to the last good state.
3. The 8 scripts are independent — completing 6 of 8 is fine; the remaining 2 can run later.
