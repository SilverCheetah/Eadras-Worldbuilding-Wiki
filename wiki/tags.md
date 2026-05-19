---
title: Tag Registry
tags: [meta, conventions]
canon_status: [established]
perspective: [reference]
historical_horizon: [all]
knowledge_access: [meta]
---

# Tag Registry

**Summary**: Canonical taxonomy of tags used in this wiki. Every page's `tags: []` frontmatter array should draw from this list.

**Sources**: User directive, 2026-04-30.

**Last updated**: 2026-04-30.

---

## Convention

Per `CLAUDE.md`, tags are **lowercase**, with **hyphens** for multi-word tags. The taxonomy below applies that convention to the user-supplied list (e.g., `Geographic Feature` â†’ `geographic-feature`).

Each page should carry **1â€“5** tags. Use the most specific applicable category tags (from the Required Taxonomy below) plus optional Modifier tags. If a page only has one or two good tags, that is fine â€” do not pad with filler.

### Obsidian + Dataview compatibility

This wiki is read in **Obsidian** with the **Dataview** plugin. That places hard rules on what is a valid tag:

- **No spaces, no capitals, no special characters.** Only letters, numbers, `-`, `_`, and `/` are valid in an Obsidian tag. Anything else is silently ignored. Our `lowercase-with-hyphens` convention satisfies this â€” verify before adding new tags.
- **YAML list form** (`tags: [foo, bar]`) is correctly parsed by both Obsidian's tag pane and Dataview queries (`FROM #foo`, `WHERE contains(tags, "foo")`).
- **Tags are declared in frontmatter only.** Don't sprinkle inline `#tag` refs in body prose â€” keep tag declarations in one place per page.
- **Forward-slash hierarchy is possible** (`races/progenitor`) â€” a Dataview query for `#races` would match `races/progenitor` too. Currently unused. Don't introduce hierarchy ad-hoc; if you think it'd help, propose it to the user first.
- **`aliases:` is a recognized Obsidian field** for alternate page names. Useful for canon-spelling drift (e.g., `aliases: [Vos, Voas]`) â€” currently unused but available.

---

## Required Taxonomy (user-mandated, 2026-04-30)

These are the canonical category tags. Use them on every applicable page going forward.

| Tag | Use for |
| --- | --- |
| `characters` | Named individuals (mortal, divine, or otherwise) |
| `races` | Sapient species and subspecies (Velrathi, Tarran, Beast-folk, etc.) |
| `deities` | Gods, Elder Gods, Elderborn, Ascended Mortals, Archons |
| `places` | General-purpose location tag â€” use when no more specific place tag fits |
| `events` | Discrete historical events |
| `myths` | Cosmological / origin / religious narratives |
| `country` | Sovereign nations and empires |
| `item` | Named objects, artifacts, relics, weapons |
| `organization` | Factions, orders, conclaves, conspiracies |
| `religion` | Faiths, churches, doctrines, cults |
| `settlement` | Cities, towns, villages, holds |
| `condition` | Diseases, curses, status effects, afflictions |
| `document` | In-world books, scrolls, texts |
| `culture` | Cultural groups, ethnic identities, lifeways |
| `language` | Spoken or written languages |
| `material` | Substances, alloys, magical materials (Starmetal, Aetherin crystal, etc.) |
| `natural-law` | Cosmic / metaphysical laws (Omniversal Laws, Axes of Creation, etc.) |
| `plot` | Active or unresolved narrative threads |
| `profession` | Occupations, callings, social roles |
| `title` | Honorifics, ranks, named offices |
| `spell` | Specific spells or named magical effects |
| `technology` | Crafts, devices, engineering |
| `tradition` | Customs, festivals, rites, practices |
| `conflict` | Wars, feuds, ongoing struggles |
| `vehicle` | Ships, mounts-as-vehicles, conveyances |
| `geographic-feature` | Mountains, rivers, forests, seas, regions |
| `building` | Specific named structures (palaces, temples, towers) |

---

## Modifier Tags (already in use across the wiki)

These narrow scope or mark special status. Combine freely with the Required Taxonomy tags above.

