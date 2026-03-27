#!/usr/bin/env bash
set -euo pipefail

mkdir -p third_party

clone_if_missing () {
  local url="$1"
  local dst="$2"
  if [ -d "$dst/.git" ]; then
    echo "[skip] $dst already exists"
  else
    git clone "$url" "$dst"
  fi
}

clone_if_missing https://github.com/amirzandieh/QJL.git third_party/QJL
clone_if_missing https://github.com/ericshwu/PolarQuant.git third_party/PolarQuant
clone_if_missing https://github.com/tonbistudio/turboquant-pytorch.git third_party/turboquant-pytorch

echo "Done. External repositories are under third_party/."
