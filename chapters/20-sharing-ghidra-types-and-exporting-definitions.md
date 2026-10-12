# 20. Sharing Ghidra types and exporting definitions

[← Chapter index](../README.md#chapters)

Separate reusable type definitions, program-specific analysis and recovered runtime behavior.

## Three different kinds of project object
A Ghidra project can contain imported programs, Version Tracking sessions and shared data-type archives. Each program also owns its own data types; creating a structure there does not automatically share it with other DLLs. Use a shared archive for structures and function definitions that really describe a common engine boundary.

Copying a structure into a shared archive brings its constituent types along. Check pointer widths, packing, calling conventions and conflicting names rather than assuming similarly named definitions are compatible. Version Tracking transfers must be reviewed and applied to the intended participating program; a comparison does not make both programs one database.

## Export small, meaningful surfaces
For a function catalog, export selected rows and columns from the Functions view to CSV. For shared types, export a C header from the data-type archive. Record the program fingerprint, image base and whether each address is a VA or RVA alongside it. Exporting an enormous decompilation is rarely the best handoff.

For the FFX `gMagicFunctions` table at **RVA `0x00864CE8`**, keep the 32-bit pointer-table representation separate from function signatures. A 741-pointer prefix occupies `0xB94` bytes; neither a label nor a pointer establishes a callable C prototype.

```c
// A recovered 32-bit address is data until its ABI has been verified.
uint32_t engine_api_entry;
// Do not replace it with a guessed function-pointer signature.
```

For each callback that a port needs, inspect its callers, arguments, stack cleanup, return value, ownership and side effects. Write down which meaning is observed in machine code and which remains an inference. A header helps reuse analysis; it cannot supply the host engine that an effect DLL expects.

---

[← Previous chapter](19-extracting-effects-from-final-fantasy-x.md) · [Chapter index](../README.md#chapters) · [Next chapter →](21-recovering-particle-programs-and-their-timeline.md)
