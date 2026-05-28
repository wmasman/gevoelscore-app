# Daily-entry feature audit — 2026-05-28

**Scope:** the daily-entry feature folder ([docs/features/daily-entry/](../features/daily-entry/)) — Steps 0 through 6 including the 4b row redesign. Deployed to `gevoelscore-frontend.fly.dev` at commit `58a3667`; in real-usage soak.

**Methodology:** [.claude/commands/audit-feature.md](../../.claude/commands/audit-feature.md) phases 1–4. Template inherited from the [2026-05-27 auth audit](2026-05-27-auth-security-and-code-audit.md). Manual probes + grep + npm audit + live `curl` of prod. No automated SAST run.

**Verdict:** **Ship-cleared for single-user soak.** No Critical or High findings. 2 Mediums tied to the existing A3 compliance backlog (no new work needed beyond what's already tracked). Remaining items are Low / Informational polish — none block daily use.

---

## Executive summary

| Severity | Count | Items |
|---|---|---|
| Critical | 0 | — |
| High | 0 | — |
| Medium | 2 | GDPR Art 9 declaration missing for health-category data; CSP allows `'unsafe-inline'` for scripts |
| Low | 3 | Favicon 404 noise; SaveStatus inconsistency between header and inline child renders; audit-log placeholder only on writes |
| Informational | 3 | upsertDayEntry double-read; CSV export/delete still pending; range GET unrate-limited (deliberate) |

**Top three to address next** (in priority order):

1. **GDPR Article 9 declaration** ([medium](#m1-gdpr-art-9-declaration-missing-for-health-data)). The `day_entries` row + the M2M tag selection + the free-text `note` all qualify as health-related personal data under GDPR Art 9. Need a one-page `docs/compliance/gdpr-art9.md` stating lawful basis (Art 9(2)(a) — explicit consent for self-tracking), data minimisation posture, retention policy, and data-subject-rights (export, erasure). Already in the pre-launch backlog as Track A3; this audit elevates it to *the* next pre-launch gate.

2. **Audit-log INSERT collection** ([low](#l3-audit-log-todo-only-on-writes) + Medium *if* multi-user). Route handlers all carry `TODO(I3)` markers; the `directus_auth_events` collection itself doesn't exist yet. For single-user soak this is informational; for any release that exposes the app to a second person it becomes a NEN 7510 §12.4 blocker.

3. **Consolidate `<SaveStatus />` rendering** ([low](#l2-savestatus-rendered-in-both-header-and-child-components)). Step 4b lifted the wheel's status to the page header but left NoteField + TagCategoryList rendering their own ✓/⚠ inline. Result: a save can show two indicators at once (header from wheel's hook + child from its own). Cosmetic — not a correctness issue — but the design brief's "one source of save-feedback per screen" calls for a single header instance fed by all three child hooks via context.

---

## 1. Security audit

### 1.1 Standards coverage

#### OWASP Top 10 (2021) + OWASP ASVS

| Section | Daily-entry posture | Note |
|---|---|---|
| **A01 — Broken access control** | ✅ Every `/api/day-entries/*` route calls `getValidatedSession` and `validateOrigin`. The `[date]` route also rate-limits writes. | Confirmed via grep of the three route handlers — all 5 mandatory gates present on the write route (origin → rate-limit → cookie parse → session-validate → body-validate). |
| **A02 — Cryptographic failures** | ✅ TLS forced by Fly (`force_https = true`). HSTS 1 year + includeSubDomains. Cookies HttpOnly + Secure + SameSite=Strict (inherited from the login feature). | DB encryption at rest is Neon-managed but undeclared in our docs — see [M1](#m1-gdpr-art-9-declaration-missing-for-health-data). |
| **A03 — Injection** | ✅ Every body field passes a domain validator (`validateScore`, `normalizeNote`, `validateTagIds`, `validateDate`). M2M tag IDs go through Directus SDK (parameterised). No `dangerouslySetInnerHTML` anywhere in src. | `grep -rn dangerouslySetInnerHTML src/` returns nothing. |
| **A04 — Insecure design** | ✅ PUT is idempotent (upsert by date). Optimistic update + server reconciliation. Race-safe: partial patches are merged server-side. | The Step 4b → Step 5 reuse architecture means each component owns its own debounce but the *transport* layer is shared. |
| **A05 — Security misconfiguration** | ✅ 5 security headers present in prod (CSP, HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy). `poweredByHeader: false`. Dev-only `'unsafe-eval'` flag in CSP. | CSP `'unsafe-inline'` for scripts — see [M2](#m2-csp-allows-unsafe-inline-for-scripts). |
| **A06 — Vulnerable components** | ⚠️ 2 moderate `postcss` advisories bundled inside Next.js (`<8.5.10`, XSS via unescaped `</style>`). Not actionable — upstream Next has not yet bumped. | Same finding as the 2026-05-27 audit; accepted as a known live issue until Next ships the patched postcss. Not exposed via daily-entry (we don't render user-supplied CSS). |
| **A07 — ID/auth failures** | ✅ Inherits the login feature's audit-closed posture (refresh-token rotation, TFA-secret-bound-to-session, rate-limited login + verify + 2FA endpoints). | Daily-entry adds no new auth surface. |
| **A08 — Software/data integrity** | ✅ `package-lock.json` committed. No remote script execution. Origin check on every state-changing route. | — |
| **A09 — Logging failures** | ⚠️ No daily-entry events logged. `TODO(I3)` placeholder in the write route only. | See [L3](#l3-audit-log-todo-only-on-writes). |
| **A10 — SSRF** | ✅ Server-side fetches use a hardcoded `DIRECTUS_URL` env var (fly.toml internal Wireguard URL in prod). No user-controlled URLs. | Confirmed via `grep -rn "fetch(" src/lib/`. |

#### GDPR Article 9 — special-category data

| Question | Posture |
|---|---|
| Does this feature persist health-related personal data? | **Yes**: subjective `score` (1–10 wellbeing rating), free-text `note` (may contain symptoms / medication names — the live row contained "brainfog" and "naproxen"), tag selections in `mentaal` / `fysiek` / `interventie` categories. All three rows count under Art 9. |
| Lawful basis declared? | **No** — see [M1](#m1-gdpr-art-9-declaration-missing-for-health-data). |
| Data minimisation? | ✅ The schema accepts only the fields the app uses. No browser fingerprinting, no IP logging beyond rate-limit bucket keys (hashed not stored). |
| Storage limitation (retention)? | **Undeclared** — no retention policy in feature README or compliance doc. The 1,363-day historical sheet implies "keep forever" but that needs to be stated. |
| Data subject rights — access (export)? | Schema is exportable via Directus admin; no app-level CSV export endpoint yet (pre-launch backlog). |
| Data subject rights — erasure? | Schema supports delete; no app-level delete-all endpoint yet (pre-launch backlog). |
| Cross-border transfer? | Data lives in Neon `aws-eu-central-1` (Frankfurt) — same legal region as user (NL); no transfer concerns. |

#### NEN 7510 — Dutch health-info governance

| §  | Posture |
|---|---|
| **§5.10 Cryptography** | TLS in transit ✓; at-rest depends on Neon's managed encryption (claimed, undeclared in our docs). |
| **§9.4 Access control** | Single Directus role (`gevoelscore-frontend-api`) with CRUD on day_entries + tags + junctions; no public access; admin role separate. |
| **§12.4 Logging** | Placeholder `TODO(I3)` on the PUT handler. No audit-event collection live. Inherits the auth feature's incomplete posture. |
| **§13.1 Network security** | Backend reached over Fly's internal Wireguard URL (`http://gevoelscore-backend.internal:8055` in fly.toml), not the public URL. Frontend → backend traffic never crosses the public internet. |

### 1.2 Findings

#### M1. GDPR Art 9 declaration missing for health data

**Severity:** Medium (compliance gap, not a security bug). **Owner:** Track A3.

The `day_entries.note` field is free-text and the live row already contains health terms (the soak-test row included references to brainfog and naproxen). Combined with score + interventie tags, the dataset qualifies as Art 9 health data. The repo has no `docs/compliance/gdpr-art9.md` stating:

- Lawful basis (Art 9(2)(a) — explicit consent for self-tracking)
- Data minimisation posture
- Retention policy
- Storage location (Neon EU) and provider DPA reference
- Data-subject-rights mechanism

**Fix shape:** one-page doc under `docs/compliance/`, plus a "Privacy" link in the app's UI eventually (deferred until export/delete UI lands). Currently single-user so this is bureaucratic, but it's the same effort whether done now or pre-launch.

#### M2. CSP allows `'unsafe-inline'` for scripts

**Severity:** Medium. **Owner:** post-soak polish.

Current prod CSP:

```
script-src 'self' 'unsafe-inline'
```

Inline `<script>` tags can run arbitrary JS, weakening CSP's XSS protection. The reason `'unsafe-inline'` is present: Next.js's App Router injects inline runtime scripts (chunk preload, route data) and there's no nonce/hash mechanism wired up yet. Mitigation already in place: no user-supplied HTML is ever interpolated into the page (no `dangerouslySetInnerHTML`); `frame-ancestors 'none'` prevents clickjacking; `base-uri 'self'` blocks tag injection.

**Fix shape:** wire `nonce-{random}` per-request in middleware, drop `'unsafe-inline'`. Non-trivial (Next 15 nonce support is via middleware response headers + custom `<script>` rendering). Defer to post-soak unless the threat model changes (e.g. a second user, untrusted content).

#### L1. Favicon 404

**Severity:** Low (cosmetic console noise). **Owner:** polish.

No `public/favicon.ico`. Every page load logs a 404 to the browser console. Doesn't affect functionality; clouds the console when looking for real errors during soak.

**Fix:** drop a 32×32 ico at `public/favicon.ico`. Could match the warm-earth palette (clay disc on warm-white background) or stay neutral.

#### L2. SaveStatus rendered in both header and child components

**Severity:** Low (UX inconsistency, not a correctness bug). **Owner:** post-soak polish.

Step 4b lifted the wheel's `useDayEntryUpsert` hook up to `<TodayShell>` and rendered `<SaveStatus variant="glyph" />` in the page header. NoteField and TagCategoryList each still own their own hook + render their own `<SaveStatus />` inline (banner variant for errors; the `'saved'`/`'saving'` glyphs render inline next to each child).

Symptom: on a fast sequence of edits, the user can see the header glyph for the wheel save *and* a separate ✓ next to the note simultaneously. Per the brief, save feedback should be quiet and unified — "one source of save-feedback per screen". The Step 5 status note in step-5's doc flagged this exact item.

**Fix shape:** introduce a `SaveStatusContext` that broadcasts the latest status across all three child hooks; TodayShell consumes the context and renders the single header indicator. Drop the inline `<SaveStatus />` from NoteField + TagCategoryList. ~30–60 minutes of work.

#### L3. Audit-log `TODO(I3)` only on writes

**Severity:** Low (single-user soak); promoted to Medium if a second user is added. **Owner:** Track A3.

The PUT `/api/day-entries/[date]` route has the placeholder; GET `/api/day-entries` (range) and GET `/api/day-entries/today` don't. NEN 7510 §12.4 calls for read-event logging too — minimally "user X read range Y to Z at time T". For a single user the read log is uninformative, but A3 compliance work should add placeholders on both GET handlers when the collection lands.

**Fix:** add `// TODO(I3): audit-log entry` comments at the two GET handlers' return points, matching the PUT pattern.

#### I1. `upsertDayEntry` does two reads per write

**Severity:** Informational (performance, not security). **Owner:** if measured slow.

The SDK reads `day_entries` to find the existing row → does the create/update → reads `day_entries` again to return the canonical post-write shape. ~10 ms each on the Fly internal network, so ~20 ms overhead per write. The double-read exists because Directus PATCH/POST responses don't expand M2M relations by default; the alternative is to manually expand the response wire-shape.

**Defer until** write latency becomes a UX issue (which on the score-tap = cardinal screen would be visible). Not measurable at single-user scale.

#### I2. CSV export + delete-all endpoints absent

**Severity:** Informational (already tracked). **Owner:** separate feature.

The "user-owned data" cardinal principle requires both endpoints. Neither exists in the app yet (the parser ships, the UI doesn't). Directus admin REST covers manual export today. Tracked in [docs/architecture/current-state.md](../architecture/current-state.md) "What's NOT yet done" #6–7.

#### I3. Range GET intentionally unrate-limited

**Severity:** Informational (deliberate decision, recorded here for traceability). **Owner:** none — design choice.

Per the daily-entry README AC22: "GET routes are not rate-limited (read traffic is the happy path; rate limiting reads on a single-user app is theatrical)." Audit confirms this is consistent with the threat model. Re-evaluate if the app exposes reads to multiple users or to public endpoints (timeline export would change this).

### 1.3 Deployment posture (prod)

```
$ curl -I https://gevoelscore-frontend.fly.dev/
< content-security-policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';
                            img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self';
                            form-action 'self'
< strict-transport-security: max-age=31536000; includeSubDomains
< x-content-type-options: nosniff
< referrer-policy: strict-origin-when-cross-origin
< permissions-policy: camera=(), microphone=(), geolocation=()
$ curl https://gevoelscore-frontend.fly.dev/api/health
{"status":"ok"}
$ curl https://gevoelscore-frontend.fly.dev/api/day-entries/today
{"error":"unauthenticated"} (401)
```

All five mandatory headers present. Health check OK. Auth gate enforces 401 on the unauthenticated read. `x-powered-by` is absent (the `poweredByHeader: false` config worked).

---

## 2. Code audit

### 2.1 Adherence to project conventions

| Convention | Posture |
|---|---|
| TypeScript strict + `noUncheckedIndexedAccess` | ✅ `npm run typecheck` clean. |
| Filenames kebab-case | ✅ All daily-entry files. |
| Tests co-located in `__tests__/` | ✅ 13 test files all under `__tests__/`. |
| No telemetry deps | ✅ ESLint `no-restricted-imports` blocks Sentry/PostHog/Vercel Analytics. Confirmed via `npm ls --depth=0` grep. |
| User-facing Dutch via `src/copy.ts` | ✅ All components import from `@/copy`. No inline string literals in JSX (spot-checked all daily-entry components). |
| Code/comments English | ✅ Spot-checked all daily-entry components and SDK wrappers. |
| Result-style error returns | ✅ `readDayEntryByDate`, `readDayEntriesInRange`, `upsertDayEntry`, `readAllTags` all return `Result<T, E>`. |
| No PII in repo | ✅ `/private/` gitignored; real-history.csv stays out; redacted-from-docs.md kept private; no UUIDs/emails in `docs/`. |
| New deps require ADR or rationale | ✅ No new deps added by daily-entry. `clsx` + `tailwind-merge` added in Step 0 with rationale in step-0 file. |
| Em-dash forbidden in UI copy | ⚠️ Mostly clean. The post-Step-5 doc edits stripped em-dashes from `copy.ts`. Audit-doc itself uses em-dashes (per the no-emdash-in-UI memory the rule scopes to *user-facing* strings, not internal docs — confirmed). |
| No `dangerouslySetInnerHTML` | ✅ Zero occurrences. |
| ESLint suppressions are commented with rationale | ✅ 4 `jsx-a11y/no-autofocus` suppressions in login pages — each links to frontend-conventions.md. 5 `security/detect-non-literal-regexp` in tests (test fixtures iterating over const enums). 1 `react-hooks/exhaustive-deps` in `score-row.tsx` (intentional — `initialScore` only matters on mount). All clean. |

### 2.2 Architecture observations

- **Hook ownership split is deliberate but introduces L2.** TodayShell owns the wheel's hook (per Step 4b); NoteField and TagCategoryList each own their own. This was a Step 4b implementation note ("Step 5 can revisit"). Three independent debounce regimes are correct; three independent status feeds are the visible inconsistency. See L2.

- **`<DayEntryEditor />` reuse paid off.** The composite is used twice — Today screen + timeline bottom sheet — with identical save semantics. No code duplication between today-editing and past-day-editing flows.

- **Vanilla SVG chart choice held.** No chart-lib dep. ~150 LOC including hit-test, axes, gap-rendering. Trade-off (manual axis labelling, no tooltips beyond the per-point click) is accepted.

- **`scripts/verify-todays-entry.mjs` is now a soak-time tool.** Useful but not part of the test suite. Consider promoting to `npm run verify:live` or similar if the soak surfaces more "did it really save?" questions. (Not now — wait for need.)

### 2.3 Test pyramid

| Layer | Tests | Notes |
|---|---|---|
| Domain (pure logic) | ~232 (pre-existing) + 7 (streak) | Dominant. Healthy. |
| SDK wrappers (mocked Directus) | 13 (day-entries) + 2 (tags) | One test per public function path; M2M sync covered. |
| Hooks | 11 (`use-day-entry-upsert`) | Debounce + abort + cleanup + error revert. |
| Route handlers (Vitest mocked) | ~14 across the three day-entries routes | Auth, origin, rate-limit, body-validation, partial-update paths. |
| Components (jsdom) | 5+7+9+3+4+4+5 = ~37 | NoteField, save-status, score-row, today-shell, score-chart, timeline-view, tag-category-list, day-entry-editor. |
| Playwright API | 8 (existing baseline) | Auth + middleware. |
| Playwright chromium e2e | 9 daily-entry specs + auth/login carryover | Score row, today shell, note + tags, timeline + sheet, axe scans. |
| Playwright live-stack | 1 day-entries spec (existing) | Reads against real Directus baseline. |

**Total:** 500 vitest / 44 chromium e2e (45th fail is the parallel `/over` page work, out of scope). Pyramid is healthy — domain → SDK → route → component → e2e in decreasing order.

### 2.4 Dependency hygiene

```
$ npm audit --audit-level=high
2 moderate severity vulnerabilities  (both postcss-inside-Next, no actionable fix)
$ npm ls --depth=0 | wc -l
(see package.json; no new prod deps since Step 0)
```

No new prod deps for daily-entry. `@axe-core/playwright` was added in Step 0 (dev). Verified via diff against `cf07b56` (Step 0 commit).

---

## 3. Remediation roadmap

### Priority 1 — before exposing the app to anyone else

- **[M1]** Write `docs/compliance/gdpr-art9.md` declaring lawful basis, retention, data subject rights for health-category data. Tracked in Track A3.

That's it. Nothing else *blocks* a multi-user release that isn't already blocked by the existing A3 + CSV-export-UI backlog.

### Priority 2 — pre-launch polish

- **[L1]** Add `public/favicon.ico`.
- **[L2]** Consolidate `<SaveStatus />` rendering. Drop inline child renders; introduce shared status feed.
- **[L3]** Add `TODO(I3)` placeholders to the two GET handlers so A3 work covers reads too.
- **[M2]** Wire CSP nonces, drop `'unsafe-inline'`. Defer until threat model changes (e.g. second user).

### Priority 3 — when a measurement justifies it

- **[I1]** Collapse `upsertDayEntry` double-read into a single read+write. Only if write latency becomes a UX issue under real use.

### Won't do

- **[I2]** CSV export / delete-all — separate feature, tracked elsewhere.
- **[I3]** Rate-limit GET routes — deliberate design.
- Replace vanilla SVG chart with a library — vanilla SVG handles 90 points fine; the bundle saving (no dep) outweighs the lost ergonomics for a single-user app.
- Add Storybook / visual regression — single-user app, walkthrough-on-phone is the visual test.

---

## Appendix A — Methodology

Probes used:

```
git log --diff-filter=AM --name-only cf07b56^..HEAD  # files in scope since Step 0
grep -nE "getValidatedSession|validateOrigin|rateLimiter\.check"  # auth gates
grep -nE "dangerouslySetInnerHTML"  # XSS surface
grep -rnE "console\.(log|error|warn|info)" src/app/api/ src/lib/api/ src/hooks/  # PII logs
grep -nE "eslint-disable"  # suppression audit
curl -I https://gevoelscore-frontend.fly.dev/  # prod headers
curl https://gevoelscore-frontend.fly.dev/api/health  # health probe
curl https://gevoelscore-frontend.fly.dev/api/day-entries/today  # auth-gate probe
npm audit --audit-level=high  # CVE check
npm run verify  # lint + typecheck + 500/500 vitest
npx playwright test --project=chromium  # 44/45 e2e
node scripts/verify-todays-entry.mjs  # live persistence check (run by user)
```

Time spent: ~30 min synthesised audit; ~10 min remediation roadmap. No automated SAST tooling run (none in repo's tool stack).

## Cross-references

- [.claude/security-checklist.md](../../.claude/security-checklist.md) — OWASP ASVS-aligned checklist used as the spec for each row in §1.1.
- [.claude/conventions.md](../../.claude/conventions.md) — project conventions checked in §2.1.
- [2026-05-27 auth audit](2026-05-27-auth-security-and-code-audit.md) — the template + the audit that closed the auth findings this feature inherits clean state from.
- [docs/features/daily-entry/README.md](../features/daily-entry/README.md) — feature plan that declared what each step touched.
- [docs/architecture/current-state.md](../architecture/current-state.md) — the post-deploy snapshot the audit confirmed.
