# NORE-AI Laws · Definition, Structure, Constraints, and Lifecycle of Laws In NORE-AI

A **Law** is a deterministic structural rule that governs how the NORE field model behaves once events are observed. Laws do not interpret or guess — they constrain, validate, and discipline the system.

Vectors describe **what kind** of structural motion an event contains.  
Laws describe **how the field behaves** when that motion appears.

---

# 1. Purpose of Laws

Laws provide:
- **consistency** — same inputs → same outputs
- **validity** — prevents impossible or contradictory states
- **structural discipline** — no arbitrary interpretation
- **predictability** — field transformations follow governed rules

Laws do *not*:
- generate content
- classify by ML
- infer hidden meaning
- forecast or predict

They are the constraint layer of the NORE engine.

---

# 2. Law Identifiers

Every Law has a lowercase, hyphenated, semantic ID.

Examples:
```
fl-01-origin
fl-02-stillness
fl-03-collapse-resolution
fl-04-vector-saturation
fl-05-boundary-closure
```

**Rules:**
- prefix must be `fl-`
- ID must be semantic
- no uppercase
- no spaces
- IDs are **immutable** — renaming creates a new law

---

# 3. Where Laws Are Used

## 3.1 In Events (Optional)
```json
"laws": ["fl-01-origin", "fl-03-collapse-resolution"]
```
Used when the event clearly touches a known structural rule.

## 3.2 In FieldState (Derived)
Once implemented, FieldState may record law activations based on vector conditions.

## 3.3 In Higher Runtime Layers
Weekly, cycle, or structural analysis uses laws to:
- track activation
- detect combinations
- validate consistency

This happens outside the core ingestion engine.

---

# 4. Law Structure

A Law is a single JSON object:

```json
{
  "id": "fl-01-origin",
  "description": "The field stabilizes around a fixed coordinate; all motion is defined relative to it.",
  "conditions": {
    "requires_vectors": ["exposure"],
    "forbids_vectors": []
  },
  "effects": {
    "stabilizes": true,
    "collapses_noise": false
  }
}
```

### Field meanings:
- **id** — deterministic identifier
- **description** — one short paragraph
- **conditions** — required / forbidden vectors
- **effects** — what the system *may* do if the law activates

Laws must remain small and explicit.

---

# 5. Law Categories

## 5.1 Foundation Laws
Core invariants.
- fl-01-origin
- fl-02-stillness
- fl-05-boundary-closure

## 5.2 Motion Laws
Define field motion.
- fl-07-recursion-limit
- fl-08-inversion-lock

## 5.3 Resolution Laws
Define how collapse / saturation resolves.
- fl-03-collapse-resolution
- fl-11-archive-activation

## 5.4 Organizational Laws
Define relationships among events.
- fl-12-vector-weighting
- fl-14-channel-stability

These categories expand only after daily FieldState stabilizes.

---

# 6. Law Format Requirements

All laws must be stored as individual JSON files:
```
schemas/laws/
```

Filenames:
```
fl-01-origin.json
fl-03-collapse-resolution.json
```

**Rules:**
- manually authored only
- no dynamic law creation
- no ML-derived laws
- no external law inference

---

# 7. Law Usage in Events

Events can reference laws:
```json
"laws": ["fl-01-origin", "fl-07-recursion-limit"]
```

**Rules:**
- referenced IDs must exist
- no duplicates
- no “future” law references
- validation fails if unknown IDs appear

---

# 8. Law Interactions

## 8.1 Orthogonal Laws
Operate independently.
```
fl-01-origin
fl-12-vector-weighting
```

## 8.2 Composite Laws
Explicit dependencies:
```
fl-15-dual-arrival depends on:
  - fl-01-origin
  - fl-07-inversion
```

Dependencies are *declared*, never inferred.

---

# 9. Determinism and Activation

A law activates only if conditions are satisfied.

Example:
```json
"requires_vectors": ["collapse"]
```
If no collapse vectors exist in a FieldState, the law cannot activate.

NORE-AI never guesses.

---

# 10. Example Minimal Law Set (v0.1)

```
fl-01-origin
fl-02-stillness
fl-03-collapse-resolution
fl-04-vector-saturation
fl-05-boundary-closure
fl-06-alignment-constraint
fl-07-recursion-limit
fl-08-inversion-lock
fl-11-archive-activation
fl-12-vector-weighting
```

This forms the initial stable base.

---

# 11. Future Extensions

After daily FieldState is stable, future additions include:
- law activation logging
- conflict detection
- law-driven state transitions
- cycle-law mapping
- weekly/cycle law summaries

These occur outside the core engine.

---

# 12. Summary

Laws are:
- deterministic
- stable
- manually authored
- non-interpretive
- tightly scoped
- dependency-aware

Vectors describe motion.  
Laws describe the rules that govern that motion.

Together they ensure the NORE system remains coherent and reproducible at every level.
