# Monthly Registers

A **Monthly Register** is a high-level aggregation over all `FieldState` files within a given calendar month. It provides a structural summary of multi-week behavior — continuity, exposure, inversion, alignment, and law pressure across an entire month — without interpreting meaning. It is purely mechanical.

Monthly Registers form the third layer of the NORE-AI hierarchy:

```
Event → FieldState (day)
FieldState → WeeklyRegister (week)
WeeklyRegister → MonthlyRegister (month)
```

Cycle registers (e.g., Cycle 8: 2025-11-30 → 2025-12-14) are built using the same pattern but operate across arbitrary ranges rather than calendar boundaries.

---

## 1. Purpose

Monthly Registers exist to:

* consolidate signal distribution at month scale
* expose dominant vectors across multiple weeks
* quantify law pressure (FL-xx counts) at a higher altitude
* offer a stable framing for cycle-level interpretation
* provide a consistent archive point for end-of-month snapshots

Monthly Registers do **not**:

* summarize meaning
* perform interpretation
* infer continuity beyond frequency patterns
* replace FieldStates or weekly registers

They exist as mirrors of the underlying data — nothing more.

---

## 2. Data Sources

Monthly Registers are built exclusively from previously-generated `FieldState` files.

Source directory:

```
data/registers/fieldstate-YYYY-MM-DD.json
```

The month closer script walks all dates between `month_start` and `month_end`, includes only existing FieldStates, and aggregates them.

---

## 3. File Naming

Monthly registers follow the fixed naming pattern:

```
monthly-YYYY-MM.json
```

Examples:

```
monthly-2025-11.json
monthly-2026-02.json
```

They live inside:

```
data/registers/
```

---

## 4. Structure

A Monthly Register is defined by the `MonthlyRegister` model:

```json
{
  "id": "monthly-2025-11",
  "month_start": "2025-11-01",
  "month_end": "2025-11-30",

  "days": [
    "2025-11-17",
    "2025-11-18",
    "2025-11-19",
    "..."
  ],

  "fieldstates": [
    "fieldstate-2025-11-17",
    "fieldstate-2025-11-18",
    "..."
  ],

  "event_count": 33,

  "channels": {
    "macro-field": 12,
    "governance": 5,
    "ai-infra": 1
  },

  "vectors": {
    "continuity": 25,
    "exposure": 25,
    "signal": 25,
    "alignment": 16,
    "inversion": 20
  },

  "laws": {
    "FL-12": 33,
    "FL-13": 33,
    "FL-06": 32,
    "FL-09": 13
  },

  "status": "complete",

  "summary": {
    "notes": "Auto-generated monthly register; aggregates FieldState counts only.",
    "dominant_themes": [
      "continuity",
      "exposure",
      "signal"
    ]
  }
}
```

### Key fields

| Field             | Meaning                                  |
| ----------------- | ---------------------------------------- |
| `days`            | Days in which FieldStates actually exist |
| `fieldstates`     | Identifiers of included FieldState files |
| `event_count`     | Total number of events across all days   |
| `channels`        | Aggregated channel counts                |
| `vectors`         | Aggregated vector frequencies            |
| `laws`            | Aggregated FL-xx law frequencies         |
| `dominant_themes` | Top 3 most frequent vectors              |

---

## 5. Generator Script

Monthly registers are produced by:

```
scripts/close_month.py
```

Usage:

```bash
python scripts/close_month.py 2025-11-30
```

Any date within the target month is acceptable.

This script:

1. Determines month start/end
2. Loads all FieldStates for that window
3. Aggregates
4. Writes:

```
data/registers/monthly-YYYY-MM.json
```

---

## 6. Status Values

| Status     | Meaning                                           |
| ---------- | ------------------------------------------------- |
| `complete` | All FieldStates for the month have been finalized |
| `partial`  | Reserved for future streaming mode (not used yet) |
| `empty`    | No FieldStates found for the month                |

In practice, monthly registers will almost always be generated at month-end and immediately marked `complete`.

---

## 7. Dominant Themes

Dominant themes are frequency-based only:

```
Top 3 vectors by total count
```

No weighting, no interpretation.

If continuity and exposure tie, whichever appears first in the sorted vector map is listed earlier — deterministic.

---

## 8. How Monthly Registers Feed Cycle Registers

Monthly registers reframe the raw daily → weekly structure into a single consolidated snapshot. Cycle registers (e.g., Cycle 8: Nov 30–Dec 14) will consume FieldStates **directly**, not the monthly register, but the monthly layer acts as an anchor for broader pattern recognition.

---

## 9. When to Close a Month

NORE-AI recommends:

* run daily FieldState builder (`run_day_and_week.py`) every day you have events
* run `close_month.py` on the last day of the month or immediately after
* do not run it mid-month — it assumes the month is ready to finalize

For November:

```
python scripts/close_month.py 2025-11-30
```
