# 08. Camera state, collision and transitions

[← Chapter index](../README.md#chapters)

Camera changes require an identified native camera owner, a coordinate convention and a write point. There is no assumed external camera controller in this chapter.

## Find the active camera path

Start from native orbit, zoom or field-of-view changes and identify the data that reaches the scene's view/projection matrices. Distinguish an editable camera goal from the final collision-adjusted output. Writing a cached matrix can appear to work for one frame while the native update immediately replaces it.

Record the actual writer, its update thread, the lifetime of its containing object and the branch that selects scripted cameras. A complete native camera-controller ABI is not provided here. Do not apply a guessed matrix write as a universal camera hook.

## A complete, engine-independent smoothing calculation

For a scalar position component or distance, exponential smoothing can be calculated without a hidden helper:

```python
from math import exp

def smooth_value(current, goal, game_dt, time_constant):
    if game_dt <= 0:
        return current
    if time_constant <= 0:
        return goal
    weight = 1.0 - exp(-game_dt / time_constant)
    return current + (goal - current) * weight
```

Apply this independently to compatible position components. Handle angular wrap separately; interpolating 359° to 1° as ordinary scalars takes the long route. This calculation produces a desired value, not a native collision solution.

## Preserve scene behavior

If adding formation framing, compute the centre from eligible actor positions and choose distance from group extent and field of view. Reject stale positions and teleports before estimating velocity. Pass the goal through the recovered native collision path so walls, floors and ceilings still constrain the result.

Suspend game-time integration while a modal pause owns the scene. Retain the current goal and smoothing state when the world is unchanged. On resume, restart the elapsed-time measurement instead of accumulating wall-clock time spent paused.

For an actual area change, stop reading retired actors and camera objects. Reacquire the new scene and initialize its goal from current positions. If holding an outgoing rendered camera, retain values rather than pointers into the departing scene and release that hold when the native transition completes. These lifecycle rules must be implemented with the target build's actual transition signals.

---

[← Previous chapter](07-target-arrows-and-action-lines.md) · [Chapter index](../README.md#chapters) · [Next chapter →](09-rendering-huds-inside-the-game.md)
