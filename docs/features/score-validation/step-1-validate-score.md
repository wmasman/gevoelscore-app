# Step 1: Implement Score type + validateScore

**Estimated time:** 30–45 minutes
**Test layer:** Domain
**Risk:** Low — pure function, single file, no I/O, no platform deps
**Prerequisite:** none (this is the first real RED → GREEN cycle on the project)

> TDD is mandatory — see [`.claude/testing.md`](../../../.claude/testing.md).

---

## Acceptance criteria (this step delivers all six)

- [ ] AC1: Given an integer between 1 and 10 inclusive, when `validateScore` is called, then it returns `{ ok: true, value }` with the same number.
- [ ] AC2: Given a number above 10, when validated, then `{ ok: false, error: 'out_of_range' }`.
- [ ] AC3: Given a number below 1, when validated, then `{ ok: false, error: 'out_of_range' }`.
- [ ] AC4: Given a half-value (4.5), when validated, then `{ ok: false, error: 'not_integer' }`.
- [ ] AC5: Given a decimal in range (3.1, 5.999), when validated, then `{ ok: false, error: 'not_integer' }`.
- [ ] AC6: Given a non-number input (string, null, undefined, NaN, object), when validated, then `{ ok: false, error: 'wrong_type' }`.

## Technical constraints (this step)

- [ ] Pure TS, zero dependencies — no `next/*`, `@directus/sdk`, Zod, React imports.
- [ ] Synchronous, sub-millisecond execution.
- [ ] Input typed as `unknown` — no implicit `any`.
- [ ] Return type is a discriminated union (TypeScript narrows on `r.ok`).
- [ ] No `console.log`, no side effects, no I/O.

## Test plan

Copy-pasteable. Save as `src/lib/domain/__tests__/score.test.ts`.

```typescript
import { describe, expect, it } from 'vitest';
import { validateScore } from '../score';

describe('score', () => {
  describe('validateScore — accepts valid scores', () => {
    it.each([1, 2, 3, 4, 5, 6, 7, 8, 9, 10] as const)(
      'given integer %i, when validated, then it returns { ok: true, value: %i }',
      (input) => {
        const result = validateScore(input);

        expect(result.ok).toBe(true);
        if (result.ok) {
          expect(result.value).toBe(input);
        }
      },
    );
  });

  describe('validateScore — rejects out-of-range', () => {
    it.each([11, 100, Number.POSITIVE_INFINITY])(
      'given %s (above 10), when validated, then it returns out_of_range',
      (input) => {
        const result = validateScore(input);

        expect(result).toEqual({ ok: false, error: 'out_of_range' });
      },
    );

    it.each([0, -1, Number.NEGATIVE_INFINITY])(
      'given %s (below 1), when validated, then it returns out_of_range',
      (input) => {
        const result = validateScore(input);

        expect(result).toEqual({ ok: false, error: 'out_of_range' });
      },
    );
  });

  describe('validateScore — rejects non-integer', () => {
    it('given 4.5 (half-value), when validated, then it returns not_integer', () => {
      const result = validateScore(4.5);

      expect(result).toEqual({ ok: false, error: 'not_integer' });
    });

    it.each([3.1, 5.999])(
      'given decimal %s, when validated, then it returns not_integer',
      (input) => {
        const result = validateScore(input);

        expect(result).toEqual({ ok: false, error: 'not_integer' });
      },
    );
  });

  describe('validateScore — rejects wrong type', () => {
    it.each([
      ['string', '3'],
      ['null', null],
      ['undefined', undefined],
      ['NaN', Number.NaN],
      ['object', {}],
      ['array', [3]],
      ['boolean', true],
    ])(
      'given %s, when validated, then it returns wrong_type',
      (_label, input) => {
        const result = validateScore(input);

        expect(result).toEqual({ ok: false, error: 'wrong_type' });
      },
    );
  });
});
```

---

## Done criteria

- [ ] All six ACs are GREEN
- [ ] RED captured below (test file written, run, all expected failures recorded)
- [ ] GREEN captured below (function implemented, full suite passes)
- [ ] Full suite still passes (no regressions)
- [ ] `npm run typecheck` clean
- [ ] `npm run lint` clean (no-op for now — wired up later)
- [ ] No new HIGH gate findings
- [ ] No walkthrough needed (pure domain layer, no UI)
- [ ] Refactor pass: stated or "none needed"

---

## Execution order (followed by `/build-step`)

### 1.1 Baseline

Run `npm test` once to confirm current state: 1 failed (the `_scaffold` test), 0 passed. Record the failure line.

### 1.2 Write tests (RED)

1. Create `src/lib/domain/__tests__/score.test.ts` with the test code above.
2. Run: `npm test -- score.test`
3. Expected: all `describe`s fail at the import line — `Cannot find module '../score'`. That's a *setup* failure, not a meaningful RED.
4. To get a meaningful RED, first create `src/lib/domain/score.ts` with a stub that compiles but always returns wrong:

```typescript
export type Score = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
export type ScoreError = 'out_of_range' | 'not_integer' | 'wrong_type';
export type ValidateScoreResult =
  | { ok: true; value: Score }
  | { ok: false; error: ScoreError };

export function validateScore(_input: unknown): ValidateScoreResult {
  return { ok: false, error: 'wrong_type' }; // intentionally wrong — RED first
}
```

