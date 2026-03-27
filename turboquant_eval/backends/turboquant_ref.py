from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any, Dict

import torch

from .base import EvalResult, QuantBackend


def _load_turboquant_module(repo_dir: str = "third_party/turboquant-pytorch"):
    repo_path = Path(repo_dir)
    module_path = repo_path / "turboquant.py"
    if not module_path.exists():
        raise FileNotFoundError(
            f"TurboQuant reference file not found at {module_path}. "
            "Run scripts/setup_external.sh first."
        )

    spec = importlib.util.spec_from_file_location("turboquant_ref_impl", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TurboQuantRefBackend(QuantBackend):
    name = "turboquant_ref"

    def setup(self, config: Dict[str, Any]) -> None:
        _load_turboquant_module(config.get("repo_dir", "third_party/turboquant-pytorch"))

    def run_kv_fidelity(self, config: Dict[str, Any]) -> EvalResult:
        module = _load_turboquant_module(config.get("repo_dir", "third_party/turboquant-pytorch"))

        device = config.get("device", "cpu")
        dtype_name = config.get("dtype", "float32")
        dtype = getattr(torch, dtype_name)
        dim = int(config.get("dim", 128))
        num_queries = int(config.get("num_queries", 16))
        num_keys = int(config.get("num_keys", 64))
        bits = int(config.get("bits", 3))
        qjl_dim = int(config.get("qjl_dim", dim))
        seed = int(config.get("seed", 42))

        torch.manual_seed(seed)

        queries = torch.randn(num_queries, dim, device=device, dtype=dtype)
        keys = torch.randn(num_keys, dim, device=device, dtype=dtype)

        quant = module.TurboQuantProd(d=dim, bits=bits, qjl_dim=qjl_dim, device=device)
        compressed = quant.quantize(keys)

        gt = queries @ keys.T
        est_rows = []
        for i in range(num_queries):
            q = queries[i].unsqueeze(0)
            est_rows.append(quant.inner_product(q, compressed))
        est = torch.cat(est_rows, dim=0).reshape_as(gt)

        err = est - gt
        mse = torch.mean(err ** 2).item()
        mae = torch.mean(err.abs()).item()
        cosine = torch.nn.functional.cosine_similarity(
            gt.flatten().unsqueeze(0), est.flatten().unsqueeze(0)
        ).item()

        memory = {}
        if hasattr(module, "TurboQuantKVCache"):
            cache = module.TurboQuantKVCache(d_key=dim, d_value=dim, bits=bits, device=device)
            cache.append(keys, keys)
            memory = cache.memory_usage_bits()

        return EvalResult(
            backend=self.name,
            task="kv_fidelity",
            metrics={
                "mse": float(mse),
                "mae": float(mae),
                "cosine": float(cosine),
                **{k: float(v) for k, v in memory.items()},
            },
            artifacts={
                "shape_gt": list(gt.shape),
                "shape_est": list(est.shape),
            },
        )
