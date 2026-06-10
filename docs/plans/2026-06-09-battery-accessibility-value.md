# Battery Accessibility Value

status: completed

## Context

The sample displays the normalized battery level in a local label and sets a
static accessibility label of `Battery Level`. Because the static label does
not include the current percentage or unknown state, assistive technologies need
a separate accessibility value for the current reading.

## Completed Scope

- Added `batteryLevelAccessibilityValue(_:)` for known percentages and unknown
  readings.
- Updated the visible label display path to set `accessibilityValue` alongside
  the text.
- Added XCTest source coverage for known, zero, and unknown accessibility
  values.
- Extended the static baseline and docs so the visible local reading remains
  accessible without adding logging or persistence.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
