# 18. License boards, prices and purchase previews

[← Chapter index](../README.md#chapters)

Board position, license record, acquired-license state and the content granted by a license are separate data relationships.

## Trace a stock purchase

Start with one known native license. Follow selection, LP cost display, affordability, adjacency, purchase, ownership update and its actual grant. Follow the description and icon lookup separately. A string-table index is not necessarily the license ID or acquired-bit index.

On the reference executable, the menu path near `0x55F96F` calls `0x323600`; flags differ from another board-view route. Purchase/guard routines near `0x323910` and `0x323D10` provide additional entry points. Recover their arguments from native callers rather than using a guessed purchase prototype.

In the battle-record layout used by this path, LP is a DWORD at `+0x190` and license ownership data begins at `+0x194`. Establish the extent and mapping from native readers before editing it. This document supplies no alternative saved layout or class remapping.

## Decode grants without replacing their IDs

The PC license-record parser must first obtain each record's declared extent. In the record family used here, byte `+5` is a type discriminator. Some action-grant families use eight 16-bit values beginning at `+8`, with `0xFFFF` as an unused entry. Apply that interpretation only to types whose native consumers confirm it.

Preserve the distinction between a node that grants equipment access, an action, an augment or another license-dependent capability. Do not infer the grant type from the icon color or displayed name.

## Bit arithmetic is separate from mapping

Once the native bit index has been established, read it with explicit bounds:

```python
def acquired(bitmap, bit_index):
    if bit_index < 0 or bit_index >= len(bitmap) * 8:
        raise ValueError('license bit outside decoded bitmap')
    return bool(bitmap[bit_index // 8] & (1 << (bit_index % 8)))
```

This helper does not convert a license ID to a bit index. Recover that mapping before calling it. Writing a bit directly also omits native purchase side effects and should not stand in for the purchase path.

Keep owned-state checks separate from affordability. Preserve native board adjacency, unlock rules, job interactions and LP debit. A changed label or LP cost must agree across selection, help and purchase; translating a label must not change which license is acquired.

---

[← Previous chapter](17-native-save-boundaries.md) · [Chapter index](../README.md#chapters) · [Next chapter →](19-native-effect-assets.md)
