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

Key Directories

src/nore_ai/ – Python package containing the engine, models, and schema-based validation.

schemas/ – JSON Schema definitions for data on disk.

data/events/ – Daily raw event logs (*.jsonl).

data/registers/ – Future output directory for daily/weekly structural summaries.

run_day.py – The recommended entrypoint for running the pipeline (no install required).

tests/ – Unit tests validating the engine and data contracts.

3. Data Model
3.1 Event

Defined both in:

schemas/event.schema.json

nore_ai/models/event.py

Required fields:

id: str

timestamp: str (ISO 8601, includes timezone offset)

source: str

channel: str

vectors: list[str]

text: str

meta: object (free-form but must be an object)

Optional fields (used by runtime, not required by schema):

laws: list[str]

confidence: float

severity: str

decision: str

status: str

runtime: str

3.2 Law

Defined in nore_ai/models/law.py.

Represents named structural laws (e.g., FL-11, OCI-04):

id

name

description

meta

3.3 Register

Defined in nore_ai/models/register.py.

Groups events into structured collections:

id

name

events: list[Event]

3.4 FieldState

Defined in nore_ai/models/field_state.py.

Represents a distilled snapshot of a day:

day

events: list[Event]

summary: dict

Not yet fully implemented in the pipeline—reserved for future expansion.

4. Engine

Engine modules exist under src/nore_ai/engine:

4.1 ingest.py

Loads JSONL data → produces raw Event instances.

4.2 validate.py

Runs JSON Schema validation against schemas/event.schema.json.

Returns:

list[Event] (valid)

list[str] (errors)

4.3 pipeline.py

The top-level day pipeline.

Current functionality:

Read events

Validate events

Return (events, errors)

Planned extensions:

cluster events

assign priority

derive daily FieldState

write output registers to data/registers/

5. Running the Engine (Recommended Method)

Rather than installing the package or relying on a CLI entrypoint, the simplest and most stable invocation is the provided script:

run_day.py

This script:

Automatically adds src/ to sys.path

Calls run_day_pipeline()

Loads schema automatically

Requires no installation

Usage:
python run_day.py -e data/events/2025-11-16.jsonl
python run_day.py --events data/events/2025-12-04.jsonl
python run_day.py --events data/events/2026-01-01.jsonl

Output:
[nore-ai] run-day completed
  valid events     : N
  validation errors: M
  first few errors:
    - ...


This flow is optimized for NORE-AI’s real-world use:
edit → add events → run → validate without worrying about environment state.

6. Testing

Tests live in tests/:

tests/test_event_model.py – validates the Event class and JSON round-trip behavior.

tests/test_pipeline.py – ensures pipeline ingest + validation logic works end-to-end.

Run all tests:

python -m unittest

7. Future Extensions

Planned additions:

cluster.py – rule-based grouping of events

prioritize.py – score + rank events and clusters

summary.py – produce FieldState per day

output of daily registers to data/registers/YYYY-MM-DD.json

weekly/monthly aggregate pipelines

These modules will plug directly into the existing pipeline and follow the same deterministic structure.
