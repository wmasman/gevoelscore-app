# Step 3: Context tab + Periodes-section list view (read-only)

> **2026-06-02 evening update**: tab label revised "Periodes" → **Context** as a final structural refinement. The component was renamed `PeriodesView` → `ContextView` and restructured to contain a `<PeriodesSection>` sub-component (h2 "Periodes" wrapping the existing h3 sub-groups). The tab order also changed: **Context / Vandaag / Tijdlijn**, with Vandaag centre-positioned. This file's body below still uses the older "Periodes" tab name in many places — those references are historic, describing the step as originally drafted. The shipped code uses Context. See [README.md History](README.md#history) for the full rename timeline.

---

**Estimated time:** ~3 hours
**Test layers:** Vitest component for `PeriodesView` (jsdom + @testing-library/react); Vitest component test extending `today-shell.test.tsx` for the 3-tab nav; no new API tests (step-2 covered the wire); no Playwright e2e (the existing daily-entry flow's screen-changed assertions remain green; e2e for the new tab can wait until step-4 when mutations land).
**Risk:** Low. Pure read path: page.tsx adds a fourth concurrent fetch, TodayShell gains a new tab branch, a new component renders. No mutations, no state lifted out of TodayShell. The existing Vandaag + Tijdlijn flows are untouched.
**Prerequisite:** Step-2 GREEN + deployed (commit `e37bad2` and previous). `readAllEpisodes` is wired and verified by the episodes-smoke; the schema is live; the user role has CRUD permissions on episodes.

> Adds the **Periodes** tab as the third top-level surface (Vandaag / Periodes / Tijdlijn), and ships a read-only `PeriodesView` list grouped by category and active-vs-afgerond. **No create/edit/archive UI in step-3** — those land in step-4. **No tap-to-detail in step-3** — the cards are non-interactive list items. The tab exists to render the data that step-2 made fetchable.

---

## Open decision to confirm before build

**The "+ Nieuwe interventie" / "+ Nieuwe periode" buttons** — where do they ship?

The README's UI sketch shows them at the top of the Periodes tab. They launch the create form which is step-4's deliverable.

- **Option A (recommended): defer to step-4.** Step-3 ships the list view only. Empty state says "Nog geen periodes" — a literal description, not a CTA. Step-4 lands buttons + form together as one feature. Less risk of half-built UI confusing brainfog soak-testing.
- **Option B: present in step-3 as inert placeholders.** Buttons visible but disabled or toast "binnenkort". The affordance is visible earlier, but a button you can't press is itself friction for a brainfog user — they might tap it twice "to make sure".
- **Option C: present in step-3, navigate to a stub route.** More plumbing, partial UX.

**Default chosen below: Option A.** If you prefer B, the AC changes are small (an `aria-disabled` button + a Dutch label) but the plan stays otherwise the same. Flag in chat before the loop starts if A isn't right.

---

## Acceptance criteria

### Tab navigation

- [ ] **AC1: TodayShell's bottom-nav tablist gains a third tab "Periodes"**, between Vandaag and Tijdlijn. Order: Vandaag / Periodes / Tijdlijn. Each tab has `role="tab"` + `aria-selected` (matching the existing pattern).
- [ ] **AC2: Tapping the Periodes tab swaps the main content** to `<PeriodesView>`. Tapping Vandaag swaps back to the existing today-card flow. Tapping Tijdlijn swaps to `<TimelineView>`. No regressions on either existing tab.
- [ ] **AC3: Tab state is component-local** (`useState<Tab>('today')`) — same as today's Tijdlijn tab. No URL search-param plumbing in v1.5. A hard refresh returns to Vandaag, which is the right default for the daily flow.
- [ ] **AC4: The Periodes label is added to `copy.ts`** under a stable key (e.g. `copy.periodes.title = 'Periodes'`). All user-facing strings in step-3 live in `copy.ts`.

### Data flow

- [ ] **AC5: `page.tsx` fetches episodes** via `readAllEpisodes(session.accessToken)` alongside the existing 3 reads (entry / tags / timeline) in the same `Promise.all`. Active-only — uses the wrapper's default `{ includeArchived: false }`.
- [ ] **AC6: `episodes: Episode[]` threads through TodayShell** as a new prop (default `[]` if the read fails — same fail-soft pattern as the other reads in page.tsx).
- [ ] **AC7: PeriodesView receives `episodes` + `today` as props.** No internal fetch, no client-side state shadow. Server-rendered through.

### List rendering

- [ ] **AC8: Empty state**: when `episodes.length === 0`, PeriodesView renders a single short line: "Nog geen periodes." Brainfog-friendly — no CTA, no instruction, no preview of what's possible (those land alongside the create form in step-4).
- [ ] **AC9: Grouped sections** (when episodes exist), in this order — and only sections with ≥1 episode are rendered (no empty section headers):
  1. **INTERVENTIES (actief)** — `category === 'interventie' && archived_at === null && (end_date === null || end_date >= today)`
  2. **INTERVENTIES (afgerond)** — `category === 'interventie' && archived_at === null && end_date !== null && end_date < today`
  3. **LEVENSGEBEURTENISSEN (actief)** — `category === 'levensgebeurtenis' && archived_at === null && (end_date === null || end_date >= today)`
  4. **LEVENSGEBEURTENISSEN (afgerond)** — `category === 'levensgebeurtenis' && archived_at === null && end_date !== null && end_date < today`
- [ ] **AC10: Archived episodes (`archived_at !== null`) are NOT rendered** in any section. The "active episodes only" default at the API layer + this client-side filter together ensure archived episodes stay hidden in v1.5. Archived management ships in v1.5b (tag-management-settings).
- [ ] **AC11: Sort within a section**: active = `start_date` DESC (newest start first). Afgerond = `end_date` DESC (most recently ended first). Stable.
- [ ] **AC12: Each list item shows**: the episode label (truncated with ellipsis if too long for the row), and the date range string. Date range copy: ongoing → `"{start_date} → lopend"`. Closed → `"{start_date} → {end_date}"`. Dates formatted Dutch via the existing `formatDateDutch` helper.
- [ ] **AC13: List items are NON-INTERACTIVE in step-3.** Plain text (a `<div>` or `<li>` with semantic content), no `role="button"`, no `onClick`, no `tabIndex`. Step-4 changes them into tappable cards that open the detail screen. Reason: a tappable card that does nothing is worse than a static list for brainfog discoverability.

### Accessibility + design

- [ ] **AC14: Section headers use `<h2>`** with stable section ids. The PeriodesView root has `aria-label="Periodes"` (or equivalent).
- [ ] **AC15: WCAG 2.5.5 touch targets**: even though the items are non-interactive, the eventual interactive surface (step-4) will require min 44×44px. Step-3 sets the spacing so step-4 doesn't need a layout rework — items have at least 44px height.
- [ ] **AC16: Restraint principles**: no badges, no counts, no chrome beyond the section header + the date-range subline. Matches the design brief's "restrained visual cues".
- [ ] **AC17: Reduced motion**: no animation in this step. The tab switch is an instant content swap (matches the existing Vandaag/Tijdlijn behaviour).

### Regression

- [ ] **AC18: Existing daily flow is unchanged.** The Vandaag tab renders exactly as before; QuickEntryFlow popout still opens for score / note / tags; past-day cards still pulse on save. Verified by the existing TodayShell tests staying green.
- [ ] **AC19: Existing Tijdlijn flow is unchanged.** TimelineView still receives the same props; range toggle + chart/heatmap toggle still work.
- [ ] **AC20: Verify gate green.** `npm run verify` clean.

---

## Technical constraints

- **Server-rendered through, no client fetch.** PeriodesView reads from a prop. Step-2's GET endpoint exists but isn't called by step-3 code paths — it's reserved for the post-mutation refresh case in step-4.
- **Episodes default `[]` on read failure.** Same posture as the existing reads in page.tsx — a failed Directus call shouldn't crash the page; the empty list just shows the empty state. The other tabs still work even if episodes failed to fetch.
- **No new dependency.**
- **No new route, no new API.**
- **No motion / animation.** Section headers + list items are static.
- **All copy lives in `copy.ts`.** No string literals in JSX outside of the test files.
- **All user-facing text is Dutch.** Per the project rule. English allowed only in code, comments, and tests.
- **Forbidden patterns** (per design brief): no em-dashes in copy (per [feedback-no-emdash-in-ui](../../../.claude/projects/c--Users-Gebruiker-Documents-gevoelscore-app/memory/feedback_no_emdash_in_ui.md)). Use `:` or `→` for date-range separator. The plan above uses `→`.
- **List items must be at least 44×44px tall** for the future tap target — even though step-3 doesn't make them tappable, the layout must accommodate step-4 without rework.

---

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | No | Read-only client component; no API surface added. |
| New collection storing user data | GDPR Art 9 | No | Already addressed in step-1. |
| New env var | A02 | No | — |
| New dependency | ADR | No | Pure React component. |
| Reduced motion / animation | WCAG 2.3.3 | Yes (vacuously) | Step-3 introduces NO motion. AC17. |
| Aria labelling | WCAG 1.1.1 | Yes | Section headers + tablist + aria-selected per AC1, AC14. |
| Forbidden UI patterns | brief.md | Yes | Restraint, no badges/counts, list items non-interactive in step-3. AC13, AC16. |
| Copy in Dutch via copy.ts | conventions.md | Yes | AC4 + copy table below. |
| Touch target 44×44 | WCAG 2.5.5 | Forward-looking | Layout accommodates step-4 mins. AC15. |
| No emdash in UI copy | memory feedback | Yes | Date-range separator is `→`, not `—`. |

---

## Plan

### 3.0 New copy keys in `src/copy.ts`

Add a `periodes` namespace:

```ts
periodes: {
  title: 'Periodes',                        // tab label
  ariaLabel: 'Periodes',                    // PeriodesView root aria-label
  empty: 'Nog geen periodes.',
  section: {
    interventiesActive:  'Interventies (actief)',
    interventiesDone:    'Interventies (afgerond)',
    levensgebeurtenissenActive: 'Levensgebeurtenissen (actief)',
    levensgebeurtenissenDone:   'Levensgebeurtenissen (afgerond)',
  },
  dateRange: (startNl: string, endNl: string | null): string =>
    endNl === null ? `${startNl} → lopend` : `${startNl} → ${endNl}`,
},
```

### 3.1 New component `src/components/periodes-view.tsx`

Client component (or server component — see note). Pure rendering: takes `episodes` + `today` as props, computes the four groupings via plain TS, renders sections with headers + lists.

```ts
'use client';

import { copy } from '@/copy';
import { formatDateDutch } from '@/lib/domain/date';
import type { Episode } from '@/lib/domain/episode';

type Props = {
  episodes: Episode[];
  today: string;
};

export function PeriodesView({ episodes, today }: Props) {
  const groups = groupEpisodes(episodes, today);
  if (groups.totalActive === 0 && groups.totalDone === 0) {
    return (
      <section aria-label={copy.periodes.ariaLabel} className="flex flex-col gap-4">
        <p className="text-base text-fg-muted">{copy.periodes.empty}</p>
      </section>
    );
  }
  return (
    <section aria-label={copy.periodes.ariaLabel} className="flex flex-col gap-6">
      {groups.interventiesActive.length > 0 && (
        <Group title={copy.periodes.section.interventiesActive} items={groups.interventiesActive} />
      )}
      {groups.interventiesDone.length > 0 && (
        <Group title={copy.periodes.section.interventiesDone} items={groups.interventiesDone} />
      )}
      {groups.levensgebeurtenissenActive.length > 0 && (
        <Group title={copy.periodes.section.levensgebeurtenissenActive} items={groups.levensgebeurtenissenActive} />
      )}
      {groups.levensgebeurtenissenDone.length > 0 && (
        <Group title={copy.periodes.section.levensgebeurtenissenDone} items={groups.levensgebeurtenissenDone} />
      )}
    </section>
  );
}

function Group({ title, items }: { title: string; items: Episode[] }) {
  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-sm font-medium uppercase tracking-wider text-fg-muted">{title}</h2>
      <ul className="flex flex-col divide-y divide-border rounded-md border border-border">
        {items.map((ep) => (
          <li key={ep.id} className="flex min-h-11 flex-col gap-1 p-4">
            <span className="text-base text-fg">{ep.label}</span>
            <span className="text-sm text-fg-subtle">
              {copy.periodes.dateRange(
                formatDateDutch(ep.start_date),
                ep.end_date ? formatDateDutch(ep.end_date) : null,
              )}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

The grouping helper is pure and easy to test independently:

```ts
type Groups = {
  interventiesActive: Episode[];
  interventiesDone: Episode[];
  levensgebeurtenissenActive: Episode[];
  levensgebeurtenissenDone: Episode[];
  totalActive: number;
  totalDone: number;
};

export function groupEpisodes(episodes: Episode[], today: string): Groups {
  const out: Groups = {
    interventiesActive: [],
    interventiesDone: [],
    levensgebeurtenissenActive: [],
    levensgebeurtenissenDone: [],
    totalActive: 0,
    totalDone: 0,
  };
  for (const ep of episodes) {
    if (ep.archived_at !== null) continue;
    const isActive = ep.end_date === null || ep.end_date >= today;
    if (ep.category === 'interventie') {
      if (isActive) out.interventiesActive.push(ep);
      else out.interventiesDone.push(ep);
    } else if (ep.category === 'levensgebeurtenis') {
      if (isActive) out.levensgebeurtenissenActive.push(ep);
      else out.levensgebeurtenissenDone.push(ep);
    }
  }
  // Sort within each bucket.
  out.interventiesActive.sort((a, b) => (a.start_date > b.start_date ? -1 : 1));
  out.interventiesDone.sort((a, b) => ((a.end_date ?? '') > (b.end_date ?? '') ? -1 : 1));
  out.levensgebeurtenissenActive.sort((a, b) => (a.start_date > b.start_date ? -1 : 1));
  out.levensgebeurtenissenDone.sort((a, b) => ((a.end_date ?? '') > (b.end_date ?? '') ? -1 : 1));
  out.totalActive =
    out.interventiesActive.length + out.levensgebeurtenissenActive.length;
  out.totalDone =
    out.interventiesDone.length + out.levensgebeurtenissenDone.length;
  return out;
}
```

The grouping helper might be worth living in `src/lib/domain/episode-groups.ts` so it can be unit-tested without React. Decided yes — same pattern as `tag-sort.ts`.

### 3.2 Extend `page.tsx`

Add the fourth read to the Promise.all, default to `[]` on failure, pass to TodayShell:

```ts
import { readAllEpisodes } from '@/lib/api/episodes';
import type { Episode } from '@/lib/domain/episode';

// ...
let episodes: Episode[] = [];
const [entryResult, tagsResult, rangeResult, episodesResult] = await Promise.all([
  readDayEntryByDate(session.accessToken, today),
  readAllTags(session.accessToken),
  readDayEntriesInRange(session.accessToken, from, today),
  readAllEpisodes(session.accessToken),  // active-only by default
]);
if (entryResult.ok) entry = entryResult.value;
if (tagsResult.ok) allTags = tagsResult.value;
if (rangeResult.ok) timelineEntries = rangeResult.value;
if (episodesResult.ok) episodes = episodesResult.value;

return (
  <TodayShell
    date={today}
    entry={entry}
    allTags={allTags}
    timelineEntries={timelineEntries}
    episodes={episodes}
  />
);
```

### 3.3 Extend `TodayShell`

Three changes:
- Extend `Tab` type union: `type Tab = 'today' | 'periodes' | 'timeline'`.
- Add new conditional branch for `tab === 'periodes'` rendering `<PeriodesView episodes={episodes} today={date} />`.
- Add a third button to the bottom-nav tablist (between Vandaag and Tijdlijn).

The third button matches the existing button styling. `aria-selected` semantics already correct.

### 3.4 No new icon / no manifest change / no service-worker change

Step-3 is structural. No new assets.

---

## Test list (RED-first)

### Unit: `src/lib/domain/__tests__/episode-groups.test.ts` (new)

The grouping function is pure — easy to unit-test exhaustively.

- [ ] `given an empty list, then all groups are empty and totals are 0`
- [ ] `given an active interventie (end_date=null), then it lands in interventiesActive`
- [ ] `given an active interventie (end_date in future), then it lands in interventiesActive`
- [ ] `given an active interventie (end_date == today), then it lands in interventiesActive (today is inclusive)`
- [ ] `given an interventie whose end_date is yesterday, then it lands in interventiesDone`
- [ ] `given an archived interventie (archived_at not null), then it lands in NO group`
- [ ] `given a mix of interventies, then they distribute by status`
- [ ] `given a levensgebeurtenis with no end_date, then it lands in levensgebeurtenissenActive`
- [ ] `given a closed-range levensgebeurtenis, then it lands by status`
- [ ] `active sort: most recent start_date first`
- [ ] `done sort: most recent end_date first`
- [ ] `totals reflect the visible (non-archived) counts`

### Component: `src/components/__tests__/periodes-view.test.tsx` (new)

- [ ] `given an empty list, then renders the "Nog geen periodes." line and no section headers`
- [ ] `given a single active interventie, then renders ONLY the Interventies (actief) section`
- [ ] `given a single afgerond levensgebeurtenis, then renders ONLY the Levensgebeurtenissen (afgerond) section`
- [ ] `given a full mix, then renders all four sections in the documented order`
- [ ] `each list item renders the label`
- [ ] `each list item renders the date range — ongoing case ("→ lopend")`
- [ ] `each list item renders the date range — closed-range case ("→ <date>")`
- [ ] `list items are NOT buttons and do NOT have onClick (DOM smoke check: no role="button" on the list-item element)`
- [ ] `archived episodes (archived_at not null) are not rendered (negative test — passes the prop, asserts absence)`
- [ ] `section header is an <h2> with the documented Dutch label`
- [ ] `root has aria-label="Periodes"`

### Component: extend `src/components/__tests__/today-shell.test.tsx`

Existing TodayShell tests already exist. New cases:

- [ ] `the bottom-nav tablist contains three tabs (Vandaag, Periodes, Tijdlijn) in that order`
- [ ] `tapping Periodes shows the PeriodesView; the today-card is no longer in the document`
- [ ] `tapping back to Vandaag restores the today-card`
- [ ] `tab state is independent across remounts — fresh render starts on Vandaag (regression sanity)`
- [ ] `with episodes prop empty + Periodes selected, the empty-state text renders`
- [ ] `with episodes prop non-empty + Periodes selected, at least one section header renders`

### Existing tests must stay green

- All current TodayShell tests (Vandaag flow, Tijdlijn switch, QuickEntryFlow open/close, pulse behaviour, past-day cards).
- All current TimelineView tests.
- All API tests.

### Page-level smoke (manual)

Verify the wired-up data flow on a deployed environment after step-3 ships:
- Load `/` while logged in — Periodes tab visible at bottom.
- Tap Periodes — current episodes list renders. (At this point in the soak there's no test data; the empty state shows.)
- Tap Vandaag — today-card flow restored exactly as before.
- Tap Tijdlijn — timeline view restored exactly as before.

---

## Done-when

The Done sequence has the same dependency shape as step-2: local TDD → commit + push → deploy → smoke.

**Local — TDD loop:**
- [ ] (1) All listed Vitest tests written and RED first.
- [ ] (2) Implementation lands; all listed tests GREEN.
- [ ] (3) `npm run verify` clean.

**Commit + deploy:**
- [ ] (4) Commit + push.
- [ ] (5) Fly deploy via `fly deploy -a gevoelscore-frontend` (manual — there is no GitHub Action; the Done-when of step-2 documented the wrong assumption and step-3 follows the established manual-deploy pattern).

**Live smoke checks:**
- [ ] (6) Manual smoke: load `/` on iPhone PWA, tap Periodes, confirm the tab appears + the empty-state line renders (no test data yet, so empty is the expected state). Quick verify that Vandaag + Tijdlijn still work.
- [ ] (7) `scripts/run-auth-smoke.ps1` PASS (regression check on auth + day-entries read paths).

**Documentation:**
- [ ] (8) README ACs F3 (Periodes tab as third surface) + F9 (server-rendered without local-state shadow) + F10 (v1 surfaces still work) ticked in `docs/features/verloop-and-episodes/README.md`.

**Commit message:** `feat(episodes): step-3 — Periodes tab + PeriodesView list (read-only)`.

---

## Out of scope (step-3)

- **Create form / "+ Nieuwe" buttons** — step-4.
- **Tap-to-detail / episode detail screen** — step-4.
- **Edit-in-place / archive button** — step-4.
- **Tag-linking from the episode detail** — step-5.
- **Showing archived episodes** in any UI (a "gearchiveerd" filter / toggle) — v1.5b tag-management-settings.
- **Calendar-binding affordance** — v1.6.
- **Timeline episode overlay** (episode bands on the line chart, tints on the heatmap) — separate sibling feature [features/timeline-episode-overlay/](../timeline-episode-overlay/), ships after step-5.
- **URL search-param for tab state** (`?tab=periodes`) — defer until soak shows refresh-loses-tab is annoying enough to fix.

---

## Notes for step-4

What step-4 needs to remember from step-3:

- The Periodes tab + PeriodesView are wired and rendered. Episodes flow server-side from page.tsx through TodayShell as a prop.
- The list items in step-3 are non-interactive. Step-4 makes them buttons that open the detail/edit screen.
- The "+ Nieuwe interventie" + "+ Nieuwe periode" buttons need to be added to PeriodesView in step-4 — likely at the top of the section, above the first group header.
- Mutations (create + update + archive) should call `router.refresh()` after the API write, the same pattern as `useDayEntryUpsert`. The server component re-runs and a fresh `episodes` prop arrives. The GET endpoint is the fallback for client-side refetches if `router.refresh()` doesn't suit a future case.
- The grouping helper (`groupEpisodes`) handles the active/afgerond split. Step-4's archive action sets `archived_at` to an ISO timestamp — after `router.refresh()` runs, the archived episode disappears from PeriodesView automatically (AC10 filters archived in client too).
- The empty state copy in step-3 is "Nog geen periodes." When step-4 lands the create buttons, the empty state likely changes to something like "Nog geen periodes. Voeg een interventie of periode toe." Decision: revise then, not preemptively.
