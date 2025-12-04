# Game Manager JSON Form (9 Bytes)

```json
{
  "stage": "2^8", // State ID (256 uniques)
  "attack_amount": "2^10", // Attack amount to read from attack.mem (1024 attacks)
  "platform_amount": "2^10", // Platform amount to read from platform.mem (1024 attacks)
  "gravity_direction": "2^3", // 0 gravity and 4 gravity axis
  "display_pos_x1": "2^8", // position x1 (multiply 4 before use in game)
  "display_pos_y1": "2^8", // position x2 (multiply 4 before use in game)
  "display_pos_x2": "2^8", // position x1 (multiply 4 before use in game)
  "display_pos_y2": "2^8", // position x2 (multiply 4 before use in game)
  "wait_time": "2^8", // Waiting time before next stage (25.6 seconds)
  "free(unused)": "2^1" // Unused for now
}
```

# Attack Object JSON Form (9 Bytes)

```json
{
  "type": "2^5", // attack type (32 types, design for future work too)
  "colider_type": "2^2", // Squar, Circle/Capsule, Tilt left capsule, Tilt right capsule.
  "movement_direction": "2^3", // 8 Nomal direction
  "speed": "2^5", // 32 levels of speed
  "pos_x": "2^8", // Spawns position x (multiply 4 before use in game)
  "pos_y": "2^8", // Spawns position y (multiply 4 before use in game)
  "w": "2^8", // Width (multiply 4 before use in game)
  "h": "2^8", // Height (multiply 4 before use in game)
  "wait_time": "2^8", // Waiting time before next stage (25.6 seconds)
  "destroy_time": "2^8", // 0 for out of screen, 1 for our of display screen, and other are (25.4 second)
  "destroy_trigger": "2^2", // 0 untrigger, 1 destroy when end scrren, 2 destroy when end display blcok, 3 destrou when hit player
  "free(unused)": "2^7" // Unused for now
}
```

# Platform Object JSON Form (8 Bytes)

```json
{
  "movement_direction": "2^3", // 8 Nomal direction
  "speed": "2^5", // 32 levels of speed
  "pos_x": "2^8", // Spawns position x (multiply 4 before use in game)
  "pos_y": "2^8", // Spawns position y (multiply 4 before use in game)
  "w": "2^8", // Width (multiply 4 before use in game)
  "h": "2^8", // Height (multiply 4 before use in game)
  "wait_time": "2^8", // Waiting time before next stage (25.6 seconds)
  "destroy_time": "2^8", // Waiting before attack destroy (256 second)
  "destroy_trigger": "2^2", // 0 untrigger, 1 destroy when end scrren, 2 destroy when end display blcok, 3 destrou when hit player
  "free(unused)": "2^6" // Unused for now
}
```
