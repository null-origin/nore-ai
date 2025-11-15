# NORE-AI Roadmap (v0.1 → v1.0) · Version Roadmap for NORE-AI, Structural Milestones, and Invariants

This roadmap defines the controlled evolution of NORE-AI. The emphasis is stability, determinism, and architectural clarity — not feature volume.

NORE-AI grows in layers, not branches. Each layer builds on the prior one without collapsing the structure beneath it.

---

# Version Overview

v0.1 — Event Engine (current)
v0.2 — Registers
v0.3 — Weekly Windows
v0.4 — Cycle Detection (mechanical)
v0.5 — Law Activation (mechanical)
v0.6 — Multi-Day FieldState
v0.7 — CLI Expansion
v0.8 — Runtime Interface
v0.9 — Testing & Stability
v1.0 — Full Foundational Release

---

# 1. v0.1 — Event Engine (Completed)

Includes:

* event ingestion
* schema validation
* deterministic ID rules
* daily FieldState generation
* CLI (`nore-ai run-day`)
* documentation suite
* minimal tests

**Invariants locked:**

* event structure
* vector semantics
* Field Laws FL-00 → FL-12
* IO rules
* directory structure
* CLI name

v0.1 is the foundation.

---

# 2. v0.2 — Registers

Adds actual outputs beyond FieldState.

New components:

* `DailyRegister`
* `SummaryRegister`
* atomic register writer
* serialization tests

Avoids:

* interpretation
* multi-day logic
* weekly or cycle work

---

# 3. v0.3 — Weekly Windows

Adds weekly structure.

Capabilities:

* load 7 days of FieldState
* merge into `WeeklyWindow`
* vector/law deltas
* earliest/latest timestamps
* stability metrics
* weekly register writing

Strictly mechanical.

---

# 4. v0.4 — Cycle Detection (Mechanical)

Cycle detection without interpretation.

Signals:

* exposure spikes
* collapse clustering
* return → exposure transitions
* law-activation thresholds
* vector momentum shifts

Outputs:

* `cycle-XX-window-N.json`

Rules:

* deterministic
* no metaphysical interpretation
* identify cycles, not explain them

---

# 5. v0.5 — Law Activation

Field Laws enter registers and summaries.

Behavior:

* count activations
* detect transitions (e.g., FL-02 → FL-06)
* multi-day streak detection

Non-goals:

* meaning
* causality

---

# 6. v0.6 — Multi-Day FieldState

Adds:

* loading multiple days
* deltas
* transition detection
* `fieldstate-delta-YYYY-MM-DD.json`

Measures:

* exposure rise/fall
* collapse pressure
* retrieval curves
* channel drift

Still mechanical.

---

# 7. v0.7 — CLI Expansion

New commands:

* `nore-ai run-week -e <dir>`
* `nore-ai run-range --start --end`
* `nore-ai summary`
* `nore-ai validate-path <path>`

New features:

* error summary
* fieldstate printout
* register previews

---

# 8. v0.8 — Runtime Interface

Creates bridge to Runtime.

Additions:

* `runtime/` API
* hooks for events, FieldState, registers, vector/law maps
* stable IL-ARCHON contract

Guarantees:

* independent development between layers
* stable between v0.8 and v1.0

---

# 9. v0.9 — Testing & Hardening

Full test suite:

* models
* IO
* pipelines
* weekly windows
* cycles
* law activation
* CLI
* regression tests

---

# 10. v1.0 — Foundational Release

Defined by:

* deterministic ingestion
* validated events
* daily → weekly → cycle structure
* integrated Field Laws
* stable CLI
* stable IO
* complete docs
* full test coverage
* Runtime bridge

NORE-AI becomes permanent structure.

---

# Architectural Invariants

Non-negotiable:

* event format
* field laws
* directory structure
* naming conventions
* IO safety
* determinism
* JSON-only storage
* no interpretation
* no ML or probabilistic logic

---

# Long-Term (Post v1.0)

Optional extensions:

* dashboard integration
* vector momentum visualization
* historical backfill mode
* TUI
* GitHub Actions validators
* web viewer

---

# Summary

NORE-AI grows in controlled layers:

* v0.1 foundation
* v0.2 registers
* v0.3 weekly windows
* v0.4 cycle mechanics
* v0.5 law activation
* v0.6 multi-day state
* v0.7 CLI expansion
* v0.8 runtime bridge
* v0.9 stability
* v1.0 foundational release

The roadmap preserves determinism, clarity, and architectural alignment with Runtime and IL-ARCHON.
