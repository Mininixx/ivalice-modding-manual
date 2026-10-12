# 02. Moving a Berserk party leader

[← Chapter index](../README.md#chapters)

The native status classifier separates movement restrictions from action restrictions. Changing the movement decision can preserve Berserk's status and combat behavior.

## Exact instruction boundary

Use the executable fingerprint in [Address reference](30-native-addresses-and-hook-ownership.md). The relevant instructions are:

| Preferred VA | Original bytes | Meaning |
| --- | --- | --- |
| `0x23B166` | `25 3B 40 00 88` | `AND EAX, 0x8800403B` |
| `0x23B16B` | `0F 44 CB` | `CMOVE ECX, EBX`, consuming those flags |
| `0x23B173` | `81 E2 3B 00 00 88` | A separate `AND EDX, 0x8800003B` |

Immediately before the first AND, the code loads `actor+0x698`, reads DWORDs at `+0x64` and `+0x3C` from that object, combines them with OR and copies the combined status into EAX. The actor is in RDI at this instruction site. These register meanings are local to this path, not a function prototype.

## Smallest change for movement classification

Berserk occupies bit 27 in this status word. Removing only that bit from the first mask changes `0x8800403B` to `0x8000403B`. The replacement instruction is:

```text
Preferred VA 0x23B166
Before: 25 3B 40 00 88
After:  25 3B 40 00 80
```

The instruction length stays five bytes, so the following CMOVE still reads flags from the AND. This alters the classification at that site for every actor that reaches it. It is not an actor-filtered patch.

For an actor-specific extension, intercept this instruction, compare the current actor with the chosen live actor, execute the selected AND last, then return to `0x23B16B`. Preserve every register used by the filter. No comparison or arithmetic may overwrite the AND's flags before the CMOVE. Any ownership record used by that filter must be implemented by the extension itself.

Leave the second mask, both stored status banks and the native movement calculation unchanged. Do not clear the Berserk status to obtain movement.

## Action admission is independent

The manual-command body contains `TEST ECX,0x8800203B` at `0x311D72`. That is a different restriction boundary. Changing it would change command admission and is outside the movement-only patch described above. See [Native command submission](04-independent-menus-with-native-command-execution.md).

Check the executable hash and exact instruction bytes before applying either an in-memory or file patch. A preferred VA must be translated before use; it is not a file offset. This chapter provides the instruction-level change, not a DLL loader or patch installer.

---

[← Previous chapter](01-moving-additional-party-members.md) · [Chapter index](../README.md#chapters) · [Next chapter →](03-binding-controllers-to-live-actor-identities.md)
