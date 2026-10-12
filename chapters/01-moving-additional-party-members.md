# 01. Moving additional party members

[← Chapter index](../README.md#chapters)

Movement work starts at the native movement consumer. The engine must remain responsible for collision, slopes, animation and navigation state.

## Native entry point

For the executable identified in [Address reference](30-native-addresses-and-hook-ownership.md), preferred VA `0x2E4380` begins with `40 53 56 41 56 48 83 EC 60`. It receives a context in `RCX` and an output address in `RDX`; the prologue clears the output. It reads the physics pointer from `context+0xB8`. Treat this as an internal function, not a public movement API.

The associated movement layout uses floating-point heading at physics `+0xA4` and magnitude at `+0xD0`. Context, actor and physics are different objects. Recover their relationship from the caller before writing either value. A character's persistent party record is not a physics object.

## Derive a direction without an external helper

The following pure Python calculation takes two horizontal camera basis vectors and a normalized input axis. It computes a desired direction; it does not access or modify the game.

```python
from math import atan2, hypot

def horizontal_intent(stick_x, stick_y, right_xz, forward_xz, deadzone=0.2):
    radius = hypot(stick_x, stick_y)
    if radius <= deadzone:
        return None, 0.0
    x = right_xz[0] * stick_x + forward_xz[0] * stick_y
    z = right_xz[1] * stick_x + forward_xz[1] * stick_y
    if hypot(x, z) == 0.0:
        return None, 0.0
    strength = min(1.0, (radius - deadzone) / (1.0 - deadzone))
    return atan2(x, z), strength
```

The angle convention and deadzone above are example choices. Establish axis signs, heading convention and magnitude units by following the native leader's input-to-movement path. Do not assume a normalized strength of 1.0 is a valid engine movement magnitude.

## Interception boundary

A new movement extension must select an eligible live actor before modifying the consumer's inputs. Preserve the original branch for other actors and modes. Apply changes on the native update path, with the instruction's live registers and flags preserved. Repeated world-position writes bypass collision and are a different operation.

Additional manual actors require new input ownership and arbitration with follower AI. Vanilla does not provide independent per-player command blocks. Define those in the extension being written; neither their storage nor a prebuilt controller is assumed here.

Stop using an actor when its scene or identity changes. Reacquire the physics object after a transition. This chapter does not define a complete follower-AI override; inspect turning, approach and idle decisions separately before claiming independent movement is complete.

---

[Chapter index](../README.md#chapters) · [Next chapter →](02-moving-a-berserk-party-leader.md)
