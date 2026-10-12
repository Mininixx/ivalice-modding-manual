# FFXII TZA Native Modding Manual

Technical instructions for AI coding assistants working from **vanilla FINAL FANTASY XII: The Zodiac Age (PC)**.

The chapters describe native engine boundaries, data relationships and the code needed when adding new behavior. No preloaded mod framework, custom class system, private DLL or unpublished helper library is assumed.

## Start here

- [Identify the executable and translate addresses](chapters/30-native-addresses-and-hook-ownership.md).
- [Understand native manual-command submission](chapters/04-independent-menus-with-native-command-execution.md).
- [Read Action data and plan an allocation](chapters/11-adding-actions-without-breaking-existing-commands.md).
- [Prepare a concrete implementation request for an AI](chapters/31-preparing-an-implementation-handoff.md).

## How to use the reference

Native addresses refer to the exact executable fingerprint in Chapter 30. Instruction bytes, reconstructed calling contracts and incomplete investigation points are distinguished in the text. A named address is not automatically a fully documented callable function.

Algorithms for a new UI, queue, renderer or controller are explicitly described as code to implement. Where a native signature or format is unresolved, the chapter states that limit. Do not invent a helper or assume an additional runtime exists to fill the gap.

The chapter files are the maintained documentation. The only included tool is a [read-only PE inspector](tools/inspect_native.py), implemented with the Python standard library. Run it against your own executable; no game assets or binaries are distributed here.

## Chapters

### Input, UI and world state

1. [Moving additional party members](chapters/01-moving-additional-party-members.md)
2. [Moving a Berserk party leader](chapters/02-moving-a-berserk-party-leader.md)
3. [Binding controllers to live actor identities](chapters/03-binding-controllers-to-live-actor-identities.md)
4. [Independent menus with native command execution](chapters/04-independent-menus-with-native-command-execution.md)
5. [Multiple native target circles](chapters/05-multiple-native-target-circles.md)
6. [Independent area-of-effect circles](chapters/06-independent-area-of-effect-circles.md)
7. [Target arrows and action lines](chapters/07-target-arrows-and-action-lines.md)
8. [Camera state, collision and transitions](chapters/08-camera-state-collision-and-transitions.md)
9. [Rendering HUDs inside the game](chapters/09-rendering-huds-inside-the-game.md)
10. [Area changes, interaction and state retirement](chapters/10-area-changes-interaction-and-state-retirement.md)

### Actions, results and progression

11. [Adding actions without breaking existing commands](chapters/11-adding-actions-without-breaking-existing-commands.md)
12. [Queueing commands on the game thread](chapters/12-queueing-commands-on-the-game-thread.md)
13. [Damage, status results and enemy reaction](chapters/13-damage-status-results-and-enemy-reaction.md)
14. [Native damage modifiers and debuffs](chapters/14-native-damage-modifiers-and-debuffs.md)
15. [Native status and revival lifetimes](chapters/15-native-status-and-revival-lifetimes.md)
16. [Replacing status icons without square borders](chapters/16-replacing-status-icons-without-square-borders.md)
17. [Native save boundaries](chapters/17-native-save-boundaries.md)
18. [License boards, prices and purchase previews](chapters/18-license-boards-prices-and-purchase-previews.md)

### Assets, rendering and audio

19. [Native effect assets](chapters/19-native-effect-assets.md)
20. [Sharing Ghidra types and exporting definitions](chapters/20-sharing-ghidra-types-and-exporting-definitions.md)
21. [Native effect timelines](chapters/21-native-effect-timelines.md)
22. [Native effect resources and scene submission](chapters/22-native-effect-resources-and-scene-submission.md)
23. [Placing and scaling effects on real actors](chapters/23-placing-and-scaling-effects-on-real-actors.md)
24. [Weapon animation and hit timing](chapters/24-weapon-animation-and-hit-timing.md)
25. [Resolving sound events to the correct audio stream](chapters/25-resolving-sound-events-to-the-correct-audio-stream.md)
26. [Making added sounds follow the game’s SFX volume](chapters/26-making-added-sounds-follow-the-games-sfx-volume.md)
27. [Creating convincing weapon surfaces without changing geometry](chapters/27-creating-convincing-weapon-surfaces-without-changing-geometry.md)
28. [Coloring obtained equipment and preserving enemy suffixes](chapters/28-coloring-obtained-equipment-and-preserving-enemy-suffixes.md)
29. [Encounter identity and reward placement](chapters/29-encounter-identity-and-reward-placement.md)

### Native integration and handoff

30. [Native addresses and hook ownership](chapters/30-native-addresses-and-hook-ownership.md)
31. [Preparing an implementation handoff](chapters/31-preparing-an-implementation-handoff.md)

## Public references

- [Microsoft PE format](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format) and [x64 calling convention](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention).
- [Ghidra introduction](https://ghidra.re/ghidra_docs/GhidraClass/Beginner/Introduction_to_Ghidra_Student_Guide.html).
- [FFXII asset-format specifications and tools](https://github.com/StyuDEV/ffxii-tza-tools), an optional external resource for extracted game assets.
