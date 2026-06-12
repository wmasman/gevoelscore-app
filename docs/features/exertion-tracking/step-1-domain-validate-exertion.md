# Step 1: Domain — `validateExertion` + composer wiring

**Estimated time:** 45–60 min
**Test layer:** Domain (pure TS)
**Risk:** Low–Medium — the validator is trivial; the *ripple* into the exact-key-set `validateDayEntry` composer (and its fixtures) is where regressions hide.
**Prerequisite:** none (independent of Step 2).

---

## Acceptance criteria (this step)

- [ ] AC1: `validateExertion(null)` → `{ ok: true, value: null }`.
- [ ] AC2: `validateExertion({ cognitive, physical, emotional })` with each field an integer 1–4 or null → ok.
- [ ] AC3: per-field out-of-range (`0`, `5`, `2.5`) → `invalid_cognitive` / `invalid_physical` / `invalid_emotional`.
- [ ] AC4: bad shape (missing key, extra key, empty object, non-object, array, number, string, boolean) → `invalid_shape` (object-ish) or `wrong_type` (non-object).
- [ ] AC5: `validateDayEntry` accepts an entry with `exertion` populated and with `exertion: null`; rejects a bad exertion with `invalid_exertion`; rejects an entry *missing* the `exertion` key with `invalid_shape`.

## Technical constraints

- Pure TS. No platform imports (no Zod/Directus/React/Next). No I/O, no side effects.
- Result-style return matching `validateScore` / `validateSubScores`.
- `validateDayEntry` must call `validateExertion` internally — no duplicated logic.
- Mirror `src/lib/domain/sub-score.ts` exactly in structure (struct-or-null, per-field `validateFieldOrNull` helper), changing only: range 1–4, keys `{cognitive, physical, emotional}`, error names.

### Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01,A03,A07,A08 | No | domain-only |
| New collection storing user data | GDPR Art 9 | No | no persistence |
| New dependency | ADR/rationale | No | pure TS |
| `dangerouslySetInnerHTML` | A03 | No | — |
| New env var with secret | A02,A05 | No | — |
| New telemetry dep | Cardinal no-telemetry | No | — |

## Test plan

**File**: `src/lib/domain/__tests__/exertion.test.ts` (new) — model on [`sub-score.test.ts`](../../../src/lib/domain/__tests__/sub-score.test.ts).

```typescript
import { describe, expect, it } from 'vitest';
import { validateExertion } from '../exertion';

describe('exertion', () => {
  it('given null, when validated, then it is accepted as null', () => {
    expect(validateExertion(null)).toEqual({ ok: true, value: null });
  });

  it('given each axis an integer 1–4 or null, when validated, then accepted', () => {
    const input = { cognitive: 1, physical: 4, emotional: null };
    expect(validateExertion(input)).toEqual({ ok: true, value: input });
  });

  it('given all axes null, when validated, then accepted', () => {
    const input = { cognitive: null, physical: null, emotional: null };
    expect(validateExertion(input)).toEqual({ ok: true, value: input });
  });

  describe('per-field range', () => {
    it.each([0, 5, 2.5, Number.POSITIVE_INFINITY])(
      'given cognitive=%s, when validated, then invalid_cognitive',
      (bad) => {
        expect(validateExertion({ cognitive: bad, physical: null, emotional: null }))
          .toEqual({ ok: false, error: 'invalid_cognitive' });
      },
    );
    it('given physical=0, then invalid_physical', () => {
      expect(validateExertion({ cognitive: null, physical: 0, emotional: null }))
        .toEqual({ ok: false, error: 'invalid_physical' });
    });
    it('given emotional=2.5, then invalid_emotional', () => {
      expect(validateExertion({ cognitive: null, physical: null, emotional: 2.5 }))
        .toEqual({ ok: false, error: 'invalid_emotional' });
    });
  });

  describe('shape', () => {
    it('given missing key, then invalid_shape', () => {
      expect(validateExertion({ cognitive: 1, physical: 2 }))
        .toEqual({ ok: false, error: 'invalid_shape' });
    });
    it('given extra key, then invalid_shape', () => {
      expect(validateExertion({ cognitive: 1, physical: 2, emotional: 3, extra: 1 }))
        .toEqual({ ok: false, error: 'invalid_shape' });
    });
    it('given empty object, then invalid_shape', () => {
      expect(validateExertion({})).toEqual({ ok: false, error: 'invalid_shape' });
    });
    it.each([
      ['number', 3], ['string', '{}'], ['array', [1, 2, 3]], ['boolean', true],
    ])('given %s, then wrong_type', (_l, input) => {
      expect(validateExertion(input)).toEqual({ ok: false, error: 'wrong_type' });
    });
  });
});
```

