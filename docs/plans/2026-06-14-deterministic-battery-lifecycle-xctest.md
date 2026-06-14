# Make Battery Lifecycle XCTest Deterministic

status: completed

## Context

Both hosted macOS events failed the same lifecycle test at exact head
`706b29fa46a7eabbaa55a085ad0ef90b99185b73`. The test directly mutated
process-global `UIDevice.current` monitoring state, and the notification test
spent about 61 seconds crossing to `OperationQueue.main` from the test runner.

## Requirements

- R1. Preserve production `UIDevice.current` monitoring and main-queue callback
  behavior.
- R2. Let XCTest own deterministic, controller-local monitoring state.
- R3. Let the test subclass receive battery notifications synchronously.
- R4. Preserve observer idempotence, teardown, prior-state restoration, visible
  and accessibility refresh assertions, and hosted XCTest coverage.
- R5. Record old-head failures and new-head verification truthfully.

## Scope Boundaries

- Do not remove, skip, filter, retry, or weaken any XCTest.
- Do not change workflow triggers, runner, timeout, signing, project, or scheme
  configuration.
- Do not claim local Xcode execution on Linux.

## Implementation

- Add overridable controller seams for monitoring reads/writes and notification
  queue selection.
- Keep production seam implementations backed by `UIDevice.current` and
  `OperationQueue.main`.
- Override the seams in the test subclass with local state and synchronous
  notification delivery.
- Strengthen static contracts for both production and test implementations.

## Verification

- Run focused static validation plus root and external-directory `make check`.
- Reject hostile mutations that reconnect tests to global state, remove the
  synchronous test queue, or weaken production semantics.
- Audit the exact diff, generated artifacts, project/workflow preservation, and
  credential-like additions before committing.
- Require both canonical hosted macOS events to succeed at the new exact head.

## Work Completed

- Added overridable monitoring read/write and notification-queue seams to the
  controller while keeping production implementations on `UIDevice.current`
  and `OperationQueue.main`.
- Moved XCTest monitoring state into the test subclass and made only the test
  notification delivery synchronous.
- Preserved all lifecycle, observer identity, teardown, prior-state,
  presentation, workflow, project, and scheme coverage.

## Verification Completed

- Both old-head hosted macOS events failed at
  `706b29fa46a7eabbaa55a085ad0ef90b99185b73`, with the monitoring lifecycle
  test failing and the notification test taking about 61 seconds.
- The focused static gate plus root and external-directory `make check` passed;
  xcodebuild remains unavailable on Linux, so no local XCTest run is claimed.
- All six isolated hostile mutations were rejected across production
  monitoring, main-queue delivery, local test state, synchronous test delivery,
  documentation, and completed plan evidence.
- Exact-path diff, project/workflow/scheme preservation, generated-artifact,
  whitespace, shell, Python, and credential-like addition audits passed.
- Both canonical hosted macOS events remain required on the new exact head
  before terminal success is recorded.
