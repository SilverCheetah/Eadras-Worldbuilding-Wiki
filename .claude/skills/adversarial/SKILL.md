---
name: adversarial
description: Stress-test a piece of canon by spawning two parallel subagents — a Skeptic (finds contradictions, weak assumptions, over-claims, missing evidence) and an Advocate (defends structural strengths, articulates design rationale, finds supporting evidence, identifies load-bearing claims). Outputs both reports plus an aggregator analysis to derived/adversarial/. Read-only over wiki; never modifies canon. Use before committing significant new canon, when auditing canon that has gone through major revision, or to find blind spots in established material.
---

# Adversarial Probe

A canon stress-test executed by two subagents working in parallel under different mandates. The Skeptic tries to break the canon; the Advocate tries to hold it up. The aggregator surfaces where they converge (high-confidence canon), where they diverge (open questions the user must resolve), and what specific changes would address the Skeptic's findings without losing what the Advocate is defending.

Like `/five-whys`, this skill probes — it does not write canon. All output goes to `derived/adversarial/`.

## When to invoke

- `/adversarial <slug>` — probe an entire wiki page.
- `/adversarial <slug>#<section>` — probe a specific section (e.g., `/adversarial gods-of-eadras#Position-in-the-multiverse`).
- `/adversarial canon "<claim>"` — probe a hypothetical / draft claim *before* committing it to a page. Useful for testing canon before write.
- `/adversarial recent` — probe whatever was most recently committed (per `log.md`'s last entry).

## Procedure

1. **Locate the probe target.** Read the named page(s) or extract the claim. If probing a section, read the full page for context and focus the analysis on the named section.
2. **Identify adjacent canon.** Wikilinks from the target page tell you what else is relevant. The probe should consider what the target relies on (upstream) and what relies on it (downstream).
3. **Spawn two subagents in parallel**, each with focused mandates:

   **Skeptic** — Read the target and adjacent canon. Produce a structured report covering:
   - **Contradictions** — places where the target conflicts with adjacent canon. Cite specific pages/lines.
   - **Over-claims** — places where the target asserts more than the supporting canon establishes. The threshold: if a mortal scholar within Eadras could not verify the claim from existing canon, flag it.
   - **Weak assumptions** — places where the target depends on a premise that isn't established and isn't obviously true.
   - **Missing implications** — places where the target's claim, taken seriously, implies consequences elsewhere that the canon does not yet handle.
   - **Schema or convention violations** — frontmatter issues, tag misuse, perspective mismatches, etc.
   - **Where the canon would break under pressure** — if the canon is challenged (by a contradicting source, a counterexample, a competing in-universe school), which parts are vulnerable.

   **Advocate** — Read the same target and adjacent canon. Produce a structured report covering:
   - **Load-bearing claims** — what does the target establish that other canon depends on. These are the parts most worth keeping.
   - **Structural strengths** — where the target coheres elegantly with adjacent canon, where its internal logic is tight, where its design serves narrative/thematic ends.
   - **Supporting evidence** — specific other pages whose content supports the target's claims.
   - **Why the design choices are good** — articulate the intent, the worldbuilding payoff, the thematic resonance. The Advocate's job is to make the *case* for the canon, not to be neutral.
   - **What the canon contributes** — what would be lost (in setting depth, in story potential, in worldbuilding leverage) if this canon were removed or weakened.

4. **Aggregate.** Combine both reports into a single artifact at `derived/adversarial/<slug-or-topic>-YYYY-MM-DD.md`. The aggregator should produce:
   - **Both reports in full**, side by side or stacked.
   - **Areas of agreement** — claims that both agents endorse (Skeptic finds no issue *and* Advocate identifies as load-bearing). These are high-confidence canon.
   - **Areas of disagreement** — claims the Skeptic challenges that the Advocate defends. These are the user-decision points. Each disagreement should be stated clearly.
   - **Suggested actions** — for each Skeptic finding, what minimal change would address it; for each Advocate-identified strength, what would protect it. Present as options, not directives.

5. **Do not write to the wiki.** The aggregator output goes only to `derived/adversarial/`. The user reads, decides, and (if anything is to be changed) edits the wiki themselves or asks for follow-up edits.

## Output structure

```markdown
# Adversarial Probe: <topic>

**Probe target:** <slug, section, or quoted claim>
**Date:** YYYY-MM-DD
**Pages consulted:** [[a]], [[b]], [[c]]

---

## Skeptic's findings

### Contradictions
- ...

### Over-claims
- ...

### Weak assumptions
- ...

### Missing implications
- ...

### Schema / convention issues
- ...

### Pressure points
- ...

---

## Advocate's findings

### Load-bearing claims
- ...

### Structural strengths
- ...

### Supporting evidence
- ...

### Design rationale
- ...

### What would be lost
- ...

---

## Areas of agreement (high confidence)

- ...

## Areas of disagreement (user judgment needed)

For each disagreement:
- **Claim:** ...
- **Skeptic says:** ...
- **Advocate says:** ...
- **Possible resolutions:** ...

## Suggested actions

(Options, not directives. The user decides.)

- For Skeptic finding X: minimal change Y would address it.
- For Advocate-identified strength Z: protecting it would mean ...
```

## Constraints

- **Two subagents, in parallel.** This is the canonical use of parallel subagents in the workflow. Spawn them in a single tool call so they run concurrently.
- **Each subagent reads independently.** Don't pre-summarise the canon for them; let them form their own view from the source pages. (Each can be given pointer guidance to specific pages, but the analysis should be theirs.)
- **Skeptic must cite specific evidence.** Vague "this feels weak" findings are not useful. Each Skeptic finding should point at a specific page, line, or claim.
- **Advocate must defend on canon-internal grounds**, not just author-side preference. "I like it" doesn't count; "it serves the Tome conceit by X and supports adjacent canon Y" does.
- **Read-only over the wiki.** All output to `derived/adversarial/`.
- **The aggregator does not take sides.** Surfacing the disagreement clearly is more valuable than resolving it. The user resolves.

## Notes

This skill is at its best when run *before* canon is committed. Running it after the fact (on already-established canon) is useful for audit, but the asymmetric value is catching issues before they need a retcon. As a workflow: draft canon → run `/adversarial` → resolve findings → commit.

The Skeptic/Advocate framing is deliberate — not Devil's Advocate / Defender, but two analysts each with a partisan mandate. Both are doing their job correctly when one finds problems and the other defends. Agreement between them is the strongest possible signal that a piece of canon is sound; disagreement is the signal that user judgment is required.
