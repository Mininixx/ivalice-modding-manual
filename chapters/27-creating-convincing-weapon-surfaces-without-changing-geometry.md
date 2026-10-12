# 27. Creating convincing weapon surfaces without changing geometry

[← Chapter index](../README.md#chapters)

A native weapon's appearance depends on mesh, UVs, textures, internal resource names and material state. A diffuse edit changes only part of that system.

## Find the resource actually used

Resolve the equipped weapon record to its model and material resources. Record every model variant or equipment record sharing those resources before editing them. A shared texture can affect more than one inventory item.

Inspect both the outer `.dds.phyre` filename and the container's internal exported resource name. A material can request the internal name; renaming only the outer file does not establish a new binding.

Use the public [FFXII format/tool repository](https://github.com/StyuDEV/ffxii-tza-tools) to inspect model and texture containers when its documented formats match the input. Read each tool's input/output contract before repacking; a glTF export is not itself a game-ready replacement.

## Preserve the intended geometry and material

For a texture-only edit, retain vertex positions, rigging, UV coordinates, normals and the material's existing normal/specular bindings. Separate blade, guard, grip and pommel using the actual mesh and UV islands rather than guessed rectangles.

Create masks from the relevant UV triangles, with padding appropriate to the sampler. Account for overlapping UV islands: changing one texel may affect several surfaces. Preserve alpha and palette representation where the resource requires them.

## Understand the limit of a diffuse texture

Painted highlights can suggest polished metal or crystal, but they do not create new geometry, physical refraction or guaranteed emission. Inspect the native shader and material before promising those effects. A material parameter edit is a different change from a diffuse edit and should be documented separately.

Retain an unchanged native input and compare the rebuilt container's structure, names, dimensions and pixel format with it. Keep the original asset outside the edited output directory. A successfully exported preview does not prove that the native resource loader will accept the replacement.

---

[← Previous chapter](26-making-added-sounds-follow-the-games-sfx-volume.md) · [Chapter index](../README.md#chapters) · [Next chapter →](28-coloring-obtained-equipment-and-preserving-enemy-suffixes.md)
