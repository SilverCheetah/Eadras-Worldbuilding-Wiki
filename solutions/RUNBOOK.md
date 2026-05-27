# Eadras Wiki Cleanup Runbook — Phases 1 and 2

**Audience:** Josh, running locally against `D:\Worldbuilding\Worldbuilding LLM Wiki\`
**Created:** 2026-05-27
**Companion documents:** `Eadras_Issues_Register.md` and `Eadras_Worldbuilding_Audit.md`
**Scripts:** `scripts/01-fix-mojibake.py` through `scripts/08-small-targeted-fixes.py`

This runbook implements every Phase 1 and Phase 2 item from the Issues Register. It is designed to be followed top-to-bottom, with `git` commits after each step so that any individual change can be reverted independently. Verified end-to-end on a fresh clone of `857a096`; produces 236 modified files, net ~2,000-line reduction.

---

## Prerequisites

1. **Python 3.10+** installed.
2. **`ftfy` library** installed:
   ```
   pip install ftfy
   ```
   (Required for Step 1 only. All other scripts are stdlib-only.)
3. **Local repo at `D:\Worldbuilding\Worldbuilding LLM Wiki\`** with the baseline commit `857a096` on `main`.
4. **The two upload files** kept somewhere accessible — these are the inputs to Steps 4 and 5:
   - The cleaned `unicorns.md` (the 312-line version shared 2026-05-27).
   - The in-progress `system-governance.md` (with the stacked `## 6.` headers).

If your refresh of either file is newer than the 2026-05-27 uploads, use the newer one — the scripts re-process them internally so they don't care which version they get.

---

## Safety net (run before anything else)

```
cd "D:\Worldbuilding\Worldbuilding LLM Wiki"
git status
git pull
git log -1 --format="%H %s"
```

You should see `857a096 Initial commit: Eadras worldbuilding wiki under git` and a clean working tree. If your working tree is dirty, commit or stash first — the scripts assume a clean starting state.

For extra safety, branch first:

```
git checkout -b cleanup/phases-1-and-2
```

Each step below shows its own commit so you can also work on `main` directly and cherry-pick if preferred.

---

## Step 1 — Mojibake sweep (Phase 1)

**Fixes:** Issue Register #1. 6,556 character-level instances of UTF-8→cp1252→UTF-8 round-trip corruption across 227 files.

**Dependencies:** `ftfy`.

```
python scripts/01-fix-mojibake.py
```

This runs in **dry-run mode by default** and reports every file with the before/after mojibake count. Expected: ~227 files listed, every line ending in `→ 0`. Spot-check the output for any file that lists a non-zero "after" count (none should).

If satisfied, apply:

```
python scripts/01-fix-mojibake.py --write
git diff --stat | tail -5
```

The `--stat` output should report ~227 files with insertions and deletions of comparable magnitude (the byte-count drops because `â€"` is 5 bytes but `—` is 3).

Spot-check a representative file before committing:

```
git diff wiki/inspirations.md
```

You should see `â€" → —`, `â€™ → '`, `â†' → →` and similar. No content changes — only character repairs.

Commit:

```
git add -A
git commit -m "Sweep mojibake from 227 wiki files (ftfy)"
```

---

## Step 2 — Escape pipes in table-cell wikilinks (Phase 1)

**Fixes:** Issue Register #3 (revised). 186 wikilinks inside markdown tables where unescaped alias-pipes break the table's column structure.

**IMPORTANT correction from the 2026-05-27 audit:** the Issue Register originally said 136 backslash-pipe wikilinks were *corruption* needing removal. They are not — they are **correct Obsidian syntax** for tables. The real issue is the *opposite*: 186 wikilinks in tables that **lack** the needed `\|` escape. This script adds escapes; it never removes them.

Dry-run:

```
python scripts/02-escape-pipes-in-table-wikilinks.py
```

Expected output: 34 files listed totalling 186 fixes. `peoples-of-eadras.md` should be the worst-affected at 17. `eadras-timeline.md` at 52 is the worst.

Apply:

```
python scripts/02-escape-pipes-in-table-wikilinks.py --write
git diff wiki/peoples-of-eadras.md | head -30
```

You should see lines change from e.g. `| [[the-three|Mark] | ...` (broken) to `| [[the-three\|Mark]] | ...` (escaped).

Commit:

```
git add -A
git commit -m "Escape pipes in table-cell wikilinks (186 fixes)"
```

---

## Step 3 — Normalize line endings and clean leading frontmatter garbage (Phase 1)

**Fixes:** Issue Register #7 (`celestia.md`), #8 (line endings), #9 (`aramet.md`).

```
python scripts/03-normalize-line-endings.py
```

Expected output: two files affected.
- `wiki/aramet.md`: 1 byte of leading whitespace stripped.
- `wiki/celestia.md`: 37 CRLF, 191 lone CR, 192 bytes of leading whitespace stripped.

