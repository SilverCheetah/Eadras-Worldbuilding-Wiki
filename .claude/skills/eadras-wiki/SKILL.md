---
name: eadras-wiki
description: Use this skill whenever working with the Eadras worldbuilding wiki at D:\Worldbuilding\Worldbuilding LLM Wiki — editing wiki pages, adding new canon, processing AI chat ingests into wiki-ingest documents, regenerating prompt protocols, working with calendar systems (AP, BP, Firethorn regnal, First Rebrightening, Dragon Empire cycles, Velrathi Banishment-count, Katharim death-ledger, Bold conduit-cycles), or answering questions about Eadras canon. Triggers on file edits under wiki/, on ingest-document processing tasks (filenames matching *-01-inworld-facts.txt, *-02-meta-commentary.txt, *-03-principles-and-diagnosis.txt, *-04-narrative-scenes.txt), on protocol regeneration under wiki/protocols/, on any reference to Eadras canon, and on user requests mentioning specific Eadras topics (gods, peoples, the Great Betrayal, Apotheosis, Velveth, Imma, the Tome of Baldaran, calendars, AP dates, etc.). Do NOT use this skill for non-Eadras worldbuilding work.
---

# Eadras Wiki Skill

Operational rules for Claude Code work on the Eadras worldbuilding wiki at `D:\Worldbuilding\Worldbuilding LLM Wiki\`.

## On every session-start touching the wiki

1. **Read `wiki/system-governance.md` first.** Canonical rule-set for everything below. Every metadata, naming, calendar, canon-hierarchy, and AI-interaction rule is documented there.
2. **Read `wiki/calendar.md`** for the full calendar-system reference if the task touches dates.
3. **Skim `wiki/eadras-timeline.md`** to ground BP chronology and era anchors before producing dated material.
4. **Check `wiki/_sealed/README.md`** if the working topic might touch sealed material; the one-way-link rule is absolute.

## Source-of-truth precedence

(Highest authority first.)

1. `wiki/` pages with `canon_status: [established]`
2. `wiki/_sealed/` pages (plot-spine secrets only; bound by sealed-folder rules)
3. `wiki/system-governance.md` (for rules, not setting facts)
4. `wiki/` pages with `canon_status: [proposed]` or `[pending]` (flag conflicts with established canon)
5. `wiki/protocols/` files (derived exports; never canonical — regenerate when canon drifts)
6. `canon_status: [deprecated]` pages (traceability only)

User direction during a session supersedes all canon for that session; update the wiki to match.

## Key reference pages

Consult these directly rather than restating from memory:

- **`wiki/system-governance.md`** — the canonical rule-set
- **`wiki/calendar.md`** — AP and mortal-calendar systems, conversion table, gap-tracking queries
- **`wiki/naming-conventions.md`** — per-people naming styles, Velrathi title morphology, Arathi theophorics
- **`wiki/eadras-timeline.md`** — canonical chronology, era anchors, event dates
- **`wiki/principles-of-eadras.md`** — 36 in-world cosmological principles
- **`wiki/inspirations.md`** — thematic spine and design principles
- **`wiki/open-questions.md`** — load-bearing canon gaps and live wires

## Folder semantics

| Folder | Purpose | Rules |
|---|---|---|
| `wiki/` | In-world canon (273+ pages) | Default working area. All metadata, naming, calendar, hierarchy rules apply. |
| `wiki/_sealed/` | OOC plot-spine secrets | One-way wikilinks only (sealed→public OK, public→sealed forbidden). No leakage. Only update on explicit user direction. |
| `wiki/protocols/` | Portable primers for external AI sessions | Derived export layer; never canonical. Regenerate when upstream canon drifts. |
| `wiki/rpg/` | Game-mechanic-specific material | Conforms to governance; separate subfolder for navigability. |
| `templates/` | Templater templates for new pages | `event.md`, `deity.md`, `race.md`, `place.md`, `organization.md`, `new-page.md`. Edit only on user direction. |
| `excalidraw/` | Embedded Excalidraw diagrams | Referenced from wiki pages but stored separately. |
| `kanban/` | Task-tracking boards | OOC-grade; not canon. |
| `raw/` | Source-document archive | Raw chat exports, PDFs, ingest materials. Not canon. |
| `.claude/skills/eadras-wiki/` | This skill | Loaded on every Eadras session. |

## Calendar discipline

Eadras uses a **two-tier multi-system calendar architecture**. Critical points:

- **AP (Absolute Physical time)** is the cosmologically-true master, anchored at the Primordial Sacrifice. **Only the Tome and Gods originate AP dates.** Mortals never derive AP — they only quote what was handed to them.
- **Six mortal calendars** are canonical, all approximate relative to AP, all mutually-imperfect when converted to each other: BP, Firethorn regnal, First Rebrightening (Fr.), Dragon Empire cycles, Velrathi Banishment-count, Katharim death-ledger years, Bold conduit-cycles.
- **Every event page must have `ap_date` in frontmatter** (even if `[unknown]`). The Dataview gap-query at `wiki/calendar.md` surfaces pages missing this.
- **Display the culturally-appropriate calendar in body text**; cite BP as the cross-reference: *Thoramis Year 340 (~10,000 BP)*.
- **Mortal-calendar disagreements are not errors.** A Velrathi date and a Katharim date for the same event will differ by a few decades; the gap reflects mortal drift from AP-truth.

When working on event pages:

1. Use `templates/event.md` for new event pages — it prompts for all calendar fields.
2. For existing pages missing `ap_date`, add it as `[unknown]` if the Tome's value has not been canonized. Do not invent AP values.
3. Add applicable mortal-calendar fields based on the event's cultural context.
4. The Dataview conversion table at `wiki/calendar.md` will pick up the changes automatically.

## Working tasks

### Editing a wiki page

1. Read the existing page in full before editing. Note its frontmatter values.
2. Preserve frontmatter integrity. Field order from `system-governance.md` Section 1.
3. Update `Last updated:` to the current real-world date (ISO format).
4. Update `Sources:` if the edit derives from new raw material.
5. If the edit changes a load-bearing fact, check whether any `wiki/protocols/` page depends on it. Flag for regeneration.
6. If the edit adds or changes a date, ensure calendar fields are consistent.

### Adding a new wiki page

1. Confirm the topic does not exist. Search the wiki first.
2. **Use the appropriate Templater template** from `templates/` — the template prompts for required frontmatter via Templater's suggester/prompt API. For event pages, `templates/event.md` handles the full calendar field set.
3. Filename: lowercase, hyphen-separated, no spaces, no apostrophes, no diacritics.
4. Body structure: properties-toggle widget, H1 title, Summary, Sources, Last updated, horizontal rule, body with `##` headers, optional Related pages collapsible.
5. Mark `canon_status: [proposed]` if not yet finalized; promote to `[established]` after user review.

