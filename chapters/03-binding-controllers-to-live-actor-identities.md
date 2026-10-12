# 03. Binding controllers to live actor identities

[← Chapter index](../README.md#chapters)

Separate operating-system input from the game entity that receives it. A controller index, party slot, actor handle and pointer are different identifiers.

## Sample an actual device

On Windows, `XInputGetState(index, &state)` reads one of the XInput user indices 0–3. A successful call supplies button bits, triggers and thumb-stick axes; a disconnected device must produce an unavailable state, not a fallback to another index. See Microsoft's [XInputGetState reference](https://learn.microsoft.com/en-us/windows/win32/api/xinput/nf-xinput-xinputgetstate).

Keep previous and current button masks to distinguish an edge from a held button:

```cpp
const unsigned pressed  = current & ~previous;
const unsigned released = previous & ~current;
const unsigned held     = current & previous;
```

Reset the previous mask when a device is disconnected or reassigned. Apply deadzones to analog axes before converting them into menu events. A repeat timer for menu navigation should be separate from analog movement.

SDL is an alternative input library, not an additional native game subsystem. If choosing it, use its documented device identity and event APIs for the selected SDL version. Do not merge SDL and XInput index numbers as if they identify the same device. Steam Input can change which virtual device the game sees; its effect must be established for the particular configuration, not prescribed as a universal on/off rule.

## Native actor resolution

For the reference executable, `0x31B7E0` accepts the 32-bit identity used by the native manual-command wrapper and returns a live actor or null. It first checks world readiness and delegates to native handle/object resolution. Its return value can cease to be valid after a scene transition.

Do not cache a pointer merely because the persistent character remains in the party. Resolve the handle again at the game-thread operation that uses it. Retain the full handle; a displayed name or party-list position does not replace it.

## Input ownership must be implemented

Vanilla has a native leader and native menu input. An independent input system must define which events it consumes and which reach that existing path. If it handles a Confirm edge, forwarding the same edge can trigger two actions. Keep title/load menus and modal dialogs under their own policy.

Keyboard bindings must be read from the actual game configuration and native interpretation. Do not hardcode Space, Backspace or controller face-button labels as universal meanings. Device discovery alone does not establish that gameplay routing or native command submission is working.

---

[← Previous chapter](02-moving-a-berserk-party-leader.md) · [Chapter index](../README.md#chapters) · [Next chapter →](04-independent-menus-with-native-command-execution.md)
