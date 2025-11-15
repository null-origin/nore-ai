# **Testing Guide for NORE-AI**

This document defines the **testing philosophy**, **test categories**, **required coverage**, and **invariants** for NORE-AI.

Tests ensure that NORE-AI remains:

* deterministic
* stable across versions
* regression-resistant
* schema-aligned
* IO-consistent
* integration-safe for the NORE Runtime and IL-ARCHON layers

Testing exists to *preserve the architecture* — not to chase edge cases.

---

# **1. Test Philosophy**

NORE-AI tests obey four core principles.

## **1. Determinism**

Given the same input, the system must always produce the same output.

## **2. Purity**

Tests treat the system as pure functions:
*(raw events) → (validated events + FieldState)*

No test relies on:

* external APIs
* environment variables
* system time
* randomness

## **3. Isolation**

Tests must not interact with:

* real `data/events`
* real `data/registers`
* production schemas

Temporary, throwaway directories must be used.

## **4. Minimality**

Tests are small, direct, and structural:

* no heavy mocking
* no complex fixtures
* no large datasets

The purpose is to verify *structure*, not behavior outside scope.

---

# **2. Test Directory Layout**

All tests live under:

```
tests/
```

Recommended structure:

```
tests/
  test_event_model.py
  test_pipeline.py
  test_fieldstate.py
  test_registers.py (v0.2+)
  test_weekly.py (v0.3+)
  test_cycles.py (v0.4+)
  test_law_activation.py (v0.5+)
  test_cli.py (v0.7+)
  utils/
    tempdir.py
    helpers.py
```

Only the first two files are required initially; additional files appear as features expand.

---

# **3. Required Test Categories**

Each version of NORE-AI must satisfy the following test categories.

---

## **3.1 Model Tests (v0.1+)**

Covers:

* Event dataclass
* FieldState dataclass
* Register models (v0.2+)

Tests must verify:

* correct object construction
* type constraints
* stable `.to_dict()` output
* no missing required fields
* deterministic ordering

---

## **3.2 Schema Validation Tests (v0.1+)**

Ensure the schema rejects:

* missing fields
* wrong types
* invalid event IDs
* invalid timestamps
* empty vectors array
* extra illegal fields

Schema tests must verify:

* valid events pass cleanly
* errors accumulate without crashing

---

## **3.3 Pipeline Tests (v0.1+)**

Test the `run_day_pipeline` logic:

* valid event → included
* invalid event → returned in error list
* mixed inputs → both lists populated
* malformed JSON does not crash
* correct event count
* preserved deterministic ordering

---

## **3.4 IO Tests (v0.2+)**

Verify:

* atomic write pattern
* correct output paths
* stable JSON formatting
* no mutation during serialization
* overwrite behavior allowed

No test ever writes to real `data/`.

---

## **3.5 Register Tests (v0.2+)**

Test:

* DailyRegister
* SummaryRegister
* serialization format
* field name stability
* deterministic ordering

---

## **3.6 Weekly Window Tests (v0.3+)**

Covers:

* merging 7 days of FieldState
* vector & law aggregation
* earliest/latest timestamps
* delta computations
* weekly register generation

All must remain purely mechanical.

---

## **3.7 Cycle Detection Tests (v0.4+)**

Test mechanical cycle logic:

* exposure spikes
* collapse clusters
* transition points
* rule-based thresholds
* deterministic naming of cycle windows

No interpretive logic is ever tested.

---

## **3.8 Law Activation Tests (v0.5+)**

Ensure:

* correct frequency counting
* multi-day streak detection
* law-transition identification
* deterministic outputs

No inference tests — strictly observed activation.

---

## **3.9 CLI Tests (v0.7+)**

Covers:

* CLI parsing
* run-day with config
* run-day with `--events` shortcut
* error output text
* consistent behavior across runs

---

# **4. Test Tools and Utilities**

## **4.1 Temporary Directory Utility**

All write tests use:

```python
import tempfile
```

or the helper:

```python
from tests.utils.tempdir import temp_dir
```

Tests must never touch real repository paths.

## **4.2 Helper Functions**

Recommended helpers:

* `make_event_line(...)`
* `write_jsonl(path, lines)`
* `load_json(path)`
* `assert_same_dict(a, b)`

These enforce consistent formatting.

---

# **5. Snapshot Tests (Optional v0.9+)**

Snapshots confirm:

* stable FieldState structure
* stable register output
* stable JSON ordering

Snapshots must be small and tightly scoped.

---

# **6. Test Invariants**

These invariants must remain unbroken across all versions.

## **6.1 No Nondeterminism**

Tests must not depend on:

* current time
* randomness
* machine-specific paths

## **6.2 Schema Stability**

Required fields remain required.

## **6.3 Input Immutability**

Events are strictly read-only.

## **6.4 JSON Stability**

Output spacing, ordering, and formatting remain consistent.

## **6.5 File Safety**

Tests must confirm:

* atomic writes
* no partial output
* no directory side effects

---

# **7. Coverage Targets**

(Minimum required starting v0.9)

* 90% model coverage
* 100% schema logic
* 100% pipeline logic
* 90% FieldState
* 75% registers & weekly windows
* 75% CLI
* 100% invariants

Coverage numbers enforce structural reliability, not metric chasing.

---

# **8. Running Tests**

Run full suite:

```
python -m unittest
```

Run a single file:

```
python -m unittest tests.test_pipeline
```

Verbose mode:

```
python -m unittest -v
```

---

# **9. Summary**

Tests in NORE-AI:

* protect the architecture
* preserve determinism
* detect regressions
* enforce schema stability
* validate IO safety
* support safe evolution toward v1.0

The test suite is not decorative — it is the structural foundation ensuring coherence throughout the NORE Runtime and IL-ARCHON layers.
