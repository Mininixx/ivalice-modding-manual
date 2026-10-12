# Ivalice Modding Manual

Practical implementation instructions for **FINAL FANTASY XII: The Zodiac Age (PC)**, for mod developers and AI coding assistants.

This manual brings together the native engine interfaces, data layouts and implementation patterns used in **Ivalice Together** and **Ivalice Reforged**. It explains how to connect player input, character ownership, combat commands, effects, UI and persistent data while preserving the game's native behavior.

Updated: 12 October 2026. All 31 chapters are included below.

## What you will find

| Area | Topics |
| --- | --- |
| Co-op and input | Independent movement and menus, native Berserk movement, XInput/SDL routing, keyboard ownership, guests and reserve players |
| Camera and presentation | Shared camera, area transitions, Party/Pause suspension, target circles, action lines and in-game HUD rendering |
| Combat and abilities | Action/effect allocation, native command queues, resource payment, damage and buffs |
| Saves and progression | Versioned save extensions, inventory bounds, license ownership, LP costs, board regions and class-specific icons |
| Effects and assets | FFX effect extraction, particle programs, native scene submission, weapon attachments, impact timing, audio and materials |
| Implementation | Address relocation, hook ownership, frozen runtime modules, dependency contracts and handoffs between developers or AI assistants |

## Where to start

