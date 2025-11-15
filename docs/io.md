# IO Conventions (Input / Output) · Rules for Loading, Validating, Serializing, and Writing Data In NORE-AI

This document defines the **I/O rules** for NORE-AI. All input/output is:
- deterministic
- minimal
- schema-validated
- non-interactive
- free of side effects

These rules govern how events are loaded, validated, serialized, written, and stored.

---

# 1. IO Philosophy
NORE-AI treats IO as strictly mechanical:
- no unpredictable directory creation
- no modification of existing data files
- no runtime timestamps
- no external API calls
- no randomness

Given the same inputs, IO must always produce the same outputs.

---

# 2. Event Loading (JSONL)

## 2.1 Input Format
Events are loaded from:
```
data/events/YYYY-MM-DD.jsonl
```
Each line = one complete event.

## 2.2 Loading Rules
- stream line-by-line
- ignore empty lines
- malformed JSON triggers a validation error

## 2.3 Error Conditions
Errors may include:
- malformed JSON
- missing fields
- invalid types
- date mismatches between ID and filename
- empty/invalid vectors
- non-ISO timestamps

Errors must accumulate but not stop processing.

---

# 3. Schema Validation
Schema file:
```
schemas/event.schema.json
```
Validation uses JSON Schema.

Rules:
- all required fields validated
- unknown fields allowed (forward compatible)
- validation errors **do not raise** — they accumulate in an error list

If any invalid event exists, the pipeline prints:
```
validation errors: <N>
```
Current v0.1 behavior: no register/FieldState is written if errors occur.

---

# 4. Writing Registers and FieldState

## 4.1 Output Directory
All write operations target:
```
data/registers/
```
Directory must already exist.

## 4.2 Serialization Format
All register and FieldState outputs:
- formatted JSON
- 2-space indentation
- stable key ordering
- valid UTF-8
- newline at EOF

## 4.3 Overwriting Rules
- overwriting existing files is allowed
- no backup files created
- writes must be atomic (temp → fsync → rename)

## 4.4 File Naming
```
fieldstate-YYYY-MM-DD.json
daily-YYYY-MM-DD.json
weekly-YYYY-WW.json
```
Write failures abort the pipeline.

---

# 5. Serialization Rules (JSON)
Allowed JSON types:
- strings
- numbers
- booleans
- lists
- dictionaries

Not allowed:
- NaN / Infinity
- datetime objects (must be converted to strings)
- Python objects

Dataclasses must implement deterministic `to_dict()` serialization.

---

# 6. Writer Behavior
The future module `nore_ai.io.writer` must:
- never introduce new fields
- never mutate event objects
- write files atomically
- preserve list order
- pretty-print JSON registers only (not JSONL)

Safe write pattern:
```
file.tmp → fsync → rename to final
```

---

# 7. Read/Write Determinism
Given identical:
- event file
- schema
- pipeline code

NORE-AI must:
- load events identically
- validate identically
- produce identical FieldState
- serialize identical registers

Any nondeterminism = bug.

---

# 8. Standardized IO Errors
Errors use predictable shapes:

## 8.1 FileNotFound
```
{"error": "file_not_found", "path": "<path>"}
```

## 8.2 JSONDecodeError
```
{"error": "json_decode_error", "line": <line_number>}
```

## 8.3 SchemaValidationError
```
{"error": "schema_validation_error", "id": "<event_id>", "message": "<reason>"}
```

## 8.4 WriteError
```
{"error": "write_error", "path": "<path>"}
```

Errors must not crash the process.

---

# 9. IO Separation Principle
NORE-AI separates:
- IO
- validation
- transformation
- summarization

No stage may leak into another:
- IO does not validate
- validation does not write files
- summarization does not mutate events

---

# 10. Test Environment Behavior
Tests must:
- use temporary dirs
- avoid real data
- write only to `tmp/` or Python `tempfile`
- treat IO as disposable

Tests should assert:
- correct loading behavior
- schema validation
- serialization accuracy
- atomic write integrity
- accurate error reporting

---

# 11. Summary
The IO layer enforces:
- deterministic loading
- strict schema alignment
- atomic writes
- consistent serialization
- disciplined directory behavior
- reproducible output

IO is a mechanical bridge:
```
(raw files) → (validated events) → (registers + FieldState)
```
Its stability ensures the entire NORE runtime behaves predictably.
