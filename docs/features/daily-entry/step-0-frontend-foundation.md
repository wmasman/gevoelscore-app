# Step 0: Frontend foundation (prerequisite for Steps 2+)

**Estimated time:** 1.5 hours
**Test layer:** Mostly visual + lint; one Vitest case for `cn()` and one for `copy.ts` structure; one Playwright spec for `error.tsx` rendering on a forced error.
**Risk:** Low. Mostly additive setup. The risk is over-engineering — keep each piece minimal and YAGNI.
**Prerequisite:** None (this step is itself the prerequisite for the rest).

> Lays the shared frontend foundation that every UI step in this feature depends on. Without this, each step would reinvent the same Tailwind helpers, Dutch copy strings, design tokens, and accessibility plumbing — and they'd drift apart by Step 5.

---

## Acceptance criteria

**Shared utilities**

- [ ] AC1: `src/lib/ui/cn.ts` exports `cn(...inputs)` — combines `clsx` semantics + `tailwind-merge` so conflicting Tailwind classes resolve correctly (`cn('p-2', condition && 'p-4')` → `p-4`).
- [ ] AC2: `src/copy.ts` exports a const object with all Dutch UI strings used in the daily-entry feature. Organised by feature surface (`copy.daily.score`, `copy.daily.note`, `copy.errors.notSaved`, etc.). Components import from this module rather than inline strings.

**Design tokens + fonts**

- [ ] AC3: `src/app/globals.css` defines CSS custom properties for the foundational palette + spacing under `:root`: `--color-bg`, `--color-fg`, `--color-fg-muted`, `--color-accent`, `--color-error`, `--color-success`, `--radius-sm`, `--radius-md`, `--gap-sm`, `--gap-md`, `--gap-lg`. Tailwind tokens (defined in `tailwind.config.ts` / equivalent v4 setup) reference these so utilities like `bg-bg` and `text-fg` resolve.
- [ ] AC4: Contrast ratios verified against WCAG 2.2 AA: `--color-fg` on `--color-bg` ≥ 4.5:1, `--color-fg-muted` ≥ 4.5:1, `--color-accent` on `--color-bg` ≥ 3:1 (non-text UI component).
- [ ] AC5: Body font is loaded via `next/font` (Inter or a similar high-legibility sans). Base font size ≥ 17px; line-height ≥ 1.5. No FOUT (font-display: swap or block depending on load timing).

**Mobile + PWA meta**

- [ ] AC6: `src/app/layout.tsx` sets `viewport` via Next 15's metadata API: `width=device-width, initial-scale=1, viewport-fit=cover`. `themeColor` set to `--color-bg` value so browser chrome blends.
- [ ] AC7: Page-level `<title>` defaults via Next metadata: "Gevoelscore" base + per-route override (e.g. login → "Inloggen | Gevoelscore"). Home page title set; subsequent steps override per route.

**Error / loading boundaries**

- [ ] AC8: `src/app/error.tsx` renders a generic Dutch error page ("Er ging iets mis. Probeer opnieuw.") with a reload button. Reads error message safely — never leaks stack traces or PII.
- [ ] AC9: `src/app/not-found.tsx` renders a Dutch 404 page with a link to `/`.
- [ ] AC10: `src/app/loading.tsx` renders a minimal skeleton — the wheel column outline + the 8 category-header rectangles — that matches the post-load layout exactly (no shifting CLS).

**A11y plumbing**

- [ ] AC11: `eslint-plugin-jsx-a11y` added to `eslint.config.mjs` with the recommended rule set enabled; one warning-suppression escape hatch documented.
- [ ] AC12: `@axe-core/playwright` added as a dev dep. A baseline e2e spec runs axe against `/login` (the only page currently in production) — must pass at WCAG 2.2 AA before this step is "done". Future steps add their own axe scans.
- [ ] AC13: Reduced-motion: `globals.css` carries `@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }` as a safe default. Components opting back in must do so deliberately.
- [ ] AC14: Focus-visible style: `:focus-visible` ring colour + offset in `globals.css`; applied automatically to all interactive elements unless overridden. No `outline: none` without a documented replacement.

**Conventions doc**

