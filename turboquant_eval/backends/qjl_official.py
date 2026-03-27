from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from .base import EvalResult, QuantBackend
from .common import parse_qjl_longbench_stdout, run_command, save_command_logs


class QJLOfficialBackend(QuantBackend):
    name = "qjl_official"

    def setup(self, config: Dict[str, Any]) -> None:
        repo_dir = Path(config.get("repo_dir", "third_party/QJL"))
        if not repo_dir.exists():
            raise FileNotFoundError(
                f"QJL repo not found at {repo_dir}. Run scripts/setup_external.sh first."
            )

    def run_kv_fidelity(self, config: Dict[str, Any]) -> EvalResult:
        raise NotImplementedError(
            "kv_fidelity is not wired for qjl_official yet. Use longbench first."
        )

    def run_longbench(self, config: Dict[str, Any]) -> EvalResult:
        repo_dir = str(config.get("repo_dir", "third_party/QJL"))
        output_dir = str(config.get("output_dir", "results"))
        cwd = str(config.get("cwd", repo_dir))

        command = self._build_command(config)
        run_info = run_command(command, cwd=cwd)
        artifacts = save_command_logs(output_dir, self.name, "longbench", run_info["stdout"], run_info["stderr"])

        per_dataset, metrics, notes = parse_qjl_longbench_stdout(run_info["stdout"])
        if run_info["returncode"] != 0:
            notes.append("QJL command exited with a non-zero return code.")
            notes.append("If upstream argument handling fails, override `command` in the YAML config with your patched launcher.")

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
        return [
            "python",
            str(config.get("script", "run_longbench.py")),
            "--model_name",
            str(config.get("model_name", "lmsys/longchat-7b-v1.5-32k")),
            "--dtype",
            str(config.get("dtype", "float16")),
            "--key_quantization_bits",
            str(config.get("key_quantization_bits", 256)),
            "--key_quantization_bits_initial_layers",
            str(config.get("key_quantization_bits_initial_layers", 512)),
            "--initial_layers_count",
            str(config.get("initial_layers_count", 15)),
            "--outlier_count_general",
            str(config.get("outlier_count_general", 8)),
            "--outlier_count_initial_layers",
            str(config.get("outlier_count_initial_layers", 8)),
            "--value_quantization_bits",
            str(config.get("value_quantization_bits", 2)),
            "--group_size",
            str(config.get("group_size", 32)),
            "--buffer_size",
            str(config.get("buffer_size", 128)),
            "--seed",
            str(config.get("seed", 42)),
            "--dataset_name",
            str(config.get("dataset_name", "narrativeqa")),
            "--n_data",
            str(config.get("n_data", 150)),
        ]
