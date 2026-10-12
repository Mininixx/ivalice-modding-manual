# 04. Independent menus with native command execution

[← Chapter index](../README.md#chapters)

An independent menu is new UI code. Vanilla supplies action data, actor resolution and a manual-command path, but it does not supply a ready-made multi-menu service. This chapter documents the native boundary needed to connect a new frontend to ordinary game execution.

All preferred VAs below refer to the exact executable in [Address reference](30-native-addresses-and-hook-ownership.md). The names used for C++ types are descriptive names introduced here, not exported game symbols.

## 1. Keep the frontend's state explicit

The frontend needs the following data, owned by the new implementation:

| Value | Purpose |
| --- | --- |
| Issuer handle | The live actor requesting an action |
| Page and cursor | UI navigation only; never used as an Action ID |
| Selected Action ID | Native action-table identity, stored separately from its name |
| Target handle | Full native target identity |
| Scene/selection revision | Reject a selection made before a scene or issuer change |
| Phase | Browsing, targeting, request pending, or closed |

Resolve labels from the language's game data. A name reference and an Action ID need not be the same number. Build availability from native state and re-evaluate it at confirmation; displaying an enabled row does not guarantee that an actor remains eligible a frame later.

## 2. Resolve and validate on the game thread

The following native boundaries are visible in the reference binary:

| Preferred VA | Calling boundary |
| --- | --- |
| `0x31B7E0` | Resolves the 32-bit handle accepted by manual submission to an actor; null when unavailable |
| `0x317BC0` | Receives Action ID in CX, actor pointer in RDX, optional DWORD reason output in R8 |
| `0x311CD0` | Manual-command wrapper: issuer in ECX, target in EDX, Action ID in R8W, scope argument in R9D |
| `0x311B20` | Internal route used by the wrapper; resolves handles and may take a multi-actor branch |
| `0x311CF0` | Per-actor submission body; writes the native request fields |

The reconstructed types for the first three boundaries are:

```cpp
#include <cstdint>

using ResolveActor = void* (*)(uint32_t handle);
using ValidateAction = int32_t (*)(uint16_t action, void* actor,
                                   uint32_t* reason);
using SubmitManual = int32_t (*)(uint32_t issuer, uint32_t target,
                                uint16_t action, uint32_t scope);
```

These are in-process x64 function pointers. They cannot be called by casting a remote process address inside an external Python process. Resolve their addresses as `module_base + (preferred_va - 0x120000)` only after matching the executable.

The validator returns state 3 on its fully ready path, state 1 for some blocked/deferred states, and state 0 for earlier admission failures. It writes the underlying reason to the optional output. Do not replace those states with a single “nonzero means allowed” check. The routine checks several availability conditions; it is not proof that a target is valid for every action.

## 3. Submit an ordinary, single-actor request

For the ordinary single-actor route, use scope zero. The wrapper clears the internal byte argument, moves the Action ID into R9W, passes scope on the stack and calls `0x311B20`. A nonzero scope enters different behavior, including enumeration of party actors; it is not a generic success flag.

This fragment belongs inside a caller function and shows only the native call boundary after handle, target, scene and readiness checks. `module_base` is a `uintptr_t`; `issuer` and `target` are `uint32_t`, and `action` is `uint16_t`. These are values obtained by the caller, not omitted helper libraries:

```cpp
// Must execute inside the game, at the established game-thread boundary.
auto resolve = reinterpret_cast<ResolveActor>(module_base + 0x1FB7E0);
auto validate = reinterpret_cast<ValidateAction>(module_base + 0x1F7BC0);
auto submit = reinterpret_cast<SubmitManual>(module_base + 0x1F1CD0);

void* actor = resolve(issuer);
if (!actor || !resolve(target)) {
    // Ordinary live-target example: refuse stale or unavailable handles.
    return;
}
uint32_t reason = 0;
if (validate(action, actor, &reason) != 3) {
    // Keep the reason for UI feedback; do not bypass native rejection.
    return;
}
const int32_t raw_result = submit(issuer, target, action, 0);
// raw_result alone does not prove admission or completed execution.
```

This example excludes zero-target/reserve-member requests, summon dismissal and other special routes. Those require their own native caller analysis. Do not apply an ordinary actor-target prototype to every visible menu command.

## 4. Understand what submission actually writes

The body at `0x311CF0` obtains the status record through actor `+0x698`. It combines DWORDs at status `+0x64` and `+0x3C`, then tests `0x8800203B` before writing the ordinary request.

| Actor-relative field | Width | Observed write on the request path |
| --- | --- | --- |
| `+0xBA0` | 16 bits | Requested Action ID |
| `+0xBB8` | 32 bits | Target handle, or a native alternate-target path |
| `+0xBA4` | 16 bits | OR with `0x8000` |
| `+0x000` | 64 bits | OR with `0x4000` |
| `+0x6B0` | 32 bits | Target-mode bookkeeping |

The routine also invokes `0x317E60` and has additional action-specific side effects. Writing only the Action ID and target is not equivalent to calling the native path.

**A zero return is ambiguous.** The status-rejection branch and the ordinary accepted path both reach a zero return. Observe the request fields and subsequent native consumption to distinguish admission from no-op. Missing issuer/target resolution can return `-1` in the outer route; an unusable actor/status record can reach `-2` in the inner body. Neither a return code nor a displayed animation proves final damage, payment or completion.

## 5. Supply an explicit dispatcher

A possible game-thread integration site is the five-byte call at `0x28E480`: `E8 6B 28 00 00`, calling `0x290CF0`. Replacing that call is not the whole dispatcher. A new extension must install its own compatible wrapper, preserve the original call and implement request transfer.

A simple design uses a bounded queue of value-only requests protected by a mutex. The input/UI producer copies `{sequence, issuer_handle, target_handle, action_id, scene_revision}` under that mutex. The game-thread wrapper removes a request, releases the mutex, resolves current actors, rejects stale scene revisions, validates and submits. Never hold the queue mutex while invoking the game. Return feedback through a separate value-only queue. These queues are extension code to implement; no DLL containing them is assumed.

Follow the [Microsoft x64 calling convention](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention): preserve live state around the interception, maintain stack alignment and provide the callee's shadow space. Do not call engine UI routines from a controller polling thread.

## 6. Finish the frontend separately

The renderer, target-list builder and native wait-mode integration are separate implementation work. A target list must retain full handles and distinguish ordinary targets, dead allies and special commands using native eligibility rules. Re-resolve the selection immediately before submission.

Close or invalidate the menu when its issuer or scene disappears. Do not deduct MP/items in the frontend when the native executor is responsible for payment. Document any target-filter or wait-mode branch whose native behavior remains unresolved instead of silently accepting all targets or calling an unspecified helper.

---

[← Previous chapter](03-binding-controllers-to-live-actor-identities.md) · [Chapter index](../README.md#chapters) · [Next chapter →](05-multiple-native-target-circles.md)
