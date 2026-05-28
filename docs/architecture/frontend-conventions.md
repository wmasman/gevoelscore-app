# Frontend conventions

Operational policy for the Next.js + React + Tailwind frontend. Adopted 2026-05-28 as part of [daily-entry Step 0](../features/daily-entry/step-0-frontend-foundation.md). Cross-cutting decisions that every component touches; documenting them once so they don't drift across step files.

Pairs with [`.claude/conventions.md`](../../.claude/conventions.md) (project-wide rules) and [`.claude/security-checklist.md`](../../.claude/security-checklist.md) (OWASP ASVS). This doc covers the UI surface specifically.

---

## Component policy

### Server components are the default

Use server components unless the file genuinely needs client-only APIs (state, refs, event handlers, browser APIs). The `'use client'` directive is opt-in, not default. Server components stream HTML, read cookies via `next/headers`, and call the SDK directly without HTTP hops.

### `'use client'` triggers

Add `'use client'` only when one of these is present:
- `useState`, `useReducer`, `useRef`, `useEffect`, `useContext`
- DOM event handlers (`onClick`, `onChange`, etc.)
- Browser APIs (`window`, `document`, `localStorage`)
- Third-party client-only libraries

Pass server-fetched data down as props; let the client component own only the interactivity.

### File structure

- `src/app/` — route segments (App Router conventions)
- `src/components/` — shared components used by multiple routes
- `src/hooks/` — shared React hooks
- `src/lib/ui/` — pure UI utilities (`cn`, formatters)
- `src/lib/auth/`, `src/lib/api/`, `src/lib/domain/` — non-UI library code
- `src/__tests__/copy.test.ts` — top-level test for the copy module
- Component tests in `src/components/__tests__/<name>.test.tsx`
- Hook tests in `src/hooks/__tests__/<name>.test.ts`

### Styling: utility-first Tailwind + design tokens

- All styling via Tailwind utility classes. No CSS modules, no styled-components.
- Conditional classes go through `cn()` from `src/lib/ui/cn.ts`. Never string-concat classes manually.
- Design tokens (colours, radius, gap) live as CSS custom properties in `src/app/globals.css` and are exposed to Tailwind via `@theme`. Components reference tokens (`bg-bg`, `text-fg`, etc.), not raw hex values.
- Dark mode + accessibility theming is deferred to v1.5+; the token layer is the seam that makes it tractable.

### Copy discipline

All user-facing Dutch strings live in `src/copy.ts`. Components import `import { copy } from '@/copy'` and reference `copy.daily.score.label`. Inline string literals in JSX are a smell; fix in code review.

This is the future i18n seam — structured *now* so v1.5/v2 multi-language is a refactor, not a rewrite.

---

## Accessibility target

### Formal: WCAG 2.2 Level AA

Enforced by three layers:

1. **Lint time**: `eslint-plugin-jsx-a11y` (recommended ruleset) catches missing labels, click-without-keyboard, bad ARIA roles. Pre-commit hook blocks errors.
2. **e2e time**: `@axe-core/playwright` scans pages for contrast, ARIA, structure violations. Baseline lives at `tests/e2e/a11y-baseline.spec.ts`; new UI steps add per-feature scans.
3. **Manual at Done time**: every `/build-step` Done section gains "keyboard-only flow works" and "VoiceOver announces correctly" for components that touch new ARIA.

### Brainfog extensions (above WCAG)

WCAG doesn't directly address cognitive fatigue. Long COVID makes those exact gaps the highest-stakes. Five project-wide rules:

| Brainfog rule | WCAG floor | Project target |
|---|---|---|
| Touch targets | 24×24 (AA), 44×44 (AAA) | ≥ 48×48 |
| Body text size | 16px implied | ≥ 17px @ default zoom, line-height ≥ 1.5 |
| Animation duration | No specific rule | ≤ 200ms; `prefers-reduced-motion` disables |
| Information density | No specific rule | Max 5 primary actions visible at once |
| Time pressure | SC 2.2.1 (adjustable timers) | No timers on user-facing flows |

### Specific WCAG 2.2 SCs needing per-step attention

The rest fall out of `jsx-a11y` + axe; these need explicit thought in each step:

