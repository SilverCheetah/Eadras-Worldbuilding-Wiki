# Eadras Worldbuilding Issues Register

**Prepared for:** Eadras Worldbuilding Wiki (`https://github.com/SilverCheetah/Eadras-Worldbuilding-Wiki`)
**Audit date:** 2026-05-27
**Repository state:** baseline commit `857a096` (single commit on `main`); 284 markdown files under `wiki/`; 274 audited (excluding 4 sealed files and 6 templates per governance §4 and §1).
**Method:** Programmatic sweep of the live repo for mojibake, broken wikilinks, structural corruption, frontmatter compliance, deprecated-reference propagation, and duplicate sections — combined with refresh of the issues raised in the 2026-05-24 register and audit.
**Supersedes:** 2026-05-24 issues register. Issues from that document are carried forward with current status; new issues are appended.

---

## Priority Key

- **Critical** — Blocks load-bearing canon, file integrity, or downstream work; fix in the next session.
- **High** — Distorts reader understanding, breaks navigation, or is actively misleading; fix before further major drafting.
- **Medium** — Real but bounded; queue for a targeted pass.
- **Low** — Polish, optional expansion.
- **Maintenance** — Encoding, formatting, schema, automation hygiene.

---

# I. Acute Wiki Hygiene (machine-detectable, fixable in a single sweep)

These issues were found by direct scan of the live repo (`857a096`) on 2026-05-27 and are the highest-leverage fixes available: they are mechanical, locatable, and unblock everything else.

## 1. Mojibake (UTF-8 → cp1252 → UTF-8 corruption) across the wiki

**Priority:** Critical
**Type:** Encoding / file integrity
**Scope:** **227 of 274 audited files; 6,556 instances total**

**Issue:**
A UTF-8-to-cp1252-to-UTF-8 round-trip has left the signature `â€` byte sequence throughout the wiki, principally on em dashes (`—` → `â€"`), en dashes (`–` → `â€"`), smart quotes (`"` → `â€œ`, `"` → `â€\x9d`, `'` → `â€™`, `'` → `â€˜`), and ellipses (`…` → `â€¦`). Every file containing the prior register's commentary about mojibake is itself still mojibaked — the issue has been *documented* but not *swept*.

**Top 15 worst-affected files:**

| Instances | File |
|---:|---|
| 1135 | `wiki/unicorns.md` |
| 134 | `wiki/open-questions.md` |
| 96 | `wiki/amunorians.md` |
| 93 | `wiki/worldbuilding-needs.md` |
| 92 | `wiki/mythic-recitations.md` |
| 91 | `wiki/gods-of-eadras.md` |
| 78 | `wiki/spirits.md` |
| 72 | `wiki/arathi.md` |
| 68 | `wiki/back-rooms.md` |
| 68 | `wiki/dragon-empire.md` |
| 66 | `wiki/black-hand.md` |
| 66 | `wiki/inspirations.md` |
| 65 | `wiki/draconic-language.md` |
| 65 | `wiki/arathi-cataclysm.md` |
| 61 | `wiki/flesh-eaters.md` |

