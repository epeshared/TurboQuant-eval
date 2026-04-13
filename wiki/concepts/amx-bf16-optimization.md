---
title: AMX BF16 Optimization
kind: concept
updated: 2026-04-10
status: active
sources:
  - raw/legacy-memory/2026-04-08-third-party-turboquant-pytorch-changes.md
  - raw/legacy-memory/2026-04-08-vdb-sandbox-turboquant-changes.md
---

# AMX BF16 Optimization

## Concept

TurboQuant only benefits from Sapphire Rapids AMX if the relevant matrix multiplies stay in BF16 all the way through the implementation. Float32-only helper paths erase most of the hardware advantage.

## What changed

- Dtype-aware construction was added for rotation and QJL matrices.
- `compressors_v3.py` was updated so compression and reconstruction matrix multiplies can run with BF16 tensors.
- The benchmark path was adjusted so ann-bench can instantiate and materialize BF16-capable TurboQuant flows correctly.

## What was measured

- On a representative D=128 case, the BF16 path improved end-to-end compression plus decompression time by about 1.17x.
- The decompression path, which is closer to pure matrix multiply, improved by about 1.51x.
- For ANN benchmarking on dbpedia-openai-1000k, forcing AVX512 BF16 with `ONEDNN_MAX_CPU_ISA=AVX512_CORE_BF16` made TurboQuant about 4.0x to 4.8x slower than the AMX-enabled BF16 path.

## Limiting factor

The benchmark notes identify `torch.bucketize()` as a major remaining bottleneck in the compression path. That limits how much of the AMX benefit appears in end-to-end timings.

## Why this matters

This concept explains the difference between "BF16 is supported" and "BF16 is actually fast". For this repository, the important point is not just datatype correctness, but whether the data path keeps enough BF16 matmul work intact for AMX to matter.

## Related pages

- [../sources/third-party-turboquant-pytorch-changes-2026-04-08.md](../sources/third-party-turboquant-pytorch-changes-2026-04-08.md)
- [../sources/vdb-sandbox-turboquant-changes-2026-04-08.md](../sources/vdb-sandbox-turboquant-changes-2026-04-08.md)
- [../comparisons/ann-methods-dbpedia-1m.md](../comparisons/ann-methods-dbpedia-1m.md)