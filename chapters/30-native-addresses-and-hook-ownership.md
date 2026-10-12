# 30. Native addresses and hook ownership

[← Chapter index](../README.md#chapters)

Native addresses are meaningful only with an executable identity and an explicit address convention.

## Reference executable

| Property | Value |
| --- | --- |
| File | `FFXII_TZA.exe`, PC x64 |
| File length | 32,864,752 bytes |
| SHA-256 | `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8` |
| SHA-1 | `0751de97e1831b1f5a80d40c80e1fcfa609ae402` |
| PE machine | `0x8664` |
| Preferred image base | `0x120000` |
| PE timestamp field | `0x5DCA7FD7` |

The fingerprint selects this binary, not every storefront build or later revision. Extracted data files need their own identities; an executable hash does not establish that a Battle Pack or texture is unchanged.

## Translate addresses correctly

Unless labeled otherwise, executable addresses in these chapters are preferred VAs for the binary above:

```text
RVA = preferred_VA - preferred_image_base
runtime_address = live_module_base + RVA
file_offset = matching_section.PointerToRawData
              + RVA - matching_section.VirtualAddress
```

The file-offset formula applies only inside a section's raw-backed range. Virtual zero-filled data has no equivalent bytes to read from disk. Microsoft's [PE format reference](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format) defines the relevant header and section fields.

The included [read-only PE inspector](../tools/inspect_native.py) calculates the file fingerprint and translates supplied preferred VAs without importing a game runtime or loading a DLL:

```text
python tools/inspect_native.py "path/to/FFXII_TZA.exe" --va 0x23B166 --size 5
```

The executable path is supplied by the reader. The script reads the file and prints JSON; it does not attach to or modify the game.

## Native instruction signatures

| Preferred VA | RVA | Bytes | Boundary |
| --- | --- | --- | --- |
| `0x23B166` | `0x11B166` | `25 3B 40 00 88` | Movement status mask |
| `0x23B173` | `0x11B173` | `81 E2 3B 00 00 88` | Separate action-related mask |
| `0x28E480` | `0x16E480` | `E8 6B 28 00 00` | Call to native UI update `0x290CF0` |
| `0x291959` | `0x171959` | `83 F8 02` | Target-marker capacity comparison |
| `0x311D72` | `0x1F1D72` | `F7 C1 3B 20 00 88` | Manual submission status test |

Matching a few bytes is a local check, not a replacement for the binary fingerprint and caller analysis. Other addresses in the manual are investigation points; an address by itself does not supply a function prototype or object layout.

## Install hooks with the actual ABI

Recover instruction boundaries, argument widths, live registers, stack alignment, relative operands and return behavior. The [Microsoft x64 ABI](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention) defines register arguments, shadow space and register preservation. A mid-function interception also has live state beyond an ordinary function-call boundary.

Relocate every displaced relative instruction correctly and preserve the original route. Memory allocation and executable-page protection changes belong to an explicitly implemented hook installer; no installer library is assumed here. If a site already differs from the expected native bytes, identify its owner before chaining or replacing it.

On teardown, restore only bytes still owned by the extension and release executable backing storage only after no thread can execute it. A DLL load message does not prove that its dependent native hooks or data readers initialized correctly.

---

[← Previous chapter](29-encounter-identity-and-reward-placement.md) · [Chapter index](../README.md#chapters) · [Next chapter →](31-preparing-an-implementation-handoff.md)
