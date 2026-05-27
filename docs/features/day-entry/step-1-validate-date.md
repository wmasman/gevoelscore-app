# Step 1: validateDate

**Estimated time:** 30–45 min
**Test layer:** Domain
**Risk:** Low — single pure function, well-defined rules
**Prerequisite:** [score-validation](../score-validation/README.md) complete (sets the Result-style pattern this follows)

---

## Acceptance criteria

- [ ] AC1.1: Accepts real calendar dates in `YYYY-MM-DD` from `'2022-09-03'` (the user's first logging day) up to today.
- [ ] AC1.2: Rejects bad format (`'2026/05/26'`, `'May 26'`, `'2026-5-26'`, `'20260526'`, `''`, `'2026-05-26T00:00:00Z'`) → `'invalid_format'`.
- [ ] AC1.3: Rejects calendar-impossible (`'2026-02-30'`, `'2026-13-01'`, `'2026-00-15'`, `'2026-04-31'`, `'2025-02-29'` non-leap-year) → `'invalid_calendar_date'`.
- [ ] AC1.4: Accepts `'2024-02-29'` (leap year). Rejects tomorrow → `'future_date'`.
- [ ] AC1.5: Rejects non-string (number, null, undefined, object, Date) → `'wrong_type'`.

## Technical constraints

- Pure TS, zero deps.
- Synchronous.
- Uses `vi.setSystemTime` to pin "today" so the future-date tests are deterministic.

## Test plan

`src/lib/domain/__tests__/date.test.ts` — full code shipped in the implementation phase.

## Done criteria

- [x] All ACs GREEN
- [x] RED captured: `npm test` → 18 failed | 7 passed (date.test.ts) on 2026-05-26. The 7 passes were the wrong_type tests passing accidentally because the stub always returns `wrong_type`. The 18 failures were meaningful assertion mismatches.
- [x] GREEN captured: `npm test -- date.test` → 25 passed (25) on 2026-05-26.
- [x] Full suite passes: 51/51 after step.
- [x] Typecheck clean.
- [x] No new HIGH gate findings (pure domain, no I/O, no new deps).
- [x] Refactor: none needed — round-trip date check via Date reconstruction is the cleanest approach short of native `Temporal` (deferred to when it ships).
