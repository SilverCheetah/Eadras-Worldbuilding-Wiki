---
title: Calendar Systems of Eadras
tags: [meta, conventions, calendar, reference]
canon_status: [established]
perspective: [reference]
historical_horizon: [all]
knowledge_access: [meta]
---

# Calendar Systems of Eadras

**Summary**: The canonical reference for all dating systems in use across the Eadras wiki. **AP (Absolute Physical time)** is the cosmologically-true master system, anchored at the Primordial Sacrifice and accessible only to the [[tome-of-baldaran|Tome of Baldaran]] and the [[gods-of-eadras|Gods]]. Mortal civilizations use **multiple, independent, approximate calendars** anchored to events meaningful to them — [[firethorn-empire|Firethorn]] regnal years, the [[anti-magic-crusade|First Rebrightening]], [[dragon-empire|Dragon Empire]] imperial cycles, the [[great-banishment|Velrathi Banishment-count]], [[katharim|Katharim]] death-ledger years, and [[bold|Bold]] conduit-cycles among others. **No mortal calendar is precise relative to AP**; conversions between mortal systems are themselves approximate, like real-world conversions between Julian, Gregorian, and Mayan Long Count. Event chronology lives at [[eadras-timeline]]; this page documents the systems themselves.

**Sources**: User direction 2026-05-15 (AP system canonization, multi-mortal-calendars framing); [[system-governance|System Governance]] Section 3.

**Last updated**: 2026-05-15

---

## The cosmological split

Calendar systems in Eadras divide into two categories separated by a categorical cosmological gap:

> [!important] Two kinds of calendar
> **AP (Absolute Physical time)** is cosmologically true. Only the Tome and the Gods originate AP dates.
>
> **Mortal calendars** are anchored to culturally-meaningful events. Multiple, coexistent, mutually-disagreeing, all approximate relative to AP.

This is not a flaw of mortal civilization. **Mortals cannot perceive Absolute Physical duration**, because they lack the cosmological reference frame from which AP is measurable. Every mortal calendar is a *best-effort approximation* anchored to a culturally-graspable event, accumulating drift across deep time. Civilizations that lasted millions of years (the [[arathi|Arathi]]) accumulated centuries of cumulative chronological drift in their own records. Civilizations that lasted only thousands (the Firethorn) drifted less but still drifted.

Conversions between mortal calendars are like Julian-to-Gregorian or Gregorian-to-Mayan-Long-Count conversions: *possible, but imperfect*. A Velrathi archivist's regnal date and a Dragon Empire scribe's cycle date for the same event will not align exactly when naively converted; the gap reflects accumulated mortal drift, not Tome error.

---

## AP — Absolute Physical time

**Anchor**: AP 0 = the moment of the [[primordial-duo|Primordial Sacrifice]], when Evye and Fryr completed their dissolution into creation.

**Direction**: Forward. AP increases monotonically. Events after the Sacrifice have positive AP values; nothing has a canonical "negative AP" value (the Mythos itself begins at the Sacrifice).

**Access**: The [[tome-of-baldaran|Tome of Baldaran]] and the [[gods-of-eadras|Elder Gods]] perceive duration from the absolute reference frame and can originate AP values directly. **No mortal can.** Mortals encountering an AP value are reading it from a Tome-curated source or receiving it through divine revelation; they cannot derive AP values from their own observation.

**Precision**: The Tome knows AP values to whatever precision it chooses to record. Most AP values in the wiki are recorded to the nearest year; some are coarser (the Primordial Sacrifice itself is recorded as AP 0 by definition, not by measurement). The Tome may choose not to surface precise AP values where mystery serves the narrative better.

**Storage**: AP dates live in event-page frontmatter as the `ap_date` field, hidden from default display by Obsidian's native property-panel folding. The Tome preserves the cosmological truth; mortal-facing date display uses whichever mortal calendar is appropriate to the page's perspective.

---

## Mortal calendar systems

Six major mortal calendars are currently canonical. All are approximate relative to AP; conversions between them are imperfect.

### Firethorn regnal years (FR)

