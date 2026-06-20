# Battery Lifecycle Deep Review

status: completed

## Scope

Deep-review the linear PR stack from `#3` through `#7`, following battery state
from view lifecycle entry through monitoring ownership, notification delivery,
normalization, presentation, accessibility, teardown, tests, Make gates, and
hosted workflows.

## Root Cause

The stacked changes correctly added visible-lifecycle ownership and stale
callback generations, but only battery-level notifications refreshed an
already-visible controller. Returning from the background could therefore
leave stale text until another battery event. Tests also used the process-wide
notification center, making observer isolation implicit rather than owned.

## Fix Shape

- Retain exact battery-level and application-active observer tokens from one
  notification center.
- Accept battery notifications only from the owned device object.
- Route both callbacks through the same active-generation guard and main queue.
- Remove both tokens before restoring the captured monitoring state.
- Isolate XCTest notification delivery with a private center and probe state.
- Use explicit finite validation and deterministic half-away-from-zero
  percentage rounding for text and accessibility.

## Verification Plan

- Run the static baseline from the repository and an external directory.
- Build and execute focused XCTest on an iOS simulator.
- Kill isolated mutations for observer ownership, foreground refresh,
  generation rejection, restoration, event identity, finite validation, and
  rounding.
- Scan the current tree and full history for credentials without printing
  candidate values.
- Require exact-head hosted Check and CodeQL before merge.

## Verification Completed

- The static baseline, checker compilation, action workflow validation, and
  diff checks passed.
- A generic unsigned simulator `build-for-testing` compiled the production and
  XCTest changes. A later clean retry was interrupted by concurrent local
  Xcode/Interface Builder contention; exact-head hosted XCTest is the canonical
  executable gate.
- The new tests cover appearance and foreground refresh, duplicate observer
  prevention, hidden-view rejection, stale generations, exact event identity,
  prior-state restoration, deinit cleanup, finite normalization, and rounding.
- Exact-head hosted Check and CodeQL remain mandatory before merge.
