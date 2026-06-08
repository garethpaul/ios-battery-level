# Changes

## 2026-06-08

- Enabled battery monitoring before reading `UIDevice.batteryLevel`.
- Kept the battery-level read explicit without leaving an unused local warning.
- Added `make check` and a static iOS battery sample baseline for plist/storyboard XML, Xcode metadata, source inventory, and privacy guardrails.
- Documented the legacy Xcode project, local-only battery data expectations, and static verification workflow.
