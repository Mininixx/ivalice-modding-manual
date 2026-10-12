# 06. Independent area-of-effect circles

[← Chapter index](../README.md#chapters)

Area previews and single-target markers use different native object paths. Their allocation and list contracts must be recovered separately.

## Locate the native area preview

On the [reference executable](30-native-addresses-and-hook-ownership.md), investigate factory `0x2911D0`, list append `0x3F34D0` and target-manager list field `+0x10F40`. Follow a native area-targeting action from menu selection through its factory call. Identify which argument supplies radius and which object anchors position.

Record the factory's full arguments and return ownership. The function addresses alone do not establish a callable signature. Preserve the list's sentinel, linking convention and native destruction path; do not assume a standard C++ container layout.

## Additional previews require new ownership

For an additional preview, the new implementation needs an entry containing its native object identity, target identity, radius and scene lifetime. These are design requirements, not an existing game library. Create or update objects on the native UI thread.

If temporarily isolating a native list during creation, retain its original head and all existing links. Restore them on success and failure before appending the new object with the native operation. Never treat an unchanged node pointer as proof that a second allocation succeeded.

## Preserve the user's display setting

The area-display option is represented by bit 22 in the DWORD at `[0x215E6E0]+4` in the reference layout. Read the settings pointer and current flags before changing it. If an extension enables the bit, remember whether it was already enabled and preserve all unrelated bits.

A user can change the setting while the extension is active. Restore only state still owned by the extension; do not blindly write an old full DWORD. Reacquire the setting object if its identity changes.

For preview size, use the native action's radius convention. Screen diameter is affected by perspective and is not a reliable world-space measurement.

---

[← Previous chapter](05-multiple-native-target-circles.md) · [Chapter index](../README.md#chapters) · [Next chapter →](07-target-arrows-and-action-lines.md)
