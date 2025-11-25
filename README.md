# Project Directory Overview

```bash
Project/
├── UpperTale.cache/             # Ignored (Vivado cache)
├── UpperTale.hw/                # Ignored (Vivado hardware config)
├── UpperTale.ip_user_files/     # Ignored (Vivado IP files)
├── UpperTale.runs/              # Ignored (build output: synth, impl, bitstream)
├── UpperTale.sim/               # Ignored (simulation output)
│
├── UpperTale.srcs/              # IMPORTANT: actual project files used by Vivado
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
Vivado only **references** the file — it does NOT make a new copy.

**Recommended workflow:**  
Move your file into `UpperTale.srcs/` first, then add it to Vivado.  
This keeps all paths consistent and prevents broken references.

---

## 2. Deleting files in Vivado does NOT delete the real file

Removing a file from Vivado’s hierarchy only removes the _reference_.  
The actual file still remains on disk.

**If you really want to delete a file:**

- Delete it inside Vivado
- Also delete the actual file in `UpperTale.srcs/`

---

## 3. After pulling updates, you may need to re-add files

Sometimes you will get conflicts when pulling from git.  
If you don’t care about your current progress and want to reset to the latest commit, use:

- `git reset --hard HEAD`
- `git clean -fdx`

After pulling, the updated files will appear in `UpperTale.srcs/`.  
However, Vivado does **not always re-import** them automatically.

**If some file missing**

using `add file` for all items in these folder. It will add only files referenct that you have no import in vivado project yet.

- Add source files: `UpperTale.srcs/sources_1/new/`
- Add constrain files: `UpperTale.srcs/constrs_1/new/`
- Add simulation files: `UpperTale.srcs/sim_1/new/`

**Tip:**  
If `git pull` still gives errors, try closing Vivado first.

---

## 4. Before committing, clean the `UpperTale.srcs/` folder

Because teammates must re-add files after pulling, a messy folder makes the project harder to use.  
Keep only the valid and necessary files inside.

**Before committing:**

- Remove unused or temporary files
- Check that the directory structure is correct
- Commit only final HDL / XDC / simulation files

---

# Summary

Vivado uses **references**, not copies.  
Always keep the real working files inside `UpperTale.srcs/`, and clean them before pushing updates.  
This keeps the project clean, predictable, and easy for implementation.
