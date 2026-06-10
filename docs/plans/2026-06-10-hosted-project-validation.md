# Hosted Project Validation

status: completed

## Context

The static baseline covered battery normalization, local-only privacy,
project metadata, and UI/test guardrails, but it only printed a reminder when
Xcode was installed. The repository had no current hosted project-file check.

## Completed Scope

- Added a pinned GitHub Actions workflow with read-only repository permissions.
- Runs the canonical `make check` gate on a bounded `macos-15` job.
- Parses `ChargeMe.xcodeproj` whenever Xcode is available.
- Kept battery reads, monitoring changes, signing, and simulator behavior
  outside hosted CI.
- Extended the checker and documentation to preserve the CI contract.

## Verification

- `python3 scripts/check-baseline.py`
- `make check`
- workflow YAML parse
- `git diff --check`
