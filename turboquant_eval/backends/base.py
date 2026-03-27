from __future__ import annotations

from abc import ABC
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class EvalResult:
    backend: str
    task: str
    status: str = "success"
    schema_version: str = "0.2"
    metrics: Dict[str, float] = field(default_factory=dict)
    per_dataset: Dict[str, float] = field(default_factory=dict)
    artifacts: Dict[str, Any] = field(default_factory=dict)
    run: Dict[str, Any] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class QuantBackend(ABC):
    name: str

    def setup(self, config: Dict[str, Any]) -> None:
        return None

    def run_task(self, task: str, config: Dict[str, Any]) -> EvalResult:
        if task == "kv_fidelity":
            return self.run_kv_fidelity(config)
        if task == "longbench":
            return self.run_longbench(config)
        raise NotImplementedError(f"Task not implemented for backend={self.name}: {task}")

    def run_kv_fidelity(self, config: Dict[str, Any]) -> EvalResult:
        raise NotImplementedError(f"kv_fidelity is not implemented for backend={self.name}")

    def run_longbench(self, config: Dict[str, Any]) -> EvalResult:
        raise NotImplementedError(f"longbench is not implemented for backend={self.name}")
