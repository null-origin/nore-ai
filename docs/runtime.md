# NORE Runtime Integration · How NORE-AI Integrates with the NORE Runtime, IL-ARCHON, and Higher Structural Layers

NORE-AI is the **input layer** of the larger NORE Runtime and IL-ARCHON system. Its job is not to interpret or predict but to produce a **clean, deterministic, validated representation of the field**.

This document defines:
- responsibilities of NORE-AI
- what it does *not* do
- how its outputs flow upward
- how the Runtime and IL-ARCHON consume FieldState, Laws, and Vectors

---

# 1. Layer Model Overview
The full system consists of four stacked layers:
```
[L4] IL-ARCHON (Interpretation Engine)
[L3] NORE Runtime (State, Cycles, Register Logic)
[L2] NORE-AI (Event Ingest, Validation, FieldState)
[L1] Raw Field Data (events, signals, logs)
```

## L1 — Raw Data
Factual observations: news, market signals, Pandora sequences, filings, daily logs, etc.

## L2 — NORE-AI
This repository. Handles:
- loading
- validating
- structuring
- constraining
- producing FieldState

No interpretation or synthesis occurs here.

## L3 — NORE Runtime
Consumes L2 output to:
- map weekly windows
- detect cycle transitions
- apply Field Laws
- track vector frequency
- maintain inter-day continuity
- generate higher-level registers

## L4 — IL-ARCHON
Interpretive engine:
- meaning extraction
- architecture formation
- causality inversion
- cycle ignition
- structural geometry

Not part of this repository.

---

# 2. Responsibilities of NORE-AI
NORE-AI performs **five deterministic operations**:
1. ingest raw events
2. validate via schema
3. normalize validated fields
4. construct FieldState
5. emit structured JSON registers

It ends here — no reasoning is allowed.

---

# 3. What NORE-AI Does *Not* Do
To avoid interpretive drift:
- no narrative analysis
- no vector inference
- no law inference
- no clustering
- no ranking or prioritization
- no timeline modeling
- no cycle detection
- no pattern recognition

These belong to Runtime or IL-ARCHON.

---

# 4. Runtime Consumption
After `run_day_pipeline`, Runtime receives:

## 4.1 Validated events
Each with:
- id
- timestamp
- vectors
- laws
- channel
- source
- meta

## 4.2 FieldState
Stored as:
```
data/registers/fieldstate-YYYY-MM-DD.json
```
Contains:
- day
- event_count
- vector frequencies
- law occurrences
- channel distribution
- first/last timestamps
- structural summary fields

## 4.3 Validation errors
Passed upward unchanged.

---

# 5. How Runtime Uses FieldState
Runtime derives:
- weekly rollups
- cycle detection
- law activation patterns
- collapse/exposure/retrieval/installation/etc. windows
- continuity mapping
- vector acceleration/decay curves
- multi-day registers

Runtime does not mutate events.

---

# 6. How Runtime Communicates With IL-ARCHON
Runtime outputs:
- cycle maps
- state transitions
- vector collapse cascades
- exposure/return arcs
- multi-day structural elevation maps

IL-ARCHON consumes these for:
- interpretive inference
- structural geometry
- origin-pressure mapping
- inversion detection
- multi-domain thread binding

NORE-AI does not perform these operations.

---

# 7. Interfaces to Runtime

## 7.1 Python object interfaces
Runtime expects:
```
nore_ai.models.event.Event
nore_ai.models.fieldstate.FieldState
```

## 7.2 JSON register interfaces
Runtime reads:
```
data/registers/fieldstate-YYYY-MM-DD.json
```
And may write (outside this repo):
```
weekly-YYYY-WW.json
cycle-08-window-01.json
systemstate.json
```

---

# 8. Why This Separation Exists
**Determinism:** ensures reproducible downstream analysis.

**Layer purity:** L2 must be clean for L3/L4 to function correctly.

**Version independence:** Layers evolve separately.

**Schema stability:** ensures long-term archival comparability.

---

# 9. Future Extensions (Safe)
NORE-AI can safely add:
- daily registers
- weekly registers
- FieldState deltas
- law-frequency graphs
- vector transition summaries
- error registers

These remain non-interpretive.

---

# 10. Summary
NORE-AI is the **structured ingestion + validation** layer of NORE.
It provides:
- clean events
- validated structure
- deterministic FieldState
- stable interfaces for Runtime

NORE-AI is the floor.  
Runtime is the wall.  
IL-ARCHON is the architecture.