### Processing an AI chat into ingest documents

1. Follow the system-prompt ruleset (canonical ingest-processing prompt, typically in `raw/`).
2. Filename: snake_case truncation of the TOPIC header, not the literal word "topic." E.g. `velveth-01-inworld-facts.txt`.
3. Produce 3 or 4 files per topic: 01 in-world facts, 02 meta-commentary, 03 principles-and-diagnosis, 04 narrative-scenes (only when narrative warrants).
4. Mark new canon `[CANONIZED]`; mark canon that sharpens existing wiki pages `[WIKI_REFINED]`.
5. End every file with `LIVE WIRES` of open questions.
6. **Ingest documents are not canon yet** — they are processed inputs for user review. Do not merge into wiki without explicit user direction.

### Regenerating a protocol

1. Read the protocol's drift-watch section. Read the upstream pages it depends on.
2. Rewrite the protocol body to match current canon.
3. Version-promote: v1 → v2.
4. Add or update the *Changes from previous version* section.
5. Set `canon_status: [pending]` during the rewrite; restore to `[established]` when finalized.

### Answering an Eadras canon question

1. Search the wiki for the topic.
2. Cite the relevant pages by wikilink in your response.
3. If the wiki is silent or contradictory, say so explicitly. Do not invent.
4. If user asserts canon that differs from the wiki, treat user direction as authoritative for the session and flag the discrepancy for wiki update.

## Plugin awareness

The wiki uses Obsidian with the following plugins. Be aware when editing:

- **Templater** — templates in `templates/` use Templater syntax (`<%* %>` for code, `<% %>` for variable substitution). Templates prompt for frontmatter via `tp.system.prompt` and `tp.system.suggester`. Test templates after editing; broken Templater syntax breaks page creation.
- **Dataview** — DQL queries in pages (e.g. the conversion table at `wiki/calendar.md`). Use DQL for tables and JS-Dataview only when DQL is insufficient. Queries depend on frontmatter field names being consistent across pages — do not rename fields without updating queries.
- **Chronos Timeline** — visual timelines via `chronos` codeblocks. The `wiki/calendar.md` page is the model. Event codeblocks use `EVENT [tag] AP/BP-date ~ description` syntax; period codeblocks use `PERIOD [tag] start - end # description`.
- **Meta Bind** — bidirectional widgets bound to frontmatter. Useful for author workflows; do not add Meta Bind widgets that bind to fields not in the frontmatter spec.
- **Admonitions** — use standard Obsidian callout syntax (`> [!note]`, `> [!warning]`, `> [!important]`). Avoid plugin-specific custom admonition types unless they are vault-wide canon.
- **Excalidraw, Kanban, PDF++, Importer, BRAT** — supporting plugins; do not embed their content in wiki canon pages without explicit reason. Excalidraw diagrams in `excalidraw/`, Kanban boards in `kanban/`, raw materials in `raw/`.

## What this skill never does

- Never invent canon to fill a gap silently. Open canon is open canon; surface it.
- Never invent AP date values. The Tome's precision is the Tome's to publish; use `ap_date: [unknown]` until canonized.
- Never write content with genre-default framing (generic high fantasy, generic dark fantasy, generic elves, generic empire). Every element should be plausibly produced by the specific being or culture said to produce it.
- Never leak `wiki/_sealed/` material into public pages, even obliquely.
- Never describe procedural detail for sealed mysteries (Apotheosis mechanism, Decree wording, Tome interior, etc.).
- Never treat `wiki/protocols/` content as canonical when wiki access is available.
- Never skip frontmatter on a new page. Pages without frontmatter are non-canonical and will break wiki tooling.
- Never rename frontmatter fields without updating all Dataview queries that reference them.
- Never modify Templater templates without explicit user direction.

## Thematic spine (non-negotiable)

`continuity · memory · catastrophe · identity · structure · survival · meaning`

Every new element of Eadras must touch at least one. Binding constraint on all canon expansion.

## When in doubt

Read `wiki/system-governance.md` again. Then ask the user. Do not improvise on rules.
