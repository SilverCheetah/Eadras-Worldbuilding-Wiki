---
title: Wizard Mechanics â€” Arcane Casting & Grimoires
tags: [rpg, splat-material, mechanics, magic, eadras]
canon_status: [pending]
perspective: [ooc]
historical_horizon: [all]
knowledge_access: [meta]
---

# Wizard Mechanics â€” Arcane Casting & Grimoires

**Summary**: RPG-side mechanical treatment of the arcane casting tradition documented at [[wizards]]. Mental-capacity formula, grimoire reading prep times, the *Personal Shorthand* feat, and the spell-ingredient framework. **Splat-book material**, not in-universe canon â€” the in-universe lore lives at [[wizards]] and refers to these mechanics qualitatively without the explicit math.

**Sources**: User direction 2026-05-09 evening (post the main 2026-05-09 ingest).

**Last updated**: 2026-05-09

---

## Mental capacity

A wizard's **maximum memorized spell levels** (the total volume of spells they can hold ready in mind at once) is calculated as:

> **Intelligence score + (Wisdom modifier Ã— 2) + (character level Ã— 2)**

Each spell takes up space in this pool **equal to its spell level**.

A wizard with INT 16, WIS 14 (+2 mod), at character level 5 therefore has memorized capacity of:

`16 + (2 Ã— 2) + (5 Ã— 2) = 16 + 4 + 10 = 30`

â€¦which they could fill, for example, with two 5th-level spells (cost 10), three 3rd-level spells (cost 9), four 2nd-level spells (cost 8), and three 1st-level spells (cost 3) for a total of exactly 30. Or any other distribution that fits.

Capacity is allocated at the wizard's daily preparation. Spells dropped during the day to free capacity for new memorization require **fresh preparation time** before the new memorization is ready.

## Grimoire casting

Any spell **not currently memorized** must be cast by **reading directly from a grimoire**. This requires **1 extra round of preparation per spell level**.

| Spell Level | Extra Prep | Total Casting Time |
|---|---|---|
| 1st | 1 round | spell's normal casting time + 1 round |
| 2nd | 2 rounds | spell's normal casting time + 2 rounds |
| 3rd | 3 rounds | spell's normal casting time + 3 rounds |
| ... | ... | ... |
| 9th | 9 rounds | spell's normal casting time + 9 rounds |

This applies whether the wizard is reading from their own grimoire (in personal shorthand) or from someone else's (in formal notation, or in deciphered shorthand). The base rule is the same; the *Personal Shorthand* feat below is what reduces the prep.

## Personal Shorthand (feat)

> **Personal Shorthand**
>
> *Prerequisite: Wizard or other arcane caster who maintains a personal grimoire.*
>
> You have developed your own unique system of magical notation. When casting a spell from **your own grimoire**, you only require **1 round of preparation, regardless of the spell's level.**

The feat applies only to the wizard's own grimoire. Casting from another wizard's grimoire â€” even if you have studied and partially deciphered their shorthand â€” uses the standard `1 round per spell level` rule, because the cognitive flow of reading-and-casting is broken by the constant translation step.

