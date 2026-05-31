---
title: The Eadras World Map
tags: [geographic-feature, eadras, natural-law]
canon_status: [established]
perspective: [tome-neutral]
historical_horizon: [all]
knowledge_access: [common]
---

# The Eadras World Map

**Summary**: The reference frame for the modern surface of Eadras — the equirectangular dragon-memory map, its coordinate system anchored to the Worldbreaker Scar, the planetary climate model that governs its latitude bands and ocean gyres, and the tectonic-assembly history that produced the modern arrangement of continents (the eastern continent [[halaran|Halaran]], the two western landmasses, and the great oceans between). Eadras is a spinning globe with standard within-system astrophysics *and* mythic infrastructure simultaneously true — physics sets the baseline grid; the [[mythos|Mythos]] adds named anomalies on top of it.

**Sources**: EADRAS WORLDBUILDING — MAP SESSION.txt (map-building working session, 2026-05-31); cross-references [[eadras-tectonic-history]], [[seven-conduits]], [[night-sky-cosmology]].

**Last updated**: 2026-05-31.

---

## The map frame and coordinate system

The modern **dragon-memory world map** is an **equirectangular (plate carrée) projection**, 2048 px wide by 1024 px tall — a true 2:1 ratio, so it maps cleanly onto a globe.

- **Latitude**: top edge = 90°N, bottom edge = 90°S, equator at the vertical centre. Lines are drawn at 30° intervals. Scale: **1° = 5.689 px** on both axes (30° = 170.67 px).
- **Longitude — the Prime Meridian runs through the [[arathyn|Worldbreaker Scar]]** (the central volcanic island, Arathyn). The entire coordinate system is anchored to the impact wound: **every position on Eadras is measured from the Cataclysm.** The 180° anti-meridian falls at the map's wrap edges.
- The Scar sits at **~668, 378** — roughly **23.6°N**, on the tropic line, consistent with the established placement of Arathyn north of the equator in the tropics.

### Reference latitude rows

| Latitude | y-pixel |
|---|---|
| 90°N | 0 |
| 60°N | 171 |
| 30°N | 341 |
| Equator | 512 |
| 30°S | 683 |
| 60°S | 853 |
| 90°S | 1024 |

### The antipode rule

