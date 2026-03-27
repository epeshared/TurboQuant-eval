from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class EvalResult:
    backend: str
    task: str
    metrics: Dict[str, float]
    artifacts: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class QuantBackend(ABC):
    name: str

    def setup(self, config: Dict[str, Any]) -> None:
        return None

    def run_task(self, task: str, config: Dict[str, Any]) -> EvalResult:
        if task == "kv_fidelity":
            return self.run_kv_fidelity(config)
        raise NotImplementedError(f"Task not implemented for backend={self.name}: {task}")

    @abstractmethod
    def run_kv_fidelity(self, config: Dict[str, Any]) -> EvalResult:
        raise NotImplementedError
