# NORE-AI

NORE-AI is the **structural ingestion and validation engine** for the broader NORE Runtime and IL-ARCHON system. Its job is not to interpret, predict, or generate meaning — it provides a **clean, deterministic, schema‑aligned representation of the field**.

It forms **Layer 2** of the full architecture:

* **L4 — IL‑ARCHON** (interpretation, geometry, architecture)
* **L3 — NORE Runtime** (cycles, state, transitions)
* **L2 — NORE-AI** (events, validation, FieldState)
* **L1 — Raw Field Data** (news, signals, sequences, notes)

NORE-AI is intentionally minimal, stable, and mechanical.

---

# Purpose

NORE-AI answers one question:

> **"What happened today, and how can it be expressed structurally without interpretation?"**

It provides:

* deterministic event ingestion
* strict schema validation
* clean FieldState summaries
* register outputs (daily, weekly)
* stable IO and naming conventions
* predictable interfaces for the Runtime layer

It never infers, interprets, ranks, or speculates.

---

# Core Concepts

## **Events (L1 → L2)**

Atomic, timestamped, schema‑validated observations.

Stored in `data/events/YYYY-MM-DD.jsonl`.

Each line is one self‑contained JSON object with:

* id
* timestamp
* channel
* source
* vectors
* optional laws
* text
* optional meta

Events are the raw structure NORE-AI transforms.

---

## **FieldState (Daily Summary)**

A deterministic, non‑interpretive summary of a single day.

Includes:

* event count
* vector frequencies
* channel/source distribution
* earliest/latest timestamps
* event IDs

Written to:

```
data/registers/fieldstate-YYYY-MM-DD.json
```

---

## **Registers (v0.2+)**

Grouped collections of events and derived metadata.

Types:

* daily
* weekly
* cycle windows (future)

Stored in:

```
data/registers/
```

Registers add structure but not interpretation.

---

# Repository Structure

```
├── data/
│   ├── events/        # raw JSONL event files
│   └── registers/     # FieldState + register outputs
├── docs/              # architecture, laws, naming, IO
├── schemas/           # JSON schemas (event, future models)
├── src/
│   └── nore_ai/
│       ├── models/    # Event, FieldState, Register
│       ├── pipeline/  # run-day pipeline
│       ├── io/        # reader/writer modules
│       └── cli/       # nore-ai command
└── tests/             # isolated, deterministic test suite
```

---

# Field Laws

NORE-AI enforces the foundational Field Laws FL‑00 → FL‑12.

These laws:

* restrict what the system is allowed to do
* enforce structural physics
* prevent interpretive drift

They never add meaning — they constrain mechanics.

---

# Naming Conventions

NORE-AI uses strict naming to maintain reproducibility.

### **Events**

`YYYY-MM-DD.jsonl` → each line: `s-YYYY-MM-DD-NN`

### **FieldState**

`fieldstate-YYYY-MM-DD.json`

### **Registers**

`daily-YYYY-MM-DD.json`
`weekly-YYYY-WW.json`

### **Schemas**

`event.schema.json`

Full rules exist in `docs/naming.md`.

---

# IO Rules

IO is:

* deterministic
* atomic
* non-destructive
* schema‑validated

Writers always:

* write to a temp file
* flush + fsync
* atomically rename

Readers always:

* stream JSONL lines
* validate per schema
* accumulate errors without crashing

See `docs/io.md`.

---

# CLI

Primary entrypoint:

```
nore-ai run-day --events data/events/2025-11-16.jsonl
```

Future commands (v0.7+):

* `run-week`
* `run-range`
* `summary`
* `validate-path`

---

# Roadmap (v0.1 → v1.0)

Core progression:

* **v0.1** — Event engine (current)
* **v0.2** — Registers
* **v0.3** — Weekly windows
* **v0.4** — Cycle detection (mechanical)
* **v0.5** — Law activation
* **v0.6** — Multi-day FieldState
* **v0.7** — CLI expansion
* **v0.8** — Runtime bridge
* **v0.9** — Test suite
* **v1.0** — Foundational release

NORE-AI grows in layers — never breaking determinism.

---

# Testing Philosophy

Tests guarantee:

* schema stability
* deterministic FieldState output
* correct IO behavior
* no nondeterminism
* safe evolution of features

Temporary directories are required; tests never touch real data.

See `docs/testing.md`.

---

# Runtime Integration

The Runtime consumes:

* validated Event objects
* FieldState files
* (future) registers, deltas, law maps

NORE-AI never interprets — it provides structure.

See:

* `docs/runtime.md`

---

# Summary

NORE-AI is the **structural backbone** of the NORE system:

* deterministic event pipeline
* strict schema validation
* pure JSON output
* daily FieldState
* register system
* stable directory + naming rules
* atomic IO
* no interpretation

It ensures that everything above it — Runtime (L3) and IL‑ARCHON (L4) — has a clean, reproducible, trustworthy foundation.
