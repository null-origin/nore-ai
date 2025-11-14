# NORE-AI Architecture

## 1. Purpose

NORE-AI is a deterministic event-processing engine that consumes structured JSONL event files and returns validated, typed `Event` objects and errors.

This engine is intentionally minimal:

* **Input:** JSONL files under `data/events/YYYY-MM-DD.jsonl`
* **Models:** `Event`, `Law`, `Register`, `FieldState`
* **Engine Pipeline:** `ingest → validate → (cluster → prioritize → summarize)`

All higher-level components (NORE Runtime, IL-ARCHON, dashboards, registers) operate as clients of this core engine.

---

## 2. Repository Layout

```
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
      cli/
  tests/
```

### Key Directories

* **src/nore_ai/** – Python package containing the engine, models, and schema-based validation.
* **schemas/** – JSON Schema definitions for data on disk.
* **data/events/** – Daily raw event logs (`*.jsonl`).
* **data/registers/** – Future output directory for daily/weekly structural summaries.
* **run_day.py** – Recommended entrypoint for running the pipeline.
* **tests/** – Unit tests validating the engine and data contracts.

---

## 3. Data Model

### 3.1 Event

Defined in:

* `schemas/event.schema.json`
* `nore_ai/models/event.py`

**Required fields:**

* `id: str`
* `timestamp: str` (ISO 8601 with timezone)
* `source: str`
* `channel: str`
* `vectors: list[str]`
* `text: str`
* `meta: object` (must be a JSON object)

**Optional fields:**

* `laws: list[str]`
* `confidence: float`
* `severity: str`
* `decision: str`
* `status: str`
* `runtime: str`

### 3.2 Law

Defined in `nore_ai/models/law.py`.

Represents named structural laws (e.g., FL-11, OCI-04):

* `id`
* `name`
* `description`
* `meta`

### 3.3 Register

Defined in `nore_ai/models/register.py`.

Groups events into structured collections:

* `id`
* `name`
* `events: list[Event]`

### 3.4 FieldState

Defined in `nore_ai/models/field_state.py`.

Represents a distilled snapshot of a day:

* `day`
* `events: list[Event]`
* `summary: dict`

Not yet implemented in the main pipeline.

---

## 4. Engine

Engine modules live under `src/nore_ai/engine/`.

### 4.1 ingest.py

Loads JSONL data → produces raw `Event` instances.

### 4.2 validate.py

Runs JSON Schema validation using `schemas/event.schema.json`.

Returns:

* `list[Event]` (valid events)
* `list[str]` (validation errors)

### 4.3 pipeline.py

Top-level day pipeline.

**Current functionality:**

* Read events
* Validate events
* Return `(events, errors)`

**Planned extensions:**

* Cluster events
* Assign priority
* Derive daily `FieldState`
* Write register outputs to `data/registers/`

---

## 5. Running the Engine (Recommended)

Use the standalone script **run_day.py**.

This script:

* Adds `src/` to `sys.path`
* Calls `run_day_pipeline()`
* Loads schema automatically
* Requires no installation

### Usage

```bash
python run_day.py -e data/events/2025-11-16.jsonl
python run_day.py --events data/events/2025-12-04.jsonl
python run_day.py --events data/events/2026-01-01.jsonl
```

### Output

```yaml
[nore-ai] run-day completed
  valid events     : N
  validation errors: M
  first few errors:
    - ...
```

This workflow supports the iterative development pattern:
**edit → add events → run → validate** without managing environment state.

---

## 6. Testing

Tests are located in `tests/`.

* `tests/test_event_model.py` – Validates Event model + JSON round-trip.
* `tests/test_pipeline.py` – Validates ingest + validation end-to-end.

Run all tests:

```bash
python -m unittest
```

---

## 7. Future Extensions

Planned enhancements:

* `cluster.py` – rule-based grouping of events
* `prioritize.py` – score + rank events and clusters
* `summary.py` – generate daily `FieldState`
* Write daily registers to `data/registers/YYYY-MM-DD.json`
* Weekly/monthly aggregation pipelines

All future modules will integrate into the deterministic pipeline structure.
