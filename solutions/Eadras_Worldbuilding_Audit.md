# Eadras Worldbuilding Audit

**Audit date:** 2026-05-27
**Repository:** `https://github.com/SilverCheetah/Eadras-Worldbuilding-Wiki` (`main` branch, baseline commit `857a096`)
**Audit scope:** All public wiki pages under `wiki/` (284 markdown files total; 274 audited — 4 `_sealed/` files referenced by filename only per governance §4; 6 `templates/` files excluded as scaffolding).
**Refreshes:** 2026-05-24 *Eadras Worldbuilding Audit*. This document carries forward the qualitative findings of that audit and refreshes them against the current repo state, with particular attention to the items flagged for completion in Josh's working notes.
**Companion:** *Eadras_Issues_Register.md* — the mechanical-issue list with priorities and recommended fixes.

**Method**:

- Direct programmatic scan of the live repo for mojibake, broken wikilinks, deprecated-reference propagation, duplicate sections, frontmatter compliance.
- Cross-reference of findings against the 2026-05-24 audit and issues register.
- Verification of items in Josh's stored project memory (Section 6 governance status, `unicorns.md` corruption, git migration baseline).

**Standing rules observed**:

- No new lore invented.
- Exact names and spellings preserved.
- Ambiguity flagged, not resolved.
- Inter-page disagreements marked as **possible contradictions** for author decision.
- Stubs treated as signals about authorial attention, not failures.

**Standing reminder**: The wiki maintains two excellent internal audit pages — `wiki/open-questions.md` (last touched 2026-05-14) and `wiki/worldbuilding-needs.md` (last touched 2026-05-09). This audit cross-references them rather than duplicating their content; they remain the authoritative living indexes.

---

## 1. Project Status Summary

### Most developed (stable, internally consistent, recent canon activity)

The strong-spine classifications from the 2026-05-24 audit hold up under re-examination. No previously-strong area has degraded:

- **Cosmology of magic and metaphysics.** Four-order magic system (`wizards.md`, `priests.md`, `netharim.md`, `lexanari.md`), `pillar-magic.md`, `true-language.md`, the Weave as defensive structure (`magic-in-eadras.md`), `seven-conduits.md`, `eldritch-cycle.md`. The 2026-05-09 rework plus the 2026-05-14 make-it-mine pass closed nearly every load-bearing question. `druids.md` is preserved as a sub-priesthood specialization (not retired, as the rework log entry might suggest at first read).
- **Deep-time history.** `eadras-timeline.md`, `arathi-cataclysm.md`, `worldbreaker-mechanism.md`, `chaos-crusades.md`, `eldravath.md`, `great-exchange.md`, `demon-war.md`, `great-betrayal.md`, `great-banishment.md`, `anti-magic-crusade.md`, `lost-zenith.md`. The 10-million-year master chronology is locked.
- **Divine architecture and doctrine.** `divine-bureaucracy.md`, `infernal-bureaucracy.md`, `icons.md`, `apotheosis.md`, `doctrine-of-unheld-hand.md`, `doctrine-of-open-palm.md`, `three-bells-of-intervention.md`, `hearth-witness-mandate.md`, `petition-of-abandoned-circumstance.md`, `divine-concordat.md`, `decree-of-shali-shani-ioa.md`, `baldaranic-council-cycle.md`, `divine-containment-protocols.md`. Theology remains one of the wiki's strongest layers.
- **Spear-of-Crystallized-Entropy containment narrative.** `spear-of-crystallized-entropy.md` (four-hidings sequence), `grand-conjunction.md` (despite a stale Summary line — see §3.1), `divine-containment-protocols.md`, `black-hand.md`, `white-palm.md`. The 2026-05-13 supersession resolved most prior tension.
- **Progenitor races' cultural layers.** `velrathi.md` + `velrathi-architecture.md` + `velrathi-tea-culture.md` + `velrathi-cognitive-frogs.md`; `tarans.md` + `taran-architecture.md` + `taran-venom-aged-liquor.md`; `elfen.md` + `elfen-architecture.md` + `elfen-blossom-wines.md`. Architecture and signature drinks remain nailed down.
- **Calendars.** `calendar.md` plus the six mortal systems (AP, Firethorn regnal, First Rebrightening, Dragon Empire cycles, Velrathi Banishment-count, Katharim death-ledger, Bold conduit-cycles) are documented and mutually understood as imperfect.
- **Cultural-drinks tree.** `aqua-vitae.md` and the seven race-specific signature-drink pages, with `tchoukou.md` and `goblin-tunnel-cheese.md` extending the foodways layer.

### New strong areas not classified in prior audit

