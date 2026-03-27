from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Dict

from .base import EvalResult, QuantBackend


class PolarOfficialBackend(QuantBackend):
    name = "polar_official"

    def setup(self, config: Dict[str, Any]) -> None:
        repo_dir = Path(config.get("repo_dir", "third_party/PolarQuant"))
        if not repo_dir.exists():
            raise FileNotFoundError(
                f"PolarQuant repo not found at {repo_dir}. Run scripts/setup_external.sh first."
            )

    def run_kv_fidelity(self, config: Dict[str, Any]) -> EvalResult:
        raise NotImplementedError(
            "kv_fidelity is not wired for polar_official yet. "
            "Use this backend first for upstream-script-based tasks such as long-context evaluation."
        )

    def run_external(self, script: str, extra_args: list[str] | None = None, cwd: str | None = None) -> EvalResult:
        cmd = ["python", script] + (extra_args or [])
        proc = subprocess.run(
            cmd,
            cwd=cwd or "third_party/PolarQuant",
            capture_output=True,
            text=True,
            check=True,
        )
        return EvalResult(
            backend=self.name,
            task=script,
            metrics={},
            artifacts={"stdout": proc.stdout, "stderr": proc.stderr},
        )
