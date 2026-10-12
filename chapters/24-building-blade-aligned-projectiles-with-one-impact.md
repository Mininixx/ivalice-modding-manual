# 24. Building blade-aligned projectiles with one impact

[← Chapter index](../README.md#chapters)

Use a real weapon reference, a game-time trajectory and one authoritative damage handoff.

## Reuse a coherent part of an effect
For the custom red slash, isolate one half of Aim's opposing arcs, preserve its animation and recolor the intended component. Use **Aim phase 56–94** for its contact burst. These phase numbers belong to that clip; do not substitute the whole two-sided circle or an unrelated Distiller burst.

The current example binds Broadsword record 4097 to private action 4261, effect 522 and clip 37. These IDs describe one installation and must be allocated again for a different content set.

## Follow the equipped blade, then release toward the target
Resolve the weapon attachment through `j_blade` selector `0x200` / `n_grip` selector `0x201`, using bounded child/sibling traversal. The field at `model+0x18` identifies an instance slot rather than a resource-model ID. Validate each hierarchy node and transform before using it.

Use the blade/socket-space span as the size reference; the Broadsword example uses about `0.944344922` along socket Y with a 1.5 visual multiplier. Keep origin, blade orientation, projectile travel direction and visual size as separate controls. An enemy-sized arc cannot substitute for a blade-sized origin just because both use a radius.

Sample the arc's ridge for collision (33 points in this implementation), sweep between successive game-time positions and update against the target's current placement. Sparks originate on that moving ridge, live for 0.5 game-seconds and fade throughout that lifetime. Pausing the game must freeze both movement and spark aging.

## Contact owns the damage event
The original action callback and the projectile can both reach damage. Removing an event from the visual clip alone is insufficient; arbitrate the shared combat authorization.

Place an `irfm_flight_hit` gate **before** the once flag and finalize through `irfj_result` with the exact authorized RESULT buffer, source, target and callback context. Consume the authorization once. A burst can then finish playing without any further combat event; the visual-only clip excludes events 3/128.

```text
accepted native hit → authorized pending projectile
projectile contact → authenticate result → consume once → native damage
                   → target-anchor burst + one impact sound
late animation callback → no remaining authorization → no second damage
```

Place the burst at the normal native target anchor even if collision occurs at a different ridge point. Retire target-dependent work on miss, death or identity loss, and keep late callbacks from reusing a consumed result.

---

[← Previous chapter](23-placing-and-scaling-effects-on-real-actors.md) · [Chapter index](../README.md#chapters) · [Next chapter →](25-resolving-sound-events-to-the-correct-audio-stream.md)
