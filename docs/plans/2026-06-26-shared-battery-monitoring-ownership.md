# Shared Battery Monitoring Ownership

status: completed

## Problem

`UIDevice.current.isBatteryMonitoringEnabled` is process-global, but each visible
`ViewController` captured and restored it independently. With two overlapping
controllers, the first disappearance restored monitoring to `false` while the
second controller was still visible. The final disappearance then restored the
intermediate `true` state instead of the process state from before either owner.

## Design

- Give each controller an idempotent reference to its exact lease coordinator.
- Share a process-wide visible-owner count and the monitoring state captured by
  the first owner.
- Keep that count in an injectable coordinator: production controllers share
  one coordinator, while parallel XCTest cases use isolated coordinators.
- Enable monitoring only on the first acquisition.
- Remove exact observers before releasing a controller's lease.
- Restore the original monitoring state only after the final lease is released.

## Test-First Evidence

- RED: the portable baseline rejected the overlapping-controller XCTest because
  no shared battery-monitoring ownership existed.
- GREEN: static source contracts require first-acquire and last-release ordering.
- Hosted XCTest remains the executable authority for the overlapping lifecycle.
- The first hosted run exposed cross-test interference from a static test
  fixture; coordinator injection preserves production sharing without leaking
  ownership across parallel XCTest probes.

## Verification

- The focused XCTest shares one monitoring probe between two controllers and
  proves the first disappearance keeps monitoring enabled while the final
  disappearance restores the original disabled state.
- Isolated mutations reject premature final-owner restoration, release before
  exact-ownership detachment, and an overlap test that uses isolated coordinators.
