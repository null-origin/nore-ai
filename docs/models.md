# NORE-AI Data Models

This document defines the core data models used by NORE-AI:
- `Event` — atomic unit of input
- `Law` — structural rule reference
- `Register` — grouped events
- `FieldState` — summarized snapshot of a window

Models reside in:
```
src/nore_ai/models/
  event.py
  law.py
  register.py
  field_state.py
```
Each is a simple dataclass with explicit fields and no hidden behavior.

---

# 1. High-Level Relationships

```
Raw JSONL  ──>  Event[]  ──>  Register(s) / FieldState
                  │              ▲
                  │              │
                  └────── Law references (by id)
```

- Events are the only objects read from disk.
- Laws may be referenced by events.
- Registers group events into bundles.
- FieldState summarizes a day or window.

---

# 2. Event
**File:** `nore_ai/models/event.py`  
**Schema:** `schemas/event.schema.json`  
**Input:** `data/events/YYYY-MM-DD.jsonl`

## 2.1 Purpose
Event is the sole on-disk input model. All higher-level objects derive from Events.

## 2.2 Core Fields (Required)
- **id: str** — `s-YYYY-MM-DD-NN` (e.g., `s-2025-11-14-02`)
- **timestamp: datetime** — parsed ISO-8601 with timezone
- **source: str** — e.g., `cnbc`, `reuters`, `pandora`, `user`
- **channel: str** — e.g., `corporate`, `macro`, `sports`, `music`, `user`
- **vectors: list[str]** — structural role markers
- **text: str** — human-readable description
- **meta: dict[str, Any]** — free-form contextual object (must be a dict)

## 2.3 Optional Fields
- `laws: list[str] | None` — e.g., `["FL-11", "OCI-04"]`
- `confidence: float | None`
- `severity: str | None`
- `decision: str | None`
- `status: str | None`
- `runtime: str | None`

Optional fields are omitted if `None` at serialization time.

## 2.4 Serialization
- **Event.from_dict(d)** → Event
- **Event.to_dict()** → dict (JSON‑safe)

---

# 3. Law
**File:** `nore_ai/models/law.py`

## 3.1 Purpose
Represents a structural rule that can be linked to events, registers, or FieldStates.
Examples:
- `FL-11` — Field Law
- `OCI-04` — Origin Contact Interval
- `AXIOM-0` — Core invariant

## 3.2 Fields
- **id: str** — unique identifier
- **name: str** — short label
- **description: str** — explanation of the law
- **meta: dict[str, Any] (optional)** — extended attributes

## 3.3 Relationship to Events
Events may include:
```json
"laws": ["FL-11", "OCI-04"]
```
Law objects are not required during ingestion but become important for interpretation.

---

# 4. Register
**File:** `nore_ai/models/register.py`

## 4.1 Purpose
Groups events into meaningful collections (daily, cycle, thematic, macro, etc.).

## 4.2 Fields
- **id: str** — e.g., `daily-2025-11-16`, `cycle-8-window-1`
- **name: str** — human-readable label
- **events: list[Event]** — ordered event list
- **meta: dict[str, Any] (optional)** — aggregates, tags, summaries

## 4.3 Usage
Registers (planned output containers) will hold:
- daily summaries
- weekly/cycle windows
- OCI windows
- thematic bundles (e.g., *Pentair Binder*, *Macro Inversion #1*)

---

# 5. FieldState
**File:** `nore_ai/models/field_state.py`

## 5.1 Purpose
Represents the state of the field during a specific window (usually a day). Built on top of Events and Registers.

## 5.2 Fields
Typical structure:
- **day: date** — primary date
- **events: list[Event]** — events inside this window
- **summary: dict[str, Any]** — aggregated indicators

Planned summary contents:
- `event_count`
- vector frequencies
- channel counts
- source counts
- `time_window` (first/last timestamps)
- `dominant_vectors`
- `notes`

## 5.3 Usage
Current:
- defined but not produced by pipeline

Planned:
- emitted by extended `run_day_pipeline`
- written to `data/registers/YYYY-MM-DD.field.json`
- used for weekly/cycle/dashboard layers

---

# 6. Errors (Runtime Only)
Validation errors are simple strings (list[str]).

Example:
```
"s-2025-11-14-01: None is not of type 'string'"
```

Future (optional):
```python
@dataclass
class ValidationError:
    event_id: str
    message: str
    path: list[str]
```

Currently: raw strings keep the engine minimal.

---

# 7. Model Interaction in the Pipeline

## 7.1 Current
1. JSONL line → `dict`
2. `dict` → `Event` via `Event.from_dict`
3. schema validation
4. return `(events, errors)` from `run_day_pipeline`

## 7.2 Planned
- Events grouped into `Register`
- FieldState synthesized from events + registers
- FieldState/Register optionally serialized

---

# 8. Summary
- **Event** is the ingest boundary.
- **Law** references structural meaning.
- **Register** groups events.
- **FieldState** summarizes a window.

Models are small, explicit, deterministic — the backbone of all future NORE-AI pipelines.
