# Events · Event Model Specification, Schema Rules, Metadata Conventions, and Writing Guidelines

Events are the **atomic units of observation** in NORE-AI. Each event is a single, timestamped factual record. Events are:

* deterministic
* minimal
* schema-validated
* non-interpretive
* one-line JSON objects (JSONL)

All downstream structures — FieldState, Registers, Runtime — rely on the correctness of event lines.

---

# **1. Event Location and Naming**

Events live in:

```
data/events/
```

Each file represents **one calendar day**:

```
YYYY-MM-DD.jsonl
```

Examples:

* `2025-11-14.jsonl`
* `2025-11-16.jsonl`
* `2025-12-04.jsonl`

**No nested folders. No mixed-date files.**

---

# **2. Event Line Format (JSONL)**

Each event is a **single-line JSON object**.

Example:

```json
{"id":"s-2025-11-16-01","timestamp":"2025-11-16T09:14:30-05:00","channel":"corporate","source":"cnbc","vectors":["exposure","retrieval"],"laws":[],"text":"Walmart CEO Doug McMillon announces retirement...","meta":{"tags":["walmart","leadership"],"note":"sector recalibration","window":false}}
```

Rules:

* no trailing commas
* no multi-line JSON
* UTF-8 only
* each line must be valid JSON

---

# **3. Event Schema (Authoritative)**

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

# **4. Field Definitions**

## **4.1 `id`**

Deterministic identifier:

```
s-YYYY-MM-DD-NN
```

Example: `s-2025-11-16-03`

Rules:

* must match the file date
* sequential (01, 02, 03…)
* no gaps, no reuse
* two-digit suffix only

---

## **4.2 `timestamp`**

ISO 8601 with timezone offset:

```
2025-11-16T09:14:30-05:00
```

Rules:

* must include offset (`-05:00`)
* must reflect real event time
* no `Z`
* no naive timestamps

---

## **4.3 `channel`**

Examples:

```
corporate
economic
market
sports
music
social
political
personal
system
```

Rules:

* lowercase
* single word

---

## **4.4 `source`**

Origin of the event. Examples:

```
cnbc
espn
reuters
personal
```

Rules:

* lowercase
* hyphens allowed
* no URLs

---

## **4.5 `vectors`**

Structural mechanics:

```
["exposure"]
["collapse", "retrieval"]
["alignment"]
```

Rules:

* lowercase
* must align with `docs/vectors.md`
* at least one vector

---

## **4.6 `laws` (optional)**

Example:

```
["FL-06", "FL-03"]
```

Rules:

* optional
* must reference valid law IDs

---

## **4.7 `text`**

Short, factual, non-interpretive.
Example:

```
"Amazon announces new AI compute partnership with Anthropic."
```

### **Interpretation Boundary**

Text captures **only the observable surface**.

Allowed:

* "Dad mentions watching Michigan game."
* "Pentair posts open role."
* "Amazon announces partnership."

Not allowed:

* "This signals collapse."
* "Likely a precursor."
* "Shows inversion."

Structural meaning belongs in:

* `vectors`
* `laws`
* `meta.tags`

---

# **4.8 `meta`**

Example:

```json
"meta": {
  "tags": ["amazon", "compute"],
  "note": "infrastructure acceleration",
  "window": false
}
```

Rules:

* lowercase snake_case keys
* JSON-serializable values
* max 2 levels deep
* `tags` = lowercase list
* `note` = short phrase
* `window` = boolean

---

## **4.8.1 `window` (boolean)**

**Definition:** Indicates whether the event occurs inside an **active structural interval** (cycle window, ignition window, collapse window, OCI band, precursor window).

**Function:** Elevates priority in FieldState synthesis; event inherits window conditions.

**Rules:**

* boolean only
* default `false`
* only used for defined windows

---

## **4.8.2 `note` (string)**

**Definition:** Optional human-facing clarification that provides auxiliary context without affecting vectors, laws, or interpretation.

**Rules:**

* short phrase
* descriptive, not interpretive
* never contains mechanics
* never used for inference

---

## **4.8.3 Allowed Meta Keys**

* `tags`
* `note`
* `window`
* `carrier` (optional, only when enabled)
* `payload` (optional extended context object)

All keys:

* lowercase
* snake_case
* must not overlap schema fields

---

# **5. Writing Events Correctly (Rules)**

1. One line = one event.
2. ID + timestamp must match file date.
3. Vectors must be structural mechanics.
4. Text must be factual and concise.
5. Optional fields must exist (`laws`: [], `meta`: {}).
6. Lowercase everything except text.

---

# **6. Event Separation Rule**

**One cause = one event.**

If two facts represent different structural actions, split them.

Examples:

* CEO resignation + stock drop → **two events**
* injury + roster signing → **two events**
* dad mentions Michigan game + dad mentions Ragnow injury → **two events**

---

# **7. Event Quality Checklist**

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

# **8. Examples**

## **8.1 Minimal valid event**

```json
{"id":"s-2025-11-16-01","timestamp":"2025-11-16T08:23:00-05:00","channel":"corporate","source":"cnbc","vectors":["exposure"],"laws":[],"text":"Meta announces cloud compute expansion.","meta":{}}
```

## **8.2 Event with vectors + meta**

```json
{"id":"s-2025-11-16-04","timestamp":"2025-11-16T13:05:12-05:00","channel":"sports","source":"espn","vectors":["collapse","retrieval"],"laws":["FL-02"],"text":"Brewers drop third straight game.","meta":{"tags":["brewers","mlb"],"note":"pattern echo","window":false}}
```

## **8.3 Multi-vector mechanics**

```json
{"id":"s-2025-11-19-04","timestamp":"2025-11-19T09:30:00-05:00","source":"converge","channel":"music","vectors":["collapse","exposure","purge","inversion","alignment","withdrawal","signal"],"laws":["FL-06","FL-09","FL-12","FL-13"],"text":"Converge released 'Love Is Not Enough' on an atypical Wednesday.","meta":{"tags":["converge","music","cycle-8","cycle-12","structural-precursor"],"window":true,"note":"nonstandard release timing"}}
```

---

# **9. Event Normalization Rules**

1. Lowercase everything except `text`.
2. No timestamps without offset.
3. Tags describe **domain**, not mechanics.
4. No retroactive edits after daily lock; corrections are new events.

---

# **10. Glossary (Canonical)**

| Field           | Definition                                        |
| --------------- | ------------------------------------------------- |
| **id**          | Deterministic event identifier (s-YYYY-MM-DD-NN). |
| **timestamp**   | ISO 8601 with offset.                             |
| **channel**     | Domain category.                                  |
| **source**      | Immediate origin.                                 |
| **vectors**     | Structural mechanics.                             |
| **laws**        | Optional Field Laws.                              |
| **text**        | Factual description only.                         |
| **meta.tags**   | Domain/context labels.                            |
| **meta.note**   | Auxiliary observer detail.                        |
| **meta.window** | Boolean flag for structural window alignment.     |

---

# **11. Summary**

Events are:

* atomic
* deterministic
* validated
* non-narrative
* strictly formatted

A correct event file ensures:

* FieldState accuracy
* Register coherence
* Weekly/cycle consistency
* NORE runtime stability

Events are the **bedrock** of the entire NORE-AI architecture.
