# GDPR Article 9 — special-category data declaration

**Status:** active 2026-05-28. Single-user app. Reviewed on every feature that touches `day_entries`, `day_entries_tags`, `projects`, `project_entries`, `notes`, `health_daily`, `garmin_daily`, or `weather_daily`.

**Cross-references:** [REQUIREMENTS.md](../REQUIREMENTS.md) (cardinal principles), [docs/architecture/current-state.md](../architecture/current-state.md) (deployed surface), [.claude/security-checklist.md](../../.claude/security-checklist.md) (OWASP ASVS), [docs/audits/2026-05-28-daily-entry-audit.md](../audits/2026-05-28-daily-entry-audit.md) (the audit finding that prompted this doc).

---

## What this doc is

GDPR Article 9 forbids processing "special categories of personal data" unless one of ten narrow exceptions applies. Health data is one such category. This app persists self-rated wellbeing scores (1–10), a free-text daily note that frequently contains symptoms or medication names (the soak-test row already contained `brainfog` and `naproxen`), and tag selections from a `fysiek` (physical-symptoms) cluster and an `interventie` (medical-interventions) cluster. The combination unambiguously qualifies as Article 9 health data.

This document is the written declaration of the lawful basis, retention policy, technical safeguards, and data-subject-rights mechanism that the app's processing relies on. It exists so the same answer is given every time the question is asked — by the operator, by a future contributor, by a regulator if v2 ever opens the app to a second user.

---

## 1. Data classification

| Field | Where stored | Category | Notes |
|---|---|---|---|
| `day_entries.score` (1–10) | Self-hosted Postgres on Fly.io (Amsterdam) via Directus, per [ADR 0007](../decisions/0007-self-hosted-postgres-on-fly.md); Neon Postgres (Frankfurt) until 2026-07-14 | Health — subjective wellbeing | Quantitative self-rating; cannot be derived without consent. |
| `day_entries.note` (free text) | Same | Health — symptoms, medications, free narrative | Highest sensitivity in the dataset. May contain prescription names, diagnoses, mood-state words. |
| `day_entries_tags` (M2M) | Same | Health — categorised symptoms / interventions / activities | Selected from a curated 83-tag set across 8 categories including `fysiek`, `mentaal`, `interventie`. |
| `day_entries.created_at` / `updated_at` | Same | Behavioural — logging patterns | Could reveal periods of illness via gaps. Treated as part of the health record. |
| `projects` + `project_entries` (v1.5) | Same | Health — intervention adherence | Records of medications/treatments started + their per-day status. |
| `garmin_daily`, `health_daily`, `weather_daily` (v2 placeholders) | Schema present, empty | Health — biometric / passive observational | Future v2 native-iOS scope. When populated they remain under this declaration. |

The session cookie (`gs_session`) and rate-limit bucket key (hashed IP) are operational metadata, not Article 9 data, but listed here for completeness.

---

## 2. Lawful basis

**Primary basis: GDPR Article 9(2)(a) — explicit consent.**

The sole data subject (the author) gives explicit consent to processing by virtue of:
- Choosing to install and operate the app
- Authenticating with a personal account they created
- Manually entering each row (no passive collection)
- Operating the infrastructure (Fly.io account; Neon account until 2026-07-14, since decommissioned per [ADR 0007](../decisions/0007-self-hosted-postgres-on-fly.md)) under their own credentials

Consent is documented by the existence of this declaration, the [REQUIREMENTS.md](../REQUIREMENTS.md) statement that data lives on infrastructure the author controls, and the architectural decision in [ADR 0002](../decisions/0002-pwa-with-directus-backend.md) that no third-party services touch the data.

