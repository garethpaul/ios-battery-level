# Hosted XCTest Roadmap Reconciliation Design

## Context

`VISION.md` still lists adding hosted test execution after a shared scheme is
maintained as future work. The repository already has a shared `ChargeMe`
scheme, a pinned macOS workflow that runs `make test`, simulator discovery, and
completed hosted XCTest plans. Leaving the item under `Next priorities` makes
the roadmap contradict the maintained build and test authority.

## Options Considered

1. Remove only the stale bullet. This fixes the immediate contradiction but
   allows the same stale claim to return unnoticed.
2. Replace the stale bullet and add a fail-closed source contract. This keeps a
   useful roadmap synchronization boundary and makes future drift executable.
3. Change the workflow or XCTest setup. This duplicates completed work and
   risks altering a currently green native gate without evidence of a defect.

## Decision

Use option 2. Preserve all application, project, test, Make, and workflow
behavior. Replace the completed future item with an ongoing requirement to keep
roadmap and validation guidance synchronized with the shared scheme and hosted
XCTest workflow. Extend `scripts/check-baseline.py` to require the maintained
guidance, reject the stale future claim, require a completed plan, and require a
cycle record in `CHANGES.md`.

## Verification

- Add the checker contract first and observe the baseline fail because the
  roadmap, plan, and change record are absent.
- Update only documentation to satisfy the contract.
- Run the repository and external-directory Make gates.
- Apply isolated mutations to the synchronization guidance, stale claim,
  completed plan status, and change-history evidence.
- Require exact-head hosted baseline, XCTest, CodeQL, and review before merge.
