# 19. Native effect assets

[← Chapter index](../README.md#chapters)

Begin with a native XII action and resolve the resources that produce its visible effect. No effect interpreter or runtime from another game is assumed.

## Build a resource dependency chain

Record the Action ID, its effect reference, the resource selected by the native effect path, and all textures, meshes, materials, animations and sound references consumed by that resource. Keep numeric record IDs separate from archive names and internal container names.

Extract the required files from the user's own `FFXII_TZA.vbf` into a separate working directory. Use the archive extractor's actual file list; do not construct a resource path from a translated spell name. Preserve the extracted bytes before decoding or converting them.

## Distinguish native formats

Character `.cm` and `.ca` files use `@FRP` containers for model and animation data. HD resources also use `.phyre` containers. A container's extension does not establish its complete internal type or the expected renderer contract.

The public [ffxii-tza-tools project](https://github.com/StyuDEV/ffxii-tza-tools) documents these asset formats and supplies named, inspectable Python tools. Its README lists the required Python version, input types and command-line usage. It is an optional external tool source, not a DLL expected to be loaded in the game.

## Produce an inspectable inventory

For each extracted dependency, record:

| Field | Purpose |
| --- | --- |
| Archive path and file hash | Identify the exact input |
| Container type and internal name | Identify what the resource loader expects |
| Parent reference | Explain why the resource is needed |
| Decoded properties | Dimensions, vertex format, material or animation data |
| Unsupported fields | Preserve them rather than silently dropping them |

Work first with an unchanged native resource. Establish that extraction, decoding and any repacking preserve its structure before adding an edit. A converter producing a viewable image does not prove that the game can load the repacked container.

This chapter covers discovery and inventory. Use the specific format documentation for actual decoding; do not invent an all-purpose “effect DLL” interface. Keep copyrighted game assets local and publish independently written schemas or explanatory code instead.

---

[← Previous chapter](18-license-boards-prices-and-purchase-previews.md) · [Chapter index](../README.md#chapters) · [Next chapter →](20-sharing-ghidra-types-and-exporting-definitions.md)
