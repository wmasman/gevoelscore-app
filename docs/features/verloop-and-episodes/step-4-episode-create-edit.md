# Step 4: Episode create + edit form + archive

**Estimated time:** ~6 hours (the largest step in this feature — substantial UI surface, full mutation path, lots of states to test).
**Test layers:** Vitest component tests for the `EpisodeFormSheet` composite, the field components (label, category-locked-display, date range, ongoing toggle, description), and the create/edit hook (analogous to `useDayEntryUpsert`). Vitest component test for the launchers (`+ Nieuwe interventie` / `+ Nieuwe periode` buttons) and the tap-to-edit affordance on existing list items. Existing ContextView + TodayShell tests stay green. No new Playwright test in step-4 (the closed-loop episodes-smoke already covers POST/PATCH against the wire; step-4 component tests cover the form interaction surface).
**Risk:** Medium. New mutation paths through the existing API; `router.refresh()` integration; client-side validation matching server-side rules; the form has 5 fields and 4 visible states (create-interventie, create-event, edit-active, edit-afgerond) plus the archive button. Bug surface is real but contained — no schema change, no API change.
**Prerequisite:** Step-3 GREEN + deployed. The Context tab renders the Periodes section read-only. Step-2's POST and PATCH endpoints are live + verified by episodes-smoke. The rename Periodes → Context shipped in commit `ed3d347` — step-4 is built on the Context + Periodes-section structure.

> Step-4 ships the mutation surface for episodes. New `+ Nieuwe interventie` / `+ Nieuwe periode` launcher buttons inside the Periodes section, a single composite form (`EpisodeFormSheet`) for both create and edit, the date-range UX with the "lopend" toggle, the archive button, and the `router.refresh()` plumbing so the list updates after every mutation. **No tag-linking in step-4** — that's step-5's affordance, gated to the episode-detail screen.

---

## Open decisions to confirm before build

Three calls worth surfacing — none of them are blockers, but all three shape the form's feel.

### Q1: Form presentation pattern — sheet, modal, or route?

The existing daily flow uses BottomSheet (the `QuickEntryFlow` popout). It's the established thumb-first pattern. Episode form has more fields though (label / category / start_date / end_date / lopend-toggle / description / [delete] / [archive] / [save]).

- **Option A (recommended): BottomSheet, scrollable interior.** Consistent with the rest of the app. The sheet's `h-[min(380px,calc(100dvh-160px))]` cap accommodates a vertical scroll for the description field. Same primitive, same dismiss patterns (drag-down, Escape, close button).
- Option B: Full-screen dialog (`<dialog>` element or a modal route). More room for a date picker, but breaks the thumb-first convention.
- Option C: Separate routes `/context/new?category=interventie` and `/context/[id]`. Most explicit. Adds router state + page-level mount/unmount churn.

### Q2: Save UX — explicit "Bewaar" button or auto-save?

The brief's auto-save rule is specific to the daily-entry flow (one tap, sub-10s). Episodes are config-style entries — multiple coordinated fields, not a quick log. Auto-save on a date picker is also awkward (do you save on every typed digit?).

- **Option A (recommended): Explicit `Bewaar` button.** Submit-on-tap; until then, edits stay in form state. Discard-on-close behaviour (no auto-save). Pair with a `Verwijder` button on edit-mode for the archive flow.
- Option B: Auto-save on field blur, like NoteField's 1.5s debounce. Feels lighter but the date-pair validation needs both dates before it can be checked — auto-save on a half-edited pair is weird.

### Q3: Archive UX — one-tap or confirm dialog?

The existing app has no confirm dialogs (per the brief: "no friction in the main flow"). Archive is reversible — soft-delete only, archived_at can be cleared.

- **Option A (recommended): One-tap archive.** Tap `Archiveer` in the edit form → episode disappears from active list. No "are you sure". Reversible via the v1.5b tag-management-settings screen (where archived episodes can be surfaced + un-archived).
- Option B: Confirm dialog "Weet je het zeker?". Safer but adds friction; the action is already reversible at the data layer.