Apply, and optionally write `.gitattributes` to enforce LF going forward:

```
python scripts/03-normalize-line-endings.py --write --write-gitattributes
git status
```

If `.gitattributes` is created, also run:

```
git add .gitattributes
git add -A --renormalize
```

Verify celestia.md is now readable:

```
head wiki/celestia.md
```

You should see the YAML frontmatter starting at line 1.

Commit:

```
git add -A
git commit -m "Normalize line endings to LF; strip leading garbage from celestia.md and aramet.md"
```

---

## Step 4 — Commit cleaned `unicorns.md` (Phase 1)

**Fixes:** Issue Register #2 and #6. Resolves the 262× section-duplication corruption.

**Input:** The cleaned 312-line `unicorns.md` (the 2026-05-27 upload, or any newer version you have).

Dry-run, telling it where the cleaned source is:

```
python scripts/04-fix-unicorns.py --cleaned "C:\path\to\unicorns-cleaned.md"
```

Expected output:
- Original target: ~411,072 chars, 2,400 lines, 1,135 mojibake, 262× mythic-voice header.
- Cleaned source after processing: ~27,590 chars, ~313 lines, 0 mojibake, 1× mythic-voice header, 2 duplicate sources removed.

Apply:

```
python scripts/04-fix-unicorns.py --cleaned "C:\path\to\unicorns-cleaned.md" --write
```

Verify:

```
wc -l wiki/unicorns.md   # ~313 lines
grep -c "â€" wiki/unicorns.md   # 0
grep -c "## The unicorn mythic voice" wiki/unicorns.md   # 1
```

Commit:

```
git add wiki/unicorns.md
git commit -m "Replace unicorns.md with cleaned version (resolves 262x section duplication)"
```

---

## Step 5 — Finalize `system-governance.md` Section 6 (Phase 2)

**Fixes:** Issue Register #10 and #12. Removes the stacked `## 6.` header and the inconsistent `[#anchor]` lines; bumps `Last updated` date.

**Input:** The in-progress `system-governance.md` (the 2026-05-27 upload with the stacked `## 6.` headers and the new git-workflow body).

Dry-run:

```
python scripts/05-fix-governance-section-6.py --source "C:\path\to\system-governance.md"
```

Expected output: three actions taken.
- Removed stale `## 6. Backups and Exports` header.
- Removed 5 self-anchor `[#x](#x)` lines.
- Updated `Last updated` to today's date.

Apply:

```
python scripts/05-fix-governance-section-6.py --source "C:\path\to\system-governance.md" --write
```

If you want a specific date instead of today, add `--date YYYY-MM-DD`.

Spot-check:

```
git diff wiki/system-governance.md
```

Commit:

```
git add wiki/system-governance.md
git commit -m "Finalize system-governance §6 (git workflow; closes 2026-05-15 todo)"
```

---

## Step 6 — Sweep deprecated-stub references (Phase 2)

**Fixes:** Issue Register #5 (revised — fuller scope than originally reported).

**Auto-fixes** the simple cases (Related-list entries pointing at `[[dashar]]`, `[[heart-of-the-goddess]]`, `[[weavespinners]]`). **Reports** the body-text references for authorial decision; the script does NOT touch them.

Dry-run produces a complete categorized report:

```
python scripts/06-sweep-deprecated-refs.py
```

You will see four categories:
- **A. Related-list removals** — auto-fixable. Expect 4–5 items across `conduit-cities.md`, `voroik.md`, `lirra.md`.
- **B. Meta-page references** — intentionally preserved (open-questions, worldbuilding-needs, index, inspirations, log).
- **C. Place-name body-text references** — Heart of the Goddess as a metaphysical place. Authorial decision needed.
- **D. Mechanism / table body-text references** — Da'shar relationship rows etc. Authorial decision needed.

Read categories C and D carefully — these are the items the audit flagged as needing your decision.

Apply category A only:

```
python scripts/06-sweep-deprecated-refs.py --write
```

Commit:

```
git add -A
git commit -m "Sweep deprecated-stub references from Related lists"
```

Then **manually edit** the category C and D files according to your decision:

- `wiki/voroik.md:44` — Heart of the Goddess as the place where Lirra appears as two eyes.
- `wiki/lirra.md:89, :102, :116, :161` — Multiple references to Heart of the Goddess as a place plus a Da'shar table row.
- `wiki/eras.md:45` — Reference to walking into the Heart of the Goddess as a place of high-magic-era play.
- `wiki/rpg/closed-time-bubble.md:30` — Heart of the Goddess as a metaphysical setting.

Once edited, commit:

```
git add -A
git commit -m "Resolve Heart of the Goddess / Da'shar body-text references (authorial decisions)"
```

---

## Step 7 — Rebuild `peoples-of-eadras.md` race table (Phase 2)

**Fixes:** Issue Register #4. The "Original Races" table is structurally malformed (6-column header, variable-cell rows, wikilinks split across columns). Rebuilds as a clean 3-column table.

