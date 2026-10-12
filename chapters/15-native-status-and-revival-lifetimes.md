# 15. Native status and revival lifetimes

[← Chapter index](../README.md#chapters)

Native status state, its visual presentation and revival placement have related but distinct lifetimes.

## Status storage and eligibility

The native command and movement routines in this executable read `actor+0x698` as the battle-status record and combine DWORDs at `+0x3C` and `+0x64`. These represent different status banks. Clearing one without examining the other can leave the effective status unchanged.

Follow the native apply/remove routines for the desired status. A visible bit does not describe all associated duration counters, immunities and action restrictions. Do not implement a persistent buff by reapplying its cast animation every update.

## Observe effect creation separately from updates

For effect lifecycle investigation, native call site `0x46F0AF` calls `0x3B8670` in the path beginning near `0x46EFD0`. Recover the caller's complete object and argument contract before attaching new behavior. An update callback that only sometimes sees an initial tick is not a reliable substitute for a creation callback.

If adding an attached visual, make the persistent effect state own its age and expiration. Make the current model own only the attachment. Replacing a model or recreating a draw object must not silently restart the logical duration.

## Native revival placement

Investigate `0x311F70` as part of the native resurrection-destination path. Follow an ordinary Phoenix Down through placement, effect timing, HP restoration, status changes and resumed AI. Recover the complete call signature and its prerequisites before invoking it.

Preserve the engine's distinction between preparing a destination and performing the revival. Moving a living actor or restoring HP early can produce different collision, animation and battle behavior from the native sequence.

The scene clock and pause behavior must determine any additional duration implemented by an extension. Real-world elapsed time continues while the game is paused and cannot be substituted without changing gameplay. This chapter does not assume an additional auto-revival system or imported halo asset.

---

[← Previous chapter](14-native-damage-modifiers-and-debuffs.md) · [Chapter index](../README.md#chapters) · [Next chapter →](16-replacing-status-icons-without-square-borders.md)
