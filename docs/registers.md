# NORE-AI Registers · Register Architecture & Output Specification

Registers are structured collections of events — the intermediate layer between raw `Event` data and higher‑order structures such as `FieldState`, weekly/cycle windows, and dashboards.

They are not required for ingestion or validation but become essential once grouping, summarization, and structural interpretation begins.

---

# 1. Purpose of Registers

Registers answer the question:

**“What happened in this window, and how do the events relate structurally?”**

Where an **Event** is an individual unit, a **Register** is a container of structurally related events.

Registers enable:
- daily rollups
- weekly or cycle‑window summaries
- vector‑frequency analysis
- structural arc detection
- dashboard grouping
- alignment between NORE Runtime and NORE‑AI

---

# 2. Relationship to Other Models

```
Event[]  →  Register  →  FieldState  →  Weekly/Cycle Structures
```

- **Events** are raw inputs.
- **Registers** group events.
- **FieldState** summarizes one or more registers.
- **Weekly/Cycle structures** merge multiple registers into larger windows.

Registers assume all events are already validated.

---

# 3. Register Model Structure

**File:** `src/nore_ai/models/register.py`

```python
@dataclass
class Register:
    id: str
    name: str
    events: list[Event]
    meta: dict[str, Any] = field(default_factory=dict)
```

### Field Breakdown
| Field   | Type          | Purpose |
|---------|---------------|---------|
| `id`    | string        | deterministic identifier |
| `name`  | string        | readable summary label |
| `events`| list[Event]   | events belonging to this register |
| `meta`  | object        | structured extras (vector counts, tags, notes) |

`meta` is optional but key for FieldState.

---

# 4. Register Naming Conventions

Registers must follow deterministic naming patterns.

## 4.1 Daily Register
```
daily-YYYY-MM-DD
```
Example: `daily-2025-11-16`

## 4.2 Weekly Register
```
weekly-YYYY-WW
```
Where `WW` is the ISO week number.

Example: `weekly-2025-47`

## 4.3 Cycle Window Register
```
cycle-N-window-K
```
Where:
- `N` = cycle number
- `K` = window index

Example: `cycle-8-window-1`

## 4.4 Thematic Register
```
theme-<slug>
```
Examples:
- `theme-pentair-binder`
- `theme-origin-retrieval`
- `theme-inversion-cluster`

---

# 5. Register Output Format

Registers will be written as JSON in:
```
data/registers/
```
Example:
```
data/registers/2025-11-16.register.json
```

## 5.1 Example Output
```json
{
  "id": "daily-2025-11-16",
  "name": "Daily Register — 2025-11-16",
  "events": [
    "s-2025-11-16-01",
    "s-2025-11-16-02",
    "s-2025-11-16-03"
  ],
  "meta": {
    "event_count": 3,
    "vectors": {
      "exposure": 1,
      "retrieval": 1,
      "collapse": 1
    },
    "channels": ["corporate", "sports"],
    "sources": ["cnbc", "espn"],
    "time_window": {
      "first": "2025-11-16T08:24:00-05:00",
      "last": "2025-11-16T21:03:00-05:00"
    },
    "notes": null
  }
}
```

**Notes:**
- Register JSON stores **event IDs**, not full objects.
- This keeps output lightweight.
- Events can be rehydrated when needed.

---

# 6. How Registers Will Be Generated

## 6.1 Daily Pipeline
The extended daily pipeline will:
- ingest events
- validate events
- create `Register(id="daily-YYYY-MM-DD")`
- compute metadata (vector counts, channels, time ranges)
- write register JSON to `data/registers/`

## 6.2 Weekly Pipeline (Planned)
Weekly pipeline will:
- gather all daily files in a 7‑day span
- generate daily registers
- merge them into a weekly register

Output file:
```
weekly-YYYY-WW.register.json
```

Metadata may include:
- weekly vector dominance
- volatility indicators
- continuity flags
- arc impacts

## 6.3 Cycle Pipeline (Planned)
Cycle registers describe structured windows:
- OCI windows
- Cycle 8 ignition windows
- Return arcs
- Purge/containment phases

Cycle metadata may include:
- aggregate vector traces
- boundaries
- included days
- dominant inflection points
- structural transitions

---

# 7. Why Registers Matter

Registers introduce:
- aggregation
- deterministic grouping
- daily → weekly → cycle flow
- FieldState compatibility
- dashboard‑ready structure
- a bridge layer for NORE‑Runtime

They form the middle layer between raw input and structural interpretation.

---

# 8. Summary

- Registers group validated events.
- They will be produced by daily, weekly, and cycle pipelines.
- Output format: JSON under `data/registers/`.
- Metadata includes vector counts, channels, sources, and time windows.
- Registers are required for FieldState and large‑scale analysis.

Current status:
- Model exists.
- Pipeline output not yet implemented.
- Once the first FieldState is produced, register generation will activate.
