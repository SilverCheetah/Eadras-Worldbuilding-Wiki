# LLM Wiki

A personal knowledge base maintained by Claude Code.
Based on Andrej Karpathy's LLM Wiki pattern.

**Entry points**: [[index]] · [[tags]] · [[log]]

## Purpose

This wiki is a structured, interlinked knowledge base for building a fantasy setting named Eadras.
Claude maintains the wiki. The human curates sources, asks questions, and guides the analysis.

## Folder structure

```
raw/          -- source documents (immutable -- never modify these)
wiki/         -- markdown pages maintained by Claude
wiki/index.md -- table of contents for the entire wiki
wiki/log.md   -- append-only record of all operations
```

## Ingest workflow

When the user adds a new source to `raw/` and asks you to ingest it:

1. Read the full source document
2. Discuss key takeaways with the user before writing anything
3. Create a summary page in `wiki/` named after the source
4. Create or update concept pages for each major idea or entity
5. Add wiki-links ([[page-name]]) to connect related pages
6. Update `wiki/index.md` with new pages and one-line descriptions
7. Append an entry to `wiki/log.md` with the date, source name, and what changed

A single source may touch 10-15 wiki pages. That is normal.

## Page format

Every wiki page should follow this structure:

```markdown
---
title: Page Title
tags: []
---

# Page Title

**Summary**: One to two sentences describing this page.

**Sources**: List of raw source files this page draws from.

**Last updated**: Date of most recent update.

---

Main content goes here. Use clear headings and short paragraphs.

Link to related concepts using throughout the text.

<details>
<summary>Related pages</summary>

- - </details>
```

**Related pages convention**: always wrap the related-pages list in a `<details><summary>Related pages</summary>…</details>` block (with blank lines around the inner content). The block folds by default in reading mode; readers tap the summary to expand. Same pattern is used for collapsible Axes-of-Creation slider sections via `<details class="axes-block">`.

**Rules for Claude:**
- Always include the YAML frontmatter at the very top of every new or updated page
- Fill in `title:` with the exact page title
- Add between 1 and 5 relevant tags inside the tags: [] array
- Only add tags that actually describe the core content of this page
- If the page is very specific and only has one or two good tags, that's perfectly fine — don't add filler tags
- Keep tags lowercase, use hyphens for multi-word tags (example: `magic-system`, `the-three`)
- Update `last_updated` only when you actually change the page

## Citation rules

- Every factual claim should reference its source file
- Use the format (source: filename.pdf) after the claim
- If two sources disagree, note the contradiction explicitly
- If a claim has no source, mark it as needing verification

## Question answering

When the user asks a question:

1. Read `wiki/index.md` first to find relevant pages
2. Read those pages and synthesize an answer
3. Cite specific wiki pages in your response
4. If the answer is not in the wiki, say so clearly
5. If the answer is valuable, offer to save it as a new wiki page

Good answers should be filed back into the wiki so they compound over time.

## Lint

When the user asks you to lint or audit the wiki:

- Check for contradictions between pages
- Find orphan pages (no inbound links from other pages)
- Identify concepts mentioned in pages that lack their own page
- Flag claims that may be outdated based on newer sources
- Check that all pages follow the page format above
- Report findings as a numbered list with suggested fixes

## Rules

- Never modify anything in the `raw/` folder
- Always update `wiki/index.md` and `wiki/log.md` after changes
- Keep page names lowercase with hyphens (e.g. `machine-learning.md`)
- Write in clear, plain language
- When uncertain about how to categorize something, ask the user
