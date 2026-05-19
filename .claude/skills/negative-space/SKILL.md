---
name: negative-space
description: Scan the wiki for under-covered cells of (historical_horizon × race × tag) and identify the parts of canon that are thin and worth writing into. Output is a ranked list of gaps with suggested page topics, written to derived/negative-space/. Read-only over the wiki; never modifies canon. Use when the user wants to know what to develop next, where the canon is thin, or which expected combinations of era/race/theme have no coverage.
---

# Negative Space

A vault-wide negative-space scan. Identifies cells in the (historical_horizon × race × tag) coverage grid that are sparsely populated, and reports the top gaps with suggested page topics.

The point of this skill is to convert "what should I write next?" from a guessing game into a query. The wiki itself contains the answer; this skill exposes it.

## When to invoke

- `/negative-space` — full vault scan, top 20 gaps reported.
- `/negative-space <era>` — focus on what's thin within one specific historical_horizon era (e.g., `/negative-space high-firethorn`).
- `/negative-space <race>` — focus on what's thin around one race or lineage (e.g., `/negative-space velrathi` or `/negative-space halflings`).
- `/negative-space <tag>` — focus on one canonical tag from `wiki/tags.md`.
- `/negative-space deep` — slow mode: read every page's body for thematic gaps as well as frontmatter gaps. Use sparingly; it's expensive.

## Procedure

1. **Enumerate wiki pages.** Glob `wiki/**/*.md`. Exclude `wiki/_sealed/` by default per CLAUDE.md's sealed-page rules (the user can override with `/negative-space sealed`). Also exclude `wiki/log.md`, `wiki/index.md`, `wiki/tags.md`, `wiki/open-questions.md`, `wiki/worldbuilding-needs.md` (meta pages, not canon-coverage).
2. **Read frontmatter** of each page — `tags`, `historical_horizon`, `canon_status`, `perspective`. Skip body content unless `deep` mode is invoked.
3. **Build the coverage grid.** For each (era × racial-tag) pair, count pages. For each cell, record:
   - Number of pages
   - Sample of titles
   - Predominant `canon_status` (rough proxy for maturity)
4. **Identify gaps.** Cells with zero pages are *full gaps*. Cells with one or two pages are *thin gaps*. Cells with five or more are well-populated.
5. **Filter for salience.** A cell isn't a "gap" if it's *expected* to be empty. Use canon to determine which cells are non-applicable:
   - Race didn't exist yet in that era (e.g., halflings before the Change).
   - Era pre-dates relevant cosmology (e.g., demon-war content during primordial era).
   - The race is established as never having been in the relevant region/era.
   Existing canon should drive these exclusions; if uncertain, mark as *plausible gap* and let the user confirm.
6. **Cross-reference [[open-questions]] and [[worldbuilding-needs]].** Pages flagged there are known gaps; the scan should pick them up and rank them.
7. **Rank gaps** by:
   - **Activity recency** — eras and races that appear frequently in the most recent log.md entries are "active" and gaps in them are higher-priority.
   - **Adjacent density** — a cell with zero pages whose neighbours (adjacent era × same race, or same era × adjacent race) are dense is an anomalous gap.
   - **User-flagged status** — items in open-questions or worldbuilding-needs rank highest.
8. **Suggest specific page topics** for each top gap. Three concrete suggestions per gap, drawn from what would plausibly fill it. The skill does *not* propose canon content; only topic names.
9. **Write output** to `derived/negative-space/scan-YYYY-MM-DD.md` using the structure below.

## Output structure

```markdown
# Negative-Space Scan: <date>

**Scan scope:** <full / era=X / race=Y / tag=Z / deep>
**Pages scanned:** N
**Cells evaluated:** (E × R)
**Date:** YYYY-MM-DD

---

## Coverage summary

| Axis | Best-covered | Worst-covered | Notes |
|---|---|---|---|
| Era (historical_horizon) | ... | ... | |
| Race / lineage | ... | ... | |
| Tag (canonical) | ... | ... | |

## Top gaps (ranked)

### Gap 1 — (era × race × tag combination)
- **Pages currently in this cell:** N (titles listed)
- **Expected to have content?** yes / no / uncertain (one-line reasoning)
- **Adjacent coverage:** how dense are neighbouring cells
- **User-flagged?** yes (in [[open-questions]] / [[worldbuilding-needs]]) / no
- **Suggested page topics (3):**
  1. <specific page title proposal>
  2. <specific page title proposal>
  3. <specific page title proposal>
- **Estimated effort:** small (single page) / medium (2–3 pages) / large (cluster)

### Gap 2 — ...
```

## Constraints

- **Read-only over the wiki.** Never modify canon. All output goes to `derived/negative-space/`.
- **Exclude `wiki/_sealed/`** unless explicitly invoked with the `sealed` mode (and even then, work carefully per the sealed-content rules in CLAUDE.md).
- **Respect canon_status.** Pages with `canon_status: rework-pending` count as "covered" but flag them as unstable.
- **Don't propose specific canon.** The skill identifies *that* a gap exists and suggests *topic names*, not canon claims. The user fills the gap.
- **Use existing canon for salience exclusions.** A cell of (primordial-era × halflings) is non-applicable; the scan should recognise this from existing canon, not invent reasoning to ignore it.

## Notes

This skill is for triage, not for writing. It produces a ranked list of where canon is thin so the user can pick what to develop next. The user remains the authority on which gaps to fill and what to fill them with. Multiple negative-space scans across months will form a history of *what was thin and got filled* — worth keeping in `derived/negative-space/` as a project record.
