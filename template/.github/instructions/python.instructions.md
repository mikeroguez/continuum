---
applyTo: "**/*.py"
---

Python changes must preserve the standard-library-only runtime of Continuum.
Keep the mirrored implementation under `template/tools/_continuum/` aligned
with the root implementation when the change affects the CLI. Add or update
`unittest` coverage under `tests/` and run the documented test command.

