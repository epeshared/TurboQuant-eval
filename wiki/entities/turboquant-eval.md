---
title: TurboQuant-eval
kind: entity
updated: 2026-04-10
status: active
sources:
  - README.md
  - raw/legacy-memory/2026-04-08-third-party-turboquant-pytorch-changes.md
  - raw/legacy-memory/2026-04-08-vdb-sandbox-turboquant-changes.md
---

# TurboQuant-eval

TurboQuant-eval is the repository-level evaluation hub for comparing multiple compression backends under a normalized workflow.

## Role in the stack

- It standardizes task entrypoints.
- It normalizes result schema and logging.
- It keeps upstream code isolated under `third_party/`.
- It is the natural place to store cross-backend comparisons and benchmark conclusions.

## Backends currently in scope

- QJL official
- PolarQuant official
- TurboQuant reference implementation

## Current evidence captured in the wiki

- TurboQuant's nested third-party implementation required dtype-aware changes before BF16 and AMX could be used consistently.
- The ann-bench path in the outer repo gained a fused search matrix materialization flow that reduced repeated hot-path work.
- TurboQuant on BF16 plus AMX is meaningfully faster than AVX512-only TurboQuant, but still slower than HNSWFlat in absolute ANN QPS on dbpedia-openai-1000k.

## Important repository boundary

This repository should keep implementation forks isolated. If substantial library changes happen under `third_party/`, summarize them here and in source pages, but do not blur the difference between the evaluation shell and the nested upstream repositories.

## Related pages

- [../sources/repo-readme.md](../sources/repo-readme.md)
- [../sources/third-party-turboquant-pytorch-changes-2026-04-08.md](../sources/third-party-turboquant-pytorch-changes-2026-04-08.md)
- [../sources/vdb-sandbox-turboquant-changes-2026-04-08.md](../sources/vdb-sandbox-turboquant-changes-2026-04-08.md)
- [../comparisons/ann-methods-dbpedia-1m.md](../comparisons/ann-methods-dbpedia-1m.md)