---

## Acceptance criteria

### Launchers in the Periodes section

- [ ] **AC1: Two launcher buttons appear at the top of the Periodes section** inside the Context tab, BELOW the "Periodes" h2 heading and ABOVE the sub-group sections (or above the empty-state line when there are no episodes):
  - `+ Nieuwe interventie` — opens the form pre-set to `category='interventie'`.
  - `+ Nieuwe periode` — opens the form pre-set to `category='levensgebeurtenis'`. (User copy says "periode" because "levensgebeurtenis" is too clinical for the button; the underlying category remains `levensgebeurtenis` in storage.)
- [ ] **AC2: Both buttons meet the WCAG 2.5.5 touch target** (44×44 min). Side-by-side, full-width split, or stacked — TBD by the implementation, both touch-correct.
- [ ] **AC3: Category is LOCKED in the form** once launched — the user picked it by tapping the button. No category selector visible inside the form (cleaner UX, matches the README's "decision rule" that says you pick the category by which thing you're adding).
- [ ] **AC4: Empty state is revised** from "Nog geen periodes." to a short line that points at the buttons: e.g. "Nog geen periodes." stays as the line BUT the buttons above are the natural CTA. No extra prose. Brainfog-friendly.

### Episode form sheet

- [ ] **AC5: A new component `EpisodeFormSheet`** renders a BottomSheet containing the form. Pure presentational; receives `{ mode: 'create'|'edit', initialEpisode?: Episode, category: EpisodeCategory, open: boolean, onClose, onSaved, onArchived }` props.
- [ ] **AC6: Form fields, in order**:
  1. Label — `<input type="text">`, max 40 chars (matches `MAX_EPISODE_LABEL_LENGTH`), inline char counter visible at 30+ chars.
  2. Date range:
     - Start date — `<input type="date">` (native picker on iOS PWA).
     - "Lopend" toggle (checkbox or pill switch). When ON, end_date is null. When OFF, an end_date `<input type="date">` is visible.
  3. Description — `<textarea>`, max 10,000 chars (matches `MAX_EPISODE_DESCRIPTION_LENGTH`), inline char counter visible at 9,000+ chars. Resizes via CSS `field-sizing: content` where supported; min 3 lines.
  4. (Edit mode only) Archive button — see AC11.
  5. Submit button — see AC8.
- [ ] **AC7: Validation runs CLIENT-SIDE before submit**, mirroring the server-side gates:
  - Label: trimmed length 1–40, normalised whitespace. Empty → submit disabled + inline error message.
  - Category: pre-set (locked), no validation needed.
  - Date range: start_date must be a valid date; if "lopend" is OFF then end_date must be valid AND `end_date >= start_date`. Otherwise inline message + submit disabled.
  - Description: 0–10K chars. Over 10K → inline message + submit disabled.
  - calendar_binding never sent (locked to null at three layers; the form has no field for it).
- [ ] **AC8: Submit button** — explicit "Bewaar" / "Opslaan" (final Dutch copy decided in the build).
  - Create mode: POST /api/episodes, on success close the sheet + `router.refresh()`.
  - Edit mode: PATCH /api/episodes/[id], same close + refresh.
  - On server error: keep the sheet open, surface an inline banner with the error variant translated to user-friendly Dutch.
  - While in flight: button label changes to "Even geduld…" + disabled.
