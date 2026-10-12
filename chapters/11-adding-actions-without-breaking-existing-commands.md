# 11. Adding actions without breaking existing commands

[← Chapter index](../README.md#chapters)

An action record, a visible menu entry and an executable skill are separate deliverables.

## Begin with the authenticated installed content
Start from the current installed Lua, native DLLs, frozen menu modules and Battle Pack, then create staging. Historical foundation generators and loose Python trees may omit later composed changes. Do not rebuild over the current installation from an old prototype or retail baseline.

The Battle Pack has 71 sections: Actions in section 14, equipment in section 13 and English text groups in section 61. `Action+0x34` is a name reference, not necessarily the Action ID. Keep the loaded pack and the menu's mirrored pack identical.

## Track allocations in your project
Maintain an allocation registry in the project you are editing. For each Action and effect, record its ID, owning feature, active/retired/reserved state, intentional sharing and dependent consumers. Keep a versioned baseline of these assignments so a later addition cannot silently reuse an existing slot. The internal Reforged registry and planning tools are not included here; no particular directory layout or unpublished command is required to apply this process.

If no registry exists, inventory the loaded Action/effect tables and their menu, script and native-code consumers before allocating IDs. An empty-looking record may still be reserved or leased dynamically. Preserve existing IDs, including retired records and deliberate shared owners. Never compact IDs or regenerate the baseline merely to accept a conflicting change.

The following reservations describe the reference Reforged layout. Reconcile them with the actual target version; they are not universal allocations for every FFXII mod.

| Reservation / boundary | Rule |
| --- | --- |
| Actions `111–114`, effects `504–507` | Dynamic Mix leases; never permanent skill slots |
| Effects `723/724` | Reserved even without a direct Action-table consumer |
| Menu IDs `>=0xFF00` | Selectors/sentinels, not ordinary executable Actions |
| Effects above `511` | Require their own routing, metadata and initialization |
| Action table | Read its current extent; 8,048 records in the 11 October layout |

Prepare a read-only allocation proposal before editing the pack: list how many Action/effect records the feature needs, the candidate IDs, evidence that each is free and every consumer that must accept it. A proposed ID is not proof of executable capacity. Extend every affected consumer bound, including native execution checks, custom command preparation, category buffers and save/ownership ranges where applicable. In the reference implementation, `irfj_mix_prepare` is one such preparation consumer; locate the equivalent boundary in the code you actually have. There is no universal 511 limit; never globally replace 511/512.

## Preserve the native execution contract
| Field or boundary | Rule |
| --- | --- |
| `Action+0x1E` | Native category; 2 is Technick in this path |
| `Action+0x09` | Action charge field |
| `Action+0x0C`, bit 27 | Selects weapon charge from `Weapon+0x27` |
| `Action+0x24` | Physical Attack clones retain signed `-1` |
| `Action+0x26` | Keep the physical clone's native value; zero in this contract |
| Admission | Resolve class, actual ownership, MP/resource, target and execution state |

For physical techniques, retain the normal weapon-hit route at `0x325260`; a positive visual EFX in the physical contract can suppress that hit. Attach a separate visual-only carrier when needed. For Skullbreaker, calculate the 100% base through native Attack (Action 150) with the **currently equipped weapon**, then apply the skill multiplier. Do not substitute a fixed magic/base-power formula.

## Use canonical class identity
Canonical classes are 0 Mystic, 1 Rift Assassin, 2 Gambler, 3 Skullbreaker, 4 Templar, 5 Transmuter, 6 Beastlord, 7 Renegade and 8 Arcanist. Saved IDs 9/10/11 alias 0/1/2. Use the same canonical-ID mapping in offline content generation and runtime ownership checks. The reference native matcher is named `irid_matches`; it is an implementation symbol, not a helper included here. Sparse saves use the assigned primary class. A stale secondary or visible class byte must not grant an ability.

## Compose the complete dependency chain
Register Action/effect, menu, license, admission, payment, calculation, application and cleanup together. Declare intentional sharing. For every intentional change to an existing Action, record its ID, before/after record hashes and the reason in your project's change manifest. Compare this explicit list with the staged binary diff so unrelated records cannot change silently.

Preserve one pending manual order per member; the reference queue owner is `irfq`. Retain readiness and initialization guards. Follow the dependency graph of the implementation being edited when changing Lua or shaders. In the reference Reforged build, Lua authentication updates precede blackhole-visual updates, and imported FFX shaders have a matching compiler/hash chain. These are implementation-specific dependency relationships, not tools shipped with this manual. Preserve the corresponding code and guards when those components are present. Embedded assembly comments must not contain a literal `%`, which the Lua loader can interpret as a placeholder delimiter.

Validate the exact staged files against the allocation baseline before installation. Check duplicate or reserved IDs, intentional sharing, changes to existing records, declared dependency hashes, table extents and execution-path bounds. Use the target project's available tools or implement these checks against its actual data formats; this documentation repository does not provide a registry validator. Resolve mismatches at their source instead of replacing the expected baseline or weakening guards to make a conflict pass. Install with the game closed, authenticated preimages and a rollback copy.

---

[← Previous chapter](10-area-changes-interaction-and-state-retirement.md) · [Chapter index](../README.md#chapters) · [Next chapter →](12-queueing-commands-on-the-game-thread.md)
