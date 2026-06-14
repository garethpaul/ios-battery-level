# Stale Battery Notification Guard

status: planned

## Context

The controller removes its battery-level observer when the view disappears,
but a callback already queued on `OperationQueue.main` can still run after
teardown. If a later appearance installs a new observer before that callback
runs, token presence alone also cannot distinguish the old lifecycle from the
new one.

## Priority

This is a narrow asynchronous lifecycle race. A stale callback should never
refresh a hidden view or act on behalf of a later appearance generation.

## Scope

1. Assign a monotonically increasing generation to each visible battery-update
   lifecycle.
2. Capture that generation when installing the observer and accept callbacks
   only while the same generation remains active.
3. Invalidate the active generation during teardown before restoring battery
   monitoring state.
4. Add deterministic XCTest and static contracts that reject stale callbacks
   without changing production notification delivery or monitoring ownership.
5. Synchronize maintenance, privacy, and lifecycle guidance.

## Verification Plan

- Run all four Make gates from the checkout and the absolute Makefile check
  from an external directory.
- Run checker compilation and XCTest runner shell syntax.
- Reject mutations that remove generation increment, capture, callback guard,
  teardown invalidation, or test coverage.
- Inspect the exact diff, generated artifacts, changed lines for credentials,
  and preservation of project/workflow/scheme/runner files.

## Risk And Rollback

The guard only suppresses callbacks from inactive lifecycle generations.
Rollback restores token-only callback acceptance; no persisted data, network,
or physical-device setting is otherwise changed.

## Work Completed

Pending implementation.

## Verification Completed

Pending implementation and exact evidence.
