# Exertion tracking — cognitive / physical / emotional load

**Feature:** An optional, skippable deeper layer on the daily entry: three subjective exertion axes (cognitief / fysiek / emotioneel), each on a 4-point worded scale (geen / een beetje / behoorlijk / veel), capturing how much *load the user spent* in each domain that day.
**Version:** v2 (the prioritized next major feature after calendar-binding v1.6; sub-scores/exertion were always deferred to v2 in [daily-entry](../daily-entry/README.md))
**Status:** Planning (2026-06-05)
**Parent docs:** [docs/research/](../../research/) (ui-ux-patterns-from-visible-welltory §§1.2/1.5, pacing-and-crash-mitigation §2/§5, pais-pem-literature-review §2), [data-model.md](../../architecture/data-model.md), [design/brief.md](../../design/brief.md)

---

## Why this feature exists

The gevoelscore captures *how the day felt* — the outcome. The pacing/PEM research ([pacing-and-crash-mitigation.md](../../research/pacing-and-crash-mitigation.md)) is consistent and clear that the single highest-value *leading* signal is **exertion split across independent axes**: cognitive, physical, and emotional load each draw on the same energy envelope, and a step-counter sees only one of them. High load tends to be paid back as a delayed cost — the gevoelscore sagging 48–72h later.

This feature captures that input. The single overall gevoelscore stays the cardinal one-tap entry; exertion is an additive, optional layer for the days the user wants to record what they spent. Capturing it now lays the ground for the delayed-cost analysis later (deliberately a separate follow-up — see Future Considerations).

**Design provenance:** designed collaboratively 2026-06-05. The model moved through several framings (carry-forward → feeling-breakdown → exertion); the load/exertion reading was chosen deliberately as the research's highest-value version. Carry-forward + anti-drift were considered and dropped (exertion varies day to day, so pre-filling yesterday is usually wrong).

## User need

On a day where the user did a lot — or notably little — they want to record the *shape* of the load, not just the felt result, so that over time the connection between exertion and the delayed cost becomes legible. It must never slow down the one-tap score: on a brainfog day the user taps the score and is done; on a reflective day they can open one row and place three quick taps.

## What this feature ships

1. A nullable **`exertion` JSON field** on `day_entries`: `{ cognitive, physical, emotional }`, each an integer 1–4 or null.
2. A pure-TS domain validator **`validateExertion`**, wired into the `validateDayEntry` composer.
3. **API + route** wiring: the day-entries client surfaces and persists exertion; the write route validates it.
4. An **`<ExertionSection>`** UI: an always-present collapsed "Inspanning" row below score/note/tags in the daily popout (today *and* past-day edits), expandable to three worded 4-point axis pickers, each saving optimistically.

**Deliberately deferred (separate features):**
- The **48–72h delayed-cost / lag analysis** that correlates exertion against the later gevoelscore. That is the *payoff*, but it is a much larger analysis+visualisation feature. This feature only captures and displays the day's own exertion.
- A **4th `social` axis** (the research lists cognitive/emotional/physical/social). Three axes were chosen; social is a future-consideration add.
- **Feeling-breakdown** (decomposing the gevoelscore itself). The empty `sub_scores` column stays reserved for it.

## Acceptance criteria

**Domain (Step 1):**
- [ ] AC1: `validateExertion(null)` → `{ ok: true, value: null }`.
- [ ] AC2: `validateExertion({ cognitive: 1, physical: 4, emotional: null })` → ok (each field integer 1–4 or null).
- [ ] AC3: `validateExertion` rejects per-field out-of-range with a field-specific error: `0`, `5`, `2.5` on any axis → `invalid_cognitive` / `invalid_physical` / `invalid_emotional`.
- [ ] AC4: `validateExertion` rejects bad shape (missing key, extra key, empty object, non-object, array) → `invalid_shape` / `wrong_type`.
- [ ] AC5: `validateDayEntry` accepts an entry with `exertion` populated and with `exertion: null`; rejects a bad exertion value with `invalid_exertion`; rejects an entry *missing* the `exertion` key with `invalid_shape` (exact-key-set composer).

**Schema (Step 2):**
- [ ] AC6: `day_entries` has a nullable `exertion` column of type `json`; applying the migration script twice is idempotent (no error, no duplicate).
- [ ] AC7: `verify-schema.mjs` asserts the `exertion` column exists and is nullable; the frontend Directus role can read and write it.

