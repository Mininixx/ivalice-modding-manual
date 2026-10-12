# 14. Implementing Breaks and bounded debuffs

[← Chapter index](../README.md#chapters)

Represent combat modifiers by owner, damage family and lifetime instead of destructive stat edits.

## Four independent modifiers
| Debuff | Operation at the damage boundary |
| --- | --- |
| Power Break | Source’s physical damage × 0.75 |
| Magic Break | Source’s magical damage × 0.75 |
| Armor Break | Target’s physical damage received × 1.25 |
| Mental Break | Target’s magical damage received × 1.25 |
| Full Break | Enable all four effects |

This is a model of outgoing/incoming damage, not an instruction to subtract 25% from every attack/defense attribute. Distinguish physical and magical damage in the native calculation path, and leave healing and unrelated results outside the modifier.

Apply these custom Breaks after an actual HP-reducing hit. Reapplication does not stack another multiplier. Records are retired on KO, despawn, scene/save changes or identity reuse. Include the debuff in any “target is debuffed” query used by other passives.

Armor Break also neutralizes **Resist Piercing Damage** for the affected piercing-weapon calculation, considering both permanent and temporary banks. It does not erase an enemy’s augment data globally. Validate the intended defense exception at the calculation that consumes it.

## Count actions, not result callbacks
A separate weakening skill halves the target’s next two damage-dealing attacks. One area action may emit several target RESULTS; consuming one charge for each result would make its duration depend on target count. Track the offensive action identity and spend the debuff charge once for that action. Healing does not consume it.

---

[← Previous chapter](13-damage-status-results-and-enemy-reaction.md) · [Chapter index](../README.md#chapters) · [Next chapter →](15-persistent-buffs-halos-and-automatic-revival.md)
