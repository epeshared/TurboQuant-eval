# TurboQuant-eval Wiki Schema

This repository uses a three-layer documentation pattern inspired by Karpathy's LLM Wiki note.

## Layers

1. `raw/`
   - Immutable source material.
   - Examples: clipped articles, experiment notes, benchmark outputs, copied emails, exported chats, or frozen snapshots of internal notes.
   - Agents may read from this directory, but must not edit existing source files.

2. `wiki/`
   - LLM-maintained knowledge base.
   - This is where summaries, entity pages, concept pages, and comparison pages live.
   - Agents are expected to update this layer as new sources arrive or new analysis is produced.

3. `AGENTS.md`
   - The schema for how the wiki is organized and maintained.
   - If the wiki structure evolves, update this file first.

## Directory layout

```text
raw/                       Immutable inputs and captured source material
wiki/
  index.md                 Content index; read this first
  log.md                   Append-only operational log
  overview.md              Current high-level synthesis of the repo state
  sources/                 One page per source or source bundle
  entities/                Stable subjects: repos, backends, datasets, hardware
  concepts/                Cross-cutting ideas and mechanisms
  comparisons/             Tables and multi-system analyses
memory/                    Legacy working notes; useful inputs but not canonical raw
```

## Page conventions

All pages in `wiki/` should be Markdown and should use YAML frontmatter when practical.

Recommended frontmatter fields:

```yaml
title: Human readable title
kind: overview | source | entity | concept | comparison
updated: YYYY-MM-DD
status: active | draft | frozen
sources:
  - path/to/source.md
```
```

Write short, factual pages. Separate observed results from interpretation. If a claim depends on a dated benchmark or experiment, include the date and source link.

## Operations

### Ingest

When a new source arrives:

1. Copy or save the immutable source into `raw/` when possible.
2. Create or update one page in `wiki/sources/` that summarizes the source.
3. Update affected pages in `wiki/entities/`, `wiki/concepts/`, and `wiki/comparisons/`.
4. Update `wiki/index.md` if new pages were created.
5. Append a dated entry to `wiki/log.md`.

### Query and file-back

When answering questions from this repository's knowledge base:

1. Read `wiki/index.md` first.
2. Read the smallest set of linked pages needed to answer the question.
3. If the answer creates durable knowledge, file it back into `wiki/` as a new or updated page.
4. Log the update in `wiki/log.md`.

### Lint

Periodically check for:

- orphan pages not linked from `wiki/index.md`
- claims superseded by newer measurements
- contradictions across comparison pages
- source pages that have no downstream concept/entity updates
- pages with stale benchmark numbers but no date context

## Editing rules

- Do not rewrite or paraphrase an existing raw source in place; create a wiki page instead.
- Treat `memory/` as legacy input material. It can inform the wiki, but new canonical sources should go under `raw/`.
- Keep the wiki interlinked with standard Markdown links.
- Favor one subject per page.
- Put benchmark tables in `wiki/comparisons/`, not in entity pages.
- Put mechanism explanations in `wiki/concepts/`, not in source pages.
- Use `wiki/log.md` as an append-only timeline. Do not rewrite prior log entries except to fix formatting mistakes.

## Current repository-specific scope

The current knowledge base is centered on:

- the `TurboQuant-eval` evaluation shell
- upstream backend coverage for QJL, PolarQuant, and TurboQuant reference code
- BF16 / AMX optimization work
- ANN benchmark comparisons involving TurboQuant, HNSW, and IVF variants

Future pages should preserve this scope unless the repository purpose changes.