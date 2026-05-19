<%*
const title = await tp.system.prompt("Race name (display title)");
const race_type = await tp.system.suggester(
  ["Progenitor","Engineered","Descendant","Engineered-and-extinct","Aberrant"],
  ["progenitor","engineered-race","descendant","engineered-and-extinct","aberrant"],
  false,
  "Race type"
);
const horizon = await tp.system.suggester(
  ["all","primordial","progenitor-era","nerathi-era","high-firethorn","demon-war","dimming","modern-era"],
  ["all","primordial","progenitor-era","nerathi-era","high-firethorn","demon-war","dimming","modern-era"],
  false,
  "Historical horizon"
);
const access = await tp.system.suggester(
  ["common","general","scholarly"],
  ["common","general","scholarly"],
  false,
  "Knowledge access"
);
const status = await tp.system.suggester(
  ["established","proposed","pending","deprecated"],
  ["established","proposed","pending","deprecated"],
  false,
  "Canon status"
);
const tags_extra = await tp.system.prompt("Additional tags (comma-separated, e.g. 'eadras, modern-era', optional)", "eadras");
const tags_full = `races, ${race_type}, ${tags_extra}`;
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

## Origins and creation

<!-- Created directly by one of the Three? Engineered by another race? Natural? Layered creation history? -->

## Biology and appearance



## Society and social structure



## Spirituality and religion

<!-- Primary tier of devotion; secondary tier; Elder God acknowledgment; major patrons -->

## Material culture and daily life



## Economy and technology



## Relations with outsiders

<!-- How other peoples refer to them; stereotypes; diplomatic/trade/military patterns -->

## Language, naming, communication

<!-- Defer to [[naming-conventions]] for naming style; document only the people-specific deviations or extensions here -->

## Subgroups and variations



## Open canon and future hooks

<!-- What remains deliberately undefined? Plot hooks? -->

---

<details>
<summary>Related pages</summary>

- [[peoples-of-eadras]]
- [[naming-conventions]]

</details>
