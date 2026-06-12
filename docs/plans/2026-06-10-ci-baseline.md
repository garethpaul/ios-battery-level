# iOS Battery Level CI Baseline

status: completed

## Context

The sample has an SDK-free `make check` baseline for battery-level behavior,
Xcode metadata, docs, and privacy guardrails. Full app verification still needs
macOS and Xcode. The missing guard was hosted CI for the static baseline.

## Changes

- Added `.github/workflows/check.yml` for GitHub Actions.
- Ran the Python static baseline on Ubuntu with Python 3.12.
- Kept full simulator/device verification documented as a macOS toolchain task.
- Extended the checker and docs so hosted CI stays visible.

## Verification

- `make check`
- `git diff --check`
