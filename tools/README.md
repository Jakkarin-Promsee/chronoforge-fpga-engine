# ChronoForge Level Compiler Toolchain

> The ChronoForge Level Compiler is a Python-based utility pipeline designed to translate human-readable, stage-separated JSON level definitions into fixed-width memory (.mem) files required for the ChronoForge FPGA Engine ROMs to the main hardware runtime.

---

## Table of contents

1. Overview
2. File / directory layout
3. JSON schemas (game_manager, attack_object, platform_object)
4. Bit-packing rules & scaling
5. Compiler pipeline (high-level)
6. Python reference: scripts and code examples

   - main_compiler.py
   - source_stage_to_json_compiler.py
   - json_to_mem_compiler.py
   - json_encoders.py

7. Examples
8. CLI usage
9. Implementation notes & best practices
10. Change log

---

## 1. Overview of the Process

The entire compilation process is orchestrated by a single script (main_compiler.py) and executed in two sequential stages:

- **Data Folding**: Reads all stage files from `./tools/source/`, orders them chronologically, and combines them into three unified JSON source files.
- **Bit-Packing**: Reads the unified JSON sources, applies data scaling and bit-width constraints, and generates the final hexadecimal memory files in `./mem/`.

This document describes JSON structure, scaling rules (how values are converted for hardware), and provides canonical Python reference code snippets for the compiler.

---

## 2. File Structure

```bash
ChronoForge-FPGA-Engine/
├── mem/ <-- FINAL FPGA ROMs that already link to Vivado
│   ├── game_manager.mem
│   ├── attack_object.mem
│   └── platform_object.mem
├── tools/
│   ├── main_compiler.py  <-- 1. START HERE
│   ├── compiler/
│   │   ├── json_encoders.py          <-- Core logic library
│   │   ├── json_to_mem_compiler.py   <-- STAGE 2: Bit-Packing
│   │   └── source_stage_to_json_compiler.py <-- STAGE 1: Data Folding
│   ├── source/
│   │   ├── stage00.json              <-- INPUT: Level Designer Data
│   │   └── stage01.json
│   └── json-source-decode/
│       ├── game_manager.json         <-- Intermediate/Unified Source
│       └── ...
└── ...
```

---

## 3. JSON schemas

### 3.1 Game Manager (one entry per stage)

Field names and human-readable limits. Values shown as how designers should set them (in _full pixels_ and _seconds_ where applicable). The compiler will scale certain fields.

```json
{
  "game_manger": {
    "stage": 0,
    "attack_amount": 6,
    "platform_amount": 3,
    "wait_time": 1.0,
    "gravity_direction": 3,
    "display_pos_x1": 130,
    "display_pos_y1": 251,
    "display_pos_x2": 506,
    "display_pos_y2": 391,
    "free(unused)": 0
  }
}
```

| Field                             | Meaning                                                                                                 | Usage Notes                                                                                                                                                        |
| --------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **stage**                         | Stage index (0–255).                                                                                    | Used by hardware runtime to trigger stage logic. Must match the `stageXX.json` filename.                                                                           |
| **attack_amount**                 | Number of attack objects in this stage (0–255).                                                         | Hardware will load exactly this many attacks from the ROM for this stage.                                                                                          |
| **platform_amount**               | Number of platform objects in this stage (0–255).                                                       | Same idea as attack_amount, but for platforms.                                                                                                                     |
| **wait_time**                     | Delay before the next stage starts (0-25.5 seconds).                                                    | Compiler converts seconds → ticks (`seconds × 10`). The engine waits for all attacks/platforms to finish spawning before applying this wait.                       |
| **gravity_direction**             | Direction of applied global gravity (0-4).                                                              | 0=no gravity, 1=up, 2=right, 3=down, 4=left.                                                                                                                       |
| **display_pos_x1 / y1 / x2 / y2** | Defines the rectangular area with border (in full pixels, 0-1023) the player is allowed to move inside. | Values are divided by 4 during packing (to fit 8-bit limit). Represents the game display bounds for this stage. (x1, y1) is top-left and (x2, y2) is bottom-right. |
| **free (unused)**                 | Reserved bit.                                                                                           | Must stay 0 for future version compatibility.                                                                                                                      |

### 3.2 Attack object (one entry per attack)

Each attack entry is packed into fixed bit widths (see section 4).

```json
{
  "type": 0,
  "colider_type": 0,
  "movement_direction": 0,
  "speed": 2,
  "pos_x": 320,
  "pos_y": 240,
  "w": 20,
  "h": 20,
  "wait_time": 2.0,
  "destroy_time": 0.0,
  "destroy_trigger": 1,
  "free(unused)": 0
}
```

