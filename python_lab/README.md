# Game Manager JSON Form

```json
{
  "stage": "2^8", // State ID (256 uniques)
  "attack_combo": "2^10", // Attack amount to read from attack.mem (1024 attacks)
  "ground_type": "2^4", // Ground types (16 types)
  "free(unused)": "2^2", // Unused for now (4 frees combinations)
  "wait_time": "2^8" // Waiting time before next stage (25.6 seconds)
}
```

# Attack Object JSON Form

```json
{
  "type": "2^5", // attack type (32 types, design for future work too)
  "colider_type": "2^2", // Squar, Circle/Capsule, Tilt left capsule, Tilt right capsule.
  "movement_direction": "2^3", // 8 Nomal direction
  "speed": "2^2", // Stop, Slow, Normal, Fast
  "free(unused)": "2^3", // Unused for now (8 frees combinations)
  "pos_x": "2^8", // Spawns position x (multiply 4 before use in game)
  "pos_y": "2^8", // Spawns position y (multiply 4 before use in game)
  "w": "2^8", // Width (multiply 4 before use in game)
  "h": "2^8", // Height (multiply 4 before use in game)
  "time": "2^8" // Waiting time before next stage (25.6 seconds)
}
```
