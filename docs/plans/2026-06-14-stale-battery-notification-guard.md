# Stale Battery Notification Guard

status: completed

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

- Added a monotonic battery-update generation that is captured when the
  observer is installed and invalidated before teardown.
- Routed notification refresh through an active-generation predicate so stale
  queued callbacks cannot read or display battery state.
- Added deterministic XCTest coverage, mutation-sensitive static contracts,
  and synchronized lifecycle and privacy guidance.

## Verification Completed

- All four Make gates passed in an isolated completed-plan preflight copy and
  again in the implementation worktree.
- The absolute Makefile check passed from an external directory.
- `python3 -m py_compile scripts/check-baseline.py` passed; its exact generated
  bytecode path was removed before the final artifact audit.
- `sh -n scripts/run-tests.sh` passed.
- Five isolated hostile mutations were rejected: removing the start increment,
  generation capture, callback guard, teardown invalidation, or XCTest
  discovery each failed the maintained baseline.
- `git diff --check` passed, along with exact intended-path, generated-artifact,
  changed-line credential, privacy, dependency, project, workflow, scheme, and
  runner-preservation audits.
- Local `xcodebuild was unavailable`; no local XCTest execution is claimed.