| Field                  | Meaning                                                   | Usage Notes                                                                                                              |
| ---------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **type**               | Attack pattern ID (0–31).                                 | You can map these IDs in your hardware/animation engine.                                                                 |
| **colider_type**       | Collision shape (0-3).                                    | 0=square, 1=circle, 2=oval. Influences hit detection module.                                                             |
| **movement_direction** | Direction attack moves (0-7).                             | 0–7 (full 8-direction system). [0: up, 1: up+right, 2: right, 3: down+right, 4: down, 5: down+left, 6: left, 7: up+left] |
| **speed**              | Movement speed value (0–31).                              | Linear speed fed into pixel-movement hardware.                                                                           |
| **pos_x / pos_y**      | Initial spawn coordinates (full pixels, 0-1023).          | Divided by 4 during packing.                                                                                             |
| **w / h**              | Collision box width and height (full pixels, 0-1023).     | Divided by 4 in encoder.                                                                                                 |
| **wait_time**          | Delay before the **next attack** spawns (0-25.5 seconds). | Encoder multiplies by 10. This is key for pacing attack waves.                                                           |
| **destroy_time**       | Time before object auto-destroys (0-25.5 seconds).        | If trigger=0, object always destroys after this time.                                                                    |
| **destroy_trigger**    | Defines how attack disappears (0-3).                      | 0=use destroy_time, 1=out of display area, 2=out of screen boundaries.                                                   |
| **free (unused)**      | Reserved bits.                                            | Must be 0 for stability.                                                                                                 |

### 3.3 Platform object

```json
{
  "movement_direction": 2,
  "speed": 0,
  "pos_x": 340,
  "pos_y": 300,
  "w": 40,
  "h": 6,
  "wait_time": 2.0,
  "destroy_time": 5.0,
  "destroy_trigger": 1,
  "free(unused)": 0
}
```

| Field                  | Meaning                                                 | Notes                                                                                                                        |
| ---------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **movement_direction** | Direction the platform moves (0-7).                     | Same 0–7 direction map as attacks [0: up, 1: up+right, 2: right, 3: down+right, 4: down, 5: down+left, 6: left, 7: up+left]. |
| **speed**              | Movement speed (0–31).                                  | Platforms use same unit as attacks.                                                                                          |
| **pos_x / pos_y**      | Starting location (full pixels, 0-1023).                | Divided by 4 during encoding.                                                                                                |
| **w / h**              | Platform’s physical size (full pixels, 0-1023).         | Determines where the player can stand.                                                                                       |
| **wait_time**          | Delay before next platform is spawned (0-25.5 seconds). | Used only in platform sequence.                                                                                              |
| **destroy_time**       | Auto-remove time (0-25.5 seconds).                      | Has same behaviour as attacks.                                                                                               |
| **destroy_trigger**    | Removal logic (0-3).                                    | 0=timer, 1=leaving game area, 2=leaving screen.                                                                              |
| **free (unused)**      | Reserved bits.                                          | Keep at 0.                                                                                                                   |

---

## Notes

### 1. `wait_time` parameter

- `wait_time` represents the **delay between reading two consecutive objects**.
- It is **not** the same as destroy time—`wait_time` controls timing flow, not how long an object exists.

### 2. Stage-Level Execution

- A stage transitions to the next stage **only after all attack objects in that stage have been spawned**, including the final attack’s `wait_time`.
- Be careful when designing platform objects:
  If a platform’s lifetime is too short, it may disappear **before** the stage finishes running all attack waits.

### 3. Key Design Concept

- For each stage, first define:
  - **Player-enabled areas** ((x1, y1) to (x2, y2), movement limits)
  - **Gravity settings** (the direction of gravity)
- After that, design the **gameplay flow** by planning the timings of all attack objects (using `wait_time` to control pacing).
- Only after the attack timing is complete, add the **platform objects** so their durations match the intended flow.

---

## 4. Stage Setting JSON schemas

```bash
ChronoForge-FPGA-Engine/
├── tools/
│   └── source/
│       ├── stage01.json
│       ├── stage02.json
│       ├── ...
│       └── stageXX.json
```

All game stage have to write in `./tools/source/stage*.json` for the compiler. The order or redering will be 01 to XXX. And inside of each `stage.json` require 3 main items.

```json
{
  "game_manger": {...},

  "attack_object": [
    {...},
    {...},
    {...}
    ...
  ],

  "platform_object": [
    {...},
    {...},
    {...},
    ...
  ]
}
```

---

