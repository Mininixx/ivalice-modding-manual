# 14. Native damage modifiers and debuffs

[← Chapter index](../README.md#chapters)

A native debuff can affect a stat, a damage formula, a status bit or a target eligibility rule. These mechanisms should not be treated as interchangeable.

## Identify the actual operand

Trace the native action that applies the debuff, then locate the next calculation that consumes the affected value. Determine whether the stored value belongs to persistent character data, a live battle record or a temporary calculation. Record its width, signedness, range and reset point.

For example, reducing an attack stat by 25 percent need not reduce final damage by 25 percent. A nonlinear formula, defense subtraction, rounding and damage caps can change the result. Describe the real operation rather than assigning a percentage from the effect's name.

## Modify at the intended boundary

If the goal is a final-damage modifier, preserve the original result calculation and alter only the relevant result family. If the goal is a stat debuff, preserve the native stat's limits and stacking rules. Do not edit a shared enemy template to apply a temporary effect to one live enemy.

A new temporary modifier needs storage implemented by the new extension. Its identity should include the native actor handle and scene lifetime; its data should include the modifier family, value, expiry rule and stacking policy. None of that storage exists merely because a native status is visible.

## Count the correct event

An area action may produce one result per target. A “next action” rule must be consumed at the action boundary, while a “next hit” rule may be consumed per accepted hit. Use the native action identity or its owning execution object, not a timer that guesses when an animation should finish.

Remove transient records when actors retire or their scene ends. A reused pointer must not inherit the previous enemy's modifier. Keep such runtime state outside vanilla save records unless a fully specified persistence mechanism is separately implemented.

This chapter intentionally assigns no new ability IDs, damage multipliers or class rules. Recover the stock action's calculation before extending it.

---

[← Previous chapter](13-damage-status-results-and-enemy-reaction.md) · [Chapter index](../README.md#chapters) · [Next chapter →](15-native-status-and-revival-lifetimes.md)
