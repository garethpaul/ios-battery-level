# Battery Monitoring Lifecycle Plan

status: completed

Follow-up: `2026-06-25-battery-disappearance-boundary.md` moves the same
observer and monitoring teardown contract to `viewWillDisappear` so cleanup
begins before the disappearance transition continues.

## Context

`ios-battery-level` enables `UIDevice.batteryMonitoringEnabled` before reading `batteryLevel`, but the sample leaves monitoring enabled after the read. The project should keep the API requirement visible without changing device monitoring state longer than needed.

## Objectives

- Move battery-level access into a focused helper.
- Capture the previous `batteryMonitoringEnabled` state before enabling monitoring.
- Restore the previous monitoring state after reading `batteryLevel`.
- Extend the static baseline so the lifecycle guard remains visible without Xcode.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