A wizard who maintains **multiple personal copies** of their grimoire (a recommended practice â€” see [[wizards#Grimoires as treasure]]) can use the feat on any of their own copies, provided each copy is up to date with the personal shorthand. Updating a backup copy to match a working copy is itself a multi-day task.

## Grimoires as treasure (rules summary)

- A wizard's grimoire is **a major treasure category** in adventure terms. Looting one is on par with a magic item of significant value, possibly higher for senior wizards' books.
- Working grimoires are **routinely trapped or warded.** GMs running grimoire-as-loot scenes should select an appropriate ward effect from the standard arcane-trap table or similar.
- **Personal shorthand decipherment** is a long-term task. Default ruling: deciphering another wizard's shorthand takes (the original wizard's level Ã— 1 week) of dedicated study, or longer if the original wizard was particularly cryptic. After successful decipherment, the deciphering wizard can read-and-cast from the grimoire at the standard `1 round per spell level` rate (the *Personal Shorthand* feat does **not** apply, because the shorthand is not the deciphering wizard's own).
- A captured grimoire that is **not** deciphered is still useful as a **scroll-like object** for the wizard who possesses it: spells visible in the grimoire can be cast at the standard rate, but spells encoded in shorthand are not accessible until the work is done. (GM ruling: typical loot grimoires are 30%â€“80% in personal shorthand; the rest is in formal notation that anyone can read.)
- A wizard who **kills another wizard and loots the grimoire** can, after decipherment, add the looted spells to their own grimoire. Doing so requires the looter to **transcribe the spell into their own personal shorthand**, which costs an additional `(spell level Ã— 1 day)` per spell, but afterward the spell is fully usable as if it had been the looter's all along.

## Spell ingredients

Spells classified as **ingredient-required** consume the listed ingredient when cast. Spells classified as **ingredient-optional** can be cast without, but get a measurable bonus when an appropriately-flavored ingredient is included.

The **ingredient flavor** is determined by the source of the mana the ingredient holds. Examples:

| Ingredient | Flavor | Spell Categories Enhanced |
|---|---|---|
| Hippogriff feather | Air / wind | Flight, gust, weather-touch, message-on-wind |
| Mana-rich water (sacred spring, conduit-near sea) | Water / life | Healing, water-shape, ocean magic, life-tide |
| [[mana-metals\|Mithril shaving]] | Pure-arcane | General-purpose enhancement, weak |
| [[mana-metals\|Orichalcum dust]] | Pure-arcane | General-purpose enhancement, strong |
| Dragon scale | Fire / sovereignty | Fire magic, dominion workings, draconic abjuration |
| Unicorn mane (freely given) | Healing / sanctity | Heavy healing, blessing, anti-Chaos warding |
| [[crystalmancy\|Crystalmancy lineage shaving]] | Lineage-specific | Workings aligned with that lineage |

The full ingredient table is open canon (see [[wizards#Open canon]]).

### Ingredient bonus (default ruling)

For ingredient-optional spells, including an appropriately-flavored ingredient grants:

- **+1 effective caster level** for purposes of the spell's effects (damage, duration, range, etc., as applicable), or
- **+1 to the spell's save DC**, or
- **An automatic minor flavor effect** appropriate to the ingredient (e.g., a wind spell with hippogriff-feather ingredient gains a brief beautiful gust visual; this is mostly cosmetic but can have minor flavor impact at GM discretion)

GMs should choose one of the three on a per-spell basis, or invent something thematically tighter. The general principle is that **ingredient-optional spells reward thoughtful ingredient choice without making it mandatory.**

For ingredient-required spells, the listed ingredient is a hard requirement. Without it, the spell cannot be cast.

## Open mechanical questions

- **Whether *Personal Shorthand* is a feat at all** in the final splat, or whether it should be a baseline ability of all wizards (with the spell-level prep penalty as the standard rule for foreign grimoires only). The current treatment makes it a feat to keep the penalty meaningful for wizards who haven't taken it; an alternative gives all wizards the benefit on their own grimoires by default and removes a feat slot from a heavy class.
- **Decipherment time formulas.** The `original-wizard-level Ã— 1 week` ruling above is a working default; it may be too fast or too slow at the table.
- **Spell preparation time on first daily memorization.** The standard SRD rule is 1 hour of preparation per day to set the wizard's memorized list; whether Eadras-specific tuning shortens or extends this, and whether the personal-shorthand benefit applies to that initial preparation, is open.
- **Ingredient-bonus stacking.** Whether two ingredients (e.g., hippogriff feather + mana-rich water for a wind-and-storm spell) stack, or whether only the most appropriate ingredient applies, is open.
- **Multi-source casting in mechanics.** Per [[wizards]], a wizard's spell list draws from Eldritch / quintessence, positive and negative energy, and alien mana, with the energy used depending on the spell. Whether this needs explicit mechanical handling at the spell-list level â€” different energy types for different spell *circles* or for spells with different magical *signatures* â€” or whether it remains pure flavor is open. Default: pure flavor; the mechanics treat all wizard spells uniformly regardless of underlying energy.

<details>
<summary>Related pages</summary>

- [[wizards]]
- [[magic-in-eadras]]
- [[mana-metals]]
- [[crystalmancy]]
- [[rpg/README]]

</details>
