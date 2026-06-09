# Zero Battery Level Boundary

status: completed

## Context

`UIDevice.batteryLevel` uses values between `0.0` and `1.0` for known battery
percentages. The helper already rejects unknown, non-finite, and out-of-range
values; the lower valid boundary should also stay explicit so `0.0` is not
confused with the unknown negative sentinel.

## Completed Scope

- Added an XCTest assertion for `normalizedBatteryLevel(0.0)`.
- Extended the static baseline so the zero battery-level boundary remains
  covered by checked-in tests.
- Updated project docs to describe zero-level preservation alongside unknown,
  non-finite, and out-of-range normalization.

## Verification

- `make check`
- `git diff --check`
