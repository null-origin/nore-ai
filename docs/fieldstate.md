# FieldState

`FieldState` is the **daily structural snapshot** produced after NORE-AI processes a single event file. It is the deterministic summary of what was observed on that day — no forecasting, inference, or narrative. It forms the bridge between:

- raw events (`Event`)
- organized daily knowledge (`Register`)
- higher-order windows (weekly/cycle-level structures)

FieldState is the lowest-level stateful representation inside the NORE runtime.

---

# 1. Purpose

FieldState answers:

**“What was the shape of the field today, given only what was logged?”**

It captures:
- event metrics
- vector distribution
- channel/source distribution
- observational time window
- structural notes
- deterministic ID
- event references

It does **not**:
- predict
- interpret
- infer hidden meaning
- rank-order events
- generate narrative

Its sole purpose is to stabilize the day into a reproducible structure.

---

# 2. File Naming

FieldState files live under:
```
data/registers/
```

Filename:
```
fieldstate-YYYY-MM-DD.json
```

Examples:
- `fieldstate-2025-11-16.json`
- `fieldstate-2025-12-04.json`

---

# 3. Model Structure

FieldState is a dataclass with explicit, deterministic fields.

```python
@dataclass
class FieldState:
    id: str                        # "fieldstate-YYYY-MM-DD"
    day: date                      # 2025-11-16
    event_ids: List[str]           # ["s-2025-11-16-01", ...]
    count: int                     # event count
    vectors: Dict[str, int]        # {"exposure": 4, "collapse": 1}
    channels: Dict[str, int]       # {"corporate": 2, "sports": 1}
    sources: Dict[str, int]        # {"cnbc": 1, "espn": 1}
    time_start: Optional[str]      # earliest timestamp
    time_end: Optional[str]        # latest timestamp
    notes: Optional[str] = None    # optional annotation
```

---

# 4. Field Definitions

## 4.1 `id`
Deterministic identifier:
```
fieldstate-YYYY-MM-DD
```

## 4.2 `day`
Python `date`. Must match the filename date.

## 4.3 `event_ids`
List of event IDs in ingestion order.
- No reordering
- No deduplication

## 4.4 `count`
Number of valid (schema-passing) events.

## 4.5 `vectors`
Frequency map of all vectors.

Example:
```json
{
  "exposure": 6,
  "retrieval": 3,
  "collapse": 1
}
```

## 4.6 `channels`
Distribution of event channels.

## 4.7 `sources`
Distribution of event sources.

## 4.8 `time_start` / `time_end`
Earliest and latest timestamps across the day's events.
Represents the observational window.

## 4.9 `notes`
Optional short annotation. Only manually editable field.

---

# 5. How FieldState Is Created

Daily pipeline sequence:
```
ingest → validate → summarize → FieldState
```

Computed values:
- event ID list
- event count
- vector frequencies
- channel frequencies
- source frequencies
- earliest timestamp
- latest timestamp
- deterministic ID

FieldState is a pure function of:
```
event file + schema + pipeline code
```
No runtime clocks, randomness, or external inputs.

---

# 6. FieldState vs Register

| Model       | Purpose                     | Contains                         |
|-------------|-----------------------------|----------------------------------|
| FieldState  | analytic snapshot of a day  | counts, distributions, windows   |
| Register    | archival grouping of events | event IDs, metadata              |

Registers store:
- event IDs
- metadata

FieldState stores:
- analytic structure

Weekly/cycle registers will use multiple FieldStates as inputs.

---

# 7. Serialization Format

FieldState is written as JSON.

Example:
```json
{
  "id": "fieldstate-2025-11-16",
  "day": "2025-11-16",
  "event_ids": [
    "s-2025-11-16-01",
    "s-2025-11-16-02"
  ],
  "count": 2,
  "vectors": {
    "exposure": 1,
    "retrieval": 1
  },
  "channels": {
    "corporate": 1,
    "music": 1
  },
  "sources": {
    "cnbc": 1,
    "pandora": 1
  },
  "time_start": "2025-11-16T08:23:00-05:00",
  "time_end": "2025-11-16T21:12:45-05:00",
  "notes": null
}
```

---

# 8. Determinism Requirements

FieldState must always be identical for identical inputs.

No:
- randomness
- fuzzy interpretation
- environment-dependent behavior
- external APIs

If the input file does not change, the FieldState must never change.

---

# 9. Future Extensions

Will be added only after daily FieldState stabilizes:

- weekly FieldState
- vector trajectory summaries
- channel volatility
- 7-day rolling averages
- cycle-window aggregations
- FieldState ↔ Register cross-links

All future layers treat FieldState as the canonical source of truth.

---

# 10. Summary

FieldState is the daily backbone of NORE-AI.
It provides the first stable, deterministic structural representation of each day.

It is:
- reproducible
- minimal
- stable
- non-interpretive
- purely structural

This ensures the entire NORE runtime rests on the same foundation every time it is run.
