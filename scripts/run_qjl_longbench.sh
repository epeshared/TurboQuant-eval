#!/usr/bin/env bash
set -euo pipefail

python -m turboquant_eval.runners.run_backend \
  --backend qjl_official \
  --task longbench \
  --config configs/longbench_qjl.yaml