- **Three Cultures Ethical Triangle.** `three-cultures-ethical-triangle.md` formalizes the goblin / Amunorian / Dragon Empire axis as a coherent philosophical configuration. This is a recent strong-canon addition.
- **Cross-cultural bathing customs.** `bathing-customs.md` is unusually thorough — Velrathi origin, Rathari/Beast-Folk propagation, Orden cast-iron pots, gnome/goblin practice. A small-scale model of how cultural diffusion is documented elsewhere should follow.
- **Mythic recitations.** `mythic-recitations.md` consolidates dragon, unicorn, humanoid, orcish, Katharim, and Tome scholarly recitation voices for the three foundational catastrophes (Cataclysm, Chaos Incursions, Demon War). Load-bearing for any future Eadran mythic-recitation material.

### Partially developed (skeleton present; substance uneven) — unchanged from prior audit

- **Modern political geography** — see §6 and §9 below. Gated on map geometry.
- **Cosmology of outer planes** — `celestia.md`, `nyxar.md`, `dreadharrow.md`, `concordance.md`, `bastion-of-light.md`, `nexus.md` remain thin. `celestia.md` is additionally **file-corrupted** (see Issue Register #7).
- **Modern race cultural and demographic detail** — gated on race-deepening protocol passes.
- **Religion in daily life** — institutional skeleton rich; folk-religious layer absent.
- **Languages** — metaphysical hierarchy locked; in-fiction linguistic detail open.
- **Cosmology of the deep oceans** — Bathyric Mandate explicitly deferred.

### Underdeveloped (mostly absent on the present-day axis) — unchanged

- Modern continental geography.
- Climate, biome, rivers, ecology of the modern world.
- Magical economy.
- Magical communication infrastructure.
- Magical agriculture, medicine, standardized transport.
- Ascended Mortal Gods roster (13 named; ~6 with substantive pages).
- Standard fantasy bestiary by biome.
- Pre-Eldravath survivor continent pages (`avalon.md`, `damedes.md`, `culethor.md`, `therion.md`, `aurettos.md`) — tectonic-snapshot stubs.

### Quantitative snapshot — refreshed

- **284** total markdown files in `wiki/` on the live repo.
- **274** active content/reference files (excluding `_sealed/`, `templates/`).
- **3** explicit `[deprecated]` pages: `dashar.md`, `heart-of-the-goddess.md`, `weavespinners.md` — see Issue Register #5 for cleanup of references to them.
- **227** files contain UTF-8 round-trip mojibake corruption (`â€` byte triplets) — see Issue Register #1.
- **0** true orphan pages — every active wiki page has at least one inbound wikilink. This is a strong sign of cross-linking discipline, unchanged since prior audit.
- **44** broken-target wikilinks across 27 unique missing targets — see Issue Register #11. **Excluding** the 136 backslash-pipe-corrupted wikilinks in tables, which are a separate mechanical issue (Issue Register #3).
- **272** files use LF line endings; **1** (`wiki/celestia.md`) uses CRLF — file-corruption artifact, see Issue Register #7.

User's stored working estimate (per memory): **35–65% complete**. The wide uncertainty band is appropriate; the 2026-05-27 scan does not tighten it because most of the gap is authorial-development work, not mechanical-completeness work.

---

## 2. Canon Stability Assessment

The 30-row classification table from the 2026-05-24 audit holds without material change. Three notes on refresh:

| # | Lore area | Classification (current) | Refresh note |
|---|---|---|---|
| 12 | Magic system (four orders + Pillar Magic + Weave) | Stable canon | Druids confirmed as sub-priesthood (not retired); 69 wikilinks to `druids.md` are correct. |
| 18 | Anti-Magic Crusade + Black Hand + Century of Sorrows | Stable canon, timeline pinch still open (§3.2) | No new commits to relevant pages since prior audit. |
| 19 | Spear of Crystallized Entropy + Grand Conjunction precessional cycle | **Contradictory (Summary vs body) — unfixed since prior audit** | See §3.1. |
| 30 | Tag taxonomy / system governance | **In flux** — `system-governance.md` Section 6 in mid-edit | See Issue Register #10. |

The other 27 rows of the prior table remain as classified; refer to *Eadras_Worldbuilding_Audit.md* 2026-05-24 §2 for the unchanged rows.

---

## 3. Continuity and Consistency Issues

The 11 continuity items from the prior audit (§3.1–§3.11) all remain unresolved. Direct re-verification of three high-priority ones:

### 3.1 Grand Conjunction cycle period — Summary vs. body

**Confirmed still open.** `grand-conjunction.md` line 12 Summary still says *"recurring on a roughly 5,000-year cycle"*; the body says **10,000 years final**. The fix is one line. Per `open-questions.md`, the cross-page sweep (over Spear, Lost Zenith, timeline, Black Hand) is **explicitly deferred** until Josh solidifies the period; only the in-file contradiction is actionable now.

### 3.2 Demon War (~10,000 BP) and Anti-Magic Crusade (~9,000–10,000 BP) overlap

**Confirmed still open.** No microtimeline page added since prior audit. The Weave-creation-during-Crusade question still depends on Josh's decision about explicit sequencing.

### 3.3 Mirror-plane corruption sequencing — First Chaos Crusade vs Spear hidings

**Confirmed still open.** One sentence on each of four pages would close it, but no edits since prior audit.

The other 8 continuity items from prior §3 (Weave / Eldravath unicorn / Verdant Scar / Demonfall Marches / Sea'tua dating / Unheld vs Open Palm / Icon vs Avatar) remain in their prior status and are reproduced by reference rather than re-listed here.

---

## 4. Mechanical Wiki Hygiene (new section)

This section is a new addition to the audit, because the issues it covers are large enough in scope to deserve top-level treatment rather than being scattered through the rest of the report. Full details, file lists, and proposed fixes live in the **Eadras Issues Register**; this section sums the impact for orientation.

### 4.1 Encoding corruption (mojibake)

**Scope:** 227 of 274 audited files contain UTF-8 → cp1252 → UTF-8 round-trip corruption. ~6,556 character-level instances. The signature is the byte triplet `â€` (from re-decoded em dash, en dash, smart quotes, ellipsis).

**Where it hurts most:** Every page whose summary or body uses em dashes — which is nearly every prose page. Currently visually tolerable but breaks any text-search-by-special-character workflow and any export-to-other-format pipeline.

**Why it matters:** This is the largest single-mechanism issue surface in the wiki and the highest-leverage one to fix — one Python pass closes it on every file at once.

### 4.2 Backslash-pipe wikilink corruption in markdown tables

**Scope:** 24 files contain 136 instances of `[[slug\|Display]]` (literal backslash before alias-pipe inside the wikilink target). The backslash was placed to escape the table-cell-separator pipe but ended up inside the wikilink itself, breaking 136 wikilinks in Obsidian.

**Where it hurts most:** Reference tables that aggregate races, gods, calendars, languages. `peoples-of-eadras.md` (27), `gods-of-eadras.md` (14), `elfen.md` (11), `velrathi.md` (9). These are exactly the high-traffic navigation tables.

**Why it matters:** Tables in these pages currently render as broken navigation. Single Python sweep closes it.

### 4.3 `unicorns.md` duplication corruption

**Scope:** One file. The live committed version has the section `## The unicorn mythic voice — sorrowful, watchful, alarmed` and its body block **repeated 262 times**, expanding the file to 2,400 lines / 411KB when the real content is ~280 lines.

**Status:** A cleaned 312-line version was uploaded to this conversation 2026-05-27 but **has not been committed to the repo**. The cleaned version still has CRLF line endings and 76 mojibake instances of its own.

**Why it matters:** This is the most acute single-file corruption in the wiki. Closing it via commit, after running the mojibake and line-ending sweeps, removes the most-visible damaged page.

### 4.4 Deprecated-reference propagation

**Scope:** Three correctly-deprecated stub pages (`dashar.md`, `heart-of-the-goddess.md`, `weavespinners.md`) are still wikilinked from 5 active pages (`conduit-cities.md`, `voroik.md`, `lirra.md`, `inspirations.md`, `eras.md`).

**Why it matters:** This is the specific issue Josh flagged ("lingering deprecated lore fragments"). Per governance §4, *"Redirect wikilinks from other pages to the new canonical target."* The redirection wasn't done in the 2026-05-14 rework. The fix is 6–8 manual edits.

### 4.5 `system-governance.md` Section 6 mid-merge state

**Scope:** One section in one file. Two `## 6.` headers stacked back-to-back (`## 6. Backups and Exports` immediately followed by `## 6. Backups and Recovery`). The stale section body was deleted; the stale header was not. `Last updated` was not bumped to reflect the new git-workflow content.

**Why it matters:** This is the specific item Josh's working memory flagged as the immediate next step ("updating `system-governance.md` Section 6"). The governance document is *meta-canonical for rules* (per its own §4), so a half-merged state in it is more disorienting than a half-merged state in setting canon.

### 4.6 Other small-scale mechanical issues

- `celestia.md`: 193 bytes of garbage `\r` characters before frontmatter; CRLF line endings (the only CRLF file in the repo). Both file-corruption artifacts.
- `aramet.md`: one blank line before frontmatter; minor schema deviation.
- `peoples-of-eadras.md`: table structurally broken (5 columns rendered when 3 are intended; wikilinks split across columns). See §4.2 and Issue Register #4.
- `dwarves.md`: `## Naming` heading appears twice — probable accidental duplicate.
- `inspirations.md`: `[[wiki-page-1]]` and `[[wiki-page-2]]` placeholder wikilinks escaped a template.
- `unicorns.md` Sources line: same source string repeats three times after a previous corruption residue.

---

## 5. Map-Layer Coverage Audit

The 47 audit rows on map / climate / geography / placement from the prior audit (§5–§8) remain unchanged. The map development project is still in-progress per Josh's memory; no map pages have been added or substantively changed.

**Key gating items**, in order of unblocking effect:

1. **Modern continent geometry.** Eldravath breakup is not yet drawn. Without it, every polity sits in named-but-unplaced space.
2. **Conduit termini placement.** 14 termini known; only Bold has substantive detail; 13 unfilled slots. Each is a natural campaign-region anchor.
3. **Climate / biome overlay.** Universally absent except for `amunorians.md` (desert original, Mediterranean diaspora). Resolves §9's universal Biome-column gap.
4. **Trade route overlay.** Defined for Bold–Orden–Azure triangle; absent elsewhere.
5. **Rivers and freshwater.** Almost no named rivers anywhere; minor exception in Amunor.

---

## 6. Modern Polities and Cultures

Status unchanged from prior audit (§6, §9, §10). The 19-criterion grid in prior §9 holds — no polity has had a substantive development pass since 2026-05-24. Three observations:

- **Language column remains universally missing.** No polity has a documented spoken language. Most homogeneous gap in the modern-cultures axis.
- **Clothing column remains nearly universally missing.** Tariq al-Honor is the lone exception with explicit garment detail.
- **Foodways column remains the strongest of the underdeveloped columns,** anchored by the cultural-drinks tree and `tchoukou.md` / `goblin-tunnel-cheese.md`.

**Recommended first focus:** Bold–Orden–Azure triangle. It is the only region readable as a campaign setting today; completing it (Orden Hanseatic structure, Bold republic governance, Azure Basin internal politics) would make one region fully playable, which is a discrete and motivating milestone.

---

## 7. Historical Causality Audit

Unchanged from prior audit (§7, §8). The wiki's historical causality remains unusually well-traced for a setting at this stage; the major flag is still §3.2 (Demon War / Crusade overlap). Minor flags from the prior audit (Tariq al-Honor founding mechanism, Sarathim spatial origin, Bold founding event) remain in their prior status.

---

## 8. Stub Ideas and Underdeveloped Concepts

`open-questions.md` and `worldbuilding-needs.md` remain the authoritative living indexes. The top-impact stub catalog from the prior audit (§4.1 modern continental map; §4.2 thirteen unfilled conduit cities; §4.3 Ascended Mortal Gods roster; §4.4 outer-plane inhabitants; etc., through §4.15 deep-sea civilization) is unchanged.

**The 2026-05-27 scan confirms two patterns worth highlighting**:

1. **The "weight by inbound links" pattern.** `demonfall-gate` (8 broken inbound wikilinks) is referenced more than several other developed concepts. Inbound link-count of broken targets is a useful priority signal for which missing pages to create first.
2. **The "typo vs. concept" disambiguation.** Some broken wikilinks point at near-existing slugs (`velrathi-tea-tradition` → real page is `velrathi-tea-culture`; `mythic-retellings-of-the-cataclysm-and-demon-war` → real page is `mythic-recitations`). These are typos to sweep, not concept gaps. Others (`demonfall-gate`, `bold-republic`, `shadowdark-gaia`, `veil-gaia`) genuinely refer to pages that don't exist; Josh needs to decide whether they should.

---

## 9. Culture / Nation Template Gaps

Unchanged from prior audit (§9). The 19-criterion grid covering 19 polity rows holds; no row's coverage has materially shifted since 2026-05-24.

---

## 10. Magic / Metaphysics Integration Audit

Unchanged from prior audit (§10). The magic system remains well-balanced at the design layer; the wording reconciliation in `magic-in-eadras.md` (§3.4 of prior audit) is still open. No new contradictions surfaced.

---

## 11. Inter-Audit Drift: What Has and Hasn't Changed Since 2026-05-24

This section exists to make the rate-of-progress visible.

### Has changed

- **Repository migration**: The wiki is now under git (baseline commit `857a096` on `main`). Per Josh's memory, GitHub repo is at `SilverCheetah/Eadras-Worldbuilding-Wiki` and the migration is complete. (The `system-governance.md` Section 6 update reflecting this is in progress but not yet finalized — see Issue Register #10.)
- **`unicorns.md` cleanup in progress**: The 262× duplication has been resolved in a draft uploaded 2026-05-27; commit pending.
- **(Possibly)** governance Section 6 content. The new content references the git workflow but the stale "Backups and Exports" header is still adjacent.

### Has not changed

- The 11 continuity items from prior §3.
- The 87 development items in the prior issues register.
- The 30-row canon-stability classification.
- The qualitative gap-coverage in modern political geography, modern race cultural depth, religion-in-daily-life, languages, biome layer, magical economy, magical communication.
- The mojibake corruption (this is the biggest non-finding; it was flagged 2026-05-24 and was not swept).
- The deprecated-stub propagation (flagged 2026-05-24; not swept).
- The `peoples-of-eadras.md` table (flagged 2026-05-24; not rebuilt).

### Implication

The mechanical-hygiene items have the largest impact-per-effort ratio of any work currently available. Every one of them is locatable, fixable in one session, and removes a class of noise that obscures the more interesting authorial work below. Three working sessions of mechanical sweep work would clear the hygiene backlog and leave the audit landscape much cleaner for the next round of development passes.

---

## 12. Items Skipped from Prior Audit

A small number of items from the 2026-05-24 audit (§11 Areas where modest content additions could go; §12 What is fine left as-is; §13 Recommended development passes; §14 Source file index) are not reproduced in this refresh because they remain accurate as written and don't benefit from repetition. Refer to the 2026-05-24 audit for those sections; they remain in force.

---

## 13. Recommended Next Development Passes (refresh)

Re-ordered against the cleanup backlog. Phase numbering matches the Issues Register §IV.

### Phase 1 — Mechanical hygiene sweeps (1 session)

Issues Register items 1, 2, 3, 8. These unblock everything downstream by removing noise.

### Phase 2 — Targeted manual fixes (2 sessions)

Issues Register items 4, 5, 6, 7, 9, 10, 11 (Group A typos), 13, 14, 15. These close most of the open hygiene items.

### Phase 3 — Authorial decisions (gated on Josh)

- Continuity items 3.1–3.11 from prior audit.
- Image-asset convention (Issues Register #11 Group B).
- Missing-concept decisions (Issues Register #11 Group A: `demonfall-gate`, `bold-republic`, `shadowdark-gaia`, etc.).

### Phase 4 — Development passes (from prior audit §13)

In order of unblocking effect:

1. **Modern map geometry pass** — already in progress per memory.
2. **Climate and biome pass** — gated on (1).
3. **Polity placement pass** — gated on (1)+(2).
4. **Conduit cities pass** (12 unfilled termini) — gated on (1).
5. **Trade routes and rivers pass** — gated on (1)+(3).
6. **Ascended Mortal Gods roster + Bureau assignment pass** — independent; can run any time.
7. **Magic-in-society pass** — independent.
8. **Religion-in-daily-life pass** — independent.
9. **Race deepening pass per playable race** — independent.
10. **Stub-cleanup pass on outer planes and thin Elder God pages** — independent; small.

Items 6–10 are independent of the map work and can be tackled in parallel with the map pass.

---

## 14. Source File Index

Direct programmatic reads during this audit:

- All 274 active content files under `wiki/` (excluding `_sealed/`, `templates/`).
- `wiki/log.md` (full read; not in bundle but in live repo).
- `wiki/index.md`, `wiki/system-governance.md` (uploaded 2026-05-27 refresh), `wiki/open-questions.md`, `wiki/worldbuilding-needs.md`, `wiki/calendar.md`.
- 2026-05-24 *Eadras_Issues_Register.md* and *Eadras_Worldbuilding_Audit.md* (for refresh cross-reference).
- Live GitHub repo `SilverCheetah/Eadras-Worldbuilding-Wiki` cloned at baseline `857a096`.

`wiki/_sealed/README.md`, `wiki/_sealed/fourth-attempt-impalement.md`, `wiki/_sealed/probability-fracture-child.md`, `wiki/_sealed/sculptor-of-silence.md` — referenced by filename only per sealed-folder governance; contents not read.

Templates (`wiki/templates/template--*.md`) — listed but not audited as content.

---

*End of audit. Cross-reference: `Eadras_Issues_Register.md` for the per-issue actionable list and priority groupings. `open-questions.md` and `worldbuilding-needs.md` remain the authoritative living indexes for open canon and forward-looking gaps.*
