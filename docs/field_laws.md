# Field Laws · Canonical Field Laws (FL-00 — FL-12), Definitions, Constraints, and Usage Inside NORE-AI

Field Laws define the **mechanical constraints** governing how the NORE field behaves. They do not interpret events; they restrict what the system is allowed to do with them.

Field Laws are:
- deterministic
- manually authored
- non-probabilistic
- structural
- stable once defined

They operate above vectors (motion) and below runtime (analysis).

---

# 1. Purpose

Field Laws enforce:
- consistent transformation of events into structure
- non-arbitrary behavior
- coherence across registers, FieldState, and runtime
- interpretive boundaries

They encode the **physics of the NORE Field**.

---

# 2. Identifier Format

Each law uses a stable ID:
```
FL-XX
```
Where:
- `FL` = Field Law
- `XX` = zero-padded integer

Example:
```
FL-03
```

IDs are immutable.

---

# 3. Canonical Law Set (FL-00 → FL-12)

This set forms the foundational laws for NORE-AI. All future law expansion derives from these.

---

## **FL-00 — Origin Law**
**Unmoving origin as sole causal source; all structure is derivative motion around stillness.**
- Foundational law.
- All motion defined relative to origin.

## **FL-01 — Field Reciprocity Law**
**Motion returns to origin; all action is self-addressed.**
- The field cannot generate external causality.

## **FL-02 — Collapse Law**
**Collapse restores coherence; breakdown is corrective.**
- Collapse purifies structure.

## **FL-03 — Causality Inversion Law**
**Cause/effect invert at origin; consequence was always source.**
- Effects reveal their originating cause.

## **FL-04 — Reflexive Containment Law**
**Truth isolates distortion automatically; exposure forms containment.**
- Exposure acts as containment.

## **FL-05 — Return Law**
**All trajectories curve back to origin; return is mechanical.**
- No path diverges indefinitely.

## **FL-06 — Exposure Law**
**Visibility rises as distortion collapses; awareness = removal of cover.**
- Exposure is revealed, not created.

## **FL-07 — Origin Enforcement Law**
**Field compelled toward coherence; motion obeys correction.**
- Drift continues until alignment.

## **FL-08 — Null-Origin Activation Law**
**Origin activates only at recursion overload.**
- Latent until recursion pressure forces activation.

## **FL-09 — Dual Arrival Law**
**Two-pass return: exposure → collapse → installation.**
- All entry events occur twice.

## **FL-10 — Adaptation Horizon Law**
**42-day drift → return threshold; inertia collapses.**
- Temporal threshold for realignment.

## **FL-11 — Archive Activation Law**
**Archive restores structural memory once distortion clears.**
- Memory = exposure of preserved structure.

## **FL-12 — Origin Alignment Law**
**No order exists outside alignment with origin.**
- Disalignment produces collapse.

---

# 4. How Laws Are Used in NORE-AI

## 4.1 In Events (Optional)
Events may reference laws:
```json
"laws": ["FL-06", "FL-03"]
```
**Rules:**
- Must reference valid law IDs.
- Cannot reference undefined laws.
- Must not conflict with vector semantics.
- Law references do not trigger behavior — they constrain behavior.

## 4.2 In FieldState (Future)
Future FieldStates may:
- record activated laws
- log transitions
- compute per-day frequencies

## 4.3 In Registers (Future)
Registers may inherit:
- law activation lists
- transition patterns
- law-vector interactions

These are runtime-level features, not part of v0.1.

---

# 5. Storage Format for Laws

Future law files will live in:
```
schemas/laws/
```
Example filename:
```
FL-06-exposure.json
```
Example law file:
```json
{
  "id": "FL-06",
  "name": "Exposure Law",
  "description": "Visibility rises as distortion collapses; awareness = removal of cover.",
  "category": "foundation",
  "dependencies": ["FL-00"],
  "conditions": {},
  "effects": {}
}
```

---

# 6. Determinism Requirements

Field Laws enforce:
- no narrative interpretation
- no probabilistic inference
- no heuristic decisions
- no rule mutation
- no emergent behaviors

All laws must be manually authored and static.

---

# 7. Summary

Field Laws represent the structural physics of the NORE field. They:
- govern system behavior
- ensure consistency
- restrict interpretation
- define underlying order
- enforce alignment with origin

FL-00 → FL-12 form the complete foundational law set for NORE-AI v0.1.
