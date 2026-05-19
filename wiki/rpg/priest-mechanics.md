---
title: Priest Mechanics â€” Divine Casting & Favor
tags: [rpg, mechanics, magic, religion, eadras]
canon_status: [pending]
perspective: [ooc]
historical_horizon: [all]
knowledge_access: [meta]
---

# Priest Mechanics â€” Divine Casting & Favor

**Summary**: RPG-side mechanical treatment of the priestly casting tradition documented at [[priests]]. Daily channeling-capacity formula, the four Favor states with their numerical effects, no-memorization spell access, and the deity-set restoration timing rules. **Splat-book material**, not in-universe canon â€” the in-universe lore lives at [[priests]] and refers to these mechanics qualitatively without the explicit math.

**Sources**: User direction 2026-05-09 evening (in the same session that produced [[rpg/wizard-mechanics]]).

**Last updated**: 2026-05-09

---

## Daily channeling capacity

A priest's **daily divine capacity** â€” the total spell levels they can channel in a 24-hour cycle â€” is calculated as:

> **Wisdom score + Current Favor + (character level Ã— 2)**

Where *Current Favor* is a numerical adjustment from the [[#Favor states|Favor table]] below. Each spell channeled costs **its spell level** out of this pool.

A priest with WIS 16, Neutral Favor (+0), at character level 5 therefore has a daily capacity of:

`16 + 0 + (5 Ã— 2) = 16 + 0 + 10 = 26`

â€¦which they could spend, for example, on two 5th-level spells (cost 10), three 3rd-level spells (cost 9), three 2nd-level spells (cost 6), and a 1st-level spell (cost 1) for a total of exactly 26. They may cast spells in any combination as long as remaining capacity is sufficient; the choice is made *at the moment of casting*, not at preparation time.

### No memorization

Priests do **not** prepare a daily spell list the way [[rpg/wizard-mechanics|wizards]] do. They may **cast any spell they know** as long as they have sufficient remaining capacity for it.

What a priest *knows* â€” the spells available to them at all â€” is determined by their level, their god's portfolio, their personal training, and any specialty doctrine of their order. The list is generally larger than what a same-level wizard's prepared list could be, but it does not change day to day; the priest cannot suddenly *learn* a new spell without the appropriate training and standing.

The combination â€” large known list, no daily preparation, capacity-pool consumption â€” produces the canonical priest play feel: **flexible, responsive, situationally adaptive**, with the catch that a priest who runs through their pool on a poor early decision has nothing left for the crisis that arrives later.

## Favor states

Favor is **not a fixed score**. It fluctuates based on the priest's behavior, devotion, and service. The **Divine Bureaucracy** continuously monitors and adjusts it; for game-mechanical purposes, the GM tracks the priest's current Favor state and adjusts it according to in-game events.

| State | Numerical Adjustment | Frequency |
|---|---|---|
| **God's Favorite** | +6 (or higher; see below) | Extremely rare |
| **Positive Favor** | +2 | Earned by exceptional service |
| **Neutral Favor** | +0 | Default; most priests, most of the time |
| **Negative Favor** | âˆ’2 | Earned by violation, laxness, or acting against tenets |
| **Severely Fallen** | âˆ’4 (or worse) | Rare; serious betrayal pending restoration |
| **Cut Off** | n/a; cannot channel | A formal break; priest is effectively non-functional until restoration |

Default suggested step is **2 levels per state band**; GMs running stricter or looser tables can adjust the magnitude. The default produces a meaningful but not crushing variation: a priest in Positive Favor can reach for one or two spells they would otherwise miss, while a priest in Negative Favor loses one or two they would otherwise have had.

### God's Favorite (special)

The exalted state is rare enough that it is **GM-discretion-only** to award it. There is no XP-thresholded path to it, no "unlock at level X" trigger, and no in-fiction action a player character can take that *guarantees* it. The GM decides â€” typically as a long-arc payoff for years of in-fiction service â€” and once the state is granted, the priest receives:

- A **+6 Favor adjustment** to capacity (default; can be higher at GM discretion)
- **Access to one or more spells outside their ordinary tradition's list** (GM-chosen, narratively appropriate to the deity)
- **Occasional direct divine attention** â€” the player should expect the GM to use this as a story hook, not as a free magical resource. (The [[doctrine-of-unheld-hand|Doctrine of the Unheld Hand]] still applies; direct attention is rare even for Favorites.)
- The status **may be revoked** the same way ordinary Positive Favor can drop, with the additional weight that fallen Favorites are theologically marked. Some traditions require formal stripping of the status before its loss is institutionally complete.

## Favor changes during play

GMs adjust Favor in response to in-game events. The default cadence is conservative â€” Favor should not change on every encounter, and certainly not on every spell cast â€” but should respond to:

- **Major in-fiction service to the god's interests** (positive adjustment)
- **Major in-fiction violation of the god's tenets** (negative adjustment)
- **Sustained patterns of behavior** (positive or negative, evaluated over time rather than per-event)
- **Crisis decisions where the priest chose between divine duty and personal safety/comfort** (positive if they chose duty, negative if they chose to slack)

A useful rough heuristic: **Favor should change at most once or twice per major arc of play**, not session-to-session. The exception is the dramatic Favor reset â€” a priest who commits a major betrayal mid-session may drop one or two states immediately, and the GM should not delay that drop for procedural reasons.

### Restoration of lost Favor

A priest who has dropped to Negative Favor or worse can restore their standing through formal procedures the priesthood maintains. Typical mechanical requirements:

- **Confession to a senior priest** (a roleplay scene; no mechanical cost beyond the time)
- **Penance** appropriate to the violation (mechanical cost varies; can include time, expenditure, dangerous service)
- **Restitution** to those harmed (in-fiction action)
- **Supervised return to service** for a period before the GM restores Neutral Favor

GMs should make the restoration arc itself a meaningful piece of play, not a paperwork exercise. The point is that a fallen priest *recovers* through real action.

## Restoration of daily capacity

When the priest's daily capacity is **exhausted**, they cannot channel again until they have **rested and restored their connection to the divine through prayer**.

The restoration is **scheduled to the deity's preferred time**, not the priest's:

| Time | Frequency | Example deities |
|---|---|---|
| **Sunup** | Most common | [[ioa|Ioa]], [[vos|Vos]], [[raja|Raja]], [[nara|Nara]], most order-aligned gods |
| **Sundown** | Common | Reflective, hearth-evening, twilight-aligned gods (specific assignments open canon) |
| **Noon** | Rare | [[daj|Daj]] (war, strife, the sharpener of blades) |
| **Midnight** | Rare | [[nox|Nox]] (night, secrets, the loathsome); some traditions of [[shani|Shani]] |

The restoration is **not flexible** within a god's tradition. A priest of Vos who tries to restore at noon will simply not restore. The discipline of waking, sleeping, and praying around the deity's appointed hour is part of the priest's ongoing life and should be played at the table as such.

### What the prayer looks like mechanically

For game-mechanical purposes, the restoration prayer takes **1 hour of focused devotional activity** at the deity's appointed time. The priest cannot be doing other things during this hour (combat, complex magical work, distracted multitasking); the prayer is a real commitment of attention.

A priest who **misses** their restoration window â€” slept through it, was prevented by circumstance, or is in an environment where the time cannot be properly observed (deep underground with no sense of surface time, on another plane where local time differs from Eadras's, etc.) â€” does **not** restore that day's capacity. They must wait until the next occurrence of their deity's appointed hour. This produces real tactical pressure on long underground expeditions and on the rare planar excursions, and is a legitimate planning consideration for adventure design.

A priest whose **conduct during the day was inconsistent with their god's tenets** may find their restoration is **partial** â€” full capacity does not return, even though the prayer was performed correctly. This is a Favor adjustment in slow motion: the Bureaucracy is reducing capacity through under-grant rather than through a formal Favor-state change. GMs use this for nuanced consequences that don't merit a full Favor-state shift.

## Druidic Favor (druid-specific case)

Druids are unique among divine casters in that they may serve **up to three deities simultaneously** â€” [[qoxli|Qoxli]], [[sylph|Sylph]], and [[nox|Nox]]. Rather than maintaining three separate Favor tracks, druids have a single unified score called **Druidic Favor**.

Druidic Favor represents how well the druid is **maintaining the balance** between the gods they serve. It fluctuates based on their actions, decisions, and ability to honor the interests and domains of all chosen patrons without unduly favoring one over the others.

A druid's daily capacity is calculated identically to other priests, with *Druidic Favor* slotting into the *Current Favor* position of the formula:

> **Wisdom score + Druidic Favor + (character level Ã— 2)**

The druid-specific adjustment rules:

- When a druid's actions **promote natural balance and harmony** between their patrons' domains, their Druidic Favor **rises**.
- When a druid **neglects one deity's domain, shows clear favoritism, or disrupts the balance** between the three, their Druidic Favor **falls**.

This single unified Favor score reflects the fundamental nature of druidism: **the maintenance of balance between multiple divine forces.**

For single-patron druids, "balance" is trivial â€” there is only one set of interests to honor â€” and Druidic Favor behaves essentially identically to an ordinary priest's Favor with their one chosen god. For two-patron and tri-patron druids, the balance-maintenance burden is real and produces the structural reason multi-patron service is rarer than single-patron service: the same unified score must accommodate more interests being kept aligned at once.

The standard Favor states (Neutral / Positive / Negative / God's Favorite) and their numerical adjustments apply to Druidic Favor identically; the difference is purely in **what the GM is tracking the druid against** â€” single-deity standing for ordinary priests, balance-of-multiple-deities for multi-patron druids.

The in-universe treatment is at [[priests#Druids as priests]] and [[druids#Status as a sub-priesthood]].

## Combined mechanical reference

For quick GM reference at the table:

- **Daily capacity** (priests) = WIS + Favor adjustment + (level Ã— 2)
- **Daily capacity** (druids) = WIS + **Druidic Favor** + (level Ã— 2)
- **Each spell** costs its spell level
- **Spell access** = anything the priest/druid knows; no daily memorization
- **Favor states** = +6/+2/0/âˆ’2/âˆ’4/cut-off; default state is Neutral (0)
- **Druidic Favor** = single unified score; rises with balance, falls with neglect/favoritism/imbalance
- **Restoration** = 1 hour of prayer at deity's appointed time; missed window = no restoration that day
- **Conduct affects restoration** independent of Favor-state changes (slow-motion Favor adjustment)

## Open mechanical questions

- **Whether all priests of all gods restore at the same hour for a given deity.** The default rule is yes â€” priests of Vos all restore at sunup. Whether some unusual priests within an order can negotiate a different restoration time is open. The current treatment says no.
- **Whether the Favor adjustment is added to the formula or used as a multiplier.** The user direction reads as additive (`Wisdom + Current Favor + (level Ã— 2)`). Whether higher-tier tables prefer a multiplicative version (`(WIS + levelÃ—2) Ã— (1 + Favor/10)`) for a different feel is open.
- **Whether the Bureaucracy can grant a *temporary* one-shot Favor boost** (e.g., for a priest about to undertake a major mission for the god) without a sustained state change. Useful as a story mechanic; whether it is canonical is open.
- ~~**Whether multi-deity priests** ([[druids|tri-patron druids]] are the obvious case) track three separate Favor states or a single unified one.~~ **Resolved 2026-05-09**: a single unified ***Druidic Favor*** that fluctuates based on how well the druid maintains balance among the chosen gods' interests. See [[priests#Druids as priests]] for the in-universe treatment. Mechanically: one Favor adjustment in the daily-capacity formula, regardless of how many patrons the druid serves; the Favor is tracked by the GM as the druid's standing in keeping their patrons' interests in balance, with multi-patron druids facing a harder game (more interests to keep aligned at once on the same shared track).
- **Whether the restoration hour can be observed *flexibly* on planes where local time does not match Eadras's**. The current ruling is no â€” the priest is dependent on Eadras-local time, and an extended planar expedition is genuinely a problem for a priestly party. Whether some gods grant exceptions to this is open.

<details>
<summary>Related pages</summary>

- [[priests]]
- [[magic-in-eadras]]
- [[doctrine-of-unheld-hand]]
- [[gods-of-eadras]]
- [[rpg/wizard-mechanics]]
- [[rpg/README]]

</details>
