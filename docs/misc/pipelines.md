# NORE-AI Pipelines

This document describes the pipelines built on top of the NORE-AI engine. Pipelines define how raw JSONL event data is transformed into structured outputs.

Current implementations are minimal and deterministic; future extensions will maintain determinism while adding clustering, prioritization, and state summarization.

---

## 1. Daily Pipeline (`run_day_pipeline`)

The daily pipeline is the core operational unit of NORE-AI.

### Entry Function
`nore_ai.engine.pipeline.run_day_pipeline(config)`

### Invoked By
- `run_day.py` (`python run_day.py -e data/events/YYYY-MM-DD.jsonl`)
- Future runners (weekly, cycle-level, dashboard extraction)

---

## 1.1 Inputs

The pipeline expects a config dictionary:

```json
{
  "events_path": "data/events/YYYY-MM-DD.jsonl",
  "event_schema": "schemas/event.schema.json",
  "validate": true
}
```

When running through `run_day.py`, this config is generated automatically.

---

## 1.2 Steps

### Step 1 — Ingest
Loads a JSONL file and converts each line into an in-memory `Event` instance.

**Module:** `nore_ai/engine/ingest.py`

### Step 2 — Validate
Validates each event against the JSON Schema defined in:

**Schema:** `schemas/event.schema.json`

Validation returns:
- a list of valid `Event` instances
- a list of error strings describing failures

**Module:** `nore_ai/engine/validate.py`

### Step 3 — Return Results
The function currently returns:
- `events: list[Event]`
- `errors: list[str]`

Future versions will return a `FieldState` along with raw events.

---

## 1.3 Outputs

### Current Output (Console)
```
[nore-ai] run-day completed
  valid events     : N
  validation errors: M
  first few errors:
    - ...
```

### Returned Python Objects
- `events`: parsed and validated
- `errors`: any validation issues

### Planned Output
- daily register files under `data/registers/YYYY-MM-DD.json`
- `FieldState` snapshot (structured summary of the day)
- clustered and prioritized event groups

---

## 2. Weekly Pipeline (Planned)

A weekly pipeline will:
- collect all `data/events/YYYY-MM-DD.jsonl` files within a 7-day window
- run each day through the daily pipeline
- aggregate results into:
  - a weekly register
  - a weekly `FieldState`
  - weekly cluster/prioritization metrics

**Location:** `nore_ai/engine/pipelines/weekly.py`

---

## 3. Cycle Pipeline (Planned)

Cycle-level pipelines support longer structural windows (e.g., OCI windows, Cycle 8 ignition ranges, 42-day inversions).

They will:
- ingest a specified date range
- merge events
- derive:
  - cycle registers
  - structural laws triggered
  - pattern summaries
  - collapse → retrieval → return mappings

**Target Module:** `nore_ai/engine/pipelines/cycle.py`

---

## 4. Dashboard Pipeline (Future)

A higher-level pipeline will produce dashboard-ready outputs:
- aggregate metrics
- vector-frequency heatmaps
- structural change detection
- real-time anomaly surfaces

This layer consumes deterministic output but does not alter core logic.

---

## 5. Design Principles

All NORE-AI pipelines follow the same constraints:

### Deterministic
Given identical input files, the pipeline must always produce the same output.

### Minimal
No hidden state; no external dependencies beyond the repository.

### Composable
Daily pipeline → weekly → cycle → dashboard.

### Explicit
Every transformation is intentional and directly inspectable in code.

---

## 6. Summary

The daily pipeline is implemented and functional.

Weekly, cycle, and dashboard pipelines are planned extensions that will follow the same architectural principles.

`run_day.py` remains the recommended entrypoint for daily analysis without package installation.

