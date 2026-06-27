# Changes

- Preserved absolute Makefile roots containing spaces and added a recursive-safe full-baseline regression.

## 2026-06-26 12:17 PDT - P2 - Reconcile hosted XCTest roadmap

### Summary

Reconciled the completed hosted XCTest roadmap item with the maintained shared
scheme, pinned macOS workflow, simulator discovery, and canonical `make test`
gate. No Swift, Xcode project, Make, or workflow behavior changed.

### Work completed

- Replaced the stale future claim with an ongoing roadmap and validation
  synchronization boundary.
- Added a fail-closed baseline contract that rejects the completed priority if
  it returns.
- Added design and implementation records for the evidence-backed docs change.

### Threads

- None. The audit was completed directly after confirming no public pull
  requests, issues, or unmerged remote work needed finishing first.

### Files changed

- `VISION.md` — retired the completed hosted-test priority.
- `scripts/check-baseline.py` — enforces the current roadmap contract.
- `docs/plans/2026-06-26-hosted-xctest-roadmap-design.md` — records the design.
- `docs/plans/2026-06-26-hosted-xctest-roadmap.md` — records implementation and verification.
- `CHANGES.md` — this cycle record.

### Validation

- Red-first `python3 scripts/check-baseline.py` rejected the missing roadmap,
  plan, and history evidence before documentation changed.
- `make lint`, `make test`, `make build`, and `make check` passed from the
  checkout and through the absolute Makefile path from `/tmp`; XCTest skipped
  truthfully because `xcodebuild` is unavailable locally.
- Four isolated hostile mutations rejected weakened synchronization guidance,
  restoration of the stale priority, incomplete plan status, and missing
  history evidence.
- Python and shell syntax, diff, artifact, and credential-shaped-content audits
  passed. Hosted XCTest, CodeQL, and exact-head review remain required.

### Bugs / findings

- P2 documentation: `VISION.md` described adding hosted XCTest after a shared
  scheme as future work even though both have been maintained since June 12.

### Blockers

- None for portable validation; native Xcode evidence is hosted on macOS.

### Next action

- Complete local and hosted exact-head validation, then merge only the reviewed
  green commit.

## 2026-06-26

- Replaced per-controller battery-monitoring restoration with a shared visible
  ownership lease for the process-global `UIDevice` setting.
- Kept monitoring enabled while overlapping controllers remain visible and
  restored the original process state only after the final owner disappears.
- Added focused overlapping-lifecycle XCTest, portable ownership-order
  contracts, parallel-test-isolated coordinator injection, and a completed
  design record.

## 2026-06-25

- Moved battery observer and monitoring teardown to the start of the
  disappearance transition. Battery observers stop in viewWillDisappear before the disappearance transition continues.
- Added focused XCTest and static contracts for transition-start cleanup.

- Removed a stale numeric XCTest count from the README so the documented hosted
  validation remains accurate as focused battery coverage grows.

## 2026-06-19

- Refresh the visible battery presentation when the application becomes active.
- Isolate lifecycle tests with a private notification center and exact battery
  notification object, while removing both observer tokens during teardown.
- Use explicit finite validation and deterministic half-away-from-zero
  percentage rounding for visible and accessibility values.

## 2026-06-14

- Rejected stale queued battery callbacks by lifecycle generation so removed
  observers cannot refresh hidden or later appearances.
- Refresh visible and accessibility battery values on battery-level and
  application-active notifications while the view is visible, with scoped
  observers and bounded monitoring-state restoration.
- Kept simulator tests isolated from process-global battery monitoring state
  and main-queue notification stalls while preserving production UIKit
  behavior.

## 2026-06-13

- Made every Make verification target derive the checkout root so static and
  XCTest gates work from external directories.
- Refreshed visible and accessibility battery values on each view appearance
  instead of keeping the initial load-time reading.

## 2026-06-12

- Added a shared Xcode scheme and portable simulator discovery so hosted macOS
  CI executes the existing XCTest suite through `make test`.
- Disabled persisted checkout credentials and retained unsigned simulator
  execution without battery telemetry, deployment, or signing material.
- Fixed Swift comment stripping so quoted plain-HTTP URLs remain visible to the
  local-only privacy baseline.
- Revalidated battery values in text and accessibility formatters so invalid
  direct inputs use the unknown state.

## 2026-06-10

- Added a GitHub Actions workflow that runs the SDK-free `make check` baseline
  for the local-only battery-level sample.
- Migrated the app and XCTest source from Swift 2 syntax to Swift 5.
- Raised the deployment target from iOS 8.3 to iOS 12.
- Upgraded Xcode-enabled validation from project parsing to an unsigned iOS
  Simulator build of the app target.
- Added pinned, read-only macOS CI for the canonical `make check` baseline.
- Made Xcode-enabled checks parse `ChargeMe.xcodeproj` without reading battery
  state or changing battery-monitoring behavior.
## 2026-06-09

- Added an accessibility value for the visible battery-level label so known,
  zero, and unknown readings are exposed to assistive technologies.
- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static battery sample baseline.
- Added a zero battery-level boundary assertion so `0.0` remains a valid
  normalized percentage.
- Added a visible local battery-level label with formatter coverage for known
  and unknown readings.

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