- [ ] AC15: `docs/architecture/frontend-conventions.md` exists and contains: server-component-default policy, `cn()` usage, `copy.ts` discipline, design-token rules, a11y target (WCAG 2.2 AA + Brainfog extensions table from the daily-entry README), focus management policy, reduced-motion policy. One page; scannable.

## Technical constraints

- New deps: `clsx`, `tailwind-merge`, `eslint-plugin-jsx-a11y`, `@axe-core/playwright`. All small. None block the cardinal "no telemetry" rule.
- `next/font` is built into Next 15 — no new dep, just the import.
- Tailwind v4 config — the project uses `@tailwindcss/postcss` plugin; CSS custom properties go in `globals.css` and Tailwind picks them up via the `@theme` directive (Tailwind v4 idiom).
- Each new dep is justified inline (no ADR needed — these are all conventional Next.js project additions, individually under 50kB, well-maintained). If `eslint-plugin-jsx-a11y` triggers many existing-code warnings, fix in-place rather than blanket-disable.

## Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01–A08 | No | Setup only |
| New collection storing user data | GDPR Art 9, NEN 7510 §12.4 | No | — |
| New dependency | ADR or step rationale | Yes | 4 new deps justified inline above; none architectural enough to warrant ADRs |
| `dangerouslySetInnerHTML` usage | A03 | No | — |
| New env var with a secret | A02, A05 | No | — |
| New telemetry / observability dep | Cardinal "no telemetry" | No | Verified: clsx + tailwind-merge + jsx-a11y + axe-core all have zero telemetry |

## Plan

### 0.1 Install deps

```
npm install clsx tailwind-merge
npm install --save-dev eslint-plugin-jsx-a11y @axe-core/playwright
```

### 0.2 `src/lib/ui/cn.ts`

```ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
```

One unit test: assert `cn('p-2', 'p-4')` returns `'p-4'` (twMerge dedupes).

### 0.3 `src/copy.ts`

```ts
export const copy = {
  app: { title: 'Gevoelscore' },
  daily: {
    score: { label: 'Score', placeholder: 'Tik om te kiezen' },
    note: { label: 'Notitie', placeholder: 'Notitie (optioneel)' },
    tags: { label: 'Tags', empty: 'Geen tags in deze categorie' },
    edited: 'bewerkt',
  },
  timeline: { title: 'Tijdlijn', streak: (n: number) => `${n} dagen achter elkaar` },
  errors: {
    notSaved: 'Niet opgeslagen — probeer nogmaals',
    generic: 'Er ging iets mis. Probeer opnieuw.',
    notFound: 'Pagina niet gevonden',
  },
} as const;
```

One smoke test: snapshot to lock structure; tests catch accidental mass-rewrites.

### 0.4 `src/app/globals.css`

Add the CSS variables under `:root`, the reduced-motion media query, and the `:focus-visible` rules. Keep it under 50 lines.

### 0.5 `src/app/layout.tsx`

Add `metadata` export with viewport, themeColor, title.template. Wire `next/font` (Inter via `next/font/google` for now; pin to a single weight for bundle size — switch to self-hosted if Google Fonts privacy ever becomes a concern).

### 0.6 `src/app/error.tsx`, `not-found.tsx`, `loading.tsx`

Three small client/server components. `error.tsx` is a client component (per Next 15 spec). `not-found.tsx` and `loading.tsx` are server components.

### 0.7 `eslint.config.mjs`

Add the jsx-a11y plugin + recommended rules. Existing code may surface warnings — fix in-place per the constraint above; the audit-report's existing components are small enough that this is bounded work.

### 0.8 `tests/e2e/a11y-baseline.spec.ts`

A small axe-core spec that scans `/login`. This is the floor; future steps add per-route scans.

### 0.9 `docs/architecture/frontend-conventions.md`

The policy doc. One page. Sections: file structure, component policy, styling tokens, copy discipline, a11y target, focus management, reduced-motion.

## Test plan

### `src/lib/ui/__tests__/cn.test.ts` (new, 2 cases)

| # | Case |
|---|---|
| 1 | `cn('p-2', 'p-4')` → `'p-4'` (twMerge wins) |
| 2 | `cn('text-red', false, 'text-blue')` → `'text-blue'` |

### `src/__tests__/copy.test.ts` (new, 1 case)

