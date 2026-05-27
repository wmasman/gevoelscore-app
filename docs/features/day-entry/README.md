# DayEntry domain

**Feature:** Domain-layer validation for the rest of `DayEntry`'s fields — date, note, tag_ids, sub_scores, sleep_hours — plus the composer that validates a whole DayEntry.
**Version:** v1
**Status:** Complete (2026-05-26)
**Tests:** 119 tests across 6 new files (170 total project tests, all GREEN)
**Parent doc:** [docs/architecture/data-model.md "DayEntry"](../../architecture/data-model.md)

---

## Overview

- **What:** Pure-TS validators for every `DayEntry` field except `score` (already shipped via [score-validation](../score-validation/README.md)), plus `validateDayEntry()` — the composer that checks a whole `DayEntry` shape end-to-end.
- **Why:** Every downstream feature (daily-entry UI form validation, CSV import row validation, Directus response shape validation) needs a single source of truth for what a valid DayEntry looks like. Defining it in the platform-free domain layer means the rule is written once.
- **Impact:** Unlocks the Daily/Home screen, CSV import (the 1.363-day historical sheet), Directus response parsing, and the past-day Edit pattern's "valid before save" check.

---

## User need

The user logs entries that must be coherent: a real date, a sensible score, optional text and tags, and timestamps that respect causality. The system must reject invalid input at the domain boundary so the UI can give specific feedback ("note can't be only whitespace", "duplicate tags") rather than generic "save failed" errors, and so the Directus persistence layer never sees malformed data.

---

## Acceptance criteria

Each line becomes one or more `it` blocks. Sub-divided by step.

**Step 1 — `validateDate`:**

- [ ] AC1.1: Accepts a real calendar date in `YYYY-MM-DD` format that is today or in the past.
- [ ] AC1.2: Rejects strings not matching `^\d{4}-\d{2}-\d{2}$` (`'2026/05/26'`, `'May 26'`, `'2026-5-26'`).
- [ ] AC1.3: Rejects calendar-impossible dates (`'2026-02-30'`, `'2026-13-01'`, `'2025-02-29'` — 2025 is not a leap year).
- [ ] AC1.4: Rejects future dates (tomorrow and beyond).
- [ ] AC1.5: Rejects non-string inputs (number, null, undefined, object).

**Step 2 — `normalizeNote` + `validateTagIds`:**

- [ ] AC2.1: `normalizeNote(null)` → `{ ok: true, value: null }`.
- [ ] AC2.2: `normalizeNote('')`, `normalizeNote('   ')`, `normalizeNote('\n\t ')` → `{ ok: true, value: null }` (whitespace-only normalizes to null).
- [ ] AC2.3: `normalizeNote('hello')` → `{ ok: true, value: 'hello' }`.
- [ ] AC2.4: `normalizeNote('  hello  ')` → `{ ok: true, value: 'hello' }` (leading/trailing whitespace trimmed).
- [ ] AC2.5: Rejects non-string-non-null inputs (number, object, array, boolean).
- [ ] AC2.6: `validateTagIds([])` → `{ ok: true, value: [] }`.
- [ ] AC2.7: `validateTagIds(['a','b'])` → `{ ok: true, value: ['a','b'] }`.
- [ ] AC2.8: `validateTagIds(['a','a'])` → `{ ok: false, error: 'duplicates' }`.
- [ ] AC2.9: Rejects non-array inputs.
- [ ] AC2.10: Rejects arrays containing non-string elements.

**Step 3 — `validateSubScore` + `validateSubScores` + `validateSleepHours`:**

- [ ] AC3.1: `validateSubScore` accepts integers 1–6.
- [ ] AC3.2: `validateSubScore` rejects 7, 0, decimals, non-number, NaN, Infinity.
- [ ] AC3.3: `validateSubScores(null)` → `{ ok: true, value: null }`.
- [ ] AC3.4: `validateSubScores({ cognitive: 4, physical: null, mental: 5 })` → ok (per-field 1–6 or null).
- [ ] AC3.5: `validateSubScores({ cognitive: 7, ... })` → rejected (cognitive out of 1–6).
- [ ] AC3.6: `validateSubScores` rejects missing keys / extra keys / non-object inputs.
- [ ] AC3.7: `validateSleepHours(null)` → ok.
- [ ] AC3.8: `validateSleepHours(7.5)` → ok (decimals allowed, unlike scores).
- [ ] AC3.9: `validateSleepHours(0)` → ok, `validateSleepHours(24)` → ok (range inclusive).
- [ ] AC3.10: `validateSleepHours(-1)` → rejected, `validateSleepHours(25)` → rejected.
- [ ] AC3.11: Rejects non-number-non-null, NaN, Infinity.

**Step 4 — `validateDayEntry` composer:**

- [ ] AC4.1: Accepts a minimal valid v1 DayEntry (date, score, note, tag_ids, timestamps, v1.5/v2 fields all null/empty).
- [ ] AC4.2: Accepts a DayEntry with `sub_scores` populated (v2 forward-compat).
- [ ] AC4.3: Rejects with `'invalid_date'` when date fails.
- [ ] AC4.4: Rejects with `'invalid_score'` when score fails.
- [ ] AC4.5: Normalizes note (whitespace → null) and returns the normalized value.
- [ ] AC4.6: Rejects with `'invalid_tag_ids'` when tag_ids has duplicates.
- [ ] AC4.7: Rejects with `'invalid_timestamp_order'` when `created_at > updated_at`.
- [ ] AC4.8: Rejects with `'invalid_shape'` when input is not an object / missing required keys / extra keys.

