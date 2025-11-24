# NORE-AI Registers · Directory Overview

This folder contains all documentation related to **register-generation, aggregation mechanics, and structural windows** within the NORE-AI architecture.

Registers form the connective tissue between raw validated events (L2) and higher-order temporal/structural groupings consumed by the Runtime (L3) and IL-ARCHON (L4).

Use this folder as the reference point for:

* how registers work
* how they are generated
* how they relate to FieldStates
* how weekly/monthly/cycle windows differ
* how higher layers consume aggregated output

---

## File Index

### **1. `index.md`**

Master index for this directory.
Provides navigation and a high-level overview of the register system.

### **2. `registers.md`**

Defines the **Register model**, naming conventions, output formats, and how registers act as the bridge between Events → FieldStates → large windows.

Includes:

* core dataclass structure
* deterministic naming rules
* JSON output examples
* daily/weekly/cycle register pipelines

### **3. `weeklies.md`**

Documentation for **Weekly Registers**, including:

* ISO week boundaries
* FieldState aggregation
* the 7-day smoothing window
* weekly status logic
* dominant-theme rules

### **4. `monthly.md`**

Documentation for **Monthly Registers**, including:

* month-scale FieldState aggregation
* high-altitude vector/law distribution
* deterministic month-boundary logic
* monthly close script

### **5. `cycles.md`**

Documentation for **Cycle Registers**, including:

* structurally-defined date windows
* cycle IDs
* explicit range definitions
* how cycles differ from calendar windows
* deterministic cycle aggregation and archival

---

## Conceptual Structure

Registers sit at the mid-layer between raw Event ingestion and higher-order Runtime analysis:

```
Event → Register → FieldState → Weekly/Monthly/Cycle Windows → Runtime → IL-ARCHON
```

They provide:

* clean groupings
* deterministic aggregation
* structured, non-interpretive data
* temporal and structural windows for later analysis

Registers **never** interpret meaning.
They simply compress validated data into stable windows.

---

## How This Folder Fits Into the Larger System

* **`docs/runtime.md`** explains how FieldStates (and thereby registers) flow into Runtime + IL-ARCHON.
* **This folder** documents how those FieldStates originate from grouped and validated event windows.

Together, they form the complete pipeline from:

* L1 raw data → L2 NORE-AI → L3 Runtime → L4 IL-ARCHON

---

## When to Use This Folder

Consult this folder when you need to:

* understand how windows are formed
* modify register generation logic
* review register structure before writing analysis scripts
* understand how cycles differ from weeks/months
* design new structural windows (cycle clusters, quarters, phases)

---

## Future Additions

This directory may later include:

* quarterly registers
* phase registers
* sliding-window registers
* register diff specs (FieldState deltas)
* visualization schemas

The architecture is modular — any temporal or structural window can be defined and documented here.

---

**This folder is the authoritative reference for all NORE-AI register aggregation logic.**
