# 31. Preparing an implementation handoff

[← Chapter index](../README.md#chapters)

Give the next AI a precise implementation contract.

## Start from the correct release
Identify the installed executable, current Lua/native dependencies and the actual frozen modules. Keep standalone Ivalice Together and Reforged as separate variants. Apply shared control fixes to each variant's own authenticated base; never package the integrated runtime as the standalone co-op release.

Create staging from the current version. Preserve layered successor code that may not exist in loose sources or old builders. For a frozen executable, compare module/function structure before composing the smallest change; an old executable is not a safe replacement for one matching function.

## Follow the owner through the full operation
1. Define the trigger and intended behavior.
2. Identify the native input, queue, result, renderer, audio or save-stream boundary.
3. Specify actor/member identity, generation, area and lifetime.
4. Preserve existing ownership, cancellation and failure cleanup.
5. Synchronize producers, consumers, layouts, content registries and authentication dependencies.
6. Check signatures, bounds, relocation, resources and the release's required integration gate.
7. Prepare exact file replacements and rollback preimages; install loaded-file changes with the game and affected runtimes closed.

Respect the user's scope for game launches, saves and runtime instrumentation. A document update does not authorize gameplay changes, collectors or save edits.

## Copyable implementation brief
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

---

[← Previous chapter](30-native-addresses-and-hook-ownership.md) · [Chapter index](../README.md#chapters)