**Realm / setting modifiers**
- `eadras` â€” anchored in the Eadras Mythos
- `omniverse` â€” pertains to the wider Omniverse outside Eadras
- `cosmology` â€” concerns the structure of reality
- `plane` â€” a specific plane of existence

**Race / lineage modifiers**
- `progenitor` â€” one of the three progenitor races (Velrathi, Tarran, Elfen)
- `engineered-race` â€” created by a progenitor race
- `extinct` â€” race no longer exists in current canon
- `arathi` / `velrathi` / `tarran` / `elfen` / `rathar` â€” lineage anchors

**Deity modifiers**
- `elder-god` â€” one of the ten Elder Gods
- `elderborn` â€” child of an Elder God
- `ascended-mortal` â€” mortal who became divine
- `creator` â€” creator-tier deity
- `avatar` â€” avatar of a higher power

**Magic / metaphysics**
- `magic` â€” pertains to magical practice
- `weave` â€” pertains to the Weave specifically
- `sorcerer` â€” pertains to sorcery
- `doctrine` â€” religious or metaphysical doctrine
- `void` â€” pertains to Chaos / pre-ontological reality
- `demon` â€” demonic being or origin
- `entity` â€” non-categorized supernatural being

**History / narrative**
- `history` â€” historical content
- `war` â€” pertains to a war (use alongside `conflict` or `events`)
- `faction` â€” a political/social faction (use alongside `organization`)
- `order` â€” a formal order (use alongside `organization`)
- `conspiracy` â€” a conspiratorial faction

**Meta**
- `meta` â€” wiki-meta page (this page, conventions, etc.)
- `conventions` â€” documents wiki conventions

---

## Tagging Policy (set 2026-04-30)

1. **Forward-only by default** â€” Apply the Required Taxonomy on every new page.
2. **Correct as you go** â€” When editing an existing page for content reasons, also update its tags to the new taxonomy via the Merge Map below. No standalone re-tagging passes.
3. **Migration sweep trigger** â€” If, by **2026-05-30**, a substantial portion of the wiki has not been touched by edit-as-you-go re-tagging, perform a full migration sweep across all remaining pages.
4. **New category tags are allowed** â€” If a natural new category emerges that doesn't fit any existing tag, add it to the Required Taxonomy. It **must not** conflict with (duplicate or overlap) any existing tag. If a conflict arises, **ask the user** before adding.
5. **Ask on conflict** â€” Any time an old-tag â†’ new-tag merge is ambiguous, or a candidate new tag overlaps an existing one, stop and ask.

## Merge Map (old â†’ new)

When editing a page that carries an old tag, replace it with the new tag per this table.

| Old tag | Replace with | Notes |
| --- | --- | --- |
| `race` | `races` | Category swap |
| `deity` | `deities` | Category swap |
| `event` | `events` | Category swap |
| `myth` | `myths` | Category swap |
| `place` | `places` | Category swap (use a more specific tag like `settlement`, `country`, `geographic-feature`, or `building` if it fits) |
| `faction` | `organization` | Drop `faction` once `organization` is present |
| `order` | `organization` | `order` may be kept as a modifier if the page's nature as a formal order is salient |
| `war` | `conflict` | For finished wars also add `events`; `war` may be retained as modifier |

**Modifier tags (`eadras`, `omniverse`, `cosmology`, `plane`, `weave`, `magic`, `doctrine`, `progenitor`, `engineered-race`, `extinct`, `arathi`, `velrathi`, `tarran`, `elfen`, `rathar`, `elder-god`, `elderborn`, `ascended-mortal`, `creator`, `avatar`, `void`, `demon`, `entity`, `history`, `conspiracy`, `sorcerer`, `meta`, `conventions`)** are **not** merged â€” they continue to coexist with the Required Taxonomy.

## Migration Status

- **2026-04-30** â€” Required Taxonomy adopted. ~110 pre-existing pages still on old singular-form tags; migration occurs as pages are edited, with full sweep no later than **2026-05-30** if forward edits do not cover the wiki.

<details>
<summary>Related pages</summary>


- [[index]]
- [[log]]

</details>
