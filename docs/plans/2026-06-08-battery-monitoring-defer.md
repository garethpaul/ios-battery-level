# Battery Monitoring Defer Plan

status: completed

## Context

`readBatteryLevel()` temporarily enables `UIDevice.batteryMonitoringEnabled` so `UIDevice.batteryLevel` can return a meaningful sample value. The helper restores the previous monitoring state, but that restoration should stay tied to helper scope if the implementation grows new exit paths later.

## Objectives

- Use `defer` to restore the previous `batteryMonitoringEnabled` value.
- Preserve the existing helper return type and call site.
- Extend the static baseline so the lifecycle guard requires deferred restoration.
- Document the helper-scope restoration expectation.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
