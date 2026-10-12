# 12. Queueing commands on the game thread

[← Chapter index](../README.md#chapters)

The native request is a transition into the game's action state machine. A frontend request, a queued native command and a completed action are different events.

## Native request fields

The per-actor submission routine and its call contract are documented in [Chapter 04](04-independent-menus-with-native-command-execution.md). Its ordinary path writes a 16-bit Action ID to actor `+0xBA0`, a 32-bit target to `+0xBB8`, sets bit `0x8000` in the WORD at `+0xBA4`, and sets `0x4000` in the QWORD at actor `+0`.

Do not implement submission by copying these writes alone. The native routine performs status checks, special-action bookkeeping and an additional call to `0x317E60`.

Follow readers of the request fields to identify when the request moves into the current action. The current-action field at actor `+0x714` is separate from the request field. Determine whether a native request replaces charging, waits for an executing action or is rejected by following those consumers; the submission return value is insufficient.

## A queue owned by a new frontend

If input arrives outside the game thread, implement a small queue of value-only requests. A minimal request contains a sequence number, issuer handle, target handle, Action ID and the frontend's scene revision. Do not enqueue raw actor pointers for later use.

Choose queue semantics explicitly: FIFO, one pending request per issuer, or reject while busy. Those are extension decisions. Do not describe a custom queue as a vanilla service.

At the native update boundary, remove a request under synchronization, release the lock, resolve its current handles, compare scene revision and run native validation. A request that became stale must be discarded. Never invoke engine callbacks while holding an input-thread lock.

## Readiness and payment

`0x317BC0` reports availability and a reason, but it does not replace the native execution state machine. A paused game can report that an otherwise meaningful command is not currently executable. Preserve that distinction instead of converting all rejections into queued success.

Leave MP/item consumption with the native path when submitting stock commands. Retrying after an ambiguous return can submit the same action twice. Track request identity and consumption before deciding to retry. On scene retirement, drop frontend requests whose handles came from the previous scene.

---

[← Previous chapter](11-adding-actions-without-breaking-existing-commands.md) · [Chapter index](../README.md#chapters) · [Next chapter →](13-damage-status-results-and-enemy-reaction.md)
