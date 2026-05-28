# Score Validation

**Feature:** Domain-layer validation for the daily `Score` value (integer 1–10)
**Version:** v1
**Status:** Complete (2026-05-26)
**Parent doc:** [docs/REQUIREMENTS.md#user-requirements-v1](../../REQUIREMENTS.md) line 24; [docs/architecture/data-model.md "Score validation"](../../architecture/data-model.md)

---

## Overview

- **What:** A `Score` type and a `validateScore(input: unknown)` function in `src/lib/domain/`. Returns Result-style `{ ok, value }` or `{ ok, error }`. No I/O, no platform deps.
- **Why:** Every downstream feature (daily entry, CSV import, Directus read, dashboard) needs a single source of truth for what a valid score is. Domain-layer first means the rule is defined once and reused everywhere — and the first real `/build-step` cycle on the project lands on testable pure logic with no infrastructure dependency.
- **Impact:** Unlocks the daily-entry screen (UI form validation), CSV import row validation, and Directus response shape checks. Also retires the `_scaffold/` proof folder.

---

## User need

The user logs a score on a scale of 1–10 (integers only — half-values were considered and rejected in REQUIREMENTS.md line 24). The app must reject any input outside this set with a clear, specific reason, so the daily-entry UI can show useful feedback ("only whole numbers 1–10") instead of silently accepting bad data or showing a generic "invalid" error.

---

## Acceptance criteria

Each line becomes one `it` block.

- [ ] **AC1**: Given an integer between 1 and 10 inclusive, when `validateScore` is called, then it returns `{ ok: true, value }` with the same number.
- [ ] **AC2**: Given a number above 10 (`11`, `100`, `Infinity`), when validated, then it returns `{ ok: false, error: 'out_of_range' }`.
- [ ] **AC3**: Given a number below 1 (`0`, `-1`, `-Infinity`), when validated, then it returns `{ ok: false, error: 'out_of_range' }`.
- [ ] **AC4**: Given a half-value (`4.5`), when validated, then it returns `{ ok: false, error: 'not_integer' }`.
- [ ] **AC5**: Given a decimal in range (`3.1`, `5.999`), when validated, then it returns `{ ok: false, error: 'not_integer' }`.
- [ ] **AC6**: Given a non-number input (`'3'`, `null`, `undefined`, `NaN`, `{}`), when validated, then it returns `{ ok: false, error: 'wrong_type' }`.

---

## Technical constraints

- **No platform imports.** Pure TS. No `next/*`, no `@directus/sdk`, no Zod, no React. Per [.claude/conventions.md](../../../.claude/conventions.md) the domain layer is platform-free.
- **No I/O, no side effects.** Pure function. Same input → same output, every time.
- **Synchronous and fast.** Must run in << 1ms. Called from every keystroke-debounced form change in the future daily-entry screen.
- **Discriminated-union return.** `{ ok: true; value: Score } | { ok: false; error: ScoreError }`. TypeScript narrows on `r.ok`.

---

## Test plan

| File | Cases (one per `it`, mapped to AC) |
|------|------------------------------------|
| `src/lib/domain/__tests__/score.test.ts` | AC1: each of 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 accepted; AC2: out_of_range high; AC3: out_of_range low; AC4: not_integer (4.5); AC5: not_integer (3.1); AC6: wrong_type (string, null, undefined, NaN, object) |

AC1 will use `it.each` over `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` to keep the ten valid scores as ten discrete assertions without writing ten near-identical `it` blocks.

---

## Cardinal-principle impact

| Principle | Impact | How we stay inside |
|-----------|--------|--------------------|
| One-tap entry | Enables it | Validation result drives whether the tap "took" — fast enough to be invisible to the user |
| Sub-10-second flow | Enables it | Synchronous, no I/O, sub-millisecond — adds zero to the budget |
| Brainfog-friendly | Enables it | Discriminated error type means the UI can show "only whole numbers 1–10" instead of "invalid", which helps on a 4-out-of-6 day |
| No unsolicited notifications / ads / analytics | N/A | No UI, no network, no logging |
| User-owned data | Enables it | Rejects bad input at the domain boundary before it reaches Directus |
| Export / delete still works | N/A | No persisted data introduced |

---

## Alternatives considered

### Decision: Result-style return value

- **Chose**: `{ ok: true; value: Score } | { ok: false; error: ScoreError }` — explicit, TypeScript-narrowable on `r.ok`, no exceptions to forget to catch.
- **Considered and rejected**:
  - **Throws on invalid** — concise but easy to forget to catch in form-handler code. Causes "uncaught exception in event handler" crashes if missed once. The throws-version is a one-line wrapper if a future caller wants it.
  - **Type-guard predicate only** (`isScore(input): input is Score`) — fine for narrowing but doesn't carry an error message. Form validation needs the reason, not just yes/no.
  - **Zod schema** (`z.number().int().min(1).max(6)`) — would mean the domain layer takes a Zod dep, which conflicts with [.claude/conventions.md](../../../.claude/conventions.md) ("domain — pure TS, no platform imports"). Zod stays in `src/lib/validation/` per data-model.md line 35. The day a CSV importer needs Zod for the whole row, the Zod schema for `score` can call `validateScore` internally and re-shape to Zod's error format.
- **Revisit when**: a second caller emerges that genuinely wants throws (e.g. a strict reader at the Directus boundary). At that point, add a one-line `parseScore` wrapper. No need to anticipate it now.
- **Migration path**: `function parseScore(x: unknown): Score { const r = validateScore(x); if (!r.ok) throw new Error(r.error); return r.value; }` — three lines, no change to existing callers.

---

## Future considerations

- **`parseScore` wrapper** (throws variant) — add when the Directus read boundary needs it. Until then, callers can wrap inline.
- **`isScore` type guard** — add when TypeScript narrowing inside `switch` / `if` becomes a pattern. Trivial to add later.
- **Zod re-export** — when CSV import lands, `src/lib/validation/csv-row.ts` will likely have a `z.custom<Score>()` that delegates to `validateScore`. No change to `score.ts` needed.
- **`SubScores` v2** — data-model.md line 144 specifies `cognitive | physical | mental` each follow the same `Score` validation. The `Score` type defined here is reused there verbatim.

---

## Privacy & permissions

User-control framing: nothing leaves the function. No telemetry, no logging, no I/O.

- **OAuth scopes / browser permissions requested**: none — pure logic.
- **Where the data lives**: the function takes an `unknown` and returns a Result. Nothing persists.
- **Data that leaves the author's infrastructure**: none.
- **Export coverage**: N/A — no new persisted field.
- **Delete coverage**: N/A — same.

---

## Security

Threat framing: this is a validation function on `unknown` input. The threats are: lying about its own return shape (TypeScript trust failure), leaking input into a log, or being a vector for prototype pollution / unsafe type coercion.

- **Access control**: N/A — no auth surface introduced.
- **In transit**: N/A — no network.
- **At rest**: N/A — no storage.
- **Injection / untrusted input**: input is `unknown`, validated via `typeof` and `Number.isInteger`. No `eval`, no string concat, no JSON parse, no Object/Array index lookup on user-controlled keys. Safe by construction.
- **Web surface**: N/A — pure logic, no DOM.
- **Permissions**: N/A.
- **PWA-specific**: N/A.
- **Build hygiene & logging**: function does not `console.log` its inputs. Error type is an opaque string literal, not the input value.
- **Supply chain**: zero new dependencies. (Confirms the domain layer's "platform-free" commitment in [conventions.md](../../../.claude/conventions.md).)

---

## v1.5 / v2 readiness

- **Directus schema impact**: none. This is domain-layer-only; the Directus `day_entries.score` column shape was already decided in [data-model.md](../../architecture/data-model.md) and isn't touched here.
- **`DayEntry` impact**: none — `DayEntry.score: Score` was already specified; this feature provides the type, not changes to its consumers.
- **Other schema impact**: none.
- **Integration shape**: N/A — no integrations.
- **Deferred assumptions**: the `SubScores` (v2) cognitive/physical/mental fields reuse this `Score` type verbatim per data-model.md line 144 — no change needed when v2 lands.

---

## Architecture

### File tree

```
src/lib/domain/
  score.ts                       — Score type, ScoreError type, validateScore function
  __tests__/
    score.test.ts                — AC1–AC6, one describe per behavior cluster
```

Deletion in the same feature (Step 2):

```
src/lib/_scaffold/               — DELETED
vitest.config.ts                 — _scaffold exclusion line removed from coverage config
```

### Key types

```typescript
export type Score = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;

export type ScoreError = 'out_of_range' | 'not_integer' | 'wrong_type';

export type ValidateScoreResult =
  | { ok: true; value: Score }
  | { ok: false; error: ScoreError };

export function validateScore(input: unknown): ValidateScoreResult;
```

### Integration with existing code

- **Imports from `src/lib/api/`**: none — domain layer doesn't import from API.
- **Imports from `src/lib/validation/`**: none — domain layer doesn't import from validation.
- **New hooks / app routes / components**: none.
- **Existing callers that change**: none yet. Future callers will be: the daily-entry form (UI), CSV import row validation (`src/lib/validation/csv-row.ts`), Directus response shape validation (`src/lib/validation/day-entry.ts`).

---

## Steps

### Step 1: Implement Score type + validateScore
- Write the test file, run it RED, implement the function, run it GREEN, refactor.
- See: [step-1-validate-score.md](step-1-validate-score.md)

### Step 2: Retire the `_scaffold` proof
- Delete `src/lib/_scaffold/`, update `vitest.config.ts` coverage exclude.
- See: [step-2-remove-scaffold.md](step-2-remove-scaffold.md)

---

## Key Files

### New files to create

| File | Contents |
|------|----------|
| `src/lib/domain/score.ts` | `Score` type, `ScoreError` type, `ValidateScoreResult` type, `validateScore()` function |
| `src/lib/domain/__tests__/score.test.ts` | AC1–AC6 with one nested `describe` per error category |

### Files to modify

| File | Change |
|------|--------|
| `vitest.config.ts` | Remove `'**/_scaffold/**'` from coverage `exclude` list |

### Files to delete

| File | Reason |
|------|--------|
| `src/lib/_scaffold/_scaffold.ts` | Proof scaffold — first real domain test takes over |
| `src/lib/_scaffold/__tests__/_scaffold.test.ts` | Same |
| `src/lib/_scaffold/README.md` | Same |

### Reference docs (patterns to extract from)

| Doc | What to extract |
|-----|-----------------|
| [docs/REQUIREMENTS.md#user-requirements-v1 line 24](../../REQUIREMENTS.md) | "Integer 1–10 only, no halves, no decimals" — matches original Google Sheet's 1–10 column |
| [docs/architecture/data-model.md "Score validation"](../../architecture/data-model.md) | Test list, type definition, validation rules |
| [.claude/testing.md](../../../.claude/testing.md) | Test file shape, Given/When/Then sentence pattern |

---

## Verification

### Automated

1. Tests: `npm test -- score.test`
2. Types: `npm run typecheck`
3. Lint: `npm run lint` (no-op for now per package.json; will be wired up when ESLint lands)
4. Full suite: `npm test`

### Manual

1. None — this is pure logic, no UI. No browser / device walkthrough applies.
2. After Step 2: verify `npm test` finds only the new score tests (the scaffold sanity test is gone).

### Testing strategy

This feature establishes the pattern for all future domain-layer tests:

- One `describe('<module>', ...)` outer block.
- One `describe('<behavior>', ...)` nested block per error category (or per behavior cluster).
- `it` strings are full Given/When/Then sentences — they double as documentation when the suite runs.
- `it.each` for tabular cases (e.g. AC1's six valid scores) — keeps the assertion concrete while compacting near-identical lines.
- Arrange / Act / Assert sections visually separated by blank lines.

The next domain feature (`DayEntry` types, `Tag` types, date validation) follows the same shape.
