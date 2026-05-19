<%*
const title = await tp.system.prompt("Place name (display title)");
const place_type = await tp.system.suggester(
  ["geographic-feature","settlement","region","country","plane"],
  ["geographic-feature","settlement","region","country","plane"],
  false,
  "Place type (first tag)"
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
  "Knowledge access"
);
const status = await tp.system.suggester(
  ["established","proposed","pending","deprecated"],
  ["established","proposed","pending","deprecated"],
  false,
  "Canon status"
);
const tags_extra = await tp.system.prompt("Additional tags (comma-separated, e.g. 'eadras, arathi, extinct')", "eadras");
const tags_full = `${place_type}, ${tags_extra}`;
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

## Location and geography



## History



## Inhabitants and culture



## Notable features

<!-- Landmarks, structures, named locales within the larger place -->

## Modern status

<!-- Present-era condition: thriving / fallen / ruined / mythical / contested -->

---

<details>
<summary>Related pages</summary>

- 

</details>
