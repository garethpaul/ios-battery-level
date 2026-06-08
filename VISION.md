## iOS Battery Level Vision

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
- Maintain security policy for the sample

Next priorities:

- Add README setup and verification notes
- Enable and document battery monitoring if needed for accurate readings
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

## What We Will Not Merge (For Now)

- Telemetry around battery or device state
- Broad app features unrelated to battery APIs
- Project migration mixed with behavior changes
- Generated signing material

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
