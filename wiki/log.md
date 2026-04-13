---
title: TurboQuant-eval Wiki Log
kind: overview
updated: 2026-04-10
status: active
---

# TurboQuant-eval Wiki Log

Append-only record of wiki operations.

## [2026-04-10] init | bootstrap wiki structure

- Created `AGENTS.md` to define the raw/wiki/schema workflow.
- Added `raw/README.md` to document immutable source handling.
- Added `wiki/index.md`, `wiki/log.md`, and `wiki/overview.md`.
- Added source pages for the repo README and two existing TurboQuant change notes.
- Added concept pages for AMX BF16 optimization and fused search materialization.
- Added an entity page for the TurboQuant-eval repository.
- Added an ANN comparison page covering TurboQuant, HNSW, and IVF results.

## [2026-04-10] ingest | promote legacy memory notes into raw

- Added frozen canonical snapshots under `raw/legacy-memory/` for the two key historical TurboQuant notes.
- Repointed wiki source pages and frontmatter references from `memory/` to the new raw canonical paths.
- Updated the overview to reflect that the raw layer is now populated, though still incomplete.

## [2026-04-10] ingest | freeze benchmark result files into raw

- Added frozen `ann-bench` benchmark snapshots under `raw/benchmarks/ann-bench/` for the key TurboQuant, HNSW, and IVF comparison runs.
- Added README files documenting the canonical benchmark snapshot layout.
- Added a dedicated wiki source page for the frozen ann-bench result bundle.
- Repointed the ANN comparison page to cite the frozen raw benchmark files directly.