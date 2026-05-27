---
description: Audit a feature after it lands. Re-walks the security checklist + conventions + dep hygiene against the feature's files; produces a skeleton audit doc under docs/audits/ for human review.
---

# Audit Feature

Codifies what the 2026-05-27 auth audit did manually. Run this *after* a feature is implemented and merged, to catch the class of issue `/build-step`'s per-step gates can miss: cross-cutting concerns, dep churn, convention drift, and standards-checklist coverage at the feature level.

**Pairs with**: [`/plan-feature`](plan-feature.md) (declares what the feature touches), [`/build-step`](build-step.md) (enforces per-step gates during implementation).

**Refers to**: [`.claude/security-checklist.md`](../security-checklist.md), [`.claude/conventions.md`](../conventions.md), [`.claude/testing.md`](../testing.md), [`docs/audits/2026-05-27-auth-security-and-code-audit.md`](../../docs/audits/2026-05-27-auth-security-and-code-audit.md) (the template the skill recreates).

## When to use

- After a feature folder's last step is committed and deployed.
- After a sequence of related features has landed (e.g. "audit everything that touched auth this month").
- When the user says "are we good to ship this?" — for a sanity pass before exposing to anyone but the user themselves.

**Don't use** during active implementation — `/build-step` covers in-flight gates. This skill assumes the code is settled.

## Inputs

- A feature name (`/audit-feature daily-entry`) — scopes to files in `docs/features/<name>/` + their declared touched files.
- A path glob (`/audit-feature src/lib/auth/`) — scopes to a directory.
- A commit range (`/audit-feature commit-range HEAD~10..HEAD`) — useful for "everything since the last audit."
- No argument → ask which feature / scope.

## Outputs

A skeleton audit doc at `docs/audits/<YYYY-MM-DD>-<scope>-audit.md` following the structure of the existing [2026-05-27 audit](../../docs/audits/2026-05-27-auth-security-and-code-audit.md). The skill does NOT mark findings as fixed — the human reviewer fills in severity calibration, decides Priority 1/2/3 buckets, and either fixes during the review or schedules them.

---

## Phase 1: Establish scope

### 1.1 Resolve the input

- Feature name → list files via `docs/features/<name>/README.md` + step files' declared "touches" sections + `git log --diff-filter=AM --name-only` for the feature's commit range.
- Path glob → resolve via `Glob`.
- Commit range → `git diff --name-only <range>`.

Output: a flat list of files in scope. **Stop and confirm with the user** if the list is empty or unexpectedly small.

### 1.2 Read the feature plan (if any)

`docs/features/<name>/README.md` should declare which checklist sections the feature touched (Phase 5.7 of `/plan-feature` mandates a Standards-enforcement table per step). The audit cross-references claims-vs-reality:

- Does every step's "Standards-enforcement" table match the actual code?
- Did any step claim "no new route handler" but a route file landed? (drift signal)
- Did any step claim "no new dependency" but `package.json` changed? (dep drift signal)

### 1.3 Snapshot the current state

Three things go into the audit's "What's in scope" section:

- File count + LOC (`wc -l` over the in-scope files).
- Test count (`npm test 2>&1 | grep "Tests"`).
- Deploy status (commit hash + Fly app name + URL).

---

## Phase 2: Run the standards checks

Each check produces zero or more findings. A finding has: severity (Critical/High/Medium/Low/Informational), category (A0X / GDPR / NEN), path + line, and a one-sentence "fix" suggestion.

### 2.1 OWASP Top 10 + ASVS walk

For each file in scope, walk the checklist line-by-line. Specific automated probes:

| Check | How |
|---|---|
| A01 — every API route requires auth | Grep for `route.ts` files; for each, verify `getValidatedSession` or `cookies()` + session check is present |
| A02 — cookies HttpOnly+Secure+SameSite=Strict | Grep for `Set-Cookie` builders; verify attributes |
| A03 — Zod / domain validators on every body field | For each `await request.json()`, verify subsequent narrowing through a validator |
| A03 — no `dangerouslySetInnerHTML` without `@security-reviewed:` | ESLint rule catches this; report any suppressions |
| A04 — rate limit on state-changing endpoints | Grep route handlers for `rateLimiter.check` calls |
| A05 — security headers present | Verify `next.config.ts` `headers()` block matches the audit baseline |
| A07 — generic error responses | Grep for `error: '...'` in route handlers; verify the user-facing strings are coarse (no "user not found", no stack traces) |
| A08 — origin check on every state-changing endpoint | Grep for `validateOrigin` |
| A09 — no PII in logs | Grep for `console.log` / `console.error` / `console.warn` near user-input variables (email, password, note) |
| A10 — no user-controlled fetch URLs | Grep server-side `fetch(` calls; verify URLs are not built from request body |

### 2.2 GDPR Article 9 walk (if the feature touches health data)

- Does the feature add new fields to `day_entries` or related collections? If yes, confirm:
  - Audit-log INSERT placeholder is present (`TODO(I3)`) per A3 compliance backlog
  - Export endpoint is unaffected (still covers the new fields)
  - Delete-all endpoint is unaffected (still removes the new fields)
  - Retention policy line in `docs/features/<name>/README.md` Privacy section

