# 07. Target arrows and action lines

[← Chapter index](../README.md#chapters)

One visual family can have several render paths; identify each owner at its own call site.

## Two render sites, one ownership table
The action arrow and the target line use separate paths. The palette hooks are **VA `0x3F719C`** for the arrow and **VA `0x3F54D2`** for the target line. Both read a published table of up to three `(handle, palette)` pairs.

The arrow path identifies its source through `[rsi+0x2D0]`; the target-line path uses `[r15+0x810]` at its own hook site. These are context-specific structures, not interchangeable actor offsets. Preserve the displaced instructions and change the palette only for a matching owned handle.

This keeps native geometry, depth, animation and fade. The arrow hook also preserves a native special palette case (`4`) instead of blindly recolouring every draw. Recolouring one path does not guarantee the other will match.

## Distinguish target selection from action execution
A menu’s current target, a queued action’s target, a world arrow and a party-portrait cursor are related but not identical. An executing action may keep its native target while the next menu is selecting another. Give each presentation an explicit source of truth and lifetime.

---

[← Previous chapter](06-independent-area-of-effect-circles.md) · [Chapter index](../README.md#chapters) · [Next chapter →](08-a-shared-camera-that-still-respects-the-scene.md)