For any point **(x, y)**, its antipode is **(x + 1024, wrapped to ≤ 2048; and 1024 − y)** — shift half the map width horizontally (wrapping at the edge) and mirror across the equator. This is the working rule behind every [[seven-conduits|conduit]] Far-Kin pairing and the antipodal relationships catalogued [below](#Marked-coordinates-and-antipodes).

### Projection caveat

On an equirectangular projection, **high-latitude features are horizontally exaggerated** and equatorial features are truest to scale. The far north — e.g. [[ratharil|Ratharil's]] reach across northern [[halaran|Halaran]] — is smaller in true area than its map width suggests. Scholars and dragons who reckon distance from the map correct for this; naïve readers overestimate the polar lands.

---

## The planetary climate model

Eadras has **standard within-system astrophysics and mythic infrastructure simultaneously true** (dual-truth). The world is a spinning globe — not a bounded plane — with an Earth-like axial tilt (~23°), producing four seasons and Earth-analogue latitude bands.

> [!note] Geocentric astronomy, heliocentric climate
> Consistent with [[night-sky-cosmology|night-sky canon]], the sun revolves around Eadras, as do the other planets, with the sun farthest out — a functioning geocentric (Ptolemaic-style) system. This does **not** change climate: temperature banding comes from sunlight geometry on a tilted spinning sphere, which a geocentric model reproduces identically. In-world astronomers can hold an accurate, predictive geocentric astronomy while the mythic layer is also literally true.

### Climate bands by latitude

| Band | Latitude | Character |
|---|---|---|
| **Tropical** | 0–30° (either side) | Hot/wet near the equator, drier toward 30°. |
| **Temperate** | 30–60° | The broad habitable belt — warm-temperate at 30°, cool at 60°. |
| **Subpolar → polar** | 60–90° | Boreal/taiga at 60°, tundra and permanent ice toward 90°. |

Because Eadras is **~70% ocean**, the whole world runs milder and wetter than Earth — fewer true deserts, more maritime temperate forest. The **~30° latitudes are the natural dry/desert latitudes**, where any sizeable continental interior can go arid.

### Ocean currents and gyres

Coriolis on the spinning globe sets the rotation of the great gyres:

- **Northern-hemisphere gyres rotate clockwise.**
- **Southern-hemisphere gyres rotate counterclockwise.**

Currents redistribute heat: a gyre's poleward limb warms a coast; its equatorward limb cools one. This is the mechanism behind [[halaran|Halaran's]] warm west coast and cool southeast tail.

### Mythic anomalies override the baseline locally

Physics sets the baseline grid; the Mythos adds named anomalies. Mythic climate anomalies are permitted to locally override the astrophysical baseline — the [[arathyn|Worldbreaker Scar]] as a heat anomaly, ley/magitek warmth, moon-tidal effects, and the like. The grid is the default; anomalies are the exceptions, and each is named.

---

## Tectonic assembly of the modern arrangement

The modern map is the product of a second great continental assembly and its rifting. (For the deep pre-supercontinent lineage and the [[eldravath|Eldravath]] supercontinent, see [[eadras-tectonic-history]].)

Drift sequence to the modern arrangement:

1. All continents **assembled into a second megacontinent ~4 million years ago.**
2. It then **rifted apart around the [[arathyn|Worldbreaker Scar]]** — the rift centre.
3. Two fragments drifted poleward and **crossed the poles**: one northern fragment over the north pole, one southern fragment under the south pole.
4. Those two pole-crossing fragments **merged on the far side of the world**, fusing into the single large eastern continent — **[[halaran|Halaran]]**.
5. The remainder drifted **west** and split into the **two western landmasses** (the northwestern continent of the [[dragon-empire|Dragon Empire]] and [[verdant-scar|Verdant Scar]]; and the southwestern **Dark Continent** behind its ward — almost certainly the established prison-continent **[[varkhul|Varkhul]]** inside the [[continental-ward|Continental Ward]]; see the [note below](#Marked-coordinates-and-antipodes)).

### The geology records the journey

The pole-crossing fragments **glaciated heavily during the crossing**. The northern third of Halaran carries **relict glacial terrain** — fjords, U-valleys, glacial lakes, scoured rock — even where it now sits at milder latitudes. Where the northern and southern fragments welded together, the crust crumpled up into an **east–west volcanic suture range** across Halaran's middle (a Himalaya-analogue, but mantle-active and volcanic). The geology is readable by scholars and dragons as direct evidence of the drift history.

> [!warning] Naming reconciliation pending (FLAG ONLY)
> The historical-reconstruction maps from this session use fragment names — **Valdaran, Elyndar, Korvath, Thalindor** — that differ from the deep tectonic-lineage names already in canon (**[[avalon|Avalon]], [[damedes|Damedes]], [[culethor|Culethor]], [[eldravath|Eldravath]]**; see [[eadras-tectonic-history]]). These are **two naming systems for the same drift history** and require a dedicated reconciliation pass. They are deliberately **not merged here.** See [[open-questions]].

---

## Marked coordinates and antipodes

Positions fixed on the dragon-memory map this session. Antipodes are computed by the [antipode rule](#The-antipode-rule).

| Feature | Coordinate (x, y) | Approx. latitude | Antipode | Antipode lands on |
|---|---|---|---|---|
| **[[arathyn|Worldbreaker Scar]]** (Arathyn) | 668, 378 | ~23.6°N | 1692, 646 | — (Prime-Meridian anchor) |
| **[[ratharil|Ratharil]]** (Rhtrakhadara) | 1332, 190 | ~58°N | 308, 834 | **Dark Continent coast** ([[varkhul|Varkhul]]), ~58°S (cold, near southern ice) |
| **[[verdant-scar|Verdant Scar]]** (Arath-Veyr) | 151, 385 | ~22°N | 1175, 639 | **Halaran** — a ruined [[anti-magic-crusade|Crusade]] [[order-sharanel|Tower of Lirra]] by the forest-river |
| **[[bold|Bold]]** | 1692, 450 | — | 668, 574 | open ocean, south of the equator (no Bold↔Scar pairing) |
| Unnamed conduit city | 345, 416 | — | 1369, 608 | **Halaran** |

Notes on the load-bearing antipodes:

- **Ratharil ↔ the Dark Continent ([[varkhul|Varkhul]]).** The point exactly opposite the City of Dragons is a specific cold coastal point on the sealed southwestern continent — *"the shore opposite Rhtrakhadara."* The map session's unnamed "Dark Continent behind the unbreachable ward" matches the established **prison-continent Varkhul** inside the **[[continental-ward|Continental Ward]]** precisely (southwestern, sealed, Exile Lands); the identification is treated as canon here but is folded into the [tectonic-naming reconciliation](#Tectonic-assembly-of-the-modern-arrangement) for the deep lineage. The dragons placed their one neutral city as far from the forbidden land as the planet allows. Whether this antipode marks a ward-meets-sea point, an unreachable pilgrimage coordinate, or a weak point in the seal is open canon.
- **Verdant Scar ↔ a ruined Crusade Tower on Halaran.** This is consistent with established [[verdant-scar|Verdant Scar]] canon: the Scar's pre-Cataclysm antipode was [[altea|Altea]], but the surface drifted, so the *modern* antipode is one of the six Crusade-ruined [[order-sharanel|Towers of Lirra]] — now fixed at (1175, 639) in the Halaran heartland.
- **Bold has no Scar pairing.** Bold's antipode is open ocean at a different latitude from the Scar; the earlier speculative Bold↔Scar pairing is **corrected and dropped.** Bold's conduit Far-Kin remains open canon.

---

## Related pages

<details>
<summary>Related pages</summary>

- [[halaran]]
- [[eadras-tectonic-history]]
- [[arathyn]]
- [[seven-conduits]]
- [[conduit-cities]]
- [[night-sky-cosmology]]
- [[ratharil]]
- [[verdant-scar]]
- [[bold]]
- [[dragon-empire]]
- [[open-questions]]

</details>