### 2.3 NEN 7510 walk

- §5.10 Cryptography — TLS forced (verify `force_https = true` in fly.toml); at-rest depends on provider
- §9.4 Access control — single role per feature, least-privilege; verify Directus role permissions match new collection access
- §12.4 Logging — audit-log INSERTs exist (when A3 lands) or `TODO(I3)` placeholders exist (until A3 lands)
- §13.1 Network security — verify Fly internal Wireguard URL is used for backend (no public Directus URL in `DIRECTUS_URL` env)

### 2.4 Code audit

Walk against [`.claude/conventions.md`](../conventions.md) + `CLAUDE.md` "Key rules":

- TypeScript strict + `noUncheckedIndexedAccess` — `npm run typecheck` clean
- Filenames kebab-case — `Glob` the in-scope files, check for camelCase / PascalCase
- Tests co-located in `__tests__/` — grep test files outside `__tests__/`
- No telemetry deps — `npm ls` against the blocked list
- User-facing Dutch — spot-check copy strings against English markers
- Code/comments English — spot-check comments for Dutch leakage
- Result-style error returns — grep SDK wrappers for `{ ok: true } | { ok: false }`
- No PII in repo — re-grep `private/` is gitignored
- Architectural deps have ADRs — diff `package.json` against base; for each new dep, find an ADR or step rationale

### 2.5 Dependency hygiene

- `npm audit --audit-level=high` (also the Dockerfile gate — Step 10 of auth-hardening)
- `npm ls --depth=0` count vs. prior baseline
- New dev/prod deps since the last audit: each must have either an ADR or a step rationale per the standards-enforcement table

### 2.6 Test pyramid health

For the in-scope code:
- Domain layer / pure logic — should dominate test count
- Route handlers — Vitest unit + Playwright e2e + (optional) live-stack
- UI components — Vitest jsdom
- e2e count should be **less** than route-handler count (pyramid, not inverted)

Flag if the ratio inverts.

### 2.7 Deployment posture (if the feature is deployed)

- `curl -I <prod-url>` — all 5 security headers present
- `curl <prod-url>/api/health` — 200 OK
- Cookie attrs on a fresh login response — HttpOnly; Secure; SameSite=Strict; Max-Age >= 24h

---

## Phase 3: Synthesise + write the report

### 3.1 Template

Use the [2026-05-27 auth audit](../../docs/audits/2026-05-27-auth-security-and-code-audit.md) as the template. Section structure:

1. Header: scope, methodology, verdict
2. Executive summary: severity counts + Top N to fix
3. Section 1 — Security audit
   - 1.1 Standards mapped (OWASP Top 10 + ASVS + GDPR + NEN 7510 tables)
   - 1.2 Findings (synthesised, by severity)
   - 1.3 Deployment posture
4. Section 2 — Code audit
   - 2.1 Adherence to project conventions
   - 2.2 Architecture observations
   - 2.3 Test pyramid
   - 2.4 Dependency hygiene
5. Section 3 — Remediation roadmap (Priority 1/2/3 + Won't do)
6. Appendix A — Methodology

### 3.2 Severity calibration

Severity is a human judgement. The skill SUGGESTS severity based on patterns:

- **Critical**: token leak in network response, SQL injection, broken auth on production data
- **High**: bypass of an auth/rate-limit gate; client-controlled secret; PII in logs; missing origin check on a state-changing endpoint
- **Medium**: missing security header; CSRF token plumbing gap; rate-limit bucket too generous
- **Low**: cosmetic; token-format validation missing; cookie URL-encoding pedantry
- **Informational**: architectural concern, no current bug

The skill writes severity *suggestions*; the human reviewer can revise.

### 3.3 The "Won't do" section

For each Low/Informational finding, the skill writes a *suggested* rationale for deferring. Final call: human reviewer.

### 3.4 Reflect findings to source

After writing the audit, optionally append `[Flagged 2026-XX-XX — audit Y]` markers near the offending code (as comments) so the next `/audit-feature` run can detect "still open."

---

## Phase 4: Hand off to the human

Output to the user:

- Path to the audit doc
- Severity counts (Critical / High / Medium / Low / Informational)
- Top 3 to fix first (the skill's best guess; human verifies)
- A one-sentence summary: "n findings across m files; v out of v gates green; recommend Priority 1 sweep before [next milestone]"

Then **stop**. Implementation of fixes is via `/plan-feature` (if a remediation feature is warranted) + `/build-step` (for each fix). The audit skill does not write code.

---

## What this skill explicitly does NOT do

- **Does not fix findings** — outputs a doc only. Findings flow through `/plan-feature` + `/build-step` like any other work.
- **Does not run during implementation** — that's `/build-step`'s job. This skill assumes the code is settled.
- **Does not replace human security review for high-stakes deploys** — e.g. before exposing the app to other users. Use this skill as one layer among several.
- **Does not assume the feature is "done"** — only that it's at a coherent checkpoint worth auditing.
