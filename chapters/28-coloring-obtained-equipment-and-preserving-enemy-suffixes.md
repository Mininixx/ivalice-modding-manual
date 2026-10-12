# 28. Coloring obtained equipment and preserving enemy suffixes

[← Chapter index](../README.md#chapters)

Native display strings contain identity, localization and formatting rules. Treat them as structured UI output rather than raw English text.

## Follow the acquisition formatter

Start from a stock item-acquisition message and trace the formatter that receives its item identity and quantity. Identify the category, lookup table, localized grammar and any native color controls. Prefer modifying the formatting stage to rewriting item names globally.

The reference executable's formatting investigation includes instruction site `0x536C0B` and functions around `0x263A10`, `0x272CE0`, `0x24ABE0` and `0x2B58F0`. Recover the specific call path and arguments for the intended message; this list is not a set of interchangeable text APIs.

Preserve quantity, articles, pluralization and the formatter's termination/reset behavior. A combat-log string and an inventory label can use different paths. Decode the game's character/control encoding before inserting bytes; ordinary UTF-8 or terminal escape codes are not automatically accepted.

## Native enemy suffixes

In the native enemy-name path, the signed field at `BWEI+0x102` controls a branch that reads the 16-bit instance value at `+0x100`. For the eligible branch, a zero instance has no suffix; positive values wrap over 26 letters:

```python
def instance_suffix(instance):
    if instance < 0:
        raise ValueError('expected an unsigned instance value')
    return '' if instance == 0 else chr(ord('A') + (instance - 1) % 26)
```

This formula does not implement the preceding native eligibility branch or locate BWEI. Recover those from the native caller before applying it to an actor.

Display letters can repeat: 27 maps to A. Never use a formatted name or its suffix to identify a target. Commands and results require the full live handle independently of what the UI displays.

---

[← Previous chapter](27-creating-convincing-weapon-surfaces-without-changing-geometry.md) · [Chapter index](../README.md#chapters) · [Next chapter →](29-encounter-identity-and-reward-placement.md)
