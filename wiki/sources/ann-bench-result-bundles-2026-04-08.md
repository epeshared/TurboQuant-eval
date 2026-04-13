---
title: ann-bench result bundles on 2026-04-08
kind: source
updated: 2026-04-10
status: active
sources:
  - raw/benchmarks/ann-bench/turbo-quant/result/20260407_165642/results.json
  - raw/benchmarks/ann-bench/turbo-quant/result/20260407_170043/results.json
  - raw/benchmarks/ann-bench/turbo-quant/result/20260408_082226/results.json
  - raw/benchmarks/ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_wide/results.json
  - raw/benchmarks/ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_avx512only/results.json
  - raw/benchmarks/ann-bench/hnsw/result/20260408_compare_hnswflat_wide/results.json
  - raw/benchmarks/ann-bench/hnsw/result/20260408_compare_hnswsq_bf16_wide/results.json
  - raw/benchmarks/ann-bench/ivf/result/20260408_compare_ivfsq_bf16_wide/results.json
---

# ann-bench result bundles on 2026-04-08

## Source set

This page groups the frozen benchmark result files that back the current TurboQuant ANN performance discussion.

### TurboQuant rerank and fused-search milestones

- `raw/benchmarks/ann-bench/turbo-quant/result/20260407_165642/results.json`
- `raw/benchmarks/ann-bench/turbo-quant/result/20260407_170043/results.json`
- `raw/benchmarks/ann-bench/turbo-quant/result/20260408_082226/results.json`

### Cross-method comparison set

- `raw/benchmarks/ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_wide/results.json`
- `raw/benchmarks/ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_avx512only/results.json`
- `raw/benchmarks/ann-bench/hnsw/result/20260408_compare_hnswflat_wide/results.json`
- `raw/benchmarks/ann-bench/hnsw/result/20260408_compare_hnswsq_bf16_wide/results.json`
- `raw/benchmarks/ann-bench/ivf/result/20260408_compare_ivfsq_bf16_wide/results.json`

## What this source set is used for

- Verifying the stepwise TurboQuant search-path improvements.
- Comparing TurboQuant BF16 against HNSWFlat, HNSWSQ BF16, and IVFSQ BF16.
- Quantifying the difference between AMX-enabled TurboQuant and AVX512-only TurboQuant.

## Related pages

- [../comparisons/ann-methods-dbpedia-1m.md](../comparisons/ann-methods-dbpedia-1m.md)
- [vdb-sandbox-turboquant-changes-2026-04-08.md](vdb-sandbox-turboquant-changes-2026-04-08.md)