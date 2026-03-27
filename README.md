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
│   ├── runners/
│   └── tasks/
└── results/
```

## What is included in this bootstrap

- backend abstraction (`QuantBackend`)
- adapter skeletons for QJL official / PolarQuant official / TurboQuant reference
- a first runnable task: `kv_fidelity`
- a simple runner CLI
- helper scripts to clone external repos into `third_party/`

## What is not included yet

This bootstrap **does not vendor upstream code automatically** and does not pretend that all backends are already
feature-complete. In particular:

- `qjl_official` currently shells out to an external script you provide via config
- `polar_official` currently shells out to an external script you provide via config
- `turboquant_ref` is the first backend with an in-process implementation path

That keeps the scaffold honest and easy to iterate on.

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

If you already have your own forks, edit the script first.

### 3. Run the synthetic KV fidelity check with the community TurboQuant reference

```bash
python -m turboquant_eval.runners.run_backend \
  --backend turboquant_ref \
  --task kv_fidelity \
  --config configs/kv_fidelity.yaml
```

Results are written to `results/`.

## Planned next steps

- add LongBench runner normalization
- add Needle-in-a-Haystack support
- add vector-search recall / memory benchmarks
- add unified parsing for upstream logs
- optionally switch third-party setup to git submodules later
