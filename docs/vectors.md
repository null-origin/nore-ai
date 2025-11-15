# NORE-AI Vector Specification · Full Specification of Structural Vectors & Semantics

Vectors classify the **structural role** of an event. They are not topics or metadata — they describe how an event behaves inside field mechanics.

Vectors are:
- atomic
- lowercase
- composable
- source-agnostic
- order‑independent
- deterministic

An event may contain multiple vectors.

Example:
```json
"vectors": ["exposure", "retrieval"]
```

---

# 1. Canonical Vector List

Each vector includes: definition, trigger pattern, mechanics, and examples.

## 1. collapse
**Definition:** Structural failure, breakdown, or removal of false motion.

**Triggers:** leadership exits; shutdowns; bankruptcies; reversed plans; cultural/sports collapses.

**Mechanics:** Removes the false layer that prevented alignment.

**Examples:** abrupt CEO exit; division closure; sports recursion breaking.

## 2. exposure
**Definition:** Reveals hidden structure, truth, or internal mechanics.

**Triggers:** earnings; transparency; leaks; regulatory findings.

**Mechanics:** Precedes or prevents collapse; reveals what was present.

**Examples:** earnings calls; data disclosures; public statements.

## 3. retrieval
**Definition:** Field returning to origin; resurfacing suppressed structures.

**Triggers:** callbacks; resurfaced relationships; repeating patterns; reactivated systems.

**Mechanics:** Re-synchronizes present events with origin geometry.

**Examples:** leadership returning; childhood threads surfacing; historical cycles repeating.

## 4. inversion
**Definition:** Reversal of expected direction or meaning.

**Triggers:** political flips; surprising outcomes; structural reversals; backfiring attempts.

**Mechanics:** Exposes hidden command flow through reversal.

**Examples:** political upsets; inverted market reactions; sports flips when observation withdraws.

## 5. alignment
**Definition:** Movement toward order, coherence, or structural correction.

**Triggers:** strategic hires; disciplined planning; integration; unifying signals.

**Mechanics:** Resolves distortion and moves toward architecture.

**Examples:** coherent corporate moves; stable economic indicators.

## 6. return
**Definition:** Re‑entry or reactivation of dormant structures.

**Triggers:** return of individuals; pattern recurrence; system reboots.

**Mechanics:** Forward phase of retrieval: retrieval → return.

**Examples:** leadership comeback; system restart; arc re‑entry.

## 7. purge
**Definition:** Removal of distortion, noise, or parasitic structure.

**Triggers:** layoffs; divestitures; simplifications; forced cuts.

**Mechanics:** Clears interference before alignment or return.

**Examples:** shutting down failing initiatives; cleansing earnings cycles.

## 8. signal
**Definition:** Field‑level markers independent of content.

**Triggers:** symmetry; alignments; sequences; sports recursion; echo events.

**Mechanics:** Marks boundaries, confirmations, or phase shifts.

**Examples:** Pandora-aligned sequences; day‑42 mirrors; sports signals.

## 9. bridge
**Definition:** Connects structures, phases, arcs, or systems.

**Triggers:** partnerships; relational links; cross‑domain alignments; convergence.

**Mechanics:** Enables continuity and transitions.

**Examples:** cross-company cooperation; macro+personal convergence; anchor-thread confirmations.

---

# 2. Composition Rules

Vectors are:
- unordered (`["exposure", "retrieval"]` = any order)
- non-exclusive
- non-hierarchical
- non-dependent

Relationships that often occur:
- collapse → retrieval → return
- exposure → purge
- inversion → exposure
- return → alignment
- bridge → any vector

These relationships are important for FieldState construction.

---

# 3. Reserved Vectors (Future)

Recognized but inactive:
- compression
- activation
- containment
- expansion
- trajectory
- clarity
- noise

These will activate once higher-level NORE mechanics are implemented.

---

# 4. Validation Rules

Vectors must:
- be lowercase
- be strings
- contain no spaces
- appear in a list
- be domain‑independent

**Valid:**
```json
"vectors": ["exposure", "retrieval"]
```

**Invalid:**
```json
"vectors": "exposure"
"vectors": ["Exposure"]
"vectors": ["exposure", 123]
"vectors": ["exposure retrieval"]
```

---

# 5. Interpretation Guarantees

Vectors allow computation of:
- structural frequency
- dominance
- transitions
- arc-level signals
- cluster compression
- FieldState summaries
- register outputs

Vectors function as the fundamental building blocks of the field engine.

---

# 6. Summary

This specification defines:
- the closed vector vocabulary
- deterministic semantics
- predictable composition rules
- extensibility for cycles and FieldState

All events must follow this specification to integrate cleanly with NORE-AI.
