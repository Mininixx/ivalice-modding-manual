# 22. Getting imported effects into the native scene

[← Chapter index](../README.md#chapters)

A registered effect must also survive material selection, scene submission and renderer ownership.

## Implement each rendering boundary
1. **Catalog:** a private action selects an allocated effect ID.
2. **Submission:** the effect is accepted into the native world-render queue.
3. **Appearance:** it draws with the intended placement, material, depth and timing.

A menu entry and a successful DLL load establish neither the second nor the third. Treat private effects 510/511 and actions 3767/3768 as allocated records, not free slots in another installation.

## Native material fields can quietly suppress or distort a draw
Respect these structure-specific contracts:

| Boundary | Contract |
| --- | --- |
| Material processing at `0x449AB0` | An all-type-0 material set returned early; the converted carrier required type 1 |
| Morph selector at `+0x190` in its own record | An inherited donor curve selected the wrong mesh; use a deliberate constant selection per track |
| Vector routine `0x430B90`, flags `+0x30` | Flags select zero/one/curve paths and couple axes; supplying three curves alone is insufficient |
| Sprite routine `0x449560`, its `+0x190` | A float translation vector, including negative fractions; not a color field |
| Private carrier/model flags | Use the matching blend/queue path and carrier model flags `0x01 → 0x05` |

Identical offsets in different native structures do not describe identical fields. Recover the containing type before changing them.

## Enqueued objects must outlive the callback
The current scene transport owns a snapshot of the view matrix and draw identity at both sort and Gi stages. It does not leave a queued pointer to temporary particle scratch memory. Its identity includes root, attachment, definition, battle, location, generation, caster, target and area.

The sort-copy path at `0x3A2C80` rounds size up to 16-byte units and has a 40,960-slot capacity. Gi allocation at `0x1A1470` has a different rounding convention, reserving an additional unit even for an exact multiple. Guard both capacity and byte range rather than assuming the same allocator contract.

`0x20E630(pair, 2)` queues the prepared pair's pointer; it does not make an independent copy of all supplied data. Keep backing storage stable through consumption. World effects need the scene's depth/camera path; the final Present overlay used by flat HUD panels is a different rendering boundary.

## Capture the camera used by this draw
`GiBeginEff+8` is an inverse-screen transform, not the world view. Its projection at `+0x48` is useful, while the world-view snapshot is captured through the scene path (`0x1F7E528`). The current validator checks finite affine/orthonormal structure and a positive determinant, then applies the required axis conversion.

Do not require the draw snapshot to equal another independently updated camera cache (`0x2AEDEF0`). Match ownership and lifetime first; valid matrices captured at different moments need not be bit-identical.

---

[← Previous chapter](21-recovering-particle-programs-and-their-timeline.md) · [Chapter index](../README.md#chapters) · [Next chapter →](23-placing-and-scaling-effects-on-real-actors.md)
