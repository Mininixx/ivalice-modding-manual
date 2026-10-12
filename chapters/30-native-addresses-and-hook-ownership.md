# 30. Native addresses and hook ownership

[← Chapter index](../README.md#chapters)

Make every low-level claim reproducible on the intended binary.

## Match the executable version
The reference `FFXII_TZA.exe` uses PE machine `0x8664` and preferred image base `0x120000`.

Unless explicitly marked RVA, XII addresses in this manual are **preferred virtual addresses from the reference build**. Convert them before use:

```python
runtime_address = live_module_base + (preferred_va - 0x120000)
```

FFX has its own executable, pointer width, image base and address vocabulary. A generated wrapper's temporary allocation address is neither game's stable RVA.

## Inspect the current bytes and the predecessor
Check instruction boundaries, original signatures, calling convention, stack alignment, register preservation, relocation and jump reach. If an owned hook already occupies the site, authenticate its payload and follow the supported chain; blindly restoring retail bytes would remove another feature.

Authenticate the expected predecessor at each seam, including `0x306480`, before chaining the FFX module. An incompatible predecessor can prevent later services, including save readers, from initializing. Require every dependent module to be ready; another block's “ready” message cannot authorize a missing service.

On teardown, restore only a patch whose current bytes still equal the bytes this owner installed. Retire publication before releasing backing memory. Keep a manifest of signatures, active owners, allocations, source revision and installed hashes.

## The file on disk may not be the executing source
Frozen Python modules inside an installed executable can differ from loose development files. Extract/disassemble the installed module when resolving a contradiction. Label a source-tree finding as such; do not silently elevate it to evidence of the current running build.

---

[← Previous chapter](29-auditing-encounter-identity-threat-and-reward-placement.md) · [Chapter index](../README.md#chapters) · [Next chapter →](31-preparing-an-implementation-handoff.md)
