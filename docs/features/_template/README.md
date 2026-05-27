# Feature Name

**Feature:** One-line description
**Version:** v1 | v1.5 | v2
**Status:** Planning | In Progress | Complete
**Parent doc:** Link to the relevant section of `docs/REQUIREMENTS.md`, `docs/app_brief_gevoelscore.md`, or `docs/technisch_document.md`

> Copy this folder to `docs/features/{feature-name}/` and replace placeholders. Created by `/plan-feature`.

---

## Overview

- **What:** What this feature does, in one sentence.
- **Why:** What problem it solves, with a pointer to where that problem is documented (brief section, requirement, conversation).
- **Impact:** What changes for the user once this is shipped.

---

## User need

The behavior the user is trying to accomplish, in their words. One paragraph max. Pulled from the brief, requirements, or a direct conversation.

---

## Acceptance criteria

Bullet checklist of Given/When/Then behaviors. Each line becomes one `it` block during implementation. If a criterion is vague ("works well", "is fast enough"), refine it until it's testable.

- [ ] AC1: Given <precondition>, when <action>, then <expected result>
- [ ] AC2: Given ..., when ..., then ...
- [ ] AC3: ...

---

## Technical constraints

Hard constraints from cardinal principles, privacy / security rules, and v1.5/v2 readiness that apply to this feature specifically. These shape both the implementation and the test plan.

- **Online**: [feature requires network; graceful "no network, retry" state per ADR 0002 — or specify if this feature uniquely needs offline support]
- **Storage**: [any new Directus collection or field; nullable for v1.5/v2 passive-data sources; access only via `src/lib/api/`]
- **Validation**: [Zod schemas in `src/lib/validation/` for any new boundary input — CSV imports, Directus responses, OAuth payloads]
- **Permissions**: [OAuth scopes (Google Calendar v1.5+), browser geolocation (v2), browser notifications (v2) — narrowest scope; default deny]
- **Performance**: [any timing budget — e.g. "daily-entry flow stays ≤ 10s on a 3G connection over Safari iOS"]
- **Dependencies**: [any new dep audited per `.claude/conventions.md` — license, telemetry, maintainer]

---

## Test plan

For each layer touched, name the test file and the cases that will be written. This is the contract between planning and [`/build-step`](../../../.claude/commands/build-step.md). Doctrine: [`.claude/testing.md`](../../../.claude/testing.md).

| File | Cases (one per `it`, mapped to AC) |
|------|------------------------------------|
| `src/lib/domain/__tests__/{module}.test.ts` | AC1: ...; AC2: ... |
| `src/lib/api/__tests__/{topic}.test.ts` | AC3: ... |
| `src/lib/validation/__tests__/{schema}.test.ts` | AC4: ... |

---

## Cardinal-principle impact

Walk each of the 6 cardinal principles. State the impact and how the design stays inside the principle. Be specific — vague statements like "respects the one-tap rule" don't count.

