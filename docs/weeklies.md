# Weekly Registers

A **Weekly Register** is the intermediate aggregation layer in NORE-AI. It binds together all `FieldState` files that fall within the same ISO week, producing a stabilized summary of the week’s structural motion.

Hierarchy:

```
Event → FieldState (day)
FieldState → WeeklyRegister (week)
WeeklyRegister → MonthlyRegister (month)
```

Weekly registers are mechanically generated — they capture **frequency**, not meaning.

---

## 1. Purpose

Weekly registers serve three functions:

### 1. Aggregate daily FieldStates

Collect and unify counts of:

* vectors
* laws
* channels
* sources
* total event volume

### 2. Provide a stable 7‑day snapshot

Daily data is noisy; weekly registers compress signal into a mid-range time window suitable for:

* early trend detection
* mid-cycle analysis
* pressure mapping for origin-alignment laws

### 3. Form the foundation for monthly and cycle-level registers

Weekly registers are not interpreted directly — they stabilize the data before it is elevated.

---

## 2. How They’re Generated

Weekly registers are created automatically by:

```
scripts/run_day_and_week.py YYYY-MM-DD
```

This script performs:

1. Build the day’s `FieldState`
2. Load existing weekly register (if any)
3. Append today’s FieldState
4. Re‑aggregate totals
5. Write back:

```
data/registers/weekly-YYYY-WW.json
```

The script ensures idempotency — running it multiple times per day does not corrupt the weekly register.

---

## 3. File Naming Convention

Weekly registers follow ISO week numbering:

```
weekly-YYYY-WW.json
```

Examples:

```
weekly-2025-W47.json
weekly-2025-W48.json
weekly-2026-W01.json
```

All weekly registers live in:

```
data/registers/
```

---

## 4. Structure

A weekly register is produced by the `WeeklyRegister` model.

### Example

```json
{
  "id": "weekly-2025-W47",
  "week_start": "2025-11-17",
  "week_end": "2025-11-23",

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
    "notes": "Auto-generated weekly register; aggregates FieldState counts only.",
    "dominant_themes": [
      "continuity",
      "exposure",
      "signal"
    ]
  }
}
```

---

## 5. Status Values

| Status     | Meaning                                               |
| ---------- | ----------------------------------------------------- |
| `partial`  | Week is still in progress (default while days remain) |
| `complete` | Week has closed (after the final day is processed)    |
| `empty`    | Reserved — the week had no events (not typical)       |

`scripts/run_day_and_week.py` automatically marks a week as `complete` once Sunday is processed.

---

## 6. Dominant Themes

Dominant themes are selected mechanically:

```
Top 3 vectors by frequency for the week.
```

Ties are broken deterministically by ordering — no semantic interpretation.

This produces a stable **weekly vector fingerprint**.

---

## 7. Weekly Boundary Logic

ISO week rules apply:

* Week starts: **Monday**
* Week ends: **Sunday**
* Year boundary handled automatically

The script calculates:

* `week_start` using ISO week lookup
* `week_end` using ISO lookup + 6 days offset

This yields consistent weekly windows.

---

## 8. Relationship to Other Registers

### FieldState → WeeklyRegister

Daily → Weekly (aggregation only)

### WeeklyRegister → MonthlyRegister

Weekly aggregates contribute indirectly via FieldStates.

### WeeklyRegister → CycleRegister (future)

Cycles aggregate directly from FieldStates to avoid calendar coupling, but weekly registers provide a clean mid-range diagnostic layer.

---

## 9. Closing a Week

A week closes automatically when:

```
scripts/run_day_and_week.py <date>
```

is run for the **Sunday** of that week.

Example:

```bash
python scripts/run_day_and_week.py 2025-11-23
```

The weekly register’s `status` flips to `"complete"`.

---

## 10. When to Use Weekly Registers

Use them when you want:

* a mid-level trend view
* law distribution smoothing
* vector pressure comparison
* cycle overlay preparation
* a stable grouping layer between daily and monthly cadence

Do **not** use them for interpretation — that belongs to the runtime layer, not the register layer.
