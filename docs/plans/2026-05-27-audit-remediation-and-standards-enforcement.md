# Audit remediation + standards-enforcement plan (2026-05-27)

Two-track plan triggered by [`docs/audits/2026-05-27-auth-security-and-code-audit.md`](../audits/2026-05-27-auth-security-and-code-audit.md). Track A closes the audit findings. Track B builds the rails so future features can't silently regress the same standards.

The audit itself documents *what* needs to change. This plan adds *how* and *when* — and crucially, *how to make sure the next feature doesn't reintroduce the same class of bug*.

---

## Context

The login feature shipped with 0 critical / 4 high / 7 medium findings. None catastrophic, but two patterns the audit exposed are bigger than any single fix:

1. **`.claude/security-checklist.md` and `.claude/conventions.md` are documented but not mechanically enforced.** Today they live or die by whether `/plan-feature` and `/build-step` get invoked. A future tired-evening commit can land code that violates A05 (security headers), A03 (input validation), or the no-telemetry rule with no friction.
2. **There is no CI, no pre-commit hook, no pre-push hook.** `npm test`, `npm run typecheck`, `npm run lint` exist but nothing forces them to run before code lands. Local discipline is the only safety net.

Daily-entry is the next big feature — it will store special-category personal data (GDPR Article 9). It must not ship until the standards are mechanically enforceable, not just documented.

---

## Track A — Audit remediation

The audit already groups findings by Priority 1/2/3. This plan turns each priority into a numbered step file under a feature folder, matching the established [`docs/features/login/`](../features/login/) shape — so each fix has Acceptance Criteria, Technical Constraints, Test Plan, and a Done section before any code runs.

### A1 — Priority 1 (before daily-entry ships, ~3h)

New folder: `docs/features/auth-hardening/` with 4 step files.

| # | Step | Fixes | Touches |
|---|---|---|---|
| 1 | Bind TFA secret server-side | H2 | new `src/lib/auth/pending-tfa.ts`; `2fa/generate`, `2fa/enable` route handlers; body schema drops `secret` |
| 2 | Rate-limit 2FA endpoints | H1 | `stores.ts` (+2 limiters, 5/5min by IP+session); both 2FA routes |
| 3 | Trust Fly-Client-IP over XFF | H4 | `stores.ts:getClientIp`; `current-state.md` deploy assumption |
| 4 | Security response headers | M1 | `next.config.ts` (`async headers()` + `poweredByHeader: false`); new Playwright spec asserting all 5 headers |

Verification per step: live `curl -I` snapshot recorded in the step's Done section; Vitest count delta noted; live-stack regression stays green.

### A2 — Priority 2 (hardening pass, ~3h, this month)

Same feature folder, steps 5–10:

