# Battery Presentation Normalization

status: planned

## Context

Device reads are normalized before display, but the text and accessibility
formatters accept optional raw floats directly. A future caller can bypass the
read helper and expose impossible values such as `150%` or `nan%` instead of the
existing unknown state.

## Scope

- Normalize non-nil battery values inside both presentation formatters.
- Preserve valid zero, partial, and full percentages.
- Return the existing visible and accessibility unknown strings for invalid,
  out-of-range, or non-finite values.
- Add XCTest and static baseline coverage for both presentation paths.

## Verification

- `make check`
- `git diff --check`
- Mutations bypassing formatter normalization must fail the baseline.
- Hosted macOS validation must execute the ChargeMe XCTest suite.