**API + route (Step 3):**
- [ ] AC8: Reading a row persists exertion round-trip: `flatten()` surfaces a stored `{cognitive,physical,emotional}`; a row with SQL `NULL` exertion yields `exertion: null`.
- [ ] AC9: `upsertDayEntry` with `{ exertion }` in the patch persists it; a patch carrying *only* exertion leaves score/note/tags untouched; a patch omitting exertion leaves a previously-stored exertion untouched.
- [ ] AC10: `PUT /api/day-entries/[date]` validates the `exertion` body field via `validateExertion`; an invalid value returns `400 invalid_request` with no field-by-field leak; a valid value persists and returns the canonical post-write shape.

**UI (Step 4):**
- [ ] AC11: A collapsed "Inspanning" row appears below the tags in the daily popout, on today and on a past-day edit. Collapsed by default; the score path above it is unaffected.
- [ ] AC12: Expanding reveals three axes — cognitief, fysiek, emotioneel — each a row of four options labelled geen / een beetje / behoorlijk / veel (rendered word + position, **no colour scale**; only the selected option carries the accent).
- [ ] AC13: Tapping an option saves immediately via `useDayEntryUpsert` (optimistic, revert on error); re-tapping the same value is a no-op; axes are independent; an untouched axis stays `null`.
- [ ] AC14: Score-only entry still saves with one tap and never requires touching exertion; a timed good-day flow that skips exertion stays ≤ 10s.
- [ ] AC15: Touch targets ≥ 48×48; text ≥ 17px; every option keyboard-operable with a visible focus ring; `prefers-reduced-motion` respected; axe scan clean; the expandable row announces its state to assistive tech.

## Technical constraints

- **Online-first** (per [ADR 0002](../../decisions/0002-pwa-with-directus-backend.md)): exertion saves are network writes; on failure the optimistic value reverts with the existing non-blocking error state. No offline queue.
- **Storage**: new `exertion` JSON column on the existing `day_entries` collection, added via an **idempotent Directus REST script** in `directus/scripts/` (one-POST rule; never `schema apply`). Accessed through `src/lib/api/day-entries.ts`; validated by the pure-TS domain layer.
- **No new dependencies.**
- **No colour-coded scale** ([design/brief.md](../../design/brief.md) Forbidden): the worded option is the meaning; the accent fills only the selected option.
- **Copy**: reflective Dutch in `src/copy.ts`; no em-dash, no exclamation, no second-person questions.
- **Accessibility**: WCAG 2.2 AA + brainfog floor (≥48px targets, ≥17px text, ≤200ms motion, max 5 primary actions visible — the collapsed row keeps the default surface within this).
- **Thumb-first**: the exertion controls are an input surface and live in the bottom input zone, consistent with the popout.
- **Reuse**: the optimistic save path is `useDayEntryUpsert(date)`; the exertion section is one more caller, not a new mechanism. No carry-forward / provenance flags (dropped).

## Test plan

| File | Cases (one per `it`) |
|------|----------------------|
| `src/lib/domain/__tests__/exertion.test.ts` | accepts null; accepts each axis 1–4 or null; rejects 0/5/decimal per axis with field error; rejects missing/extra key, empty object, non-object, array |
| `src/lib/domain/__tests__/day-entry.test.ts` (extend) | accepts entry with exertion populated; accepts exertion null; rejects bad exertion → `invalid_exertion`; rejects entry missing `exertion` key → `invalid_shape` |
| `src/lib/api/__tests__/day-entries.test.ts` (extend) | flatten surfaces stored exertion; NULL exertion → null; upsert persists exertion patch; exertion-only patch leaves score/note/tags; omitted exertion left untouched |
| `src/app/api/day-entries/[date]/__tests__/route.test.ts` (extend) | valid exertion persists + 200; invalid exertion → 400 invalid_request; exertion absent from body still succeeds |
| `directus/scripts/verify-schema.mjs` (extend) | exertion column exists, type json, is_nullable true |
| `src/components/__tests__/exertion-section.test.tsx` | collapsed by default; expands on activation; three axes render four worded options; selected option carries accent only; tap calls save with right patch; re-tap no-op; keyboard + role/state announced |
| `tests/e2e/exertion.spec.ts` | skip-exertion good-day flow ≤10s; expand + set one axis persists across reload; axe clean |

## Cardinal-principle impact

