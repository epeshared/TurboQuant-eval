---
title: ANN Methods on dbpedia-openai-1000k
kind: comparison
updated: 2026-04-10
status: active
sources:
  - raw/legacy-memory/2026-04-08-vdb-sandbox-turboquant-changes.md
  - raw/benchmarks/ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_wide/results.json
  - raw/benchmarks/ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_avx512only/results.json
  - raw/benchmarks/ann-bench/hnsw/result/20260408_compare_hnswflat_wide/results.json
  - raw/benchmarks/ann-bench/hnsw/result/20260408_compare_hnswsq_bf16_wide/results.json
  - raw/benchmarks/ann-bench/ivf/result/20260408_compare_ivfsq_bf16_wide/results.json
---

# ANN Methods on dbpedia-openai-1000k

## Setup

- Dataset: dbpedia-openai-1000k-angular
- Dimensionality: 1536
- Base vectors: about 990k
- Queries: 1k
- Metric: angular or cosine
- Threads: 16 on Sapphire Rapids

## Methods compared

- HNSWFlat
- HNSWSQ BF16
- TurboQuant BF16 with AMX
- TurboQuant BF16 with AVX512-only
- IVFSQ BF16

## Frozen raw artifacts

- `raw/benchmarks/ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_wide/results.json`
- `raw/benchmarks/ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_avx512only/results.json`
- `raw/benchmarks/ann-bench/hnsw/result/20260408_compare_hnswflat_wide/results.json`
- `raw/benchmarks/ann-bench/hnsw/result/20260408_compare_hnswsq_bf16_wide/results.json`
- `raw/benchmarks/ann-bench/ivf/result/20260408_compare_ivfsq_bf16_wide/results.json`

## Representative QPS by recall target

| Target recall@10 | HNSWFlat | HNSWSQ BF16 | TurboQuant BF16 | TQ BF16 (AVX512) | AMX/AVX512 | IVFSQ BF16 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| ~0.87 | 28,869 | 35,038 | 1,688 | 355 | 4.8x | 2,649 |
| ~0.93 | 22,412 | 21,129 | 1,685 | 355 | 4.7x | 1,340 |
| ~0.95 | 21,232 | 14,187 | 1,685 | 355 | 4.7x | 1,340 |
| ~0.97 | 16,383 | 3,095 | 1,685 | 355 | 4.7x | 674 |
| ~0.98 | 12,067 | not reachable | 1,459 | 346 | 4.2x | 343 |
| ~0.99 | 9,250 | not reachable | 1,459 | 346 | 4.2x | 343 |
| ~0.995 | 7,576 | not reachable | 1,459 | 334 | 4.4x | 89 |
| ~0.999 | 2,091 | not reachable | 1,043 | 258 | 4.0x | not reachable |

## Main conclusions

- HNSWFlat is the clear absolute-QPS leader across all practical recall levels.
- HNSWSQ BF16 has strong low-recall throughput, but tops out around 0.97 recall on this dataset.
- TurboQuant covers a wider high-recall range than HNSWSQ BF16 and IVFSQ BF16.
- TurboQuant is heavily dependent on AMX for competitive performance; AVX512-only mode is much slower.
- IVFSQ BF16 trails badly at high recall.

## Storage-efficiency angle

The benchmark notes report that TurboQuant can reach about 674 bytes per vector in one representative configuration, far smaller than the HNSWFlat footprint. That is the main reason TurboQuant remains interesting despite its lower absolute QPS.

## Related pages

- [../concepts/amx-bf16-optimization.md](../concepts/amx-bf16-optimization.md)
- [../concepts/fused-search-materialization.md](../concepts/fused-search-materialization.md)
- [../sources/ann-bench-result-bundles-2026-04-08.md](../sources/ann-bench-result-bundles-2026-04-08.md)
- [../sources/vdb-sandbox-turboquant-changes-2026-04-08.md](../sources/vdb-sandbox-turboquant-changes-2026-04-08.md)