## 4. Compile JSON to MEM code

Execution is simple, requiring only the **Master Compiler** script.

### 4.1 Navigate to the `tools/` directory.

```bash
cd ChronoForge-FPGA-Engine/tools/
```

### 4.2 **Execute** the master script using your Python interpreter.

```bash
python main_compiler.py
```

The `main_compiler.py` will handle all steps automatically, providing formal console logs throughout the process while compile each game stage at `tools/source/stage*.json` to `mem/*.mem` that already connect to vivado project.

---

### 5. Build and Upload Project to FPGA Board

Follow these steps to turn your Verilog/VHDL project into a running system on the FPGA:

#### 0. Compile .JSON game code to .MEM from previous step.

#### 1. Synthesize

- Converts your HDL code into a low-level hardware netlist.
- Check for errors and warnings.
- Make sure all modules are connected correctly and no signals are left undefined.

#### 2. Implement (Place & Route)

- The tool places logic blocks onto the FPGA fabric.
- Routes all wires between them.
- Fix any timing violations that appear during this step.

#### 3. Generate Bitstream

- After implementation succeeds, create the `.bit` file.
- This file contains the final hardware configuration for your design.

#### 4. Upload to FPGA Board

- Connect your Basys3 (or other board) via USB.
- Open the Hardware Manager.
- Program the FPGA using the generated `.bit` file.
- Wait until programming completes—your design should start running immediately.

---

## 6. Bit-packing rules & scaling (High level)

This section enumerates each field, its bit-width, how to scale, and packing order (MSB-first within each composite entry). These sizes match the hardware ROM layout.

### 6.1 Game manager (9 bytes, 74 bits — canonical ordering)

| Field             | Bits | Notes                                                               |
| ----------------- | ---: | ------------------------------------------------------------------- |
| stage             |    8 | uint8, must equal stage number derived from filename (stageXX.json) |
| attack_amount     |   10 | uint10                                                              |
| platform_amount   |   10 | uint10                                                              |
| gravity_direction |    3 | uint3                                                               |
| display_pos_x1    |    8 | encoder: `value // 4` (integer division)                            |
| display_pos_y1    |    8 | `value // 4`                                                        |
| display_pos_x2    |    8 | `value // 4`                                                        |
| display_pos_y2    |    8 | `value // 4`                                                        |
| wait_time         |    8 | encoder: `int(round(value * 10))` -> 0..255 mapping to 0..25.5s     |
| free(unused)      |    1 | set to 0                                                            |

Total: 74 bits (packed into 9 bytes in ROM)

### 6.2 Attack object (9 bytes, 86 bits — canonical ordering)

| Field              | Bits | Scale                                                                                    |
| ------------------ | ---: | ---------------------------------------------------------------------------------------- |
| type               |    5 | uint5                                                                                    |
| colider_type       |    2 | uint2                                                                                    |
| movement_direction |    3 | uint3                                                                                    |
| speed              |    5 | uint5                                                                                    |
| pos_x              |    8 | `pos_x // 4` (uint8)                                                                     |
| pos_y              |    8 | `pos_y // 4` (uint8)                                                                     |
| w                  |    8 | `w // 4` (uint8)                                                                         |
| h                  |    8 | `h // 4` (uint8)                                                                         |
| wait_time          |    8 | `int(round(value * 10))` (uint8)                                                         |
| destroy_time       |    8 | `int(round(value * 10))` (uint8)                                                         |
| destroy_trigger    |    3 | uint3 (but note spec earlier listed 3 bits; some designs use 2 — follow hardware schema) |
| free(unused)       |    7 | reserved; set to 0                                                                       |

Total: 86 bits (should be packed into 11 bytes or into fixed-width words used by ROM — the encoder enforces exact wiring and alignment used by hardware)

> **Important**: Keep ordering consistent with the hardware spec. The `json_encoders.pack_bits()` helper ensures correct bit width and endianness.

### 6.3 Platform object (8 bytes, 71 bits)

| Field              | Bits | Scale                    |
| ------------------ | ---: | ------------------------ |
| movement_direction |    3 | uint3                    |
| speed              |    5 | uint5                    |
| pos_x              |    8 | `pos_x // 4`             |
| pos_y              |    8 | `pos_y // 4`             |
| w                  |    8 | `w // 4`                 |
| h                  |    8 | `h // 4`                 |
| wait_time          |    8 | `int(round(value * 10))` |
| destroy_time       |    8 | `int(round(value * 10))` |
| destroy_trigger    |    3 | uint3                    |
| free(unused)       |    6 | reserved                 |

Total: 71 bits

---