| Principle | Impact | How we stay inside |
|-----------|--------|--------------------|
| One-tap entry | Additive only | Score still saves on first tap; exertion is below it, collapsed, optional. Never a required field, never a gate. |
| Sub-10-second flow | Neutral when skipped | The collapsed row adds one element, not one decision. Walkthrough stopwatches a skip-exertion flow ≤10s (AC14). |
| Brainfog-friendly | Positive (worded scale) | 4 worded options beat a 10-point ruler; collapsed by default keeps density low (one extra row, within the max-5 rule). |
| No unsolicited notifications / ads / analytics | None | No telemetry; no new deps. |
| User-owned data | Stays in Directus | Exertion is a `day_entries` column in the author's own Directus; no third party. |
| Export / delete still works | Covered | As a `day_entries` column, exertion is included in CSV/JSON export and full-delete automatically. |

## Alternatives considered

### Decision: dedicated `exertion` field vs. reusing the empty `sub_scores` column
- **Chose:** a new `exertion` JSON column. Exertion (an *input* / load) is semantically distinct from `sub_scores` (designed as a *feeling* deep-dive of the outcome). Honest naming; keeps both doors open.
- **Rejected:** overloading `sub_scores`. It is documented as a feeling decomposition on a 1–6 scale; repurposing it would mislead and would block ever shipping both.
- **Revisit when:** never expected; if feeling-breakdown is dropped permanently, `sub_scores` could be removed in a cleanup.

### Decision: 4-point worded scale (1–4, geen/een beetje/behoorlijk/veel) vs. 1–10 / 1–6
- **Chose:** 1–4 worded. Mirrors Visible's None/Mild/Moderate/Severe severity grid; lowest decision-load; the words carry meaning so a different scale than the 1–10 gevoelscore causes no confusion.
- **Rejected:** 1–10 (matches the gevoelscore but heavier per-axis × 3) and the existing 1–6 sub-score scaffold (built for a different, feeling concept).

### Decision: capture-only vs. capture + delayed-cost analysis in one feature
- **Chose:** capture + display today only. Shippable, low-risk, no charting.
- **Rejected:** bundling the 48–72h lag analysis. That is a large, separate analysis/visualisation feature; bundling would balloon scope and risk.

### Decision: drop carry-forward + anti-drift
- **Chose:** no carry-forward. Exertion varies day to day; pre-filling yesterday's load is usually wrong and would corrupt the signal.
- **Rejected:** the Visible-style "use previous answers" + anti-drift nudge. Those fit stable values (a feeling baseline), not daily-varying load.

## Future considerations

- **Delayed-cost surfacing** — correlate exertion (t) against the gevoelscore (t+2 / t+3), descriptively and hedged for confounding, framed as personal pattern-finding (never prescription). The reason this feature exists; planned as its own feature once enough exertion data accrues.
- **4th axis `social`** — the research's fourth load type. Add only if the three feel insufficient. The validator and column generalise to it.
- **Garmin/HRV corroboration (v2)** — a wearable layer becomes the objective leading edge the subjective exertion can be checked against.

## Privacy & permissions

- No new permissions, OAuth scopes, or browser APIs. No new data *shapes* leaving the device boundary beyond the existing day-entry write.
- Exertion lives in the author's self-hosted Directus; no third-party service touches it.
- **Export**: included automatically in any `day_entries` CSV/JSON export and in a Postgres dump. **Delete**: removed with the row on full-wipe — no orphan store.
- **Field-level permissions**: the new column must be readable + writable by the `gevoelscore-frontend-api` role. `day_entries` is already an allowed collection; Step 2 verifies the role's field access covers `exertion` (re-run `setup-permissions.mjs` only if field access is enumerated rather than `*`).

## v1.5 / v2 readiness

- `DayEntry` gains one nullable field; all existing nullable v1.5/v2 fields (`sub_scores`, `sleep_hours`, `garmin`, `health`, `weather`, `derived`, …) remain untouched.
- Follows the standard "store per day on `day_entries`" shape, so the future delayed-cost analysis and the Garmin layer slot in without migration.
- The native iOS app (v2 per ADR 0002) talks to the same `/api/day-entries` route; nothing here blocks it.

## Architecture

