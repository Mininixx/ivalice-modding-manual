# 23. Placing and scaling effects on real actors

[← Chapter index](../README.md#chapters)

An actor's persistent record, live object, model, skeleton and attachment are separate objects. Use the native handle resolver before selecting an anchor.

## Reference object layout

For the executable in [Address reference](30-native-addresses-and-hook-ownership.md), actor-array data is exposed through globals `0x208E688` and `0x208E6A0`. The associated actor layout has stride `0xF50`, a 32-bit identity at `+8` and a battle-record pointer at `+0x698`. Confirm the actual allocation/count before iterating; an arbitrary fixed upper bound is not a substitute for the container's extent.

The handle/object path at `0x2E9B80` and model-related path at `0x3326C0` are useful native investigation points. Their full signatures must be recovered before direct calls. Handle bits, object kind and generation must be checked using the native resolver's own logic; do not turn a handle into an array offset by guessing.

## Choose an anchor by purpose

| Purpose | Data to recover |
| --- | --- |
| Ground effect | Actor's native ground/feet position |
| Body-centred impact | Model's native circle/impact centre |
| Head attachment | Current head joint transform |
| Weapon attachment | Equipped weapon's socket and model transform |

The model-circle centre used by one native path is at model `+0x670`. Establish that the pointer is the expected model type before reading it. That offset does not describe every actor or visual object.

For a joint attachment, compose the local joint transform with the model and world transforms using the engine's matrix convention. Verify row/column order and handedness with a known translation and rotation before combining matrices.

## Scale once, in a stated space

Choose whether size is fixed in world units, relative to a model radius or relative to visible mesh bounds. Apply that choice at one explicit stage. Do not multiply by a model scale already included in the selected world transform.

Exclude fully transparent geometry when measuring a visible rim or outline. Reacquire the attachment when the model changes, and retire it when the handle, scene or native object generation changes.

---

[← Previous chapter](22-native-effect-resources-and-scene-submission.md) · [Chapter index](../README.md#chapters) · [Next chapter →](24-weapon-animation-and-hit-timing.md)
