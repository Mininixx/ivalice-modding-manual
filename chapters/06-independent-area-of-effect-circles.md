# 06. Independent area-of-effect circles

[← Chapter index](../README.md#chapters)

Area previews use another native object family and another list.

## Do not reuse the single-target-circle contract
The area controller uses the factory at **VA `0x2911D0`**, list append at `0x3F34D0`, and manager list field `+0x10F40`. Its owned objects carry distinct player tags (`AOP1`, `AOP2`, `AOP3`). Radius is supplied to the area factory; it is not inferred from the on-screen diameter of a single-target marker.

Native creation is dispatched on the UI thread. The dispatcher temporarily isolates the list, creates the requested object, restores the existing list and appends the owned object through the native operation. Preserve failure cleanup as carefully as the success path.

## Borrow settings without losing the user’s settings
Area rendering is controlled by bit 22 in the settings flags at `[0x215E6E0]+4`. The controller remembers whether that bit was already enabled. On release it removes only the enablement it introduced, retaining unrelated flags. If the settings object changes, release the old ownership before acquiring the new object.

---

[← Previous chapter](05-multiple-native-target-circles.md) · [Chapter index](../README.md#chapters) · [Next chapter →](07-target-arrows-and-action-lines.md)
