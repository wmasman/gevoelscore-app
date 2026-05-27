# Step 1: Name

**Estimated time:** X hours
**Test layer:** Domain | API client | Validation | Integration | Component | Screen | Visual-baseline-only
**Risk:** Low / Medium / High — why
**Prerequisite:** none (Step 1 is always first) — or: "Step N from another feature complete"

> Copy this to `step-1-{slug}.md` inside your feature folder and replace placeholders. Add `step-2-{slug}.md`, etc. as needed.
> TDD is mandatory — see [`.claude/testing.md`](../../../.claude/testing.md). Visual-baseline-only is the single escape (pure-styling work).

---

## Acceptance criteria (subset of feature README's criteria delivered by this step)

- [ ] AC1: Given <precondition>, when <action>, then <expected result>
- [ ] AC2: ...

## Technical constraints (applicable to this step)

- [ ] [Constraint that must hold — e.g. "score validation runs synchronously, no I/O"]
- [ ] [Constraint from a gate — e.g. "no telemetry deps added"]

## Test plan

Copy-pasteable test code. One `it` block per AC. File path explicit.

**File**: `src/lib/{module}/__tests__/{module}.test.ts`

```typescript
import { describe, expect, it } from 'vitest';
// import { thingUnderTest } from '../{module}';

describe('{module}', () => {
  describe('{behavior}', () => {
    it('given <precondition>, when <action>, then <expected>', () => {
      // Arrange

      // Act

      // Assert
      expect(actual).toBe(expected);
    });
  });
});
```

---

## Done criteria

- [ ] Every AC above is GREEN
- [ ] RED was captured before implementation (output recorded below)
- [ ] GREEN was captured after implementation (output recorded below)
- [ ] Full suite still passes (no regressions)
- [ ] `npm run typecheck` clean
- [ ] `npm run lint` clean
- [ ] No new HIGH gate findings (cardinal / privacy / security / v1.5-v2)
- [ ] Walkthrough done if step touched daily screen (≤ 10s timed, brainfog pass, offline pass)
- [ ] Refactor pass complete (or "none needed" stated)

---

## Execution order (followed by `/build-step`)

### 1.1 Baseline (skip if creating new code)

If this step modifies existing behavior, capture current state for comparison:

- Failing-test output of the current state, or
- Screenshot of the affected screen, or
- CSV diff if data shape changes

### 1.2 Write tests (RED)

Paste the test code above into the file. Run:

```
npm test -- {pattern}
```

Must FAIL for the reason stated in each AC. Record the failure line under Done.

### 1.3 Implement (GREEN)

Smallest code that turns the RED tests GREEN. Files to create / modify:

- `src/lib/{module}/{file}.ts` — [purpose]

Reference patterns from:

- [path]: [what to extract]

Run again:

```
npm test -- {pattern}
```

Must PASS. Record the pass line under Done.

### 1.4 Regression check

```
npm test
```

Everything that was GREEN before must still be GREEN.

### 1.5 Refactor

Clean up while GREEN stays GREEN. State what was changed, or "none needed".

### 1.6 Walkthrough — only if the step changed the daily screen

1. Open the app in Safari iOS (primary daily-driver context) and cross-check in Chrome / Firefox.
2. Time the daily-entry flow with a stopwatch — must stay ≤ 10s on a good-day simulation.
3. Brainfog walkthrough: one-handed, low light, arm's length on a phone. Any tap that needs a second attempt is a fail.
4. Network-loss check: DevTools Network → Offline. Verify the "no network, retry" state per [ADR 0002](../../../docs/decisions/0002-pwa-with-directus-backend.md).

### 1.7 Checkpoint

What's safe to commit at this point. State the commit message that will be used:

```
{feature-name}/step-1: <one-line summary>

Acceptance criteria addressed:
- AC1: <criterion>
- AC2: <criterion>

Tests: <X new, Y passing total>
```

---

## Done (filled in during `/build-step`)

- [ ] AC1: `<criterion>` — test `<file>:<it name>` GREEN
- [ ] AC2: ...
- [ ] RED captured: `<command>` → `<failure summary>` on <date>
- [ ] GREEN captured: `<command>` → `<X passing>` on <date>
- [ ] Type check clean
- [ ] Lint clean
- [ ] No new HIGH gate findings
- [ ] Walkthrough (if applicable): ...
- [ ] Refactor: ...

---

## What this step does NOT do

Explicit scope boundary — keeps the step focused and prevents creep:

- [Thing that sounds like it belongs here but doesn't — and where it lives instead]
- [Future work that might tempt scope expansion]
