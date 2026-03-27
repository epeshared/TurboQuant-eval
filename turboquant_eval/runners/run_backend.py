from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

import yaml

from turboquant_eval.backends.polar_official import PolarOfficialBackend
from turboquant_eval.backends.qjl_official import QJLOfficialBackend
from turboquant_eval.backends.turboquant_ref import TurboQuantRefBackend
from turboquant_eval.tasks.kv_fidelity import save_result


BACKENDS = {
    "qjl_official": QJLOfficialBackend,
    "polar_official": PolarOfficialBackend,
    "turboquant_ref": TurboQuantRefBackend,
}


def load_config(path: str) -> Dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a TurboQuant-eval backend task.")
    parser.add_argument("--backend", required=True, choices=sorted(BACKENDS.keys()))
    parser.add_argument("--task", required=True)
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    backend = BACKENDS[args.backend]()
    backend.setup(config)
    result = backend.run_task(args.task, config)

    output_dir = config.get("output_dir", "results")
    result_path = save_result(result.to_dict(), output_dir)

    print(f"[done] wrote {result_path}")


if __name__ == "__main__":
    main()
