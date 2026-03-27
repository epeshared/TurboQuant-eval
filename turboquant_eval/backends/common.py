from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple


def run_command(command: Sequence[str], cwd: str | None = None) -> Dict[str, Any]:
    start = time.time()
    proc = subprocess.run(
        list(command),
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    elapsed = time.time() - start
    return {
        "command": list(command),
        "cwd": cwd,
        "returncode": proc.returncode,
        "elapsed_seconds": round(elapsed, 4),
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def save_command_logs(output_dir: str, backend: str, task: str, stdout: str, stderr: str) -> Dict[str, str]:
    log_dir = Path(output_dir) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    stdout_path = log_dir / f"{backend}_{task}.stdout.log"
    stderr_path = log_dir / f"{backend}_{task}.stderr.log"

    stdout_path.write_text(stdout or "", encoding="utf-8")
    stderr_path.write_text(stderr or "", encoding="utf-8")

    return {
        "stdout_log": str(stdout_path),
        "stderr_log": str(stderr_path),
    }


def normalize_percent_score(score: float) -> float:
    if 0.0 <= score <= 1.0:
        return round(score * 100.0, 2)
    return round(score, 2)


def _finalize_longbench_metrics(per_dataset: Dict[str, float], extra_metrics: Dict[str, float] | None = None) -> Dict[str, float]:
    metrics: Dict[str, float] = dict(extra_metrics or {})
    metrics["longbench_dataset_count"] = float(len(per_dataset))
    if per_dataset:
        metrics["longbench_avg_score"] = round(sum(per_dataset.values()) / len(per_dataset), 2)
    return metrics


def parse_qjl_longbench_stdout(stdout: str) -> Tuple[Dict[str, float], Dict[str, float], List[str]]:
    per_dataset: Dict[str, float] = {}
    notes: List[str] = []
    runtime_seconds = None

    for line in stdout.splitlines():
        m = re.search(r"Average score for dataset\s+(.+?):\s+([-+0-9.eE]+)", line)
        if m:
            dataset = m.group(1).strip()
            score = normalize_percent_score(float(m.group(2)))
            per_dataset[dataset] = score
            continue

        m = re.search(r"Total evaluation time:\s+([0-9.]+)\s+seconds", line)
        if m:
            runtime_seconds = float(m.group(1))

    if not per_dataset:
        notes.append("No per-dataset score was parsed from QJL stdout.")

    metrics = _finalize_longbench_metrics(
        per_dataset,
        {"runtime_seconds": runtime_seconds} if runtime_seconds is not None else {},
    )
    return per_dataset, metrics, notes


def parse_polar_longbench_stdout(stdout: str) -> Tuple[Dict[str, float], Dict[str, float], List[str]]:
    per_dataset: Dict[str, float] = {}
    notes: List[str] = []
    current_dataset = None

    for line in stdout.splitlines():
        m = re.search(r"Report\s+(.+?)\s+results:", line)
        if m:
            current_dataset = m.group(1).strip()
            continue

        m = re.search(r"(?:em\s+)?score is\s+([0-9.]+)", line)
        if m and current_dataset:
            per_dataset[current_dataset] = round(float(m.group(1)), 2)
            current_dataset = None

    if not per_dataset:
        notes.append("No per-dataset score was parsed from PolarQuant stdout.")

    metrics = _finalize_longbench_metrics(per_dataset)
    return per_dataset, metrics, notes


def parse_json_result_file(path: str) -> Tuple[Dict[str, float], Dict[str, float], List[str]]:
    file_path = Path(path)
    if not file_path.exists():
        return {}, {}, [f"Result JSON not found: {path}"]

    data = json.loads(file_path.read_text(encoding="utf-8"))
    per_dataset: Dict[str, float] = {}
    for key, value in data.items():
        if isinstance(value, dict):
            continue
        if isinstance(value, (int, float)):
            per_dataset[str(key)] = normalize_percent_score(float(value))

    notes: List[str] = []
    if not per_dataset:
        notes.append(f"No scalar per-dataset scores found in {path}")

    metrics = _finalize_longbench_metrics(per_dataset)
    return per_dataset, metrics, notes
