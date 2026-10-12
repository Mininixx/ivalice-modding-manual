# 13. Damage, status results and enemy reaction

[← Chapter index](../README.md#chapters)

A hit can change HP while silently losing the reaction that should follow it.

## Work at the native RESULT boundary
The physical-impact implementation preserves a complete RESULT before chaining the prior applicator. At this result boundary, result kind at `+4 == 0` and flag `+0x2C & 0x100` identify the successful physical-result case. Misses and blocks should not produce the same status/impact treatment as damage-bearing hits.

For added Blind, Silence and Sleep, private calculator records use native routines `0x385F60` and `0x387CB0`. Merge only the accepted status bit and its counters into the weapon RESULT. Preserve unrelated HP/MP fields, status fields and global scratch state. A newly applied Sleep must not be removed by the very hit that applied it.

## Trace reaction after the applicator
Follow both the retail applicator (`0x3112F0`) and subsequent enmity/AI feedback. Preserve reaction ownership when wrapping the applicator; an early `xor eax,eax; ret` after damage can suppress a later stage.

Authenticate these post-hit boundaries: save epoch mismatch; null battle; changed battle; null location; changed location; location area at `+0x1244` mismatch; location UI area at `+0x125C` mismatch. Do not remove these guards globally; make result delivery and reaction use the same current identity.

Read the child-hit record using stride `0x50`, a DWORD count and up to 16 **4-byte full handles**, indexed from 1. Do not widen those handles based on a stale comment.

## Keep class damage and utility scaling separate
For Skullbreaker, define 100 percent base damage as the native basic Attack result using the equipped weapon, then apply that skill's modifiers. Preserve the native damage family, defense and accepted-hit semantics.

For Transmuter, apply the damage-only `irmd_offense` bonus at native Mix admission and freeze it in the accepted recipe. Only category `0x10` uses this offense helper. Require canonical primary class 5 and actual ownership of Alchemical Craft 169 plus each contributing license; preserve live admission registers, including R10/R11. Keep healing, revival, status duration, ingredient use and cleanup on their own paths.

Use the current license-driven progression: core 169 adds 20 percent; nodes 735/736/745/746 add 25 each, 747/753/754 add 20 each, 734/762/763/1160/1161 add 14 each, and 1174/1175/1176/1177 add 30 each. These are additive offensive bonuses, not a replacement for existing buff potency. Do not reactivate the retired offense immediates alongside the helper; that would count bonuses twice. Keep native help and both custom-node catalogs synchronized with future changes.

---

[← Previous chapter](12-queueing-commands-on-the-game-thread.md) · [Chapter index](../README.md#chapters) · [Next chapter →](14-implementing-breaks-and-bounded-debuffs.md)
