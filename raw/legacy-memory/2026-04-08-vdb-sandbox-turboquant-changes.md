# Frozen Source Snapshot

Imported into `raw/legacy-memory/` on 2026-04-10 from `memory/vdb-sandbox_turboquant_changes_20260408.md`.
This file is the canonical raw source snapshot for the corresponding wiki source page.

---

# vdb-sandbox TurboQuant 变更记录

日期：2026-04-08

---

## 一、ann-bench 搜索缓存路径优化

### 仓库信息

- 路径：/nvme5/xtang/vdb-workspace/vdb-sandbox
- Git 仓库：[intel-sandbox/vdb-sandbox](https://github.com/intel-sandbox/vdb-sandbox)
- 分支：main
- 保留提交：[abe189b](https://github.com/intel-sandbox/vdb-sandbox/commit/abe189bf90bcf3fb450921bb393ad97136ba6fb2)

### 修改文件

- ann-bench/turbo-quant/src/bench_turboquant_ann.py

### 修改内容

1. 新增 `make_turboquant_prod()`，使 ann-bench 无论第三方库是否暴露 dtype 参数都能正确实例化 `TurboQuantProd`。
2. 保留批量 `exact_rerank()` 实现——分块收集候选向量后用 `torch.bmm` 代替逐查询 Python 循环。
3. 保留近似搜索融合路径——拼接 `[q, q_proj]` 和 `[k_mse, weighted_qjl]`，用一次大矩阵乘完成打分。
4. 将融合搜索矩阵的构建移入 materialize/cache 阶段（`build_search_matrix()`），缓存直接存储 `search_matrix`，避免每次搜索时重复计算 `weighted_qjl` 拼接。
5. 升级缓存格式版本号，签名中加入 `search_layout=fused_matrix_v1`，防止与旧缓存格式冲突。
6. 保留对旧缓存格式（k_mse/qjl_signs/residual_norm）的兼容回退，但缓存既不是融合搜索格式也不是遗留格式时会报明确错误。
7. `materialized_bytes_per_vector()` 现在基于缓存中实际存储的张量计算字节数。

### 效果

- 将每个 base block 的重复计算（加权拼接）移到缓存构建阶段一次性完成，搜索热路径无冗余工作。
- 缓存迁移更安全——机器上可能存在多种实验性缓存格式时不会静默出错。

### 验证快照

| 阶段 | 结果文件 |
|------|---------|
| rerank 优化 | ann-bench/turbo-quant/result/20260407_165642/results.json |
| rerank + 近似搜索融合 | ann-bench/turbo-quant/result/20260407_170043/results.json |
| 融合搜索缓存（本次变更后） | ann-bench/turbo-quant/result/20260408_082226/results.json |

代表性结果：bits=4, qjl_dim=1536, rerank=100 → **1095.83 QPS, recall@10=0.9988**

### 保留说明

- 这些变更属于外层 vdb-sandbox 仓库，需要在该仓库中提交。
- 当前已保留在 main 分支的 commit abe189b 中。
- 如果外层仓库被 reset 或 checkout 到其他分支，即使嵌套的 third_party/turboquant-pytorch 仍有本地修改，这些 benchmark 端优化也会丢失。

---

## 二、compressors_v3.py BF16/AMX dtype 优化

### 修改文件

- third_party/turboquant-pytorch/compressors_v3.py

### 背景

`MSECompressor` 和 `TurboQuantV3` 原来硬编码 fp32，旋转/反旋转的 matmul 无法利用 AMX BF16 加速。

### 修改内容

1. **`MSECompressor.__init__`** — 新增 `dtype` 参数，通过 `resolve_torch_dtype()` 解析，传给 `generate_rotation_matrix()` 生成对应精度的旋转矩阵 Pi。
2. **`MSECompressor.compress()`** — `states.reshape(N, D).float()` → `.to(dtype=self.dtype)`，旋转 matmul 跟随 dtype。`codebook.quantize()` 前显式 `.float()` 避免 bucketize 内部重复转换开销。
3. **`MSECompressor.decompress()`** — `vec_norms.float()` → `.to(self.dtype)`，重建 matmul `centroids @ Pi` 跟随 dtype。
4. **`TurboQuantV3.__init__`** — 新增 `dtype` 参数，透传给两个 `MSECompressor`。
5. **import** — 从 `turboquant` 追加导入 `resolve_torch_dtype`。

### 向后兼容

- 不传 `dtype`（默认 `None`）→ 返回 fp32，行为与修改前完全一致。
- 传 `dtype="bf16"` 时旋转/反旋转走 BF16 GEMM → PyTorch oneDNN → AMX tile 路径。

### 性能测试

环境：SPR (Sapphire Rapids), 16 核 (taskset 0-15), PyTorch 2.11+cpu, oneDNN
输入：(B=1, H=32, S=2048, D=128), 65536 向量, bits=4

| D | fp32 压缩 | bf16 压缩 | 压缩加速 | fp32 解压 | bf16 解压 | 解压加速 | fp32 总计 | bf16 总计 | **总加速** |
|---|---|---|---|---|---|---|---|---|---|
| 64 | 15.0 ms | 16.0 ms | 0.93× | 4.9 ms | 7.6 ms | 0.65× | 19.9 ms | 23.6 ms | 0.84× |
| **128** | 40.5 ms | 40.3 ms | 1.01× | 28.3 ms | 18.7 ms | **1.51×** | 68.7 ms | 58.9 ms | **1.17×** |
| 256 | 86.0 ms | 88.4 ms | 0.97× | 55.9 ms | 45.1 ms | 1.24× | 141.9 ms | 133.5 ms | 1.06× |
| 512 | 176.5 ms | 176.7 ms | 1.00× | 126.0 ms | 100.1 ms | 1.26× | 302.5 ms | 276.8 ms | 1.09× |

### 瓶颈分析

- **解压路径** 是纯 matmul（`centroids[idx] @ Pi × norms`），bf16 在 D=128 时加速 1.51×。
- **压缩路径** 被 `torch.bucketize`（约占 60% 耗时）限制，该操作只能跑 fp32。matmul 省下的 2ms 被 bucketize 开销稀释。
- **D=64** 维度过小，matmul 本身不到 1ms，bf16 额外的 dtype 转换开销反而更大。
- 典型 LLM head_dim=128 场景下总体 **1.17× 加速**。

### 准确度

- fp32 与 bf16 重建结果对比：MSE=1.00e-03, cosine_sim=0.9995（对量化场景完全可接受）。

---

## 三、四种 ANN 方法性能对比

### 测试环境

- 数据集：dbpedia-openai-1000k-angular (d=1536, 990k base, 1k queries, k=10, angular/cosine)
- 硬件：SPR, 16 核 (taskset 0-15)
- Faiss 构建：faiss-orig/build (avx512_spr)
- PyTorch：2.11+cpu, oneDNN（AMX BF16 自动 dispatch）

### 测试方法

| 方法 | 索引类型 | 距离计算精度 | 存储精度 |
|------|---------|------------|---------|
| HNSWFlat | Faiss IndexHNSWFlat | fp32 | fp32 |
| HNSWSQ BF16 | Faiss IndexHNSWSQ (QT_bf16) | bf16 | bf16 |
| TurboQuant BF16 | MSE + QJL, PyTorch matmul | bf16 | bf16 搜索矩阵 |
| IVFSQ BF16 | Faiss IndexIVFScalarQuantizer (QT_bf16) | bf16 | bf16 |

### 结果数据位置

- TurboQuant BF16 (AMX)：ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_wide/results.json
- TurboQuant BF16 (AVX512)：ann-bench/turbo-quant/result/20260408_compare_turboquant_bf16_avx512only/results.json
- HNSWFlat：ann-bench/hnsw/result/20260408_compare_hnswflat_wide/results.json
- HNSWSQ BF16：ann-bench/hnsw/result/20260408_compare_hnswsq_bf16_wide/results.json
- IVFSQ BF16：ann-bench/ivf/result/20260408_compare_ivfsq_bf16_wide/results.json

### 各 Recall 水平下的 QPS 对比

| 目标 Recall@10 | HNSWFlat | HNSWSQ BF16 | TurboQuant BF16 | TQ BF16 (AVX512) | AMX/AVX512 | IVFSQ BF16 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| ~0.87 | 28,869 | **35,038** | 1,688 | 355 | 4.8× | 2,649 |
| ~0.93 | **22,412** | 21,129 | 1,685 | 355 | 4.7× | 1,340 |
| ~0.95 | **21,232** | 14,187 | 1,685 | 355 | 4.7× | 1,340 |
| ~0.97 | **16,383** | 3,095 | 1,685 | 355 | 4.7× | 674 |
| ~0.98 | **12,067** | ❌ 不可达 | 1,459 | 346 | 4.2× | 343 |
| ~0.99 | **9,250** | ❌ 不可达 | 1,459 | 346 | 4.2× | 343 |
| ~0.995 | **7,576** | ❌ 不可达 | 1,459 | 334 | 4.4× | 89 |
| ~0.999 | **2,091** | ❌ 不可达 | 1,043 | 258 | 4.0× | ❌ 不可达 |

> **AVX512-only 说明**：通过 `ONEDNN_MAX_CPU_ISA=AVX512_CORE_BF16` 禁用 AMX，仅使用 AVX512 BF16 指令。AMX 在各 recall 水平提供 **4.0–4.8× 加速**（裸 GEMM 加速 5.5×，端到端因非 GEMM 开销稀释）。

### 关键结论

1. **HNSWFlat 全面领先**：在所有 recall 水平上 QPS 最高，从低 recall 的 37K 到 0.999 recall 仍有 2K QPS。
2. **HNSWSQ BF16 有 recall 天花板（~0.967）**：BF16 量化噪声导致图构建质量下降，在 d=1536 数据集上无法突破 0.97。低 recall 区间 QPS 最高（35K）。
3. **TurboQuant BF16 (AMX)**：recall 范围最广（可达 0.999），但 QPS 上限低（~1.9K），适合对 recall 要求极高、内存受限的场景。
4. **TurboQuant BF16 (AVX512-only)**：禁用 AMX 后 QPS 降至 258–355，比 AMX 版慢 4.0–4.8×，证实 AMX 是 TurboQuant BF16 性能的关键加速器。
5. **IVFSQ BF16**：高 recall 区间 QPS 极低（0.995 recall 仅 89 QPS），全面落后。

### 存储效率

| 方法 | 每向量字节 | 0.99 recall QPS |
|------|----------|----------------|
| HNSWFlat (M=48) | ~6,288B | 9,250 |
| HNSWSQ BF16 | ~3,144B | ❌ 不可达 |
| TurboQuant BF16 (b=4,qjl=768) | 674B | 1,459 |
| IVFSQ BF16 | ~3,072B | 343 |

TurboQuant 在存储效率（QPS/GB）上最优，适合内存受限场景。HNSWFlat 在绝对 QPS 上是冠军。