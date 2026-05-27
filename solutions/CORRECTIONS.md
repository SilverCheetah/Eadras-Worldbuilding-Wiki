# Audit Corrections — 2026-05-27 Implementation Notes

While implementing the Phase 1 / Phase 2 solution scripts, three findings from the original 2026-05-27 audit (`Eadras_Issues_Register.md`, `Eadras_Worldbuilding_Audit.md`) were revised after closer inspection of the actual repo. This document records the corrections so the audit reasoning stays trustworthy going forward.

---

## Correction 1 — Issue Register #3 was inverted

**Original audit text (incorrect):**
> "Across 24 files, wikilinks inside markdown tables have been written as `[[slug\|Display]]` with a literal backslash before the pipe. The backslash was presumably inserted to escape the pipe character that markdown uses as table-column delimiter, but it was placed *inside* the wikilink target — making the wikilink target itself end in `\` and breaking the link in Obsidian."

**Correction:**
The 136 backslash-pipe wikilinks (`[[slug\|Display]]`) are **NOT corruption**. They are **correct Obsidian syntax** for wikilinks placed inside markdown tables. Per Obsidian's documentation, `\|` inside a table-cell wikilink is necessary to prevent the table parser from treating the alias-pipe as a column separator.

**What was actually broken:**
The opposite. There were **186 wikilinks in table cells with UNESCAPED pipes** across 34 files — including `peoples-of-eadras.md` (the worst-affected table). These are the wikilinks that break Obsidian rendering, because the table parser splits them across cells.

**Solution script:** `02-escape-pipes-in-table-wikilinks.py` ADDS the escape; it never removes it. The 136 already-escaped wikilinks are left alone.

**How the error happened:** The initial audit scan flagged `\|` as suspicious without checking whether it's inside a table row. Once classified by context (135 of 136 inside table rows, the 1 remaining in `log.md` as descriptive prose), the pattern was clearly correct syntax rather than corruption.

---

## Correction 2 — Issue Register #13 false-positive on `inspirations.md`

**Original audit text (partially incorrect):**
> "`inspirations.md` contains the wikilinks `[[wiki-page-1]]` and `[[wiki-page-2]]` — clearly placeholder text that escaped a template."

**Correction:**
The `[[wiki-page-1]]` and `[[wiki-page-2]]` references in `inspirations.md` are **inside an HTML comment block** (lines 138–146) — they are intentional template placeholders showing the format for future entries. Not residue from a broken edit.

**Implication for the broader audit:** the original wikilink scan did not skip HTML comments. The "44 broken wikilinks" count in Issue Register #11 may include similar false-positives elsewhere. After comment-stripping, the count drops to ~42 — but the impact is small because most of the broken links are in `log.md` (also intentionally preserved) or are real broken concept-references.

**Solution script:** `08-small-targeted-fixes.py` strips HTML comments before reporting placeholder leaks. The script correctly reports "no action required" for `inspirations.md`.

---

## Correction 3 — Issue Register #5 understated the scope

**Original audit text (incomplete):**
> "Three deprecated stub pages... still referenced from 5 active pages."

**Correction:**
The "5 active pages" referred only to pages with deprecated-stub references in their **Related lists**. The actual scope is larger:

| Category | Count | Treatment |
|---|---:|---|
| Related-list items (auto-fixable) | 4 | Sweep |
| Meta/audit pages (intentional preservation) | 5+ | Skip (open-questions, worldbuilding-needs, index, inspirations, log) |
| Place-name body-text references | 5 | Authorial decision |
| Mechanism / table body-text references | 1 | Authorial decision |

The **place-name body-text references** are the most significant addition. `lirra.md` has 4 separate references to "Heart of the Goddess" as a metaphysical place where stars shine, where Lirra communes, where she sees Loom-Marks. `voroik.md`, `eras.md`, and `rpg/closed-time-bubble.md` each have one. The 2026-05-14 deprecation retired the *mechanism* of sorcerer-transmutation in the Heart, but the *place* itself was not declared retired. This needs an authorial decision before the deprecation can be considered fully propagated.

**Solution script:** `06-sweep-deprecated-refs.py` auto-fixes only the clean Related-list cases. Categories B, C, and D are reported as informational output, classified, and listed by file + line number for manual review.

---

## What didn't change

The following audit findings held up exactly as documented:

- Mojibake scope: 227 files, ~6,556 instances. (After dependency installation: 6,951 instances counted by `ftfy`'s broader pattern set — same files, slightly more thorough fix.)
- `unicorns.md` 262× section duplication.
- `system-governance.md` Section 6 stacked-header state.
- `peoples-of-eadras.md` table structure broken.
- `celestia.md` 193-byte leading garbage + CRLF line endings.
- `aramet.md` leading-blank-line frontmatter.
- `dwarves.md` duplicate `## Naming`.
- The typo wikilinks for `velrathi-tea-tradition`, `flesh-crafters`, `mythic-retellings-of-the-cataclysm-and-demon-war`, `ascended-mortal-deities-mechanism`.
- The `order-sworn-sorcerers` → `order-sworn-netharim` rename (correctly classified as rename, not retirement).
- `druids.md` correctly preserved as a sub-priesthood (not a deprecated mechanism — the rework redefined the order, not retired it).

---

## Updated counts after Phase 1 + Phase 2 application

End-to-end test on a fresh clone of `857a096` produced:

| Metric | Before | After |
|---|---:|---:|
| Mojibake characters | 6,556 | 0 |
| Broken table wikilinks (unescaped pipes) | 186 | 0 |
| `unicorns.md` size | 411 KB | 27 KB |
| `unicorns.md` mythic-voice section duplications | 262 | 1 |
| `system-governance.md` `## 6.` headers | 2 stacked | 1 clean |
| Related-list deprecated refs | 5 | 0 |
| `celestia.md` CRLF / leading-garbage bytes | 37 / 193 | 0 / 0 |
| Files modified | — | 236 |
| Atomic commits | — | 8 |
