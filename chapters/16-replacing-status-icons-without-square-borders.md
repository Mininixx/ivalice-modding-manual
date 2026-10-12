# 16. Replacing status icons without square borders

[← Chapter index](../README.md#chapters)

A status icon depends on its native draw descriptor, texture region, palette and active-status selection. Editing only the visible image may leave the actual selected frame unchanged.

## Trace from status to draw

Identify one stock status and follow its UI selection to the native descriptor. Record the selected frame, palette, UV rectangle, dimensions and texture resource. Inspect `tex2pack_ys.bin` and the corresponding native UI resources for the selected language/build; do not assume coordinates from another atlas.

Determine whether the UI uses one cell with a priority/cycling rule or separate cells for multiple statuses. Preserve that behavior when replacing an image. Drawing a second icon on top of the existing cell does not change native selection.

For a new icon, choose its region from an actual atlas inventory and update all referencing descriptors. No private frame number or spare palette is reserved by this manual.

## Account for filtered texture samples

Linear filtering can sample pixels outside the visually obvious icon boundary. A transparent centre does not prevent colored neighbors from bleeding through the edge. Inspect the native UVs, filtering mode, mipmaps and palette interpretation together.

Include padding appropriate to the atlas sampler and keep transparent-edge RGB consistent with the intended alpha representation. When scaling artwork, use an alpha-aware process so invisible RGB does not create dark or bright fringes.

Palette-based UI textures and direct-color textures require different edits. Preserve palette indices when editing an indexed image; a color-converted PNG does not automatically preserve the native palette mapping.

## Keep the replacement reversible

Retain the original descriptor and resource binding. Restore the normal image when the native status no longer selects the replacement. Use the same lifetime as the owning UI object and re-resolve descriptors after a scene or resource reload.

For native texture and material containers, consult the public [FFXII asset-format documentation](https://github.com/StyuDEV/ffxii-tza-tools). Its tools operate on extracted game files and are separate, explicitly named resources.

---

[← Previous chapter](15-native-status-and-revival-lifetimes.md) · [Chapter index](../README.md#chapters) · [Next chapter →](17-native-save-boundaries.md)
