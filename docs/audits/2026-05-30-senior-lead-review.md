# Senior-lead review — 2026-05-30

Companion to [2026-05-30-app-audit.md](./2026-05-30-app-audit.md). The audit answered "what's wrong"; this answers "what kind of codebase is this, and what posture is right for the next week given that it's a one-person project with no real users, valuing fast iteration, and aiming for a professional-grade standard."

## Verdict in one paragraph

This is a genuinely professional codebase already. TypeScript strict + `noUncheckedIndexedAccess`, `eslint-plugin-jsx-a11y` + `-security` + `-no-secrets` enforced at lint time, 593 vitest unit tests + Playwright e2e + a separate live-stack test config, pre-commit lint-staged + pre-push `npm run verify`, 5 ADRs covering every real architecture pivot, separate `docs/` subtrees for architecture / operations / compliance / decisions / design / features / audits, idempotent Directus schema scripts, and operations runbooks for deploy + rotate + wipe. The bar is already above where most solo projects ever get — the question isn't "how do we become professional" but "what specifically is missing to keep this defensible as the surface grows."

## What's already strong (don't undo)

- **TypeScript discipline**: strict + `noUncheckedIndexedAccess` + `noImplicitOverride` + `noUnusedLocals`/`noUnusedParameters` ([tsconfig.json:10-15](../../tsconfig.json#L10)). This stays.
- **Lint policy embeds standards**: a11y + security + no-secrets plugins ([package.json:58-60](../../package.json#L58)). Standards are reachable through `npm run lint`, not external docs.
- **Multi-layer testing**: unit (Vitest) + e2e (Playwright) + live-stack ([package.json:17-23](../../package.json#L17)). The live-stack config is the unusual bit — most solo projects skip integration entirely.
- **TDD doctrine actually followed**: every fix this week (auth, popout, data flow) was RED → GREEN → REFACTOR. The doctrine isn't aspirational, it shows up in git history.
- **ADRs cover decisions, not implementations**: 0001 Expo→PWA pivot (superseded but kept), 0002 PWA + Directus reasoning, 0003 Fly + Neon (with amendment), 0004 tag provenance, 0005 frontend session persistence. Each one is a future-self briefing for "why this is shaped like this."
- **Operations docs**: credentials inventory + deploy/rotate/wipe runbooks. Solo projects rarely have these.
- **Repo hygiene**: LICENSE (MIT for code) + LICENSE-DOCS (CC BY-SA 4.0 for docs) + a README that gives the architecture in 5 lines + a working repo tour.
- **Per-feature TDD plans**: `docs/features/{name}/README.md` + numbered step files. Discoverable, sequenceable, resumable.

## Genuine gaps for "professional defensible"

Each of these is a one-PR move. Listed in approximate order of leverage.

### 1. No CI on push or PR

The pre-push hook is local. If you push from another machine (or `prepare`'s `simple-git-hooks` install was skipped), nothing catches a regression before it lands on `main` — and `main` deploys to prod. The pre-push hook ran clean for the last three commits, but it's load-bearing.

**Recommendation**: a single GitHub Actions workflow at `.github/workflows/verify.yml` running `npm ci && npm run verify` on `push` to `main` and on pull requests. ~30 minutes. Closes the "what if my hook didn't run" gap permanently.

### 2. No dependency-update automation

`package.json` has 30+ deps. Without Dependabot or Renovate, drift accumulates silently until a CVE forces a panic-update (we just had one — Next.js 15.5.18 patched CVE-2025-29927; would have been caught earlier with weekly bumps).

**Recommendation**: enable Dependabot on the repo with weekly schedule and grouped updates (`patches`, `minor` separate from `major`). Free, 1-file config.

### 3. Audit findings have no tracker

Three audit docs, ~70 findings between them, no central "what's open / what's done / what's been triaged-as-won't-fix" view. Findings rot into "we audited that once" without follow-through.

**Recommendation**: pick one of (a) a single `docs/audits/OPEN.md` updated when fixes land, or (b) GitHub Issues opened per finding tagged `audit:a11y`, `audit:security`, etc. (b) plays better with PR linking; (a) is zero-overhead but easier to forget.

### 4. No coverage floor + no bundle-size budget

`npm run test:coverage` exists but isn't enforced. Same for bundle size — Next.js can quietly add 80kb to a route. A "professional codebase" assertion needs measurable backing.

**Recommendation**: add `--coverage --coverage.lines=70 --coverage.branches=65` to the test command (start lenient, ratchet up). Add `@next/bundle-analyzer` and a CI step that fails if the home route's JS bundle exceeds, e.g., 200kb gzipped. Both are catch-on-CI items.

### 5. Single-user assumption isn't gated, just documented

`day_entries` has no `user_created`/`user_id` filter — see audit finding S-H3. ADR 0005 documents the follow-up. But "documented" doesn't prevent a teammate (or future-you on a long-weekend break) from minting a second test user and silently corrupting Willem's data. There's no schema gate enforcing the single-user contract.

**Recommendation**: in the meantime (until multi-user lands), add a runtime guard in `src/lib/auth/get-validated-session.ts` or middleware that rejects any session whose underlying Directus user id isn't `WILLEM_USER_ID` (a Fly secret). Two lines. Tear it out the day v1.5 multi-user gates land.

## Architectural concerns from a scalability angle

These come from the same audit but framed as "what would block scaling beyond solo":

- **`day_entries` has no per-user column** — already a S-H3 finding. Hard gate for v1.5. Addressing it requires schema migration + every API call updated + a test asserting cross-read fails. Half-day of work.
- **Frontend holds the Directus admin static token** — S-H1. Single highest-leverage security fix. Doesn't change behavior, dramatically shrinks blast radius. ~1 hour including runbook update.
- **Session store lock is per-Fly-machine** — the in-process `Map<sessionId, Promise>` lock works because `fly.toml` has `min_machines_running = 1`. The day you scale horizontally, parallel refreshes race again across machines. Document this in `get-validated-session.ts` and in ADR 0005's "scope" section.
- **Route handlers each carry ~10 lines of identical preamble** (origin + rate-limit + session-validate). Six handlers, 60 lines of duplicate boilerplate. A `withAuthAndRateLimit(handler, options)` wrapper would DRY this AND make the security policy auditable in one place. Refactor opportunity, not urgent.

## Anti-patterns to consciously NOT adopt

The "make it professional" instinct can over-engineer for a solo project. Skip these until usage actually demands:

- **Storybook**: pure overhead at this scale. Component lab pattern (`src/components/lab/`) is the right substitute.
- **Staging environment**: deploys complete in 90 seconds, rollback is `flyctl machines restart`, and there are no users to protect. Stay single-environment until adding a tester.
- **Error tracking (Sentry, etc.)**: privacy stance + single user. Acceptable trade-off; document why in ADR 0002.
- **Microservices / domain split**: cardinal principle is "simple." One Next.js app + one Directus + one Postgres is exactly right.
- **OpenAPI spec generation**: the API has 6 routes, all called from the same Next.js app. Documented inline. Don't.
- **Container-based dev environment (Devcontainer)**: skip until a contributor needs it. `npm install && npm run dev` already works from a clean clone.

## Proposed sequencing for "this week"

The user asked for: all high security + all other med/high. Audit produced 14 highs and 19 mediums = 33 items, plus the iOS sheet bug surfaced this morning (already coherent in the working tree). A realistic week of solo work, day-by-day:

### Day 0 — half-hour, before any other fix

- Add `.github/workflows/verify.yml` running `npm run verify` on push + PR.
- Enable Dependabot via `.github/dependabot.yml` (weekly, grouped).
- Optional: create `docs/audits/OPEN.md` listing every finding as a checkbox so we can tick them off.

This guards every subsequent day's commits.

### Day 1 — visible polish wins (~4 hours)

Cluster of low-risk, high-visibility changes the user will feel immediately.

- [ ] **iOS sheet fix** (BottomSheet `maxHeight` + flex column; QuickEntryFlow `flex-1 min-h-0`; NoteField `flex-1` textarea) — sitting in working tree, ship as part of today
- [ ] **M-C1**: PWA manifest + `apple-touch-icon` + `apple-mobile-web-app-capable` meta. Re-install on phone after deploy.
- [ ] **A-H3 + M-H3**: 44×44 sweep — close ✕, settings cog, tag chips, "Toon meer", tabs. One PR.
- [ ] **D-H1**: replace `animate-pulse` blocks in [loading.tsx](../../src/app/loading.tsx) with static `bg-surface-muted` skeletons.
- [ ] **D-H2**: `text-white` → `text-bg`; `bg-[var(--color-accent)]` → `bg-accent` in [error.tsx](../../src/app/error.tsx) + [not-found.tsx](../../src/app/not-found.tsx).
- [ ] **D-M1**: `"Weet je het zeker?"` → `"Bevestigen."`
- [ ] **D-L2**: `"Annuleer"` → `"Annuleren"`.
- [ ] **A-M3, A-M4**: darken `--color-fg-subtle` to ~`#7b6d5f` (≈4.5:1) — visible everywhere immediately.

### Day 2 — accessibility high (~4 hours)

- [ ] **A-H1**: remove 500 ms score auto-advance, OR gate it behind `!prefers-reduced-motion` + lengthen to 1500 ms with a visible cancel affordance.
- [ ] **A-H2 + M-L3**: initial focus inside `QuickEntryFlow` lands on the active step's primary control (score circle / note textarea / first tag chip) — `BottomSheet` takes `initialFocusRef`.
- [ ] **A-H4**: single page-level live region; one announcement per "saved" transition, throttled to ≥5 s; readable text in `sr-only` span.
- [ ] **A-H5**: clarify `BottomSheet` handle semantic — either make it a real button or accept it's cosmetic and widen the close ✕ to 44×44 in Day 1's sweep.
- [ ] **A-M2**: `aria-valuetext` on `ScoreCircle` ("`${value} van 10`").
- [ ] **A-M5**: suppress auto-advance + pulse-class-toggle when `prefers-reduced-motion`.
- [ ] **A-M6**: logout confirm focuses the Cancel button on entry to `confirming`.

### Day 3 — mobile + layout (~4 hours)

- [ ] **M-H1**: `min-h-screen` → `min-h-dvh` on the 6 top-level shells; add `padding-bottom: env(safe-area-inset-bottom)` to `<main>`.
- [ ] **M-H2**: move tab switcher to a fixed bottom bar; padding-bottom on `<main>` so the last past-day card doesn't get occluded.
- [ ] **M-H4**: scope `hover:` to pointer devices globally (`@media (hover: hover)` wrapper or a `globals.css` reset for `(hover: none)`); drop the `!` workaround on the pulse class.
- [ ] **M-M2**: `html, body { overscroll-behavior: none; }` in globals.css.
- [ ] **M-M6**: `-webkit-tap-highlight-color: transparent;` on body.
- [ ] **M-M3**: drop `flush: true` on the score commit so keyboard arrow-bursts coalesce.
- [ ] **M-M4**: auto-switch to Heatmap when `range === 90` on chart.

### Day 4 — security S-H1 + S-M cluster (~5 hours)

The single highest-leverage day of the week.

- [ ] **S-H1**: provision a Directus role + policy + user scoped to CRUD on `frontend_sessions`. Mint static token. Set `DIRECTUS_TOKEN` on Fly. Rotate existing admin token. Update [docs/operations/runbooks/rotate-credentials.md](../operations/runbooks/rotate-credentials.md).
- [ ] **S-M1**: rename cookies to `__Host-gs_session` / `__Host-gs_pending_otp`. Re-login once; verify Set-Cookie headers.
- [ ] **S-M2**: tighten origin check — reject POST/PUT/PATCH/DELETE with neither Origin nor Referer.
- [ ] **S-M3**: `setInterval` sweep for rate-limiters + pending stores in `stores.ts`.
- [ ] **S-M4**: wrap `store.peek(sessionId)` in try/catch inside `getValidatedSession`.
- [ ] **S-M5**: add permissive read rate limiter on `/api/day-entries` + `/api/day-entries/today` (120/min).

### Day 5 — security S-H2 + S-H3 prep + design tail (~4 hours)

- [ ] **S-H2**: AES-256-GCM encrypt `access_token` + `refresh_token` columns in `frontend_sessions`. Key from a new Fly secret (NOT `DIRECTUS_TOKEN`). Migrate existing rows.
- [ ] **S-H3 prep**: add `user_created` column on `day_entries`, `tags`, `day_entries_tags`, `frontend_sessions` via Directus migration. Don't enforce filtering yet — single-user app — but the column needs to exist before any second tester logs in.
- [ ] Add the runtime "reject any session whose Directus user ID isn't Willem" guard recommended above. Two lines, immediate single-user gate.
- [ ] **D-M2**: extract inline Dutch literals on auth pages + error/not-found into `copy.ts`.
- [ ] **D-M3**: extract `'Klaar'`, `'Sluiten'`, `'Schermen'`, `'Bereik'`, `'Weergave'` and the past-day `aria-label` template into `copy.ts`.
- [ ] **D-L1**: `TRANSITION_MS = 250` → `200` in [bottom-sheet.tsx](../../src/components/lab/bottom-sheet.tsx).

### Explicitly deferred (not "this week")

- **A-M1**: `ScoreChart` roving-tabindex + accessible trend summary. Bigger refactor. Defer to a dedicated chart-a11y session.
- **M-M1 / M-M5**: BottomSheet content sizing edge cases beyond today's fix (drag-while-keyboard-up math). Re-evaluate after the user soak-tests today's iOS fix on their phone.
- **S-L2 + S-L4**: per-email rate limit + per-IP OTP attempt counter. Multi-user concerns; defer with S-H3.
- **S-L1**: CSP nonce-based inline scripts. Wait for a Next.js 15.x point release that ships native support.
- **A-L1-L3 + S-L3 + D-L3 + D-I1**: low-severity polish, no rush.

## Recommendation on next move

I propose:

1. Ship the iOS sheet fix as a standalone commit right now (it's a real visible production bug, sitting coherent in the working tree, verify is green).
2. Then before any other fix, land the Day 0 setup (`.github/workflows/verify.yml` + Dependabot + `docs/audits/OPEN.md`) as a separate small commit — that guards every subsequent commit.
3. Then proceed Day 1 → 5 as sequenced above.

This sequencing gets the user-facing bug into prod within minutes, hardens the rest of the week's commits behind CI before risking them, and front-loads visible-impact work over invisible structural work so each day has something the user can feel.
