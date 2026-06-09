# Non-Finite Battery Level Guard

status: completed

## Context

`normalizedBatteryLevel(_:)` rejected negative unknown values and values above
`1.0`, but separate comparisons can still let `NaN` through because all direct
comparisons with `NaN` return false. Non-finite values should be treated as
absent device state rather than a usable percentage.

## Objectives

- Reject non-finite battery levels such as `NaN`.
- Preserve valid `0.0...1.0` battery levels.
- Keep unknown negative and above-range values returning `nil`.
- Extend the static baseline and XCTest source coverage for the normalization
  boundary.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- `git diff --check`
