---
title: third_party turboquant-pytorch changes on 2026-04-08
kind: source
updated: 2026-04-10
status: active
sources:
  - raw/legacy-memory/2026-04-08-third-party-turboquant-pytorch-changes.md
---

# third_party turboquant-pytorch changes on 2026-04-08

## Source

- Primary file: `raw/legacy-memory/2026-04-08-third-party-turboquant-pytorch-changes.md`
- Origin: canonicalized from `memory/third_party_turboquant_pytorch_changes_20260408.md` on 2026-04-10
- Preserved nested-repo commit referenced by the source: `3f90e1c`

## Key facts extracted

- The nested `third_party/turboquant-pytorch` repository received dtype-aware changes across `turboquant.py`, `compressors.py`, and `compressors_v3.py`.
- `resolve_torch_dtype()` and dtype-aware matrix generation were added so rotation and QJL operations can run in BF16 instead of staying stuck in float32-only paths.
- The quantization path was changed to use Lloyd-Max codebook bucket boundaries with `torch.bucketize()` instead of full diff tensor materialization plus `argmin`.
- A fused attention scoring path was introduced so query and key features can be concatenated and scored with one matrix multiply.
- `materialize_search_index()` was added so ann-bench can consume a fused search matrix directly from the library.

## Main interpretation

This source is the implementation-side foundation for later benchmark wins. Without these nested-repo changes, the outer ann-bench optimizations would still be limited by float32-only library behavior.

## Risks and operational notes

- This is an independent git repository under `third_party/`.
- Changes in this repo are not preserved by commits in the outer repository.
- The source explicitly warns that these changes are easy to lose unless they are committed or exported separately.

## Related pages

- [../concepts/amx-bf16-optimization.md](../concepts/amx-bf16-optimization.md)
- [../concepts/fused-search-materialization.md](../concepts/fused-search-materialization.md)
- [../entities/turboquant-eval.md](../entities/turboquant-eval.md)