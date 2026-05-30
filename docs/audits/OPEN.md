# Open audit findings

Central tracker for findings from the audit docs in `docs/audits/`. Each item links to its detail in the source audit. Tick items when they ship to prod; explicitly mark wont-fix with a short rationale.

**Sources:**
- [2026-05-27-auth-security-and-code-audit.md](./2026-05-27-auth-security-and-code-audit.md)
- [2026-05-28-daily-entry-audit.md](./2026-05-28-daily-entry-audit.md)
- [2026-05-30-app-audit.md](./2026-05-30-app-audit.md) — four-perspective audit (a11y / security / mobile / design)

**Sequencing:** see [2026-05-30-senior-lead-review.md](./2026-05-30-senior-lead-review.md) for the Day 0 → Day 5 plan.

---

## Week of 2026-05-30 — in scope

### Day 0 — repo infra (guards every subsequent commit)

- [x] GitHub Actions `verify` workflow on push + PRs
- [x] Dependabot weekly grouped updates
- [x] This `OPEN.md` tracker

### Day 1 — visible polish

- [x] iOS sheet fix (M-M1 deeper repro) — shipped `a238ca8`
- [x] M-C1 / D-L3: PWA manifest + apple-mobile-web-app meta tags (icons deferred — need design assets)
- [x] A-H3 / M-H3: 44×44 sweep — close ✕, settings cog, tag chips, "Toon meer", tabs
- [x] D-H1: replace `animate-pulse` skeleton with static `bg-surface-muted` blocks in `loading.tsx`
- [x] D-H2: `text-white` → `text-bg`, `bg-[var(--color-accent)]` → `bg-accent` in `error.tsx` + `not-found.tsx`
- [x] D-M1: `"Weet je het zeker?"` → `"Bevestigen."`
- [x] D-L2: `"Annuleer"` → `"Annuleren"`
- [x] A-M3: darken `--color-fg-subtle` to `#7b6d5f` for ≥4.5:1 AA contrast
- [x] A-M4: documented `text-accent` size rule in globals.css (≥24 px or bold ≥18.66 px); smaller call sites → `text-accent-active`

### Day 2 — accessibility high

- [x] A-H1: removed 500 ms score auto-advance; replaced with explicit "Volgende: notitie" button (disabled until first commit, anti-anchoring)
- [x] A-H2 / M-L3: initial focus on the active step's primary control via `data-autofocus` selector in `useFocusTrap`
- [x] A-H4: `SaveAnnouncer` page-level live region; one announcement per "saved" transition; throttled to ≥5 s
- [x] A-H5: close ✕ widened to 44×44 in Day 1 covers this — handle stays `aria-hidden` as cosmetic
- [x] A-M2: `aria-valuetext={'${value} van 10'}` on ScoreCircle
- [x] A-M5: pulse suppressed in TodayShell when `prefers-reduced-motion` (auto-advance already removed in A-H1)
- [x] A-M6: logout confirm wraps in `role="alertdialog"` and focuses Cancel button on state transition

### Day 3 — mobile + layout

- [x] M-H1: `min-h-screen` → `min-h-dvh` on the 6 top-level shells; `padding-bottom: max(p,env(safe-area-inset-bottom))`
- [x] M-H2: bottom tab bar (fixed `<nav>` outside `<main>`; main padding-bottom accounts for it)
- [x] M-H4: `@media (hover: none)` reset reverts `:hover` styles on touch devices
- [x] M-M2: `html, body { overscroll-behavior: none; }`
- [x] M-M6: `body { -webkit-tap-highlight-color: transparent; }`
- [x] M-M3: dropped `flush: true` on score commit so keyboard arrow bursts coalesce
- [x] M-M4: TimelineView auto-switches to Heatmap when range=90

### Day 4 — security S-H1 + S-M cluster

- [ ] S-H1: provision Directus role + policy + user scoped to CRUD on `frontend_sessions`; rotate admin token; update `docs/operations/runbooks/rotate-credentials.md`
- [ ] ~~S-M1: cookie rename to `__Host-gs_session` / `__Host-gs_pending_otp`~~ — **deferred**: ~16 test files hardcode `'gs_session='` in Cookie header literals; the mechanical churn outweighs the residual real risk on a single-subdomain Fly deployment. Re-evaluate when multi-subdomain or production exposure changes.
- [x] S-M2: origin check rejects state-changing methods (POST/PUT/PATCH/DELETE) with neither Origin nor Referer. GETs stay lenient (Safari quirk).
- [x] S-M3: `setInterval(.unref())` every 25 min in `stores.ts` sweeping all 5 rate limiters + 2 pending stores. Guarded with `globalThis.__gsAuthSweeper` against dev hot-reload duplicates.
- [x] S-M4: `store.peek(sessionId)` wrapped in try/catch in `getValidatedSession` — transient Directus errors return null (caller redirects to /login + retries on next request) rather than bubbling as 500.
- [x] S-M5: `dayEntryReadRateLimiter` (120/5min) wired to `/api/day-entries` (range) + `/api/day-entries/today` (single).

### Day 5 — security S-H2 + S-H3 prep + copy migration + design tail

- [ ] S-H2: AES-256-GCM encrypt `access_token` + `refresh_token` columns in `frontend_sessions`
- [ ] S-H3 prep: add `user_created` column on `day_entries`, `tags`, `day_entries_tags`, `frontend_sessions` (column only; filtering enforced in v1.5)
- [ ] Runtime single-user gate: reject any session whose Directus user id ≠ Willem's (two-line guard with a Fly secret)
- [ ] D-M2: extract inline Dutch literals on auth pages + error/not-found into `copy.ts`
- [ ] D-M3: extract `'Klaar'`, `'Sluiten'`, `'Schermen'`, `'Bereik'`, `'Weergave'`, past-day `aria-label` template into `copy.ts`
- [ ] D-L1: `TRANSITION_MS` 250 → 200 in `bottom-sheet.tsx`

---

## Deferred (not in week 2026-05-30)

These are real findings but explicitly out of scope this week. See the senior-lead review for reasoning.

- A-M1: ScoreChart roving-tabindex + accessible trend summary — bigger refactor, dedicated session.
- M-M1 / M-M5: BottomSheet drag-math edge cases beyond today's fix — re-evaluate after soak.
- S-L1: CSP nonce-based inline scripts — wait for Next.js 15.x native support.
- S-L2 + S-L4: per-email rate limit + per-IP OTP attempt counter — multi-user concerns, ship with S-H3 proper.
- A-L1, A-L2, A-L3, A-I1, S-L3, S-I1, S-I2, M-L1, M-L2, M-I1, D-L1, D-I1: low-severity polish, no fixed timing.

---

## Wont-fix (with rationale)

(Empty for now.)

---

## How to use this file

- Tick a box when the fix is committed AND deployed to prod.
- For multi-PR items (e.g. S-H1's role + token + rotation + runbook), tick the parent when ALL parts have landed.
- If a finding is contested or deferred, MOVE it to "Deferred" with a one-line reason — don't leave it indefinitely unticked.
- Re-run the relevant audit (or a tighter follow-up) when ticking ≥ 50 % of items, so we know the picture is current.