**Anchor**: First year of the reign of the founding Firethorn Emperor.
**Direction**: Forward, by emperor and year-of-reign (e.g. "Thoramis Firethorn, Year 287").
**Resolution**: Year-level. Sub-year dating uses imperial month-names.
**Used by**: [[firethorn-empire|Firethorn-era]] historical records, [[velrathi|Velrathi]] pre-Banishment archives, [[tarans|Tarran]]-descended scholarly traditions.
**Status**: Historical — no longer used as a living calendar. Quoted in wiki pages covering the high-Firethorn era and the Demon War.
**Drift**: Several decades of cumulative drift across the empire's ~8,000-year lifespan, by Tome-internal estimate; the Firethorn imperial astronomical bureau periodically adjusted but did not eliminate the drift.

> [!note] Naming overlap
> "FR" is also the abbreviation for *First Rebrightening* (below). Context resolves the ambiguity, but where confusion is possible, use *Firethorn Regnal* and *First Rebrightening* in full.

### First Rebrightening (Fr.)

**Anchor**: End of the [[thousand-year-dimming|Thousand-Year Dimming]] — approximately the horizon at which the [[weave|Weave]]'s magical recovery became socially perceptible.
**Direction**: Forward.
**Resolution**: Year-level for modern records; coarser for the first centuries after the Dimming ended.
**Used by**: [[order-sharanel|Order Sharanel]], the [[tome-of-baldaran|Tome of Baldaran]]'s modern-era references, [[lirra|Lirran]] clergy, [[knights-of-lirra|Knights of Lirra]].
**Status**: Semi-formal. Not used by common folk; not adopted by all modern polities (the [[dragon-empire|Dragon Empire]] uses its own imperial-cycle system; [[bold|Bold]] uses its conduit-cycles).
**Drift**: The anchor itself is approximate — "the end of the Dimming" is a transition, not a single dated event. Modern Fr. dating is reliable for inter-Order Sharanel work and Lirran clergy correspondence but disagrees with other modern calendars by amounts up to a few decades on long-ago events.

### Dragon Empire imperial cycles

**Anchor**: Founding of the post-Demon-War dragon-mercenary coup that established the Empire.
**Direction**: Forward, by *imperial cycle* (a ~60-year administrative unit) and year-within-cycle.
**Resolution**: Cycle and year. Sub-year dating uses bureaucratic quarter-notations.
**Used by**: [[dragon-empire|Dragon Empire]] bureaucracy and all matters routed through it.
**Status**: Currently active. The dominant calendar across the eastern continents.
**Drift**: The 60-year-cycle structure is itself adjusted periodically by imperial astronomers; current cycle-length is closer to 59.7 years averaged across the Empire's history, with bureaucratic conversions to round years for record-keeping.

### Velrathi Banishment-count

