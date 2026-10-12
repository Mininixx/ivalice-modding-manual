# 29. Encounter identity and reward placement

[← Chapter index](../README.md#chapters)

An encounter combines a species/model, spawn record, behavior, progression context and rewards. Keep those identities separate when editing vanilla data.

## Inventory the native encounter

Record the area/subarea, spawn conditions, actor template, model, scale, faction, territory, entry animation and AI action groups. Include phase-dependent behavior and scripts that the actor can reach indirectly. A renamed actor can still reference the same native species and shared behavior.

Follow shared records before editing them. A template or Action used by several areas will affect every consumer if changed in place. Prefer an explicitly allocated local record when the requested change is local, after checking all native index limits.

## Preserve initialization and progression

Copying a behavior script does not supply compatible spawn initialization, skeleton, attachments, animation or death/despawn behavior. Determine which native record owns each part. Preserve story triggers, quest rewards and noncombat interactions unless the change explicitly targets them.

Compare model bounds and scale together. Equal scale numbers applied to different meshes do not imply equal world size. Retain a coherent relation between encounter role, movement space, durability and available player resources.

## Trace a reward to an actual inventory item

An item name is insufficient to classify a reward. Resolve its native inventory identity and check whether it is equipment, a consumable, loot/bazaar material, currency or quest data. For consumables, establish the executable Action or use contract rather than assuming every gem-like name means an item usable in combat.

Treat ordinary drops, rare rewards, steals and treasure contents as distinct consumers. Identify the condition and selection process of each table before changing a weight or chance.

For a multi-stage reward path, probability follows its conditional stages:

```text
P(item) = P(spawn) × P(reward selection | spawn)
          × P(item selection | spawn, reward selection)
```

The values must come from the actual native rules. Do not multiply unrelated table percentages as if the events were independent. A catalog entry with no reachable spawn/reward path will not appear during ordinary play.

Keep a before/after record of the exact native data entries being changed, including shared references and language-dependent text. This chapter imposes no custom classes, regional quotas or item allocations.

---

[← Previous chapter](28-coloring-obtained-equipment-and-preserving-enemy-suffixes.md) · [Chapter index](../README.md#chapters) · [Next chapter →](30-native-addresses-and-hook-ownership.md)
