# Unknown Battery Level Plan

status: completed

## Context

`UIDevice.batteryLevel` returns a negative value when the current battery level is
unknown. Returning that sentinel as a percentage makes the sample contract less
clear and can encourage callers to treat unavailable device state as real data.

## Objectives

- Return an optional battery level from the read helper.
- Normalize unknown negative battery levels to `nil`.
- Replace generated XCTest placeholders with assertions for unknown and known
  battery-level values.
- Keep `batteryMonitoringEnabled` restoration tied to `defer`.
- Extend the static baseline so the optional normalization and testability
  wiring remain visible on hosts without Xcode.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
