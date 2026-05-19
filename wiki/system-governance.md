---
title: System Governance
tags: [meta, conventions, governance, reference]
canon_status: [established]
perspective: [reference]
historical_horizon: [all]
knowledge_access: [meta]
---

# System Governance

**Summary**: The operational rule-set governing how the Eadras wiki is structured, written, processed, and updated. Codifies the **conventions actually in use** across the wiki as of 2026-05-15: metadata standards, naming rules, calendar rules (multi-system AP-and-mortal architecture), canon hierarchy, AI interaction rules, and the protocol-derivation discipline that keeps `wiki/protocols/` synchronized with canon. Distinct from [[inspirations|Inspirations]] (design principles for how Eadras should *feel*) and from [[principles-of-eadras|Principles of Eadras]] (in-world cosmological laws). When a page is added, refactored, or processed by an AI session, it must conform to this document.

**Sources**: Direct codification of established practice across 273 pages of `wiki-export-2026-05-15.md`; the `wiki/_sealed/README.md` sealed-folder rules; the `wiki/naming-conventions.md` morphology canon; the `wiki/protocols/` protocol-page conventions; user direction 2026-05-15 (governance canonization, AP system, multi-calendar architecture, plugin integration). 2026-05-16 reconciliation pass with `CLAUDE.md` (axes block, OOC tonal-references block, schema exceptions, renames-and-aliases, source-to-wiki ingest workflow, question-answering, lint, citation format, backups-and-exports section, no-`sed` rule).

**Last updated**: 2026-05-16

---

## How to read this document

This is a **reference page**, not in-world content. It uses `perspective: [reference]` and `knowledge_access: [meta]`. The Tome of Baldaran does not contain a page about how its own wiki is organized; this is OOC author/curator infrastructure, alongside [[naming-conventions|Naming Conventions]], [[calendar|Calendar Systems of Eadras]], and [[eadras-timeline|Eadras Timeline]].

The eight sections below are independent; reference the relevant one for the task at hand.

This document is **canonical for wiki rules**. The Claude Code skill at `.claude/skills/eadras-wiki/SKILL.md` loads it on every session and applies the rules below to all wiki edits and ingest processing. The prompt-template files under `wiki/protocols/` are *portable primers for external AI sessions* (Grok, ChatGPT, fresh Claude sessions without the skill) and must themselves conform to this governance.

### Hierarchy of authority

When sources conflict, this is the order of precedence:

1. **`wiki/` (in-world canon)** — the source of truth. Always wins.
2. **`wiki/_sealed/` (OOC plot-spine secrets)** — overrides public canon only on the specific points it covers; otherwise non-canonical-facing. Bound by sealed-folder rules (Section 4).
3. **This governance document** — canonical for *rules*, not for *setting facts*. Updates to setting facts go in wiki pages first.
4. **`wiki/protocols/`** — derived export layer; never canonical. Regenerated when canon drifts.
5. **Author/session-local working notes** — not canon until merged into `wiki/`.
6. **`canon_status: [deprecated]` pages** — formerly canonical; cite only for traceability.

User direction during a session supersedes all canon for that session; the wiki is then updated to match.

---

## 1. Metadata Standards

Every wiki page MUST have YAML frontmatter at the top of the file, between two `---` lines. The order shown below is the canonical order; preserve it when editing.

### Frontmatter fields — required across all pages

| Field | Type | Description |
|---|---|---|
| `title` | string | Display title. Human-readable, not the filename. Title Case for proper nouns and major concepts; sentence case for common-noun pages. |
| `tags` | list | Category and topic tags. The **first tag** is the primary category and serves the role of a type field — the wiki does not use a separate `type:` field. |
| `canon_status` | list (single value) | `established` / `proposed` / `pending` / `deprecated` |
| `perspective` | list (single value) | `tome-neutral` / `tome-recovered` / `tome-sealed` / `reference` / `ooc` |
| `historical_horizon` | list (single value) | `all` / `primordial` / `progenitor-era` / `nerathi-era` / `high-firethorn` / `demon-war` / `dimming` / `modern-era` |
| `knowledge_access` | list (single value) | `common` / `general` / `scholarly` / `esoteric` / `meta` / `sealed` |

### Frontmatter fields — optional

| Field | Type | Description |
|---|---|---|
| `aliases` | list | Alternative titles for wikilinking and search. **Required on renamed pages** — every prior slug and display-name must be listed so existing `[[oldslug]]` wikilinks resolve. See Section 2 *Renames and aliases*. |
| `axes_profile` | dict | Four-axis position on the [[axes-of-creation\|Axes of Creation]]. Each axis takes a value in `[-1.0, 1.0]`. Only set on pages whose subject occupies a meaningful position (cultures, factions, races, major individuals, religious orders, philosophical movements); only populate after the user confirms values via the Meta Bind sliders. See Section 1 *Axes-of-Creation block* below for the slider markup. |
| `cssclasses` | list | Omit when no class applies. The standard value is `axes-unset`, present on axes-block pages until `axes_profile` values are confirmed; remove it once values are set. Obsidian's native property folding handles the property-panel; no custom CSS is required. |

### Frontmatter fields — required on event/history pages

