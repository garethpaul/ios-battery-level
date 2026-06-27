# ios-battery-level

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/ios-battery-level` is a Apple platform application or Swift sample. Battery identifier.

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: Swift (3).

## Repository Contents

- `CHANGES.md` - concise history of maintenance changes
- `ChargeMe` - source or example code
- `ChargeMe.xcodeproj` - Xcode project file
- `ChargeMeTests` - source or example code
- `Makefile` - local verification entry point
- `SECURITY.md` - security reporting and disclosure guidance
- `scripts/check-baseline.py` - static iOS battery sample verifier
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: ChargeMe, ChargeMeTests
- Dependency and build manifests: none detected
- Entry points or build surfaces: `make check`, ChargeMe.xcodeproj
- Test-looking files: ChargeMeTests/ChargeMeTests.swift, ChargeMeTests/Info.plist

## Getting Started

### Prerequisites

- Git
- macOS with Xcode for building Apple platform projects
- Python 3 for local static verification on non-macOS hosts

### Setup

```bash
git clone https://github.com/garethpaul/ios-battery-level.git
cd ios-battery-level
make lint
make test
make build
make check
```

The checked-in project has no external dependency manifest. Use Xcode for full builds and `make check` for static verification on hosts without Xcode.

## Running or Using the Project

- Open `ChargeMe.xcodeproj` in Xcode, choose the app or sample scheme, and run it on the matching simulator/device.
- The sample enables `batteryMonitoringEnabled` before reading `UIDevice.batteryLevel`, preserves zero and other valid levels, normalizes unknown, non-finite, or out-of-range levels to `nil`, revalidates values at the presentation boundary, rounds percentages consistently for text and accessibility, shows the value in a visible local label such as `Battery Level: Unknown`, exposes the current reading as an accessibility value, then uses `defer` to restore the previous monitoring state.
- While visible, the controller owns exact battery-level and application-active
  observer tokens. Both deliver on the main queue, refresh the same local
  presentation path, reject stale lifecycle generations, and are removed
  before the prior battery-monitoring state is restored.
- Visible controller instances share ownership of the process-global battery
  monitoring setting. The first owner captures and enables it; the final owner
  restores the original state, so overlapping views cannot disable each other.
- Battery observers stop in viewWillDisappear before the disappearance transition continues.
- Keep battery/device state local-only; do not add analytics, persistence, or network reporting without a dedicated privacy design.

## Testing and Verification

Run the local static baseline:

```bash
make lint
make test
make build
make check
```

The `lint`, `test`, and `build` targets intentionally alias the static baseline
on hosts without the legacy Xcode toolchain, so the standard local gate commands
stay available while preserving the single source of truth.

The baseline runs `scripts/check-baseline.py`, parses plist/storyboard/project XML, checks the Swift source inventory and testability wiring, verifies that battery monitoring is enabled before reading battery level, confirms zero battery levels are preserved, confirms unknown, non-finite, or out-of-range levels normalize to `nil`, requires a visible local label, accessibility value, and focused XCTest assertions for the normalization and display helpers, verifies restoration afterward with `defer`, and guards against logging, network reporting, upload, or analytics behavior.
Each view appearance performs a fresh scoped read, updating both visible text and
the accessibility value without leaving battery monitoring enabled.
The visible lifecycle also rejects stale queued battery callbacks by lifecycle
generation, so a removed observer cannot refresh a hidden or later appearance.
Focused XCTest also covers overlapping visible controllers and final-owner
restoration of the process-global monitoring state.

The pinned GitHub Actions check runs `make test` on `macos-15`. It first runs
the static baseline, then compiles the unsigned Swift 5 app and executes the
battery lifecycle, normalization, formatting, and accessibility XCTest suite on
an available iPhone simulator. It does not read live battery state, alter
device monitoring outside test process lifetime, deploy, or use signing
material.

For runtime verification on macOS, launch the sample on a simulator or device
and confirm the visible and accessibility values match the local battery state.

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- No required secret or credential file was identified in the repository scan. If you add integrations later, keep secrets out of git.

## Security and Privacy Notes

- Review changes touching network requests, sockets, or service endpoints; examples from the scan include ChargeMe/Info.plist, ChargeMeTests/Info.plist.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include ChargeMe/Info.plist, ChargeMeTests/Info.plist.
- Battery and device state are local diagnostic signals. Avoid logging, persisting, uploading, or profiling this data unless the data flow and user consent are documented first.
- Keep each view appearance refresh tied to the scoped battery read helper.

## Maintenance Notes

- Every Make verification target derives the checkout root from the loaded
  Makefile, so an absolute Makefile path works from any working directory,
  including checkout paths containing spaces.
- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-09-battery-level-upper-bound.md` for the out-of-range battery-level guardrail.
- See `docs/plans/2026-06-09-nonfinite-battery-level.md` for the non-finite battery-level guardrail.
- See `docs/plans/2026-06-09-zero-battery-level.md` for the zero battery-level boundary guardrail.
- See `docs/plans/2026-06-09-visible-battery-level.md` for the visible local battery-level display guardrail.
- See `docs/plans/2026-06-09-battery-accessibility-value.md` for the battery
  accessibility value guardrail.
- See `docs/plans/2026-06-09-make-gate-aliases.md` for the local gate alias guardrail.
- See `docs/plans/2026-06-10-ci-baseline.md` for the initial hosted static
  baseline and `docs/plans/2026-06-10-hosted-project-validation.md` plus
  `docs/plans/2026-06-10-swift-5-app-build.md` for its macOS build evolution.
- See `docs/plans/2026-06-12-hosted-xctest.md` for the shared scheme,
  simulator discovery, and hosted XCTest gate.
- See `docs/plans/2026-06-13-battery-view-appearance-refresh.md` for fresh
  appearance-time presentation.
- Run `make lint`, `make test`, `make build`, and `make check` before pushing changes to Swift sources, plist/storyboard files, Xcode metadata, battery behavior, or privacy documentation.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
