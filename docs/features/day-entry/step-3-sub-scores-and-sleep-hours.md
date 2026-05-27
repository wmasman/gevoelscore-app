# Step 3: validateSubScore + validateSubScores + validateSleepHours

**Estimated time:** 35–45 min
**Test layer:** Domain
**Risk:** Low — three pure functions
**Prerequisite:** Step 2 complete

---

## Acceptance criteria

**validateSubScore (1–6 integer):**

- [ ] AC3.1: Accepts integers 1–6.
- [ ] AC3.2: Rejects 0, 7, decimals, non-number, NaN, +/-Infinity.

**validateSubScores (struct of 3 sub-scores or null):**

- [ ] AC3.3: `validateSubScores(null)` → `{ ok: true, value: null }`.
- [ ] AC3.4: Accepts `{ cognitive: 4, physical: null, mental: 5 }` (each field 1–6 or null).
- [ ] AC3.5: Rejects when any field is out of 1–6 (e.g. cognitive: 7 → `'invalid_cognitive'`).
- [ ] AC3.6: Rejects missing keys, extra keys, non-object inputs.

**validateSleepHours (0–24, decimals allowed, null OK):**

- [ ] AC3.7: `validateSleepHours(null)` → ok.
- [ ] AC3.8: `validateSleepHours(7.5)` → ok (decimals allowed — unlike scores).
- [ ] AC3.9: `validateSleepHours(0)` → ok, `validateSleepHours(24)` → ok (range inclusive).
- [ ] AC3.10: `validateSleepHours(-1)` → `'out_of_range'`, `validateSleepHours(25)` → `'out_of_range'`.
- [ ] AC3.11: Rejects non-number-non-null, NaN; +/-Infinity → `'out_of_range'`.

## Done criteria

- [x] All ACs GREEN
- [x] RED captured: `npm test` → 42 failed | 98 passed on 2026-05-26.
- [x] GREEN captured: `npm test` → 140/140 passing on 2026-05-26.
- [x] Full suite passes, typecheck clean.
- [x] No new HIGH gate findings.
- [x] Refactor: extracted private `validateFieldOrNull` helper in `sub-score.ts` to keep the three per-field branches symmetric and avoid duplicated null-check boilerplate.
