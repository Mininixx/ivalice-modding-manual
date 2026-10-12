# 08. A shared camera that still respects the scene

[← Chapter index](../README.md#chapters)

Use formation-aware focus while keeping collision and native camera ownership explicit.

## Derive focus from the current formation
Use valid controlled actors to compute group centre, horizontal separation, bounded vertical separation and filtered velocity. Keep separate settling times for focus, zoom-out and zoom-in. Bound sample speed and age; a teleport must not become a velocity spike. Keep P1 camera input independent of P1's alive/reserve state.

Limit camera-height obstruction filtering to a bounded corridor between the controlled actors. Retain floors, ceilings and geometry outside that corridor. Preserve native wall pressure, hysteresis and recovery; release control for scripted scene cameras.

## Keep a committed camera through the outgoing area
Use the native current area, pending destination and coherent world signature together. Current/UI location slots update separately while unloading; their temporary disagreement must stop new admission without instantly revoking an already committed outgoing camera.

In `camera_area_admission`, freeze the last complete admitted output while the source area is still leaving. Keep renderer ownership and suspend camera integration. Use the bounded hold lease (500,000 microseconds in the current protocol); a dead worker must not hold the scene forever. Do not keep dereferencing retired actors to maintain that image.

For the new area, revoke old collision corridors, resolve fresh actor identities and positions, seed the new goal, and publish a new admission generation. A renderer goal ACK is insufficient: require a subsequent active output commit before enabling the new camera consumers. Revalidate world/owner identity at that final enable boundary. Do not restore a prior-area camera cache into the new scene.

## Suspend calculation during Party and Pause
Treat a modal menu in the same world as suspension, not camera destruction. Keep orbit, focus, zoom and collision history; stop position integration, velocity updates and elapsed game-time accumulation while the menu is open. The renderer may keep presenting the last committed frame and renewing the bounded hold.

On close, confirm area and world identity. Resume from preserved camera state; clear stale present timestamps and velocity samples so the pause duration cannot cause a jump. Use `camera_reset_for_ownership` to avoid calling `controller.reset()` for a same-world menu handoff. Reset/reseed normally for an actual area/save change or invalid identity. A broad reset on every ownership transition causes the visible camera snap when leaving menus.

---

[← Previous chapter](07-target-arrows-and-action-lines.md) · [Chapter index](../README.md#chapters) · [Next chapter →](09-rendering-huds-inside-the-game.md)