Pages tagged `events` or `history` (or any page describing a dated occurrence) MUST include the calendar fields:

| Field | Type | Description |
|---|---|---|
| `ap_date` | list (single value, integer or string) | The **Absolute Physical** cosmologically-true date. Required. Use `[unknown]` when the Tome's value has not been canonized. See Section 3 and [[calendar]]. |
| `bp_date` | list (single value, integer) | The Before-Present mortal-system date. Required for any event with a documented BP value. |
| `firethorn_regnal` | list, optional | Firethorn regnal year (e.g. `[Thoramis Year 340]`). Use only for Firethorn-era events. |
| `first_rebrightening` | list, optional | First Rebrightening year (Fr. value). Use only for modern-era events. |
| `dragon_empire_cycle` | list, optional | Dragon Empire imperial-cycle date. Use only when the event is recorded in Dragon Empire records. |
| `velrathi_banishment` | list, optional | Velrathi Banishment-count year. Use only for post-Banishment Velrathi events. |
| `katharim_ledger` | list, optional | Katharim death-ledger year. Use when the event appears in the Katharim records. |
| `bold_conduit_cycle` | list, optional | Bold conduit-cycle date. Use only for Bold-era events. |

All single-value fields are formatted as a single-item list in square brackets — `canon_status: [established]`, not `canon_status: established`. This is a YAML convention for Obsidian property-pane compatibility; do not change it.

### Field value reference

#### `tags` first-tag categories

The first tag is the page's primary category. The set in use across the wiki:

- **People & beings**: `races`, `deities`, `creatures`, `entity`
- **Cosmos & laws**: `cosmology`, `natural-law`, `plane`
- **Places**: `geographic-feature`, `settlement`, `region`, `country`
- **Culture & practice**: `culture`, `tradition`, `religion`
- **Magic & craft**: `magic`, `alchemy`
- **History**: `history`, `events`
- **Things**: `document`, `organization`
- **Era-specific bundling**: `arathi` (when combined with another primary tag for Arathi-era material)
- **Reference & meta**: `meta`, `sealed`, `ooc`

Additional tags after the first describe topic, era, faction, or salient relationships.

#### `canon_status`

- **`established`** — confirmed canonical material. Downstream pages may rely on it.
- **`proposed`** — under active development; may shift before being established. Use for working drafts and exploratory canon.
- **`pending`** — depends on resolution of some other piece of canon. Use sparingly.
- **`deprecated`** — formerly canonical, superseded, retained for traceability.

#### `perspective`