---

## Technical constraints

- **No platform imports.** Pure TS. No Zod, no Directus, no React, no Next.
- **No I/O, no side effects.** Pure functions.
- **Result-style return for all validators**, matching `validateScore`'s contract.
- **Composer uses sub-validators internally** — no duplicated validation logic.

---

## Test plan

| File | Cases |
|------|-------|
| `src/lib/domain/__tests__/date.test.ts` | AC1.1–AC1.5 |
| `src/lib/domain/__tests__/note.test.ts` | AC2.1–AC2.5 |
| `src/lib/domain/__tests__/tag-ids.test.ts` | AC2.6–AC2.10 |
| `src/lib/domain/__tests__/sub-score.test.ts` | AC3.1–AC3.6 |
| `src/lib/domain/__tests__/sleep-hours.test.ts` | AC3.7–AC3.11 |
| `src/lib/domain/__tests__/day-entry.test.ts` | AC4.1–AC4.8 |

---

## Cardinal-principle impact

| Principle | Impact | How we stay inside |
|-----------|--------|--------------------|
| One-tap entry | Enables it | All validators run synchronously, sub-ms |
| Sub-10-second flow | Enables it | No I/O, no async; pure type-narrowing |
| Brainfog-friendly | Enables it | Specific error codes mean the UI can show specific feedback |
| No notifications / ads / analytics | N/A | Pure logic |
| User-owned data | Enables it | Bad data rejected at the boundary before reaching Directus |
| Export / delete still works | N/A | No persisted state introduced |

---

## Alternatives considered

### Decision: Hand-rolled `validateDate` instead of `Date.parse` or a date library

- **Chose:** Hand-roll regex + `Date` construction + round-trip check (parse the string, reconstruct, confirm bytes match).
- **Considered and rejected:**
  - **`Date.parse`** — too permissive (`Date.parse('2026-02-30')` returns a valid number; JS auto-rolls Feb 30 to March 2). Catches the wrong category of errors.
  - **`date-fns` / `dayjs`** — third-party dep. Domain layer is platform-free per [.claude/conventions.md](../../../.claude/conventions.md).
  - **`Temporal.PlainDate`** — not yet stable in Node 18+ / browsers. Re-evaluate when it ships natively.
- **Revisit when:** `Temporal` ships natively in all supported runtimes — then swap out the hand-rolled parser for the standard API.

### Decision: Separate `validateSubScore` (1–6) rather than parameterizing `validateScore`

- **Chose:** Separate function. Score is 1–10, SubScore is 1–6 — different semantics, different valid sets.
- **Considered and rejected:** `validateInteger(input, min, max)` — premature abstraction. Two callers with hard-coded ranges is fine.

---

## Privacy & permissions

Same as score-validation: pure functions, nothing leaves the call, no telemetry, no I/O. N/A across the board.

---

## Security

- Input is `unknown`. No `eval`, no string concat into anything sensitive, no JSON parse on inputs (the strings stay strings).
- `validateDate` uses a strict regex; reduces the input-shape space before any further processing.
- `validateTagIds` checks `Array.isArray` before iterating; no prototype-pollution path.
- Zero new dependencies — domain layer stays platform-free.
- Errors are opaque string literals, not echoed input — no PII leak via error payloads.

---

## v1.5 / v2 readiness

- **`DayEntry` impact:** the composer accepts all v1.5/v2 fields (`sub_scores`, `sleep_hours`, `special_event`, `project_entry_ids`, `calendar_event_ids`, `garmin`, `health`, `weather`, `derived`) as nullable / empty array. In v1, callers pass nulls/empties; in v1.5/v2 the same composer is extended with deep validation for the populated values.
- **Directus schema:** not touched by this feature — the schema lives in the Directus admin UI, the composer just validates what comes back over the wire.

---

## Architecture

```
src/lib/domain/
  date.ts                   — validateDate
  note.ts                   — normalizeNote
  tag-ids.ts                — validateTagIds
  sub-score.ts              — validateSubScore (1–6), validateSubScores ({c,p,m})
  sleep-hours.ts            — validateSleepHours (0–24, decimals allowed)
  day-entry.ts              — DayEntry type, validateDayEntry composer
  score.ts                  — already exists
  __tests__/
    date.test.ts
    note.test.ts
    tag-ids.test.ts
    sub-score.test.ts
    sleep-hours.test.ts
    day-entry.test.ts
    score.test.ts           — already exists
```

---

## Steps

### Step 1: `validateDate`
- See: [step-1-validate-date.md](step-1-validate-date.md)

### Step 2: `normalizeNote` + `validateTagIds`
- See: [step-2-note-and-tag-ids.md](step-2-note-and-tag-ids.md)

### Step 3: `validateSubScore` + `validateSubScores` + `validateSleepHours`
- See: [step-3-sub-scores-and-sleep-hours.md](step-3-sub-scores-and-sleep-hours.md)

### Step 4: `validateDayEntry` composer
- See: [step-4-day-entry-composer.md](step-4-day-entry-composer.md)

---

## Verification

`npm test`, `npm run typecheck`. No UI in this feature; no walkthrough.
