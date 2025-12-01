# Game Manager JSON Form (5 Bytes)

```json
{
  "stage": "2^8", // State ID (256 uniques)
  "attack_amount": "2^10", // Attack amount to read from attack.mem (1024 attacks)
  "platform_amount": "2^10", // Platform amount to read from platform.mem (1024 attacks)
  "free(unused)": "2^4", // Unused for now
  "wait_time": "2^8" // Waiting time before next stage (25.6 seconds)
}
```

# Attack Object JSON Form (7 Bytes)

```json
{
  "type": "2^5", // attack type (32 types, design for future work too)
  "colider_type": "2^2", // Squar, Circle/Capsule, Tilt left capsule, Tilt right capsule.
  "movement_direction": "2^3", // 8 Nomal direction
  "speed": "2^5", // 32 levels of speed
  "free(unused)": "2^1", // Unused for now
  "pos_x": "2^8", // Spawns position x (multiply 4 before use in game)
  "pos_y": "2^8", // Spawns position y (multiply 4 before use in game)
  "w": "2^8", // Width (multiply 4 before use in game)
  "h": "2^8", // Height (multiply 4 before use in game)
  "time": "2^8" // Waiting time before next stage (25.6 seconds)
}
```

# Platform Object JSON Form (6 Bytes)

```json
{
  "movement_direction": "2^3", // 8 Nomal direction
  "speed": "2^5", // 32 levels of speed
  "pos_x": "2^8", // Spawns position x (multiply 4 before use in game)
  "pos_y": "2^8", // Spawns position y (multiply 4 before use in game)
  "w": "2^8", // Width (multiply 4 before use in game)
  "h": "2^8", // Height (multiply 4 before use in game)
  "time": "2^8" // Waiting time before next stage (25.6 seconds)
}
```
