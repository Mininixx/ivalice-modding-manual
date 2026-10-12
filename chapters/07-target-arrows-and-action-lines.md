# 07. Target arrows and action lines

[← Chapter index](../README.md#chapters)

Selection arrows and action lines have separate draw paths. A change to one will not necessarily affect the other.

## Locate the native source identity

For the [reference executable](30-native-addresses-and-hook-ownership.md), the palette-related instruction sites are `0x3F719C` for an arrow path and `0x3F54D2` for a target-line path. At those particular sites, the source identity is accessed through `[RSI+0x2D0]` and `[R15+0x810]`, respectively.

These are fields of the draw contexts in those routines, not universal actor offsets. Trace the caller to establish the containing objects and palette argument width before writing a hook. Preserve the complete displaced instructions and every live register affected by the interception.

## Keep the engine geometry

If the requested change is a color, change only the palette selection and retain native geometry, depth, animation and fade. Read the existing special-case palette branches before replacing their result. Preserve special palette value 4 where that native branch applies; a blanket constant would also recolor exceptional states.

A new per-actor palette rule can be represented by a map from full handle to palette value. That map must be implemented by the extension, synchronized with its render consumer and cleared when actors or scenes retire. It is not a vanilla table supplied by this manual.

The rule must distinguish the actor drawing the line from its target. Two actors aiming at the same target may need different source palettes.

## Keep different targets distinct

The native action already executing, the next command waiting for execution, and the target currently highlighted by a menu can be different. Trace which one a draw context represents. Preserve the original draw when the source cannot be resolved; do not recolor every draw because a target name happens to match.

---

[← Previous chapter](06-independent-area-of-effect-circles.md) · [Chapter index](../README.md#chapters) · [Next chapter →](08-camera-state-collision-and-transitions.md)
