# 24. Weapon animation and hit timing

[← Chapter index](../README.md#chapters)

Weapon animation, contact timing and damage delivery must remain connected when editing an attack's presentation.

## Recover the equipped attachment

Follow the native model hierarchy from the current actor to its equipped weapon. Joint selectors such as `j_blade` (`0x200`) and `n_grip` (`0x201`) identify attachment choices in the relevant native path. A model field that names an instance is not necessarily an archive resource ID.

Traverse hierarchy links with bounds and cycle detection. Preserve the distinction between socket-local geometry, model space and world space. A weapon's visible length must be measured in the space in which an effect is scaled.

## Follow the native hit event

Trace the stock attack from command acceptance to its animation event and native physical-hit/result path. Establish which callback authorizes damage, which computes the result and which applies it. The relevant physical route includes `0x325260`; see [Result application](13-damage-status-results-and-enemy-reaction.md).

Removing an animation event from an edited visual is not proof that damage stopped. Another execution callback can still reach the native hit. Conversely, replaying an effect event can duplicate an already-authorized hit.

## Adding travel is a separate implementation

If a new visual should travel before impact, the extension must own a pending-hit record and an explicit state transition:

```text
native action accepted -> pending visual travel
first authorized contact -> finalize native hit once -> completed
actor/target/scene invalidated -> cancelled
```

That record and the collision calculation are new code, not a preloaded service. Do not retain a pointer to a temporary native result buffer across frames without establishing its lifetime. Recover a supported later-execution path or retain an independently owned representation with a complete conversion contract.

Use swept geometry between successive game-time positions when discrete frame samples would skip a target. Once the hit is consumed, later animation callbacks must not apply it again. Keep native target rules, resource payment and post-hit reactions intact.

No custom weapon, clip number, action allocation or damage multiplier is prescribed by this chapter.

---

[← Previous chapter](23-placing-and-scaling-effects-on-real-actors.md) · [Chapter index](../README.md#chapters) · [Next chapter →](25-resolving-sound-events-to-the-correct-audio-stream.md)
