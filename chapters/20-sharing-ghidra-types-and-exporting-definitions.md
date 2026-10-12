# 20. Sharing Ghidra types and exporting definitions

[← Chapter index](../README.md#chapters)

A useful reverse-engineering handoff includes the binary identity, types, calling conventions and the evidence behind each recovered field.

## Import the intended binary

In Ghidra, create a project and import the exact executable or DLL being studied. Check the detected architecture, compiler specification and image base before analysis. Preserve a SHA-256 fingerprint of that input so addresses cannot silently move to a different build.

Follow the official [Introduction to Ghidra](https://ghidra.re/ghidra_docs/GhidraClass/Beginner/Introduction_to_Ghidra_Student_Guide.html) for the import and analysis workflow. Imported programs and shared data-type archives serve different purposes: the program stores its analysis, while an archive can share reusable structures across programs.

## Recover a type from its consumers

For a candidate field, record access width, signedness, alignment, read/write sites and object lifetime. A decompiler-generated `longlong` is not automatically a pointer, and a repeated offset does not prove that two objects have the same structure.

Use explicit-width types when the machine access establishes the width. Leave unknown bytes represented as padding or undecoded storage. Do not name unknown fields after the feature you hope they implement.

For a function, inspect multiple callers. Establish which registers or stack slots carry arguments, which registers are live across the call, and whether a returned pointer is borrowed or owned. A function-pointer typedef must reflect that work; a label alone is not a prototype.

## Export small, reusable definitions

Export selected types as a C header and retain the program fingerprint and address convention alongside it. Export a function/address table with columns for preferred VA, RVA, proposed signature and confidence. A header should distinguish confirmed fields from hypotheses.

Do not copy a complete decompilation when a short structure and its relevant callers explain the contract. Conversely, do not distribute a wrapper name without the contract needed to replace it.

Version Tracking can help transfer analysis between binary revisions, but review the matches before applying them. Shared names do not prove shared semantics or byte-compatible layouts.

---

[← Previous chapter](19-native-effect-assets.md) · [Chapter index](../README.md#chapters) · [Next chapter →](21-native-effect-timelines.md)