**Anchor**: The first full year after the [[great-banishment|Great Banishment]] of the Velrathi to [[shadowdark-gaia|Shadowdark Gaia]].
**Direction**: Forward.
**Resolution**: Year-level. Sub-year dating uses Velrathi observance-calendar months tied to [[veyr-keth|Veyr'Keth]] crystalline-light cycles.
**Used by**: Exiled [[velrathi|Velrathi]] court records, [[velveth|Velveth]] cult observances, Velrathi diplomatic correspondence to surface entities.
**Status**: Currently active in the Velrathi exile community. Not used by surface mortals.
**Drift**: The Veyr'Keth crystalline-light cycles are not Eadran day-cycles; the Velrathi calendar has decoupled from Prime-Material seasonal time by roughly a century of cumulative drift since the Banishment, as Tome estimates show.

### Katharim death-ledger years

**Anchor**: Founding of the first [[katharim|Katharim]] death-ledger at [[kharathen|Kharathen]] — approximately the early post-Demon-War recovery horizon.
**Direction**: Forward.
**Resolution**: Year-level. The death-ledger records every named death and is the most institutionally-rigorous mortal calendar; cross-ledger reconciliation by senior death-priests preserves precision.
**Used by**: [[katharim|Katharim]] internal records, cross-cultural soul-routing correspondence with [[shali|Shali]] and [[shani|Shani]]'s offices.
**Status**: Currently active. Used continuously since founding.
**Drift**: The Katharim discipline holds drift to within roughly a decade across the system's ~10,000-year lifespan — the most accurate mortal calendar, by Tome estimate, though still imperfect.

### Bold conduit-cycles

**Anchor**: Activation of the first [[conduit-cities|conduit]] of [[bold|Bold]]'s Tower of Seven Spires.
**Direction**: Forward, by *conduit-cycle* (the period between successive [[grand-conjunction|Grand Conjunctions]], roughly 1,000 years).
**Resolution**: Cycle and year-within-cycle.
**Used by**: [[bold|Bold]] mercantile records, the Conduit Republic's legislative ledger, modern [[order-sharanel|Order Sharanel]] practical work.
**Status**: Currently active in Bold's institutional sphere; used by Bold-affiliated merchants and orders.
**Drift**: The Grand Conjunction anchor is astronomical and well-attested; drift within a cycle is minimal, but the system has only existed for a few cycles total — long-term drift behavior is unproven.

---

## Master conversion table

Major events across all canonical systems, side by side. **All mortal-system values are approximate** relative to AP; cells marked *N/A* indicate the system either predates or postdates the event and has no defined value for it. AP values shown as *[Tome value]* indicate the Tome holds a precise value that has not been published; the wiki preserves it as hidden frontmatter on the relevant event page.

```dataview
TABLE WITHOUT ID
  file.link AS "Event",
  ap_date AS "AP",
  bp_date AS "BP",
  firethorn_regnal AS "Firethorn Regnal",
  first_rebrightening AS "Fr.",
  dragon_empire_cycle AS "Dragon Cycle",
  velrathi_banishment AS "Velrathi B.C.",
  katharim_ledger AS "Katharim D.L.",
  bold_conduit_cycle AS "Bold C.C."
FROM "wiki"
WHERE contains(tags, "events") OR contains(tags, "history")
WHERE ap_date OR bp_date
SORT ap_date ASC
```

The query above pulls live from event-page frontmatter. As new event pages are added with appropriate calendar fields, they automatically join the table. Events lacking calendar data should appear in the gap-tracking query (below) so the curator can complete them.

### Coverage gap query

Events missing AP dates or appropriate mortal-system dates, with the **era-appropriate calendar** flagged for each. The *Needs* column shows which mortal-system field should be filled in based on the event's `historical_horizon`. ✓ means the field is present; **MISSING** means the field is required for this era and absent; — means the field is not applicable to this era.

```dataview
TABLE WITHOUT ID
  file.link AS "Event",
  historical_horizon AS "Era",
  choice(ap_date, "✓", "**MISSING**") AS "AP",
  choice(bp_date, "✓", "—") AS "BP",
  choice(
    contains(list("high-firethorn","demon-war","dimming"), historical_horizon[0]),
    choice(firethorn_regnal, "✓", "**needs Firethorn**"),
    "—"
  ) AS "Firethorn",
  choice(
    contains(list("dimming","modern-era"), historical_horizon[0]),
    choice(first_rebrightening, "✓", "**needs Fr.**"),
    "—"
  ) AS "Fr.",
  choice(
    historical_horizon[0] = "modern-era",
    choice(dragon_empire_cycle, "✓", "(if Dragon Empire)"),
    "—"
  ) AS "Dragon",
  choice(
    contains(list("demon-war","dimming","modern-era"), historical_horizon[0]),
    choice(velrathi_banishment, "✓", "(if post-Banishment Velrathi)"),
    "—"
  ) AS "Velrathi",
  choice(
    contains(list("dimming","modern-era"), historical_horizon[0]),
    choice(katharim_ledger, "✓", "(if Katharim-recorded)"),
    "—"
  ) AS "Katharim",
  choice(
    historical_horizon[0] = "modern-era",
    choice(bold_conduit_cycle, "✓", "(if Bold-recorded)"),
    "—"
  ) AS "Bold"
FROM "wiki"
WHERE contains(tags, "events") OR contains(tags, "history")
WHERE !ap_date OR (
  contains(list("high-firethorn","demon-war","dimming"), historical_horizon[0]) AND !firethorn_regnal
) OR (
  contains(list("dimming","modern-era"), historical_horizon[0]) AND !first_rebrightening
)
SORT historical_horizon ASC, file.name ASC
```

**Reading the query output:**

- The **Era** column shows the page's `historical_horizon` value, so you can sort by era and tackle backfill in chronological waves.
- **AP** flags every page missing the cosmologically-true date. This is always required.
- **BP** flags whether the page has a BP date; not strictly required but useful for cross-reference.
- **Firethorn / Fr. / Dragon / Velrathi / Katharim / Bold** columns show:
  - **✓** — field is populated, no action needed
  - **\*\*needs X\*\*** — the era requires this field but the page is missing it (bold + asterisks for emphasis)
  - **(if X)** — the field *may* be applicable depending on cultural context; populate if your sources include it
  - **—** — the era's outside this calendar's scope; no action

**Triage workflow:**

1. Sort the query output by Era (already the default sort).
2. Work top-down: fill in `ap_date: [unknown]` first for every page that's missing AP — that satisfies the hard requirement immediately, even before the Tome publishes the precise value.
3. Then for each event, add the era-required mortal-calendar field(s). The bold **MISSING** flags are the immediate worklist; the *(if X)* hints indicate optional cross-system entries that improve the conversion table's completeness.
4. After updating frontmatter, the Dataview cache refreshes automatically; re-open `calendar.md` in Reading View to see the gap-list shrink.

The triage logic encoded in the query reflects [[system-governance]] Section 3:

- **High-Firethorn / Demon-War / early-Dimming events** → `firethorn_regnal` is the appropriate mortal calendar
- **Modern-era events** → may require `first_rebrightening` (Order Sharanel / Lirran), `dragon_empire_cycle` (Dragon Empire affairs), `bold_conduit_cycle` (Bold mercantile), `velrathi_banishment` (Velrathi exile), or `katharim_ledger` (Katharim records), depending on the event's cultural context
- **Primordial / Progenitor-era / Nerathi-era events** → AP only; no mortal calendar reaches them

---

## Visual timeline

The Chronos Timeline visualization below renders the major-event spine across AP and the mortal systems. AP is the base axis; mortal-system tracks above show where each system's coverage begins and ends.

```chronos
EVENT
[AP-anchor] AP 0 ~ Primordial Sacrifice (Evye and Fryr complete dissolution into creation; AP begins)
[Cataclysm] AP [Tome value] ~ Arathi Cataclysm (Worldbreaker; the canonical 10,000,000 BP anchor)
[Chaos-I] ~6 mybp BP ~ First Chaos Crusade
[Eldravath] ~6 mybp BP ~ Eldravath supercontinent forms
[Silver-Plains] ~6 mybp BP ~ Silver Plains Flare (first unicorns)
[Chaos-II] ~2 mybp BP ~ Second Chaos Crusade
[Great-Exchange] ~19,000 BP ~ The Great Exchange
[Dao-rescue] ~50,000 BP ~ Dao rescues the Three
[Humanoids] 39,000 BP ~ Humanoid races created by the Three
[Firethorn-start] 18,000 BP ~ Firethorn Empire begins (FR Year 1)
[Firethorn-peak] 15,000 BP ~ Firethorn Empire peaks
[Demon-War] 10,000 BP ~ Demon War; Great Betrayal; Banishment
[Anti-Magic] 10,000–9,000 BP ~ Anti-Magic Crusade; Century of Sorrows
[Dimming-start] ~9,000 BP ~ Thousand-Year Dimming begins
[Dimming-end] ~8,000 BP ~ Thousand-Year Dimming ends; First Rebrightening begins (Fr. Year 1)
[Present] 0 BP ~ Present (modern era; next Grand Conjunction approaching)

PERIOD
[Arathi-era] AP [Tome value] - ~10,000,000 BP # Arathi/Nerathi hypercivilization
[Recovery] ~10,000,000 - ~8,000,000 BP # Post-Cataclysm recovery
[Eldravath-period] ~6,000,000 - ~5,000,000 BP # Eldravath supercontinent era
[Dragon-Unicorn-coexistence] ~5,000,000 - ~2,000,000 BP # Dragon-unicorn coexistence under the Compact
[Humanoid-era] 39,000 BP - present # Humanoid civilizations
[Firethorn-era] 18,000 - 10,000 BP # Firethorn Empire
[Modern-era] ~8,000 BP - present # First Rebrightening
```

The Chronos codeblock above will render in the Obsidian reading view when the Chronos Timeline plugin is active. AP values marked *[Tome value]* are placeholders pending canonical pinning of those magnitudes; the visualization renders the events even with placeholder AP values, treating them as ordinal positions on the timeline.

---

## How event pages should record dates

Every event page MUST include:

1. **`ap_date`** in frontmatter — the cosmologically-true AP value, as an integer. *Required*. Where the Tome's value has not been published, use `ap_date: [unknown]` until the value is canonized.
2. **`bp_date`** in frontmatter — the BP value. *Required* for any event with a known BP date from the [[eadras-timeline|timeline]].
3. **Any applicable mortal-calendar field** in frontmatter, when the event has a defined value in that system:
   - `firethorn_regnal` — Firethorn-era events only
   - `first_rebrightening` — modern-era events only
   - `dragon_empire_cycle` — post-Empire-founding events relevant to the Dragon Empire
   - `velrathi_banishment` — post-Banishment Velrathi events
   - `katharim_ledger` — events recorded in the Katharim death-ledger
   - `bold_conduit_cycle` — Bold-era events
4. **The page's primary display date** in body text uses the calendar most appropriate to the event's cultural context. A Firethorn-era event displays its Firethorn regnal year primary; a Bold mercantile event displays its conduit-cycle date primary. The other systems are visible through the calendar conversion table on this page.

Example frontmatter for an event page:

```yaml
---
title: The Great Betrayal
tags: [events, history, demon-war]
ap_date: [unknown]
bp_date: [10000]
firethorn_regnal: [Thoramis Year 340]
canon_status: [established]
perspective: [tome-neutral]
historical_horizon: [demon-war]
knowledge_access: [common]
---
```

The `ap_date: [unknown]` marker signals to the Tome's curator that this event's AP value is pending canonization; the page works fully without it, and the gap-tracking query will flag it for triage.

---

## Drift between mortal systems

When mortal calendars disagree on an event's date, the disagreement reflects accumulated drift from AP-truth across the different systems' lifespans. The Tome treats all mortal values as approximations and converts to AP internally; the wiki preserves the mortal values as they appear in mortal records, with the AP value as hidden ground truth.

Example: a Velrathi archive at Veyr'Keth dates an event to *Banishment-count Year 8,213*, while a Katharim death-ledger at Kharathen dates the same event to *Death-Ledger Year 8,201*. A naive conversion would suggest a 12-year discrepancy. The Tome records the AP value as the cosmologically-true measurement; the 12-year discrepancy is mortal drift, not Tome error.

The wiki preserves both mortal values where both are documented. The `ap_date` field is the cosmological referent.

---

## Open questions

- The exact AP magnitude of the Primordial Sacrifice → Cataclysm interval is currently *Tome-internal* and has not been published. Once canonized, all pre-Cataclysm AP values can be normalized.
- Several modern polities (the Azure Basin's various poleis, the Beast-Folk Circles, the Amunorian diaspora) have not yet had their own calendar systems canonized. These should be added to this page as they develop.
- The Arathi/Nerathi had their own pre-Cataclysm astronomical calendar; if recovered material adds canon, this page should incorporate it as a seventh (extinct) mortal system.

---

<details>
<summary>Related pages</summary>

- [[eadras-timeline]]
- [[system-governance]]
- [[tome-of-baldaran]]
- [[primordial-duo]]
- [[arathi-cataclysm]]
- [[demon-war]]
- [[anti-magic-crusade]]
- [[grand-conjunction]]
- [[firethorn-empire]]
- [[dragon-empire]]
- [[bold]]
- [[velrathi]]
- [[katharim]]

</details>
