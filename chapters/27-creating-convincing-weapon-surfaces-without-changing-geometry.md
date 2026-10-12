# 27. Creating convincing weapon surfaces without changing geometry

[← Chapter index](../README.md#chapters)

Treat the UV layout, native alpha and internal material binding as part of the artwork.

## Start from the material actually used by the weapon
For a diffuse-only weapon edit, preserve geometry, rig, normal and specular maps. The private Broadsword example uses `w9300 / 0x770800`, derived from `w2105`, with a 256×128 diffuse. Inspect every referencing inventory record, including retired/private clones, before changing a shared binding.

Identify the material's diffuse import and the texture container's internal export name. Renaming the outer `.dds.phyre` file is insufficient. Match the internal DDS export name to the resource requested by the material; a correct outer filename with an old internal name can render a white weapon.

## Preserve the hilt from geometry-derived masks
Derive protected masks from the actual mesh faces and UVs. In the Broadsword example, faces 10–45 form the blade; the other 40 faces cover hilt, guard and pommel. Protect those UVs with a two-texel margin instead of using a broad rectangular atlas selection.

Fit new blade artwork into the native UV layout. Preserve alpha, hidden RGB and protected pixels through repacking. Account for private resource-name substitutions when comparing container geometry.

## What texture alone can suggest
Painted facets and internal-looking light can suggest crystal; controlled veins can suggest stone; directional highlights can suggest brushed metal; cracks with bright cores can suggest heated material. Their success depends on the existing mesh, shader, UV density and lighting. A diffuse edit cannot create real refraction, new silhouette geometry or guaranteed light emission from an opaque material.

---

[← Previous chapter](26-making-added-sounds-follow-the-games-sfx-volume.md) · [Chapter index](../README.md#chapters) · [Next chapter →](28-coloring-obtained-equipment-and-preserving-enemy-suffixes.md)
