# Frozen Source Snapshot

Imported into `raw/legacy-memory/` on 2026-04-10 from `memory/third_party_turboquant_pytorch_changes_20260408.md`.
This file is the canonical raw source snapshot for the corresponding wiki source page.

---

# third_party turboquant-pytorch Changes

Date: 2026-04-08

Repository
- Path: /nvme5/xtang/vdb-workspace/vdb-sandbox/TurboQuant-eval/third_party/turboquant-pytorch
- Original upstream repo at capture time: [tonbistudio/turboquant-pytorch](https://github.com/tonbistudio/turboquant-pytorch)
- Local branch at capture time: master
- Pre-rebase HEAD at capture time: [2fdeff1](https://github.com/tonbistudio/turboquant-pytorch/commit/2fdeff133804d555114d418934284fddf8a3090c)
- Preserved commit: [3f90e1c](https://github.com/epeshared/turboquant-pytorch/commit/3f90e1c33a23619d4eadf306f042ff54da7324c6)
- Current remote holding preserved commit: [epeshared/turboquant-pytorch](https://github.com/epeshared/turboquant-pytorch)
- Modified files in this independent repo:
  - turboquant.py
  - lloyd_max.py
  - compressors.py
  - compressors_v3.py

Important Separation From vdb-sandbox
- This is an independent nested git repository.
- Its changes do not appear in `git status` for the outer /nvme5/xtang/vdb-workspace/vdb-sandbox repo.
- A vdb-sandbox commit or push does not preserve these edits.
- If you want to keep these optimizations, commit them inside this nested repo or export a patch from this nested repo.

Files Changed
- turboquant.py
- lloyd_max.py
- compressors.py
- compressors_v3.py

turboquant.py Summary
- Added resolve_torch_dtype() to normalize string or torch dtype inputs.
- Added dtype-aware matrix generation for rotation and QJL matrices.
- Added dtype support to TurboQuantMSE and TurboQuantProd constructors.
- Made rotate() and unrotate() explicitly align input device and dtype with the stored buffers.
- Switched TurboQuantMSE.quantize() to use the LloydMaxCodebook quantize path instead of manually materializing diffs and calling argmin.
- Added materialize_search_index() so ann-bench can build a fused search matrix directly from the library.
- Expanded inner_product() to support scalar, vector, and batched pairwise use cases instead of only the simple elementwise estimator path.
- Kept the estimator mathematically equivalent while making batched BF16 execution possible.

lloyd_max.py Summary
- Replaced abs(argmin) quantization with torch.bucketize() over precomputed Lloyd-Max boundaries.
- This removes the explicit (..., n_levels) diff tensor materialization from the quantize path.
- This should reduce quantize/build/materialize cost, especially during cache construction.

compressors.py Summary
- Added dtype-aware constructor options for TurboQuantCompressorV2 and TurboQuantCompressorMSE.
- Reused the shared LloydMaxCodebook quantize path instead of local diff/argmin quantization.
- Reused the shared rotation/QJL helpers instead of building separate float32-only matrices.
- Removed the duplicate rotation matmul in TurboQuantCompressorV2.compress().
- Stopped forcing the attention scoring path through float32-only tensors.
- Replaced the old three-step attention score path with a fused query/key concatenation path:
  - query_search = [queries, S@queries]
  - key_search = [k_mse, weighted_signs]
  - scores = query_search @ key_search^T
- This is the key third-party change aimed at making BF16 / AMX execution realistic for the attention-side scoring path.

compressors_v3.py Summary
- Replaced the local diff/argmin quantize path with the shared LloydMaxCodebook bucketize path.
- This keeps the V3 path aligned with the same faster quantization method.

Why These Changes Matter
- Before these edits, the third-party code still had several float32-only paths that blocked or reduced BF16 / AMX benefit.
- The nested repo now exposes the library features ann-bench expects for dtype-aware search materialization.
- The quantization path is lighter because it uses bucketize instead of building full centroid-diff tensors.

Validation Notes
- Import and runtime sanity checks passed after the changes.
- The ann-bench TurboQuant-only rerun using the current combined state completed successfully and produced result/20260408_082226.

Representative Result Seen Through ann-bench
- bits=4, qjl_dim=1536, rerank=100 reached about 1095.83 QPS at recall@10 0.9988 in ann-bench/turbo-quant/result/20260408_082226/results.json.

Suggested Preserve Commands
- cd /nvme5/xtang/vdb-workspace/vdb-sandbox/TurboQuant-eval/third_party/turboquant-pytorch
- git status --short
- git add turboquant.py lloyd_max.py compressors.py compressors_v3.py
- git commit -m "Add dtype-aware fused search and bucketize quantization"

Optional Extra Safety
- cd /nvme5/xtang/vdb-workspace/vdb-sandbox/TurboQuant-eval/third_party/turboquant-pytorch
- git diff > /nvme5/xtang/vdb-workspace/vdb-sandbox/TurboQuant-eval/memory/third_party_turboquant_pytorch_changes_20260408.patch

Important Note
- These changes are the easiest part to forget because they live under third_party and are not tracked by the outer repo. If you change outer branches, push only vdb-sandbox, or later clean this nested repo, these optimizations can disappear unless they are separately committed or exported.
- This third-party optimization set is currently preserved in commit 3f90e1c on master and has been pushed to epeshared/turboquant-pytorch.