# Hosted XCTest

status: completed

## Context

The Swift 5 migration made the app compile on current Xcode, but hosted CI did
not execute the twelve existing battery normalization, formatting, and
accessibility tests because the project had no shared scheme.

## Completed Scope

- Added a shared `ChargeMe` scheme containing the app and unit-test targets.
- Added portable iPhone simulator discovery with explicit destination overrides.
- Kept `make check` as the SDK-free static gate and made `make test` execute
  XCTest whenever Xcode is available.
- Changed hosted macOS CI to run the complete `make test` gate without signing.
- Made Swift line-comment stripping preserve quoted URL strings so transport
  checks evaluate the actual source.

## Verification

- `make check`
- `make test`
- `sh -n scripts/run-tests.sh`
- hosted macOS XCTest run
- hostile mutations removing the scheme, test command, simulator discovery,
  or credential-free checkout must fail
- a mutation adding a quoted plain-HTTP endpoint must fail
- `git diff --check`
