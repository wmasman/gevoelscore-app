# Step 5: Reconciliation and cleanup

**Estimated time:** 1.5 hours
**Test layer:** Whatever the chosen reconciliation path requires. Most likely: existing-test removal + e2e updates + a manual real-device validation pass on the deployed app.
**Risk:** Low-Medium. Code risk is small (mostly deletions or route changes). The real risk is that the post-deploy mobile validation reveals issues — that's why this step is structured as "validate first, then commit to the cleanup".
**Prerequisite:** [Steps 0–4](README.md#steps) shipped and deployed to the dev environment.

> **Status: outline.** Full step detail depends entirely on the reconciliation decision made in Step 4.

---

## Scope summary

Two distinct sub-steps, in order:

### 5.A — Post-deploy mobile validation

Open the deployed dev environment on the iPhone PWA. Run the full validation checklist that was deferred during prototype testing:

1. **iOS keyboard handling** during the note step — does the panel stay above the keyboard? Are the back/forward buttons reachable?
2. **Crossfade morph quality** on touch — does the transition feel smooth, jarring, or invisible?
3. **End-of-flow tint-pulse** registering as spatial confirmation — does the user see it land on the today-card?
4. **Past-day tint distinction** reading without a label — does the cooler surface-muted bg register as "this is a different day" in < 500ms?
5. **One-handed thumb reach** for all interactive elements — score circle, back, forward, drag-handle. Stopwatch the full flow on a good-day and a brainfog-simulated day.
6. **Auto-save under network throttling** — does mid-flow dismiss preserve data when network is slow?
7. **Gesture isolation on touch** — score-circle drag does not dismiss the sheet, even on near-diagonal drags.

Record findings in the spec doc's Validation log section.

### 5.B — Reconciliation cleanup

Conditional on the Step 4 reconciliation option:

**If Option A (replace) was chosen** in Step 4:
- Remove the now-superseded Step 4b code: `<ScoreRow>` component, the horizontal-row CSS, the page-header `<SaveStatus>` placement, any tests that asserted the row's layout
- Update `daily-entry/` README to reflect that Step 4b is superseded; add a short note explaining the design pivot
- Update `daily-entry/` Step 5's plan to reflect that `<NoteField>` and `<TagCategoryList>` are now consumed by `QuickEntryFlow` rather than rendered directly in TodayShell
- One commit, clearly titled `chore: remove superseded score-row in favour of quick-entry-popout`

**If Option B (coexist) was chosen** in Step 4:
- Add a user preference to `Settings` page: "Klassieke invoer" vs "Snelle invoer (popout)"
- Add the preference column to the user record (or a localStorage key for v1 simplicity)
- Conditional render in `<TodayShell>` based on the preference
- Tests for both flows continue to run
- Document the toggle in user-facing help text (if any exists at that point)

**If Option C (defer) was chosen** in Step 4:
- The popout already lives at a separate route (`/lab/quick-entry-popout` or similar) and the home flow is untouched
- This sub-step becomes a recommendation: based on the 5.A validation findings, either schedule a follow-up step to promote popout to home, or document the decision to keep it as a lab experiment indefinitely
- If promoting, write the promotion step plan (essentially Option A above) and run it as a separate work item

---

## Acceptance criteria

- [ ] AC1: All 7 items in 5.A validated and recorded in the [Validation log](../../design/explorations/quick-entry-popout.md#validation-log) with findings (pass / fail / partial + notes)
- [ ] AC2: Reconciliation cleanup matching the chosen option lands cleanly. `npm run verify` green throughout (i.e., the cleanup commit doesn't break tests for the other path)
- [ ] AC3: `daily-entry/` README updated to reflect the reconciliation outcome (link added pointing to this step's outcome)
- [ ] AC4: Stopwatch result for "fresh-day full flow on a brainfog simulation" recorded — must be ≤ 10 seconds per the cardinal principle, ideally well under
- [ ] AC5: If Option A: no orphan files, no orphan tests, no orphan CSS. Verify with `npm run lint --max-warnings 0`
- [ ] AC6: If Option B: the toggle defaults to whichever flow is more battle-tested at the time of this step (likely Classic for safety, with Popout opt-in)

---

## Done criteria

- [ ] **Mobile validation completed; findings logged** — left to the user (the seven 5.A items, recorded in [the spec doc's Validation log](../../design/explorations/quick-entry-popout.md#validation-log)).
- [x] Reconciliation cleanup landed per Option A (this build session):
  - `<DayDetailSheet>` deleted; `<TimelineView>` now opens `<QuickEntryFlow>` directly with `isPastDay=true`
  - `<DayEntryEditor>` deleted (no more callers after the home + timeline integrations both use the popout)
  - `<ScoreRow>` deleted (no more callers after Step 4b's superseding)
  - Corresponding test files (`day-entry-editor.test.tsx`, `score-row.test.tsx`) deleted
  - `<NoteField>` + `<TagCategoryList>` retained — both are consumed by `<QuickEntryFlow>`'s note and tags steps
- [x] Cross-doc references updated: `daily-entry/` README's Steps section flags every superseded item; the spec's Validation log gets a 2026-05-29 entry plus the seven mobile-validation checkboxes for the user.
- [x] No regression in the surviving test suite — `npm run verify` clean (582/582)

## Done

- [x] 5.B.i — Timeline edit surface unified with home: `<QuickEntryFlow>` is the only edit affordance across both tabs. Past-day taps from the chart or the heatmap open the same popout with the past tint.
- [x] 5.B.ii — Orphan code removed: `day-detail-sheet.tsx`, `day-entry-editor.tsx`, `score-row.tsx` and their two test files. ESLint + tsc + vitest all clean afterwards.
- [x] 5.B.iii — `daily-entry/` README's "Steps" list carries supersession notes inline so future readers see the history (Step 4 → 4b → quick-entry-popout/4) without having to cross-walk three docs.
- [x] 5.B.iv — Spec doc's Validation log gets the 2026-05-29 ship entry + the seven 5.A checkboxes for the user to tick as they soak.
- [ ] 5.A — Mobile validation: the seven items in the spec's Validation log are left for the user. The popout is shipped to prod; the user runs the checklist on the iPhone PWA over the next few days and records findings.
- [x] RED/GREEN: no new tests in this step — the verify gate confirms the existing suite still passes after the orphan removal.
- [x] Type check + lint: clean (lint catches dead-import regressions; nothing flagged).
- [x] No new HIGH cardinal-principle / privacy / security findings (deletion-only step on the production code).
- [ ] Walkthrough: the seven 5.A items ARE the walkthrough. Logged in the spec's Validation log for the user.

### Side-quests caught during implementation

- **lab/ promotion deferred.** The three lab/ files (`bottom-sheet.tsx`, `score-circle.tsx`, `quick-entry-flow.tsx`) are now reachable from the canonical home + timeline routes. Strictly speaking they should move out of `lab/` per the BUILD-HANDOFF's quarantine rule ("code may be promoted out of lab/ once Step 4 makes a reconciliation decision"). Deferring until after the 5.A mobile validation closes — if any of the seven items fail in a way that needs a redesign, the rename adds churn to no benefit. Tracked as a single follow-up: once the soak passes, move the three files and update three imports.
- **TimelineView re-fetch on close.** The old `<DayDetailSheet>` re-fetched the visible range via `onSaved`. With `<QuickEntryFlow>`, saves are continuous (each field saves on its own settle / commit timing), so there's no single "saved" event the timeline can hook. Current behaviour: `onClose` and `onComplete` both trigger a range re-fetch. Acceptable — slight extra read but bounded by user action.
- **Timeline tests adapted to the new popout shape.** Two assertions (`role="listbox"` from ScoreRow, dialog `accessibleName` with the date) were updated to use the new contract (`role="slider"` on ScoreCircle, `bg-surface-muted` class on the past-tinted dialog).

---

## Open questions to settle during implementation

- **Whether to keep the throwaway HTML prototypes** in `docs/design/explorations/`: arguments both ways. Keep = future readers see the validation work; Delete = explorations are throwaway by nature. Probably keep, with a "superseded by feature plan" note at the top of each.
- **What the user-facing toggle name should be** if Option B is chosen — needs a Dutch label that's clear without being long. `Invoer-stijl: klassiek / popup` or similar.
- **Whether to update the design brief's "Tension to watch" section** in `Spatial principle: thumb-first` — when this step lands, the tension is resolved, so the doc should reflect that. Small edit.
