#!/usr/bin/env bash
set -euo pipefail

python -m turboquant_eval.runners.run_backend \
  --backend turboquant_ref \
  --task kv_fidelity \
  --config configs/kv_fidelity.yaml
