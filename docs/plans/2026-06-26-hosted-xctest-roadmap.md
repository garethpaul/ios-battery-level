# Hosted XCTest Roadmap Reconciliation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use executing-plans to implement this plan task-by-task.

**Goal:** Remove the completed hosted-XCTest roadmap item and prevent the stale claim from returning.

**Architecture:** Keep the Swift application, Xcode project, tests, Makefile, and workflow unchanged. Add a fail-closed documentation contract to the existing Python baseline, then reconcile `VISION.md` and record evidence in the plan and `CHANGES.md`.

**Tech Stack:** Markdown, Python 3, GNU Make, Xcode project metadata, GitHub Actions

---

status: completed

### Task 1: Add The Failing Roadmap Contract

**Files:**
- Modify: `scripts/check-baseline.py`

**Step 1: Require maintained guidance**

Require `VISION.md` to contain an ongoing hosted-XCTest synchronization
priority, reject the stale future claim, require this plan to be completed, and
require the cycle history entry.

**Step 2: Run the focused baseline**

Run: `python3 scripts/check-baseline.py`

Expected: FAIL because the roadmap, completed plan status, and change record do
not yet satisfy the new contract.

### Task 2: Reconcile The Documentation

**Files:**
- Modify: `VISION.md`
- Modify: `CHANGES.md`
- Modify: `docs/plans/2026-06-26-hosted-xctest-roadmap.md`

**Step 1: Replace the stale priority**

Remove only the completed hosted-test future item and add the ongoing
synchronization boundary.

**Step 2: Record the cycle**

Add the newest `CHANGES.md` entry and mark this plan completed with exact local
verification evidence.

**Step 3: Run the focused baseline**

Run: `python3 scripts/check-baseline.py`

Expected: PASS.

### Task 3: Prove The Contract Fails Closed

**Files:**
- Test: `scripts/check-baseline.py`

**Step 1: Apply isolated mutations**

Mutate the synchronization guidance, restore the stale future claim, change the
plan status, and remove the change-history evidence in separate temporary
copies.

**Step 2: Run the baseline after each mutation**

Expected: every mutation is rejected.

### Task 4: Run Full Validation

**Files:**
- Verify: `Makefile`

**Step 1: Run repository verification**

Run: `/usr/bin/make check`

Expected: portable checks pass; native XCTest runs only where Xcode exists.

**Step 2: Run external-directory verification**

Run: `cd /tmp && /usr/bin/make -f /tmp/code/ios-battery-level/Makefile check`

Expected: the same result through the absolute Makefile path.

### Task 5: Review And Ship

**Files:**
- Verify: exact branch head and PR checks

**Step 1: Commit and push**

Commit the focused documentation and checker changes, then open a pull request.

**Step 2: Run Codex review**

Run the branch review helper against `origin/master`. Skip only an
authentication-only failure as allowed by the maintenance objective.

**Step 3: Merge the immutable green head**

Require the PR head to match the reviewed commit, all hosted checks to pass,
and the merge state to be clean before squash-merging with
`--match-head-commit`.

## Verification Completed

- The red `python3 scripts/check-baseline.py` run failed only for the missing
  roadmap synchronization guidance, cycle record, and completed plan evidence.
- The focused baseline passed after the documentation reconciliation.
- Repository-root and external-directory Make gates passed; native Xcode and
  XCTest execution remains the hosted macOS authority where unavailable.
- Four isolated hostile mutations rejected weakened synchronization guidance,
  restoration of the stale future claim, an incomplete plan status, and missing
  change-history evidence.
- Python syntax, shell syntax, `git diff --check`, artifact, and
  credential-shaped-content audits passed before push.
