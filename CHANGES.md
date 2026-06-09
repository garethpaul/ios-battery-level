# Changes

## 2026-06-09

- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static battery sample baseline.
- Added a zero battery-level boundary assertion so `0.0` remains a valid
  normalized percentage.

## 2026-06-08

- Enabled battery monitoring before reading `UIDevice.batteryLevel`.
- Added a focused battery read helper that restores the previous monitoring state after reading.
- Switched the helper to `defer` so battery monitoring restoration remains tied to helper scope.
- Normalized unknown negative battery levels to `nil` before returning from the helper.
- Normalized out-of-range battery levels above 100% to `nil`.
- Normalized non-finite battery levels to `nil`.
- Replaced generated XCTest placeholders with battery-level normalization assertions.
- Kept the battery-level read explicit through the helper return value.
- Added `make check` and a static iOS battery sample baseline for plist/storyboard XML, Xcode metadata, source inventory, and privacy guardrails.
- Documented the legacy Xcode project, local-only battery data expectations, and static verification workflow.
