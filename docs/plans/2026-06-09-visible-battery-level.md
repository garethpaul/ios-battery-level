# Visible Battery Level

status: completed

## Context

The sample read and normalized `UIDevice.batteryLevel`, but it discarded the
result in `viewDidLoad`. That kept the API example present while leaving the app
without an observable result.

## Completed Scope

- Added a local label for the sampled battery level.
- Added a small formatter for known percentages and unknown readings.
- Kept unknown, non-finite, out-of-range, zero, and full battery normalization
  behavior unchanged.
- Added XCTest coverage for the visible battery text contract.
- Extended the static baseline and docs so the sample keeps an observable,
  local-only display path.

## Verification

- `make check`
- `git diff --check`
