# 23. Placing and scaling effects on real actors

[← Chapter index](../README.md#chapters)

Resolve a generation-bearing handle and choose an anchor appropriate to the visual.

## Resolve identity before reading a model
The global actor array is published through `0x208E688`, with count at `0x208E6A0`. The bounded reader rejects counts above 512 and uses an actor stride of `0xF50`, actor ID at `+8` and keep pointer at `+0x698`. These are build-specific facts, not a universal game SDK.

Use native handle resolution (`0x2E9B80`, followed by the appropriate model path at `0x3326C0`) rather than interpreting an actor slot as a model-resource index. The current binding also validates the generation bits `(handle >> 20) & 0x7FF` against the object generation at `+0x16`, checks the object kind and obtains the correct payload.

## There is no single correct “actor position”
| Visual purpose | Useful reference |
| --- | --- |
| Ground-attached footprint | Validated feet position |
| Normal target-centered impact | Native model circle center, at `model+0x670` |
| Persistent halo | Authenticated head joint and its current transform |
| Blade-sized projectile | Equipped weapon geometry/socket span |

In the current binding, radius comes from different payload offsets for supported object kinds. The published circle radius already includes a factor of 1.3. Keep the full sizing formula visible to avoid applying the same Slow-derived multiplier twice. A user-requested “20% larger” belongs at one explicit final stage, not independently in extraction, conversion and rendering.

Measure the **visible** reference geometry, such as a Distiller's circular rim; exclude transparent vertices that inflate the bounds. Scale for actual target size and model placement.

Retire placements when the target generation, battle/location identity or save epoch changes. A pointer that remains nonzero across a loading screen does not make the old attachment valid.

---

[← Previous chapter](22-getting-imported-effects-into-the-native-scene.md) · [Chapter index](../README.md#chapters) · [Next chapter →](24-building-blade-aligned-projectiles-with-one-impact.md)