- **1.4.3 Contrast (Min) 4.5:1** — text contrast. Enforced via the CSS tokens chosen in Step 0.
- **1.4.10 Reflow** — usable at 320px width with no horizontal scroll.
- **2.1.1 Keyboard** — every interactive element keyboard-operable.
- **2.4.3 Focus Order** — logical (top-to-bottom, left-to-right).
- **2.4.7 Focus Visible** — `:focus-visible` ring on every interactive element. Default in `globals.css`; do not override with `outline: none` without a replacement.
- **2.5.5 Target Size** — ≥ 48 (above AA's 24×24).
- **3.3.1 Error Identification** — covered by the shared `<SaveStatus />` component.
- **4.1.2 Name, Role, Value** — explicit ARIA roles for non-standard widgets (e.g. the score wheel uses `role="spinbutton"` + `aria-valuenow/min/max`; sheets use `role="dialog"` + focus trap).

### Documented exceptions

- **`autoFocus` on single-input pages** (login email, OTP, 2FA password) — `jsx-a11y/no-autofocus` is suppressed per-line with a comment. WCAG 2.4.3 permits autoFocus on page load; the rule is overly conservative. Suppressions live only on truly single-input phases — never on multi-field forms.

---

## Focus management

When a sheet, modal, or any focus-trap surface opens:
1. Move focus *into* the surface (to the close button, or to the first natural input if there isn't a close).
2. Trap `Tab` / `Shift+Tab` within the surface while open.
3. `Escape` closes the surface.
4. On close, return focus to the element that triggered the open.

When navigating between pages, Next.js handles focus by default (resets to the page root). Don't fight it.

---

## Reduced motion

`globals.css` carries a `@media (prefers-reduced-motion: reduce)` block that flattens all animation + transition durations to `0.01ms`. Components opting back in must do so deliberately — typically with a `motion-safe:` Tailwind variant for visual polish, never for functional motion.

---

## Error + loading boundaries

The App Router root has:
- `src/app/error.tsx` — generic error page (never leaks message / stack to user; technical detail goes to server logs).
- `src/app/not-found.tsx` — Dutch 404 with link home.
- `src/app/loading.tsx` — skeleton matching the post-load layout (no CLS).

Per-route `error.tsx` / `loading.tsx` files (under nested route segments) are added when a route has notably different boundaries. Default is to rely on the root.

---

## Common gotchas

Patterns that have already cost ≥15 minutes of debugging. Documented here so the next iteration recognises the symptom in 30 seconds.

### Vitest `waitFor` does not progress under `vi.useFakeTimers()`

**Symptom**: a hook test using `await waitFor(() => expect(...).toBe(...))` times out at 5000ms with no obvious reason. Tests that don't use `waitFor` (e.g. checks immediately after `act`) pass fine.

**Cause**: `waitFor` polls in real wall-clock time, but fake timers freeze `setTimeout` / promises that resolve via microtask scheduling. The polled assertion never reflects the awaited state.

**Fix**: switch fake timers per-test rather than per-suite. Only enable `vi.useFakeTimers()` in the specific tests that advance time (debounce / settle cases). All other tests use real timers.

```ts
// Right
describe('useThing', () => {
  afterEach(() => { vi.useRealTimers(); cleanup(); });

  it('debounce coalesces', () => {
    vi.useFakeTimers();   // explicit in this test only
    // ... vi.advanceTimersByTimeAsync
  });

  it('error path', async () => {
    // real timers (default) — waitFor works
    await waitFor(() => expect(result.current.status).toBe('error'));
  });
});

// Wrong: vi.useFakeTimers() in beforeEach — breaks waitFor in every test
```

### Next 15 injects a hidden `role="alert"` route announcer

**Symptom**: `page.getByRole('alert')` throws "strict mode violation: resolved to 2 elements" — your real alert + something with `id="__next-route-announcer__"`.

**Cause**: Next 15's App Router inserts a hidden ARIA-live region for screen-reader navigation announcements. It has `role="alert"` and no text content.

**Fix**: select by content, not by role.

```ts
// Right
await expect(page.getByText(/niet opgeslagen/i)).toBeVisible();

// Wrong: ambiguous in any Next app
await expect(page.getByRole('alert')).toBeVisible();
```

If you genuinely need role-based selection, filter out the announcer:

```ts
const ours = page.getByRole('alert').and(
  page.locator(':not([id="__next-route-announcer__"])'),
);
```

### Tailwind v4: prefer canonical class names over `[var(...)]`

**Symptom**: VS Code's Tailwind IntelliSense flags `text-[var(--color-fg-muted)]` with "can be written as `text-fg-muted`". Both work at runtime; the arbitrary-value form bloats the CSS output and obscures intent.

**Cause**: the `@theme` directive in `globals.css` exposes our CSS variables as Tailwind utility classes directly. Tailwind v4 prefers the canonical form because it can statically analyse it (smaller bundle, better autocomplete).

**Fix**: use the token-named class.

```tsx
// Right
<div className="bg-bg text-fg border-border ring-accent" />

// Wrong (arbitrary-value form — works but slower + ugly)
<div className="bg-[var(--color-bg)] text-[var(--color-fg)] border-[var(--color-border)] ring-[var(--color-accent)]" />
```

If a token isn't yet defined in `@theme`, add it there (see `globals.css`) rather than reaching for `[var(...)]`.

**When to add a lint rule for this**: when we catch the same regression in a code review 2+ times after this doc lands. Then install `eslint-plugin-better-tailwindcss` with auto-fix.

---

## What this doc deliberately does NOT specify

- **Component library**: no `<Button>` primitive yet. Tailwind utilities are the design system for v1. Promote to a primitive when a third surface (settings, import UI) needs it.
- **State management**: no global state lib. React state + the shared `useDayEntryUpsert(date)` hook cover v1.
- **Theme tokens for dark mode**: the CSS-variable layer is the seam; the actual dark-mode palette is v1.5+.
- **Storybook / visual regression**: single-user app at v1; overkill. Revisit pre-launch if a second user is added.

---

## Cross-references

- [`docs/design/brief.md`](../design/brief.md) — design brief (above-WCAG visual identity: warm-earth palette, Things-3 anchor, Dutch tone, forbidden patterns). This conventions doc carries the *floor*; the brief carries the *direction*.
- [`docs/features/daily-entry/README.md`](../features/daily-entry/README.md) — the feature that drove the foundation work.
- [`docs/features/daily-entry/step-0-frontend-foundation.md`](../features/daily-entry/step-0-frontend-foundation.md) — the step that implemented it.
- [`docs/audits/2026-05-27-auth-security-and-code-audit.md`](../audits/2026-05-27-auth-security-and-code-audit.md) — the audit that informed the security half of the standards layer.
- [`.claude/conventions.md`](../../.claude/conventions.md) — project-wide rules (file structure, naming, no telemetry, etc.).
- [`.claude/security-checklist.md`](../../.claude/security-checklist.md) — security checklist (OWASP ASVS curated).
