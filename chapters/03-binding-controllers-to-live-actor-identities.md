# 03. Binding controllers to live actor identities

[← Chapter index](../README.md#chapters)

Keep device, player, party member, actor and visual object identities distinct.

## Keep the ownership chain explicit
| Identity | Responsibility |
| --- | --- |
| Physical device | Samples, backend, connection and reconnect policy |
| Player slot | Menu state, palette and input routing |
| Persistent party member | Character-specific data |
| Live actor handle and generation | Current world entity |
| Model and physics object | Current rendering and movement representation |

Resolve these identities from the same coherent session snapshot. Party order is not player ownership, an actor address can be reused, and a handle is not a model-array index. Battle layouts begin at `+0x5A48`, stride `0x12`; read the native leader separately at `+0x5AA4`. Choose the intended current/UI/menu layout explicitly.

## Isolate XInput, SDL and the desktop owner
Sample each assigned device once per update. Normalize buttons and axes through its actual backend; a device shown by SDL need not expose an XInput slot. Deduplicate a physical pad represented by both backends rather than assigning the same input to two players. A missing P2/P3 device must not fall back to P1.

Assign keyboard and mouse to a single player. With desktop owner P1, retain native movement, camera and native game bindings. With desktop owner P2/P3, filter native desktop gameplay input so it cannot also operate P1. Keep permitted native frontends usable under their own input ownership.

For P1's replacement menu, read the game's `keymap.ini` and native key conversion table. In the keyboard mapping, `Circle` means Confirm and `Cross` means Cancel. `DecideButton` selects the physical gamepad face button; applying it to keyboard semantics can reverse Space/Enter and Backspace. Do not synthesize keys or rewrite the user's profile to compensate.

If a controller appears in the launcher but not in the game, inspect native input ownership and Steam Input before changing SDL/XInput code. For this runtime, disable Steam Input for FFXII and **restart the game** before reassessing device routing. Launcher detection alone does not establish which input reaches the native consumer.

## Admit frontend navigation before a field actor exists
Title and Load Game menus must retain native D-pad navigation while the co-op field session initializes. Do not claim custom directional ownership merely because the mod is enabled. Set the field-navigation latch only after gameplay readiness, a coherent world signature and a materialized active party are present. Do not use a startup timeout to release those directions.

## Transfer the complete role after KO or selection
Use one shared role identity for movement, commands, selectors, target indicators, HP palette and menu presentation. On KO, choose only a living, command-eligible, active party actor that is not owned by another enabled player. Include eligible guests. Re-read the session before committing; Stop, Stone, a disappearing actor or an incompatible execution state must not become a destination merely because HP is positive.

If no free actor exists, keep the player in reserve and block their gameplay input from reaching another player's native leader. Keep Party, Pause and Character Select available under the appropriate frontend policy. Permit an explicit selection of an occupied living character: transfer that character to the selecting player and move the displaced player to the outgoing/reserve role. P1 retains camera input while in reserve.

Commit the shared identity, increment role generation, retire old menu/target state, refresh actors/catalog identities and invalidate character-dependent presentation in the same transaction. A movement-only override leaves menus and HP colors attached to the old owner. Distinguish field KO from a town's forced native actor; a dead battle record must not immobilize the native town avatar. Preserve held Flee across an ordinary valid character swap without leaking other held menu edges.

---

[← Previous chapter](02-moving-a-berserk-party-leader.md) · [Chapter index](../README.md#chapters) · [Next chapter →](04-independent-menus-with-native-command-execution.md)
