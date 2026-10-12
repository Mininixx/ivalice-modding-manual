# 16. Replacing status icons without square borders

[← Chapter index](../README.md#chapters)

Edit the native draw descriptor and account for the texture samples around the visible artwork.

## Replace the intended cell
Drawing a new icon beside a native status icon produces two competing layouts. The working replacement wraps the native descriptor, selecting a private frame while the custom buff is active and restoring the normal descriptor after consumption. A priority policy decides which icon occupies that same cell when several custom/native statuses coexist.

One implemented halo icon uses section 5 of `tex2pack_ys.bin`, private frame 89, palette 59 and a `(64,800,52,64)` rectangle. Those are allocated project slots; re-audit availability before adopting them in another implementation.

## The visible square can originate outside the artwork
Account for fractional sampling outside the visible frame. For the private Fire weakness icon, use the isolated `y=704` frame instead of `y=640`, which reaches the adjacent Slow row through the Fire palette. Centre transparency alone cannot prevent that neighbor contamination.

Keep alpha-zero padding large enough for the native UVs and filtering. Resize artwork with an alpha-aware/premultiplied method, then deliver it in the representation the native atlas expects. Do not transplant the HUD panel blend contract into the atlas blindly.

---

[← Previous chapter](15-persistent-buffs-halos-and-automatic-revival.md) · [Chapter index](../README.md#chapters) · [Next chapter →](17-saving-new-resources-inside-each-save.md)