(Note: `wiki/unicorns.md` had 1,135 instances in the live repo's committed version; the in-progress refresh shared 2026-05-27 reduced this to 76, but the page is also the only file in the repo with CRLF line endings — see issue 7.)

**Recommended fix:**
Single Python sweep script. The transformation is deterministic — encode the file's UTF-8 as latin-1, then decode as UTF-8 — and reverses cleanly:

```python
def fix_mojibake(text: str) -> str:
    try:
        return text.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text  # already clean or differently corrupted; leave alone
```

Run with `--dry-run` first per the no-`sed` rule in `system-governance.md` §6. The `split_export.py` script in the repo root already advertises a `--fix-mojibake` flag — verify whether that flag works as documented and, if so, use it; otherwise the four-line function above is sufficient.

Commit as a single atomic sweep titled e.g. *"Fix mojibake across 227 wiki files (latin-1 → utf-8 round-trip)"*.

**Validation:** after sweep, `grep -rc 'â€' wiki/` should return zero for every file.

---

## 2. `wiki/unicorns.md` duplication corruption

**Priority:** Critical
**Type:** File corruption
**Scope:** `wiki/unicorns.md` only

**Issue:**
The live repo's committed `wiki/unicorns.md` contains the section header `## The unicorn mythic voice — sorrowful, watchful, alarmed` **repeated 262 times**, with its six-line body block duplicated alongside it. File is 2,400 lines / 411KB when the real content is ~280 lines. This is the prior register's issue #14 and was first flagged on 2026-05-24; it remains uncommitted in the live repo.

The version of `unicorns.md` uploaded for review on 2026-05-27 (312 lines) is a successful cleanup of this issue and should be the basis for the commit, but **(a) it has not been committed**, **(b) it still contains 76 mojibake instances** (see issue 1), and **(c) it uses CRLF line endings** while every other file in the repo is LF (see issue 7).

**Recommended fix:**
Commit the cleaned 312-line version of `unicorns.md`, but first:
1. Normalize line endings to LF (`dos2unix wiki/unicorns.md` or equivalent str-replace of `\r\n` → `\n`).
2. Run the mojibake fix from issue 1 on this file before or as part of the same commit.
3. Verify the Sources field is also cleaned (see issue 6 — the Sources line still contains its own internal duplications).

---

## 3. Backslash-pipe wikilink corruption (`[[slug\|Display]]`)

**Priority:** High
**Type:** Wikilink syntax / link integrity
**Scope:** **24 files; 136 instances**

**Issue:**
Across 24 files, wikilinks inside markdown tables have been written as `[[slug\|Display]]` with a literal backslash before the pipe. The backslash was presumably inserted to escape the pipe character that markdown uses as table-column delimiter, but it was placed *inside* the wikilink target — making the wikilink target itself end in `\` and breaking the link in Obsidian. The correct fix in markdown tables is to either (a) not escape the pipe (Obsidian's wikilink parser handles the alias-pipe before the table-cell pipe), (b) escape the table-cell pipes differently, or (c) replace the table with a non-table layout.

**Top 10 worst-affected files:**

| Instances | File |
|---:|---|
| 27 | `wiki/peoples-of-eadras.md` |
| 14 | `wiki/gods-of-eadras.md` |
| 11 | `wiki/elfen.md` |
| 9 | `wiki/velrathi.md` |
| 8 | `wiki/worldender-crystal.md` |
| 7 | `wiki/gaia.md` |
| 7 | `wiki/great-banishment.md` |
| 7 | `wiki/eadras-timeline.md` |
| 6 | `wiki/magic-in-eadras.md` |
| 6 | `wiki/three-who-stood.md` |

Examples in source:
- `[[ratharil\|Ratharil]]` should be `[[ratharil|Ratharil]]`
- `[[the-three\|Mark]]` should be `[[the-three|Mark]]`
- `[[battle-of-the-broken-conclaves\|Final Wall]]` should be `[[battle-of-the-broken-conclaves|Final Wall]]`

**Recommended fix:**
Single Python sweep with the regex `\[\[([^\[\]]+?)\\\|([^\[\]]+?)\]\]` → `[[\1|\2]]`. Run dry-first per governance §6. Commit as *"Strip backslash-escaped pipes from in-table wikilinks (136 fixes)"*.

**Test before sweeping:** confirm in Obsidian that the unescaped form renders correctly inside the affected tables. If table rendering is the issue, the proper fix may be different (e.g. converting offending rows to lists, or using `&#124;` for the table-cell pipe rather than escaping the wikilink-internal pipe).

---

## 4. `wiki/peoples-of-eadras.md` table structurally broken

**Priority:** High
**Type:** Table syntax / rendering
**Scope:** `wiki/peoples-of-eadras.md`

**Issue:**
This is a layered failure — the prior register's issue #13, still unresolved. The main races table has rows whose first column contains a wikilink (`**[[elfen|Elfen]]**`), but the alias-pipe inside the wikilink has been escaped to `\|` (issue 3), *and* the row has been padded with extra trailing pipes such that columns 4 and 5 appear as empty cells. The result is that:

- Some rows render with five columns when the header has three.
- Some wikilinks split visually across columns (`**[[arathi` in column 1, `Arathi]]**` in column 2).
- The table fails to render meaningfully in Obsidian preview.

**Recommended fix:**
This file requires manual rebuilding rather than sweeping. Recommended approach:
1. Inventory current row content (race name / creator / notes).
2. Rebuild the table as a three-column structure: `| Race | Creator | Notes |`.
3. Use unescaped pipes inside wikilinks (the issue 3 sweep will handle that if done first).
4. Use `&#124;` only if a literal pipe is required inside a cell *outside* a wikilink (none expected here).

Time estimate: 30–45 minutes manual edit.

---

## 5. Three deprecated stub pages still referenced from active canon

**Priority:** Medium
**Type:** Deprecated lore propagation (per Josh's flag)
**Scope:** 3 deprecated pages + 5 active pages with stale references + the log

**Issue:**
The 2026-05-14 magic-system rework set three pages to `canon_status: [deprecated]`:

- `wiki/dashar.md` (Da'shar — superseded by `lexanari` + `netharim`)
- `wiki/heart-of-the-goddess.md` (Heart of the Goddess — Weave-internal communion space, no longer canonical)
- `wiki/weavespinners.md` (Weavespinners — superseded by `windspeakers`)

Per system-governance §4 *Deprecated content*, these stubs are correctly retained for traceability. But governance §4 also says: *"Redirect wikilinks from other pages to the new canonical target."* That redirection has not happened on the following **active pages**:

| Reference | In active page | Suggested target |
|---|---|---|
| `[[dashar]]` | `wiki/conduit-cities.md:193` (Related pages section) | Remove from Related pages, or replace with `[[netharim]]` |
| `[[dashar]]` | `wiki/voroik.md:71` (Related pages) | Remove or redirect |
| `[[dashar]]` | `wiki/lirra.md:205` (Related pages) | Remove or redirect |
| `[[dashar]]` and `[[heart-of-the-goddess]]` | `wiki/inspirations.md:56` | Update inspirations reference to the new canon |
| `[[heart-of-the-goddess]]` | `wiki/voroik.md:44, :70` | Remove or redirect |
| `[[heart-of-the-goddess]]` | `wiki/eras.md:45` | Body text mention; revise sentence |
| `[[weavespinners]]` (4x) | `wiki/log.md` (changelog entries) | **Leave alone** — historical record |

(Footer Related-pages references to deprecated stubs are the most common case; these mostly need outright removal from the lists.)

**Recommended fix:**
1. Audit each non-log occurrence above.
2. Decide for each whether to redirect (replace with new canonical link), remove (Related-pages list-item), or restate (body prose).
3. Sweep in one commit per affected page or one combined commit with a clear message.

**Note:** The deprecation announcements in `wiki/open-questions.md` (lines 51–52) are correctly using strike-through with the deprecated wikilink — those are intentionally referencing the old name and should not be changed.

---

## 6. Repeated text in Sources / Last-updated fields (corruption residue)

**Priority:** Medium
**Type:** Frontmatter / metadata hygiene (corruption residue from the 2026-05-10 incident)
**Scope:** Spot-found in `wiki/unicorns.md`; sweep-needed elsewhere

**Issue:**
The 2026-05-27 refreshed `unicorns.md` Sources field reads:

> `... unicorns-01/02/03 (2026-05-15 ingest ...); DragonsAndUnicorns_01_InWorld_Facts.txt; user direction 2026-05-13 (unicorn-memory seals are Ixthal's own work); DragonsAndUnicorns_01_InWorld_Facts.txt; user direction 2026-05-13 (unicorn-memory seals are Ixthal's own work); DragonsAndUnicorns_01_InWorld_Facts.txt; user direction 2026-05-13`

The same source string is repeated three times. This matches the prior register's issue #12 (Sources duplication from the 2026-05-10 `sed -i` incident). It is not solved by the duplicate-section cleanup of issue 2 — the Sources line itself carries the residue.

**Recommended fix:**
Manual edit on `unicorns.md` Sources line: trim to a single occurrence of each source.

**Recommended sweep:**
Across the wiki, search for sources-line patterns where the same `.txt` filename appears more than once on the same line, and review each. A regex-based detector (not autofixer) is appropriate:

```python
import re
def find_dup_sources_lines(text: str) -> list[str]:
    pat = re.compile(r'^\*\*Sources\*\*: (.+)$', re.MULTILINE)
    out = []
    for m in pat.finditer(text):
        sources = [s.strip() for s in re.split(r'[;,]', m.group(1))]
        seen = {}
        for s in sources:
            seen[s] = seen.get(s, 0) + 1
        dups = {k: v for k, v in seen.items() if v > 1}
        if dups:
            out.append((m.group(1), dups))
    return out
```

Each hit needs manual review (some short tokens like "Sourceflare" may legitimately appear more than once); the autofix is risky.

---

## 7. `wiki/celestia.md` is functionally empty and has corrupted file structure

**Priority:** High
**Type:** File corruption + content stub
**Scope:** `wiki/celestia.md`

**Issue:**
Two problems compounded:

1. The file has **193 bytes (~96 carriage-return characters) of leading whitespace** before its frontmatter begins on visible line 2. This is the only file in the entire repo with this kind of leading garbage.
2. It is the **only file in the entire repo with CRLF (`\r\n`) line endings** — every other file is LF. (See issue 8 for the line-ending policy implication.)
3. The actual content is a 2-paragraph stub (per the prior audit's "Underdeveloped" classification, but this stub-status is partly an artifact of the file corruption — Obsidian and other markdown processors may be silently mishandling the leading-CR garbage and rendering it wrong).

**Recommended fix:**
1. Strip the leading whitespace block.
2. Convert CRLF to LF.
3. Verify the page renders in Obsidian.
4. The actual content-development of Celestia (which is genuinely thin) becomes a separate work item under the §IV "Cosmology and Divine-System Refinements" group of the prior register (issue #19 family).

---

## 8. Line-ending inconsistency between files

**Priority:** Low (Maintenance)
**Type:** File hygiene / cross-platform consistency
**Scope:** 1 confirmed file (celestia.md, see issue 7); refresh `unicorns.md` from upload also CRLF; sweep needed to confirm scope

**Issue:**
At the time of audit, the live committed repo had 273 LF-only files and 1 CRLF-only file (`wiki/celestia.md`). The 2026-05-27 refreshed `unicorns.md` shared in this conversation also uses CRLF.

If Josh's working environment is Windows and Obsidian re-saves files with CRLF on edit, this drift will recur. The wiki should pick one convention and enforce it.

**Recommended fix:**
1. Decide on a canonical line ending (LF is conventional for git-tracked projects; CRLF is Obsidian's default-on-Windows behaviour).
2. Add a `.gitattributes` file at repo root specifying `*.md text eol=lf` (or `eol=crlf` if chosen).
3. Run `git add --renormalize .` after committing the file.
4. Codify in `system-governance.md` §6 (or a new sub-section under §1).

---

## 9. `wiki/aramet.md` has a blank line before frontmatter

**Priority:** Low (Maintenance)
**Type:** Schema compliance
**Scope:** `wiki/aramet.md`

**Issue:**
Per governance §1 *Body structure*: *"Every wiki page MUST have YAML frontmatter at the top of the file."* The file `wiki/aramet.md` has a leading `\n` before its opening `---`. Obsidian handles this leniently; some markdown processors do not. The other 273 files in the audited set start with `---` on line 1.

**Recommended fix:**
Trim the leading newline. One-line manual fix.

---

## 10. `system-governance.md` Section 6 is in a half-merged state

**Priority:** High
**Type:** Governance drift (per Josh's memory: "updating system-governance.md Section 6")
**Scope:** `wiki/system-governance.md` only

**Issue:**
The file as shared 2026-05-27 has **two `## 6.` headers stacked back-to-back**:

```
## 6. Backups and Exports

## 6. Backups and Recovery
```

The stale "Backups and Exports" text was deleted, but its **header was not**, and the **`Last updated: 2026-05-16` date was not bumped** even though the body of Section 6 has changed substantially (the new git-based workflow). The new Section 6 content also includes `[#anchor](#anchor)` self-anchor lines under each subheading that don't appear elsewhere in the file — this stylistic addition needs a decision: keep them or remove them.

**Recommended fix:**
1. Delete the stale `## 6. Backups and Exports` header line (line 504 of the uploaded version).
2. Decide on the `[#anchor]` convention. If kept, add them to other section headings consistently; if not, strip from §6.
3. Bump `Last updated:` to the actual edit date.
4. Commit as a single change titled *"Finalize system-governance §6 git workflow (closes 2026-05-15 todo)"*.

---

## 11. Broken wikilinks pointing to nonexistent pages

**Priority:** Medium
**Type:** Link integrity
**Scope:** **44 instances across ~15 source files; 27 unique missing targets**

**Issue:**
After excluding the backslash-pipe corruption of issue 3 (which is its own pattern) and the deprecated-page references of issue 5 (where the page exists but should redirect), the remaining broken wikilinks fall into three groups:

**Group A — Pages that should probably exist but don't (concept gaps):**

| Refs | Missing target | Referenced in |
|---:|---|---|
| 8 | `[[demonfall-gate]]` | `divine-concordat.md`, `great-betrayal.md`, `velveth.md` |
| 3 | `[[shadowdark-gaia]]` | `apotheosis.md`, `calendar.md`, `velveth.md` |
| 2 | `[[bold-republic]]` | `divine-concordat.md`, `velveth.md` |
| 1 | `[[velrathi-tea-tradition]]` | `velveth.md` (page exists as `velrathi-tea-culture.md`) |
| 1 | `[[merchant-traditions]]` | `divine-concordat.md` |
| 1 | `[[ascended-mortal-deities-mechanism]]` | `imma.md` (the mechanism is canonized as `apotheosis.md`) |
| 1 | `[[veil-gaia]]` | `icons.md` |
| 1 | `[[festival-of-broken-certainties]]` | `index.md` (page exists; the index link may have a typo or path issue) |
| 1 | `[[weave]]` | `calendar.md` (concept exists across `magic-in-eadras.md`) |
| 1 | `[[lirran-orders]]` | `log.md` |
| 1 | `[[eyeless-vigil]]` | `log.md` |
| 1 | `[[flesh-crafters]]` | `log.md` (renamed to `flesh-eaters.md`) |
| 1 | `[[mythic-retellings-of-the-cataclysm-and-demon-war]]` | `log.md` (page exists as `mythic-recitations.md`) |

**Group B — Image references that don't resolve (Obsidian wikilink-to-asset format):**

| Refs | Missing target | Referenced in |
|---:|---|---|
| 2 | `[[Eadras Golden Age Map.png]]` | `altea.md`, `arathi-golden-age-map.md` |
| 1 | `[[Spear of Crystallized Entropy.png]]` | `spear-of-crystallized-entropy.md` |
| 1 | `[[Arathi crystalmancer.jpg]]` | `arathi.md` |
| 4 | `[[Eadras Nmya post-Cataclysm.jpg]]` (4 different N values) | `eadras-tectonic-history.md` |

These are wikilinks to image assets that probably live outside the `wiki/` tree (or haven't been committed to the repo). The repo currently contains no image files — confirm whether the vault expects them in an `attachments/` folder or similar, and whether they should be checked into git.

**Group C — Wiki primer / scaffolding references (in `log.md` and `inspirations.md`):**

| Refs | Missing target | Referenced in |
|---:|---|---|
| 3 | `[[project-pre-structured-triple-ingest]]` | `log.md` |
| 2 | `[[project-map-development]]` | `log.md` |
| 1 | `[[project-magic-system-rework]]` | `log.md` |
| 2 | `[[wiki-page-1]]`, `[[wiki-page-2]]` | `log.md`, `inspirations.md` |
| 2 | `[[order-sworn-sorcerers]]` | `log.md`, `inspirations.md` |
| 1 | `[[new-page]]` | `system-governance.md` (likely a template-style placeholder, not a real link) |

The `project-*` references are to documents in `memory/` per Josh's working setup; they exist outside the public wiki and the wikilinks shouldn't resolve from within `wiki/`. The `wiki-page-1` / `wiki-page-2` references look like template placeholder text that escaped into prose.

**Recommended fix:**
- **Group A**: Decide each case. `demonfall-gate` is referenced enough (8x) that it's probably a real concept that needs a page; the others are mostly typos or path errors (`velrathi-tea-tradition` → `velrathi-tea-culture`; `flesh-crafters` → `flesh-eaters`; `mythic-retellings-…` → `mythic-recitations`). The typos can be swept; the missing concepts need decisions.
- **Group B**: Confirm the attachment-folder convention and either add the images to the repo or change the references from wikilinks to plain markdown image syntax with a non-resolving placeholder note (`*image pending*`).
- **Group C**: Most of these are in `log.md` and should be left alone (the log records historical state). The two `wiki-page-1` / `wiki-page-2` references in `inspirations.md` should be removed or replaced with real links.

---

# II. Issues Carried Forward from 2026-05-24 Register

Each entry below records the current status of an issue from the prior register, with a short refresh note where the scan revealed change.

| # | Original title | Current status | Notes |
|---:|---|---|---|
| Old 1 | Grand Conjunction cycle mismatch | **Still open** | `grand-conjunction.md` Summary vs. body contradiction remains. No commits to that file since baseline. |
| Old 2 | "Lock, not recharge" framing sweep | **Still open** | Same constraint — gated on user solidifying cycle period. |
| Old 3 | Demon War / Anti-Magic Crusade microsequence | **Still open** | No microtimeline page created since prior register. |
| Old 4 | Xar'vion's Spear-use vs Lost Zenith | **Still open** | Authorial decision pending. |
| Old 5 | Deep Vault count inconsistency | **Open (not re-verified)** | Not in this scan's scope. |
| Old 6 | Worldender crystal vs Starmetal custody | **Open (not re-verified)** | Not in this scan's scope. |
| Old 7 | Spear artifact taxonomy | **Open** | Authorial decision. |
| Old 8 | Runesword count ambiguity | **Open** | Authorial decision. |
| Old 9 | Dao concealment mechanics | **Open** | Authorial decision. |
| Old 10 | Dao's local power vs avatar limitation | **Open** | Authorial decision. |
| Old 11 | Encoding corruption / mojibake | **Reframed and escalated** — see new issue 1 above. **227 files, 6,556 instances.** |
| Old 12 | Repeated Sources-field duplication | **Confirmed open** — see new issue 6. Found on `unicorns.md` Sources line; broader sweep recommended. |
| Old 13 | Broken `peoples-of-eadras.md` table | **Still open** — see new issue 4. |
| Old 14 | `unicorns.md` page corruption | **Partial resolution** — a cleaned version exists (uploaded 2026-05-27) but is uncommitted and has its own residual issues. See new issue 2. |
| Old 15 | Deprecated / rework-pending references | **Refined and itemized** — see new issue 5. The known unfixed propagation is 5 active pages. |
| Old 16 | Frontmatter tag taxonomy mismatch | **Open (not re-verified in this scan)** |
| Old 17 | Schema compliance check | **Now itemized** — see new issues 9 (aramet leading blank) and 7 (celestia leading whitespace). |
| Old 18 | Duplicate headings and repeated sections | **Largely OK except unicorns** — see new issue 2. `dwarves.md` has a `## Naming` x2 (probably the only minor case left); all other dupes scanned are structural per-race subsections. |
| Old 19 | Mythos / Limina / Prime shell diagram needed | Open (authorial) |
| Old 20 | Chaos-object wording | Open (authorial) |
| Old 21 | Omniversal Creator vs Chaos co-eternity | Open (authorial) |
| Old 22 | Bureau of Records vs Tome as observers | Open (authorial) |
| Old 23 | Bureau of Catastrophe authority | Open (authorial) |
| Old 24 | Routine divine magic vs prayer bureaucracy | Open (authorial) |
| Old 25 | Ascended Mortal Gods and Bureau leadership | Open (authorial) |
| Old 26 | Religion in daily life | Open (development pass) |
| Old 27 | Ascended Mortal cults | Open (development pass) |
| Old 28–35 | Magic-system and society integration items | Open — see audit document §10 |
| Old 36–47 | Map and geography development items | Open — gated on map-development project per Josh's memory |
| Old 48–55 | Modern polities | Open — gated on map |
| Old 56–64 | Species and culture development | Open — race-deepening protocol pass not started |
| Old 65–72 | Artifact, antagonist, and plot readiness | Open (authorial) |
| Old 73–77 | Thematic and narrative development | Open (authorial) |
| Old 78–87 | Recommended development passes | Open |

The full descriptions of Old 1–87 are preserved in the 2026-05-24 register; this audit does not duplicate them.

---

# III. New Items Surfaced by This Scan

## 12. `system-governance.md` Section 6 was the documented user-acknowledged drift

**Priority:** High
**Type:** Governance drift
**Scope:** see new issue 10 above.

This is here primarily as a cross-reference — Josh's stored memory explicitly named "updating `system-governance.md` Section 6" as an immediate next step. New issue 10 above captures the current state of that work (in-progress, half-merged) and the specific changes needed.

---

## 13. The `wiki-page-1` / `wiki-page-2` placeholder leak in `inspirations.md`

**Priority:** Low (Maintenance)
**Type:** Authoring residue
**Scope:** `wiki/inspirations.md`

**Issue:**
`inspirations.md` contains the wikilinks `[[wiki-page-1]]` and `[[wiki-page-2]]` — clearly placeholder text that escaped a template. The line also references `[[lirra]], [[magic-in-eadras]], [[order-sharanel]], [[order-sworn-sorcerers]]` — three resolve, one (`order-sworn-sorcerers`) does not (the page was renamed to `order-sworn-netharim` in the magic-system rework).

**Recommended fix:**
Manual edit. Replace the placeholder names with the actual influences being documented, and update `order-sworn-sorcerers` → `order-sworn-netharim`.

---

## 14. Naming-conventions duplicates may or may not be intentional

**Priority:** Maintenance (verify)
**Type:** Possible duplicate sections
**Scope:** `wiki/naming-conventions.md`

**Issue:**
The page has `### Formal address` 3x, `### Given names` 3x, `### Flavor` 2x. Some duplicate-headers are legitimate per-race subsections (one Velrathi block, one Tarran block, etc.), and `naming-conventions.md` is the most likely place for this to be intentional. Worth a 60-second eyeball to confirm.

**Recommended fix:**
Visual check. If the three `### Given names` sit under three different race-context H2s, this is fine — no change needed. If two are under the same parent, one is a duplicate.

---

## 15. `wiki/dwarves.md` has `## Naming` twice

**Priority:** Low (Maintenance)
**Type:** Possible duplicate section
**Scope:** `wiki/dwarves.md`

**Issue:**
Two `## Naming` headers in a file that does not have per-subrace structure to justify duplication.

**Recommended fix:**
Manual review. Probably needs one merged into the other.

---

# IV. Suggested Work Order

Group the fixes by mechanism (mass sweep vs. targeted edit) rather than priority alone, because the sweeps unblock everything else and are mechanically cheap:

### Phase 1 — Single-session sweeps (estimated 1 working session)

1. **Mojibake sweep** (issue 1) — touches 227 files, ~6,556 substitutions; single commit.
2. **Backslash-pipe sweep** (issue 3) — touches 24 files, 136 substitutions; single commit.
3. **Line-ending normalization + `.gitattributes`** (issue 8) — single commit.
4. **Commit cleaned `unicorns.md`** (issue 2) — single commit, after issues 1 and 8 are clean so the sweep can also fix the 76 mojibake instances and CRLF in the file.

### Phase 2 — Targeted fixes (estimated 2 working sessions)

5. **Rebuild `peoples-of-eadras.md` table** (issue 4) — manual rebuild; ~30–45 minutes.
6. **Finalize `system-governance.md` §6** (issues 10 and 12) — manual cleanup, bump `Last updated`.
7. **Sweep stale references to deprecated pages** (issue 5) — 6–8 manual edits across 5 files.
8. **Fix `wiki/celestia.md`** (issue 7) — strip leading whitespace, normalize line endings.
9. **Fix `wiki/aramet.md`** (issue 9) — trim leading newline.
10. **Fix broken wikilinks Group A typos** (issue 11) — 4 typo redirects (`velrathi-tea-tradition` etc.).
11. **Fix `inspirations.md` placeholder leak** (issue 13) — manual edit.
12. **Verify `naming-conventions.md` duplicates are intentional** (issue 14).
13. **Fix `dwarves.md` duplicate `## Naming`** (issue 15).
14. **`unicorns.md` Sources line dedup** (issue 6).

### Phase 3 — Decision-required fixes (gated on Josh's authorial calls)

15. **Decide on missing-concept pages** (issue 11 Group A): is `demonfall-gate` a real concept that needs a page? Are `bold-republic`, `shadowdark-gaia`, `veil-gaia` real concepts or typos?
16. **Resolve image-asset references** (issue 11 Group B): commit the images, or change the references to placeholders.

### Phase 4 — Carryover from prior register

Old issues 1–87 from the 2026-05-24 register all remain available for selection per Josh's preferred development pass ordering (modern map geometry, climate, polity placement, conduit cities, etc.). See the prior register and the accompanying *Eadras Worldbuilding Audit* for full descriptions.

---

# V. Closing Diagnosis

The setting itself remains in very good shape — the prior audit's "strong" classifications (cosmology, deep-time history, divine architecture, Spear narrative, progenitor cultures, calendars) all held up under re-examination. The cracks are almost entirely **mechanical-residue from past corruption events**, not conceptual:

- One unrepaired sed-script aftermath (mojibake, Sources duplication, possibly unicorns.md duplication).
- One unfinalized rename sweep (deprecated stubs still referenced from active pages).
- One incomplete governance edit (Section 6 stacked headers).
- One unfinalized table rebuild (peoples-of-eadras).
- One file with leading-whitespace corruption (celestia).

These are all in the **Phase 1 + Phase 2** category — they can be cleared in 2–3 working sessions of mechanical work, and doing so will materially improve every downstream audit pass, because the noise floor on broken-link and duplicate-section detection will drop to near zero. After that, the wiki's authorial gaps (modern map geometry, modern race cultural depth, religion-in-daily-life, etc.) are what's left, and they are *gaps to fill* rather than *errors to repair*.

The 2026-05-24 register's quantitative-canon ambiguities (Grand Conjunction cycle, Demon War microsequence, Spear taxonomy) are not items this audit can close — they are authorial decisions Josh needs to make before any cleanup sweep can lock them in.

---

*End of register. Cross-reference: `Eadras_Worldbuilding_Audit.md` for the qualitative companion audit covering project status, canon stability, continuity, stubs, regional gaps, and recommended development passes.*
