# ChronoForge FPGA Engine (Basys3, VGA 640×480 @ 60Hz)

## Overview

This project implements a complete hardware game runtime system on the **Basys3 FPGA**.  
The design includes:

- A custom multi-clock architecture
- A decentralized game-manager pipeline
- Parallel attack/platform object loading
- Multi-object collider and trigger runtimes
- VGA 640×480 60Hz rendering
- Custom binary `.mem` file formats and a Python compiler for generating ROM data

The system targets high determinism, predictable behavior, and scalable object handling in hardware.

---

# 1. Clock Architecture

The Basys3 100 MHz clock is divided into **five BUFG-derived clocks**, each responsible for a different subsystem:

| Clock                | Frequency | Purpose                                                  |
| -------------------- | --------- | -------------------------------------------------------- |
| `clk_vga`            | 25 MHz    | VGA 640×480 @ 60 Hz timing                               |
| `clk_player_control` | 100 Hz    | Player physics (gravity, movement, input)                |
| `clk_object_control` | 100 Hz    | Non-player object movement                               |
| `clk_centi_second`   | 100 Hz    | Global timing for wait-time counters                     |
| `clk_calculation`    | 1 kHz     | Object registration, collision logic, heavy calculations |

This architecture prevents timing noise and ensures deterministic behavior in all modules.

---

# 2. Game Manager Runtime

The system is driven by a ROM file: **`game_manager.mem`**.

Each entry represents a **game stage**:

```json
{
  "stage": "2^8",
  "attack_amount": "2^10",
  "platform_amount": "2^10",
  "gravity_direction": "2^3",
  "display_pos_x1": "2^8",
  "display_pos_y1": "2^8",
  "display_pos_x2": "2^8",
  "display_pos_y2": "2^8",
  "wait_time": "2^8",
  "free": "2^1"
}
```

## Runtime Loop

1. Read stage `CS`
2. Load its configuration
3. Sequentially load attack objects
4. Sequentially load platform objects
5. Respect each object's wait-time
6. When both lists are exhausted → advance to next stage
7. Loop at end-of-file

All operations are fully synchronized using parent ↔ child sync/update handshakes.

---

# 3. Attack Object ROM (`attack.mem`)

```json
{
  "type": "2^5",
  "colider_type": "2^2",
  "movement_direction": "2^3",
  "speed": "2^5",
  "pos_x": "2^8",
  "pos_y": "2^8",
  "w": "2^8",
  "h": "2^8",
  "wait_time": "2^8",
  "destroy_time": "2^8",
  "destroy_trigger": "2^2",
  "free": "2^7"
}
```

### Destroy Rules

- `0`: Off-screen
- `1`: Off display block
- `2`: Collide with display boundaries
- `3`: Hit player

---

# 4. Platform Object ROM (`platform.mem`)

```json
{
  "movement_direction": "2^3",
  "speed": "2^5",
  "pos_x": "2^8",
  "pos_y": "2^8",
  "w": "2^8",
  "h": "2^8",
  "wait_time": "2^8",
  "destroy_time": "2^8",
  "destroy_trigger": "2^2",
  "free": "2^6"
}
```

Platforms share similar behavior but are treated as collision-only objects.

---

# 5. Sync / Update Handshake Protocol

Every parent-child module pair uses **two wires**:

- `sync_*`
- `update_*`

## Lifecycle

1. **Parent sets sync = 0** → child loads data
2. Child performs its task → sets `update = 1`
3. Parent receives update → sets `sync = 1`
4. Child sees sync = 1 → returns to idle (update=0)

This guarantees deterministic timing at 100 MHz.

---

# 6. Multi-Object Runtime (Collider & Trigger)

There are two decentralized subsystems:

- **multi_object_collider_runtime**
- **multi_object_trigger_runtime**

Both run at **1 kHz**.

## Responsibilities

- Object registration
- Object lifecycle
- Destroy conditions
- Iterator-ready-state logic
- Parallel update of up to N objects

Objects advertise their availability through the shared:

```
iterator_ready_state[N]
```

Each **single-object runtime** decides:

- When it is free
- When it is active
- When it should auto-destroy
- When it should re-enter free state

---

# 7. Player Collision System

The player sends only:

- `player_x`
- `player_y`
- `player_w`
- `player_h`

to the multi-object collider.

## Ground Logic Example

To compute player's “ground”:

1. Check objects **below** the player
2. Filter only objects within horizontal bounds
3. Choose the **closest top surface**
4. Output:
   - `is_ground = 1`
   - `ground_y = integer`

A 2-pixel buffer prevents jitter for upward-moving platforms.

### Trigger Objects

These are computed with simple region overlapping.

---

# 8. Rendering Pipeline (VGA 25 MHz)

To minimize register usage and handle many objects:

- A **register window** covers only the player display area
- All overlapping objects are written into this window
- Outside the window: simple conditional color selection

This method supports:

- High performance
- Many simultaneous objects
- Efficient register usage

---

# 9. Python Compiler

A Python tool converts JSON scene descriptions into `.mem` ROM files:

- `game_manager.json → game_manager.mem`
- `attack.json → attack.mem`
- `platform.json → platform.mem`

The compiler ensures all values match bit constraints.

---

# 10. Current Version

**Runtime Architecture: V4**

Refactored for:

- Fully decentralized runtime
- Low wire count
- Fast object registration
- Bulletproof sync protocol
- Scalable future expansion

---

# 11. Future Work

Possible extensions:

- Additional collider types (slopes, rotated boxes)
- Parallax or animated backgrounds
- Audio controller
- Hardware sprite engine (DMA-style fetch)
- JSON scene editor GUI
- Scripting or animation timeline system

---

# 12. Suggested File Structure

```
Project/
/src
  /runtime
  /collider
  /trigger
  /vga
  /player
  /objects
/mem
  game_manager.mem
  attack.mem
  platform.mem
/tools
  json_to_mem_compiler.py
/docs
  README.md
```

---

# License

This project is licensed under the **MIT License**.
