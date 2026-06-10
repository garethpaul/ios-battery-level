# Swift 5 App Build

status: completed

## Context

The hosted gate parsed the Xcode project but did not compile its source. The app
and tests still used Swift 2-era UIKit, UIDevice, method-label, and app-delegate
syntax, while the project retained an iOS 8.3 deployment target.

## Completed Scope

- Migrated the app delegate and battery view controller to Swift 5 syntax.
- Preserved the existing battery normalization and formatter test API with
  explicit unlabeled parameters.
- Set the app and test target configurations to Swift 5.
- Raised the deployment target from iOS 8.3 to iOS 12 for current Xcode support.
- Upgraded Xcode-enabled `make check` runs to compile an unsigned Debug build of
  the app target for the iOS Simulator without launching it or reading battery
  state.
- Extended the static baseline and project documentation to preserve the new
  toolchain contract.

## Verification

- `python3 scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- hosted macOS simulator build
- `git diff --check`
