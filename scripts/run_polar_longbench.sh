#!/usr/bin/env bash
set -euo pipefail

python -m turboquant_eval.runners.run_backend \
  --backend polar_official \
  --task longbench \
  --config configs/longbench_polar.yaml
