# Cycle Registers · Canonical Template and Conventions

Cycle registers sit **above** daily, weekly, and monthly registers.

They represent **structural windows** (e.g., Cycle 8 ignition) that may cut across calendar boundaries:

* calendar weeks
* calendar months
* arbitrary ranges

NORE-AI treats cycles as **aggregated views** over an explicit date range. Interpretation remains in Runtime / IL-ARCHON — cycles are *structural summaries only*.

---

## 1. Location and Naming

Cycle registers live in:

```
data/registers/
```

Each cycle is a single JSON file:

```
cycle-<ID>.json
```

Examples:

```
cycle-8.json
cycle-12.json
cycle-16.json
```

`<ID>` should be stable and semantic:

* `8` for Cycle 8
* `08-ignition` for multiple passes
* `16-return` for Cycle 16 return window

---

## 2. Cycle Register Template (Fields)

Every cycle register MUST follow this schema:

```jsonc
{
  "id": "cycle-8",
  "range_start": "2025-11-30",
  "range_end": "2025-12-14",

  "days": [
    "2025-11-30",
    "2025-12-01",
    "2025-12-02"
    // ...
  ],

  "fieldstates": [
    "fieldstate-2025-11-30",
    "fieldstate-2025-12-01",
    "fieldstate-2025-12-02"
    // ...
  ],

  "event_count": 0,

  "channels": {
    "macro-field": 0,
    "governance": 0
    // ...
  },

  "vectors": {
    "exposure": 0,
    "collapse": 0,
    "inversion": 0
    // ...
  },

  "laws": {
    "FL-06": 0,
    "FL-12": 0,
    "FL-13": 0
    // ...
  },

  "status": "partial",

  "summary": {
    "dominant_themes": [],
    "peak_day": null,
    "peak_vectors": {},
    "peak_laws": {},
    "notes": "Auto-generated cycle register; aggregates FieldState counts only."
  }
}
```

---

## 2.1 Identity

### `id`

String. Required. Canonical cycle id used by scripts such as `print_cycle_summary.py`.

### `range_start`

String (YYYY-MM-DD). Required. First day in the window.

### `range_end`

String (YYYY-MM-DD). Required. Last day in the window (inclusive).

---

## 2.2 Membership

### `days`

Array of YYYY-MM-DD strings. Required.
Must be **contiguous** between `range_start` and `range_end`.

### `fieldstates`

Array of strings. Required.
Each must be `fieldstate-YYYY-MM-DD`.
Order must match `days`.

---

## 2.3 Aggregates

Computed from underlying FieldStates.

### `event_count`

Integer. Total events across days.

### `channels`

Object mapping channel → count.

### `vectors`

Object mapping vector → count.

### `laws`

Object mapping law id → count.

---

## 2.4 Status

### `status`

Must be one of:

* `partial` — still open
* `complete` — window sealed, no edits allowed

Once `complete`, the register is immutable.

---

## 2.5 Summary Block

### `dominant_themes`

Top 3 vectors by count. Ties broken alphabetically.

### `peak_day`

Day with highest event count. Earliest wins ties. `null` if none.

### `peak_vectors`

Top N vectors (commonly 5) by count.

### `peak_laws`

Top N laws by count.

### `notes`

Auto-generated description of how the register was constructed.

Example:

```
"Auto-generated cycle register; aggregates FieldState counts only. No interpretive content."
```

---

## 3. Example: Cycle 8 Template (Skeleton)

```json
{
  "id": "cycle-8",
  "range_start": "2025-11-30",
  "range_end": "2025-12-14",
  "days": [
    "2025-11-30",
    "2025-12-01",
    "2025-12-02",
    "2025-12-03",
    "2025-12-04",
    "2025-12-05",
    "2025-12-06",
    "2025-12-07",
    "2025-12-08",
    "2025-12-09",
    "2025-12-10",
    "2025-12-11",
    "2025-12-12",
    "2025-12-13",
    "2025-12-14"
  ],
  "fieldstates": [
    "fieldstate-2025-11-30",
    "fieldstate-2025-12-01",
    "fieldstate-2025-12-02",
    "fieldstate-2025-12-03",
    "fieldstate-2025-12-04",
    "fieldstate-2025-12-05",
    "fieldstate-2025-12-06",
    "fieldstate-2025-12-07",
    "fieldstate-2025-12-08",
    "fieldstate-2025-12-09",
    "fieldstate-2025-12-10",
    "fieldstate-2025-12-11",
    "fieldstate-2025-12-12",
    "fieldstate-2025-12-13",
    "fieldstate-2025-12-14"
  ],
  "event_count": 0,
  "channels": {},
  "vectors": {},
  "laws": {},
  "status": "partial",
  "summary": {
    "dominant_themes": [],
    "peak_day": null,
    "peak_vectors": {},
    "peak_laws": {},
    "notes": "Auto-generated cycle register; aggregates FieldState counts only. No interpretive content."
  }
}
```

---

## 4. Generator Expectations (`close_cycle.py`)

The cycle closer should:

1. Accept:

   * `cycle_id`
   * `range_start`
   * `range_end`

2. Derive `days` from the contiguous date range.

3. Build `fieldstates` as:

   ```
   fieldstate-YYYY-MM-DD
   ```

4. Aggregate:

   * event_count
   * channels
   * vectors
   * laws

5. Compute the summary block.

6. Write to `data/registers/<cycle_id>.json` with:

   ```
   "status": "complete"
   ```

---

## 5. Immutability and Archive

When a cycle register is:

* written, and
* marked `"complete"`

…it becomes immutable.

No:

* editing counts
* changing days
* rewriting vectors or laws

All reinterpretation belongs in runtime layers:

* Runtime docs
* IL-ARCHON narratives
* supplemental metadata

Cycle registers remain frozen structural records.
