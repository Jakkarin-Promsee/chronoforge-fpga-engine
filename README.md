# Project Directory Overview

```bash
Project/
├── UnderTale.cache/             # Ignored (Vivado cache)
├── UnderTale.hw/                # Ignored (Vivado hardware config)
├── UnderTale.ip_user_files/     # Ignored (Vivado IP files)
├── UnderTale.runs/              # Ignored (build output: synth, impl, bitstream)
├── UnderTale.sim/               # Ignored (simulation output)
│
├── UnderTale.srcs/              # IMPORTANT: actual project files used by Vivado
│   ├── constrs/                 # Constraint files (.xdc)
│   ├── sim/                     # Simulation files
│   └── source/                  # HDL source files (.v, .sv, .vhd)
│
├── vivado.xpr                   # Main Vivado project file
└── README.md
```

---

# ⚠️ Important Notes for Working With This Project

## 1. Adding files to Vivado does NOT copy them

When you use "Add Sources / Add Constraints / Add Simulation Files",  
Vivado only references the file — it does NOT create a new copy.

**Recommended:**  
Move your file into `UnderTale.srcs/` first, then add it to Vivado.  
This keeps paths consistent and prevents broken references.

---

## 2. Deleting files in Vivado does NOT delete the real file

Removing a file from the Vivado hierarchy only removes the reference.  
The actual file on disk still exists.

**If you really want to delete it:**

- Delete it from Vivado
- Also delete the file from `UnderTale.srcs/`

---

## 3. After pulling updates: you must re-add files

When you pull the latest commit, updated files appear in `UnderTale.srcs/`.  
Vivado will not automatically re-import them.

**You must manually re-add:**

- Source files (HDL)
- Constraint files (only if updated)
- Simulation files (only if needed)

Suggestion:  
Just re-add "source" files unless constraints or simulation changed.

---

## 4. Before committing, clean the `UnderTale.srcs/` folder

Since everyone must re-add files after pulling, a messy folder hurts the team.  
Keep only valid and final files inside.

**Before committing:**

- Remove unused files
- Confirm directory structure
- Commit only the necessary HDL / XDC / sim files

---

# Summary

Vivado uses _references_, not copies.  
Keep all real files inside `UnderTale.srcs/`, and re-add them after pulling.  
This keeps the project clean, predictable, and easy for everyone to work with.
