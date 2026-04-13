---
title: Fused Search Materialization
kind: concept
updated: 2026-04-10
status: active
sources:
  - raw/legacy-memory/2026-04-08-third-party-turboquant-pytorch-changes.md
  - raw/legacy-memory/2026-04-08-vdb-sandbox-turboquant-changes.md
---

# Fused Search Materialization

## Concept

Instead of rebuilding query-side and key-side search features during each search, the system materializes a fused search matrix ahead of time and stores it directly in cache.

## Mechanism

- Query features are represented as a concatenation like `[q, q_proj]`.
- Key features are represented as a concatenation like `[k_mse, weighted_qjl]`.
- Scoring becomes one matrix multiply between fused query features and fused key features.
- The key-side fused representation is built during materialization and cached.

## Why it matters

- It removes repeated per-block recomputation from the hot path.
- It makes benchmark results less sensitive to avoidable Python-side overhead.
- It aligns the outer ann-bench path with the nested library's newer fused search index support.

## Operational implications

- Cache format versioning matters, because the fused layout is not binary-compatible with older cache contents.
- Backward compatibility still matters for older cached experiments, but the system should fail loudly if the cache layout is unknown.

## Related pages

- [../sources/third-party-turboquant-pytorch-changes-2026-04-08.md](../sources/third-party-turboquant-pytorch-changes-2026-04-08.md)
- [../sources/vdb-sandbox-turboquant-changes-2026-04-08.md](../sources/vdb-sandbox-turboquant-changes-2026-04-08.md)
- [../entities/turboquant-eval.md](../entities/turboquant-eval.md)