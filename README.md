# TurboQuant-eval

A unified evaluation scaffold for reproducing and comparing three related compression paths:

- **QJL official** (`amirzandieh/QJL`)
- **PolarQuant official** (`ericshwu/PolarQuant`)
- **TurboQuant community reference** (`tonbistudio/turboquant-pytorch`)

This repo is intentionally structured as an **evaluation shell**, not a forced code merge. The goal is to keep
each upstream implementation isolated, while standardizing:

- task entrypoints
- metrics collection
- result schema
- comparison workflow

## Design

```text
TurboQuant-eval/
├── configs/
├── scripts/
├── third_party/                 # external repos are placed here manually
├── turboquant_eval/
│   ├── backends/
│   ├── results.py
│   ├── runners/
│   └── tasks/
└── results/
```

## What is included now

- backend abstraction (`QuantBackend`)
- adapter backends for:
  - `qjl_official`
  - `polar_official`
  - `turboquant_ref`
- a runnable synthetic task: `kv_fidelity`
- LongBench wrappers for:
  - `qjl_official`
  - `polar_official`
- unified result schema and JSON output
- raw stdout / stderr log persistence under `results/logs/`
- helper scripts to clone external repos into `third_party/`

## Result schema

Each run writes a normalized JSON object with the following top-level fields:

```json
{
  "schema_version": "0.2",
  "backend": "qjl_official",
  "task": "longbench",
  "status": "success",
  "metrics": {
    "longbench_avg_score": 31.42,
    "longbench_dataset_count": 1,
    "runtime_seconds": 123.45
  },
  "per_dataset": {
    "narrativeqa": 31.42
  },
  "artifacts": {
    "stdout_log": "results/logs/qjl_official_longbench.stdout.log",
    "stderr_log": "results/logs/qjl_official_longbench.stderr.log"
  },
  "run": {
    "command": ["python", "run_longbench.py", "..."],
    "cwd": "third_party/QJL",
    "returncode": 0,
    "elapsed_seconds": 123.45
  },
  "config": {"...": "..."},
  "notes": []
}
```

## Quick start

### 1. Create a Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Clone upstream repos into `third_party/`

```bash
bash scripts/setup_external.sh
```

### 3. Run the synthetic KV fidelity check with the community TurboQuant reference

```bash
python -m turboquant_eval.runners.run_backend \
  --backend turboquant_ref \
  --task kv_fidelity \
  --config configs/kv_fidelity.yaml
```

### 4. Run QJL official LongBench through the normalized wrapper

```bash
python -m turboquant_eval.runners.run_backend \
  --backend qjl_official \
  --task longbench \
  --config configs/longbench_qjl.yaml
```

### 5. Run PolarQuant official LongBench through the normalized wrapper

```bash
python -m turboquant_eval.runners.run_backend \
  --backend polar_official \
  --task longbench \
  --config configs/longbench_polar.yaml
```

## Notes on the official wrappers

### QJL official

The QJL backend now supports `longbench` directly and parses QJL stdout into the unified result schema. If the upstream
script needs local patching, you can override the full launch command through `command:` in the YAML config.

### PolarQuant official

The default Polar wrapper runs the upstream `test4long.py`-style workflow and parses its stdout. Because the official
PolarQuant script often contains hardcoded model/data/output paths, the wrapper also supports `command:` override in
the YAML config so you can point it at your own patched launcher script.

## Included config examples

- `configs/kv_fidelity.yaml`
- `configs/longbench_qjl.yaml`
- `configs/longbench_polar.yaml`

## Planned next steps

- add Needle-in-a-Haystack support
- add vector-search recall / memory benchmarks
- add unified aggregation across multiple LongBench runs
- optionally switch `third_party/` setup to git submodules later
