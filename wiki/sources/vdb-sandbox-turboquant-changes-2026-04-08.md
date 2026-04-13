---
title: vdb-sandbox TurboQuant changes on 2026-04-08
kind: source
updated: 2026-04-10
status: active
sources:
  - raw/legacy-memory/2026-04-08-vdb-sandbox-turboquant-changes.md
  - raw/benchmarks/ann-bench/turbo-quant/result/20260407_165642/results.json
  - raw/benchmarks/ann-bench/turbo-quant/result/20260407_170043/results.json
  - raw/benchmarks/ann-bench/turbo-quant/result/20260408_082226/results.json
  - raw/benchmarks/ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_wide/results.json
  - raw/benchmarks/ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_avx512only/results.json
  - raw/benchmarks/ann-bench/hnsw/result/20260408_compare_hnswflat_wide/results.json
  - raw/benchmarks/ann-bench/hnsw/result/20260408_compare_hnswsq_bf16_wide/results.json
  - raw/benchmarks/ann-bench/ivf/result/20260408_compare_ivfsq_bf16_wide/results.json
---

# vdb-sandbox TurboQuant changes on 2026-04-08

## Source

- Primary file: `raw/legacy-memory/2026-04-08-vdb-sandbox-turboquant-changes.md`
- Origin: canonicalized from `memory/vdb-sandbox_turboquant_changes_20260408.md` on 2026-04-10
- Preserved outer-repo commit referenced by the source: `abe189b`

## Key facts extracted

- The ann-bench search path was changed to build and cache a fused search matrix during materialization instead of reconstructing it during search.
- Cache signatures were versioned so newer fused layouts do not silently collide with older cache formats.
- `materialized_bytes_per_vector()` was updated to reflect what is actually stored.
- `compressors_v3.py` was extended with BF16-aware dtype support, allowing rotation and reconstruction matrix multiplies to use AMX-friendly BF16 execution.
- A cross-method ANN comparison was run on dbpedia-openai-1000k comparing HNSWFlat, HNSWSQ BF16, TurboQuant BF16, TurboQuant BF16 with AVX512-only, and IVFSQ BF16.

## Main interpretation

This source connects the implementation work to actual benchmark outcomes. It shows which changes were library-side, which were benchmark-side, and how the results compare against Faiss baselines.

## Frozen benchmark artifacts

The key benchmark JSON files referenced by this source are now frozen under `raw/benchmarks/ann-bench/` and summarized in [ann-bench-result-bundles-2026-04-08.md](ann-bench-result-bundles-2026-04-08.md).

## Durable benchmark conclusions from the source

- HNSWFlat is the absolute QPS leader across recall targets.
- TurboQuant reaches broader high-recall coverage than HNSWSQ BF16 and IVFSQ BF16.
- TurboQuant depends strongly on AMX; AVX512-only mode is much slower.
- TurboQuant has a strong storage-efficiency position even when absolute QPS is not the highest.

## Related pages

- [ann-bench-result-bundles-2026-04-08.md](ann-bench-result-bundles-2026-04-08.md)
- [../concepts/amx-bf16-optimization.md](../concepts/amx-bf16-optimization.md)
- [../concepts/fused-search-materialization.md](../concepts/fused-search-materialization.md)
- [../comparisons/ann-methods-dbpedia-1m.md](../comparisons/ann-methods-dbpedia-1m.md)