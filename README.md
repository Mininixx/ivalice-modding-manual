# Ivalice Modding Manual

Practical implementation instructions for **FINAL FANTASY XII: The Zodiac Age (PC)**, for mod developers and AI coding assistants.

This manual brings together the native engine interfaces, data layouts and implementation patterns used in **Ivalice Together** and **Ivalice Reforged**. It explains how to connect player input, character ownership, combat commands, effects, UI and persistent data while preserving the game's native behavior.

**[Read the complete manual →](Ivalice_Modding_Manual.md)**

## What you will find

| Area | Topics |
| --- | --- |
| Co-op and input | Independent movement and menus, native Berserk movement, XInput/SDL routing, keyboard ownership, guests and reserve players |
| Camera and presentation | Shared camera, area transitions, Party/Pause suspension, target circles, action lines and in-game HUD rendering |
| Combat and abilities | Action/effect allocation, native command queues, resource payment, damage, buffs, Mix and Pockets |
| Saves and progression | Versioned save extensions, inventory bounds, license ownership, LP costs, board regions and class-specific icons |
| Effects and assets | FFX effect extraction, particle programs, native scene submission, weapon attachments, impact timing, audio and materials |
| Implementation | Address relocation, hook ownership, frozen runtime modules, dependency contracts and handoffs between developers or AI assistants |

## Where to start

