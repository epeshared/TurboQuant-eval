from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


def save_result(result: Dict[str, Any], output_dir: str) -> Path:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    backend = result.get("backend", "unknown")
    task = result.get("task", "unknown")
    path = out_dir / f"{backend}_{task}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return path
