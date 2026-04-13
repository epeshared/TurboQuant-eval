# Frozen Benchmark Sources

This directory contains immutable benchmark artifacts that back wiki comparison pages.

Conventions:

- Preserve the original directory semantics when practical.
- Keep captured artifacts read-only after ingest.
- If a benchmark is rerun, add a new dated directory or file instead of overwriting an old result.

Current scope:

- `ann-bench/` contains the key `results.json` snapshots used in the TurboQuant ANN comparison work.