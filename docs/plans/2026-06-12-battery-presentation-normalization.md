# Battery Presentation Normalization

status: completed

## Context

Device reads are normalized before display, but the text and accessibility
formatters accept optional raw floats directly. A future caller can bypass the
read helper and expose impossible values such as `150%` or `nan%` instead of the
existing unknown state.

## Work Completed

- Normalize non-nil battery values inside both presentation formatters.
- Preserve valid zero, partial, and full percentages.
- Return the existing visible and accessibility unknown strings for invalid,
  out-of-range, or non-finite values.
- Add XCTest and static baseline coverage for both presentation paths.

## Verification Completed

- Local `make check`, `make lint`, `make test`, and `make build` passed. The
  local environment did not provide `xcodebuild`, so `make test` completed the
  static baseline and reported that XCTest requires the hosted macOS runner.
- `python3 -m py_compile scripts/check-baseline.py`,
  `sh -n scripts/run-tests.sh`, and `git diff --check` passed.
- Hostile mutations changing the plan status, inserting an unfinished-work
  marker, falsifying a run ID, or bypassing either formatter's normalization
  call were rejected by the baseline.
- The implementation push Check run `27394507895` completed successfully for
  commit `287335f16f78525ddbb899b0f7119bc7ab1555e3`.
- The implementation pull-request Check run `27394511486` completed
  successfully for commit `287335f16f78525ddbb899b0f7119bc7ab1555e3` and
  executed the ChargeMe XCTest suite on hosted macOS.
- The post-merge push Check run `27394736468` completed successfully for
  commit `7dce00c264c429756336d5bc37d8d5f79513609f`.
- The CodeQL setup run `27402322921` completed successfully for commit
  `7dce00c264c429756336d5bc37d8d5f79513609f`.
- Both presentation formatters preserve
  `let normalizedLevel = normalizedBatteryLevel(batteryLevel)` before
  converting the normalized value to a percentage.
