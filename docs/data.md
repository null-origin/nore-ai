# NORE-AI Data Format & Conventions

This document defines the canonical structure for all event data consumed by NORE-AI. It specifies rules for file placement, naming, formatting, timestamps, metadata, vectors, and normalization. These conventions ensure deterministic ingestion and validation.

---

# 1. Directory Structure

All raw daily event logs live under:

```
data/events/
```

Each file contains **one JSONL line per event**.

```
data/
  events/
    2025-11-14.jsonl
    2025-11-15.jsonl
    2025-11-16.jsonl
  registers/   (future output)
```

No subfolders. No prefixes. One file per date.

---

# 2. File Naming Rules

Daily event files must follow:

```
YYYY-MM-DD.jsonl
```

Examples:
- `2025-11-14.jsonl`
- `2025-12-04.jsonl`
- `2026-01-01.jsonl`

This ensures chronological sorting and unambiguous date extraction.

---

# 3. Event Format (JSON Schema)

Events must conform to:
```
schemas/event.schema.json
```

### Required Fields
| Field       | Type     | Description |
|-------------|----------|-------------|
| `id`        | string   | Unique event identifier (`s-YYYY-MM-DD-XX`) |
| `timestamp` | string   | ISO-8601 datetime with timezone offset |
| `source`    | string   | Origin of the event (news, feed, user, macro) |
| `channel`   | string   | Logical category (`corporate`, `macro`, `sports`, etc.) |
| `vectors`   | array    | Structural vectors |
| `text`      | string   | Human-readable description |
| `meta`      | object   | Additional contextual data |

### Optional Fields
- `laws`
- `confidence`
- `severity`
- `decision`
- `status`
- `runtime`

Optional fields should be omitted when unused.

---

# 4. ID Naming Convention

IDs must follow:

```
s-YYYY-MM-DD-NN
```

Where:
- `s` = system-level event
- `YYYY-MM-DD` = date
- `NN` = zero‑padded index for that day (`01`, `02`, `03`, ...)

Examples:
- `s-2025-11-14-01`
- `s-2025-11-14-02`
- `s-2025-12-04-07`

---

# 5. Timestamp Conventions

Timestamps **must** be:
- ISO 8601
- include date, time, and timezone offset
- include seconds

Format:
```
YYYY-MM-DDTHH:MM:SS-05:00
```

Examples:
```
2025-11-14T10:30:00-05:00
2025-12-04T09:12:47-05:00
```

Invalid formats include:
- bare dates
- missing offsets
- timestamps without seconds

---

# 6. Source Conventions

`source` identifies the producing entity.

Examples:
- `cnbc`
- `reuters`
- `pandora`
- `user`
- `espn`
- `fed`
- `pentair`
- `macro-feed`

Keep this lowercase, short, and consistent.

---

# 7. Channel Conventions

`channel` identifies the *type* of event.

Recommended channels:
- `corporate`
- `macro`
- `sports`
- `music`
- `tech`
- `social`
- `user`
- `system`

Channels are categorical, not hierarchical.

---

# 8. Vectors

`vectors` encode structural interpretation.

Common vectors:
- `collapse`
- `retrieval`
- `exposure`
- `inversion`
- `alignment`
- `return`
- `purge`
- `signal`
- `bridge`

Vectors are:
- lowercase
- conceptual
- additive
- determined at ingestion

---

# 9. Meta Object Rules

`meta` must always be an **object** — never a string, list, or null.

It may be empty (`{}`) but must be present.

Recommended keys:
- `tags`: array
- `window`: boolean or null
- `note`: short annotation
- `details`: structured info

Example:
```json
"meta": {
  "tags": ["walmart", "leadership", "retail"],
  "window": false,
  "note": "sector-wide recalibration"
}
```

---

# 10. Example Event (Fully Valid)

```json
{
  "id": "s-2025-11-14-02",
  "timestamp": "2025-11-14T10:30:00-05:00",
  "source": "cnbc",
  "channel": "corporate",
  "vectors": ["exposure", "retrieval"],
  "text": "Walmart CEO Doug McMillon to retire after nearly 12 years, succeeded by Walmart U.S. CEO John Furner.",
  "meta": {
    "tags": ["walmart", "leadership transition", "retail"],
    "window": false,
    "note": "legacy arc closure"
  }
}
```

This event will pass schema validation and pipeline ingestion.

---

# 11. Validation Behavior

Validation enforces:
- required fields
- correct types
- ISO timestamps
- `meta` is an object
- `vectors` is an array of strings

The pipeline returns:
- `events` — valid ones
- `errors` — formatted error strings

Errors never halt execution.

---

# 12. Summary

These rules ensure:
- deterministic ingestion
- zero ambiguity
- consistent structure across all ranges (daily, weekly, cycle)
- compatibility with FieldState, registers, and pipelines

Events following this spec will load reliably across all present and future NORE-AI engines.
