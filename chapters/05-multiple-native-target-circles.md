# 05. Multiple native target circles

[← Chapter index](../README.md#chapters)

The native target marker is managed by an engine-owned UI object. Increasing a count limit does not create independent marker ownership.

## Native boundaries

Use the [reference executable](30-native-addresses-and-hook-ownership.md) before interpreting these addresses.

| Preferred VA / field | Role to inspect |
| --- | --- |
| `0x291959` | `83 F8 02`, a comparison against two |
| `0x209BE80` | Target UI manager pointer |
| `0x2917E0` | Native retargeting routine |
| Manager `+0x10F00` / `+0x10EF0` | Head/current pointers involved in retargeting |
| `0x28E480` → `0x290CF0` | UI update call boundary |

Changing the immediate in `CMP EAX,2` to three changes only that comparison. Other allocation limits, list operations and destruction paths remain in force.

## Recover the object lifecycle

Follow the native menu path that creates its first marker. Record the factory's arguments, returned object, list insertion and destroy/reset calls. Then follow the same path when the player changes target or closes the menu. Distinguish a newly allocated node from a reused native node.

Before calling the retarget routine for an additional node, establish its complete prototype and the containing manager type from the native caller. The addresses above do not supply that prototype. In particular, do not cast the function to a guessed `(target, color)` signature.

If native retargeting uses the manager's current pointers, an extension must save them, select its node, perform the native operation and restore them within the same game-thread transaction. Preserve native nodes already in the list. On allocation failure, restore the manager before returning.

Store ownership of each additional node in the extension that creates it. On scene change, discard stale node identities; on teardown, remove only those additional nodes through the recovered native cleanup path. Never free engine objects with an unrelated allocator.

This chapter identifies investigation and interception boundaries. A complete marker factory/destructor ABI is not specified here; resolve it before implementing creation.

---

[← Previous chapter](04-independent-menus-with-native-command-execution.md) · [Chapter index](../README.md#chapters) · [Next chapter →](06-independent-area-of-effect-circles.md)
