# NORE-AI Conventions

This document defines the **global rules** that govern naming, file structure, identifiers, timestamps, sources, channels, vectors, configuration, and code organization across the NORE-AI repository.

These conventions remove ambiguity and ensure deterministic behavior across all pipelines.

---

# 1. Repository Structure

```
nore-ai/
  data/
    events/
      YYYY-MM-DD.jsonl
    registers/
      <register-id>.json
  docs/
    *.md
  schemas/
    event.schema.json
  src/
    nore_ai/
      models/
      engine/
      io/
      cli/
  tests/
  configs/
```

**Rules:**
- Only these directories participate in runtime behavior.
- Deterministic paths only — no dynamic folder creation.
- No symlinks inside `data/`.

---

# 2. Event File Conventions

## 2.1 Naming
Each event file represents **one calendar day**:
```
YYYY-MM-DD.jsonl
```
Examples:
- `2025-11-14.jsonl`
- `2025-12-04.jsonl`
- `2026-01-01.jsonl`

## 2.2 Location
Must live under:
```
data/events/
```

No nested folders.

## 2.3 Format
- UTF-8 JSONL
- One event per line
- Timestamps must include timezone offset

---

# 3. Event ID Conventions

Event IDs follow:
```
s-YYYY-MM-DD-NN
```
Where:
- `s` = structural event
- `YYYY-MM-DD` = event date
- `NN` = zero‑padded sequence (`01`, `02`, ...)

Examples:
- `s-2025-11-14-01`
- `s-2025-11-14-02`
- `s-2025-11-16-07`

**Rules:**
- No gaps in numbering.
- No reuse.
- ID date must match file date.

---

# 4. Timestamp Conventions

All timestamps must:
- use ISO 8601
- include timezone offset
- include seconds (milliseconds optional)

Examples:
```
2025-11-14T10:30:00-05:00
2025-12-04T21:18:43.121-05:00
```

**Rules:**
- Do not use `Z`.
- Never omit the offset.
- Never use naive timestamps.

---

# 5. Vector Conventions

Vector specification is in `docs/vectors.md`. Conventions:
- lowercase
- singular nouns
- represent structural mechanics

Example:
```
["exposure", "retrieval", "collapse", "alignment"]
```

**Rules:**
- no camelCase
- no spaces
- no custom vectors not in `vectors.md`
- order does not matter

---

# 6. Channel Conventions

Channels indicate the event domain.

Canonical channels:
```
corporate
economic
sports
music
social
political
personal
system
```

**Rules:**
- lowercase
- one word
- additions must go through docs update

---

# 7. Source Conventions

`source` reflects the event producer.

Examples:
```
cnbc
reuters
espn
pandora
mlb
personal-note
```

**Rules:**
- lowercase
- hyphens allowed
- must be real origin (internal or external)
- never a URL

---

# 8. Metadata (`meta`) Conventions

`meta` must follow:
- lowercase snake_case keys
- JSON-serializable values
- `tags` must be a list of lowercase strings
- `note` must be a short string
- nesting limited to 2 levels

Example:
```json
"meta": {
  "tags": ["walmart", "leadership", "retail"],
  "window": false,
  "note": "sector recalibration signal"
}
```

---

# 9. Register Conventions

Fully detailed in `docs/registers.md`.

**Summary:**
- deterministic IDs:
  - `daily-YYYY-MM-DD`
  - `weekly-YYYY-WW`
  - `cycle-N-window-K`
- registers store **event IDs only**
- stored under:
```
data/registers/
```

---

# 10. Config Conventions

Config files live under:
```
configs/
```
Naming:
```
<noun>.json
```
Examples:
- `global.json`
- `run-defaults.json`
- `demo.json`

**Rules:**
- no date-based config filenames

---

# 11. CLI Usage Conventions

Preferred direct usage:
```
python run_day.py -e data/events/YYYY-MM-DD.jsonl
```

Using configs:
```
python run-day configs/global.json
```

Rules:
- flags remain short (`-e`, `--events`)
- command names use hyphens (`run-day`)

---

# 12. Coding Conventions

## 12.1 Python
- absolute imports (`from nore_ai.engine...`)
- mandatory type hints
- dataclasses for models
- no global runtime state
- no singletons

## 12.2 Tests
- filenames start with `test_`
- use `unittest`

## 12.3 Schemas
- stored in `schemas/`
- JSON Schema Draft 2020‑12

---

# 13. Determinism Rules

To maintain predictability:
- no randomness
- no time-of-run generation
- no environment-based branching
- no external APIs
- no network access
- no parallelism inside pipelines

All outputs must be pure functions of:
```
events file + schema + pipeline code
```

---

# 14. Summary

These conventions standardize:
- filenames
- IDs
- timestamps
- metadata
- vectors
- registers
- configs
- source/channel taxonomy
- code organization

Adherence guarantees that every output — from event ingestion to FieldState — is reproducible exactly from the source files and engine logic.
