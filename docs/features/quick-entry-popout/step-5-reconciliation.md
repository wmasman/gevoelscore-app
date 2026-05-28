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

- [ ] Mobile validation completed; findings logged
- [ ] Reconciliation cleanup landed per the chosen option
- [ ] Feature plan README updated with final status (`Status: shipped` or `Status: deferred to v1.5` etc.)
- [ ] Cross-doc references updated (`daily-entry/` README, design brief if any new findings warrant)
- [ ] No regression in existing `daily-entry/` test suite

---

## Open questions to settle during implementation

- **Whether to keep the throwaway HTML prototypes** in `docs/design/explorations/`: arguments both ways. Keep = future readers see the validation work; Delete = explorations are throwaway by nature. Probably keep, with a "superseded by feature plan" note at the top of each.
- **What the user-facing toggle name should be** if Option B is chosen — needs a Dutch label that's clear without being long. `Invoer-stijl: klassiek / popup` or similar.
- **Whether to update the design brief's "Tension to watch" section** in `Spatial principle: thumb-first` — when this step lands, the tension is resolved, so the doc should reflect that. Small edit.
