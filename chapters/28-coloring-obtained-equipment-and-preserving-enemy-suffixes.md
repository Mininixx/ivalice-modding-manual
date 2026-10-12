# 28. Coloring obtained equipment and preserving enemy suffixes

[← Chapter index](../README.md#chapters)

Follow the formatter and native identity rules rather than patching visible strings by guess.

## Check whether the hook is actually installed
Initialize equipment-message color hooks only after `irf_code_blob` and their other required symbols are published. Authenticate the nine-byte site at `0x536C0B` and its current owner before installation.

The implementation handles acquisition messages 24/25 after native formatting and maps 495 single-class equipment entries. Preserve articles, quantities, pluralization and a final color reset. Shared consumables and gil retain their normal presentation. A colored inventory name is not proof that the combat-log formatter uses the same path.

## A display suffix is not an actor ID
Use the native suffix convention for target names. The native path checks the signed field at `BWEI+0x102`; the negative case reads the 16-bit instance value at `+0x100`. A zero instance has no suffix; positive values cycle through letters:

```python
suffix = '' if instance == 0 else chr(ord('A') + (instance - 1) % 26)
```

Thus 27 is A, 52 is Z and 53 is A. Use the native eligibility conditions as well as the modulo rule. Display letters may repeat; never identify actors by the rendered name or suffix. Selection, cancellation and damage still need the full authenticated handle.

The formatting chain includes `0x263A10`, `0x272CE0`, `0x24ABE0` and `0x2B58F0`. Verify the module actually loaded by the installed executable: an older loose source tree can disagree with the frozen program that is producing the UI.

---

[← Previous chapter](27-creating-convincing-weapon-surfaces-without-changing-geometry.md) · [Chapter index](../README.md#chapters) · [Next chapter →](29-auditing-encounter-identity-threat-and-reward-placement.md)
