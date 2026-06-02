# Step 1: Timeline gap indicator

**Estimated time:** ~2 hours
**Test layers:** Vitest component tests extending `src/components/__tests__/score-chart.test.tsx`. No new e2e — manual check on dev server covers the visual.
**Risk:** Low. Pure visual additions to ScoreChart, no data-model or API change. The heatmap branch is an audit, not code.
**Prerequisite:** None. Builds on the existing ScoreChart, ScoreHeatmap, TimelineView, and the QuickEntryFlow popout's `onPointTap` contract.

> Render a faint hollow gap-dot for every day in the active timeline range that has no logged entry. The dot sits at the chart bottom (just above the x-axis), is tappable to open the QuickEntryFlow popout for that date (retroactive logging), and carries a neutral aria-label. No visible "geen score" copy. The heatmap already renders missing days as outlined cells; this step audits that treatment against the design brief and confirms no change is needed there.

---

## Acceptance criteria

- [ ] **AC1: Gap-dots render for every missing day** in [from, to] on the line chart. Logged days continue to render exactly as today (no change to existing raw points or MA line).
- [ ] **AC2: Visual treatment is faint and neutral.** Hollow outline circle (`fill="none"`, `stroke="currentColor"` using `--color-fg-subtle` via a Tailwind utility), 3px radius, opacity ~0.3. No warm-orange, no alarm colour, no fill. Matches the design brief's "restrained visual cues" line.
- [ ] **AC3: Vertical position is the chart bottom**, just above the x-axis baseline. Computed as `cy = PADDING_TOP + chartH - 3` (so the 3px-radius dot's bottom edge touches the baseline). This places dots below the lowest possible score, making them unambiguously not-data.
- [ ] **AC4: Tappable, opens the QuickEntryFlow for that date.** Same callback contract as the existing raw points: clicking the gap-dot calls `onPointTap(date)`. TimelineView already wires `onPointTap` to `setSelectedDate`, which opens the popout with `isPastDay=true`. No new wiring needed in TimelineView.
- [ ] **AC5: Touch target is 44×44 effective.** Transparent hit circle with `r=12` SVG units overlaid on the visual dot — same pattern as existing raw points. Inside a `<g role="button" tabIndex={0}>` that grows to a 24×24 px box at the chart's render scale (~44×44 device pixels via viewBox + h-48 sizing).
- [ ] **AC6: aria-label is neutral and date-bearing.** `aria-label="{date}: geen score"`. Used by the existing raw points as `"{date}: score {score}"`. The screen-reader text mirrors that pattern but says "geen score". No "gemist", no "mis", no exclamation marks. Per [[feedback-no-emdash-in-ui]] no em-dashes either.
- [ ] **AC7: No visible "geen score" text** is rendered anywhere — neither inside the SVG, nor as a tooltip, nor a hover-revealed label. The aria-label is the only carrier; the visual is the dot itself.
- [ ] **AC8: Both ranges supported.** Gap-dots render on both 30d and 90d views. The line chart already receives `[from, to]` for both ranges; the derivation works identically.
- [ ] **AC9: Reduced-motion / a11y unchanged.** No animation added. Existing focus-visible outline still works on the dot's parent `<g>`.
- [ ] **AC10: Heatmap audit** — confirm the existing missing-cell treatment in [`src/components/score-heatmap.tsx`](../../../src/components/score-heatmap.tsx) matches the design brief:
  - Cell visual: outlined border (`border border-border`), muted background (`bg-surface-muted/40`), subtle text colour (`text-fg-subtle`). **✓ faint, neutral.**
  - Cell label: `aria-label="{date}: geen log"`. **✓ neutral wording, no guilt-tripping.**
  - Tappable: yes, fires `onCellTap` → opens QuickEntryFlow. **✓ consistent retroactive-log affordance.**

  Document this in the step's commit message. No code change to the heatmap.
- [ ] **AC11: Verify gate green.** `npm run verify` clean. No new lint disables.

---

## Technical constraints

- **No new dependency.** SVG-only addition to ScoreChart. Reuses existing `daysBetween` + `xFor` helpers from the same file.
- **No data-model change.** The gap-dots are derived in the component from `[from, to]` minus the logged dates already in `entries`. Server props unchanged.
- **No new API route.** Tapping a gap-dot opens the same popout the raw points open. The popout's `initialEntry={null}` branch already handles "no existing entry for this date" — it pre-fills score 5 and opens the score step.
- **Reuse existing `shiftDate`.** [`src/components/timeline-view.tsx`](../../../src/components/timeline-view.tsx) already has a `shiftDate(date, days)` helper inside the file. ScoreChart needs the same. Two acceptable shapes:
  - (preferred) Lift `shiftDate` into a shared location and import from both files.
  - (acceptable, minimal-change) Duplicate the small helper into ScoreChart.
  Decide during `/build-step` — lift if the diff stays small, duplicate if it grows.
- **Reuse the `onPointTap` callback.** No new prop on ScoreChart. The contract becomes: "fired when the user taps any day in the chart, logged or not". Document this in the prop's TSDoc.
- **Existing test fixture stays valid.** The "renders a tappable circle for each logged day" test counts only logged-day buttons by their aria-label pattern; gap-dots have a different aria-label so they won't accidentally inflate that count. Verify the assertion is specific enough (it uses `name: /score \d/i` — matches "score 5" but not "geen score"). ✓ existing tests should keep passing.

---

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | No | Pure UI. |
| New collection storing user data | GDPR Art 9 | No | No data. |
| New dependency | ADR | No | SVG only. |
| `dangerouslySetInnerHTML` usage | A03 | No | — |
| New env var | A02, A05 | No | — |
| Reduced motion respect | WCAG 2.3.3 | **Yes — no animation added, so trivially passes.** | — |
| Touch target size | WCAG 2.5.5 / brainfog floor | **Yes — 12-SVG-unit hit circle in a viewBox=600 chart rendered at viewport width gives ~44 device px on a 390px phone (12 × 390/600 ≈ 7.8 px CSS → 23.4 device px at 3x). Should verify on real device.** | Reuses the proven hit-target pattern from the existing raw points. |
| Aria labelling for non-text indicators | WCAG 1.1.1 | **Yes — aria-label per dot.** | — |
| User-input written to DB | A03 | No | — |
| Forbidden UI patterns from design brief | brief.md "Forbidden patterns" | **Yes — no guilt-trip language, no alarm colours, no autoplay motion. Verified.** | — |

---

## Plan

### 1.1 (optional) Lift `shiftDate` to a shared helper

`shiftDate(date, days)` lives in [`src/components/timeline-view.tsx`](../../../src/components/timeline-view.tsx) (and a similar version in `score-heatmap.tsx`). ScoreChart needs the same logic.

If the diff stays small, lift to `src/lib/domain/date.ts` (where `validateDate` already lives) as `shiftDateUtc(date, days)`. Both call sites + the new ScoreChart usage import it. One-line change in each existing site.

If lifting balloons (e.g. multiple test fixtures depend on the inline version), duplicate the helper into ScoreChart and defer the lift to a separate refactor commit. Note this choice in the build commit message.

### 1.2 Extend `src/components/score-chart.tsx`

Add derivation just after the existing `daysBetween/totalDays/stepX` setup:

```ts
const loggedDates = new Set(entries.map((e) => e.date));
const missingDates: string[] = [];
for (let i = 0; i < totalDays; i += 1) {
  const d = shiftDate(from, i);
  if (!loggedDates.has(d)) missingDates.push(d);
}
const GAP_Y = PADDING_TOP + chartH - 3; // dot bottom touches the x-axis baseline
```

Add a render block AFTER the existing raw-points loop:

```tsx
{missingDates.map((date) => (
  <g
    key={`gap-${date}`}
    role="button"
    tabIndex={0}
    aria-label={`${date}: geen score`}
    data-date={date}
    data-missing="true"
    onClick={() => onPointTap(date)}
    onKeyDown={(ev) => {
      if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault();
        onPointTap(date);
      }
    }}
    className="cursor-pointer focus-visible:outline-2 focus-visible:outline-accent"
  >
    <circle cx={xFor(date)} cy={GAP_Y} r={12} fill="transparent" />
    <circle
      cx={xFor(date)}
      cy={GAP_Y}
      r={3}
      fill="none"
      className="stroke-fg-subtle"
      strokeWidth={1}
      opacity={0.3}
    />
  </g>
))}
```

Update the prop TSDoc to note the contract change: `onPointTap` fires for both logged and missing dates.

### 1.3 Heatmap audit (no code change)

Inspect [`src/components/score-heatmap.tsx`](../../../src/components/score-heatmap.tsx) lines 110-148. Confirm against AC10:
- Cell styling for missing days uses `border border-border bg-surface-muted/40 text-fg-subtle`.
- `aria-label={`${date}: geen log`}` (factual, not guilt-tripping).
- Same `onCellTap` callback fires for any cell in range, logged or not.

If all three pass, no code change. If any fail, raise it as a follow-up in `docs/audits/OPEN.md` rather than expanding this step.

---

## Test list (RED-first)

Per [.claude/testing.md](../../../.claude/testing.md), every test below is named and RED before implementation.

### Component: extend `src/components/__tests__/score-chart.test.tsx`

- [ ] `renders a gap-dot for each missing day in [from, to]` — 3-day range with 1 logged day → 2 elements with `aria-label` matching `geen score`.
- [ ] `does not render gap-dots when all days in range are logged` — 3-day range with 3 logged days → 0 `geen score` elements.
- [ ] `renders gap-dots for the full range when no days are logged` — 3-day range with 0 logged days → 3 `geen score` elements.
- [ ] `gap-dot has role=button and aria-label with the date + "geen score"` — assert the exact aria-label form.
- [ ] `gap-dot is tappable: fires onPointTap with the missing date` — click triggers the callback with the right date string.
- [ ] `gap-dot is keyboard-accessible: Enter on focused gap-dot fires onPointTap` — same as raw points.
- [ ] `no visible "geen score" text is rendered` — `screen.queryByText(/geen score/i)` returns null; the label is only on the aria attribute.
- [ ] `gap-dot rendered at the chart bottom y-coordinate` — assert the `cy` attribute on a found gap-circle is the expected `PADDING_TOP + chartH - 3` value (read from inspected DOM via `data-date` lookup).
- [ ] `existing "renders a tappable circle for each logged day" test still passes` — regression. The original counts buttons matching `/score \d/i` which excludes "geen score". Re-run and confirm.

### Heatmap audit (no test code)

A one-paragraph note in the commit message confirms the audit was performed and the existing treatment passes. Optionally add an assertion to the existing heatmap test:

- [ ] (Optional) Extend `src/components/__tests__/score-heatmap.test.tsx` with `missing-day cells have aria-label "{date}: geen log"` if not already covered. Skip if it is.

---

## Done-when

- [ ] All listed tests written and RED.
- [ ] Implementation lands; all tests GREEN.
- [ ] `npm run verify` clean — no new lint/typecheck issues.
- [ ] Manual on dev server:
  - Open the timeline tab.
  - Confirm gap-dots appear for any day in the last 30 that the seeded data doesn't cover (or temporarily archive an entry to create a gap).
  - Tap a gap-dot → popout opens with `initialEntry=null`, score-step on, pre-filled at 5.
  - Save a score → popout closes, the gap-dot for that date is replaced by a real raw point on next render.
  - Toggle to 90d → gap-dots also appear there.
  - Toggle to Heatmap → confirm AC10 audit visually.
- [ ] Heatmap audit recorded in the commit message.
- [ ] Step + README ACs ticked.

---

## Out of scope

- "Strong" mode fallback (dashed line, background tint per column) — deferred to feedback per the README. Build the faint version first and see if it reads.
- Calendar view — not implemented yet; gap-indicator parallel can be applied when that view is scoped.
- Lifting `shiftDate` to a shared module — optional sub-step; defer if it expands the diff.
- An indicator on the today-card or any non-timeline surface — explicitly not in scope. The day-card's tag/note empty states are a separate UX question.