- **Adding or changing an ability:** [Adding actions without breaking existing commands](Ivalice_Modding_Manual.md#11-adding-actions-without-breaking-existing-commands).
- **Working on co-op controls:** [Binding controllers to live actor identities](Ivalice_Modding_Manual.md#03-binding-controllers-to-live-actor-identities).
- **Working on the camera:** [A shared camera that still respects the scene](Ivalice_Modding_Manual.md#08-a-shared-camera-that-still-respects-the-scene).
- **Changing licenses or progression:** [License boards, prices and purchase previews](Ivalice_Modding_Manual.md#18-license-boards-prices-and-purchase-previews).
- **Importing visual effects:** [Extracting effects from Final Fantasy X](Ivalice_Modding_Manual.md#19-extracting-effects-from-final-fantasy-x).
- **Writing a native hook:** Read [Native addresses and hook ownership](Ivalice_Modding_Manual.md#30-native-addresses-and-hook-ownership) first.

## Using the manual with an AI assistant

Give the assistant the relevant chapter together with the current source files, target variant and intended behavior. The [implementation brief](Ivalice_Modding_Manual.md#31-preparing-an-implementation-handoff) provides a compact structure for that request.

When implementing a change:

- Start from the current authenticated installation or release. Older prototypes and loose source files may differ from the code inside a frozen runtime.
- Match the executable, address convention, instruction bytes and existing hook owner before applying an offset.
- Keep player, character, actor, generation and scene identities distinct. Define who owns each operation and when that ownership ends.
- Preserve allocated IDs, save layouts, native execution rules and dependency contracts.
- Keep standalone **Ivalice Together** and **Ivalice Reforged** separate. Reforged class, license and custom inventory mechanics belong to the integrated variant.

Addresses and private allocations describe specific implementations. Read them with their surrounding contract; they are not universal constants for every game build or mod setup.

## Reading formats

The **[Markdown edition](Ivalice_Modding_Manual.md)** can be read directly on GitHub and used as context for an AI assistant.

The **[HTML edition source](Ivalice_Modding_Manual.html)** includes chapter search, **Copy for AI**, Markdown export and print support. It can be opened locally or published as a website through GitHub Pages.

<details>
<summary><strong>Full chapter index — 31 chapters</strong></summary>

### Control and presentation

1. [Moving additional party members](Ivalice_Modding_Manual.md#01-moving-additional-party-members)
2. [Moving a Berserk party leader](Ivalice_Modding_Manual.md#02-moving-a-berserk-party-leader)
3. [Binding controllers to live actor identities](Ivalice_Modding_Manual.md#03-binding-controllers-to-live-actor-identities)
4. [Independent menus with native command execution](Ivalice_Modding_Manual.md#04-independent-menus-with-native-command-execution)
5. [Multiple native target circles](Ivalice_Modding_Manual.md#05-multiple-native-target-circles)
6. [Independent area-of-effect circles](Ivalice_Modding_Manual.md#06-independent-area-of-effect-circles)
7. [Target arrows and action lines](Ivalice_Modding_Manual.md#07-target-arrows-and-action-lines)
8. [A shared camera that still respects the scene](Ivalice_Modding_Manual.md#08-a-shared-camera-that-still-respects-the-scene)
9. [Rendering HUDs inside the game](Ivalice_Modding_Manual.md#09-rendering-huds-inside-the-game)
10. [Area changes, interaction and state retirement](Ivalice_Modding_Manual.md#10-area-changes-interaction-and-state-retirement)

### Combat and content

11. [Adding actions without breaking existing commands](Ivalice_Modding_Manual.md#11-adding-actions-without-breaking-existing-commands)
12. [Queueing commands on the game thread](Ivalice_Modding_Manual.md#12-queueing-commands-on-the-game-thread)
13. [Damage, status results and enemy reaction](Ivalice_Modding_Manual.md#13-damage-status-results-and-enemy-reaction)
14. [Implementing Breaks and bounded debuffs](Ivalice_Modding_Manual.md#14-implementing-breaks-and-bounded-debuffs)
15. [Persistent buffs, halos and automatic revival](Ivalice_Modding_Manual.md#15-persistent-buffs-halos-and-automatic-revival)
16. [Replacing status icons without square borders](Ivalice_Modding_Manual.md#16-replacing-status-icons-without-square-borders)
17. [Saving new resources inside each save](Ivalice_Modding_Manual.md#17-saving-new-resources-inside-each-save)
18. [License boards, prices and purchase previews](Ivalice_Modding_Manual.md#18-license-boards-prices-and-purchase-previews)
19. [Extracting effects from Final Fantasy X](Ivalice_Modding_Manual.md#19-extracting-effects-from-final-fantasy-x)
20. [Sharing Ghidra types and exporting definitions](Ivalice_Modding_Manual.md#20-sharing-ghidra-types-and-exporting-definitions)
21. [Recovering particle programs and their timeline](Ivalice_Modding_Manual.md#21-recovering-particle-programs-and-their-timeline)
22. [Getting imported effects into the native scene](Ivalice_Modding_Manual.md#22-getting-imported-effects-into-the-native-scene)
23. [Placing and scaling effects on real actors](Ivalice_Modding_Manual.md#23-placing-and-scaling-effects-on-real-actors)
24. [Building blade-aligned projectiles with one impact](Ivalice_Modding_Manual.md#24-building-blade-aligned-projectiles-with-one-impact)
25. [Resolving sound events to the correct audio stream](Ivalice_Modding_Manual.md#25-resolving-sound-events-to-the-correct-audio-stream)
26. [Making added sounds follow the game’s SFX volume](Ivalice_Modding_Manual.md#26-making-added-sounds-follow-the-games-sfx-volume)
27. [Creating convincing weapon surfaces without changing geometry](Ivalice_Modding_Manual.md#27-creating-convincing-weapon-surfaces-without-changing-geometry)
28. [Coloring obtained equipment and preserving enemy suffixes](Ivalice_Modding_Manual.md#28-coloring-obtained-equipment-and-preserving-enemy-suffixes)
29. [Auditing encounter identity, threat and reward placement](Ivalice_Modding_Manual.md#29-auditing-encounter-identity-threat-and-reward-placement)

### Implementation and handoff

30. [Native addresses and hook ownership](Ivalice_Modding_Manual.md#30-native-addresses-and-hook-ownership)
31. [Preparing an implementation handoff](Ivalice_Modding_Manual.md#31-preparing-an-implementation-handoff)

</details>
