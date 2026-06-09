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
- Restore battery monitoring state with `defer` after sample reads
- Maintain security policy for the sample
- Keep `scripts/check-baseline.py` passing for battery-monitoring behavior,
  local-only device state, plist/storyboard XML, Xcode metadata, and source inventory

Next priorities:

- Add a small UI or testable wrapper only if it improves the sample
- Modernize Swift/project settings in a dedicated pass

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

Current baseline: `make check` runs `scripts/check-baseline.py` without Xcode.
It verifies that battery monitoring is enabled before reading battery level and
restored with `defer` after the read, that unknown battery levels normalize to
`nil`, and that battery/device state remains local-only with no logging, network
reporting, upload, analytics, or persistence behavior.

## What We Will Not Merge (For Now)

- Telemetry around battery or device state
- Broad app features unrelated to battery APIs
- Project migration mixed with behavior changes
- Generated signing material

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
