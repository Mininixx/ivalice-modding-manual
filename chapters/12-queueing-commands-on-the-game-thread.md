# 12. Queueing commands on the game thread

[← Chapter index](../README.md#chapters)

Read real consumer occupancy and preserve the intended replacement semantics.

## One pending manual order per member
The implemented native queue (`irfq`) keeps one pending manual request for each member. A newer request replaces that member’s pending request. This is an explicit semantic choice; it is not a ring that guarantees an execution for every button press.

Delivery observes the actor’s current action, command mailbox and published resource-consumer mailbox. Do not guess completion from a timer in the external frontend. A prefetched resource remains owned until the game acknowledges the lease’s cleanup, not merely until a host function returns.

## Distinguish queued admission from execution readiness
Native validation at `0x317BC0` calls `0x2FFCF0`. During wait-mode pause (`0x253B90`), the inner validator returns reason **`0x24`** and the outer state is **1**, rather than execution-ready state 3.

Accept only that particular “paused, wait” combination into the queue. The game still waits for pause to clear and repeats full native validation before execution. It does not broadly treat every rejection as permission.

## Payment must survive validation
Use an authenticated paid receipt tied to owner, target, generation and area so spending the final charge cannot invalidate the same paid order later. A paid order may execute; another order still needs its own charge.

```text
selected → admitted → waiting for native consumer → delivered → completed
                   ↘ replaced / invalidated / cancelled
```

Validate payment at the actual charging boundary. Do not debit again at impact, and do not let an old receipt authorize another action. Retire the receipt on replacement, cancellation, death, actor recycling or scene/save invalidation.

## Preserve Mix and stealing receipts
Mix owns dynamic Action/effect leases; retain their admission, ingredient payment, cancel/refund and result cleanup. Keep recipe construction out of menu-label logic. Transmuter's charge policy uses its class-local fractional accumulation; the 30 percent gain increase uses numerator 130 with denominator 16, without changing other classes.

Pockets is a Transmuter-specific interpretation of shared Action 169. Preserve ordinary Steal for other owners. On the first valid Pockets use against an eligible enemy, guarantee one available item from its native steal table (blue) plus two rewards from the Mega Pockets pool (yellow). If ordinary Steal already exhausted the native table, award only the two extras. A repeated Pockets use on that enemy fails.

Tie the Pockets receipt to the enemy's live identity, generation and scene, shared across players; retire it with that enemy lifecycle. Do not mistake a recycled pointer for an already robbed enemy. Preserve the action's reserved cast bit 16. Mega Pockets remains independent: always ten item units even after previous steals, with at most five distinct item types. Aggregate repeated rewards rather than letting ten different labels overflow the screen.

---

[← Previous chapter](11-adding-actions-without-breaking-existing-commands.md) · [Chapter index](../README.md#chapters) · [Next chapter →](13-damage-status-results-and-enemy-reaction.md)
