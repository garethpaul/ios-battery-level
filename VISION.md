## iOS Battery Level Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

iOS Battery Level is a small Swift sample for reading device battery level.

The repository is useful as a minimal iOS project for experimenting with
`UIDevice` battery APIs.

The goal is to keep the sample tiny, clear, and honest about what battery data
it reads.

The current focus is:

Priority:

- Preserve the simple battery-level retrieval example
- Keep the Xcode project easy to inspect
- Avoid adding analytics or network reporting of device state
- Treat unknown battery-level readings as absent values instead of percentages
- Preserve zero battery-level readings as valid percentages
- Treat non-finite battery-level readings as absent values
- Keep battery readings visible in the sample UI without adding persistence or
  reporting
- Keep the visible battery reading exposed as an accessibility value
- Refresh visible and accessibility values on every view appearance
- Restore battery monitoring state with `defer` after sample reads
- Maintain security policy for the sample
- Keep `scripts/check-baseline.py` passing for battery-monitoring behavior,
  local-only device state, plist/storyboard XML, Xcode metadata, and source inventory
- Keep `make lint`, `make test`, `make build`, and `make check` available as
  local verification gates
- Keep the app and test targets on Swift 5 with the iOS 12 deployment target
- Keep pinned GitHub Actions macOS CI executing the shared-scheme XCTest suite
  through the canonical `make test` gate

Next priorities:

- Add a small UI or testable wrapper only if it improves the sample
- Add test execution to hosted CI once a shared scheme is maintained

Contribution rules:

- One PR = one focused battery, UI, test, or documentation change.
- Keep the sample small.
- Verify behavior on simulator or device when changing battery logic.
- Keep generated build products and signing files out of git.

## Security And Privacy

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Battery state and device details should remain local diagnostic data. Do not add
network reporting, analytics, or persistent device profiling.

Current baseline: `make lint`, `make test`, `make build`, and `make check` run
`scripts/check-baseline.py` without Xcode. It verifies that battery monitoring
is enabled before reading battery level and restored with `defer` after the
read, that unknown battery levels normalize to `nil`, that zero battery levels
remain valid, that non-finite or out-of-range battery levels are rejected, and
that the visible display helper shows known and unknown readings while
battery accessibility values expose known and unknown readings. Battery/device
state remains local-only with no logging, network reporting, upload, analytics,
or persistence behavior.
Text and accessibility presentation revalidate inputs so direct callers cannot
expose non-finite or out-of-range percentages.
Each view appearance should perform a fresh scoped read without changing the
caller's prior battery-monitoring setting.
On macOS, the baseline should compile an unsigned simulator build without
launching the app, reading device battery state, or changing monitoring behavior.

## What We Will Not Merge (For Now)

- Telemetry around battery or device state
- Broad app features unrelated to battery APIs
- Project migration mixed with behavior changes
- Generated signing material

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
