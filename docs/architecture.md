# NORE-AI Architecture

## 1. Purpose

NORE-AI is a small, deterministic engine that operates on structured events.

- **Input:** JSONL event files (`data/events/YYYY-MM-DD.jsonl`)
- **Core model:** `Event`, `Law`, `Register`, `FieldState`
- **Engine:** `ingest → validate → (cluster → prioritize → summarize)`
- **Interface:** CLI command `nore-ai run-day <config>`

Everything else (NORE Runtime, IL-ARCHON, dashboards) is a client of this engine.

---

## 2. Repository Layout

```text
nore-ai/
  pyproject.toml
  README.md
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
      cli/
  tests/
