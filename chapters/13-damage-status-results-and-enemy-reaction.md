# 13. Damage, status results and enemy reaction

[← Chapter index](../README.md#chapters)

Damage calculation, result application and post-hit behavior are separate stages. Calling only an HP writer bypasses the rest of the native action.

## Follow one ordinary native attack

Begin at the accepted command described in [Chapter 04](04-independent-menus-with-native-command-execution.md). Follow its charging/execution path, the impact callback, the result calculator and the applicator. Record arguments at each boundary and identify which component owns target iteration and resource payment.

For the reference executable, `0x3112F0` is an applicator boundary to investigate, and `0x325260` belongs to the physical-hit route. These addresses are reverse-engineering entry points. A complete callable prototype for these routines is not supplied here.

In the result layout associated with this physical route, a DWORD kind at `+4` equal to zero and flag `0x100` in the field at `+0x2C` distinguish one successful physical-result case. Confirm the containing record and field widths in the selected routine; the same offset in another object has no implied meaning.

## Preserve the full result

Inventory every field written by the calculator before modifying one. HP, MP, status changes, hit/miss/block outcomes and presentation can share a result record. Preserve unknown fields and native scratch-state ownership. Copying only damage into an unrelated temporary buffer is not a complete result.

For added status behavior, follow the native immunity and application path rather than setting an actor's status bit directly. A status can need counters, duration, immunity handling, icons and interaction with the same hit that applied it.

## Retain post-hit execution

After application, follow hate/enmity, reaction animation, AI notification, death processing and the command's cleanup. An early return after subtracting HP can suppress all of those stages. A visible damage number is not proof that the action completed correctly.

If building a modifier, identify its intended family and boundary first. Apply it once to the selected native result while leaving misses, healing, unrelated resource changes and already-finalized results untouched. Do not allocate a new Action or effect merely to change a result unless its native execution route actually requires that allocation.

---

[← Previous chapter](12-queueing-commands-on-the-game-thread.md) · [Chapter index](../README.md#chapters) · [Next chapter →](14-native-damage-modifiers-and-debuffs.md)
