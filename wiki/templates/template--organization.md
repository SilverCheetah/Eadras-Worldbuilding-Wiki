<%*
const title = await tp.system.prompt("Organization name (display title)");
const org_type = await tp.system.suggester(
  ["organization","religion"],
  ["organization","religion"],
  false,
  "Primary tag"
);
const horizon = await tp.system.suggester(
  ["all","primordial","progenitor-era","nerathi-era","high-firethorn","demon-war","dimming","modern-era"],
  ["all","primordial","progenitor-era","nerathi-era","high-firethorn","demon-war","dimming","modern-era"],
  false,
  "Historical horizon"
);
const access = await tp.system.suggester(
  ["common","general","scholarly","esoteric"],
  ["common","general","scholarly","esoteric"],
  false,
  "Knowledge access (use 'esoteric' for inner-circle orders, conspiracies)"
);
const status = await tp.system.suggester(
  ["established","proposed","pending","deprecated"],
  ["established","proposed","pending","deprecated"],
  false,
  "Canon status"
);
const tags_extra = await tp.system.prompt("Additional tags (comma-separated, e.g. 'eadras, conspiracy')", "eadras");
const tags_full = `${org_type}, ${tags_extra}`;
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

## Origins and founding



## Structure and hierarchy



## Doctrine, mission, or purpose



## Practices and disciplines



## Membership and recruitment



## Relations with outsiders



## Modern status

<!-- Present-era condition: active / dormant / dissolved / underground -->

---

<details>
<summary>Related pages</summary>

- 

</details>
