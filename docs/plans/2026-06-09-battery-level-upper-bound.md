# Battery Level Upper Bound

status: completed

## Context

`UIDevice.batteryLevel` is documented as a percentage-like value between `0.0`
and `1.0`, with negative values representing an unknown level. The helper
already returns `nil` for unknown negative values; it should also reject values
above `1.0` so impossible readings are not treated as valid percentages.

## Objectives

- Return `nil` for battery levels greater than `1.0`.
- Preserve valid battery levels in the documented range.
- Add XCTest coverage for full and out-of-range battery normalization.
- Extend the static baseline and docs to capture the upper-bound guard.

## Verification

- `make check`
- `git diff --check`
