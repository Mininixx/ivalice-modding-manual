# 11. Adding actions without breaking existing commands

[← Chapter index](../README.md#chapters)

An action record, a visible menu entry and an executable skill are separate deliverables.

## Begin with the authenticated installed content
Start from the current installed Lua, native DLLs, frozen menu modules and Battle Pack, then create staging. Historical foundation generators and loose Python trees may omit later composed changes. Do not rebuild over the current installation from an old prototype or retail baseline.

The Battle Pack has 71 sections: Actions in section 14, equipment in section 13 and English text groups in section 61. `Action+0x34` is a name reference, not necessarily the Action ID. Keep the loaded pack and the menu's mirrored pack identical.

## Allocate through the registry and lock
Read `IvaliceReforged/foundation/SKILL_RELEASE_WORKFLOW.md`, `content/ability_registry.json` and `content/ability_allocation_lock.json`. Preserve existing IDs, including retired records and deliberate shared owners. Never compact IDs or regenerate the allocation lock merely to accept a conflicting change.

| Reservation / boundary | Rule |
| --- | --- |
| Actions `111–114`, effects `504–507` | Dynamic Mix leases; never permanent skill slots |
| Effects `723/724` | Reserved even without a direct Action-table consumer |
| Menu IDs `>=0xFF00` | Selectors/sentinels, not ordinary executable Actions |
| Effects above `511` | Require their own routing, metadata and initialization |
| Action table | Read its current extent; 8,048 records in the 11 October layout |

Request a read-only allocation proposal with `python -m IvaliceReforged.foundation.ability_plan <staging> --actions 3 --effects 1`. A proposed ID is not proof of executable capacity. Extend every affected consumer bound, including the native execution checks and `irfj_mix_prepare`, plus category buffers and save/ownership ranges where applicable. There is no universal 511 limit; never globally replace 511/512.

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
Canonical classes are 0 Mystic, 1 Rift Assassin, 2 Gambler, 3 Skullbreaker, 4 Templar, 5 Transmuter, 6 Beastlord, 7 Renegade and 8 Arcanist. Saved IDs 9/10/11 alias 0/1/2. Use `foundation/license_ownership.py` and native `irid_matches`; sparse saves use the assigned primary class. A stale secondary or visible class byte must not grant an ability.

## Compose the complete dependency chain
Register Action/effect, menu, license, admission, payment, calculation, application and cleanup together. Declare intentional sharing. An existing Action change needs its ID, before/after record hashes and reason in `skill_release_contract.json/reviewed_action_changes`.

Preserve one pending manual order per member in `irfq`. Retain readiness and initialization guards. When changing Lua, update the blackhole authentication dependency, then blackhole-visual; preserve their code and guards. A shader change requires the matching FFX compiler/hash chain. Embedded assembly comments must not contain a literal `%`, which the Lua loader can interpret as a placeholder delimiter.

Update all affected dependency records and the exact-candidate native validation artifact required by the release workflow. Run `python -m IvaliceReforged.foundation.ability_registry <staging>` before installation; resolve failures at their source rather than copying stale approval fields or weakening guards. Install with the game closed, authenticated preimages and a rollback copy.

---

[← Previous chapter](10-area-changes-interaction-and-state-retirement.md) · [Chapter index](../README.md#chapters) · [Next chapter →](12-queueing-commands-on-the-game-thread.md)
