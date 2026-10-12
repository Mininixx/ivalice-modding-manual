# 10. Area changes, interaction and state retirement

[← Chapter index](../README.md#chapters)

The lifetime of an actor, camera or menu object can end before a new area becomes visible. Native transition state must delimit access to these objects.

## Distinguish persistent and live state

Persistent character data may survive an area change while its actor and model are destroyed. Store persistent character identifiers for long-lived settings; resolve current handles and pointers for operations in the world.

In the reference location layout, fields at `+0x1244` and `+0x125C` represent different area-related values. Their temporary disagreement is a transition clue, not sufficient evidence of corruption. Recover the location pointer and the writers of both fields before using them as an admission rule.

## Define an extension lifecycle

An extension that owns transient objects should have explicit states:

```text
inactive -> acquiring scene -> active -> retiring -> inactive
```

Acquisition requires the native world, issuer and target objects needed for the feature. Retirement prevents new requests, detaches extension-owned render objects, discards queued handles from the old scene and releases owned resources. Reacquisition starts with fresh native identities.

Changing only the visible map number is insufficient if the engine can reload the same area. Include a scene lifetime or native-root identity in the extension's own revision tracking. Increment that revision when retiring the scene, and reject queued requests carrying an older value.

## Keep native interaction precedence

A native interaction prompt represents a specific target and use state. Find the prompt builder and activation path for the particular object type: a treasure, NPC and save crystal need not share all rules. Distance alone does not establish availability.

When an extension handles Confirm, first decide whether an actionable native interaction owns that input. If so, preserve its activation and dialogue route. A separate battle menu must not consume the same edge and silently replace the interaction.

Do not reposition actors to simulate a native transition or interaction. Preserve destination/spawn data and the engine's initialization order. A delayed corrective position or facing write is visible behavior, not a substitute for understanding that order.

---

[← Previous chapter](09-rendering-huds-inside-the-game.md) · [Chapter index](../README.md#chapters) · [Next chapter →](11-adding-actions-without-breaking-existing-commands.md)
