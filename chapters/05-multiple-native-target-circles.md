# 05. Multiple native target circles

[← Chapter index](../README.md#chapters)

Give each selection its own native node and protect the manager’s temporary state.

## Capacity and ownership are separate requirements
The native capacity check at **VA `0x291959`** compares against two. For three-player capacity, change `83 F8 02` to `83 F8 03`, after matching the original bytes. This is only the capacity gate: it does not create three independently owned selections by itself.

The target UI manager is reached through **VA `0x209BE80`**. The implementation calls native retargeting at `0x2917E0` through a dispatcher on the UI tick (`0x28E480`, original callee `0x290CF0`). This ensures the object operation occurs at the expected game-thread boundary.

## The retarget transaction
1. Authenticate the manager, target and owned circle node.
2. Save manager head/current pointers at `+0x10F00` and `+0x10EF0`.
3. Temporarily point those fields at the circle being retargeted.
4. Call the native retarget routine with the requested target and variant.
5. Restore the manager pointers and inspect the resulting node identity.

Creation additionally protects existing nodes while native code chooses/reuses a slot. Preserve that logic rather than repeatedly invoking a singleton factory and assuming it allocates a new object each time.

The publication check matches **both target and palette**. A correct target with another player’s palette is still a wrong publication. On shutdown restore only the patch and nodes that this controller still owns.

**Failure to avoid:** two players selecting the same enemy and stealing each other’s circle; a new target being published over P1’s native node; stale node reuse after a map change. A capacity patch alone will not prevent these failures.

---

[← Previous chapter](04-independent-menus-with-native-command-execution.md) · [Chapter index](../README.md#chapters) · [Next chapter →](06-independent-area-of-effect-circles.md)
