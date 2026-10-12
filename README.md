# Ivalice Modding Manual

Practical implementation instructions for **FINAL FANTASY XII: The Zodiac Age (PC)**, for mod developers and AI coding assistants.

This manual brings together the native engine interfaces, data layouts and implementation patterns used in **Ivalice Together** and **Ivalice Reforged**. It explains how to connect player input, character ownership, combat commands, effects, UI and persistent data while preserving the game's native behavior.

Updated: 12 October 2026. 31 chapters, each available as a separate file.

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

- **Adding or changing an ability:** [Adding actions without breaking existing commands](chapters/11-adding-actions-without-breaking-existing-commands.md).
- **Working on co-op controls:** [Binding controllers to live actor identities](chapters/03-binding-controllers-to-live-actor-identities.md).
- **Working on the camera:** [A shared camera that still respects the scene](chapters/08-a-shared-camera-that-still-respects-the-scene.md).
- **Changing licenses or progression:** [License boards, prices and purchase previews](chapters/18-license-boards-prices-and-purchase-previews.md).
- **Importing visual effects:** [Extracting effects from Final Fantasy X](chapters/19-extracting-effects-from-final-fantasy-x.md).
- **Writing a native hook:** Read [Native addresses and hook ownership](chapters/30-native-addresses-and-hook-ownership.md) first.

## Chapters

### Control and presentation

1. [Moving additional party members](chapters/01-moving-additional-party-members.md)
2. [Moving a Berserk party leader](chapters/02-moving-a-berserk-party-leader.md)
3. [Binding controllers to live actor identities](chapters/03-binding-controllers-to-live-actor-identities.md)
4. [Independent menus with native command execution](chapters/04-independent-menus-with-native-command-execution.md)
5. [Multiple native target circles](chapters/05-multiple-native-target-circles.md)
6. [Independent area-of-effect circles](chapters/06-independent-area-of-effect-circles.md)
7. [Target arrows and action lines](chapters/07-target-arrows-and-action-lines.md)
8. [A shared camera that still respects the scene](chapters/08-a-shared-camera-that-still-respects-the-scene.md)
9. [Rendering HUDs inside the game](chapters/09-rendering-huds-inside-the-game.md)
10. [Area changes, interaction and state retirement](chapters/10-area-changes-interaction-and-state-retirement.md)

### Combat and content

11. [Adding actions without breaking existing commands](chapters/11-adding-actions-without-breaking-existing-commands.md)
12. [Queueing commands on the game thread](chapters/12-queueing-commands-on-the-game-thread.md)
13. [Damage, status results and enemy reaction](chapters/13-damage-status-results-and-enemy-reaction.md)
14. [Implementing Breaks and bounded debuffs](chapters/14-implementing-breaks-and-bounded-debuffs.md)
15. [Persistent buffs, halos and automatic revival](chapters/15-persistent-buffs-halos-and-automatic-revival.md)
16. [Replacing status icons without square borders](chapters/16-replacing-status-icons-without-square-borders.md)
17. [Saving new resources inside each save](chapters/17-saving-new-resources-inside-each-save.md)
18. [License boards, prices and purchase previews](chapters/18-license-boards-prices-and-purchase-previews.md)
19. [Extracting effects from Final Fantasy X](chapters/19-extracting-effects-from-final-fantasy-x.md)
20. [Sharing Ghidra types and exporting definitions](chapters/20-sharing-ghidra-types-and-exporting-definitions.md)
21. [Recovering particle programs and their timeline](chapters/21-recovering-particle-programs-and-their-timeline.md)
22. [Getting imported effects into the native scene](chapters/22-getting-imported-effects-into-the-native-scene.md)
23. [Placing and scaling effects on real actors](chapters/23-placing-and-scaling-effects-on-real-actors.md)
24. [Building blade-aligned projectiles with one impact](chapters/24-building-blade-aligned-projectiles-with-one-impact.md)
25. [Resolving sound events to the correct audio stream](chapters/25-resolving-sound-events-to-the-correct-audio-stream.md)
26. [Making added sounds follow the game’s SFX volume](chapters/26-making-added-sounds-follow-the-games-sfx-volume.md)
27. [Creating convincing weapon surfaces without changing geometry](chapters/27-creating-convincing-weapon-surfaces-without-changing-geometry.md)
28. [Coloring obtained equipment and preserving enemy suffixes](chapters/28-coloring-obtained-equipment-and-preserving-enemy-suffixes.md)
29. [Auditing encounter identity, threat and reward placement](chapters/29-auditing-encounter-identity-threat-and-reward-placement.md)

### Implementation and handoff

30. [Native addresses and hook ownership](chapters/30-native-addresses-and-hook-ownership.md)
31. [Preparing an implementation handoff](chapters/31-preparing-an-implementation-handoff.md)

## Using the manual with an AI assistant

Give the assistant the relevant chapter together with the current source files, target variant and intended behavior. The [implementation brief](chapters/31-preparing-an-implementation-handoff.md) provides a compact structure for that request.

When implementing a change:

- Start from the current authenticated installation or release. Older prototypes and loose source files may differ from the code inside a frozen runtime.
- Match the executable, address convention, instruction bytes and existing hook owner before applying an offset.
- Keep player, character, actor, generation and scene identities distinct. Define who owns each operation and when that ownership ends.
- Preserve allocated IDs, save layouts, native execution rules and dependency contracts.
- Keep standalone **Ivalice Together** and **Ivalice Reforged** separate. Reforged class, license and custom inventory mechanics belong to the integrated variant.

Addresses and private allocations describe specific implementations. Read them with their surrounding contract; they are not universal constants for every game build or mod setup.

XII addresses use preferred image base `0x120000` unless explicitly identified as RVA. Resolve the runtime base and authenticate instruction bytes and hook ownership.

A [single-file edition](Ivalice_Modding_Manual.md) is also available for sharing the complete manual with an AI assistant.
