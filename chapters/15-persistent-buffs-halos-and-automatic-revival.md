# 15. Persistent buffs, halos and automatic revival

[← Chapter index](../README.md#chapters)

Bind state to the character, visuals to the current model and timing to the game clock.

## Grant at the effect birth boundary
For Auto-Life, use PAGE birth: `0x46EFD0` reaches the complete call at `0x46F0AF` to `0x3B8670`. A listener on PAGE update (`0x4FF2FE`) that requires tick zero can miss birth entirely.

Intercept the complete birth call, authenticate private EFX, generation, caster and ally, then grant once. Preserve the original native call for every effect. Keep cast creation, buff publication, presentation and consumption as separate stages.

## Keep the actual halo component
Use the golden halo component: **TBP 14608**, texture index 2, mesh 33, behaviour 2, programs 1/2. It begins at sampled frame 41 (native tick 82), and is fully formed at frame 66 (tick 132). Holding that assembled phase preserves the original trails and sprites instead of repeatedly restarting the entire cast.

The persistent visual follows `j_kao` (selector `0x1000`) above the live head, with an offset based on native radius. Its age belongs to the buff record, not a renewable EFX slot. Recreating the visual carrier must not restart formation. Keep the persistent halo silent; the cast owns the cast sound.

## Revival placement must precede the intended visual
The automatic buff consumes once after ordinary KO and waits one game-second before native revival. For manual Phoenix Down, prepare the native resurrection destination through `0x311F70` before the visual effect and retain the engine’s “position already prepared” marker. Do not revive early or reposition arbitrary living actors.

For independently expiring stack buffs, store one expiry per accepted cast. The custom Luck policy is +3 for 20 game-seconds per cast; a recast adds a new expiry instead of resetting the first one. Pause and save/scene transitions must follow an explicit lifecycle policy.

---

[← Previous chapter](14-implementing-breaks-and-bounded-debuffs.md) · [Chapter index](../README.md#chapters) · [Next chapter →](16-replacing-status-icons-without-square-borders.md)