**File**: `src/lib/domain/__tests__/day-entry.test.ts` (extend) — add to the existing composer suite:

```typescript
// inside the existing describe('validateDayEntry', ...)
it('accepts an entry with exertion populated', () => {
  const entry = { ...validBaseEntry, exertion: { cognitive: 2, physical: 4, emotional: 1 } };
  const r = validateDayEntry(entry);
  expect(r.ok).toBe(true);
});
it('accepts an entry with exertion null', () => {
  expect(validateDayEntry({ ...validBaseEntry, exertion: null }).ok).toBe(true);
});
it('rejects a bad exertion value with invalid_exertion', () => {
  const r = validateDayEntry({ ...validBaseEntry, exertion: { cognitive: 9, physical: null, emotional: null } });
  expect(r).toEqual({ ok: false, error: 'invalid_exertion' });
});
it('rejects an entry missing the exertion key with invalid_shape', () => {
  const { exertion, ...withoutExertion } = { ...validBaseEntry, exertion: null };
  expect(validateDayEntry(withoutExertion)).toEqual({ ok: false, error: 'invalid_shape' });
});
```

> **Note for the implementer:** the existing `day-entry.test.ts` builds a valid entry inline. Find that helper/literal and add `exertion: null` to it (otherwise every existing composer test breaks on the exact-key-set check). This is the ripple to watch.

## Done criteria

- [ ] Every AC GREEN; RED captured before implementation; GREEN captured after.
- [ ] Full suite passes (the existing ~119 day-entry composer assertions still green after the fixture gains `exertion`).
- [ ] `npm run typecheck` + `npm run lint` clean.
- [ ] No new HIGH gate findings.
- [ ] Refactor pass complete (or "none needed").

---

## Execution order

### 1.1 Tests (RED)
Create `exertion.test.ts` with the block above; add the composer cases to `day-entry.test.ts`. Run:
```
npm test -- exertion day-entry
```
Must FAIL: `validateExertion` does not exist; composer rejects the new key.

### 1.2 Implement (GREEN)
- Create `src/lib/domain/exertion.ts` — copy `sub-score.ts`, change range to 1–4, keys to `{cognitive, physical, emotional}` (sorted key list: `['cognitive', 'emotional', 'physical']`), error names.
- Modify `src/lib/domain/day-entry.ts`:
  - add `exertion: Exertion | null` to `DayEntry` (import the type),
  - add `'exertion'` to `REQUIRED_KEYS` (keep the array sorted),
  - add `'invalid_exertion'` to `DayEntryError`,
  - call `validateExertion(obj.exertion)` and return `invalid_exertion` on failure,
  - include `exertion: exertionResult.value` in the returned value.
Run again — must PASS.

### 1.3 Regression
```
npm test
```
All green. Pay attention to any other module constructing a `DayEntry` literal (api flatten is handled in Step 3; if typecheck flags it before Step 3, add `exertion: null` there as a stopgap and note it).

### 1.4 Refactor
Confirm `exertion.ts` and `sub-score.ts` are structurally parallel; do **not** prematurely extract a shared generic (two callers with hard-coded ranges is fine — same call the day-entry domain made for `validateSubScore` vs `validateScore`).

### 1.5 Checkpoint
Commit: `feat(exertion/step-1): validateExertion domain validator + composer wiring`.

---

## What this step does NOT do
No schema change (Step 2), no API/route wiring (Step 3), no UI (Step 4). The `flatten()` in `day-entries.ts` may need `exertion: null` to typecheck — that is Step 3's job; a one-line stopgap is acceptable here only if typecheck demands it.
