# 01. Moving additional party members

[← Chapter index](../README.md#chapters)

Give each player steering ownership while retaining the game’s movement machinery.

## The working boundary
The useful interception point is the movement consumer, not the character’s final world position. For this executable build, the detour begins at **VA `0x2E4380`**. Its context exposes the actor through `context+0x30` and the physics payload through `context+0xB8`. The generated cave accepts only the owned P2/P3 actor and the eligible native mode (`r8d == 0`). All other actors continue through the displaced native prologue.

| Physics field | Type | Published value |
| --- | --- | --- |
| `+0xA4` | float | Heading in radians |
| `+0xD0` | float | Movement magnitude |
| `+0xA0` | float | Pitch, cleared by this steering path |

This feeds the existing movement pipeline. Repeatedly teleporting world coordinates would bypass the contract being used here and is not how this implementation works.

## Construct a steering command
Project the stick onto the camera’s horizontal forward/right basis. Normalize input strength through the native stick-response policy, then choose walk/run magnitude. The sign and axis convention below comes from `player_steering`:

```python
# Pseudocode: the basis and actor were authenticated earlier.
world_x = forward_input * forward.x + right_input * right.x
world_z = forward_input * forward.z + right_input * right.z
heading = atan2(world_x, world_z)
strength = min(1.0, hypot(forward_input, right_input))
magnitude = run_or_walk_step * native_stick_fraction(strength)
```

Publish to separate per-player command blocks. Reject a zero actor before comparing pointers. Preserve scratch registers, replay displaced instructions and validate every branch destination in the emitted machine code.

## Movement is only one owner
Follower AI can still turn or approach a target. The implementation has separate facing hooks (`0x236328`, visual-facing call `0x236323`) and an action-approach gate (`0x325E07`). Scope these to the controlled follower. Do not disable native follower lists globally or seize the ordinary leader. Keep the P1 Berserk permission gate separate from follower steering.

---

[Chapter index](../README.md#chapters) · [Next chapter →](02-moving-a-berserk-party-leader.md)
