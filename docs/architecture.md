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
