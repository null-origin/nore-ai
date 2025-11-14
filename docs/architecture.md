# NORE-AI Architecture

## 1. Purpose

NORE-AI is a deterministic event-processing engine.  
It consumes structured JSONL event files and returns validated, typed `Event` objects and errors.

This engine is deliberately minimal:

- **Input:** JSONL files under `data/events/YYYY-MM-DD.jsonl`
- **Models:** `Event`, `Law`, `Register`, `FieldState`
- **Engine pipeline:**  
  `ingest → validate → (cluster → prioritize → summarize)`

Everything else (NORE Runtime, IL-ARCHON, dashboards, registers) is a client of this core engine.

---

## 2. Repository Layout

```text
nore-ai/
  pyproject.toml
  README.md
  run_day.py
  docs/
    architecture.md
  schemas/
    event.schema.json
  data/
    events/
    registers/
  src/
    nore_ai/
      models/
      engine/
      io/
      cli/        (kept for future use, optional)
  tests/
```
Key Directories

src/nore_ai/ – Python package containing the engine, models, and schema-based validation.

schemas/ – JSON Schema definitions for data on disk.

data/events/ – Daily raw event logs (*.jsonl).

data/registers/ – Future output directory for daily/weekly structural summaries.

run_day.py – The recommended entrypoint for running the pipeline (no install required).

tests/ – Unit tests validating the engine and data contracts.
