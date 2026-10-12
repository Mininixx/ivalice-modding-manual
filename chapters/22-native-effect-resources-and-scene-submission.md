# 22. Native effect resources and scene submission

[← Chapter index](../README.md#chapters)

A native effect must reach the scene renderer with valid data and live backing storage. A resource-loading success is only one part of that path.

## Follow an existing native resource

Begin with a stock effect that already uses the required primitive family. Follow its material creation, track evaluation, scene submission, sorting and draw consumption. Recover the full structures before constructing a new instance.

The reference executable provides these investigation points:

| Preferred VA | Native behavior to inspect |
| --- | --- |
| `0x449AB0` | Material processing and type-dependent branches |
| `0x430B90` | Vector evaluation, including flag-dependent constant/curve selection |
| `0x449560` | Sprite processing |
| `0x3A2C80` | Sort-stage copy/allocation path |
| `0x1A1470` | Gi-stage allocation path |
| `0x20E630` | Queuing a prepared pair by pointer |

These addresses use the [reference fingerprint](30-native-addresses-and-hook-ownership.md). Their complete parameter and structure definitions are not supplied here; they are not ready-to-call exported APIs.

## Preserve storage until consumption

Separate the producer's temporary evaluation data from the queued data the renderer will later read. If a native queue retains a pointer, a stack-local or reused scratch buffer is invalid after the producer returns.

The sort-copy path rounds sizes to 16-byte units. The Gi allocator has its own rounding behavior, including an additional unit for an exact multiple in the examined path. Recover each allocator's capacity, alignment and ownership separately rather than assuming a shared allocation contract.

Keep the effect's native scene identity and referenced resources alive until the consumer finishes. Release them through the corresponding native destruction path, not with an unrelated heap allocator.

## Camera and depth are part of the draw

Capture the view/projection state belonging to the draw's scene. A final-frame HUD overlay does not automatically receive native depth, sorting or attachment transforms. Likewise, an inverse-screen matrix is not interchangeable with a world-view matrix.

When diagnosing an invisible effect, inspect material type, blend/depth state, primitive flags, track selection, bounds and lifetime in that order. Do not repair a missing draw by globally disabling depth or replacing every material flag. A minimal new submission implementation must define its pair structure and both lifetimes before calling the queue.

---

[← Previous chapter](21-native-effect-timelines.md) · [Chapter index](../README.md#chapters) · [Next chapter →](23-placing-and-scaling-effects-on-real-actors.md)
