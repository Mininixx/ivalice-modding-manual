# 31. Preparing an implementation handoff

[← Chapter index](../README.md#chapters)

Give the next developer or AI a concrete native contract and the source needed to implement it. A descriptive helper name is not an implementation.

## Establish the vanilla baseline

Identify the executable by hash and record the relevant game-data hashes. State which stock behavior is being changed and which native behavior must remain. Provide accessible source files for any new extension code; do not refer to an unpublished directory or a DLL whose interface is unspecified.

For each native function call, give the address convention, supported binary, parameter widths, calling convention, return meaning, required thread and object lifetimes. For each binary edit, give the containing format, record identity and byte range.

## Separate native facts from new design

Mark an observed instruction or decoded native field as such. Mark a reconstructed prototype as reconstructed. Mark a proposed queue, renderer, serializer or controller as code still to implement unless its complete source is supplied.

A useful unresolved item is specific: “the factory's third argument and destructor ownership are not recovered.” “Use the native helper” hides the same missing information and is not an actionable substitute.

Keep unknown layout bytes and unclassified return states unchanged. Do not create an imaginary API to make an example look complete. Use public documentation for platform APIs and link any real external library explicitly, with its applicable version and license.

## Copyable implementation brief

```text
Requested change and native triggering action:
Executable filename, SHA-256 and preferred image base:
Relevant game-data files and hashes:
Native function/record boundaries and address convention:
Original bytes or decoded field definitions:
Parameters, return values, thread and object lifetimes:
Native behavior to preserve:
New code to implement, with its inputs and outputs:
Actual public dependencies, if any:
Unresolved ABI/layout questions:
Cancellation, scene transition and teardown behavior:
Installation files and rollback preimages:
```

Give the assistant the relevant chapter links and actual input files. Keep runtime investigation, game launches, save operations and publication within the user's authorized scope. Documentation work by itself does not require changing an installation or a save.

---

[← Previous chapter](30-native-addresses-and-hook-ownership.md) · [Chapter index](../README.md#chapters)
