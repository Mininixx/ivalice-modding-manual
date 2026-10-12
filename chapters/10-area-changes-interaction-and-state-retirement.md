# 10. Area changes, interaction and state retirement

[← Chapter index](../README.md#chapters)

Treat a transition as a change of ownership, not merely a new map number.

## Observe several signals
The session layer reads battle, location, party layouts, user-control readiness, native menu ownership and modal state. The location structure has two area fields (`+0x1244`, `+0x125C`); they can disagree while a transition is in progress. A non-null actor pointer alone is insufficient permission to keep controlling it.

The area-transition source distinguishes the current area-slot table, pending area and a transition request containing destination, spawn and previous area. Preserve destination/spawn semantics. Sending every player to a guessed coordinate is not a substitute for a valid native route.

## Retire before reacquiring
1. Revoke active movement and command publications.
2. Hide or retire owned targets, circles and transient panels.
3. Cancel resource leases and audio tied to the old scene.
4. Wait for a coherent new session and resolve fresh actor identities.
5. Reacquire only the control and presentation that the new scene permits.

Interactions also need an owner: a follower’s proximity, use prompt and activation source must describe the same actor. Native dialogs and story events should remain native and should supersede ordinary battle UI. Keep rollback for partially acquired interaction state.

## Prefer an actionable chest/NPC prompt
In `private_player_interaction`, ignore zero handles and stale aggregate publications. Search all candidate slots for a usable `state >= 2` before falling back to a proximity-only state. A high-index outer/proximity entry must not hide a lower-index usable chest.

In `_world_interactions`, consult `native_interaction_router.prompt_interaction(player)` when the aggregate is absent **or not actionable**. Prefer an exact actionable descriptor for that player, with current handle and can-use status. Route Confirm to that native interaction before the battle-menu fallback. Keep native dialogue ownership and partial-acquisition cleanup intact.

## Keep facing behavior separate
Do not reintroduce delayed facing corrections on area entry or character selection. Preserve the current native orientation behavior unless orientation work is explicitly requested. A post-load rotation write can produce a visible wrong-to-correct turn even when its final angle is correct.

---

[← Previous chapter](09-rendering-huds-inside-the-game.md) · [Chapter index](../README.md#chapters) · [Next chapter →](11-adding-actions-without-breaking-existing-commands.md)
