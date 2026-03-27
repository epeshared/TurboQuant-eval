from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from .base import EvalResult, QuantBackend
from .common import parse_polar_longbench_stdout, run_command, save_command_logs


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
            "kv_fidelity is not wired for polar_official yet. Use longbench first."
        )

    def run_longbench(self, config: Dict[str, Any]) -> EvalResult:
        repo_dir = str(config.get("repo_dir", "third_party/PolarQuant"))
        output_dir = str(config.get("output_dir", "results"))
        cwd = str(config.get("cwd", repo_dir))

        command = self._build_command(config)
        run_info = run_command(command, cwd=cwd)
        artifacts = save_command_logs(output_dir, self.name, "longbench", run_info["stdout"], run_info["stderr"])

        per_dataset, metrics, notes = parse_polar_longbench_stdout(run_info["stdout"])
        if run_info["returncode"] != 0:
            notes.append("PolarQuant command exited with a non-zero return code.")
        if not config.get("command"):
            notes.append("Default PolarQuant wrapper uses the upstream script directly. You may want to override `command` with a patched launcher because upstream paths are often hardcoded.")

        return EvalResult(
            backend=self.name,
            task="longbench",
            status="success" if run_info["returncode"] == 0 else "failed",
            metrics=metrics,
            per_dataset=per_dataset,
            artifacts=artifacts,
            run={k: v for k, v in run_info.items() if k not in {"stdout", "stderr"}},
            config=dict(config),
            notes=notes,
        )

    def _build_command(self, config: Dict[str, Any]) -> List[str]:
        if config.get("command"):
            return [str(x) for x in config["command"]]
        return ["python", str(config.get("script", "test4long.py"))]
