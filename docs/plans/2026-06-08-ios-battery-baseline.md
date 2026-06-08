# iOS Battery Level Baseline Plan

status: completed

## Context

`ios-battery-level` is a legacy Swift iOS sample that reads `UIDevice.batteryLevel`. This Linux host does not provide Xcode, so local verification needs a static baseline while full app builds remain a macOS/Xcode responsibility.

## Objectives

- Enable battery monitoring before reading battery level so the sample reflects UIKit API requirements.
- Add a local `make check` baseline for Xcode metadata, plist/storyboard XML, source inventory, and privacy guardrails.
- Keep battery/device state local-only with no analytics, network reporting, persistence, or logging.
- Document legacy Xcode verification expectations and non-macOS static checks.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
