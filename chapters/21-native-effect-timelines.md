# 21. Native effect timelines

[← Chapter index](../README.md#chapters)

A native visual effect is a time-dependent program: geometry, transforms, textures, color, material state and event timing combine to produce each frame.

## Recover the native timeline

Follow one native effect resource through creation, update, draw submission and destruction. Identify the time source and units used by its tracks. Animation sample number, render frame and game tick are different quantities until the update code establishes their relationship.

Record when each component starts, loops and ends. Include geometry that becomes invisible temporarily; deleting it because one frame has alpha zero can remove a later phase.

## Decode one track at a time

For a transform track, identify its channel, interpolation, key time format and default value. For texture animation, distinguish atlas-frame changes from UV scrolling. For material animation, distinguish RGB, alpha, additive intensity and any curve selector that changes how a value is interpreted.

Read the native consumer when a field has several meanings depending on flags. Three stored numbers are not necessarily a three-component translation. Preserve unknown callback/event records until their consumers are understood.

## Deterministic preview design

An independently written preview can use a fixed simulation step and a reproducible random seed. Convert native timing into that step explicitly. Seeking backward must restore simulation state; moving the preview camera should not advance the effect.

For an accumulator-based preview:

```text
accumulator += elapsed_game_time
while accumulator >= fixed_step:
    advance the decoded track state by fixed_step
    accumulator -= fixed_step
draw the current state without advancing it again
```

Here “advance” means evaluating the decoded tracks and particle rules implemented by the preview. It does not name an available game helper or interpreter library.

This manual does not provide a complete particle bytecode specification. Link an actual public decoder when one is used and retain its license. Do not promise playback of unknown opcodes by substituting an approximate animation without identifying the approximation.

---

[← Previous chapter](20-sharing-ghidra-types-and-exporting-definitions.md) · [Chapter index](../README.md#chapters) · [Next chapter →](22-native-effect-resources-and-scene-submission.md)
