# Step 3: API client + write route — surface and persist exertion

**Estimated time:** 1–1.5 hours
**Test layer:** API client + route handler
**Risk:** Medium — touches the upsert path; must not regress the existing score/note/tags save semantics.
**Prerequisite:** Step 1 (validator + `DayEntry.exertion`) **and** Step 2 (the column exists).

---

## Acceptance criteria (this step)

- [ ] AC8: `flatten()` surfaces a stored exertion; a row with SQL `NULL` exertion → `exertion: null`. (Contrast with `sub_scores`, which `flatten` hardcodes to null — exertion must be *real*.)
- [ ] AC9: `upsertDayEntry` with `{ exertion }` in the patch persists it; a patch carrying *only* exertion leaves score/note/tags untouched; a patch omitting exertion leaves a stored exertion untouched.
- [ ] AC10: `PUT /api/day-entries/[date]` validates the `exertion` body field via `validateExertion`; invalid → `400 invalid_request` (generic, no field leak); valid → persists + returns the canonical post-write shape. Exertion absent from the body still succeeds (partial PUT).

## Technical constraints

- `flatten()` must include `exertion` (read `row.exertion`; trust the DB shape or pass through `validateExertion` defensively and coerce failure to `null` — choose pass-through-with-validation for safety, matching the "throw/degrade at the boundary" stance).
- `DayEntryPatch` gains `exertion?: Exertion | null`. In `upsertDayEntry`, add it to the update/create payload **only when present in the patch** (`'exertion' in patch`), exactly like `note` — it is a plain column on `day_entries`, not an M2M relation.
- Route handler validates `exertion` with the domain validator before calling the client; on failure returns the existing generic `400 invalid_request`. No new error vocabulary leaked.
- Reuse the existing route guards (session via `getValidatedSession`, origin check, rate-limit on write) — do not re-implement; exertion is just one more validated field.

### Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01,A03,A04,A07,A08 | Modifies existing | guards already present; adds one validated body field. Re-verify origin check + body validation still wrap the new field. |
| New collection storing user data | GDPR Art 9 | No | existing collection/field |
| New dependency | ADR/rationale | No | — |
| `dangerouslySetInnerHTML` | A03 | No | — |
| New env var with secret | A02,A05 | No | — |
| New telemetry dep | Cardinal no-telemetry | No | — |

## Test plan

| File | Cases |
|------|-------|
| `src/lib/api/__tests__/day-entries.test.ts` (extend) | flatten surfaces `{cognitive,physical,emotional}`; NULL → null; upsert with exertion patch persists; exertion-only patch does not send score/note/tag ops; omitted exertion not overwritten |
| `src/app/api/day-entries/[date]/__tests__/route.test.ts` (extend) | valid exertion → 200 + persisted; `exertion: { cognitive: 7 }` → 400 invalid_request; body without exertion → 200 (unchanged) |

> Mirror the existing mocking style in those test files (they already stub the SDK client / `getValidatedSession`). Add `exertion` to any shared row fixture so existing assertions still pass the exact-shape `DayEntry`.

## Done criteria

- [ ] All ACs GREEN; RED then GREEN captured.
- [ ] Existing day-entries + route tests still green (fixtures updated with `exertion`).
- [ ] `npm run typecheck` + `npm run lint` clean (the `DayEntry` exact shape now requires `exertion` everywhere it is constructed — typecheck is the safety net).
- [ ] No HIGH gate findings.

---

## Execution order

### 3.1 Tests (RED)
Extend both test files per the plan. Run:
```
npm test -- day-entries route
```
Must FAIL (flatten lacks exertion; patch path ignores it; route doesn't validate it).

### 3.2 Implement (GREEN)
- `src/lib/api/day-entries.ts`: add `exertion: unknown` to `DirectusDayEntryRow`; in `flatten()` replace the absent field with a real surfaced value (validate → value or null); add `exertion?` to `DayEntryPatch`; in `upsertDayEntry` create-payload and update-payload, include `exertion` when `'exertion' in patch`.
- `src/app/api/day-entries/[date]/route.ts`: after the existing body parse, if `exertion` is present run `validateExertion`; on failure return the existing generic 400; pass the validated value into the patch.
Run again — PASS.

### 3.3 Regression
```
npm test
```
All green. Confirm the optimistic save path is untouched for score/note/tags.

### 3.4 Refactor
Keep the patch-assembly symmetric with `note`. No new abstraction.

### 3.5 Checkpoint
Commit: `feat(exertion/step-3): persist + surface exertion through api client and write route`.

---

## What this step does NOT do
No UI (Step 4). Does not change the read range query shape beyond surfacing the already-requested `*` fields (exertion comes back under `'*'` automatically). Does not add exertion to any chart/aggregate (that is the deferred delayed-cost feature).