- [ ] **AC9: Cancel / dismiss** — drag-down on the sheet, tap the close ✕, OR press Escape. None of these auto-save. Unsaved changes are discarded. There is NO "save your changes?" prompt — keeps the brainfog-friendly contract.
- [ ] **AC10: Edit mode pre-fills all fields** from `initialEpisode`. The "lopend" toggle is ON when initialEpisode.end_date === null, OFF (with the date visible) otherwise. Toggling "lopend" ON wipes the end_date input value; toggling OFF restores the previously-visible value if any (or empties if none).
- [ ] **AC11: Archive button** in edit mode only. Label: "Archiveer" (final Dutch decided in the build). One-tap. On tap: PATCH `{ archived_at: new Date().toISOString() }`. On success: close sheet + `router.refresh()`. The archived episode disappears from the active list automatically (the existing `groupEpisodes` filter handles it). No confirm dialog.
- [ ] **AC12: Future-dated start_date is accepted** (the schema + wrapper + API all allow it). Real case: book a vakantie 3 months ahead.
- [ ] **AC13: Description multi-line whitespace is preserved** by the API and rendered as-is in display (already validated end-to-end in step-2; the form just respects the textarea's literal value).

### Tap-to-edit on list items

- [ ] **AC14: Each list item inside the Periodes sub-groups becomes a button** (`role="button"`, `tabIndex={0}`, keyboard-enter handler). Tap opens the form in edit mode pre-filled with that episode.
- [ ] **AC15: Touch target ≥ 44×44**. The existing `min-h-11` (44px) layout in step-3 already accommodates this; only the interactive role + handlers are added.
- [ ] **AC16: aria-label on the item** reads as the full episode summary, e.g. `"Coaching met Sarah, 2026-04-01 tot lopend, tik om te bewerken"`. Brainfog-friendly read-aloud.

### Mutation plumbing

- [ ] **AC17: A new hook `useEpisodeUpsert`** (mirrors `useDayEntryUpsert`):
  - `create(input): Promise<Episode | null>` — POSTs, returns the new episode on success or null on error.
  - `update(id, patch): Promise<Episode | null>` — PATCHes, returns updated episode or null.
  - `archive(id): Promise<boolean>` — convenience wrapper that PATCHes archived_at to now.
  - Each mutation calls `router.refresh()` on success.
  - The hook integrates with `SaveStatusProvider` so the existing save-status banner system can surface errors.
- [ ] **AC18: SaveStatus integration** — the existing `<SaveStatus />` and `<SaveAnnouncer />` infrastructure surfaces episode mutation states. After a successful save, the announcer says "Opgeslagen." (existing copy). After an archive, the announcer says "Gearchiveerd." (new copy).
- [ ] **AC19: `router.refresh()` re-fetches via page.tsx**; the new/updated episode flows back through the prop chain to ContextView. No client-side cache mutation, no useState mirror.

### Accessibility + design

- [ ] **AC20: Form fields are labelled** — `<label>` linked to each `<input>` / `<textarea>` via `htmlFor` / `id`. Screen readers announce field name + current value.
- [ ] **AC21: Required-field affordance** — a small asterisk or "verplicht" marker on the label visible to sighted users; required="true" + aria-required="true" on the input.
- [ ] **AC22: Submit button has aria-busy="true"** while in flight.
- [ ] **AC23: Error messages have role="alert"** so they're announced when they appear.
- [ ] **AC24: Reduced motion** — sheet open/close honours `prefers-reduced-motion` (the existing BottomSheet primitive already does this).
- [ ] **AC25: No em-dash in user-facing copy** (per the locked rule). Use period, comma, colon, or arrow.
- [ ] **AC26: All copy lives in `copy.ts`** under `copy.context.form.*` and `copy.context.archive.*`.

### Regression

- [ ] **AC27: Vandaag tab is unchanged.** Daily flow keeps its sub-10-second budget. The Context tab's new mutations don't touch any daily-entry code paths.
- [ ] **AC28: Tijdlijn tab is unchanged.** The range/view toggles + score chart + heatmap still work.
- [ ] **AC29: ContextView's empty-state and read-only list behaviour unchanged when no mutation is in flight.** The list items just become tappable; everything else stays.
- [ ] **AC30: Verify gate green.** `npm run verify` clean.

---

## Technical constraints

- **BottomSheet primitive reused.** The existing `<BottomSheet>` from `src/components/lab/bottom-sheet.tsx` is the wrapper. EpisodeFormSheet is a sibling-style composite to QuickEntryFlow but with explicit-save semantics (no auto-save).
- **No new SDK dependency.** Native `<input type="date">` on iOS PWA is the date picker. No react-datepicker or other library in step-4.
- **`useEpisodeUpsert` mirrors `useDayEntryUpsert`'s shape.** Same callsite ergonomics, same SaveStatusProvider integration, same `router.refresh()` on success. Different endpoint, different error variants.
- **`router.refresh()` is the truth source for post-mutation display.** No client cache shadowing; the ContextView prop is re-fetched server-side. Matches the existing daily-entry pattern.
- **Validation parity with server.** The form's client-side rules MUST match `validateEpisodeLabel` / `validateEpisodeDescription` / `validateDateRange` exactly. Importing the validators directly in the form component is the safest move — single source of truth, no duplicated regex.
- **Forbidden patterns** (per design brief): no em-dashes in copy; no auto-advance after a single field commit; no flashing colours on save; no confirmation modals.
- **Touch targets 44×44 minimum.** Tab bar already meets this; new launcher buttons and list items must too.
- **Description has a soft client-side cap visible to the user**: the inline counter appears at >=9,000 chars. The server enforces 10,000 strictly via `validateEpisodeDescription`.
- **Label has the same soft cap pattern**: counter appears at >=30 chars; server enforces 40.
- **No URL state for the open sheet.** Tab state stays component-local (`useState`); opening the form sheet uses local state inside TodayShell or ContextView, not a query param. Matches the QuickEntryFlow pattern.
- **No optimistic update.** The list shows what the server returned via `router.refresh()`. Optimistic-update would mean rendering the new episode immediately before the API confirms — adds complexity, surfaces a state-conflict bug class. For the soak-test scale (single user), the server round-trip latency (~150–300ms) is invisible behind the closing sheet animation.

---

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | No | All API surface lives in step-2. Step-4 only adds client-side mutation calls. |
| New collection storing user data | GDPR Art 9 | No | Already addressed in step-1. |
| New env var | A02 | No | — |
| New dependency | ADR | No | Native date input, no react-datepicker. |
| Reduced motion / animation | WCAG 2.3.3 | Yes | BottomSheet primitive already handles `prefers-reduced-motion`. AC24. |
| Aria labelling | WCAG 1.1.1, 1.3.1 | Yes | AC16, AC20, AC21, AC22, AC23. |
| Required fields | WCAG 3.3.2 | Yes | AC21 — explicit `aria-required` + visible marker. |
| Error identification | WCAG 3.3.1 | Yes | AC23 — `role="alert"` on inline error messages. |
| Forbidden UI patterns | brief.md | Yes | No em-dashes; no auto-advance; one-tap archive; explicit save. |
| Touch target 44×44 | WCAG 2.5.5 | Yes | AC2, AC15. |
| Copy in Dutch via copy.ts | conventions.md | Yes | AC26. |
| No em-dash in UI copy | memory feedback | Yes | AC25. |
| CSV injection in user input | A03 (defense-in-depth) | Yes (forward-looking) | Description text could contain `=`, `+`, `-`, `@`. The CSV export path (v1.5+) MUST escape these. Step-4 does NOT introduce CSV export; the rule is documented here so the export-time guard is remembered. |
| TOCTOU on partial-date PATCH | Step-2 known limitation | Forward | Step-4 sends both dates whenever either changes (the form holds both as state, so the "send both" path is taken — the wrapper's fetch-then-validate read does NOT fire in normal use). |

---

## Plan

### 4.0 New copy keys in `src/copy.ts`

```ts
context: {
  // ... existing title, ariaLabel, periodes ...
  newInterventieButton: '+ Nieuwe interventie',
  newPeriodeButton: '+ Nieuwe periode',
  form: {
    sheetAriaLabel: 'Periode bewerken',  // singular, both create + edit
    labelField: 'Naam',
    labelPlaceholder: '',
    labelCountSuffix: (n: number) => `${n}/40`,
    startDateField: 'Begindatum',
    ongoingToggle: 'Lopend (geen einddatum)',
    endDateField: 'Einddatum',
    descriptionField: 'Beschrijving',
    descriptionPlaceholder: 'Optioneel',
    descriptionCountSuffix: (n: number) => `${n}/10.000`,
    save: 'Bewaar',
    saving: 'Even geduld…',
    cancel: 'Annuleer',
    requiredMarker: 'verplicht',
    // Inline error messages
    error: {
      labelEmpty: 'Geef een naam.',
      labelTooLong: 'Maximaal 40 tekens.',
      startDateInvalid: 'Kies een begindatum.',
      endDateInvalid: 'Kies een einddatum of zet "lopend" aan.',
      endBeforeStart: 'Einddatum moet ná de begindatum liggen.',
      descriptionTooLong: 'Maximaal 10.000 tekens.',
      serverError: 'Opslaan lukte niet, probeer opnieuw.',
    },
    listItemAriaLabel: (label: string, start: string, end: string | null): string =>
      end === null
        ? `${label}, ${start} tot lopend, tik om te bewerken`
        : `${label}, ${start} tot ${end}, tik om te bewerken`,
  },
  archive: {
    button: 'Archiveer',
    announced: 'Gearchiveerd.',  // SaveAnnouncer copy
  },
},
```

### 4.1 New hook `src/hooks/use-episode-upsert.ts`

Mirrors `useDayEntryUpsert.ts`. Three exports:
- `useEpisodeUpsert()` returns `{ create, update, archive, status }`.
- `create(input)` calls POST /api/episodes, refreshes the router on success.
- `update(id, patch)` calls PATCH /api/episodes/[id], refreshes on success.
- `archive(id)` is a thin wrapper around `update(id, { archived_at: new Date().toISOString() })`.
- Status integrates with `SaveStatusContext` for the existing save-status banner system.

### 4.2 New component `src/components/episode-form-sheet.tsx`

Single composite. Props (see AC5). Body:
- Title (variable: "Nieuwe interventie" / "Nieuwe periode" / "Bewerk interventie" / "Bewerk periode")
- Label input + counter + inline error slot.
- Start date input + inline error slot.
- "Lopend" toggle.
- End date input (conditional on toggle OFF) + inline error slot.
- Description textarea + counter + inline error slot.
- (Edit mode) Archive button row.
- Save button row.
- Wired via `useEpisodeUpsert`.

### 4.3 Extend `ContextView` — launcher buttons + tappable list items

- Two new buttons inside `<PeriodesSection>`, above the groups OR above the empty-state line.
- Sheet state lifted into ContextView: `const [sheet, setSheet] = useState<{ open: boolean, mode: 'create'|'edit', ... }>(...)`.
- Each list item becomes a `<button>` that calls `setSheet({ open: true, mode: 'edit', initialEpisode: ep, category: ep.category })`.
- The `<EpisodeFormSheet>` renders at the bottom of ContextView.

### 4.4 Test additions

- `src/hooks/__tests__/use-episode-upsert.test.ts` (new): mock fetch, assert it calls /api/episodes correctly, asserts `router.refresh()` is invoked on success.
- `src/components/__tests__/episode-form-sheet.test.tsx` (new): the full form interaction surface — typing in label, toggling lopend, picking dates, submitting create, submitting edit, archive button visibility (edit only), validation error states, server-error banner.
- `src/components/__tests__/context-view.test.tsx` (extend): launcher buttons present, tapping a list item now opens the sheet (mock the sheet open/close callback).
- `src/components/__tests__/today-shell.test.tsx`: keep existing assertions; no new tests at the shell level (the sheet state lives in ContextView).

---

## Test list (RED-first)

### Unit: `src/hooks/__tests__/use-episode-upsert.test.ts` (new)

- [ ] `create(input) POSTs to /api/episodes with the input body`
- [ ] `create(input) on 200 returns the episode and calls router.refresh()`
- [ ] `create(input) on 400 invalid_label returns null and sets status='error' with the error variant`
- [ ] `update(id, patch) PATCHes to /api/episodes/[id] with the patch body`
- [ ] `update(id, patch) on 200 returns the updated episode and calls router.refresh()`
- [ ] `update(id, patch) on 404 returns null and sets status='error' with 'not_found'`
- [ ] `archive(id) PATCHes archived_at with an ISO timestamp`
- [ ] `archive(id) on 200 returns true and calls router.refresh()`
- [ ] `during in-flight, status === 'saving'`
- [ ] `status resets to 'idle' after completion`

### Component: `src/components/__tests__/episode-form-sheet.test.tsx` (new)

**Create mode:**
- [ ] `renders the sheet with the title "Nieuwe interventie" when mode='create' and category='interventie'`
- [ ] `renders the sheet with the title "Nieuwe periode" when category='levensgebeurtenis'`
- [ ] `label input is required + aria-required="true"`
- [ ] `label counter appears at >=30 chars`
- [ ] `label > 40 chars → inline error + submit disabled`
- [ ] `empty label → inline error visible only after first interaction (no aggressive validation on initial render)`
- [ ] `start_date defaults to today`
- [ ] `lopend toggle defaults to ON in create mode → end_date input hidden`
- [ ] `toggling lopend OFF reveals end_date input with empty value`
- [ ] `end_date < start_date → inline error + submit disabled`
- [ ] `description counter appears at >=9000 chars`
- [ ] `description > 10000 chars → inline error + submit disabled`
- [ ] `valid form + tap Bewaar → calls hook.create with the form values`
- [ ] `hook.create resolves → sheet closes + onSaved fired`
- [ ] `hook.create rejects with invalid_label → inline label error + sheet stays open`
- [ ] `hook.create rejects with directus_error → top-of-form server-error banner`

**Edit mode:**
- [ ] `pre-fills label / category-locked-display / start_date / end_date / description from initialEpisode`
- [ ] `lopend toggle starts ON when initialEpisode.end_date === null`
- [ ] `lopend toggle starts OFF when initialEpisode.end_date is set`
- [ ] `archive button is visible in edit mode`
- [ ] `archive button is NOT visible in create mode`
- [ ] `tapping archive → calls hook.archive with the id + sheet closes + onArchived fired`
- [ ] `valid edit + tap Bewaar → calls hook.update with the diff (or the full set; whichever the impl chooses)`

**Dismiss:**
- [ ] `tapping ✕ → onClose fires + sheet closes, no save attempted`
- [ ] `pressing Escape → onClose fires`
- [ ] `unsaved changes are discarded on dismiss (no "are you sure" prompt)`

### Component: `src/components/__tests__/context-view.test.tsx` (extend)

- [ ] `the Periodes section has two launcher buttons: "+ Nieuwe interventie" and "+ Nieuwe periode"`
- [ ] `tapping "+ Nieuwe interventie" opens the sheet in create mode with category='interventie'`
- [ ] `tapping "+ Nieuwe periode" opens the sheet in create mode with category='levensgebeurtenis'`
- [ ] `each list item now has role="button" and an aria-label matching context.form.listItemAriaLabel(...)`
- [ ] `tapping a list item opens the sheet in edit mode with the episode pre-filled`
- [ ] `the sheet's onSaved / onArchived close the sheet (state resets)`

### Existing tests must stay green

- TodayShell, Vandaag flow, Tijdlijn switch, QuickEntryFlow.
- ContextView empty + non-empty rendering (now WITH the launcher buttons visible — the existing tests may need a small fixture update if they query the exact DOM tree shape).
- TimelineView, score-chart, heatmap.
- Domain validators (date-range, episode-label, episode-description, episode, episode-category, episode-groups).
- API SDK wrapper (episodes.ts) + route handlers.
- Auth-smoke + episodes-smoke continue to PASS post-deploy.

---

## Done-when

**Local — TDD loop:**
- [ ] (1) All listed Vitest tests written and RED first.
- [ ] (2) Implementation lands; all tests GREEN.
- [ ] (3) `npm run verify` clean.

**Commit + deploy:**
- [ ] (4) Commit + push.
- [ ] (5) `fly deploy -a gevoelscore-frontend`.

**Live smoke checks:**
- [ ] (6) `scripts/run-episodes-smoke.ps1` PASS (regression check on the API endpoints — the form's mutations route through them).
- [ ] (7) `scripts/run-auth-smoke.ps1` PASS (regression on day-entries + tags read paths).
- [ ] (8) Manual: load `/` on iPhone, switch to Context tab, tap "+ Nieuwe interventie", fill in "smoke test", save, see it appear in Interventies (actief), tap it, edit description, save, see the change, tap Archiveer, see it disappear from active list.

**Documentation:**
- [ ] (9) README ACs F5 (create-episode form) + F6 (archive reversible — already partially ticked in step-2) + F7 (tag-linking from episode detail is step-5) + F8 (Vandaag unchanged) ticked.
- [ ] (10) Update `step-4-episode-create-edit.md` Done section with the actual commit SHA + smoke results.

**Commit message:** `feat(episodes): step-4 — episode create + edit form + archive`.

---

## Out of scope (step-4)

- **Tag-to-episode linking** ("Voeg gekoppelde tag toe" affordance in episode detail) — step-5.
- **Showing archived episodes** in the Context tab (a "gearchiveerd" toggle / filter) — v1.5b tag-management-settings.
- **Calendar-binding field in the form** — v1.6.
- **Bulk operations** — never (per the README).
- **Confirm dialog** before archive — never (per the brief's "no friction" rule).
- **Optimistic update** in the list view — explicit deferral; `router.refresh()` is the source of truth, post-mutation latency hidden behind sheet-close.
- **Past-day pulse animation on save** (the daily-flow's pulse pattern) — episodes don't need it; the sheet-close animation is the completion signal.
- **URL state for the open sheet** — defer; local state is fine for v1.5.
- **Drafts / partial saves** — explicit deferral; the form is in-memory only until Bewaar is tapped.

---

## Notes for step-5

What step-5 (`step-5-tag-episode-linking.md`) needs to remember from step-4:

- The EpisodeFormSheet has a fixed-shape body in step-4. Step-5 adds a new section to the edit-mode form: "Tags die hierbij horen" — a chip list + a "+ Tag" affordance.
- The linking happens on the EPISODE side: tapping "+ Tag" in the episode edit form shows a tag picker (probably similar to `TagCategoryList` but in a smaller surface). Picked tags get their `parent_episode_id` set to this episode's id.
- API surface: step-2 left `parent_episode_id` writable via the existing `/api/tags` endpoint (the inline-tag-creation `createOrUpsertTag` accepts parent_episode_id) AND the existing PATCH /api/tags/[id] (if it exists; if not, step-5 may need to extend the tag API).
- Verify in step-5 build: the daily-flow tag picker (`TagCategoryList` in QuickEntryFlow) is UNCHANGED — AC-F8 in the README. Tag-to-episode linking surface lives entirely in the Context tab's episode edit screen.
- Removing a linked tag from an episode = setting that tag's `parent_episode_id` back to null. NOT deleting the tag — the tag stays in the user's library, it just becomes standalone again.
