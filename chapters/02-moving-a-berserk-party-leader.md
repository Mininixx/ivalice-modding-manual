# 02. Moving a Berserk party leader

[← Chapter index](../README.md#chapters)

Separate locomotion ownership from status effects and command eligibility.

## Let native input calculate movement
Use the native status-classification boundary at **preferred VA `0x23B166`**, inside `0x23B040`. This is an instruction site, not a callable function and not an RVA. With image base `0x120000`, its RVA is `0x11B166`. Match the five original bytes `25 3B 40 00 88` before installing the detour; return to `0x23B16B`.

At this boundary, `RDI` is the native leader actor and `EAX` and `EDX` contain the combined status. `actor+0x698` points to battle KEEP; combine permanent status at `KEEP+0x3C` with temporary status at `KEEP+0x64`. Berserk is bit 27.

For the authenticated P1 owner only, execute `AND EAX,0x8000403B` instead of `AND EAX,0x8800403B`. For every other actor or inactive publication, replay the original AND. Preserve the flags from that final AND for the following `CMOVE`; comparisons against the ownership record must occur before it. Preserve scratch registers, stack balance and the full displaced instruction.

The native consumer then retains responsibility for keyboard/gamepad input, movement magnitude and turning. Do not calculate P1 heading in the external worker or force physics direction each update. Keep P2/P3 steering separate.

## Publish permission and identity only
Use `build_berserk_native_movement_gate`, `install_berserk_native_movement_gate` and the current `write_p1_berserk_command` implementation in the authenticated frozen runtime. The extension-owned P1 state reserves `0x40` bytes: actor at `+0x08`, physics at `+0x10`, legacy active at `+0x18`, native permission at `+0x3C`. Resolve its base from the installed layout; these are not native actor fields.

Revoke native permission before changing identity, keep legacy active at zero, publish valid actor/physics, and arm native permission last. Revoke on status loss, owner change, KO, loading, modal UI or invalid identity. The retired vector helper must return `CLC; RET`, allowing its caller to continue through the native route. Do not restore the old heading/magnitude/facing publications.

The native gate checks permission, compares the published actor against `RDI`, and rechecks permission. Treat this as the existing ownership protocol, not as a general atomic snapshot guarantee. A change to publication synchronization also requires a matching consumer and a new runtime layout identity.

## Preserve status and action restrictions
Leave `EDX`, both KEEP status banks and the second mask at **`0x23B173`** unchanged. That second instruction applies `AND EDX,0x8800003B` for native action availability. Removing Berserk from the movement mask must not clear the status, remove its combat effects or silently enable every action. All other bits in the movement mask retain their native restrictions.

The separate manual-command policy at `0x311D72` may change `F7 C1 3B 20 00 88` to `F7 C1 3B 20 00 80`. Preserve its existing scope and any Reforged Blood Berserk rules; do not use it as the movement fix. Register the new movement hook in process-lifetime ownership and layout metadata. A process with an older incompatible layout requires a clean restart instead of live topology conversion.

---

[← Previous chapter](01-moving-additional-party-members.md) · [Chapter index](../README.md#chapters) · [Next chapter →](03-binding-controllers-to-live-actor-identities.md)
