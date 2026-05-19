---
name: five-whys
description: Probe one load-bearing element of a worldbuilding canon page by asking "why does this exist in-world?" five times in succession, surfacing either a deep-canon foundation (god, primordial event, era trauma, omniversal law) or a worldbuilding gap that requires new canon. Use when the user wants to test the foundations of an established page, find what is load-bearing under a custom or institution, or discover negative space worth filling. Output is an analysis file written to `derived/five-whys/`; the wiki itself is not modified.
---

# Five Whys

A worldbuilding probe adapted from root-cause analysis. Surfaces the foundation under a piece of canon by asking "why does this exist?" five times, each level taking the previous answer as its new question.

## When to invoke

- `/five-whys <slug>` — probe the most load-bearing element of `wiki/<slug>.md`.
- `/five-whys <slug> <element>` — probe a specific element on that page.
- `/five-whys "<free-form claim>"` — probe a thematic claim if the user names one explicitly.

## Procedure

1. **Locate the page.** Find `wiki/<slug>.md`. If the slug doesn't resolve, search for the topic and confirm with the user before proceeding.
2. **Read the page in full,** then follow wikilinks to any page the claim *depends on* (parent races, era events, founding gods, related institutions). A five-whys on a downstream page usually bottoms out two or three pages upstream — read accordingly.
3. **Identify the probe element.** If the user named one, use it. Otherwise pick the most load-bearing claim — the one that, if removed, would make most of the rest of the page incoherent. Decorative or cosmetic claims are not load-bearing; the right probe element is structural.
4. **Run five whys.** For each level (1 → 5), answer "why does this exist in-world?" Each answer becomes the next level's question. Restate the answer in Tome-neutral register.
5. **Tag every answer's provenance:**
   - **`established`** — supported by existing canon; cite the page(s) and quote the key claim if useful.
   - **`implied`** — consistent with existing canon and reasonably inferred but not explicitly stated. Surface as a *promotion candidate* — a claim the user could elevate to canon by adding it to a wiki page.
   - **`GAP`** — answer requires new canon. Pose a clear question and offer 1–3 candidate answers the user could choose between. Never silently invent.
6. **Bottom out.** A successful five-whys ends at one of:
   - A **confirmed foundational canon** (divine actor, primordial event, omniversal law, era-defining trauma).
   - A **terminal GAP** — load-bearing canon is missing at the deepest level. This is a valuable finding, not a failure.
   - A **REJECT** — the probe element turns out not to be load-bearing (usually a sign it's decorative; suggest a better element).
7. **Write output** to `derived/five-whys/<slug>-YYYY-MM-DD.md` using the structure below. The wiki itself is not modified by this skill.

## Output structure

```markdown
# Five-Whys Probe: <Page Title>

**Probe element:** <the specific claim being interrogated, quoted if from canon>
**Date:** YYYY-MM-DD
**Run on:** [[<slug>]]
**Pages consulted:** [[a]], [[b]], [[c]]

---

## Why 1 — <one-line restatement of the question at this level>

**Answer (Tome-neutral):** <prose answer in the wiki's house voice>

**Provenance:** established / implied / GAP
**Cites:** [[page]] (quoted key claim if useful)

---

## Why 2 — ...
...

---

## Foundation reached

- **Type:** divine-actor / primordial-event / era-trauma / omniversal-law / terminal-GAP / REJECT
- **Summary of the chain:** <one paragraph: what this probe revealed about why the element exists>

## Gaps surfaced

<numbered list. For each gap: the question, 1–3 candidate answers with brief implications, and a suggested next action>

## Suggested next actions

<concrete: add a paragraph to page X, file question to open-questions.md, propose new page Y, etc.>
```

## Constraints

- **One element per invocation.** If the user asks for multiple probes, run them as separate invocations — depth beats breadth.
- **Never silently invent canon.** Gaps are valuable; surface them clearly. The user decides what becomes canon.
- **Output is derived, not canon.** It lives in `derived/five-whys/`, never under `wiki/`. If the user wants to promote a finding to canon, that's a separate edit they direct.
- **Tone:** restated canon goes in Tome-neutral register, matching pages like [[arathi-cataclysm]] or [[orugi]]. Analysis (provenance notes, gap analysis, suggested actions) can be analytical and meta.
- **Wikilink everywhere** so the output is navigable in Obsidian.

## Notes

This skill probes; it does not write canon. The output is a one-page analysis the user reviews to decide what (if anything) to commit. Future invocations on the same page (probing different elements) are encouraged — a strong wiki page should survive being probed from several angles.
