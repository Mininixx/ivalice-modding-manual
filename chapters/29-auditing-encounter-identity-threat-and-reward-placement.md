# 29. Auditing encounter identity, threat and reward placement

[← Chapter index](../README.md#chapters)

Review a whole region, including combat NPCs and reachable AI actions.

## Work within the regional content rules
Before changing enemies, loot, chests, equipment, passives or hunt rewards, document the target region's allowed donor species, protected encounters, progression tiers, population totals and explicit reuse exceptions. Use the current game/mod data and the requested design constraints. If a proposed change depends on an unspecified rule, establish that constraint before changing content. The original Reforged regional design notes are not included in this repository; the workflow below describes the checks to apply in your own project. Keep Reforged-specific content changes out of standalone Ivalice Together.

Compare candidate families against the native population of every subarea and the current mod roster. A new name, recolor or alternate boss/Trial alias does not create a different species. Do not replace ordinary enemies with boss bodies. Preserve protected hunts and story actors; permission to borrow a model is not permission to rewrite its source encounter.

Place special enemies deliberately across the region rather than always selecting its first slots. Respect the authorized regional totals, access tiers and explicit reuse exceptions in the current rules. Do not invent a new universal population cap.

## Preserve threat, identity and entry behavior
Preserve the original encounter's relative size, durability and role. Compare mesh bounds as well as scale values; a regional giant should not become an ordinary-sized, ordinary-HP substitute. Use suitable weapons, posture, attachments and animation when the replacement species requires them.

When the original has an entry animation, supply a compatible entry for its replacement and retain the transition into movement/combat. Review native spawn initialization, faction, territory and despawn alongside the donor scripts. Copying four AI scripts alone does not establish a compatible spawn contract.

Inventory combat NPCs and every reachable action group and HP phase. Balance damage, healing, status duration, area, targeting, cadence and combos to the region. Use private actions/groups for local changes instead of modifying a shared global technique. Keep noncombat civilians and story interactions intact.

## Author usable rewards
Build a class-by-progression matrix covering chests, steals, ordinary drops, special drops and hunt sets. Distinguish loot/bazaar materials from usable consumables by native item identity and execution contract, not by an elemental-sounding name. Gemini Gem and Charger Barding must not stand in for usable gems or grenades where the reward is intended for immediate use.

Use the compiled inventory IDs and current consumable aliases when editing drops. Check spawn probability, route access, protected quest contents, complete equipment sets and all relevant regional data copies. A grenade in an item catalog is insufficient if no reachable loot path awards its inventory ID.

For new creature textures, retain native UVs, dimensions, alpha and material boundaries while creating the requested artwork. A palette filter alone does not satisfy a request for a new texture. Keep donor choice, encounter behavior and reward changes local to the authorized region.

---

[← Previous chapter](28-coloring-obtained-equipment-and-preserving-enemy-suffixes.md) · [Chapter index](../README.md#chapters) · [Next chapter →](30-native-addresses-and-hook-ownership.md)