| Principle | Impact | How we stay inside |
|-----------|--------|--------------------|
| One-tap entry | e.g. "adds a chip-row below score" | "score still saves on first tap; chip-row is below and optional" |
| Sub-10-second flow | e.g. "adds ~1s if tags are used" | "tags only render if user has tagged before; defaults to collapsed for new users" |
| Brainfog-friendly | | |
| No notifications / ads / analytics | | |
| User-owned data | | (new data stays in author's Directus; covered by CSV / JSON export and full-delete) |
| Export / delete still works | | |

---

## Alternatives considered

For each major decision:

### Decision 1: [topic]

- **Chose**: [option] — why
- **Considered and rejected**: [option] — why
- **Revisit when**: [trigger signals]
- **Migration path**: [how we'd switch later]

---

## Future considerations

Things deliberately deferred. For each:

- **What it is**
- **When to add it** (trigger signals)
- **Proposed approach** when the time comes

---

## Privacy & permissions

User-control framing: what's collected, where it goes, how the user takes it back.

- **OAuth scopes / browser permissions requested**: [Google Calendar `calendar.readonly` v1.5+ / geolocation v2 / notifications v2 — be specific, no "all"]
- **Where the data lives**: [author's self-hosted Directus on Fly.io; column-level encryption stance if applicable]
- **Data that leaves the author's infrastructure**: [none by default; if any third-party call, justify and add an opt-in toggle]
- **Opt-in surface**: [where in the UI the user grants / revokes a permission or integration]
- **Export coverage**: [confirm new fields are in CSV and JSON exporters; full Postgres dump via Directus admin remains available]
- **Delete coverage**: [confirm full-wipe removes all new data from Directus + clears any client-side cache / cookies]

---

## Security

Threat framing: what can be exfiltrated, corrupted, or executed by something/someone that shouldn't. Reference: OWASP ASVS for the web surface, plus the OWASP Top 10 (A01 Broken Access, A03 Injection, A05 Misconfig, A07 Auth, A08 Data Integrity, A09 Logging).

- **Access control (A01, A07)**: [Directus auth required on every collection touch; session via `httpOnly`+`Secure`+`SameSite=Strict` cookie; CSRF stance for state-changing requests; CORS origin allowlist]
- **In transit**: [HTTPS-only for the Directus instance + any external API (Google Calendar v1.5, weather v2); TLS validation default; no mixed content]
- **At rest**: [Fly.io Postgres-at-rest encryption default; any sensitive field column-level encrypted (if applicable); Directus service tokens via Fly secrets, never committed]
- **Injection / untrusted input (A03)**: [Zod-validated at the API client boundary; CSV-export formula-injection escaping; import validation rules — out-of-range scores, date bounds, column count]
- **Web surface**: [no `dangerouslySetInnerHTML` without `@security` + DOMPurify; no user-controlled `href` / `src` / `style` without validation; no secrets in client bundle; CSP allowlist documented]
- **Permissions (least privilege)**: [OAuth scope is narrowest (`calendar.readonly`); browser permissions declined by default]
- **PWA-specific**: [service worker cache strategy for sensitive responses; `manifest.webmanifest` carries no per-user state]
- **Build hygiene & logging (A09)**: [no source maps in production; no `console.log` of PII; dev-only routes / screens gated by `process.env.NODE_ENV !== 'production'`; error responses do not leak stack traces or internal paths]
- **Supply chain**: [new deps audited — license, last-published, maintainer, transitive telemetry; `npm audit` clean before merging]

---

## v1.5 / v2 readiness

- **Directus schema impact**: [unchanged / added field `X` to collection `Y` (nullable) / new collection — confirm migration is additive only]
- **`DayEntry` impact**: [unchanged / added field `X` (nullable) / N/A — confirm nullable fields for `garmin`, `health`, `weather`, `calendar_events`, `project_entries`, `derived` still exist]
- **Other schema impact**: [`projects` / `tags` / `calendar_events` / new collection — describe]
- **Integration shape**: [if this touches a data source: confirm it follows the "fetch + aggregate + store per day" module interface in `src/lib/integrations/`]
- **Deferred assumptions**: [what this feature deliberately doesn't decide yet, and where the decision will surface]

---

## Architecture

### File tree

```
src/
  ...new and modified files here
```

### Key types

```typescript
// Copy the most important type signatures this feature introduces
```

### Integration with existing code

- Imports from `src/lib/api/`: [Directus query / mutation wrappers used]
- Imports from `src/lib/validation/`: [Zod schemas applied at the boundary]
- Imports from `src/lib/integrations/`: [...]
- New hooks / app routes / components: [...]
- Existing callers that change: [...]

---

## Steps

### Step 1: [Name]
- One-line summary
- See: [`step-1-name.md`](step-1-name.md)

### Step 2: [Name]
- One-line summary
- See: `step-2-name.md`

---

## Key Files

### New files to create

| File | Contents |
|------|----------|
| `src/lib/...` | [purpose] |

### Files to modify

| File | Change |
|------|--------|
| `src/...` | [change] |

### Reference docs (patterns to extract from)

| Doc | What to extract |
|-----|-----------------|
| `docs/app_brief_gevoelscore.md#blok-N` | UX pattern |
| `docs/technisch_document.md#section` | Data model / integration shape |

---

## Verification

### Automated

1. Tests: `npm test -- <pattern>`
2. Types: `npm run typecheck`
3. Build: `npm run build`

### Manual

1. Browser walkthrough: open the app in Safari iOS (primary daily-driver context) + cross-check in Chrome / Firefox. Perform the daily-entry flow, stopwatch it.
2. Brainfog walkthrough: one-handed, low-light, arm's length on a phone. Any tap that needs a second attempt is a fail.
3. Network-loss check: DevTools Network → Offline (or disable Wi-Fi). Verify the "no network, retry" state per [ADR 0002](../../../docs/decisions/0002-pwa-with-directus-backend.md) — daily entry is allowed to fail; the UX of that failure is not.
4. Export check: trigger CSV / JSON export after using the feature, confirm new fields are present.
5. Delete check: trigger full wipe via Directus admin or the app's delete-my-account flow, confirm no orphan rows.

### Testing strategy

[Any new pattern this feature introduces — snapshot tests, fixture format, walkthrough script — describe so the next feature can reuse it.]
