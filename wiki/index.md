---
title: TurboQuant-eval Wiki Index
kind: overview
updated: 2026-04-10
status: active
---

# TurboQuant-eval Wiki Index

Read this page first. It is the content-oriented map of the wiki.

## Overview

- [overview.md](overview.md) - Current synthesis of repository purpose, active knowledge areas, and recommended reading order.

## Sources

- [sources/repo-readme.md](sources/repo-readme.md) - Summary of the repository README and the evaluation shell architecture.
- [sources/ann-bench-result-bundles-2026-04-08.md](sources/ann-bench-result-bundles-2026-04-08.md) - Frozen ann-bench result bundle summary for the TurboQuant ANN experiments.
- [sources/third-party-turboquant-pytorch-changes-2026-04-08.md](sources/third-party-turboquant-pytorch-changes-2026-04-08.md) - Source summary for the nested `third_party/turboquant-pytorch` optimization work.
- [sources/vdb-sandbox-turboquant-changes-2026-04-08.md](sources/vdb-sandbox-turboquant-changes-2026-04-08.md) - Source summary for the outer `vdb-sandbox` benchmark and ANN comparison work.

## Entities

- [entities/turboquant-eval.md](entities/turboquant-eval.md) - Canonical page for the TurboQuant-eval repository, supported backends, and current operating scope.

## Concepts

- [concepts/amx-bf16-optimization.md](concepts/amx-bf16-optimization.md) - How BF16 support and AMX acceleration were enabled and measured.
- [concepts/fused-search-materialization.md](concepts/fused-search-materialization.md) - Why the search path was fused and moved into cache materialization.

## Comparisons

- [comparisons/ann-methods-dbpedia-1m.md](comparisons/ann-methods-dbpedia-1m.md) - Cross-method ANN comparison for TurboQuant, HNSW, and IVF on dbpedia-openai-1000k.

## Working notes outside the wiki

- `memory/` contains historical working notes that helped bootstrap this wiki.
- New durable knowledge should go into `wiki/`.
- New immutable source captures should go into `raw/`.