| # | Step | Fixes |
|---|---|---|
| 5 | Extract `allowedOrigins()` to `src/lib/auth/allowed-origins.ts` | DRY (prereq for #6) |
| 6 | Hard-require allowed origins in production | M3 (throws at startup if `NEXT_PUBLIC_APP_URL` unset) |
| 7 | API-aware middleware (401 JSON instead of 307 redirect for `/api/*`) | M2 |
| 8 | Per-pending-id OTP attempt counter (cap at 3) | M5 |
| 9 | Pending-OTP password lifecycle hardening | H3 (defensive overwrite + assertion-on-log; full AES-GCM deferred unless threat model shifts) |
| 10 | Dockerfile `RUN npm audit --audit-level=high` in deps stage | L5 |

Each step bumps the regression suite. Live-stack adds one spec per step where the behaviour is observable end-to-end (specifically: 6, 7, 10).

### A3 — Priority 3 (compliance + observability, this quarter)

New folder: `docs/features/compliance-baseline/` with 3 step files.

| # | Step | Closes |
|---|---|---|
| 11 | `directus_auth_events` collection + INSERTs from route handlers (timestamp, event, outcome, hashed IP, session id) | I3, NEN 7510 §12.4 |
| 12 | `docs/privacy/article-9-basis.md` — lawful basis, data minimisation, retention, pointer to v1 export + delete | GDPR Art 9 gap |
| 13 | At-rest encryption confirmation for Neon (verify + document in [`current-state.md`](../architecture/current-state.md) "Cloud resources") | GDPR Art 32 / NEN 7510 §5.10 |
| 14 | Scope down the runtime Directus token used by `frontend_sessions`. Create a dedicated Directus user with a role + policy restricted to CRUD on `frontend_sessions` only, generate a static token for that user, swap it into the `DIRECTUS_TOKEN` Fly secret on `gevoelscore-frontend`. Removes admin-blast-radius exposure introduced by [ADR 0005](../decisions/0005-frontend-session-persistence.md). | Principle of least privilege; ADR 0005 follow-up #1 |

Step 11 is the largest: needs a Directus schema script in `directus/scripts/` (per `MEMORY.md` "Directus schema approach" — idempotent REST API scripts, no `schema apply`). The INSERTs add one line per route handler; the hashing keeps PII out of the table.

Step 14 is contained: setup-permissions-style idempotent script + one secret rotation + one rolling restart. Sequence after step 11 so the audit-events policy and the session-store policy can share a service-user pattern.

### A4 — Resolution log

Audit "Won't do" items (L2, L3, L4, L6, L7, I1, I2) get explicit `[Resolved: Won't do — see plan]` markers appended to the audit doc so the audit remains the source of truth, not this plan.

I4 (stale `MEMORY.md` claim) is closed by Track B9 below.

---

## Track B — Standards-enforcement rails

The exploration confirmed the gap: skills enforce manually, but nothing enforces at commit time, push time, or merge time. Track B layers four safety nets so the next feature can't ship the same class of bug.

### B1 — Pre-commit hook (cheap, fast feedback)

**Tool**: `simple-git-hooks` over husky. One dev dep, no postinstall surprise; for a single-developer project the husky machinery is overkill.

Hook runs `lint-staged` against staged files:
- `eslint --max-warnings 0` on `*.{ts,tsx,mjs}`
- `tsc --noEmit` (cheap — incremental via `tsbuildinfo`)
- secret scan (delegated to ESLint plugins, see B2)

Files touched:
- `package.json` — add `simple-git-hooks` + `lint-staged` configs; add `"prepare": "simple-git-hooks"` script
- New dev deps: `simple-git-hooks`, `lint-staged`

### B2 — ESLint plugins that codify the checklist

Three additions to [`eslint.config.mjs`](../../eslint.config.mjs):

| Plugin | Catches | Maps to checklist |
|---|---|---|
| `eslint-plugin-security` | Unsafe regex, eval-style sinks, child-process injection | A03 |
| `eslint-plugin-no-secrets` | High-entropy strings near `const`/`let` declarations | A05 (leaked secrets) |
| Custom `no-restricted-imports` block | `next/telemetry`, `@vercel/analytics`, `@sentry/*` | Conventions "no telemetry" rule |
| Custom `no-restricted-syntax` block | `dangerouslySetInnerHTML` not preceded by a `// @security-reviewed:` comment | A03 |

The `no-restricted-syntax` rule is the key one — it converts the checklist's "do not use without @security comment" line into a build failure.

### B3 — `npm run verify` orchestrator + pre-push hook

New scripts in `package.json`:
```json
"verify": "npm run lint && npm run typecheck && npm test && npm run test:e2e",
"verify:full": "npm run verify && npm audit --audit-level=high && npm run test:live",
"audit": "npm audit --audit-level=high"
```

Pre-push hook (via `simple-git-hooks`): runs `npm run verify`. Live-stack stays out — too slow and requires `.env.local` + a running backend; it's a CI / pre-deploy job.

### B4 — CI on GitHub Actions

New file `.github/workflows/ci.yml`. Triggered on push + PR.

Jobs:
1. **verify** — `npm ci && npm run verify` (no live-stack)
2. **audit** — `npm audit --audit-level=high` (separate so an audit failure doesn't kill the test run for triage)
3. **security-headers** — Playwright spec that boots the prod build and asserts all 5 response headers + no `X-Powered-By` (no Directus needed)

Cache: `~/.npm`, `~/.cache/ms-playwright`, `node_modules`. Total CI runtime target: under 5 minutes.

### B5 — Skill extensions (compose, don't proliferate)

Edit existing skills rather than adding new ones, except where genuinely orthogonal.

**[`.claude/commands/plan-feature.md`](../../.claude/commands/plan-feature.md)** — append Phase 5.7 "Standards enforcement check":
- For every new file the plan proposes, declare explicitly which checklist sections apply (A01–A09, GDPR Art 9 if PII, NEN 7510 §12.4 if user-action)
- Recorded as a small table in the feature README

**[`.claude/commands/build-step.md`](../../.claude/commands/build-step.md)** — add to Phase 5 Done gates:
- `npm run verify` must pass (replaces the current `npm test` + lint + typecheck individual checks)
- For new route handlers: an explicit checklist that origin check, rate limit, body validation, Result-wrappers, and `directus_auth_events` INSERT are all present (lint-style review against the file)

### B6 — New skill: `/audit-feature`

Genuinely orthogonal to the existing two, so a new skill is justified. New file `.claude/commands/audit-feature.md`.

Run after a feature lands. The skill:
1. Re-walks `.claude/security-checklist.md` against files added/modified in the feature folder
2. Runs `npm audit` and `npm run verify`
3. Diffs `package.json` vs. last audit; flags new deps lacking an ADR or step-file rationale
4. Produces a skeleton `docs/audits/{date}-{feature}-audit.md` for human review

This codifies what we did manually on 2026-05-27 — make it repeatable, not heroic.

### B7 — ADR-or-rationale gate for new deps

Lightweight: a CI step (Node script under `scripts/check-new-deps.mjs`) that diffs `package.json` against base branch. For each new entry it requires one of:
- A matching `docs/decisions/####-{dep-slug}.md`, OR
- A `<!-- dep-rationale: docs/features/{feature}/step-N.md -->` line in `package.json` (or the step file referencing it)

Failure mode is a PR comment, not a hard block — sometimes a dep lands legitimately mid-PR before the ADR is written.

### B8 — Memory hygiene

Two `MEMORY.md` updates (the file in `C:\Users\Gebruiker\.claude\projects\...\memory\`, not in repo):
- Remove the `"Pre-prototype: docs only, no source code yet"` claim (closes I4)
- Add memory: "verification gate is `npm run verify`; pre-commit + pre-push hooks live; CI on GH Actions" so future sessions don't waste time rediscovering the rails

---

## Sequencing

```
This week  [DONE 2026-05-27]
  Track A1 steps 1-4 (audit-hardening feature folder) ✅
  Track B1 + B2 + B3 (pre-commit + ESLint security + verify script) ✅
  Track B5 (skill extensions) ✅
  Track A2 steps 5-10 (hardening pass) ✅
  Track B6 (/audit-feature skill) ✅

Next:
  Daily-entry feature — the hard gate (A1 + B1-B3) is cleared, and A2 has
  further hardened the auth layer underneath. /plan-feature daily-entry.

Pre-launch backlog (deferred until before sharing with anyone else):
  - Track A3 compliance (directus_auth_events, GDPR Art 9 doc, Neon at-rest)
  - Track B4 CI on GitHub Actions (needs `git push` first)
  - Track B7 ADR-or-rationale dep gate
  - Track B8 memory hygiene (MEMORY.md "no source code yet" claim — audit I4)
  - Cleanup: src/__hook-smoke-test__.tsx removal

Discipline:
  Each Track A step uses /build-step with its step file.
  Each Track B item gets its own commit with the matching verify result.
  Daily-entry feature WAS gated on A1 + B1-B3 (now cleared).
```

---

## Critical files

**Track A — new**
- `src/lib/auth/pending-tfa.ts`
- `src/lib/auth/allowed-origins.ts`
- `tests/live-stack/security-headers.spec.ts`
- `directus/scripts/05-auth-events.mjs`
- `docs/features/auth-hardening/` (10 step files + README)
- `docs/features/compliance-baseline/` (3 step files + README)
- `docs/privacy/article-9-basis.md`

**Track A — modified**
- `src/lib/auth/stores.ts` (2 new limiters + getClientIp rewrite)
- `src/app/api/auth/2fa/generate/route.ts`, `src/app/api/auth/2fa/enable/route.ts`
- `src/middleware.ts` (API-aware branch)
- `next.config.ts` (headers + poweredByHeader)
- `Dockerfile` (audit gate)

**Track B — new**
- `.github/workflows/ci.yml`
- `.claude/commands/audit-feature.md`
- `scripts/check-new-deps.mjs`

**Track B — modified**
- `package.json` (scripts + simple-git-hooks + lint-staged configs + dev deps)
- `eslint.config.mjs` (plugins + restricted-syntax/imports)
- `.claude/commands/plan-feature.md` (Phase 5.7)
- `.claude/commands/build-step.md` (Done gates)

---

## Verification

**Track A end-state evidence** (recorded per step's Done section, summarised at end of each priority):

- Vitest count growth: 351 → ~370 (after A1) → ~395 (after A2) → ~410 (after A3)
- Live-stack: 4/4 → 5/5 (headers) → 7/7 (rate-limit on 2FA) → maintained through A2/A3
- Live `curl -I https://gevoelscore-frontend.fly.dev/login` shows: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` set; no `X-Powered-By` reflected
- The audit's "Top 5 to fix first" table all marked `[Resolved: Step N]` linking back

**Track B end-state evidence**:

- `git commit` with a deliberate lint error → rejected by pre-commit hook
- `git push` with failing test → rejected by pre-push hook
- CI run green on a representative PR (build, verify, audit, security-headers jobs all green)
- Sample feature run through `/plan-feature` shows Phase 5.7 enforced
- `/audit-feature auth-hardening` produces a skeleton audit doc
- `eslint .` flags an intentionally-introduced `dangerouslySetInnerHTML` without `@security-reviewed` comment

---

## What this plan deliberately does NOT do

- **Multi-machine deployment fix (audit I1)**: still single-machine; revisit only if a second user is ever added.
- **Refresh-cookie re-issue on rotation (I2)**: cookie value stable across refresh by design; documented, not changed.
- **AES-GCM on `pendingOtpStore` (H3 maximal fix)**: defensive-overwrite + lifecycle tightening only; full encryption deferred unless a heap-dump threat materialises.
- **Branch protection / required-reviewers on GitHub**: single-developer repo; CI green is the gate, not a second human.
- **Replacing in-memory stores with Redis / Directus-backed sessions**: orthogonal scaling concern; the auth library API is already shaped to swap stores.
