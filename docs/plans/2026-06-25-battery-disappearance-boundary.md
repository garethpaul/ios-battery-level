# Battery Disappearance Transition Boundary

status: completed

## Problem

The controller retained battery and application-active observers until
`viewDidDisappear`. During the disappearance transition, callbacks could still
read local device state and update a view that was already leaving the visible
screen.

## Design

- Stop battery updates in `viewWillDisappear` before delegating the lifecycle
  callback to UIKit.
- Preserve the existing generation invalidation, exact observer removal, and
  prior monitoring-state restoration order.
- Re-establish observation through the existing idempotent `viewWillAppear`
  path if an interactive transition is cancelled.
- Add focused XCTest coverage that posts a battery notification after
  `viewWillDisappear` and proves the reading, label, accessibility value, and
  monitoring state remain unchanged.

## Test-First Evidence

- RED: the portable source gate failed because no `viewWillDisappear` teardown
  boundary existed; local `xcodebuild was unavailable` for executing XCTest.
- GREEN: the source gate requires stop-before-super ordering and discovers the
  focused transition-start XCTest.

## Verification Completed

- Root and external-directory Make gates passed.
- Python checker compilation and shell syntax passed.
- The late-teardown method, reversed lifecycle ordering, and missing focused
  XCTest each failed an isolated copy; three hostile transition mutations were rejected.
- `git diff --check` and generated-artifact checks passed.
- Local xcodebuild was unavailable; no local simulator or physical-device
  execution is claimed, and hosted XCTest remains mandatory on the exact head.

## Runtime Boundary

Device transition animation, interactive cancellation, and notification timing
remain part of exact-commit simulator or device verification rather than the
portable source contract.
