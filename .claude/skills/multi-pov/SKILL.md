---
name: multi-pov
description: Tell a single event or topic from multiple in-universe perspectives in parallel — typically three or four race / faction / tier viewpoints, each rendered in that perspective's voice. Spawns one subagent per perspective so the accounts develop independently. Outputs all perspectives plus a comparison analysis to derived/multi-pov/. Read-only over the wiki; never modifies canon. Fits the Tome-of-Baldaran conceit precisely — many traditions, one event, different truths.
---

# Multi-POV

A single shared event told by multiple in-universe voices in parallel. The parallel-subagent execution is essential: each perspective is developed independently of the others, by a separate subagent operating under that perspective's frame, so the accounts diverge naturally where they should diverge and converge on facts where the facts are facts.

This is the skill that most directly serves the Tome conceit. The Tome of Baldaran is a chronicle that collects perspectives; this skill produces what would land in such a chronicle. Output goes to `derived/multi-pov/` — these are *not* wiki pages, but they are the kind of source the wiki could later cite when establishing how a given event was variously remembered.

## When to invoke

- `/multi-pov <event>` — full multi-POV treatment of a named event. Default: 3–4 perspectives chosen from canonical races/factions with stake in the event.
- `/multi-pov <event> <perspective1>, <perspective2>, ...` — specify perspectives explicitly.
- `/multi-pov <event> tiers` — render across divinity tiers (mortal / Elder God / Dao / OC view) instead of races.
- `/multi-pov <event> contested` — pair each perspective with its in-universe critics; produces both *here is the X account* and *here is what the Y school says about the X account*.

## Procedure

1. **Identify the event.** Read the canonical page for the event (e.g., [[demon-war]], [[arathi-cataclysm]], [[battle-of-the-broken-conclaves]], [[sorcerer-crusade]]). Read adjacent pages that establish who-was-where-doing-what.
2. **Select perspectives.** Default selection logic:
   - Whoever was present at the event
   - Whoever was directly affected (descendants count, especially in a Mythos with long memory)
   - Whoever has a documented in-universe scholarly tradition about it
   - 3–4 perspectives unless the user specifies otherwise
3. **Spawn one subagent per perspective in parallel** (single tool-call message with multiple Agent invocations). Each subagent receives:
   - The event's canonical name and page pointer
   - The perspective they're rendering (race, faction, tradition, tier)
   - Pointer to that perspective's own canonical page so they can ground voice and worldview
   - Instruction to write the account in *that perspective's voice and frame* — what *they* remember, what *they* think happened, what they emphasise, what they elide, what they don't know
   - Word budget (typically 600–900 words per perspective)
   - The other perspectives' identities (so the subagent knows what NOT to claim — its perspective doesn't have access to the other accounts)
4. **Aggregate.** Combine all accounts into `derived/multi-pov/<event>-YYYY-MM-DD.md`. Include:
   - Each perspective in full
   - A short **comparison analysis** at the end: what all perspectives agree on (factual convergence — strongest canon), where perspectives diverge (interpretation), what each perspective emphasises that the others don't notice, and what each perspective gets *wrong* about the others (if the wiki's canon can establish such errors).
5. **Do not commit to canon.** The output is for the Tome (and the user) to see how the event reads across traditions. The user may later canonise specific phrasings or insights as wiki edits; the skill does not.

## Output structure

```markdown
# Multi-POV: <event>

**Event:** <name + canonical page>
**Date of telling:** YYYY-MM-DD
**Perspectives:** <Race A>, <Race B>, <Race C>, <Race D>
**Pages consulted:** [[a]], [[b]], [[c]]

---

## <Perspective A>'s account

[full account in A's voice]

---

## <Perspective B>'s account

[full account in B's voice]

---

## <Perspective C>'s account

[full account in C's voice]

---

## Comparison

### What all perspectives converge on
- ...

### Where perspectives diverge
- **A says ... ; B says ... ; C says ...**

### What each perspective emphasises
- A foregrounds: ...
- B foregrounds: ...
- C foregrounds: ...

### What each gets wrong about the others (if canon establishes errors)
- ...
```

## Constraints

- **One subagent per perspective, in parallel.** This is what makes the perspectives genuinely independent. Spawn them in a single message with multiple Agent calls.
- **Each subagent reads independently.** Don't pre-summarise the event for them; give pointers to canonical pages and let them form their account from those.
- **Each subagent must write in their perspective's voice.** Not a third-person neutral account labelled "the Orug perspective." A first-person-tradition voice — what the Orug *say* about the event, what the Orug *teach* their young about the event, what the Orug *remember* in their liturgy. Voice matters.
- **Each subagent must respect the perspective's epistemic limits.** What does this perspective know? What couldn't they know? What sources are they working from? An Orug account of the Final Wall written by an Orug after the Orug went extinct is impossible — instead, a Katharim account *of* the Orug at the Final Wall, in Katharim voice, is what fits.
- **The aggregator does not synthesise into one true account.** The point is multiple-perspective preservation, not consensus history. Convergence is interesting; divergence is the deliverable.
- **Read-only over the wiki.** All output to `derived/multi-pov/`.

## Notes

This is the skill that converts a single event-page into a tradition-rich source. Run it on any event the wiki already documents, and the output is *immediately useful* for prose generation, for adding cultural-perspective sections to existing pages, for filling in [[open-questions]] about *how X is remembered*, and for testing whether existing event canon survives being re-told from competing angles.

Pair with `/adversarial` for the strongest possible canon testing: `/multi-pov` shows how an event reads in tradition; `/adversarial` then probes whether the canon under those tellings is sound. A canonical event that survives both is in good shape.