- **Adding or changing an ability:** [Adding actions without breaking existing commands](#11-adding-actions-without-breaking-existing-commands).
- **Working on co-op controls:** [Binding controllers to live actor identities](#03-binding-controllers-to-live-actor-identities).
- **Working on the camera:** [A shared camera that still respects the scene](#08-a-shared-camera-that-still-respects-the-scene).
- **Changing licenses or progression:** [License boards, prices and purchase previews](#18-license-boards-prices-and-purchase-previews).
- **Importing visual effects:** [Extracting effects from Final Fantasy X](#19-extracting-effects-from-final-fantasy-x).
- **Writing a native hook:** Read [Native addresses and hook ownership](#30-native-addresses-and-hook-ownership) first.

## Using the manual with an AI assistant

Give the assistant the relevant chapter together with the current source files, target variant and intended behavior. The [implementation brief](#31-preparing-an-implementation-handoff) provides a compact structure for that request.

When implementing a change:

- Start from the current authenticated installation or release. Older prototypes and loose source files may differ from the code inside a frozen runtime.
- Match the executable, address convention, instruction bytes and existing hook owner before applying an offset.
- Keep player, character, actor, generation and scene identities distinct. Define who owns each operation and when that ownership ends.
- Preserve allocated IDs, save layouts, native execution rules and dependency contracts.
- Keep standalone **Ivalice Together** and **Ivalice Reforged** separate. Reforged class, license and custom inventory mechanics belong to the integrated variant.

Addresses and private allocations describe specific implementations. Read them with their surrounding contract; they are not universal constants for every game build or mod setup.

XII addresses use preferred image base `0x120000` unless explicitly identified as RVA. Resolve the runtime base and authenticate instruction bytes and hook ownership.

<details>
<summary><strong>Full chapter index — 31 chapters</strong></summary>

### Control and presentation

1. [Moving additional party members](#01-moving-additional-party-members)
2. [Moving a Berserk party leader](#02-moving-a-berserk-party-leader)
3. [Binding controllers to live actor identities](#03-binding-controllers-to-live-actor-identities)
4. [Independent menus with native command execution](#04-independent-menus-with-native-command-execution)
5. [Multiple native target circles](#05-multiple-native-target-circles)
6. [Independent area-of-effect circles](#06-independent-area-of-effect-circles)
7. [Target arrows and action lines](#07-target-arrows-and-action-lines)
8. [A shared camera that still respects the scene](#08-a-shared-camera-that-still-respects-the-scene)
9. [Rendering HUDs inside the game](#09-rendering-huds-inside-the-game)
10. [Area changes, interaction and state retirement](#10-area-changes-interaction-and-state-retirement)

### Combat and content

11. [Adding actions without breaking existing commands](#11-adding-actions-without-breaking-existing-commands)
12. [Queueing commands on the game thread](#12-queueing-commands-on-the-game-thread)
13. [Damage, status results and enemy reaction](#13-damage-status-results-and-enemy-reaction)
14. [Implementing Breaks and bounded debuffs](#14-implementing-breaks-and-bounded-debuffs)
15. [Persistent buffs, halos and automatic revival](#15-persistent-buffs-halos-and-automatic-revival)
16. [Replacing status icons without square borders](#16-replacing-status-icons-without-square-borders)
17. [Saving new resources inside each save](#17-saving-new-resources-inside-each-save)
18. [License boards, prices and purchase previews](#18-license-boards-prices-and-purchase-previews)
19. [Extracting effects from Final Fantasy X](#19-extracting-effects-from-final-fantasy-x)
20. [Sharing Ghidra types and exporting definitions](#20-sharing-ghidra-types-and-exporting-definitions)
21. [Recovering particle programs and their timeline](#21-recovering-particle-programs-and-their-timeline)
22. [Getting imported effects into the native scene](#22-getting-imported-effects-into-the-native-scene)
23. [Placing and scaling effects on real actors](#23-placing-and-scaling-effects-on-real-actors)
24. [Building blade-aligned projectiles with one impact](#24-building-blade-aligned-projectiles-with-one-impact)
25. [Resolving sound events to the correct audio stream](#25-resolving-sound-events-to-the-correct-audio-stream)
26. [Making added sounds follow the game’s SFX volume](#26-making-added-sounds-follow-the-games-sfx-volume)
27. [Creating convincing weapon surfaces without changing geometry](#27-creating-convincing-weapon-surfaces-without-changing-geometry)
28. [Coloring obtained equipment and preserving enemy suffixes](#28-coloring-obtained-equipment-and-preserving-enemy-suffixes)
29. [Auditing encounter identity, threat and reward placement](#29-auditing-encounter-identity-threat-and-reward-placement)

### Implementation and handoff

30. [Native addresses and hook ownership](#30-native-addresses-and-hook-ownership)
31. [Preparing an implementation handoff](#31-preparing-an-implementation-handoff)

</details>

---

## 01. Moving additional party members

Give each player steering ownership while retaining the game’s movement machinery.

### The working boundary
The useful interception point is the movement consumer, not the character’s final world position. For this executable build, the detour begins at **VA `0x2E4380`**. Its context exposes the actor through `context+0x30` and the physics payload through `context+0xB8`. The generated cave accepts only the owned P2/P3 actor and the eligible native mode (`r8d == 0`). All other actors continue through the displaced native prologue.

| Physics field | Type | Published value |
| --- | --- | --- |
| `+0xA4` | float | Heading in radians |
| `+0xD0` | float | Movement magnitude |
| `+0xA0` | float | Pitch, cleared by this steering path |

This feeds the existing movement pipeline. Repeatedly teleporting world coordinates would bypass the contract being used here and is not how this implementation works.

### Construct a steering command
Project the stick onto the camera’s horizontal forward/right basis. Normalize input strength through the native stick-response policy, then choose walk/run magnitude. The sign and axis convention below comes from `player_steering`:

```python
# Pseudocode: the basis and actor were authenticated earlier.
world_x = forward_input * forward.x + right_input * right.x
world_z = forward_input * forward.z + right_input * right.z
heading = atan2(world_x, world_z)
strength = min(1.0, hypot(forward_input, right_input))
magnitude = run_or_walk_step * native_stick_fraction(strength)
```

Publish to separate per-player command blocks. Reject a zero actor before comparing pointers. Preserve scratch registers, replay displaced instructions and validate every branch destination in the emitted machine code.

### Movement is only one owner
Follower AI can still turn or approach a target. The implementation has separate facing hooks (`0x236328`, visual-facing call `0x236323`) and an action-approach gate (`0x325E07`). Scope these to the controlled follower. Do not disable native follower lists globally or seize the ordinary leader. Keep the P1 Berserk permission gate separate from follower steering.

## 02. Moving a Berserk party leader

Separate locomotion ownership from status effects and command eligibility.

### Let native input calculate movement
Use the native status-classification boundary at **preferred VA `0x23B166`**, inside `0x23B040`. This is an instruction site, not a callable function and not an RVA. With image base `0x120000`, its RVA is `0x11B166`. Match the five original bytes `25 3B 40 00 88` before installing the detour; return to `0x23B16B`.

At this boundary, `RDI` is the native leader actor and `EAX` and `EDX` contain the combined status. `actor+0x698` points to battle KEEP; combine permanent status at `KEEP+0x3C` with temporary status at `KEEP+0x64`. Berserk is bit 27.

For the authenticated P1 owner only, execute `AND EAX,0x8000403B` instead of `AND EAX,0x8800403B`. For every other actor or inactive publication, replay the original AND. Preserve the flags from that final AND for the following `CMOVE`; comparisons against the ownership record must occur before it. Preserve scratch registers, stack balance and the full displaced instruction.

The native consumer then retains responsibility for keyboard/gamepad input, movement magnitude and turning. Do not calculate P1 heading in the external worker or force physics direction each update. Keep P2/P3 steering separate.

### Publish permission and identity only
Use `build_berserk_native_movement_gate`, `install_berserk_native_movement_gate` and the current `write_p1_berserk_command` implementation in the authenticated frozen runtime. The extension-owned P1 state reserves `0x40` bytes: actor at `+0x08`, physics at `+0x10`, legacy active at `+0x18`, native permission at `+0x3C`. Resolve its base from the installed layout; these are not native actor fields.

Revoke native permission before changing identity, keep legacy active at zero, publish valid actor/physics, and arm native permission last. Revoke on status loss, owner change, KO, loading, modal UI or invalid identity. The retired vector helper must return `CLC; RET`, allowing its caller to continue through the native route. Do not restore the old heading/magnitude/facing publications.

The native gate checks permission, compares the published actor against `RDI`, and rechecks permission. Treat this as the existing ownership protocol, not as a general atomic snapshot guarantee. A change to publication synchronization also requires a matching consumer and a new runtime layout identity.

### Preserve status and action restrictions
Leave `EDX`, both KEEP status banks and the second mask at **`0x23B173`** unchanged. That second instruction applies `AND EDX,0x8800003B` for native action availability. Removing Berserk from the movement mask must not clear the status, remove its combat effects or silently enable every action. All other bits in the movement mask retain their native restrictions.

The separate manual-command policy at `0x311D72` may change `F7 C1 3B 20 00 88` to `F7 C1 3B 20 00 80`. Preserve its existing scope and any Reforged Blood Berserk rules; do not use it as the movement fix. Register the new movement hook in process-lifetime ownership and layout metadata. A process with an older incompatible layout requires a clean restart instead of live topology conversion.

## 03. Binding controllers to live actor identities

Keep device, player, party member, actor and visual object identities distinct.

### Keep the ownership chain explicit
| Identity | Responsibility |
| --- | --- |
| Physical device | Samples, backend, connection and reconnect policy |
| Player slot | Menu state, palette and input routing |
| Persistent party member | Character-specific data |
| Live actor handle and generation | Current world entity |
| Model and physics object | Current rendering and movement representation |

Resolve these identities from the same coherent session snapshot. Party order is not player ownership, an actor address can be reused, and a handle is not a model-array index. Battle layouts begin at `+0x5A48`, stride `0x12`; read the native leader separately at `+0x5AA4`. Choose the intended current/UI/menu layout explicitly.

### Isolate XInput, SDL and the desktop owner
Sample each assigned device once per update. Normalize buttons and axes through its actual backend; a device shown by SDL need not expose an XInput slot. Deduplicate a physical pad represented by both backends rather than assigning the same input to two players. A missing P2/P3 device must not fall back to P1.

Assign keyboard and mouse to a single player. With desktop owner P1, retain native movement, camera and native game bindings. With desktop owner P2/P3, filter native desktop gameplay input so it cannot also operate P1. Keep permitted native frontends usable under their own input ownership.

For P1's replacement menu, read the game's `keymap.ini` and native key conversion table. In the keyboard mapping, `Circle` means Confirm and `Cross` means Cancel. `DecideButton` selects the physical gamepad face button; applying it to keyboard semantics can reverse Space/Enter and Backspace. Do not synthesize keys or rewrite the user's profile to compensate.

If a controller appears in the launcher but not in the game, inspect native input ownership and Steam Input before changing SDL/XInput code. For this runtime, disable Steam Input for FFXII and **restart the game** before reassessing device routing. Launcher detection alone does not establish which input reaches the native consumer.

### Admit frontend navigation before a field actor exists
Title and Load Game menus must retain native D-pad navigation while the co-op field session initializes. Do not claim custom directional ownership merely because the mod is enabled. Set the field-navigation latch only after gameplay readiness, a coherent world signature and a materialized active party are present. Do not use a startup timeout to release those directions.

### Transfer the complete role after KO or selection
Use one shared role identity for movement, commands, selectors, target indicators, HP palette and menu presentation. On KO, choose only a living, command-eligible, active party actor that is not owned by another enabled player. Include eligible guests. Re-read the session before committing; Stop, Stone, a disappearing actor or an incompatible execution state must not become a destination merely because HP is positive.

If no free actor exists, keep the player in reserve and block their gameplay input from reaching another player's native leader. Keep Party, Pause and Character Select available under the appropriate frontend policy. Permit an explicit selection of an occupied living character: transfer that character to the selecting player and move the displaced player to the outgoing/reserve role. P1 retains camera input while in reserve.

Commit the shared identity, increment role generation, retire old menu/target state, refresh actors/catalog identities and invalidate character-dependent presentation in the same transaction. A movement-only override leaves menus and HP colors attached to the old owner. Distinguish field KO from a town's forced native actor; a dead battle record must not immobilize the native town avatar. Preserve held Flee across an ordinary valid character swap without leaking other held menu edges.

## 04. Independent menus with native command execution

Render a separate frontend without replacing the game’s rules for an action.

### Keep the frontend and executor separate
Independent menus need their own cursor, page, selected command and selected target. They should still query native availability, inventory, targeting restrictions and action data. The architecture separates a menu model/presenter from command submission and publishes a coherent native catalog snapshot.

A label is not an action ID. Action data can refer to a separate string-table index. Do not derive executable command IDs from menu positions or assume an action table and name table have equal lengths.

### Confirmation is a transaction
Carry the submitting member, action, full target handle and session identity from selection to confirmation. Revalidate them at submission. A target list can become stale while the player is reading it. Releasing a menu must also release its input capture and any native wait-mode bridge it owns.

For the native leader, mirror the native menu state instead of having two unrelated systems each believe they own P1. Native dialogs, story interactions and battle menus need explicit precedence.

### Authenticate identities when painting target information
The target-info panel's Libra query depends on `companion_identities`. Include that authenticated identity API in the installed frozen module and support the no-Libra branch as well as the ordinary party-member branch. Target information and command admission should both use the same validated actor identities.

### Keep player selectors independent
Maintain a separate Character Select owner for P1, P2 and P3. One player's selector must not block another player's opening, and selecting a free character must work from every enabled player slot. Apply ownership changes through the shared role transaction described in the input chapter.

### Respect interaction precedence and menu lifecycle
An actionable native use prompt takes precedence over opening a battle menu on the same Confirm edge. Opening or closing a custom selector must not briefly revoke movement for unrelated players. Distinguish the custom wait bridge from a real Party/Pause frontend, and retire only the input/menu leases owned by the closing UI.

### Keep layout and localization in the same path
Resolve user-facing labels from the selected language throughout the launcher, including secondary explanatory panels. Measure available column width after localization and scaling; wrap or clip within the owning panel instead of placing text over the next column. Keep actions keyed by IDs rather than translated labels. A game's language choice must not change controller assignment or the meaning of Confirm/Cancel.

## 05. Multiple native target circles

Give each selection its own native node and protect the manager’s temporary state.

### Capacity and ownership are separate requirements
The native capacity check at **VA `0x291959`** compares against two. For three-player capacity, change `83 F8 02` to `83 F8 03`, after matching the original bytes. This is only the capacity gate: it does not create three independently owned selections by itself.

The target UI manager is reached through **VA `0x209BE80`**. The implementation calls native retargeting at `0x2917E0` through a dispatcher on the UI tick (`0x28E480`, original callee `0x290CF0`). This ensures the object operation occurs at the expected game-thread boundary.

### The retarget transaction
1. Authenticate the manager, target and owned circle node.
2. Save manager head/current pointers at `+0x10F00` and `+0x10EF0`.
3. Temporarily point those fields at the circle being retargeted.
4. Call the native retarget routine with the requested target and variant.
5. Restore the manager pointers and inspect the resulting node identity.

Creation additionally protects existing nodes while native code chooses/reuses a slot. Preserve that logic rather than repeatedly invoking a singleton factory and assuming it allocates a new object each time.

The publication check matches **both target and palette**. A correct target with another player’s palette is still a wrong publication. On shutdown restore only the patch and nodes that this controller still owns.

**Failure to avoid:** two players selecting the same enemy and stealing each other’s circle; a new target being published over P1’s native node; stale node reuse after a map change. A capacity patch alone will not prevent these failures.

## 06. Independent area-of-effect circles

Area previews use another native object family and another list.

### Do not reuse the single-target-circle contract
The area controller uses the factory at **VA `0x2911D0`**, list append at `0x3F34D0`, and manager list field `+0x10F40`. Its owned objects carry distinct player tags (`AOP1`, `AOP2`, `AOP3`). Radius is supplied to the area factory; it is not inferred from the on-screen diameter of a single-target marker.

Native creation is dispatched on the UI thread. The dispatcher temporarily isolates the list, creates the requested object, restores the existing list and appends the owned object through the native operation. Preserve failure cleanup as carefully as the success path.

### Borrow settings without losing the user’s settings
Area rendering is controlled by bit 22 in the settings flags at `[0x215E6E0]+4`. The controller remembers whether that bit was already enabled. On release it removes only the enablement it introduced, retaining unrelated flags. If the settings object changes, release the old ownership before acquiring the new object.

## 07. Target arrows and action lines

One visual family can have several render paths; identify each owner at its own call site.

### Two render sites, one ownership table
The action arrow and the target line use separate paths. The palette hooks are **VA `0x3F719C`** for the arrow and **VA `0x3F54D2`** for the target line. Both read a published table of up to three `(handle, palette)` pairs.

The arrow path identifies its source through `[rsi+0x2D0]`; the target-line path uses `[r15+0x810]` at its own hook site. These are context-specific structures, not interchangeable actor offsets. Preserve the displaced instructions and change the palette only for a matching owned handle.

This keeps native geometry, depth, animation and fade. The arrow hook also preserves a native special palette case (`4`) instead of blindly recolouring every draw. Recolouring one path does not guarantee the other will match.

### Distinguish target selection from action execution
A menu’s current target, a queued action’s target, a world arrow and a party-portrait cursor are related but not identical. An executing action may keep its native target while the next menu is selecting another. Give each presentation an explicit source of truth and lifetime.

## 08. A shared camera that still respects the scene

Use formation-aware focus while keeping collision and native camera ownership explicit.

### Derive focus from the current formation
Use valid controlled actors to compute group centre, horizontal separation, bounded vertical separation and filtered velocity. Keep separate settling times for focus, zoom-out and zoom-in. Bound sample speed and age; a teleport must not become a velocity spike. Keep P1 camera input independent of P1's alive/reserve state.

Limit camera-height obstruction filtering to a bounded corridor between the controlled actors. Retain floors, ceilings and geometry outside that corridor. Preserve native wall pressure, hysteresis and recovery; release control for scripted scene cameras.

### Keep a committed camera through the outgoing area
Use the native current area, pending destination and coherent world signature together. Current/UI location slots update separately while unloading; their temporary disagreement must stop new admission without instantly revoking an already committed outgoing camera.

In `camera_area_admission`, freeze the last complete admitted output while the source area is still leaving. Keep renderer ownership and suspend camera integration. Use the bounded hold lease (500,000 microseconds in the current protocol); a dead worker must not hold the scene forever. Do not keep dereferencing retired actors to maintain that image.

For the new area, revoke old collision corridors, resolve fresh actor identities and positions, seed the new goal, and publish a new admission generation. A renderer goal ACK is insufficient: require a subsequent active output commit before enabling the new camera consumers. Revalidate world/owner identity at that final enable boundary. Do not restore a prior-area camera cache into the new scene.

### Suspend calculation during Party and Pause
Treat a modal menu in the same world as suspension, not camera destruction. Keep orbit, focus, zoom and collision history; stop position integration, velocity updates and elapsed game-time accumulation while the menu is open. The renderer may keep presenting the last committed frame and renewing the bounded hold.

On close, confirm area and world identity. Resume from preserved camera state; clear stale present timestamps and velocity samples so the pause duration cannot cause a jump. Use `camera_reset_for_ownership` to avoid calling `controller.reset()` for a same-world menu handoff. Reset/reseed normally for an actual area/save change or invalid identity. A broad reset on every ownership transition causes the visible camera snap when leaving menus.

## 09. Rendering HUDs inside the game

Publish coherent panel pixels, composite them in D3D11 and preserve the caller’s graphics state.

### The panel transport
Read the panel capacity from the active producer/renderer protocol. A 16-slot co-op layout uses a 128-byte shared header, a 64-byte header per slot and `1024 × 768 × 4` reserved bytes per slot; the extended content layout uses 22 slots. Match the installed layout exactly instead of mixing constants from the two variants.

Publish dimensions, logical coordinates, visibility, generation and pixel content coherently. Keep publisher/renderer heartbeats and acknowledgements. Reusing a texture when only its position changes is cheaper than uploading unchanged pixels every update. Reject oversized payloads and stale or partial publications.

### Match alpha representation to the blend state
The panel path converts straight RGBA into **premultiplied BGRA**. RGB is multiplied by the final alpha, including opacity. The corresponding blend uses `ONE / INV_SRC_ALPHA`. Multiplying RGB twice darkens edges; feeding straight RGB into this path creates fringes.

```text
premultiplied_rgb = straight_rgb * alpha
out_rgb = source_premultiplied_rgb + destination_rgb * (1 - alpha)
```

Do not globally replace every blend state with this one: other native primitives and imported particle materials can have different alpha contracts.

### Presentation and capture
Draw panels through the renderer loaded in the game and keep added audio in its in-process mixer. Do not restore an external layered-window fallback. Preserve transport recovery and the capture boundary of the actual renderer/audio consumer.

Preserve the D3D11 state you change—render targets, depth/stencil, blend, shaders, buffers, textures, samplers, viewports and scissors. Handle hidden panels, transparent corners, overlap, resize, ultrawide viewports and transport loss without leaking graphics state.

## 10. Area changes, interaction and state retirement

Treat a transition as a change of ownership, not merely a new map number.

### Observe several signals
The session layer reads battle, location, party layouts, user-control readiness, native menu ownership and modal state. The location structure has two area fields (`+0x1244`, `+0x125C`); they can disagree while a transition is in progress. A non-null actor pointer alone is insufficient permission to keep controlling it.

The area-transition source distinguishes the current area-slot table, pending area and a transition request containing destination, spawn and previous area. Preserve destination/spawn semantics. Sending every player to a guessed coordinate is not a substitute for a valid native route.

### Retire before reacquiring
1. Revoke active movement and command publications.
2. Hide or retire owned targets, circles and transient panels.
3. Cancel resource leases and audio tied to the old scene.
4. Wait for a coherent new session and resolve fresh actor identities.
5. Reacquire only the control and presentation that the new scene permits.

Interactions also need an owner: a follower’s proximity, use prompt and activation source must describe the same actor. Native dialogs and story events should remain native and should supersede ordinary battle UI. Keep rollback for partially acquired interaction state.

### Prefer an actionable chest/NPC prompt
In `private_player_interaction`, ignore zero handles and stale aggregate publications. Search all candidate slots for a usable `state >= 2` before falling back to a proximity-only state. A high-index outer/proximity entry must not hide a lower-index usable chest.

In `_world_interactions`, consult `native_interaction_router.prompt_interaction(player)` when the aggregate is absent **or not actionable**. Prefer an exact actionable descriptor for that player, with current handle and can-use status. Route Confirm to that native interaction before the battle-menu fallback. Keep native dialogue ownership and partial-acquisition cleanup intact.

### Keep facing behavior separate
Do not reintroduce delayed facing corrections on area entry or character selection. Preserve the current native orientation behavior unless orientation work is explicitly requested. A post-load rotation write can produce a visible wrong-to-correct turn even when its final angle is correct.

## 11. Adding actions without breaking existing commands

An action record, a visible menu entry and an executable skill are separate deliverables.

### Begin with the authenticated installed content
Start from the current installed Lua, native DLLs, frozen menu modules and Battle Pack, then create staging. Historical foundation generators and loose Python trees may omit later composed changes. Do not rebuild over the current installation from an old prototype or retail baseline.

The Battle Pack has 71 sections: Actions in section 14, equipment in section 13 and English text groups in section 61. `Action+0x34` is a name reference, not necessarily the Action ID. Keep the loaded pack and the menu's mirrored pack identical.

### Allocate through the registry and lock
Read `IvaliceReforged/foundation/SKILL_RELEASE_WORKFLOW.md`, `content/ability_registry.json` and `content/ability_allocation_lock.json`. Preserve existing IDs, including retired records and deliberate shared owners. Never compact IDs or regenerate the allocation lock merely to accept a conflicting change.

| Reservation / boundary | Rule |
| --- | --- |
| Actions `111–114`, effects `504–507` | Dynamic Mix leases; never permanent skill slots |
| Effects `723/724` | Reserved even without a direct Action-table consumer |
| Menu IDs `>=0xFF00` | Selectors/sentinels, not ordinary executable Actions |
| Effects above `511` | Require their own routing, metadata and initialization |
| Action table | Read its current extent; 8,048 records in the 11 October layout |

Request a read-only allocation proposal with `python -m IvaliceReforged.foundation.ability_plan <staging> --actions 3 --effects 1`. A proposed ID is not proof of executable capacity. Extend every affected consumer bound, including the native execution checks and `irfj_mix_prepare`, plus category buffers and save/ownership ranges where applicable. There is no universal 511 limit; never globally replace 511/512.

### Preserve the native execution contract
| Field or boundary | Rule |
| --- | --- |
| `Action+0x1E` | Native category; 2 is Technick in this path |
| `Action+0x09` | Action charge field |
| `Action+0x0C`, bit 27 | Selects weapon charge from `Weapon+0x27` |
| `Action+0x24` | Physical Attack clones retain signed `-1` |
| `Action+0x26` | Keep the physical clone's native value; zero in this contract |
| Admission | Resolve class, actual ownership, MP/resource, target and execution state |

For physical techniques, retain the normal weapon-hit route at `0x325260`; a positive visual EFX in the physical contract can suppress that hit. Attach a separate visual-only carrier when needed. For Skullbreaker, calculate the 100% base through native Attack (Action 150) with the **currently equipped weapon**, then apply the skill multiplier. Do not substitute a fixed magic/base-power formula.

### Use canonical class identity
Canonical classes are 0 Mystic, 1 Rift Assassin, 2 Gambler, 3 Skullbreaker, 4 Templar, 5 Transmuter, 6 Beastlord, 7 Renegade and 8 Arcanist. Saved IDs 9/10/11 alias 0/1/2. Use `foundation/license_ownership.py` and native `irid_matches`; sparse saves use the assigned primary class. A stale secondary or visible class byte must not grant an ability.

### Compose the complete dependency chain
Register Action/effect, menu, license, admission, payment, calculation, application and cleanup together. Declare intentional sharing. An existing Action change needs its ID, before/after record hashes and reason in `skill_release_contract.json/reviewed_action_changes`.

Preserve one pending manual order per member in `irfq`. Retain readiness and initialization guards. When changing Lua, update the blackhole authentication dependency, then blackhole-visual; preserve their code and guards. A shader change requires the matching FFX compiler/hash chain. Embedded assembly comments must not contain a literal `%`, which the Lua loader can interpret as a placeholder delimiter.

Update all affected dependency records and the exact-candidate native validation artifact required by the release workflow. Run `python -m IvaliceReforged.foundation.ability_registry <staging>` before installation; resolve failures at their source rather than copying stale approval fields or weakening guards. Install with the game closed, authenticated preimages and a rollback copy.

## 12. Queueing commands on the game thread

Read real consumer occupancy and preserve the intended replacement semantics.

### One pending manual order per member
The implemented native queue (`irfq`) keeps one pending manual request for each member. A newer request replaces that member’s pending request. This is an explicit semantic choice; it is not a ring that guarantees an execution for every button press.

Delivery observes the actor’s current action, command mailbox and published resource-consumer mailbox. Do not guess completion from a timer in the external frontend. A prefetched resource remains owned until the game acknowledges the lease’s cleanup, not merely until a host function returns.

### Distinguish queued admission from execution readiness
Native validation at `0x317BC0` calls `0x2FFCF0`. During wait-mode pause (`0x253B90`), the inner validator returns reason **`0x24`** and the outer state is **1**, rather than execution-ready state 3.

Accept only that particular “paused, wait” combination into the queue. The game still waits for pause to clear and repeats full native validation before execution. It does not broadly treat every rejection as permission.

### Payment must survive validation
Use an authenticated paid receipt tied to owner, target, generation and area so spending the final charge cannot invalidate the same paid order later. A paid order may execute; another order still needs its own charge.

```text
selected → admitted → waiting for native consumer → delivered → completed
                   ↘ replaced / invalidated / cancelled
```

Validate payment at the actual charging boundary. Do not debit again at impact, and do not let an old receipt authorize another action. Retire the receipt on replacement, cancellation, death, actor recycling or scene/save invalidation.

### Preserve Mix and stealing receipts
Mix owns dynamic Action/effect leases; retain their admission, ingredient payment, cancel/refund and result cleanup. Keep recipe construction out of menu-label logic. Transmuter's charge policy uses its class-local fractional accumulation; the 30 percent gain increase uses numerator 130 with denominator 16, without changing other classes.

Pockets is a Transmuter-specific interpretation of shared Action 169. Preserve ordinary Steal for other owners. On the first valid Pockets use against an eligible enemy, guarantee one available item from its native steal table (blue) plus two rewards from the Mega Pockets pool (yellow). If ordinary Steal already exhausted the native table, award only the two extras. A repeated Pockets use on that enemy fails.

Tie the Pockets receipt to the enemy's live identity, generation and scene, shared across players; retire it with that enemy lifecycle. Do not mistake a recycled pointer for an already robbed enemy. Preserve the action's reserved cast bit 16. Mega Pockets remains independent: always ten item units even after previous steals, with at most five distinct item types. Aggregate repeated rewards rather than letting ten different labels overflow the screen.

## 13. Damage, status results and enemy reaction

A hit can change HP while silently losing the reaction that should follow it.

### Work at the native RESULT boundary
The physical-impact implementation preserves a complete RESULT before chaining the prior applicator. At this result boundary, result kind at `+4 == 0` and flag `+0x2C & 0x100` identify the successful physical-result case. Misses and blocks should not produce the same status/impact treatment as damage-bearing hits.

For added Blind, Silence and Sleep, private calculator records use native routines `0x385F60` and `0x387CB0`. Merge only the accepted status bit and its counters into the weapon RESULT. Preserve unrelated HP/MP fields, status fields and global scratch state. A newly applied Sleep must not be removed by the very hit that applied it.

### Trace reaction after the applicator
Follow both the retail applicator (`0x3112F0`) and subsequent enmity/AI feedback. Preserve reaction ownership when wrapping the applicator; an early `xor eax,eax; ret` after damage can suppress a later stage.

Authenticate these post-hit boundaries: save epoch mismatch; null battle; changed battle; null location; changed location; location area at `+0x1244` mismatch; location UI area at `+0x125C` mismatch. Do not remove these guards globally; make result delivery and reaction use the same current identity.

Read the child-hit record using stride `0x50`, a DWORD count and up to 16 **4-byte full handles**, indexed from 1. Do not widen those handles based on a stale comment.

### Keep class damage and utility scaling separate
For Skullbreaker, define 100 percent base damage as the native basic Attack result using the equipped weapon, then apply that skill's modifiers. Preserve the native damage family, defense and accepted-hit semantics.

For Transmuter, apply the damage-only `irmd_offense` bonus at native Mix admission and freeze it in the accepted recipe. Only category `0x10` uses this offense helper. Require canonical primary class 5 and actual ownership of Alchemical Craft 169 plus each contributing license; preserve live admission registers, including R10/R11. Keep healing, revival, status duration, ingredient use and cleanup on their own paths.

Use the current license-driven progression: core 169 adds 20 percent; nodes 735/736/745/746 add 25 each, 747/753/754 add 20 each, 734/762/763/1160/1161 add 14 each, and 1174/1175/1176/1177 add 30 each. These are additive offensive bonuses, not a replacement for existing buff potency. Do not reactivate the retired offense immediates alongside the helper; that would count bonuses twice. Keep native help and both custom-node catalogs synchronized with future changes.

## 14. Implementing Breaks and bounded debuffs

Represent combat modifiers by owner, damage family and lifetime instead of destructive stat edits.

### Four independent modifiers
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

### Count actions, not result callbacks
A separate weakening skill halves the target’s next two damage-dealing attacks. One area action may emit several target RESULTS; consuming one charge for each result would make its duration depend on target count. Track the offensive action identity and spend the debuff charge once for that action. Healing does not consume it.

## 15. Persistent buffs, halos and automatic revival

Bind state to the character, visuals to the current model and timing to the game clock.

### Grant at the effect birth boundary
For Auto-Life, use PAGE birth: `0x46EFD0` reaches the complete call at `0x46F0AF` to `0x3B8670`. A listener on PAGE update (`0x4FF2FE`) that requires tick zero can miss birth entirely.

Intercept the complete birth call, authenticate private EFX, generation, caster and ally, then grant once. Preserve the original native call for every effect. Keep cast creation, buff publication, presentation and consumption as separate stages.

### Keep the actual halo component
Use the golden halo component: **TBP 14608**, texture index 2, mesh 33, behaviour 2, programs 1/2. It begins at sampled frame 41 (native tick 82), and is fully formed at frame 66 (tick 132). Holding that assembled phase preserves the original trails and sprites instead of repeatedly restarting the entire cast.

The persistent visual follows `j_kao` (selector `0x1000`) above the live head, with an offset based on native radius. Its age belongs to the buff record, not a renewable EFX slot. Recreating the visual carrier must not restart formation. Keep the persistent halo silent; the cast owns the cast sound.

### Revival placement must precede the intended visual
The automatic buff consumes once after ordinary KO and waits one game-second before native revival. For manual Phoenix Down, prepare the native resurrection destination through `0x311F70` before the visual effect and retain the engine’s “position already prepared” marker. Do not revive early or reposition arbitrary living actors.

For independently expiring stack buffs, store one expiry per accepted cast. The custom Luck policy is +3 for 20 game-seconds per cast; a recast adds a new expiry instead of resetting the first one. Pause and save/scene transitions must follow an explicit lifecycle policy.

## 16. Replacing status icons without square borders

Edit the native draw descriptor and account for the texture samples around the visible artwork.

### Replace the intended cell
Drawing a new icon beside a native status icon produces two competing layouts. The working replacement wraps the native descriptor, selecting a private frame while the custom buff is active and restoring the normal descriptor after consumption. A priority policy decides which icon occupies that same cell when several custom/native statuses coexist.

One implemented halo icon uses section 5 of `tex2pack_ys.bin`, private frame 89, palette 59 and a `(64,800,52,64)` rectangle. Those are allocated project slots; re-audit availability before adopting them in another implementation.

### The visible square can originate outside the artwork
Account for fractional sampling outside the visible frame. For the private Fire weakness icon, use the isolated `y=704` frame instead of `y=640`, which reaches the adjacent Slow row through the Fire palette. Centre transparency alone cannot prevent that neighbor contamination.

Keep alpha-zero padding large enough for the native UVs and filtering. Resize artwork with an alpha-aware/premultiplied method, then deliver it in the representation the native atlas expects. Do not transplant the HUD panel blend contract into the atlas blindly.

## 17. Saving new resources inside each save

Serialize stable game data and validate it before accepting a custom trailer.

### Preserve the native save and the current schema
Keep the native 353,936-byte image intact and append one versioned extension with magic `IRFWI001`. Read the schema and lengths from the current reader/writer contract; do not rebuild current saves using the older v3 592-byte trailer. The schema-7 layout uses a 2,560-byte extension, giving a 356,496-byte decoded image. These are decoded payload sizes, not an instruction to overwrite the encrypted file directly.

Use the same version, length, counts and checksum definitions in preparation, serialization and import. The native image and custom payload have separate FNV-1a checks. Reject malformed sizes, invalid fractions and incompatible records before publication. Keep supported legacy readers while writing the current schema.

Store stable inventory/member/resource data, including fractional charge progress. Do not serialize actor pointers, effect leases, pending orders or process-local timers. Bound every record before reading it, and import class/resource state only after native load completion and coherent identity.

### Keep inventory extents consistent with save preparation
The “at least 100 KB” save message can be reached when custom serialization fails, even if disk space is available. Inspect the preparation result and the equipment-bank guards before assuming a storage problem. `irfw_touch`, `irfbh_touch` and `irfcu_touch` must agree with the actual equipment table extent; the current bank has **1,137 records**, not 1,136. When changing content, derive the new count from the pack and synchronize all consumers and restoration code.

Abort a failed preparation before flushing a partial native stream. Preserve loader callback chaining in ordinary and offset-read paths. On overwrite, replace the extension rather than appending another copy. Keep resource import distinct from transient-state retirement so a new save epoch cannot erase the bars imported from that accepted load.

### Keep player saves outside development mutations
Stage changes to the runtime and schema, preserve rollback preimages and respect the user's authorization before operating on saves. Update native DLL authentication when the Lua save code changes. Never bypass a failed initialization/readiness guard to make a save operation appear available.

## 18. License boards, prices and purchase previews

Use one authoritative cost view and migrate before granting or purchasing nodes.

### Give each board one authoritative view
Selection, preview, preflight, LP debit and description must use the same board-aware cost view (`irlay_cost_view`). Ownership takes precedence over affordability: an owned license remains owned even at zero LP. The mini-board path at `0x55F96F` calls `0x323600` with flags 0; the open board uses flags 1, so both routes need the ownership policy.

Keep class-specific names, help, icons and equipment grants keyed by class and license. A shared native string or license ID must not silently replace the presentation/effect on another class. Use the assigned primary class for D205 ownership and icon lookup, including aliases 9/10/11.

### Use numeric equipment progression and reachable regions
Name equipment nodes sequentially: Armor 1, Armor 2, Armor 3, and so on. Do not restore Gear A/B labels, free “included” partner nodes or hidden A-before-B equipment requirements. Preserve ordinary board adjacency, explicit level regions and LP payment.

Use the physical `board_phase` region as the source of level/phase metadata. Early-region nodes must not inherit a later level barrier from stale stage metadata. Keep paths reachable from Essentials within the intended region and fit nodes inside the board silhouette. Match icon type and number to the actual grant, not an old title.

The appended paid equipment licenses `1420–1464` retain their IDs, grants and saved ownership. The legacy raw tables remain `9 × 1420`; use the separate bounded appended cost/level tables rather than stretching raw data and invalidating relocations. The class icon map covers `9 × 1465`, with 205 board cells per canonical class in this layout.

Synchronize source/runtime custom-node catalogs, all nine class boards, loaded board binaries, class-qualified native help and icon descriptors. Preserve every supported language atlas. Never infer UI icon correctness from the node name alone.

### Preserve sparse saved ownership
| Battle KEEP field | D205 layout |
| --- | --- |
| `+0x190` | LP, unsigned 32-bit |
| `+0x194` | Sparse ownership-bit region |
| `+0x1BC` | Low five bits for appended ownership |
| `+0x1BE` | Layout marker `0xD205`, 16-bit |
| `+0x1C0` | Receipt `0x70` |
| `+0x1C1` | Marker `0xB6` |
| `+0x1C2` | Level byte |
| `+0x1C3`, `+0x1C4`, `+0x1C5` | Primary, secondary (`255`), visible class |

Use `irfl_has`, `irfl_set` and `irfl_bit_index` instead of treating license ID as a direct bitmap index. A bulk 46-byte zero from `+0x194` overlaps metadata at `+0x1BE` and `+0x1C1`; do not perform it after initializing those markers. Keep native purchase/guard behavior at `0x323910` / `0x323D10` compatible with the mapped layout.

### Apply migrations before purchase
Run a required migration before selection and before automatic grants. Exclude automatically granted licenses from purchase refunds, record migration once and preserve already owned licenses. A new balance bonus on an owned node does not require repurchase or a retroactive LP debit. Preserve intentional skill-upgrade aliases instead of treating every shared owned bit as a blocked-purchase defect.

## 19. Extracting effects from Final Fantasy X

Start with the command table, then collect the effect program, textures and sound dependencies.

### Restrict the source game explicitly
Use the FFX magic modules, `FFX_Data.vbf` and `FFX.exe` together. Keep X-2 separate. The module collection includes more than player spells; do not treat a DLL count as a spell count.

These are x86 effect modules. They call an engine API and depend on the original game's runtime. Loading one into the x64 XII process is not a porting strategy. The useful products are a catalog, recovered behavior, texture/mesh data and audio, followed by an implementation of the required behavior in the destination engine.

### Resolve ability → program IDs
The catalog reader examines the FFX battle kernel tables. Its header has four little-endian 16-bit values at `+8`; records begin at `0x14`. The supported record strides are `0x5C` and `0x60`. A record's first `uint16` points into the string pool after the record payload; the animation IDs are `uint16` values at `+0x10` and `+0x12`.

Use the command's name, menu category and both IDs together. Do not assume the first ID is always a caster effect and the second always a target effect. The white/black-magic menu categories are helpful filters, but would omit techniques, breaks and other requested effects.

| Ability | Effect IDs | Resolved sound IDs |
| --- | --- | --- |
| Slow | 14 | 9029 |
| Demi | 102, 103 | 9021; additional 14069 kept separate |
| Auto-Life | 114, 144 | 9016, 9035 |
| Power Break | 21, 326 | 9046, 9061 |
| Magic Break | 319, 327 | 9047, 9061 |
| Armor Break | 320, 328 | 9048, 9061 |
| Mental Break | 321, 329 | 9049, 9061 |
| Full Break | 699 | 9061, 10099 |
| Dark Attack | 26, 27 | 9064 |
| Silence Attack | 24, 25 | 9063 |
| Sleep Buster | 34, 35 | 9065 |
| Luck | 7 | 9044 |
| NulFrost / NulShock | 136, 137 / 140, 141 | 9023 / 9025 |
| NulTide / NulBlaze | 142, 143 / 138, 139 | 9026 / 9024 |

### Preserve the original inputs
Extract the magic tree, associated shaders and the relevant tables. Hash original bytes and maintain an output manifest. Preserve unsupported big-endian PS3 PHYR/GCM textures as originals; route them through an appropriate decoder instead of treating a missing PNG as missing source content.

Keep the game binaries and extracted proprietary assets local. A reusable knowledge document can distribute schemas, algorithms and small explanatory examples without embedding those assets.

## 20. Sharing Ghidra types and exporting definitions

Separate reusable type definitions, program-specific analysis and recovered runtime behavior.

### Three different kinds of project object
A Ghidra project can contain imported programs, Version Tracking sessions and shared data-type archives. Each program also owns its own data types; creating a structure there does not automatically share it with other DLLs. Use a shared archive for structures and function definitions that really describe a common engine boundary.

Copying a structure into a shared archive brings its constituent types along. Check pointer widths, packing, calling conventions and conflicting names rather than assuming similarly named definitions are compatible. Version Tracking transfers must be reviewed and applied to the intended participating program; a comparison does not make both programs one database.

### Export small, meaningful surfaces
For a function catalog, export selected rows and columns from the Functions view to CSV. For shared types, export a C header from the data-type archive. Record the program fingerprint, image base and whether each address is a VA or RVA alongside it. Exporting an enormous decompilation is rarely the best handoff.

For the FFX `gMagicFunctions` table at **RVA `0x00864CE8`**, keep the 32-bit pointer-table representation separate from function signatures. A 741-pointer prefix occupies `0xB94` bytes; neither a label nor a pointer establishes a callable C prototype.

```c
// A recovered 32-bit address is data until its ABI has been verified.
uint32_t engine_api_entry;
// Do not replace it with a guessed function-pointer signature.
```

For each callback that a port needs, inspect its callers, arguments, stack cleanup, return value, ownership and side effects. Write down which meaning is observed in machine code and which remains an inference. A header helps reuse analysis; it cannot supply the host engine that an effect DLL expects.

## 21. Recovering particle programs and their timeline

Port the animation rules before judging whether a texture collection reproduces the original effect.

### An effect is more than an atlas
Use recovered effect programs, deterministic particle state and the matching HD textures. A manually arranged atlas cannot reproduce the timing and geometry by itself. Retain the original license and attribution when reusing the MIT-licensed interpreter implementation.

Slow's PS2 program is `000e.bin`; Demi's is `0066.bin`. Reconstruct required HD callbacks separately. Preserve the port's capability limits: approximate Lambert/Blinn lighting, unsupported CircleBlur and incomplete distortion must not silently become claims of PC-DLL equivalence.

### Make time reproducible
The reference interpreter steps at 30 Hz. The destination clip runtime can use a different tick rate, so convert units explicitly. Keep a deterministic random seed and restore simulation history when seeking backward. Moving the preview camera must redraw the same particle state, not advance the effect.

Export enough data per draw to preserve geometry, transforms, UV scrolling, flipbooks, vertex color, blend mode and lifetime. Preserve buildup, steady phases, disappearance and the final clear frame across repeated casts and camera changes.

### Decode callback semantics, not just numbers
Interpret Demi callback value `0x1E` as callback timing, not a second emitter's birth delay. Derive units from the program execution model.

Compare Distiller data, textures and sound selections independently of executable code. Relocation-normalized code equality does not imply equality of the complete visual program.

For color variants, retain geometry, UVs and alpha, then adjust the intended color stage. Size the visible rim, not a bounding box dominated by transparent vertices. Verify that HDR or additive white regions still preserve readable color in the actual destination renderer.

## 22. Getting imported effects into the native scene

A registered effect must also survive material selection, scene submission and renderer ownership.

### Implement each rendering boundary
1. **Catalog:** a private action selects an allocated effect ID.
2. **Submission:** the effect is accepted into the native world-render queue.
3. **Appearance:** it draws with the intended placement, material, depth and timing.

A menu entry and a successful DLL load establish neither the second nor the third. Treat private effects 510/511 and actions 3767/3768 as allocated records, not free slots in another installation.

### Native material fields can quietly suppress or distort a draw
Respect these structure-specific contracts:

| Boundary | Contract |
| --- | --- |
| Material processing at `0x449AB0` | An all-type-0 material set returned early; the converted carrier required type 1 |
| Morph selector at `+0x190` in its own record | An inherited donor curve selected the wrong mesh; use a deliberate constant selection per track |
| Vector routine `0x430B90`, flags `+0x30` | Flags select zero/one/curve paths and couple axes; supplying three curves alone is insufficient |
| Sprite routine `0x449560`, its `+0x190` | A float translation vector, including negative fractions; not a color field |
| Private carrier/model flags | Use the matching blend/queue path and carrier model flags `0x01 → 0x05` |

Identical offsets in different native structures do not describe identical fields. Recover the containing type before changing them.

### Enqueued objects must outlive the callback
The current scene transport owns a snapshot of the view matrix and draw identity at both sort and Gi stages. It does not leave a queued pointer to temporary particle scratch memory. Its identity includes root, attachment, definition, battle, location, generation, caster, target and area.

The sort-copy path at `0x3A2C80` rounds size up to 16-byte units and has a 40,960-slot capacity. Gi allocation at `0x1A1470` has a different rounding convention, reserving an additional unit even for an exact multiple. Guard both capacity and byte range rather than assuming the same allocator contract.

`0x20E630(pair, 2)` queues the prepared pair's pointer; it does not make an independent copy of all supplied data. Keep backing storage stable through consumption. World effects need the scene's depth/camera path; the final Present overlay used by flat HUD panels is a different rendering boundary.

### Capture the camera used by this draw
`GiBeginEff+8` is an inverse-screen transform, not the world view. Its projection at `+0x48` is useful, while the world-view snapshot is captured through the scene path (`0x1F7E528`). The current validator checks finite affine/orthonormal structure and a positive determinant, then applies the required axis conversion.

Do not require the draw snapshot to equal another independently updated camera cache (`0x2AEDEF0`). Match ownership and lifetime first; valid matrices captured at different moments need not be bit-identical.

## 23. Placing and scaling effects on real actors

Resolve a generation-bearing handle and choose an anchor appropriate to the visual.

### Resolve identity before reading a model
The global actor array is published through `0x208E688`, with count at `0x208E6A0`. The bounded reader rejects counts above 512 and uses an actor stride of `0xF50`, actor ID at `+8` and keep pointer at `+0x698`. These are build-specific facts, not a universal game SDK.

Use native handle resolution (`0x2E9B80`, followed by the appropriate model path at `0x3326C0`) rather than interpreting an actor slot as a model-resource index. The current binding also validates the generation bits `(handle >> 20) & 0x7FF` against the object generation at `+0x16`, checks the object kind and obtains the correct payload.

### There is no single correct “actor position”
| Visual purpose | Useful reference |
| --- | --- |
| Ground-attached footprint | Validated feet position |
| Normal target-centered impact | Native model circle center, at `model+0x670` |
| Persistent halo | Authenticated head joint and its current transform |
| Blade-sized projectile | Equipped weapon geometry/socket span |

In the current binding, radius comes from different payload offsets for supported object kinds. The published circle radius already includes a factor of 1.3. Keep the full sizing formula visible to avoid applying the same Slow-derived multiplier twice. A user-requested “20% larger” belongs at one explicit final stage, not independently in extraction, conversion and rendering.

Measure the **visible** reference geometry, such as a Distiller's circular rim; exclude transparent vertices that inflate the bounds. Scale for actual target size and model placement.

Retire placements when the target generation, battle/location identity or save epoch changes. A pointer that remains nonzero across a loading screen does not make the old attachment valid.

## 24. Building blade-aligned projectiles with one impact

Use a real weapon reference, a game-time trajectory and one authoritative damage handoff.

### Reuse a coherent part of an effect
For the custom red slash, isolate one half of Aim's opposing arcs, preserve its animation and recolor the intended component. Use **Aim phase 56–94** for its contact burst. These phase numbers belong to that clip; do not substitute the whole two-sided circle or an unrelated Distiller burst.

The current example binds Broadsword record 4097 to private action 4261, effect 522 and clip 37. These IDs describe one installation and must be allocated again for a different content set.

### Follow the equipped blade, then release toward the target
Resolve the weapon attachment through `j_blade` selector `0x200` / `n_grip` selector `0x201`, using bounded child/sibling traversal. The field at `model+0x18` identifies an instance slot rather than a resource-model ID. Validate each hierarchy node and transform before using it.

Use the blade/socket-space span as the size reference; the Broadsword example uses about `0.944344922` along socket Y with a 1.5 visual multiplier. Keep origin, blade orientation, projectile travel direction and visual size as separate controls. An enemy-sized arc cannot substitute for a blade-sized origin just because both use a radius.

Sample the arc's ridge for collision (33 points in this implementation), sweep between successive game-time positions and update against the target's current placement. Sparks originate on that moving ridge, live for 0.5 game-seconds and fade throughout that lifetime. Pausing the game must freeze both movement and spark aging.

### Contact owns the damage event
The original action callback and the projectile can both reach damage. Removing an event from the visual clip alone is insufficient; arbitrate the shared combat authorization.

Place an `irfm_flight_hit` gate **before** the once flag and finalize through `irfj_result` with the exact authorized RESULT buffer, source, target and callback context. Consume the authorization once. A burst can then finish playing without any further combat event; the visual-only clip excludes events 3/128.

```text
accepted native hit → authorized pending projectile
projectile contact → authenticate result → consume once → native damage
                   → target-anchor burst + one impact sound
late animation callback → no remaining authorization → no second damage
```

Place the burst at the normal native target anchor even if collision occurs at a different ridge point. Retire target-dependent work on miss, death or identity loss, and keep late callbacks from reusing a consumed result.

## 25. Resolving sound events to the correct audio stream

Follow the event mapping; matching a spell name or bank alone is insufficient.

### The extraction chain
Follow this chain: effect OEF audio slot → `SeSep   ` record DWORD at `+8` → sound-ID/event mapping in the binary `*_common.txt` table → FEV event name → matching FSB5 stream name → decoded WAV.

Do not equate an event index with a decoder's subsong index. For NulFrost, event 1123 maps to subsong 1242. Resolve the mapping explicitly; do not extrapolate a constant offset from another bank.

Preserve distinct cues until their triggers are known. Keep Demi main cue 9021 separate from additional cue 14069; do not combine them without resolving their event timing.

Decode the matched ADPCM stream to the required PCM format; the current mixer assets use 16-bit stereo PCM at 48 kHz. Keep extraction separate from trimming, mixing and normalization. Deduplicate identical streams while retaining each event mapping, including shared Break cue 9061.

### A correct weapon bank can still produce the wrong cue
For Ninja Sword bank `se286`, follow the normal-hit path through `0x31ADB0`, with sound class 2 and its output at `+0x34`; event 2 in `0x46C250` selects kind-0 cues 3–5. Event 3/kind 0/cue 10 is a different sound.

Use the event actually reached by the accepted native hit. A swing, contact, critical hit and finishing flourish may share a bank while using different entries. Resolve the actual asset behind an internal symbol: `NinjaHit` can reference a replacement WAV rather than the native bank.

## 26. Making added sounds follow the game’s SFX volume

Put playback in the game process, follow the right category and compare perceived level.

### Read the same category as native sound effects
The native volume routine at `0x2DE290` caps the setting at 100. The settings object is reached through `0x215E6E0`: SFX is the word at `+0x0A`, category 2, scaled by `/100`. Music at `+8` and voice at `+0x0C` are different categories.

Resolve addresses with ASLR and verify the build. The implemented reader falls silent while the configuration is unavailable. A roughly 15 ms update changes the master gain of currently playing added voices as well as new voices, without restarting their PCM.

An XAudio2 mixer inside the game process supports game-process audio capture. It is still a custom mixer: it does not automatically inherit native SEAD bank routing, spatialization or reverb. Likewise, a world/HUD renderer executing inside the game addresses a different capture boundary from an external transparent desktop window. Validate actual capture mode instead of treating all overlays as equivalent.

### Normalize an asset, then apply the live slider
Compare integrated loudness, the loudest short window and true peak. For short impacts, full-clip RMS can hide a sharp transient followed by silence; include a short-window measurement and oversampled true peak. Apply asset gain without changing pitch, duration, EQ or dynamics unless that change is intended.

Choose gain against representative native effects and allow headroom for overlapping casts. Do not reuse a prior clip's loudness target as a universal standard; individually unclipped files can still overload the combined mix.

```text
source PCM → measured asset gain → per-event/user trim → live SFX slider
                                                        → in-process mixer
```

A linear 20% volume reduction is a gain of 0.8, approximately −1.94 dB; it is not a 20 dB reduction. Trigger contact audio once from the same accepted collision as damage. Cancel or retire owned voices on scene change and avoid replaying every frame while a hit flag remains set.

## 27. Creating convincing weapon surfaces without changing geometry

Treat the UV layout, native alpha and internal material binding as part of the artwork.

### Start from the material actually used by the weapon
For a diffuse-only weapon edit, preserve geometry, rig, normal and specular maps. The private Broadsword example uses `w9300 / 0x770800`, derived from `w2105`, with a 256×128 diffuse. Inspect every referencing inventory record, including retired/private clones, before changing a shared binding.

Identify the material's diffuse import and the texture container's internal export name. Renaming the outer `.dds.phyre` file is insufficient. Match the internal DDS export name to the resource requested by the material; a correct outer filename with an old internal name can render a white weapon.

### Preserve the hilt from geometry-derived masks
Derive protected masks from the actual mesh faces and UVs. In the Broadsword example, faces 10–45 form the blade; the other 40 faces cover hilt, guard and pommel. Protect those UVs with a two-texel margin instead of using a broad rectangular atlas selection.

Fit new blade artwork into the native UV layout. Preserve alpha, hidden RGB and protected pixels through repacking. Account for private resource-name substitutions when comparing container geometry.

### What texture alone can suggest
Painted facets and internal-looking light can suggest crystal; controlled veins can suggest stone; directional highlights can suggest brushed metal; cracks with bright cores can suggest heated material. Their success depends on the existing mesh, shader, UV density and lighting. A diffuse edit cannot create real refraction, new silhouette geometry or guaranteed light emission from an opaque material.

## 28. Coloring obtained equipment and preserving enemy suffixes

Follow the formatter and native identity rules rather than patching visible strings by guess.

### Check whether the hook is actually installed
Initialize equipment-message color hooks only after `irf_code_blob` and their other required symbols are published. Authenticate the nine-byte site at `0x536C0B` and its current owner before installation.

The implementation handles acquisition messages 24/25 after native formatting and maps 495 single-class equipment entries. Preserve articles, quantities, pluralization and a final color reset. Shared consumables and gil retain their normal presentation. A colored inventory name is not proof that the combat-log formatter uses the same path.

### A display suffix is not an actor ID
Use the native suffix convention for target names. The native path checks the signed field at `BWEI+0x102`; the negative case reads the 16-bit instance value at `+0x100`. A zero instance has no suffix; positive values cycle through letters:

```python
suffix = '' if instance == 0 else chr(ord('A') + (instance - 1) % 26)
```

Thus 27 is A, 52 is Z and 53 is A. Use the native eligibility conditions as well as the modulo rule. Display letters may repeat; never identify actors by the rendered name or suffix. Selection, cancellation and damage still need the full authenticated handle.

The formatting chain includes `0x263A10`, `0x272CE0`, `0x24ABE0` and `0x2B58F0`. Verify the module actually loaded by the installed executable: an older loose source tree can disagree with the frozen program that is producing the UI.

## 29. Auditing encounter identity, threat and reward placement

Review a whole region, including combat NPCs and reachable AI actions.

### Work within the regional content rules
Before changing Reforged enemies, loot, chests, equipment, passives or hunt rewards, read `IvaliceReforged/memory/20260925_enemy_distribution/criterios_20260926.md` and the current regional donor rules. Keep this content out of standalone Ivalice Together.

Compare candidate families against the native population of every subarea and the current mod roster. A new name, recolor or alternate boss/Trial alias does not create a different species. Do not replace ordinary enemies with boss bodies. Preserve protected hunts and story actors; permission to borrow a model is not permission to rewrite its source encounter.

Place special enemies deliberately across the region rather than always selecting its first slots. Respect the authorized regional totals, access tiers and explicit reuse exceptions in the current rules. Do not invent a new universal population cap.

### Preserve threat, identity and entry behavior
Preserve the original encounter's relative size, durability and role. Compare mesh bounds as well as scale values; a regional giant should not become an ordinary-sized, ordinary-HP substitute. Use suitable weapons, posture, attachments and animation when the replacement species requires them.

When the original has an entry animation, supply a compatible entry for its replacement and retain the transition into movement/combat. Review native spawn initialization, faction, territory and despawn alongside the donor scripts. Copying four AI scripts alone does not establish a compatible spawn contract.

Inventory combat NPCs and every reachable action group and HP phase. Balance damage, healing, status duration, area, targeting, cadence and combos to the region. Use private actions/groups for local changes instead of modifying a shared global technique. Keep noncombat civilians and story interactions intact.

### Author usable rewards
Build a class-by-progression matrix covering chests, steals, ordinary drops, special drops and hunt sets. Distinguish loot/bazaar materials from usable consumables by native item identity and execution contract, not by an elemental-sounding name. Gemini Gem and Charger Barding must not stand in for usable gems or grenades where the reward is intended for immediate use.

Use the compiled inventory IDs and current consumable aliases when editing drops. Check spawn probability, route access, protected quest contents, complete equipment sets and all relevant regional data copies. A grenade in an item catalog is insufficient if no reachable loot path awards its inventory ID.

For new creature textures, retain native UVs, dimensions, alpha and material boundaries while creating the requested artwork. A palette filter alone does not satisfy a request for a new texture. Keep donor choice, encounter behavior and reward changes local to the authorized region.

## 30. Native addresses and hook ownership

Make every low-level claim reproducible on the intended binary.

### Match the executable version
The reference `FFXII_TZA.exe` uses PE machine `0x8664` and preferred image base `0x120000`.

Unless explicitly marked RVA, XII addresses in this manual are **preferred virtual addresses from the reference build**. Convert them before use:

```python
runtime_address = live_module_base + (preferred_va - 0x120000)
```

FFX has its own executable, pointer width, image base and address vocabulary. A generated wrapper's temporary allocation address is neither game's stable RVA.

### Inspect the current bytes and the predecessor
Check instruction boundaries, original signatures, calling convention, stack alignment, register preservation, relocation and jump reach. If an owned hook already occupies the site, authenticate its payload and follow the supported chain; blindly restoring retail bytes would remove another feature.

Authenticate the expected predecessor at each seam, including `0x306480`, before chaining the FFX module. An incompatible predecessor can prevent later services, including save readers, from initializing. Require every dependent module to be ready; another block's “ready” message cannot authorize a missing service.

On teardown, restore only a patch whose current bytes still equal the bytes this owner installed. Retire publication before releasing backing memory. Keep a manifest of signatures, active owners, allocations, source revision and installed hashes.

### The file on disk may not be the executing source
Frozen Python modules inside an installed executable can differ from loose development files. Extract/disassemble the installed module when resolving a contradiction. Label a source-tree finding as such; do not silently elevate it to evidence of the current running build.

## 31. Preparing an implementation handoff

Give the next AI a precise implementation contract.

### Start from the correct release
Identify the installed executable, current Lua/native dependencies and the actual frozen modules. Keep standalone Ivalice Together and Reforged as separate variants. Apply shared control fixes to each variant's own authenticated base; never package the integrated runtime as the standalone co-op release.

Create staging from the current version. Preserve layered successor code that may not exist in loose sources or old builders. For a frozen executable, compare module/function structure before composing the smallest change; an old executable is not a safe replacement for one matching function.

### Follow the owner through the full operation
1. Define the trigger and intended behavior.
2. Identify the native input, queue, result, renderer, audio or save-stream boundary.
3. Specify actor/member identity, generation, area and lifetime.
4. Preserve existing ownership, cancellation and failure cleanup.
5. Synchronize producers, consumers, layouts, content registries and authentication dependencies.
6. Check signatures, bounds, relocation, resources and the release's required integration gate.
7. Prepare exact file replacements and rollback preimages; install loaded-file changes with the game and affected runtimes closed.

Respect the user's scope for game launches, saves and runtime instrumentation. A document update does not authorize gameplay changes, collectors or save edits.

### Copyable implementation brief
```text
Objective and triggering action:
Target variant and current executable/module revision:
Files and native boundaries to change:
Address convention and expected original bytes:
Player/member/actor/scene/generation identity:
Inputs, outputs and execution owner:
Required resources and authentication dependencies:
Admission, payment, completion and cancellation rules:
UI labels, localization and ownership presentation:
Compatibility constraints and retirement behavior:
Installation order, preimages and rollback:
```

Keep the handoff focused on the current mechanism, its constraints and the instructions needed to modify it.