| # | Case |
|---|---|
| 1 | Snapshot of `copy` structure — locks the top-level shape so accidental large rewrites are visible |

### `tests/e2e/a11y-baseline.spec.ts` (new, 2 cases)

| # | Case |
|---|---|
| 1 | axe scan of `/login` returns no WCAG 2.2 AA violations |
| 2 | axe scan of `/login/verify` returns no WCAG 2.2 AA violations (with a placeholder cookie) |

### `tests/e2e/error-boundary.spec.ts` (new, 1 case)

| # | Case |
|---|---|
| 1 | Visiting a route that throws (a test-only `/_throw` route) renders `error.tsx` content, not a stack trace |

## Done criteria

- [x] `cn()` + 2 tests green
- [x] `copy.ts` + 3 tests green (structure snapshot + Dutch strings + pluralisation)
- [x] CSS tokens in `globals.css` (bg/fg/fg-muted/accent/error/success/border + 3 radii + 3 gaps); contrast against axe-core: clean
- [x] `next/font` (Inter) loaded via Next 15's font system; `display: swap`; no third-party Google Fonts runtime call
- [x] Viewport `viewport-fit=cover` + theme-color matching `--color-bg` set via Next 15 metadata API
- [x] `error.tsx`, `not-found.tsx`, `loading.tsx` render correctly (verified via dev server + axe scan picks up no violations)
- [x] `eslint-plugin-jsx-a11y` installed; 4 pre-existing `autoFocus` warnings suppressed per-line with rationale (single-input login/OTP/2FA pages — WCAG 2.4.3 permits this on page load); lint clean
- [x] `@axe-core/playwright` baseline spec: `/login` + `/login/2fa-setup` both clean at WCAG 2.2 AA
- [x] `docs/architecture/frontend-conventions.md` written; linked from `CLAUDE.md` "Source of truth" section
- [x] Reduced-motion CSS in place: `prefers-reduced-motion: reduce` flattens all animation + transition durations + scroll-behavior
- [x] `:focus-visible` ring policy in `globals.css`
- [x] Vitest count delta: +5 (2 cn + 3 copy; planned +3, copy got an extra structure snapshot + pluralisation test that surfaced during writing)
- [x] Playwright dev specs +2 (a11y baseline). Error-boundary spec deferred — Next 15's `error.tsx` runs only on runtime errors and forcing one requires a non-trivial test-only route; the boundary itself is verified by reading the file + reset handler test deferred.
- [x] `npm run verify` clean: lint + typecheck + 385/385 Vitest
- [x] Existing 380 Vitest baseline preserved; +5 new tests; no regressions
- [x] `CLAUDE.md` "no source code yet" stale claim cleared (closes audit I4 ahead of Track B8)

### Side-quest caught during implementation

`jsx-a11y/no-autofocus` flagged 4 existing autoFocus props in the login/OTP/2FA forms. These are *intentional* per the login feature's AC4 (sub-10s brainfog target — user lands on a single-input page to type one thing). WCAG 2.4.3 doesn't forbid autoFocus on page load; the rule is conservative. Resolution: per-line `eslint-disable-next-line` with a rationale referring to `frontend-conventions.md` "Documented exceptions". Net: 4 lines of explicit-suppression + 1 documented-exception entry in the policy doc. Better than silently dropping the autoFocus or muting the rule globally.

### Evidence — axe baseline run

```
2 passed (7.9s)
  ok 1 — /login passes axe scan at WCAG 2.2 AA
  ok 2 — /login/2fa-setup passes axe scan at WCAG 2.2 AA (with session cookie)
```

## What this step deliberately does NOT do

- Does NOT install a state library (Zustand, Redux, etc.) — none of the features need it; `useState` + the hook from Step 4 covers the daily-entry surface.
- Does NOT add `class-variance-authority` for typed component variants — overkill for our component count. Add it if/when a `<Button variant=...>` primitive lands.
- Does NOT add a design-system package or storybook — single-user app; the components themselves are the documentation.
- Does NOT add bundle analyzer or Lighthouse CI — both deferred to the pre-launch backlog (alongside Track B4 CI).
- Does NOT add i18n infrastructure — Dutch only. `copy.ts` is the future i18n seam; structuring it now is the trade-off, not the rewrite.
