# 09. Rendering HUDs inside the game

[← Chapter index](../README.md#chapters)

Publish coherent panel pixels, composite them in D3D11 and preserve the caller’s graphics state.

## The panel transport
Read the panel capacity from the active producer/renderer protocol. A 16-slot co-op layout uses a 128-byte shared header, a 64-byte header per slot and `1024 × 768 × 4` reserved bytes per slot; the extended content layout uses 22 slots. Match the installed layout exactly instead of mixing constants from the two variants.

Publish dimensions, logical coordinates, visibility, generation and pixel content coherently. Keep publisher/renderer heartbeats and acknowledgements. Reusing a texture when only its position changes is cheaper than uploading unchanged pixels every update. Reject oversized payloads and stale or partial publications.

## Match alpha representation to the blend state
The panel path converts straight RGBA into **premultiplied BGRA**. RGB is multiplied by the final alpha, including opacity. The corresponding blend uses `ONE / INV_SRC_ALPHA`. Multiplying RGB twice darkens edges; feeding straight RGB into this path creates fringes.

```text
premultiplied_rgb = straight_rgb * alpha
out_rgb = source_premultiplied_rgb + destination_rgb * (1 - alpha)
```

Do not globally replace every blend state with this one: other native primitives and imported particle materials can have different alpha contracts.

## Presentation and capture
Draw panels through the renderer loaded in the game and keep added audio in its in-process mixer. Do not restore an external layered-window fallback. Preserve transport recovery and the capture boundary of the actual renderer/audio consumer.

Preserve the D3D11 state you change—render targets, depth/stencil, blend, shaders, buffers, textures, samplers, viewports and scissors. Handle hidden panels, transparent corners, overlap, resize, ultrawide viewports and transport loss without leaking graphics state.

---

[← Previous chapter](08-a-shared-camera-that-still-respects-the-scene.md) · [Chapter index](../README.md#chapters) · [Next chapter →](10-area-changes-interaction-and-state-retirement.md)