5. Re-run `npm test -- score.test`
6. Expected: 10 valid-input tests fail (AC1), some out-of-range tests fail (AC2/AC3 — because they expect `out_of_range` but get `wrong_type`), some not-integer tests fail (AC4/AC5), some wrong-type tests pass (AC6 — by accident, since the stub always returns `wrong_type`).
7. Record the RED line below in the Done section.

### 1.3 Implement (GREEN)

Replace the stub in `src/lib/domain/score.ts` with the real logic:

```typescript
export type Score = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;
export type ScoreError = 'out_of_range' | 'not_integer' | 'wrong_type';
export type ValidateScoreResult =
  | { ok: true; value: Score }
  | { ok: false; error: ScoreError };

export function validateScore(input: unknown): ValidateScoreResult {
  if (typeof input !== 'number' || Number.isNaN(input)) {
    return { ok: false, error: 'wrong_type' };
  }
  // Range check runs BEFORE the integer check so that Infinity / -Infinity
  // naturally fall into out_of_range (they pass the > 10 / < 1 comparisons
  // but are not integers). Also, for inputs like -0.5, "out_of_range" is the
  // more user-meaningful error than "not_integer".
  if (input < 1 || input > 10) {
    return { ok: false, error: 'out_of_range' };
  }
  if (!Number.isInteger(input)) {
    return { ok: false, error: 'not_integer' };
  }
  return { ok: true, value: input as Score };
}
```

Run: `npm test -- score.test`
Expected: all tests pass. Record below.

### 1.4 Regression check

```
npm test
```

Expected: the new `score.test.ts` passes; the `_scaffold` test still fails (we delete it in Step 2). Confirm the score tests run + pass and nothing else regressed.

### 1.5 Refactor

The implementation is already minimal. Likely nothing to refactor. State "none needed" if so.

If you do refactor, run `npm test` again after each change. GREEN must stay GREEN.

### 1.6 Walkthrough

Not applicable — pure domain layer, no UI.

### 1.7 Checkpoint

Safe to commit after Step 1 if you also want to commit Step 2 separately. The repo state after Step 1:

- `src/lib/domain/score.ts` exists, exports `Score`, `ScoreError`, `ValidateScoreResult`, `validateScore`
- `src/lib/domain/__tests__/score.test.ts` exists, all green
- `src/lib/_scaffold/` still exists with its failing test
- Run `npm test` shows: 1 failed (`_scaffold`), N passed (score)

Commit message:

```
score-validation/step-1: domain Score type + validateScore

Acceptance criteria addressed:
- AC1: accepts integer scores 1-10
- AC2/AC3: rejects out-of-range with 'out_of_range'
- AC4/AC5: rejects non-integers with 'not_integer'
- AC6: rejects non-number input with 'wrong_type'

Tests: 27+ new (one per it.each row), all passing
_scaffold test still failing — retired in step 2
```

---

## Done (filled in during `/build-step`)

- [x] AC1: `accepts integer score 1-10` — test `score.test.ts:validateScore — accepts valid scores` GREEN (10 cases via `it.each`)
- [x] AC2: `rejects above 10` — test `score.test.ts:rejects out-of-range > above 10` GREEN (11, 100, +Infinity)
- [x] AC3: `rejects below 1` — test `score.test.ts:rejects out-of-range > below 1` GREEN (0, -1, -Infinity)
- [x] AC4: `rejects 4.5` — test `score.test.ts:rejects non-integer > 4.5` GREEN
- [x] AC5: `rejects decimals` — test `score.test.ts:rejects non-integer > decimal` GREEN (3.1, 5.999)
- [x] AC6: `rejects wrong type` — test `score.test.ts:rejects wrong type` GREEN (string, null, undefined, NaN, object, array, boolean)
- [x] RED captured: `npm test -- score.test` → 19 failed | 7 passed (26) on 2026-05-26. The 7 passes were the wrong_type tests, passing accidentally because the stub always returns `wrong_type`. The 19 failures were the valid-input, range, and not_integer tests — meaningful assertion mismatches.
- [x] GREEN captured: `npm test -- score.test` → 26 passed (26) on 2026-05-26
- [x] Full suite (regression): `npm test` → 1 failed (`_scaffold` — expected, retired in step 2) | 26 passed (27 total). No score-test regressions.
- [x] Type check clean: `npm run typecheck` → no output, exit 0
- [x] Lint: no-op (placeholder script per package.json)
- [x] No new HIGH gate findings (pure domain layer; no I/O, no network, no secrets, no telemetry, no new deps)
- [x] No walkthrough (pure domain layer, no UI)
- [x] Refactor: none needed — the 4-branch function is minimal; magic numbers `1`/`10` left inline because the literal type `1 | 2 | ... | 10` is the actual source of truth, and constants would be a single-use abstraction

---

## What this step does NOT do

- Does NOT delete `src/lib/_scaffold/` — that's Step 2, kept separate to keep the RED → GREEN diff clean.
- Does NOT add a `parseScore` (throws) wrapper. Deferred to when a caller actually needs it.
- Does NOT add an `isScore` (type guard). Deferred to when a caller actually needs it.
- Does NOT add Zod schemas. Domain layer stays Zod-free per [.claude/conventions.md](../../../.claude/conventions.md).
- Does NOT touch the daily-entry UI, Directus client, or any other downstream caller.
