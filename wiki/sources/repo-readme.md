---
title: Repository README
kind: source
updated: 2026-04-10
status: active
sources:
  - README.md
---

# Repository README

## Source

- Primary file: `README.md`

## What this source establishes

- `TurboQuant-eval` is an evaluation scaffold, not a forced merge of upstream projects.
- The current backend coverage is QJL official, PolarQuant official, and the TurboQuant community reference.
- The repository standardizes task entrypoints, metrics collection, normalized result schema, and comparison workflow.
- The currently documented runnable tasks are `kv_fidelity` and LongBench wrappers.

## Structural facts captured from the source

- `configs/` holds task configurations.
- `scripts/` holds repo setup helpers.
- `third_party/` holds upstream repositories.
- `turboquant_eval/` holds adapters, runners, tasks, and result schema code.
- Results are normalized into JSON and persist raw stdout and stderr logs.

## Why this matters for the wiki

This source defines the outer boundary of the knowledge base: the repo is about evaluation and comparison, not implementation unification. Pages that drift into unrelated model internals or generic quantization theory should link back to the evaluation use case.

## Related pages

- [../entities/turboquant-eval.md](../entities/turboquant-eval.md)
- [../comparisons/ann-methods-dbpedia-1m.md](../comparisons/ann-methods-dbpedia-1m.md)