# 19. Extracting effects from Final Fantasy X

[← Chapter index](../README.md#chapters)

Start with the command table, then collect the effect program, textures and sound dependencies.

## Restrict the source game explicitly
Use the FFX magic modules, `FFX_Data.vbf` and `FFX.exe` together. Keep X-2 separate. The module collection includes more than player spells; do not treat a DLL count as a spell count.

These are x86 effect modules. They call an engine API and depend on the original game's runtime. Loading one into the x64 XII process is not a porting strategy. The useful products are a catalog, recovered behavior, texture/mesh data and audio, followed by an implementation of the required behavior in the destination engine.

## Resolve ability → program IDs
The catalog reader examines the FFX battle kernel tables. Its header has four little-endian 16-bit values at `+8`; records begin at `0x14`. The supported record strides are `0x5C` and `0x60`. A record's first `uint16` points into the string pool after the record payload; the animation IDs are `uint16` values at `+0x10` and `+0x12`.

Use the command's name, menu category and both IDs together. Do not assume the first ID is always a caster effect and the second always a target effect. The white/black-magic menu categories are helpful filters, but would omit techniques, breaks and other requested effects.

| Ability | Effect IDs | Resolved sound IDs |
| --- | --- | --- |
| Slow | 14 | 9029 |
| Demi | 102, 103 | 9021; additional 14069 kept separate |
| Auto-Life | 114, 144 | 9016, 9035 |
| Power Break | 21, 326 | 9046, 9061 |
| Magic Break | 319, 327 | 9047, 9061 |
| Armor Break | 320, 328 | 9048, 9061 |
| Mental Break | 321, 329 | 9049, 9061 |
| Full Break | 699 | 9061, 10099 |
| Dark Attack | 26, 27 | 9064 |
| Silence Attack | 24, 25 | 9063 |
| Sleep Buster | 34, 35 | 9065 |
| Luck | 7 | 9044 |
| NulFrost / NulShock | 136, 137 / 140, 141 | 9023 / 9025 |
| NulTide / NulBlaze | 142, 143 / 138, 139 | 9026 / 9024 |

## Preserve the original inputs
Extract the magic tree, associated shaders and the relevant tables. Hash original bytes and maintain an output manifest. Preserve unsupported big-endian PS3 PHYR/GCM textures as originals; route them through an appropriate decoder instead of treating a missing PNG as missing source content.

Keep the game binaries and extracted proprietary assets local. A reusable knowledge document can distribute schemas, algorithms and small explanatory examples without embedding those assets.

---

[← Previous chapter](18-license-boards-prices-and-purchase-previews.md) · [Chapter index](../README.md#chapters) · [Next chapter →](20-sharing-ghidra-types-and-exporting-definitions.md)
