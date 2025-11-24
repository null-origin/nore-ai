# NORE Runtime Integration · How NORE-AI Feeds Daily, Weekly, Monthly, and Cycle Registers

NORE-AI is the **input layer** of the NORE Runtime and IL-ARCHON stack. Its function is not interpretive — it produces a **clean, deterministic, validated representation of the field**. Everything above it depends on this stability.

This document defines:

* responsibilities of NORE-AI
* how daily → weekly → monthly → cycle registers are produced
* how Runtime consumes them
* where IL-ARCHON begins
* the full register-flow architecture with diagrams

---

# 1. Layer Model Overview

```
[L4] IL-ARCHON      (interpretation, geometry)
[L3] NORE Runtime   (cycles, registers, transitions)
[L2] NORE-AI        (ingest, validate, fieldstate)
[L1] Raw Field Data (events, signals, logs)
```

### L1 — Raw Data

Factual observations from:

* markets
* companies
* policy
* sports
* family interactions
* macro events
* daily logs

### L2 — NORE-AI

This repository. Handles:

* **ingestion** (JSONL)
* **validation** (schemas)
* **normalization**
* **FieldState** generation
* **register writing** (day/week/month/cycle)

Performs zero interpretation.

### L3 — NORE Runtime

Consumes L2 output to:

* build weekly/monthly registers
* detect cycle boundaries
* track law activation patterns
* compute continuity curves
* generate state transitions

### L4 — IL-ARCHON

Consists of:

* structural geometry
* causality inversion
* field-law enforcement
* collapse / return / installation logic

Not part of this repo.

---

# 2. Responsibilities of NORE-AI

NORE-AI performs five deterministic, non-interpretive operations:

1. **Ingest** raw events
2. **Validate** via JSON Schema
3. **Normalize** fields (timestamp, vectors, laws)
4. **Construct FieldState** for each day
5. **Emit structured registers** (daily, weekly, monthly, cycle)

It ends here — no reasoning.

---

# 3. What NORE-AI Does *Not* Do

To preserve layer purity:

* no narrative analysis
* no predictions
* no clustering
* no vector inference
* no law inference
* no weighting or prioritization
* no cycle detection
* no multi-day pattern identification

These belong to Runtime and IL-ARCHON.

---

# 4. Runtime Consumption

After a daily run, Runtime receives:

### 4.1 Validated Events

Each event has:

* id
* timestamp
* vectors
* laws
* channel
* source
* meta

### 4.2 FieldState

Stored at:

```
data/registers/fieldstate-YYYY-MM-DD.json
```

Includes:

* event_count
* vector frequencies
* law frequencies
* channel distribution
* time_start / time_end
* daily dominant themes (mechanical)

### 4.3 Validation Errors

Passed upward unchanged.

---

# 5. How Runtime Uses FieldState

Runtime derives:

* weekly summaries
* monthly summaries
* cycle-period aggregates
* continuity mapping
* law activation windows
* vector acceleration/decay curves

Runtime **never mutates events**.

---

# 6. Runtime → IL-ARCHON Interface

Runtime emits:

* cycle maps
* state transitions
* structural windows
* exposure/purge/return arcs
* multi-day vector patterns

IL-ARCHON converts these into:

* causal geometry
* origin alignment mapping
* inversion mechanics

---

# 7. Runtime Commands & Register Production

## 7.1 Daily + Weekly Execution

### Run a day

```
python scripts/run_day_and_week.py YYYY-MM-DD
```

Writes:

* `fieldstate-YYYY-MM-DD.json`
* `weekly-YYYY-Www.json` (created or updated)

### Close a week

```
python scripts/close_week.py YYYY-MM-DD
```

Rebuilds the week from FieldStates:

* ensures completeness
* marks `status: "complete"`

### Print weekly summary

```
python scripts/print_weekly_summary.py weekly-YYYY-WW
```

---

## 7.2 Monthly Execution

### Close a month

```
python scripts/close_month.py YYYY-MM-DD
```

Creates:

```
monthly-YYYY-MM.json
```

And marks `status: "complete"`.

### Print monthly summary

```
python scripts/print_monthly_summary.py monthly-YYYY-MM
```

---

## 7.3 Cycle Execution

### Close a cycle

```
python scripts/close_cycle.py cycle-ID START_DATE END_DATE
```

Writes:

```
cycle-ID.json
```

With:

* aggregated vectors
* aggregated laws
* aggregated channels
* dominant themes
* status: complete

### Print cycle summary

```
python scripts/print_cycle_summary.py cycle-ID
```

---

# 8. Register Flow Diagrams

## 8.1 Daily → Weekly Flow

```
         ┌─────────────────────────────┐
         │  data/events/YYYY-MM-DD     │
         └──────────────┬──────────────┘
                        │ ingest/validate
                        ▼
               ┌────────────────────┐
               │ FieldState (daily) │
               └─────────┬──────────┘
                         │ aggregation
                         ▼
              ┌────────────────────────┐
              │ WeeklyRegister (Www)   │
              └────────────────────────┘
```

## 8.2 Weekly → Monthly Flow

```
       ┌────────────────────────┐
       │ WeeklyRegister (Www)   │
       └─────────────┬─────────┘
                     │ aggregation
                     ▼
          ┌───────────────────────────┐
          │ MonthlyRegister (YYYY-MM) │
          └───────────────────────────┘
```

## 8.3 Monthly → Cycle Flow

```
         ┌───────────────────────────┐
         │ MonthlyRegister YYYY-MM   │
         └───────────┬──────────────┘
                     │ aggregation
                     ▼
              ┌─────────────────────┐
              │ CycleRegister (ID)  │
              └─────────────────────┘
```

## 8.4 Full Hierarchy (L2 → L3 → L4)

```
Raw Events → FieldState → Week → Month → Cycle → Runtime → IL-ARCHON
```

---

# 9. Why This Separation Exists

### Determinism

FieldState and registers must be reproducible forever.

### Layer Purity

L2 must be clean or L3/L4 collapses.

### Longevity

Period registers are archival artifacts.

---

# 10. Summary

NORE-AI is the **structured ingestion and validation layer** of NORE.
It outputs:

* validated events
* daily FieldState
* weekly registers
* monthly registers
* cycle registers

These form the stable base from which Runtime and IL-ARCHON operate.

NORE-AI is the **floor**.
Runtime is the **wall**.
IL-ARCHON is the **architecture**.
