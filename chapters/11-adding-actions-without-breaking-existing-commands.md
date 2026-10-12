# 11. Adding actions without breaking existing commands

[← Chapter index](../README.md#chapters)

An Action record, a menu row and an effect resource are separate native objects. Editing one does not automatically extend the others.

## Read the native pack directory

The PC `battle_pack.bin` begins with a little-endian DWORD section count followed by that many DWORD section offsets. The directory identifies section boundaries; it is not the Action-record array itself. In the layout discussed here, section 14 contains Actions and section 13 contains equipment. Parse the selected section's own header before indexing records.

This standard-library example lists section spans without changing the file:

```python
import struct

def section_spans(data):
    if len(data) < 4:
        raise ValueError('missing section count')
    count = struct.unpack_from('<I', data)[0]
    end = 4 + 4 * count
    if count == 0 or end > len(data):
        raise ValueError('invalid directory')
    offsets = list(struct.unpack_from(f'<{count}I', data, 4))
    if any(x < end or x > len(data) for x in offsets):
        raise ValueError('section offset out of range')
    if offsets != sorted(offsets):
        raise ValueError('unexpected section order')
    return list(zip(offsets, offsets[1:] + [len(data)]))
```

If a different file variant uses a sentinel or another directory convention, reject it and identify that convention instead of forcing the parser to continue.

## Preserve field meaning

For a decoded Action record in this PC layout, useful fields include byte `+0x09` for charge, byte `+0x0A` for MP cost, byte `+0x1E` for menu category, and the 16-bit content reference at `+0x22`. The name reference at `+0x34` must be resolved through the corresponding text data. Keep unknown bytes unchanged.

Use a native Action of the same behavioral family as the starting point for an edit. A physical attack and a spell can use different native calculation and animation paths even when their visible effects look similar. Do not zero unknown signed fields when cloning a record.

## Adding records requires consumer analysis

Derive the current record count from the pack header. Search executable readers and tables for bounds, index widths, category buffers and effect dispatch. A 16-bit field does not prove that every 16-bit value is executable. There is no single number that describes all Action, effect, text and UI limits.

Before allocating a new record, inventory references from menus, licenses, enemy actions, scripts and effect tables. An unused label is not proof that an ID is free. Keep an explicit allocation list in the new project's own format and compare existing records byte-for-byte when rebuilding.

The native stock Attack ID is `0x96` in the command path documented in [Chapter 04](04-independent-menus-with-native-command-execution.md). Preserve its native behavior when using it to understand weapon-based execution. No extended Action table or preallocated custom ID set is assumed here.

---

[← Previous chapter](10-area-changes-interaction-and-state-retirement.md) · [Chapter index](../README.md#chapters) · [Next chapter →](12-queueing-commands-on-the-game-thread.md)
