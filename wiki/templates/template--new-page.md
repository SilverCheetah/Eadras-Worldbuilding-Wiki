<%*
const title = await tp.system.prompt("Page title");
const primary_tag = await tp.system.suggester(
  [
    "races (people)",
    "deities (gods)",
    "creatures (non-sapient)",
    "entity (cosmic-level being)",
    "cosmology",
    "natural-law",
    "plane",
    "geographic-feature",
    "settlement",
    "region",
    "country",
    "culture",
    "tradition",
    "religion",
    "magic",
    "alchemy",
    "history",
    "events",
    "document",
    "organization",
    "meta (reference)",
    "ooc (out-of-character)"
  ],
  ["races","deities","creatures","entity","cosmology","natural-law","plane","geographic-feature","settlement","region","country","culture","tradition","religion","magic","alchemy","history","events","document","organization","meta","ooc"],
  false,
  "Primary category (first tag)"
);
const tags_extra = await tp.system.prompt("Additional tags (comma-separated, optional)", "eadras");
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
const perspective = await tp.system.suggester(
  ["tome-neutral","tome-recovered","tome-sealed","reference","ooc"],
  ["tome-neutral","tome-recovered","tome-sealed","reference","ooc"],
  false,
  "Perspective"
);
const status = await tp.system.suggester(
  ["established","proposed","pending","deprecated"],
  ["established","proposed","pending","deprecated"],
  false,
  "Canon status"
);
const tags_full = `${primary_tag}${tags_extra ? ", " + tags_extra : ""}`;
-%>
---
title: <% title %>
tags: [<% tags_full %>]
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

<!-- 
If this is an event/history page, add calendar fields to frontmatter:
  ap_date: [unknown]
  bp_date: [N]
  (plus any applicable: firethorn_regnal, first_rebrightening, dragon_empire_cycle, velrathi_banishment, katharim_ledger, bold_conduit_cycle)
See [[system-governance]] Section 3 and [[calendar]].
-->

---

<details>
<summary>Related pages</summary>

- 

</details>
