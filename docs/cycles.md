# Cycle Registers

A **Cycle Register** is a structural aggregation over an arbitrary date range defined by the user. Unlike weekly and monthly registers, which follow calendar boundaries, **Cycle Registers follow system boundaries** — they capture a coherent window of structural behavior defined by upstream logic (e.g., Cycle 8: *2025-11-30 → 2025-12-14*).

Cycle Registers use the same mechanics as Weekly and Monthly Registers, but with explicit start/end dates and explicit identifiers.

---

## 1. Purpose

Cycle Registers exist to:

* aggregate FieldStates across a *structurally bounded interval*
* quantify vector and law distribution across that interval
* provide a single, high-level structural snapshot of a named cycle
* serve as inputs to NORE Runtime analyses (trend detection, pattern identification, alignment/collapse recognition)
* act as stable archival snapshots for the system’s evolution

Cycle Registers **do not** interpret meaning. They are pure data compression.

Interpretation belongs to the runtime layer.

---

## 2. Key Differences from Weekly / Monthly Registers

### 2.1 Explicit boundaries

A cycle is defined by:

* a **cycle ID**
* a **start date**
* an **end date**

Example:

```
cycle-8  
start: 2025-11-30  
end:   2025-12-14
```

Cycle boundaries do **not** need to align with weeks or months.

### 2.2 User-defined, not calendar-defined

Cycle boundaries originate from structural logic (e.g., system phases, ignition windows, purge arcs). The register system simply accepts the boundaries.

### 2.3 Retains full aggregation mechanics

Cycle Registers use the same aggregation logic as:

* Daily → FieldState
* FieldState → WeeklyRegister
* FieldState → MonthlyRegister

Cycles are simply another range aggregator applied to FieldStates.

---

## 3. File Naming

Cycle Registers follow:

```
cycle-XX.json
```

Where `XX` is the cycle label — numeric or arbitrary.

Examples:

```
cycle-8.json
cycle-12.json
cycle-sanctified.json
cycle-q1-2026.json
```

All cycle registers live in:

```
data/registers/
```

---

## 4. Register Structure

Cycle Registers share the same schema as Weekly and Monthly Registers.

### Example (partial)

```json
{
  "id": "cycle-8",
  "range_start": "2025-11-30",
  "range_end": "2025-12-14",

  "days": [
    "2025-11-30",
    "2025-12-01",
    "2025-12-02",
    "..."
  ],

  "fieldstates": [
    "fieldstate-2025-11-30",
    "fieldstate-2025-12-01",
    "..."
  ],

  "event_count": 84,

  "channels": {
    "macro-field": 29,
    "governance": 11,
    "ai-infra": 5
  },

  "vectors": {
    "continuity": 63,
    "exposure": 61,
    "signal": 57,
    "alignment": 36,
    "inversion": 44
  },

  "laws": {
    "FL-12": 84,
    "FL-13": 84,
    "FL-06": 81,
    "FL-09": 27
  },

  "status": "complete",

  "summary": {
    "notes": "Auto-generated Cycle Register; aggregates FieldState counts only.",
    "dominant_themes": ["continuity", "exposure", "inversion"]
  }
}
```

### Core fields

| Field                           | Purpose                                        |
| ------------------------------- | ---------------------------------------------- |
| `range_start` / `range_end`     | Explicit cycle boundaries                      |
| `days`                          | Days for which FieldStates exist in that range |
| `fieldstates`                   | The list of included FieldState IDs            |
| `event_count`                   | Total events across cycle                      |
| `channels` / `vectors` / `laws` | Frequency aggregates                           |
| `dominant_themes`               | Top 3 most frequent vectors                    |

---

## 5. Generation Logic

Cycle Registers are produced by a dedicated script:

```
scripts/close_cycle.py
```

Usage:

```bash
python scripts/close_cycle.py cycle-8 2025-11-30 2025-12-14
```

The script:

1. Accepts a cycle ID and start/end dates
2. Scans `data/registers/` for FieldState files in that range
3. Performs deterministic aggregation
4. Writes:

```
data/registers/cycle-8.json
```

If the cycle contains no FieldStates, the register is written with:

```
status: "empty"
```

---

## 6. When to Use Cycle Registers

Close a cycle:

* **after the last day of the cycle**
* **after all daily FieldStates have been generated**
* **after related weekly registers close** (recommended but not required)

Cycle Registers are the primary structural window for Runtime logic.

---

## 7. Relationship to Other Layers

### Daily → FieldState

Base data.

### WeeklyRegister

Mid-range smoothing.

### MonthlyRegister

High-altitude temporal grouping.

### CycleRegister

High-altitude **structural grouping**, independent of calendar.

Cycles override calendar boundaries.

---

## 8. Dominant Themes

As with weekly/monthly registers:

* strictly frequency-based
* no weighting
* no interpretation
* ties resolved deterministically

Cycle Registers are simply larger windows.

---

## 9. Lifecycle

1. A cycle is defined externally.
2. Daily FieldStates populate the window.
3. After the end-date is processed, run:

```bash
close_cycle.py
```

4. The register becomes permanent archival structure.

---

## 10. Example Workflow for Cycle 8

### Step 1: Define boundary

Cycle 8 = 2025-11-30 → 2025-12-14

### Step 2: Run daily

Use `run_day_and_week.py` for each day.

### Step 3: On 12/15

```bash
python scripts/close_cycle.py cycle-8 2025-11-30 2025-12-14
```

### Step 4: Archive

System now holds:

```
fieldstate-*.json (daily)
weekly-2025-W48.json, weekly-2025-W49.json (weekly)
monthly-2025-11.json, monthly-2025-12.json (monthly)
cycle-8.json (cycle-level)
```

---

## 11. Future Enhancements

Potential extensions:

* **Cycle clusters** (multi-cycle aggregates)
* **Quarterly registers**
* **Phase registers** (architecture phases)
* **Relative window registers** (e.g., last N days)

The architecture is uniform — any date window can be aggregated.
