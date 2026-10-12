# 21. Recovering particle programs and their timeline

[← Chapter index](../README.md#chapters)

Port the animation rules before judging whether a texture collection reproduces the original effect.

## An effect is more than an atlas
Use recovered effect programs, deterministic particle state and the matching HD textures. A manually arranged atlas cannot reproduce the timing and geometry by itself. Retain the original license and attribution when reusing the MIT-licensed interpreter implementation.

Slow's PS2 program is `000e.bin`; Demi's is `0066.bin`. Reconstruct required HD callbacks separately. Preserve the port's capability limits: approximate Lambert/Blinn lighting, unsupported CircleBlur and incomplete distortion must not silently become claims of PC-DLL equivalence.

## Make time reproducible
The reference interpreter steps at 30 Hz. The destination clip runtime can use a different tick rate, so convert units explicitly. Keep a deterministic random seed and restore simulation history when seeking backward. Moving the preview camera must redraw the same particle state, not advance the effect.

Export enough data per draw to preserve geometry, transforms, UV scrolling, flipbooks, vertex color, blend mode and lifetime. Preserve buildup, steady phases, disappearance and the final clear frame across repeated casts and camera changes.

## Decode callback semantics, not just numbers
Interpret Demi callback value `0x1E` as callback timing, not a second emitter's birth delay. Derive units from the program execution model.

Compare Distiller data, textures and sound selections independently of executable code. Relocation-normalized code equality does not imply equality of the complete visual program.

For color variants, retain geometry, UVs and alpha, then adjust the intended color stage. Size the visible rim, not a bounding box dominated by transparent vertices. Verify that HDR or additive white regions still preserve readable color in the actual destination renderer.

---

[← Previous chapter](20-sharing-ghidra-types-and-exporting-definitions.md) · [Chapter index](../README.md#chapters) · [Next chapter →](22-getting-imported-effects-into-the-native-scene.md)
