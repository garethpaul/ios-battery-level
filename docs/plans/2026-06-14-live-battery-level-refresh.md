# Live Battery Level Refresh

status: completed

## Summary

Refresh the displayed and accessible battery percentage when iOS reports a battery-level change while the screen remains visible. Scope monitoring and notification observation to the visible view lifecycle.

## Problem Frame

The controller refreshes in `viewWillAppear`, but it does not observe `UIDevice.batteryLevelDidChangeNotification`. A level change while the view remains onscreen therefore leaves both the label text and accessibility value stale until the view disappears and reappears.

## Requirements

- **R1:** A battery-level notification while the view is visible must refresh both visible and accessibility values.
- **R2:** The controller must register at most one observer and remove it when the view disappears.
- **R3:** Battery monitoring must be enabled while observing and restored to its prior setting afterward.
- **R4:** Existing unknown, zero, full, invalid, and appearance-refresh behavior must remain covered.
- **R5:** Verification must record unavailable physical-device coverage truthfully.

## Key Technical Decisions

- **Visible-lifecycle ownership:** Start monitoring and observation in `viewWillAppear`; stop and restore state in `viewDidDisappear`.
- **Token-based observer identity:** Store the notification token so repeated lifecycle calls cannot create duplicate callbacks and teardown removes the exact registration.
- **Existing read seam:** Route notification callbacks through `readBatteryLevel()` and `displayBatteryLevel(_:)` so deterministic XCTest stubs continue to cover rendering.

## Implementation Units

### U1: Add bounded battery observation

**Files:**
- `ChargeMe/ViewController.swift`

Add idempotent start/stop helpers, retain the notification token and prior monitoring state, refresh immediately on appearance, refresh on battery-level notifications, and restore state on disappearance.

### U2: Add lifecycle-sensitive XCTest coverage

**Files:**
- `ChargeMeTests/ChargeMeTests.swift`
- `scripts/check-baseline.py`

Cover notification refresh, duplicate-registration resistance, teardown behavior, and the required monitoring/observer ordering with executable and mutation-sensitive static contracts.

### U3: Record completed evidence

**Files:**
- `docs/plans/2026-06-14-live-battery-level-refresh.md`
- `CHANGES.md`
- `SECURITY.md`
- `VISION.md`
- `AGENTS.md`

Record the lifecycle invariant, actual validation, skipped physical-device coverage, and completed plan status.

## Validation

- Run `make check`, `make lint`, `make test`, and `make build` from the checkout.
- Run `make check` through the absolute Makefile path from `/tmp`.
- Reject isolated mutations that remove monitoring enablement, observer identity, notification refresh, teardown, prior-state restoration, or test coverage.
- Audit the exact intended diff for whitespace, conflicts, generated artifacts, signing material, and credential patterns.

## Verification Results

- `make check`, `make lint`, `make test`, and `make build` passed the maintained static baseline; xcodebuild was unavailable on this Linux host, so local XCTest was explicitly skipped.
- The external `make -f /absolute/path/to/Makefile check` gate passed from `/tmp`.
- All six isolated hostile mutations were rejected when they removed observer idempotence, monitoring enablement, observer-token assignment, notification refresh, lifecycle teardown, or prior-state restoration.
- No battery or device state was logged, persisted, uploaded, or sent over a network.
- Physical-device battery notification behavior remains unverified and is not claimed.

## Risks

- Linux cannot execute Xcode or observe physical battery changes; hosted macOS XCTest and later device verification remain required.
- Notification delivery depends on monitoring being enabled before observer-driven updates, so ordering is part of the maintained contract.

## Hosted XCTest Follow-Up

- Both exact-head macOS jobs exposed a deterministic-test defect: the lifecycle
  test mutated process-global `UIDevice.current` monitoring state, while the
  notification test routed through the simulator main queue and took about 61
  seconds.
- Production still uses `UIDevice.current` and `OperationQueue.main`; narrow
  overridable seams let the XCTest stub own local monitoring state and
  synchronous notification delivery.
- The focused static gate, root and external-directory `make check`, and six
  follow-up hostile mutations passed. Hosted macOS XCTest remains required on
  the new exact head and is not claimed complete until both canonical events
  succeed.
