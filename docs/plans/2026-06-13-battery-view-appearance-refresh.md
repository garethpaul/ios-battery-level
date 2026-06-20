# Battery View Appearance Refresh

status: completed

## Context

The sample reads and displays battery level only from `viewDidLoad`. A view
controller can remain alive while another screen or app state is active, so a
later appearance may continue showing the percentage captured at initial load.

Battery monitoring is already enabled only around each read and restored with
`defer`; refreshing on appearance can reuse that boundary without introducing a
long-lived observer or changing device-monitoring ownership.

## Priority

The single visible value is the purpose of the sample. It should reflect a fresh
read whenever the screen becomes visible, while keeping the existing unknown,
normalization, formatting, accessibility, and monitoring behavior.

## Requirements

- R1. `viewDidLoad` must configure the label without owning the battery read.
- R2. Every `viewWillAppear` must read and display the current battery level
  after calling `super.viewWillAppear`.
- R3. Repeated appearances must update both visible text and accessibility value.
- R4. Preserve temporary battery-monitoring enablement and deferred restoration.
- R5. Preserve normalization for unknown, non-finite, out-of-range, zero, and
  full battery values.
- R6. Add executable XCTest coverage and a lifecycle-scoped static contract.

## Implementation Units

### U1. Refresh on appearance

- **File:** `ChargeMe/ViewController.swift`
- Move the read/display call from `viewDidLoad` into `viewWillAppear`.

### U2. Add lifecycle regression coverage

- **File:** `ChargeMeTests/ChargeMeTests.swift`
- Use a deterministic controller subclass to prove two appearances display two
  different battery values and accessibility percentages.

### U3. Enforce and document the boundary

- **Files:** `scripts/check-baseline.py`, `README.md`, `SECURITY.md`,
  `VISION.md`, `CHANGES.md`
- Require refresh ordering, test intent, and completed verification evidence.

## Scope Boundaries

- Do not add long-lived battery notification observers or leave monitoring on.
- Do not change layout, percentage rounding, accessibility copy, project
  settings, workflow structure, or deployment target.
- Do not claim physical battery-state validation from simulator XCTest.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- `sh -n scripts/run-tests.sh`
- Parse plist, storyboard, XIB, scheme, workspace, project, and workflow metadata
  with all available local parsers.
- `git diff --check`
- Hostile mutations restoring the load-time read, removing the appearance hook,
  super call, read/display ordering, repeated-appearance assertions, plan status,
  or verification evidence must be rejected.

## Verification Completed

- All four Make gates (`make lint`, `make test`, `make build`, and
  `make check`) passed against the completed implementation and plan.
- `python3 -m py_compile scripts/check-baseline.py`, `sh -n
  scripts/run-tests.sh`, available plist/XML/workflow parsers, and
  `git diff --check` passed.
- A prepared baseline passed and nine hostile mutations were rejected. They
  restored load-time sampling, removed the appearance hook or super call,
  reversed refresh ordering, removed the repeated appearance or refreshed text
  or accessibility assertions, reopened the plan, or removed verification
  evidence.
- `xcodebuild` was unavailable on this Linux host, so the fifteen-test simulator
  suite was not executed locally. The canonical test runner reported that
  limitation; hosted macOS remains responsible for executable XCTest evidence.
