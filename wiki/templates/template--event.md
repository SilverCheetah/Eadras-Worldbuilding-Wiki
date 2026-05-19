<%*
const title = await tp.system.prompt("Event title (e.g. 'The Great Betrayal')");
const tags_secondary = await tp.system.prompt("Additional tags after 'events' (comma-separated, e.g. 'history, demon-war')");
const horizon = await tp.system.suggester(
  ["all","primordial","progenitor-era","nerathi-era","high-firethorn","demon-war","dimming","modern-era"],
  ["all","primordial","progenitor-era","nerathi-era","high-firethorn","demon-war","dimming","modern-era"],
  false,
  "Historical horizon"
);
const access = await tp.system.suggester(
  ["common","general","scholarly","esoteric","meta","sealed"],
  ["common","general","scholarly","esoteric","meta","sealed"],
  false,
  "Knowledge access"
);
const status = await tp.system.suggester(
  ["established","proposed","pending","deprecated"],
  ["established","proposed","pending","deprecated"],
  false,
  "Canon status"
);
const perspective = await tp.system.suggester(
  ["tome-neutral","tome-recovered","tome-sealed","reference","ooc"],
  ["tome-neutral","tome-recovered","tome-sealed","reference","ooc"],
  false,
  "Perspective"
);
const ap_date = await tp.system.prompt("AP date (integer; type 'unknown' if not yet canonized)", "unknown");
const bp_date = await tp.system.prompt("BP date (integer; leave blank to omit)");
const tags_full = `events, ${tags_secondary}`;
-%>
---
title: <% title %>
tags: [<% tags_full %>]
ap_date: [<% ap_date %>]
<% bp_date ? `bp_date: [${bp_date}]` : '' %>
canon_status: [<% status %>]
perspective: [<% perspective %>]
historical_horizon: [<% horizon %>]
knowledge_access: [<% access %>]
---

# <% title %>

**Summary**: 

**Sources**: 

**Last updated**: <% tp.date.now("YYYY-MM-DD") %>

---

## 

<!-- Body content. Use the calendar most appropriate to the event's cultural context as the primary display date; cite the BP equivalent parenthetically. -->

<!-- 
Optional calendar-specific fields to add to frontmatter as applicable:
  firethorn_regnal: [Emperor-Name Year N]
  first_rebrightening: [Fr. N]
  dragon_empire_cycle: [Cycle N Year M]
  velrathi_banishment: [Banishment Year N]
  katharim_ledger: [D.L. N]
  bold_conduit_cycle: [C.C. N Year M]
-->

---

<details>
<summary>Related pages</summary>

- 

</details>
