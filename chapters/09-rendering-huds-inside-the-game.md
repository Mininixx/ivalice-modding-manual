# 09. Rendering HUDs inside the game

[← Chapter index](../README.md#chapters)

A new HUD needs a renderer implemented by the extension. Vanilla does not expose a shared-memory panel protocol or a function that accepts arbitrary desktop-window pixels.

## Direct3D 11 integration

Obtain the swap chain/device/context from the game's actual rendering path. A device created for a separate application is not the game's device. Select a render-thread interception point, preserve the original call and draw using the current backbuffer dimensions.

For a basic image panel, the extension creates a texture, shader-resource view, vertex/index buffers, shaders and blend state. Upload new pixels only when their content changes. Place the quad in viewport coordinates and preserve its aspect ratio; display resolution and logical UI coordinates are separate quantities.

The graphics resources and hook installation are code to supply explicitly. They are not available merely because this manual contains a HUD chapter.

## Choose one alpha representation

For premultiplied color, multiply RGB by alpha once when preparing pixels and use source factor ONE with destination factor INV_SRC_ALPHA. For straight color, retain unmultiplied RGB and use SRC_ALPHA for the source RGB factor. Do not mix these representations.

```cpp
D3D11_BLEND_DESC desc{};
auto& rt = desc.RenderTarget[0];
rt.BlendEnable = TRUE;
rt.SrcBlend = D3D11_BLEND_ONE;
rt.DestBlend = D3D11_BLEND_INV_SRC_ALPHA;
rt.BlendOp = D3D11_BLEND_OP_ADD;
rt.SrcBlendAlpha = D3D11_BLEND_ONE;
rt.DestBlendAlpha = D3D11_BLEND_INV_SRC_ALPHA;
rt.BlendOpAlpha = D3D11_BLEND_OP_ADD;
rt.RenderTargetWriteMask = D3D11_COLOR_WRITE_ENABLE_ALL;
// CreateBlendState on the game's ID3D11Device; pixels must be premultiplied.
```

The byte order of CPU pixels must match the DXGI texture format. BGRA and RGBA are different layouts even when both contain four bytes per pixel.

## Restore state and rebuild resources

Restore every pipeline binding changed by the overlay, including render targets, depth/stencil, blend, shaders, buffers, textures, samplers, viewports and scissors. Release temporary COM references after restoring them. Avoid assuming that the game's next draw resets everything.

Before forwarding `ResizeBuffers`, release the extension's backbuffer references and views, then recreate them after success. Microsoft's [ResizeBuffers documentation](https://learn.microsoft.com/en-us/windows/win32/api/dxgi/nf-dxgi-idxgiswapchain-resizebuffers) explains the reference-lifetime requirement. Handle device removal separately from an ordinary resize.

A flat final-frame HUD does not provide world-space depth or native particle submission. Those require a scene-render boundary; see [Native effect submission](22-native-effect-resources-and-scene-submission.md).

---

[← Previous chapter](08-camera-state-collision-and-transitions.md) · [Chapter index](../README.md#chapters) · [Next chapter →](10-area-changes-interaction-and-state-retirement.md)
