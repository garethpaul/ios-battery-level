# Changes

## 2026-06-08

- Enabled battery monitoring before reading `UIDevice.batteryLevel`.
- Added a focused battery read helper that restores the previous monitoring state after reading.
- Kept the battery-level read explicit through the helper return value.
- Added `make check` and a static iOS battery sample baseline for plist/storyboard XML, Xcode metadata, source inventory, and privacy guardrails.
- Documented the legacy Xcode project, local-only battery data expectations, and static verification workflow.