Dry-run with verbose to see the rebuilt rows:

```
python scripts/07-rebuild-peoples-of-eadras-table.py --verbose
```

Expected output: 1 table located, 37 rows rebuilt. The verbose flag shows the first 5 rebuilt rows so you can eyeball-check the format.

Apply:

```
python scripts/07-rebuild-peoples-of-eadras-table.py --write
```

Open `wiki/peoples-of-eadras.md` in Obsidian and verify the table renders as 3 columns (Race / Creator / Notes) with all the race-info correctly aligned.

Commit:

```
git add wiki/peoples-of-eadras.md
git commit -m "Rebuild peoples-of-eadras.md race table (3 columns; escape pipes in wikilinks)"
```

---

## Step 8 — Small targeted fixes (Phase 2)

**Fixes:** Issue Register #11 Group A (typos), #15 (`dwarves.md`), the `order-sworn-sorcerers` → `order-sworn-netharim` rename in active pages.

```
python scripts/08-small-targeted-fixes.py
```

Expected fixes:
- `[[velrathi-tea-tradition]]` → `[[velrathi-tea-culture]]` (1 in `velveth.md`)
- `[[ascended-mortal-deities-mechanism]]` → `[[apotheosis]]` (1 in `imma.md`)
- `[[order-sworn-sorcerers]]` → `[[order-sworn-netharim]]` (1 in `inspirations.md`)
- `## Naming` (race etymology section) → `## Etymology` in `dwarves.md`

Apply:

```
python scripts/08-small-targeted-fixes.py --write
```

Commit:

```
git add -A
git commit -m "Sweep typo wikilinks; rename order-sworn-sorcerers→netharim outside log; clean dwarves Naming dup"
```

---

## Step 9 — Push

```
git log --oneline -10
git push
```

If you branched, merge first:

```
git checkout main
git merge cleanup/phases-1-and-2
git push
```

---

## Post-cleanup verification

Run a quick sanity-check:

```
# Mojibake should be zero
grep -c "â€" wiki/*.md wiki/rpg/*.md wiki/protocols/*.md | grep -v ":0$"

# unicorns.md should be ~17KB, not 411KB
ls -lh wiki/unicorns.md

# system-governance.md should have only one ## 6.
grep "^## 6" wiki/system-governance.md

# peoples-of-eadras.md should have a clean 3-column table
head -55 wiki/peoples-of-eadras.md
```

---

## What's NOT in Phases 1–2

The following items from the Issues Register remain open as authorial decisions and are NOT addressed by these scripts:

- **Phase 3** — missing-concept page decisions: `demonfall-gate` (8 broken references), `bold-republic`, `shadowdark-gaia`, `veil-gaia`. Should these pages exist?
- **Phase 3** — image-asset convention: `[[Eadras Golden Age Map.png]]`, `[[Spear of Crystallized Entropy.png]]`, `[[Arathi crystalmancer.jpg]]`, `[[Eadras Nmya post-Cataclysm.jpg]]`. Are these in a separate `attachments/` folder, or should they be committed to the repo?
- **Phase 4** — the 87 development items from the 2026-05-24 issues register (continuity items, magic-system gaps, modern map geometry, etc.). These are content development, not hygiene.

---

## Summary of expected impact

Starting state (`857a096`):
- 284 markdown files, 274 audited.
- 6,556 mojibake instances across 227 files.
- 186 unescaped pipes in table-cell wikilinks across 34 files.
- 5 Related-list references to deprecated pages.
- `unicorns.md`: 411 KB / 2,400 lines (real content ~17 KB).
- `peoples-of-eadras.md`: structurally broken race table.
- `system-governance.md`: stale Section 6 (governance-incorrect "not under git").
- `celestia.md`: 193 bytes of leading garbage, only CRLF file in repo.
- `aramet.md`: 1 byte of leading whitespace before frontmatter.
- Multiple typo wikilinks, one redundant heading.

After Phases 1 + 2:
- All 6,556 mojibake instances repaired.
- All 186 table-cell wikilink pipes correctly escaped.
- 4 of 5 Related-list references swept (1 remaining is in `inspirations.md` and intentionally preserved).
- `unicorns.md`: 27 KB / 313 lines.
- `peoples-of-eadras.md`: clean 3-column table.
- `system-governance.md`: Section 6 finalized, date bumped.
- `celestia.md`: clean LF file with normal frontmatter.
- `aramet.md`: leading whitespace stripped.
- `dwarves.md`, `inspirations.md`, `velveth.md`, `imma.md`: small surgical fixes.
- ~236 files modified, ~6,800 lines deleted, ~4,750 inserted (net ~2,000-line reduction).
- 8 atomic commits, each independently revertable.

What you'll be left with for Phase 3 is **content-development work** — the noise floor of mechanical issues drops to ~0, which lets the actual worldbuilding work resume without distraction.
