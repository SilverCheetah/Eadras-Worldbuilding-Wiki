# LLM Wiki — Claude Code Bootstrap

A personal knowledge base for the fantasy setting **Eadras**, maintained by Claude Code.
Based on Andrej Karpathy's LLM Wiki pattern, adapted for the Eadras Mythos Worldbuilding Project.

**Entry points**: [[index]] · [[tags]] · [[log]]

## Canonical wiki rules

**`wiki/system-governance.md` is the canonical rule-set for the wiki.** It covers:

- Frontmatter schema, locked enum values, schema exceptions
- Body conventions (Axes-of-Creation block, OOC tonal-references block, Related pages block)
- Naming rules (filenames, plurals, registers, capitalization, renames and aliases)
- Calendar rules (AP master + six mortal systems)
- Canon hierarchy (established / proposed / pending / deprecated; sealed-canon rules; probabilistic canon)
- AI interaction rules (canon resolution, tone, generation discipline, source-to-wiki ingest, question answering, lint, protocol back-propagation)
- Backups and exports (`generate_export.py`, `split_export.py`, the no-`sed` rule)
- The protocol layer (`wiki/protocols/`)
- Plugin integration (Templater, Dataview, Chronos, Meta Bind, etc.)

Read it before any non-trivial wiki work. When a rule here and a rule in `wiki/system-governance.md` appear to conflict, the governance document wins; flag the drift and update this file.

The `eadras-wiki` Claude Code skill (`.claude/skills/eadras-wiki/SKILL.md`) loads `wiki/system-governance.md` and `wiki/calendar.md` automatically on session start, and is the right entry-point for any wiki edits, ingests, or canon questions.

## Folder structure

```
raw/                 -- source documents (immutable; never modify)
wiki/                -- markdown pages maintained by Claude
wiki/index.md        -- table of contents
wiki/log.md          -- append-newest-first record of all operations
wiki/images/         -- image assets cited from wiki pages
wiki/templates/      -- Templater templates for new pages
wiki/protocols/      -- portable AI-session primers (OOC, never canon)
wiki/rpg/            -- splat-book / OOC RPG material
wiki/_sealed/        -- OOC plot-spine secrets; one-way linking only
```

## External source archives

Large files moved out of `raw/` for iPhone-sync (2026-05-15). Treat as immutable like `raw/`:

- `D:\Worldbuilding\Chat Logs\` — long chat-log source files (`Grok Chat *.txt`, `Playground generation *.txt`, `Elder Gods chat *.txt`, `Extra large grok chat *.txt`, etc.). When a wiki page's *Sources* line cites one of these filenames, the file lives in **Chat Logs**, not `raw/`.
- `D:\Worldbuilding\Worldbuilding LLM Wiki\images\` — image assets (plate-tectonics snapshots, map exports, illustrations) that originated in `raw/` but exceed the iPhone-sync size threshold. The corresponding `.txt` companion files (e.g. `Eadras – Golden Age Map.txt`) remain in `raw/`.

## Starting a session

1. **Read `wiki/system-governance.md`** for the rules — schema, body conventions, calendar, canon hierarchy, ingest, exports, tone.
2. **Read `wiki/index.md`** for the table of contents.
3. **Read the specific pages** relevant to the user's request.

## Hard rules

- **Never modify anything in `raw/` or `D:\Worldbuilding\Chat Logs\`**. Both are immutable source archives.
- **Always update `wiki/index.md`** with new pages and one-line descriptions when canon is added.
- **Always append to `wiki/log.md`** after any wiki change. New entries go at the **top** of the file (newest first), with a `## YYYY-MM-DD — Title` heading and `---` separator.
- **Never use `sed -i` / `awk -i` for cross-file edits.** Use the Edit tool for one-offs; use Python `str.replace`-based sweep scripts at repo root for sweeps. See *Backups and Exports* in `system-governance.md` for the 2026-05-10 incident this rule prevents.
- **When uncertain about categorization**, ask the user — do not invent values outside the locked enums.

## Sub-skills

Available skills (see system-prompt section for full descriptions):

- `eadras-wiki` — primary skill for wiki edits, ingests, and canon questions. Loads `system-governance.md` and `calendar.md`.
- `adversarial` — Skeptic + Advocate audit of a piece of canon.
- `five-whys` — probe one load-bearing element of a canon page.
- `multi-pov` — tell one event from multiple in-universe perspectives.
- `negative-space` — find under-covered cells of the canon.

## Help and feedback

- `/help`: get help with Claude Code.
- Report issues at https://github.com/anthropics/claude-code/issues.
