# 17. Saving new resources inside each save

[← Chapter index](../README.md#chapters)

Serialize stable game data and validate it before accepting a custom trailer.

## Preserve the native save and the current schema
Keep the native 353,936-byte image intact and append one versioned extension with magic `IRFWI001`. Read the schema and lengths from the current reader/writer contract; do not rebuild current saves using the older v3 592-byte trailer. The schema-7 layout uses a 2,560-byte extension, giving a 356,496-byte decoded image. These are decoded payload sizes, not an instruction to overwrite the encrypted file directly.

Use the same version, length, counts and checksum definitions in preparation, serialization and import. The native image and custom payload have separate FNV-1a checks. Reject malformed sizes, invalid fractions and incompatible records before publication. Keep supported legacy readers while writing the current schema.

Store stable inventory/member/resource data, including fractional charge progress. Do not serialize actor pointers, effect leases, pending orders or process-local timers. Bound every record before reading it, and import class/resource state only after native load completion and coherent identity.

## Keep inventory extents consistent with save preparation
The “at least 100 KB” save message can be reached when custom serialization fails, even if disk space is available. Inspect the preparation result and the equipment-bank guards before assuming a storage problem. `irfw_touch`, `irfbh_touch` and `irfcu_touch` must agree with the actual equipment table extent; the current bank has **1,137 records**, not 1,136. When changing content, derive the new count from the pack and synchronize all consumers and restoration code.

Abort a failed preparation before flushing a partial native stream. Preserve loader callback chaining in ordinary and offset-read paths. On overwrite, replace the extension rather than appending another copy. Keep resource import distinct from transient-state retirement so a new save epoch cannot erase the bars imported from that accepted load.

## Keep player saves outside development mutations
Stage changes to the runtime and schema, preserve rollback preimages and respect the user's authorization before operating on saves. Update native DLL authentication when the Lua save code changes. Never bypass a failed initialization/readiness guard to make a save operation appear available.

---

[← Previous chapter](16-replacing-status-icons-without-square-borders.md) · [Chapter index](../README.md#chapters) · [Next chapter →](18-license-boards-prices-and-purchase-previews.md)
