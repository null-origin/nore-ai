# Naming Conventions · Global Naming Rules for IDs, Files, Directories, Fields, Metadata, and Code Symbols In NORE-AI

This document defines the **complete naming rules** used across NORE-AI. These conventions eliminate ambiguity, ensure reproducibility, and prevent drift across events, files, schemas, metadata, models, CLI commands, and code.

All rules here are **strict** and **canonical**.

---

# 1. General Naming Rules
- lowercase unless explicitly required
- hyphens for filenames; underscores for Python variables
- no spaces, camelCase, or StudlyCaps
- no ambiguous abbreviations
- deterministic naming only
- dates and times must follow ISO 8601

---

# 2. Directory Naming
Top-level directories:
```
data/
docs/
schemas/
src/
tests/
```
Rules:
- lowercase
- single word
- no runtime-created directories
- numbers only when semantically required

---

# 3. File Naming Rules

## 3.1 Event Files
Format:
```
YYYY-MM-DD.jsonl
```
Examples:
- `2025-11-16.jsonl`
- `2025-12-04.jsonl`

Rules:
- one day per file
- must match embedded event IDs
- stored in `data/events/`

---

## 3.2 Register Files
Format:
```
<register-type>-YYYY-MM-DD.json
```
Examples:
- `fieldstate-2025-11-16.json`
- `daily-2025-11-16.json`
- `weekly-2025-W47.json`

Stored in:
```
data/registers/
```

---

## 3.3 Schema Files
Format:
```
<name>.schema.json
```
Examples:
- `event.schema.json`

---

## 3.4 Documentation Files
Format:
```
<topic>.md
```
Examples:
- `architecture.md`
- `events.md`
- `vectors.md`
- `laws.md`

Rules:
- lowercase
- hyphens allowed
- atomic topics

---

## 3.5 Python Source Files
Format:
```
snake_case.py
```
Examples:
- `event.py`
- `pipeline.py`
- `writer.py`

---

# 4. Event ID Naming (Authoritative)
Format:
```
s-YYYY-MM-DD-NN
```
Examples:
- `s-2025-11-16-01`
- `s-2025-11-16-17`

Rules:
- must match file date
- sequential, no gaps
- no reuse
- never reference another date

---

# 5. Timestamps
- ISO 8601
- always include timezone offset

Examples:
```
2025-11-16T09:14:30-05:00
2025-12-04T21:08:12.345-05:00
```
Rules:
- no "Z"
- offset required
- must reflect actual event discovery time

---

# 6. Channel Naming
Canonical channels:
```
corporate
economic
sports
music
social
political
personal
system
```
Rules:
- lowercase
- single word
- new channels require documentation update

---

# 7. Source Naming
Examples:
```
cnbc
espn
reuters
pandora
personal
mlb
```
Rules:
- lowercase
- hyphens allowed
- no URLs
- must reflect actual origin

---

# 8. Vector Naming
Rules:
- lowercase
- single word
- structural mechanics only
- must be in `docs/vectors.md`

Examples:
```
exposure
retrieval
collapse
alignment
installation
```
Not allowed:
```
fear
chaos
big event
market shift
```

---

# 9. Law Naming
Format:
```
FL-XX
```
Examples:
- `FL-00`
- `FL-06`

Rules:
- uppercase FL prefix
- zero-padded index
- IDs immutable once created

Law file examples (future):
```
FL-06-exposure.json
```

---

# 10. Metadata Field Naming (`meta`)
Keys use lowercase snake_case:
```
tags
note
window
confidence
priority
```
Values:
- JSON-serializable
- lowercase list items
- no deep nesting (> 2 levels)

Example:
```json
"meta": {
  "tags": ["amazon", "compute"],
  "note": "infrastructure acceleration",
  "window": false
}
```
Not allowed:
```
camelCase
PascalCase
Label With Spaces
```

---

# 11. Register ID Naming
Daily:
```
daily-YYYY-MM-DD
```
Weekly:
```
weekly-YYYY-WW
```
FieldState:
```
fieldstate-YYYY-MM-DD
```
Cycle-level (future):
```
cycle-08-window-01
```
Rules:
- lowercase
- hyphens only
- no underscores

---

# 12. CLI Naming
Commands use hyphenated verbs:
```
nore-ai run-day
```
Flags:
```
--events
-e
```
Rules:
- no underscores
- no camelCase
- commands must be descriptive

---

# 13. Python Code Naming
Modules: `snake_case.py`

Functions: `snake_case`

Classes: `PascalCase`

Constants: `UPPER_SNAKE_CASE`

Variables: `snake_case`

Packages: lowercase `nore_ai`

---

# 14. Summary
NORE-AI naming rules ensure:
- determinism
- clarity
- consistency
- reproducibility
- zero ambiguity

Proper naming guarantees structural coherence across all events, registers, FieldStates, configs, and runtime operations.
