---
title: TurboQuant-eval Overview
kind: overview
updated: 2026-04-10
status: active
sources:
  - README.md
  - raw/legacy-memory/2026-04-08-third-party-turboquant-pytorch-changes.md
  - raw/legacy-memory/2026-04-08-vdb-sandbox-turboquant-changes.md
---

# TurboQuant-eval Overview

TurboQuant-eval is an evaluation shell for comparing three related compression paths without forcing them into a single merged codebase: QJL official, PolarQuant official, and the TurboQuant community reference.

The current wiki focuses on three knowledge threads:

1. Repository scope and backend coverage.
2. BF16 and AMX optimization work around TurboQuant.
3. ANN benchmark comparisons between TurboQuant and Faiss-based alternatives.

## Current high-confidence conclusions

- The repository is designed as a normalized evaluation layer, not as a combined implementation fork.
- TurboQuant BF16 now has a credible AMX execution path after dtype-aware changes in the nested third-party code.
- Moving fused search matrix construction into cache materialization reduced repeated hot-path work in ann-bench.
- On dbpedia-openai-1000k, HNSWFlat dominates absolute QPS, while TurboQuant is most attractive on storage efficiency.
- Disabling AMX and falling back to AVX512 BF16 makes TurboQuant roughly 4.0x to 4.8x slower end-to-end.

## Recommended reading order

1. [entities/turboquant-eval.md](entities/turboquant-eval.md)
2. [sources/repo-readme.md](sources/repo-readme.md)
3. [concepts/amx-bf16-optimization.md](concepts/amx-bf16-optimization.md)
4. [concepts/fused-search-materialization.md](concepts/fused-search-materialization.md)
5. [comparisons/ann-methods-dbpedia-1m.md](comparisons/ann-methods-dbpedia-1m.md)

## Open gaps

- The wiki does not yet cover actual LongBench result pages for QJL or PolarQuant.
- `raw/` now contains canonicalized historical notes and selected benchmark snapshots, but it still lacks broader experiment artifacts and future source captures from ongoing work.
- No lint workflow exists yet for finding stale pages or contradictions automatically.