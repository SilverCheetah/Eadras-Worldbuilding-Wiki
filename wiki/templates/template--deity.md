<%*
const title = await tp.system.prompt("Deity name (display title)");
const deity_type = await tp.system.suggester(
  ["Elder God","Ascended Mortal","Elderborn","One of the Three","Other"],
  ["elder","ascended-mortal","elderborn","the-three","other"],
  false,
  "Deity type"
);
const horizon = await tp.system.suggester(
  ["all","primordial","progenitor-era","nerathi-era","high-firethorn","demon-war","dimming","modern-era"],
  ["all","primordial","progenitor-era","nerathi-era","high-firethorn","demon-war","dimming","modern-era"],
  false,
  "Historical horizon (use 'all' for Elder Gods; specific era for Ascended Mortals)"
);
const access = await tp.system.suggester(
  ["common","general","scholarly","esoteric"],
  ["common","general","scholarly","esoteric"],
  false,
  "Knowledge access"
);
const status = await tp.system.suggester(
  ["established","proposed","pending","deprecated"],
  ["established","proposed","pending","deprecated"],
  false,
  "Canon status"
);
const tags_extra = await tp.system.prompt("Additional tags after 'deities, " + deity_type + "' (comma-separated, optional)", "");
const tags_full = `deities, ${deity_type}${tags_extra ? ", " + tags_extra : ""}`;
-%>
---
title: <% title %>
tags: [<% tags_full %>]
canon_status: [<% status %>]
perspective: [tome-neutral]
historical_horizon: [<% horizon %>]
knowledge_access: [<% access %>]
---

# <% title %>

**Summary**: 

**Sources**: 

**Last updated**: <% tp.date.now("YYYY-MM-DD") %>

---

## Domain and portfolio



## Iconography and form



## Office and working practice

<!-- Solarion office location; cross-pantheon relationships; daily-work patterns -->

## The Icon

<!-- Prime-Material Icon: required for all gods; location typically hidden; do not reveal _sealed/-tier secrets -->

## The divine realm

<!-- Outer-plane realm; for Ascended Mortal Gods this was created at Apotheosis -->

## Worship and prayer-traffic



## Cross-cultural reception

<!-- Who venerates this deity outside their primary people? -->

---

<details>
<summary>Related pages</summary>

- [[gods-of-eadras]]
- [[icons]]
- [[solarion]]

</details>