- **`tome-neutral`** — the standard in-world wiki voice (the Tome's curated record). Most pages.
- **`tome-recovered`** — material reconstructed by the Tome from fragmentary or archaeological sources; signals uncertainty.
- **`tome-sealed`** — in-universe sealed-chapter framing (distinct from `_sealed/` folder; see Section 4).
- **`reference`** — out-of-world meta material (naming conventions, timeline, this document).
- **`ooc`** — explicitly out-of-character author/DM notes; used in `wiki/_sealed/` and `wiki/protocols/`.

#### `historical_horizon`

- **`all`** — covers multiple eras or is timeless.
- **`primordial`** — pre-creation or creation-era material.
- **`progenitor-era`** — pre-Nerathi deep pre-history.
- **`nerathi-era`** — Arathi/Nerathi hypercivilization through Cataclysm.
- **`high-firethorn`** — Firethorn Empire's mature period (~18,000–10,000 BP).
- **`demon-war`** — Demon War and immediately surrounding events.
- **`dimming`** — Anti-Magic Crusade through Thousand-Year Dimming.
- **`modern-era`** — post-Dimming through present.

#### `knowledge_access`

- **`common`** — known to ordinary mortals.
- **`general`** — known to educated mortals.
- **`scholarly`** — restricted to scholars, archmagi, senior clergy.
- **`esoteric`** — restricted to specialized orders, inner clergy, deep practitioners.
- **`meta`** — out-of-world reference material.
- **`sealed`** — author/DM-only material in `wiki/_sealed/`.

### Schema exceptions

The full schema applies to every wiki content page with the following narrow exceptions:

- **`wiki/log.md`** — append-only operational log. Bare `title:` + `tags:` only; no meta-fields.
- **`wiki/index.md`** — table of contents. Bare `title:` + `tags:` only.
- **`wiki/_sealed/*`** — sealed pages. Full schema applies, but always with `perspective: [tome-sealed]` and `knowledge_access: [sealed]`. Never linked from public pages; one-way linking only (Section 4).
- **`wiki/rpg/*`** — splat-book / OOC RPG material. Full schema applies, but always with `perspective: [ooc]`. The `canon_status` reflects the stage of the splat material (typically `pending`), not Eadras-canon status.
- **`wiki/protocols/*`** — context-loading and work-driving prompt documents. Full schema applies, with `perspective: [ooc]` and `knowledge_access: [meta]`.
- **Reference pages** (`tags.md`, `naming-conventions.md`, `eadras-timeline.md`, `open-questions.md`, `worldbuilding-needs.md`, `calendar.md`, this document) — full schema applies with `perspective: [reference]` and `knowledge_access: [meta]`.

### Body structure

After frontmatter, every page follows this body structure:

1. `# Title` — H1 matching the `title:` frontmatter field. The body starts directly with the H1; no toggle or decoration between the closing `---` of the frontmatter and the heading. Obsidian's native property folding handles the property-panel display.
2. `**Summary**: …` — one-paragraph in-prose summary.
3. `**Sources**: …` — provenance line listing raw materials, ingest files, or user-direction dates.
4. `**Last updated**: YYYY-MM-DD` — ISO date.
5. `---` — horizontal rule.
6. Body content with `##` section headers.
7. `<details><summary>Related pages</summary>…</details>` — collapsible "Related pages" section with wikilinks. Always the last thing on the page.

### Axes-of-Creation block

Pages whose subject occupies a meaningful position on the [[axes-of-creation|Axes of Creation]] (cultures, factions, races, major individuals, religious orders, philosophical movements) include a collapsible slider block bound to the frontmatter `axes_profile` dict via Meta Bind. Insert before the *Related pages* block:

````markdown
<details class="axes-block">
<summary>Axes of Creation profile</summary>

**Masculine ↔ Feminine**
`INPUT[sliderAdvanced(minValue(-1), maxValue(1), stepSize(0.05), addLabels):axes_profile.masculine_feminine]`

**Altruism ↔ Self-Interest**
`INPUT[sliderAdvanced(minValue(-1), maxValue(1), stepSize(0.05), addLabels):axes_profile.altruism_self_interest]`

**Obedient ↔ Independent**
`INPUT[sliderAdvanced(minValue(-1), maxValue(1), stepSize(0.05), addLabels):axes_profile.obedient_independent]`

**Wisdom ↔ Foolishness**
`INPUT[sliderAdvanced(minValue(-1), maxValue(1), stepSize(0.05), addLabels):axes_profile.wisdom_foolishness]`

</details>
````

While values are unset, the page carries `axes-unset` in `cssclasses`. Once the user has confirmed the slider values via Meta Bind (which writes them directly into the frontmatter `axes_profile.<axis>` keys), **remove `axes-unset` from `cssclasses`**. The slider block itself stays on the page so values can be adjusted later.

Pages whose subject does not occupy a meaningful axis position (cosmological constructs, abstract concepts, locations, artifacts, purely descriptive reference pages) omit both the `axes_profile` field and the slider block; do not add `axes-unset`.

### OOC tonal-references block

When the user has explicitly cited real-world or fictional cultural touchstones, stated an intended civilizational feel, or specified visual motifs for a page, document them in a collapsible block clearly marked OOC, placed **before** the Related pages block:

````markdown
<details class="ooc-block">
<summary>Author-side worldbuilding annotations (OOC)</summary>

### Cultural shorthand
- **[Tradition 1]** — e.g. Ottoman imperial administration
- **[Tradition 2]** — e.g. Renaissance Italian merchant-prince politics

### Intended civilizational feel
[One- or two-sentence description of the tonal / civilizational register the in-universe content is built to evoke.]

### Visual motifs
- **[Motif 1]** — e.g. Golden stone
- **[Motif 2]** — e.g. Monumental stairways

</details>
````

Any subsection may be omitted if it doesn't apply. Use only when the user has explicitly supplied the content; **do not invent cultural shorthand, intended feels, or visual motifs**. The block preserves the in-universe Tome conceit by clearly stepping outside it: the in-universe subject is not derivative of the cited works; the works are cited because they capture the *feel* the canon is built around.

For pages whose only OOC content is a small list of tonal touchstones (no intended-feel statement, no visual motifs), the simpler form remains valid: a single bulleted list under the `Author-side worldbuilding annotations (OOC)` summary, without sub-headings.

### Related pages block

Wrap the related-pages list in a collapsible block (blank lines around the inner content):

```markdown
<details>
<summary>Related pages</summary>

- [[page-1]]
- [[page-2]]

</details>
```

This block is the **last thing on the page**. Aggressively link related pages; this is the wiki's primary navigation surface.

### Templates

Templater templates for the major page types live under `wiki/templates/`. Each template auto-fills the frontmatter and seeds the canonical body structure for its type. The standing templates:

- `wiki/templates/template--event.md` — for `events` and `history` pages (full calendar fields)
- `wiki/templates/template--deity.md` — for `deities` pages
- `wiki/templates/template--race.md` — for `races` pages
- `wiki/templates/template--place.md` — for `geographic-feature`, `settlement`, `region`, `country` pages
- `wiki/templates/template--organization.md` — for `organization` and `religion` pages
- `wiki/templates/template--new-page.md` — generic template for any new wiki page; prompts for category and seeds appropriate frontmatter

When creating a new page, use the appropriate template via `Templater: Open Insert Template Modal`. Editing the templates themselves requires user direction (they encode the canonical structure).

---

## 2. Naming Rules

Conventions for the *form* of names. For the *style and structure* of names by people (Arathi theophorics, Velrathi gothic, Elfen melodic, etc.), see [[naming-conventions|Naming Conventions]].

### Filenames

- **Lowercase, hyphen-separated, no spaces, no apostrophes, no diacritics**: `eadras-timeline.md`, `house-valtharion.md`, `dashar.md` (for *Da'shar*), `xarvion.md` (for *Xar'vion*).
- **Singular form** unless the canonical title is plural (`aberrations.md` is plural because the page is about the category).
- **Filename matches `title:` frontmatter semantically but not necessarily verbatim** — filenames strip punctuation for filesystem portability; titles preserve formal form.

### Singular/plural conventions

- **People names default to invariant**: *Arathi* serves singular and plural. *Velrathi*, *Tarani*, *Elfen*, *Beast-Folk*, *Katharim* likewise.
- **Where separate plurals exist, the people's page documents them**: *Orug* → *Orugi*; *Grug* → *Grugi*. Default when in doubt: invariant.
- **Disambiguate overlapping names carefully**: *Rathar* (engineered race) vs *Rathari* (their cultural-institutional designation).
- **Empires use the possessive**: *the Firethorn Empire's*, *the Dragon Empire's* — never an `-ish` or `-an` derivation.

### Adjectival forms

- **People names form adjectives via hyphenated qualifiers, not endings**: *Arathi crystalmancy*, *Velrathi architecture*, *Beast-Folk circles*.
- **Era-feeling derivations use the Arathi/Nerathi prefix form**: *Nerathi-era*, *Arathi-style*.
- **Empires take possessive form**: *the Firethorn Empire's bureaucracy*.

### Empire and polity naming

- **Empires named by founding house, throne, or characteristic emblem** + the word *Empire*: *the Firethorn Empire*, *the Dragon Empire*, *the Amunorian Empire*.
- **Capitalize the full proper-noun phrase**; the article *the* is lowercase except at sentence-start.
- **Modern polities use their own canonical forms**: *Bold*, *Orden*, *the Azure Basin*.

### Transliteration registers

- **Arathi/Nerathi scholarly register** — diacritics preserved: *Kudur-eṭir*, *Ilu-nāṣir*, *Ašar-kalib*. Filenames drop diacritics.
- **Velrathi gothic register** — apostrophe-only, no diacritics: *Veyr'Keth*, *Vorandethi*, *Xar'vion*. Preserve the apostrophe.
- **Modern Eadran register** — clean Latin alphabet: *Bold*, *Orden*, *Solis Bay*.

### Capitalization

- **Proper nouns**: capitalized — *the Long Quiet*, *the Hall of the Long Quiet*, *the Divine Concordat*, *Article Four*.
- **Concept-titles that have become proper nouns**: capitalized — *Apotheosis*, *Icon*, *Simulacrum*, *Mythos*, *Source*, *Weave*.
- **Common-noun cognates**: lowercase — *the gods* (generic), *a wizard*, *priests*.
- **The definite article *the* before a proper-noun phrase**: lowercase except at sentence-start.

### Wikilinking

- **Use display-text wikilinks when the slug and in-context phrasing differ**: `[[firethorn-throne|Firethorn Throne]]`, `[[gods-of-eadras#Ascended Mortal Gods|Ascended Mortal Gods]]`.
- **Plain wikilinks when slug and display would match**: `[[velveth]]`, `[[imma]]`.
- **First mention on a page should be linked**; subsequent mentions need not be.
- **One-way for `_sealed/` content**: sealed→public OK, public→sealed forbidden (see Section 4).

### Renames and aliases

When a wiki page is renamed (slug changes), the renamed page **must carry an `aliases:` frontmatter** listing every prior slug and display-name that referred to the same concept. Old `[[oldslug]]` wikilinks elsewhere in the wiki — including `log.md` history, raw-source quotes, and any links the rename sweep missed — will then continue to resolve to the renamed page via Obsidian's alias system.

Example, after `taran.md` → `tarans.md`:

```yaml
aliases: [Taran, taran, Tarran]
```

The aliases convention is the **safety net** for cross-file renames. It does not replace the wikilink sweep (the sweep keeps wikilinks visually current); the two work together.

The Python sweep tooling at the repo root (`sweep_wikilinks.py`, `sweep_padded_links.py`, `verify_no_stale_slugs.py`) is the canonical mechanism for cross-file rename sweeps. **Never use `sed -i` or `awk -i` for cross-file edits** — a runaway sed sweep can destroy every wiki file mid-session. Use the Edit tool for one-offs; use Python `str.replace`-based scripts at repo root for sweeps. Always `--dry-run` first.

---

## 3. Calendar Rules

The Eadras wiki uses a **two-tier multi-system calendar architecture**. Full documentation lives at [[calendar|Calendar Systems of Eadras]]; this section codifies what every wiki page must observe.

### The architecture in brief

- **AP (Absolute Physical time)** is the cosmologically-true master system. Anchored at the Primordial Sacrifice (AP 0). Used only by the Tome and the Gods. Stored as hidden frontmatter (`ap_date`) on every event page.
- **Mortal calendars** are multiple, coexistent, mutually-disagreeing, all approximate relative to AP. Six canonical systems: BP, Firethorn regnal, First Rebrightening (Fr.), Dragon Empire cycles, Velrathi Banishment-count, Katharim death-ledger years, Bold conduit-cycles.
- **No mortal calendar is precise relative to AP.** Conversions between mortal systems are imperfect. This is canonical, not a flaw.

### What every event page must record

1. **`ap_date` in frontmatter** — required. Use `[unknown]` when not yet canonized.
2. **`bp_date` in frontmatter** — required when a documented BP value exists in the timeline.
3. **Any applicable mortal-calendar field** in frontmatter — populate the fields appropriate to the event's cultural context (Firethorn-era events get `firethorn_regnal`; modern-era events get `first_rebrightening` and/or `bold_conduit_cycle`; Dragon Empire events get `dragon_empire_cycle`; etc.).
4. **The page's primary display date in body text** uses the calendar most appropriate to the event's cultural context (Firethorn regnal years for Firethorn-era events; Bold conduit-cycles for Bold mercantile events; etc.).

### Format conventions

- **AP integers**: comma-separated for large numbers — `12,345,678`. The Tome's published precision; lower-precision values use approximate notation: `~12,300,000`.
- **BP integers**: comma-separated — `10,000,000 BP`, `39,000 BP`. Approximate values use `~`: `~6,000,000 BP`. Million-year-scale informal references may use *mybp*.
- **Firethorn regnal**: *Emperor-Name Year N* — `Thoramis Year 340`.
- **First Rebrightening**: *Fr. N* — `Fr. 412`.
- **Dragon Empire cycles**: *Cycle N Year M* — `Cycle 142 Year 23`.
- **Velrathi Banishment-count**: *Banishment Year N* — `Banishment Year 8,213`.
- **Katharim death-ledger**: *D.L. N* — `D.L. 8,201`.
- **Bold conduit-cycles**: *C.C. N Year M* — `C.C. 9 Year 412`.

### Cross-system citations

When citing a date that exists in multiple systems, the primary display uses the culturally-appropriate calendar; the parenthetical includes the BP approximation for cross-reference:

> *Thoramis Year 340 (~10,000 BP)*
> *Fr. 412 (~7,588 BP)*
> *Cycle 142 Year 23 (~150 BP)*

The AP value remains hidden in frontmatter; it does not appear in body text unless the page is specifically discussing AP-versus-mortal-system divergence.

### Page-update discipline when canon shifts

When a calendar value is updated on a page (e.g. a Tome value is published; a regnal date is corrected from a primary source):

1. Update all relevant frontmatter fields on the event page.
2. The Dataview-driven master conversion table at [[calendar]] picks up the change automatically.
3. Other pages citing the event's date in body text must be updated manually. Use the wiki's link-graph (or the appropriate Dataview query) to find references.
4. Log the change in `wiki/log.md` if the shift affects multiple pages or load-bearing canon.

### AP magnitude is open canon

The Tome holds AP values to whatever precision it has determined. The wiki may use `ap_date: [unknown]` for events whose AP magnitude has not been published. The gap-tracking Dataview query at [[calendar]] surfaces such events for curator triage.

---

## 4. Canon Hierarchy

Five canon classes with strict precedence rules.

### Precedence

(Highest authority first.)

1. **`wiki/` pages with `canon_status: [established]`** — load-bearing canon. The wiki is the source of truth for any in-world fact.
2. **`wiki/_sealed/` pages** — override public canon only on the specific points they cover; bound by sealed-folder rules. Never leak back to public pages.
3. **This governance document** — canonical for *rules*, not for *setting facts*.
4. **`wiki/` pages with `canon_status: [proposed]` or `[pending]`** — working canon; flag any contradiction with established canon.
5. **`wiki/protocols/`** — derived export layer. Never canonical. Regenerated when canon drifts.
6. **`canon_status: [deprecated]`** — formerly canonical; cite only for traceability.

### Sealed canon rules

Pages in `wiki/_sealed/` are out-of-character author/DM notes — plot-spine secrets held back from the public wiki to preserve narrative tension. Full rules in `wiki/_sealed/README.md`; the load-bearing five:

1. **No wikilinks into `_sealed/` from any page outside the folder.** Public pages remain navigable without leaking secrets.
2. **No summarizing sealed contents back into public pages.** Cross-references are one-way.
3. **When updating a public page, do not betray that a sealed counterpart exists.** Use *"currently unknown to mortals"*, *"the gods have not revealed"*, *"lost to time"*.
4. **Only update sealed pages on explicit user direction.** Treat sealed files as the user's plot notebook.
5. **Public-facing breadcrumbs** (rumors, sailor tales, sealed-chapter teases) go in the *public* page they relate to, as fragmentary in-world hearsay.

Distinguish `_sealed/` (OOC author canon) from `tome-sealed` (in-universe sealed-chapter framing).

### Probabilistic and contingent canon

Some sealed pages document **probabilistic future-states** the Tome has detected. Body-text status markers used alongside `canon_status: [proposed]`:

- **`POTENTIAL_FUTURE`** — event has not occurred; Tome detects probable branch.
- **`TIMELINE_CONTINGENT`** — event depends on multiple conditions; branch may collapse.

When citing contingent canon, qualify: *"in the actualised-branch reading of [[sculptor-of-silence]]"*, not *"per [[sculptor-of-silence]]"*.

### Deprecated content

When canon shifts and a page is superseded:

1. Set `canon_status: [deprecated]` in frontmatter.
2. Add header note: *"**Deprecated YYYY-MM-DD.** Superseded by [[new-page]]. Retained for traceability."*
3. Redirect wikilinks from other pages to the new canonical target.
4. Do not delete the page; deletion breaks the audit trail.
5. Record the deprecation in `wiki/log.md`.

---

## 5. AI Interaction Rules

Rules for AI sessions working on or with the wiki. Applies to Claude Code (via the skill), to external AI sessions using `wiki/protocols/` primers, and to any human-AI collaboration on canon.

### Canon resolution

- **Later canon supersedes earlier canon** when the two conflict on the same point.
- **User direction supersedes all canon during the session** in which it is given. Do not argue prior canon against an explicit user correction; propagate the correction to the wiki.
- **Unresolved contradictions must be flagged, not resolved silently.** Surface conflicts to the user with a summary of what each source says; ask which is canonical.
- **When canon is silent on a point**, mark it as open canon — *"the wiki has not established this"*, *"this is open for future development"* — rather than inventing a fact.

### Tone and content

- **Preserve the thematic spine**: *continuity · memory · catastrophe · identity · structure · survival · meaning*. Every new element must touch at least one.
- **Avoid genre defaults**: Eadras refuses generic-high-fantasy, generic-empire, generic-bureaucracy-of-evil framings. When in doubt: *"would this be plausibly produced by the being or culture said to produce it?"*
- **Eadras is epic dark fantasy with *earned* hope, not grimdark.** *"Light and darkness cannot exist without each other. The presence of one makes the other bigger, deeper, brighter."* Tone references: *Wheel of Time*, *Stormlight Archive*. **Never grimdark.** Nihilism is acceptable only as a villain's philosophy, never as the narrative's frame.
- **Mystery is stronger than explanation.** Some material (Apotheosis mechanism, Decree wording, Tome interior) is deliberately sealed. Do not invent procedural detail for material the wiki has chosen to leave mysterious.
- **Match canonical style on high-quality reference pages** when writing new material. Reference pages: `aberrations.md`, `arathi.md`, `arathi-cataclysm.md`, `magic-in-eadras.md`, `divine-bureaucracy.md`, `worldbuilding-needs.md`. Match the prose register, structural rhythm, and depth of those pages rather than reverting to RPG-supplement summarization.

### Interpretive vs authoritative distinctions

- **The wiki is authoritative**; the protocols are interpretive.
- **`wiki/protocols/` files are derived exports** — condensed for external-AI context-window constraints. They drift as upstream canon shifts.
- **When a protocol and a wiki page disagree, the wiki page wins.** The protocol should be regenerated.
- **Do not treat protocol-stated facts as canonical** when wiki access is available.
- **`canon_status: [proposed]` pages** are interpretive-leaning; treat as authoritative for current work but flag conflicts with `[established]` material.

### Generation discipline for new content

1. **Check for existing canon first.** Search the wiki for prior treatment before introducing a new name, place, person, or concept. Extend rather than create parallels.
2. **Follow the metadata template** (Section 1). Frontmatter is non-negotiable.
3. **Use the appropriate Templater template** for new pages — see Section 1, *Templates*.
4. **Cite sources in the Sources line, and inline where load-bearing.** Every page records the raw materials it derives from. Inline citations use the format `(source: filename.ext)` after the claim. When two sources disagree, note the contradiction explicitly. When a claim has no source, mark it as needing verification rather than asserting it.
5. **Match the perspective register** (Section 1). Do not mix registers within a page.
6. **Place `LIVE WIRES` sections at the end of ingest documents**, not in published wiki pages.
7. **For new races, polities, or peoples**: use the protocol at `wiki/protocols/race-deepening-protocol.md`.

### Source-to-wiki ingest workflow

When the user adds a new raw source to `raw/` (or to `D:\Worldbuilding\Chat Logs\` for the large chat-log archive) and asks for it to be ingested:

1. **Read the full source document.** Do not skim; the lore is usually load-bearing.
2. **Discuss key takeaways with the user before writing anything.** Surface contradictions with existing canon, ambiguities, and decisions that need user input. Get explicit go-ahead before producing wiki pages.
3. **Create a summary page in `wiki/`** named after the source (e.g. `goldenwood.md` for a goldenwood-source ingest).
4. **Create or update concept pages** for each major idea or entity. A single source may touch 10–15 wiki pages — that is normal.
5. **Add wikilinks `[[page-name]]`** to connect related pages. Aggressively cross-link.
6. **Update `wiki/index.md`** with new pages and one-line descriptions.
7. **Append an entry to `wiki/log.md`** with the date, source name, and what changed. The log is append-newest-first; new entries go at the **top** of the file.

After any significant change, cross-reference `wiki/open-questions.md` and `wiki/worldbuilding-needs.md` for live wires that may have been resolved or sharpened.

### Ingest-document processing

When processing a raw AI chat into pre-structured ingest documents (the triple/quad export shape):

- **File naming**: snake_case truncations of the TOPIC header. E.g. `velveth-01-inworld-facts.txt`.
- **Four files per topic** when narrative scenes are appropriate: 01 in-world facts, 02 meta-commentary, 03 principles-and-diagnosis, 04 narrative-scenes. Three files when the topic is purely abstract; skip file 04.
- **Tag with `[CANONIZED]`** for new canon; **`[WIKI_REFINED]`** for canon that extends or sharpens an existing page.
- **End every file with `LIVE WIRES`** of open questions.
- **Ingest documents are not canon yet** — they are processed inputs for user review. Treat as `[proposed]`-grade until merged.

### Question answering

When the user asks a question about the setting:

1. **Read `wiki/index.md` first** to find relevant pages.
2. **Read those pages and synthesize an answer.**
3. **Cite specific wiki pages** in the response via wikilinks.
4. **If the answer is not in the wiki, say so clearly** — do not invent.
5. **If the answer is valuable**, offer to save it as a new wiki page or as an addition to an existing page. Good answers should be filed back into the wiki so they compound.

### Lint and audit

When the user asks for a lint or audit:

- Check for **contradictions between pages**.
- Find **orphan pages** (no inbound wikilinks).
- Identify **concepts mentioned in pages that lack their own page**.
- Flag **claims that may be outdated** based on newer canon.
- Check that all pages **follow the body structure** (Section 1).
- Verify **frontmatter compliance** (required fields present; values within locked enums).
- Report findings as a numbered list with suggested fixes.

### Protocol back-propagation

When canon shifts in the wiki, the relevant protocol(s) under `wiki/protocols/` must be regenerated:

1. Identify the drift — what wiki page changed, which protocols depend on it.
2. Regenerate the affected protocol(s) from the current wiki state.
3. Version-promote (v1 → v2). Record changes in *Changes from previous version* section.
4. Update `Last updated` date.
5. `canon_status: [pending]` during rewrite; restore to `[established]` when finalized.

---

## 6. Backups and Exports

The wiki is **not under git**. The `wiki-export-YYYY-MM-DD.md` file at the repository root is the only cross-file recovery mechanism. The export is a single concatenated file containing every wiki page separated by `=== / FILE: wiki/<name> / ===` delimiter blocks; it can be split back into individual files via `split_export.py`.

### Two outputs per export run

`generate_export.py` (locked 2026-05-11) produces **two** files every run:

- **`wiki-export-YYYY-MM-DD.md`** — *full*. Includes everything under `wiki/`: canon, `_sealed/`, `rpg/`, `protocols/`, reference/meta pages, and `log.md`. This is the canonical backup and the file trusted users receive. One per day; same-day re-runs overwrite silently.
- **`wiki-export-YYYY-MM-DD-public.md`** — *public*. Stripped for sharing with external AI collaborators. Excludes `wiki/_sealed/*` (sealed plot-spine), `wiki/log.md` (operational changelog), `wiki/index.md` (TOC), and `wiki/inspirations.md` (OOC real-world touchstones). Keeps all in-universe canon plus `tags.md`, `naming-conventions.md`, `open-questions.md`, `worldbuilding-needs.md`, this document, `calendar.md`, and the entire `wiki/rpg/` and `wiki/protocols/` subfolders.

Stripping happens at **export-generation time**, not at share time — there is no separate "remember to strip" step. Always share the `-public.md` file; never hand the unsuffixed full export to anyone outside the trusted circle.

`--full-only` and `--public-only` flags exist for single-output runs.

### When to generate a fresh export

- After any **large change session** that touched many pages or made schema-altering changes (rename sweeps, full-wiki backfills, multi-page retcons).
- **Before closing down a session** if any wiki content has been modified that day, even on small sessions.

### Restoring from an export

`split_export.py` reverses an export back into individual `wiki/*.md` files. Supports `--only-sealed` (extract only the sealed-folder pages) and `--fix-mojibake` (repair UTF-8 corruption on the way out). The 2026-05-10 incident — when a runaway `sed -i` destroyed every wiki page mid-session — was recovered from the previous day's export via this tool.

### Cross-file edits and the no-`sed` rule

For sweeps across many files (renames, terminology shifts, schema migrations), **always use the Python `str.replace`-based scripts at repo root**: `sweep_wikilinks.py`, `sweep_padded_links.py`, `verify_no_stale_slugs.py`, and topic-specific sweep scripts as they're added. Always run with `--dry-run` first; verify the change set before committing.

**Never use `sed -i` or `awk -i`** for cross-file edits. The 2026-05-10 incident is the load-bearing reason: an in-place stream-editor regex destroyed every wiki file mid-session and required a full restore from the previous day's export. The Edit tool is fine for one-offs; Python sweep scripts are the cross-file equivalent.

---

## 7. The Protocol Layer

`wiki/protocols/` exists for one specific reason: **the wiki has grown larger than external AI sessions can load in a single context window**. Protocols are portable primers that compress relevant canon into context-window-sized blocks, paste-able into Grok, ChatGPT, fresh Claude sessions without skill access, etc.

### What protocols are

Protocols are `[ooc] [meta]` reference documents, structured as:

1. Frontmatter with `tags: [meta, eadras]`, `canon_status: [pending]` (during development) or `[established]` (stable), `perspective: [ooc]`, `historical_horizon: [all]`, `knowledge_access: [meta]`.
2. **Summary** explaining what the protocol does.
3. **Sources** citing raw materials and the wiki state the protocol derives from.
4. **Usage** explaining when and how to paste the protocol into a session.
5. **Protocol** section — the paste-able content in a fenced code block.
6. **Changes from previous version** section (v2+).
7. **Drift-watch** section listing upstream wiki pages whose changes trigger regeneration.

### What protocols are NOT

- **Not canon.** Condensed exports of canon. Wiki wins on conflict.
- **Not setting content.** They never describe new lore — they only re-export existing wiki canon.
- **Not user-facing reading material.** Paste-targets for AI sessions, optimized for token-density not human readability.

### Standing protocols

- **`core-canon-and-thematic-principles.md`** — foundational context primer for any Eadras AI session.
- **`race-deepening-protocol.md`** — 10-section template for systematically expanding any race.
- *(future protocols)* — additional task-specific templates as recurring workflows are identified.

### Drift-watch

Every protocol must include a *Drift-watch* section listing the upstream wiki pages whose material changes trigger regeneration. The core-canon protocol's drift-watch is the model:

- New principles added to upstream principles pages
- Magic-system changes
- Modern Powers additions or restructuring
- New named-canon events at major scale
- Changes to the Tier-1 Icon-Simulacrum framework or cosmological-floor canon

When a drift-watch trigger fires, the protocol is regenerated and version-promoted.

---

## 8. Plugin Integration

The wiki runs on Obsidian with the following plugins; this section describes how they integrate with governance.

### Required plugins

- **Templater** — programmatic templates for new-page creation. Templates live under `wiki/templates/`; see Section 1 *Templates*. Editing templates requires user direction.
- **Dataview** — queryable metadata. The [[calendar]] page uses Dataview queries to render the master conversion table dynamically from event-page frontmatter; gap-tracking queries surface incomplete pages. New Dataview queries should be added to relevant reference pages (calendar, timeline, open-questions) rather than scattered across content pages.
- **Chronos Timeline** — visual timeline rendering. The [[calendar]] page's visual timeline uses `chronos` codeblocks. Event pages may embed local Chronos blocks where a single-event visualization adds clarity.
- **Meta Bind** — bidirectional widgets bound to frontmatter. Useful for author-side workflows (toggling `canon_status`, selecting `perspective`, entering AP/BP dates). Templates may include Meta Bind widgets for guided authoring.

### Supporting plugins

- **Admonitions** — styled callouts. Use the standard Obsidian callout syntax (`> [!note]`, `> [!warning]`, `> [!important]`); custom admonition types may be defined for deprecated-page warnings, sealed-page entry markers, calendar-drift notices.
- **Excalidraw** — embedded hand-drawn diagrams. Use for cosmology diagrams, geographical sketches, sealed-page schematic maps. Embedded files live under `excalidraw/` in the vault root.
- **Kanban** — board view for task tracking. Used for open-questions triage, protocol regeneration queues, sealed plot-spine management. Kanban boards live under `kanban/` in the vault root and are `ooc`-grade content.
- **PDF++** — enhanced PDF embedding. Used in `raw/` source-document archival, not in wiki pages directly.
- **Importer** — bulk import from external formats. Used for ingest workflows; results route through the standard wiki-ingest process.
- **BRAT** — beta-plugin auto-updater. Operationally relevant; no canon impact.

### Plugin-aware page authoring

- **Dataview queries embedded in pages** must be syntactically clean DQL or JS-Dataview. Test the query before committing.
- **Chronos codeblocks** must follow the plugin's syntax. The [[calendar]] page is the model.
- **Templater templates** should be tested against the current frontmatter spec before adoption.
- **Meta Bind widgets** should bind to existing frontmatter fields, not introduce new ones (frontmatter spec lives in Section 1).

---

## Quick reference

### When making any wiki edit

- Frontmatter present with all required fields ✓
- First tag is the primary category ✓
- Calendar fields (`ap_date`, `bp_date`, system-specific) present on event/history pages ✓
- `canon_status` matches the page's actual confidence level ✓
- `perspective` matches the voice the page is written in ✓
- Summary, Sources, Last updated header in place ✓

### When introducing new canon

- Searched the wiki for prior treatment ✓
- Used the appropriate Templater template ✓
- Followed the relevant style register (Arathi / Velrathi / modern) ✓
- Calendar fields populated where applicable ✓
- Capitalization matches established convention ✓
- Sourced the new material in the Sources line ✓

### When canon shifts

- Public page updated first ✓
- Calendar Dataview query re-runs automatically; verify display ✓
- Dependent pages updated for consistency ✓
- Affected protocols flagged for regeneration ✓
- Deprecation handled per Section 4 if applicable ✓
- `wiki/log.md` updated ✓

### When the wiki is silent on a point

- Mark as open canon explicitly — do not invent ✓
- Surface to user as a *Live wire* in working notes ✓
- Add to `wiki/open-questions.md` if load-bearing ✓

---

<details>
<summary>Related pages</summary>

- [[calendar]]
- [[naming-conventions]]
- [[eadras-timeline]]
- [[principles-of-eadras]]
- [[inspirations]]
- [[open-questions]]
- [[_sealed/README|Sealed Folder README]]

</details>
