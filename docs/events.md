# Events · Event Model Specification, Schema Rules, Metadata Conventions, and Writing Guidelines

Events are the **atomic units of observation** in NORE-AI. Each event is a single, timestamped factual record. Events are:
- deterministic
- minimal
- schema-validated
- non-interpretive
- one-line JSON objects (JSONL)

All downstream structures — FieldState, Registers, Runtime — rely on the correctness of event lines.

---

# 1. Event Location and Naming

Events live in:
```
data/events/
```

Each file represents **one calendar day**:
```
YYYY-MM-DD.jsonl
```
Examples:
- `2025-11-14.jsonl`
- `2025-11-16.jsonl`
- `2025-12-04.jsonl`

**No nested folders. No mixed-date files.**

---

# 2. Event Line Format (JSONL)

Each event is a **single-line JSON object**.

Example:
```json
{"id":"s-2025-11-16-01","timestamp":"2025-11-16T09:14:30-05:00","channel":"corporate","source":"cnbc","vectors":["exposure","retrieval"],"laws":[],"text":"Walmart CEO Doug McMillon announces retirement...","meta":{"tags":["walmart","leadership"],"note":"sector recalibration"}}
```

Rules:
- no trailing commas
- no multi-line JSON
- UTF-8 only
- each line must be valid JSON

---

# 3. Event Schema (Authoritative)

Schema used for validation:
```json
{
  "type": "object",
  "required": ["id", "timestamp", "channel", "source", "vectors", "text"],
  "properties": {
    "id": {
      "type": "string",
      "pattern": "^s-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}$"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "channel": {
      "type": "string"
    },
    "source": {
      "type": "string"
    },
    "vectors": {
      "type": "array",
      "items": { "type": "string" },
      "minItems": 1
    },
    "laws": {
      "type": "array",
      "items": { "type": "string" },
      "default": []
    },
    "text": {
      "type": "string",
      "minLength": 1
    },
    "meta": {
      "type": "object",
      "default": {}
    }
  }
}
```
Stored at:
```
schemas/event.schema.json
```

---

# 4. Field Definitions

## 4.1 `id`
Deterministic identifier:
```
s-YYYY-MM-DD-NN
```
Example: `s-2025-11-16-03`

Rules:
- must match the file date
- sequential (01, 02, 03…)
- no gaps, no reuse
- two-digit suffix only

## 4.2 `timestamp`
ISO 8601 with timezone offset:
```
2025-11-16T09:14:30-05:00
```
Rules:
- must include offset (`-05:00`)
- must reflect real event time
- no `Z`
- no naive timestamps

## 4.3 `channel`
Allowed:
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
Rules:
- lowercase
- single word

## 4.4 `source`
Origin of the event. Examples:
```
cnbc
espn
reuters
pandora
mlb
personal
```
Rules:
- lowercase
- hyphens allowed
- no URLs

## 4.5 `vectors`
Structural mechanics:
```
["exposure"]
["collapse", "retrieval"]
["alignment"]
```
Rules:
- lowercase
- must align with `docs/vectors.md`
- at least one vector

## 4.6 `laws` (optional)
Example:
```
["FL-06", "FL-03"]
```
Rules:
- optional
- must reference valid law IDs

## 4.7 `text`
Short, factual, non-interpretive.
Example:
```
"Amazon announces new AI compute partnership with Anthropic."
```
Not allowed: commentary, speculation, implication.

## 4.8 `meta`
Example:
```json
"meta": {
  "tags": ["amazon", "compute"],
  "note": "infrastructure acceleration",
  "window": false
}
```
Rules:
- lowercase snake_case keys
- JSON-serializable values
- max 2 levels deep
- `tags` = lowercase list
- `note` = short phrase

---

# 5. Writing Events Correctly (Rules)

1. One line = one event.
2. ID + timestamp must match file date.
3. Vectors must be structural mechanics.
4. Text must be factual and concise.
5. Optional fields must exist (`laws`: [], `meta`: {}).

---

# 6. Event Quality Checklist

✔ factual?  
✔ timestamped?  
✔ sequential ID?  
✔ at least one vector?  
✔ text concise + non-interpretive?  
✔ tags lowercase?  
✔ meta valid?  
✔ belongs on this date?  

If yes → event is valid.

---

# 7. Examples

## 7.1 Minimal valid event
```json
{"id":"s-2025-11-16-01","timestamp":"2025-11-16T08:23:00-05:00","channel":"corporate","source":"cnbc","vectors":["exposure"],"laws":[],"text":"Meta announces cloud compute expansion.","meta":{}}
```

## 7.2 Event with vectors + meta
```json
{"id":"s-2025-11-16-04","timestamp":"2025-11-16T13:05:12-05:00","channel":"sports","source":"espn","vectors":["collapse","retrieval"],"laws":["FL-02"],"text":"Brewers drop third straight game.","meta":{"tags":["brewers","mlb"],"note":"pattern echo"}}
```

## 7.3 Multi-vector mechanics
```json
{"id":"s-2025-11-16-09","timestamp":"2025-11-16T20:44:53-05:00","channel":"music","source":"pandora","vectors":["exposure","alignment","retrieval"],"laws":[],"text":"Mastodon track surfaces unexpectedly in rotation.","meta":{"tags":["mastodon"],"window":false}}
```

---

# 8. Summary

Events are:
- atomic
- deterministic
- validated
- non-narrative
- strictly formatted

A correct event file ensures:
- FieldState accuracy
- Register coherence
- Weekly/cycle analysis consistency
- NORE runtime stability

Events are the **bedrock** of the entire NORE-AI architecture.