```
src/lib/domain/
  exertion.ts                 — NEW: Exertion type + validateExertion (1–4, {cognitive,physical,emotional})
  day-entry.ts                — MODIFY: add exertion to DayEntry, REQUIRED_KEYS, error union, composer
src/lib/api/
  day-entries.ts              — MODIFY: DirectusDayEntryRow.exertion, flatten() surfaces it, DayEntryPatch.exertion, upsert payload
src/app/api/day-entries/[date]/
  route.ts                    — MODIFY: validate exertion in body
src/components/
  exertion-section.tsx        — NEW: collapsed "Inspanning" row + three worded axis pickers
src/components/lab/
  quick-entry-flow.tsx        — MODIFY: mount <ExertionSection> below tags (today + past-day)
src/copy.ts                   — MODIFY: exertion labels + anchors (Dutch)
directus/scripts/
  add-exertion-field.mjs      — NEW: idempotent REST migration
  verify-schema.mjs           — MODIFY: assert exertion column
docs/architecture/data-model.md — MODIFY: document the exertion field
```

Key contract — the validator shape (reuses the `sub-score.ts` pattern):
```ts
export type ExertionValue = 1 | 2 | 3 | 4;
export type Exertion = {
  cognitive: ExertionValue | null;
  physical: ExertionValue | null;
  emotional: ExertionValue | null;
};
export function validateExertion(input: unknown):
  | { ok: true; value: Exertion | null }
  | { ok: false; error: 'wrong_type' | 'invalid_shape' | 'invalid_cognitive' | 'invalid_physical' | 'invalid_emotional' };
```

## Steps

1. **[Step 1 — Domain: `validateExertion` + composer](step-1-domain-validate-exertion.md)** — pure-TS validator (1–4, three axes) + wire into `validateDayEntry`. Independent of Step 2.
2. **[Step 2 — Directus `exertion` field + schema verify](step-2-directus-exertion-field.md)** — idempotent REST migration + `verify-schema.mjs` assertion + field-permission check. Independent of Step 1.
3. **[Step 3 — API client + write route](step-3-api-and-route.md)** — surface + persist exertion in `day-entries.ts`; validate in the route. Prerequisite: Steps 1 + 2.
4. **[Step 4 — `<ExertionSection>` UI + copy + e2e](step-4-exertion-section-ui.md)** — collapsed row, three worded pickers, optimistic save, walkthrough. Prerequisite: Step 3.

Build order: Steps 1 and 2 in parallel → Step 3 → Step 4 (the UX-risk step, last, while patterns settle).

## Key files

**New:** `src/lib/domain/exertion.ts`, `src/lib/domain/__tests__/exertion.test.ts`, `src/components/exertion-section.tsx`, `src/components/__tests__/exertion-section.test.tsx`, `directus/scripts/add-exertion-field.mjs`, `tests/e2e/exertion.spec.ts`.

**Modify:** `src/lib/domain/day-entry.ts` (+ test), `src/lib/api/day-entries.ts` (+ test), `src/app/api/day-entries/[date]/route.ts` (+ test), `src/components/lab/quick-entry-flow.tsx`, `src/copy.ts`, `directus/scripts/verify-schema.mjs`, `docs/architecture/data-model.md`.

**Patterns to extract:** `src/lib/domain/sub-score.ts` (validator shape), `src/components/note-field.tsx` + `tag-category-list.tsx` (how sections plug into `QuickEntryFlow` + call `useDayEntryUpsert`), `directus/scripts/setup-schema.mjs` (the `sub_scores` json field definition is the template for `exertion`).

## Verification

- **Automated**: Vitest (domain + api + route + component), `npm run typecheck`, `npm run lint`, `verify-schema.mjs` against prod, axe e2e.
- **Manual (cardinal gate)**: one-handed, low light, arm's length. Stopwatch a skip-exertion good-day flow ≤10s. Expand + set three axes ≤ a few seconds. Offline: set an axis with the network off → optimistic value reverts with the existing error state.
- **`npm run predeploy`** before any deploy (SSR-only bug catch).

## Quality gates

Run per [plan-feature](../../../.claude/commands/plan-feature.md) Phase 5. Summary for this additive, low-risk feature:
- **Cardinal**: PASS — one-tap preserved; collapsed-by-default keeps density inside the max-5 rule; ≤10s verified when skipped (AC14). No HIGH.
- **Privacy**: PASS — no new deps/permissions/third parties; export + delete cover the new column by construction. No HIGH.
- **Security**: PASS with always-applies items — the write route already enforces session + origin + rate-limit + generic 400; exertion adds one validated body field (A03/A08 covered by reusing the domain validator + existing route guards). No `dangerouslySetInnerHTML`, no new secret, no new dep. Per-step Standards-enforcement tables in each step file.
- **v1.5/v2**: PASS — one nullable field, standard per-day shape, existing fields untouched.
