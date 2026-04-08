# vdb-sandbox TurboQuant ann-bench Changes

Date: 2026-04-08

Repository
- Path: /nvme5/xtang/vdb-workspace/vdb-sandbox
- Git repo: [intel-sandbox/vdb-sandbox](https://github.com/intel-sandbox/vdb-sandbox)
- Branch at capture time: main
- Preserved commit: [abe189b](https://github.com/intel-sandbox/vdb-sandbox/commit/abe189bf90bcf3fb450921bb393ad97136ba6fb2)
- Tracked modified file in this repo: ann-bench/turbo-quant/src/bench_turboquant_ann.py

Why This File Matters
- This is the benchmark-side implementation that recovered TurboQuant ANN QPS on CPU.
- These changes are tracked by the outer vdb-sandbox repo and should be committed there.
- These changes are separate from the nested third_party/turboquant-pytorch repo changes.

Files Changed
- ann-bench/turbo-quant/src/bench_turboquant_ann.py

Key Changes
- Added make_turboquant_prod() so ann-bench can instantiate TurboQuantProd whether the third-party repo exposes a dtype argument or not.
- Kept the batched exact_rerank() implementation that gathers candidates in chunks and uses torch.bmm instead of a Python per-query loop.
- Kept the approximate-search runtime fusion path that concatenates [q, q_proj] and [k_mse, weighted_qjl] and scores with one large matmul.
- Moved fused search matrix creation into the materialize/cache stage with build_search_matrix().
- Changed the cache payload to store search_matrix directly instead of recomputing weighted_qjl and concatenation on every search call.
- Bumped the ann-bench cache format and added search_layout=fused_matrix_v1 to the cache signature to avoid collisions with older local cache layouts.
- Kept legacy runtime fallback for caches that still expose k_mse/qjl_signs/residual_norm, but now emit a clear error if the cache is neither fused-search nor legacy dense-search.
- materialized_bytes_per_vector() now reports bytes based on the tensors actually stored in the cache.

Effect Of These Changes
- Removed repeated per-block runtime work from the hot search loop by precomputing the fused search matrix once during cache build.
- Preserved the benchmark-side rerank optimization and approximate-search fusion that were already validated earlier.
- Made ann-bench cache migrations safer on a machine that may still have older experimental TurboQuant cache formats.

Validation Snapshots
- TurboQuant-only rerank-optimized run: ann-bench/turbo-quant/result/20260407_165642/results.json
- TurboQuant-only rerank + approximate-search runtime fusion run: ann-bench/turbo-quant/result/20260407_170043/results.json
- TurboQuant-only fused-search-cache run after the current changes: ann-bench/turbo-quant/result/20260408_082226/results.json

Representative Result
- bits=4, qjl_dim=1536, rerank=100 reached about 1095.83 QPS at recall@10 0.9988 in result/20260408_082226/results.json.

What Must Be Preserved Separately
- These changes live in the outer vdb-sandbox repo and must be committed there.
- They are visible from `git status` run at /nvme5/xtang/vdb-workspace/vdb-sandbox.
- They are not enough by themselves to preserve the nested third-party library optimizations.

Suggested Preserve Commands
- cd /nvme5/xtang/vdb-workspace/vdb-sandbox
- git status --short
- git add ann-bench/turbo-quant/src/bench_turboquant_ann.py
- git commit -m "Optimize TurboQuant ann-bench search cache path"

Important Note
- If the outer repo is reset, checked out to another branch, or cherry-picked without committing this file, the benchmark-side optimization path can be lost even if the nested third-party repo still contains its own local edits.
- This benchmark-side optimization set is currently preserved in commit abe189b on main.