If this app is ever extended to a second user, consent must be re-collected per user via an explicit opt-in screen at first login. That screen does not yet exist (it's not needed for the single-user case).

**Secondary basis (sanity check): Article 9(2)(h) — preventive or occupational medicine for personal health management** would also apply, but explicit consent is the cleaner and stronger basis for a self-tracking tool.

---

## 3. Data minimisation

The schema accepts exactly the fields the app uses; nothing speculative.

- No browser fingerprinting (no analytics, no Sentry, no PostHog — ESLint `no-restricted-imports` enforces this).
- No IP address persisted. Rate-limit buckets hash IPs in-memory; buckets reset on machine restart.
- No third-party CDNs serve content involving user data (Inter font is the only externally-sourced asset and it's served via `next/font` — fetched at build, not at request time).
- No telemetry. No crash reporting. No error aggregation service.
- Session cookies are scoped to the frontend origin, `HttpOnly` + `Secure` + `SameSite=Strict`.
- Server-side logs contain no user-input strings (verified by `grep -rnE "console\.(log|error|warn)" src/app/api/ src/lib/api/`).

---

## 4. Storage limitation (retention)

**Active retention: indefinite while the operator chooses to keep it.**

The app exists to replace a Google Sheet that contained 1,363 consecutive days of self-tracking. The value of the dataset comes from its longitudinal completeness; retention has no fixed end. The operator retains the right to delete the entire dataset at any time via the (forthcoming) export-and-delete mechanism — see §6.

**Backups:**
- Neon takes automatic daily snapshots of the database. Retention follows Neon's free-tier policy (current: 7 days point-in-time recovery on free tier).
- Fly volumes (`gevoelscore_uploads`) are encrypted and snapshotted automatically.
- No third-party backup destination exists.

**No automatic deletion** is performed. The schema has no soft-delete or TTL columns; rows persist until explicitly removed.

If a user (in a future multi-user scenario) requests erasure, the deletion must propagate through:
1. `day_entries` and cascaded `day_entries_tags` (M2M with CASCADE on both FKs)
2. `project_entries` and `project_entries_tags`
3. `directus_users` row
4. Active sessions in the in-memory session store
5. Any Neon snapshots — only via Neon support, since point-in-time recovery preserves the row for the retention window.

The Neon retention window means full erasure within the app is immediate; full erasure across backups takes up to 7 days. This is documented because GDPR Art 17 erasure includes backups.

---

## 5. Technical and organisational measures

| Measure | Implementation | Verified by |
|---|---|---|
| **Encryption in transit (frontend ↔ backend)** | TLS 1.3 forced by Fly edge; HSTS 1 year + `includeSubDomains` | `curl -I https://gevoelscore-frontend.fly.dev/` |
| **Encryption in transit (backend ↔ Neon)** | TLS via Neon's pooler endpoint, `sslmode=require` in `DB_CONNECTION_STRING` | Neon connection-string format; default for the pooler |
| **Encryption at rest** | Neon-managed AES encryption of the underlying storage | Neon's claim; not independently verified. Re-verify via Neon support if a third party ever asks. |
| **Backend not publicly addressable from frontend** | Server-side fetches use `http://gevoelscore-backend.internal:8055` (Fly Wireguard); public URL only used by browser-side admin login | `fly.toml` `DIRECTUS_URL` setting |
| **Authentication** | Email + password + mandatory TOTP 2FA via Directus; session in `httpOnly` + `Secure` + `SameSite=Strict` cookie; refresh-token rotation | Login feature steps 1–10 + auth-hardening audit findings closed |
| **Authorisation** | Single Directus role (`gevoelscore-frontend-api`) with CRUD on v1 collections only; no public read | [docs/architecture/current-state.md](../architecture/current-state.md) §"Permissions on `gevoelscore-frontend-policy`" |
| **Rate limiting** | Login 5/5min, 2FA 5/5min, day-entry writes 60/5min — all per-IP via Fly's `Fly-Client-IP` header | [src/lib/auth/stores.ts](../../src/lib/auth/stores.ts) |
| **Audit logging** | Placeholder `TODO(I3)` on the PUT route handler. The `directus_auth_events` collection is on the pre-launch A3 backlog. Single-user soak operates without this; multi-user release blocks on it landing. | [docs/audits/2026-05-28-daily-entry-audit.md](../audits/2026-05-28-daily-entry-audit.md) L3 |
| **Security headers** | CSP, HSTS, X-Content-Type-Options, Referrer-Policy, Permissions-Policy — all 5 present in prod | Same audit, §1.3 |
| **Input validation** | Every body field through a domain validator (`validateScore`, `normalizeNote`, `validateTagIds`, `validateDate`); generic 400 on failure (no field-by-field leak) | Same audit, §1.1 row A03 |
| **No PII in logs / repo** | `grep` confirms; `/private/` gitignored; UUIDs + emails redacted from `docs/` | Same audit, §2.1 |

---

## 6. Data-subject rights

The operator is also the sole data subject; in practice, "rights" reduce to "mechanisms the operator can use against their own data". They are listed in GDPR's order so the same mechanism is available if multi-user ever happens.

| Right (Art) | Mechanism today | Mechanism after pre-launch backlog |
|---|---|---|
| **Access (Art 15)** | Directus admin REST returns JSON of any row the role has access to. `scripts/verify-todays-entry.mjs` is a thin example. | Self-service export endpoint (CSV / JSON / Postgres dump). Tracked in `docs/architecture/current-state.md` §"What's NOT yet done". |
| **Rectification (Art 16)** | Edit-any-day flow exists: tap a day on the timeline → bottom sheet → edit + save. Past entries editable from Day 1. | Same. |
| **Erasure (Art 17)** | Manual delete via Directus admin UI. Cascading deletes through M2M junctions are configured. Neon snapshots persist up to 7 days. | Self-service "delete all my data" endpoint. Same backlog. |
| **Restriction (Art 18)** | Single-user — operator restricts by not editing. | Multi-user: a per-row "frozen" flag (not in schema today; would be a new field). |
| **Portability (Art 20)** | Directus admin REST returns JSON. | Same CSV/JSON export endpoint serves both Art 15 and Art 20. |
| **Object (Art 21)** | Not applicable (no profiling, no marketing). | Same. |
| **Automated decision-making (Art 22)** | No automated decisions. Score is human-entered. Tag-inference at import (`source='note_pattern'` on M2M junction) is one-time and explicit. | Same — any future ML inference must surface an opt-out. |

---

## 7. Sharing with third parties

**Strict policy: none.** Confirmed by the cardinal principle "no analytics / tracking / ads / third-party telemetry" (CONTRIBUTING.md). Verified by `npm ls --depth=0` against the ESLint-blocked list (Sentry, PostHog, Vercel Analytics, DataDog, Mixpanel, Amplitude, etc.).

The only third parties that touch infrastructure:
- **Fly.io** — application hosting. Standard DPA in their ToS. EU region (`ams`). No application data is sent to Fly beyond what's in the runtime processes (logs they retain are operational, not application-data dumps).
- **Neon** — managed Postgres. Standard DPA. EU region (`aws-eu-central-1`). Holds the actual data at rest.
- **Google Fonts CDN** — Inter font. Fetched at build time via `next/font`, not at request time. No browser-side request to Google during normal operation. (The build host sees the request once per deploy.)

No transfer outside the EU. No sub-processors beyond what Fly and Neon declare.

---

## 8. Breach response

If a breach occurs (credential leak, database compromise, untracked third-party access):

1. **Contain.** Rotate static tokens (see [docs/operations/runbooks/rotate-credentials.md](../operations/runbooks/rotate-credentials.md)). Take the frontend offline if necessary (`fly scale count 0 --app gevoelscore-frontend`).
2. **Assess.** Determine which rows were exposed. With single user this is trivially "all or nothing"; with multi-user it would require log analysis (depends on A3 audit-log landing).
3. **Notify** (Art 33) — the operator is also the data subject, so notification reduces to "make a note". For a multi-user release, notification within 72h becomes a real obligation. The notification template lives at [docs/operations/runbooks/breach-notification.md](../operations/runbooks/breach-notification.md) — **does not yet exist; create before multi-user launch**.

---

## 9. Review cadence

This declaration is reviewed:
- On every feature that adds a new field to an Art 9 collection (see "What this doc is" trigger list).
- After every security audit (next: 2026-08 quarterly).
- On any architectural change that affects storage location, encryption posture, or third-party touchpoints.
- Before any multi-user release. Required additions at that point: per-user consent screen, breach-notification runbook, Art 13 transparency notice as a `/privacy` page in the app.

**Last reviewed:** 2026-05-28 by the operator, against commit `58a3667`.
