# ADR 0002: Switch to PWA frontend with Directus backend

- **Status**: Accepted
- **Date**: 2026-05-26
- **Supersedes**: [ADR 0001](0001-framework-expo.md)
- **Deciders**: Willem Masman (author), Claude (AI collaborator)

## Context

[ADR 0001](0001-framework-expo.md) locked Expo (React Native) for v1 with the reasoning that the author's React/TypeScript fluency, Vitest test loop, and Expo's cloud-build path (no Mac required) outweighed native Swift's HealthKit advantages — and that HealthKit was anyway a v2 concern.

That reasoning held against native Swift. It did not survive a fresh look at what Apple's platform actually costs to ship on, and what trades become attractive when those costs are visible.

Three things prompted the reconsideration:

1. **Apple Developer Program cost surfaced concretely.** $99/year recurring, plus 7-day re-sideload friction on the free path, plus App Store review for any external sharing. None of this is hard; all of it is friction this app's cardinal principle does not need.

2. **PWA storage durability was honestly assessed.** Safari aggressively evicts IndexedDB. A pure-local PWA would risk losing the very dataset that motivated the project. This made local-only PWA unviable on its own.

3. **The author already runs Directus 11.17.2 on Fly.io for TVO.** All the infrastructure costs that normally make "cloud backend" expensive (auth, API design, admin UI, schema management, file uploads, monitoring patterns) are already paid for elsewhere in the author's stack.

Once Directus came into the picture, the math flipped. A cloud-backed PWA stops fighting Safari's storage limits AND drops every Apple-platform cost.

## Options reconsidered

### Expo + native SQLite (ADR 0001's choice)

- ✅ Native UX polish, HealthKit-ready, robust offline storage
- ❌ $99/year Apple Developer Program when daily use starts
- ❌ App Store review on every update
- ❌ Slower v1 ship (2-3 months vs. 1-2 months for PWA)
- ❌ Cloud sync remains a v2 problem the author would have to design and build later

### Local-first PWA (IndexedDB / sql.js)

- ✅ Zero Apple friction, instant updates, cross-platform free
- ❌ Safari storage eviction is a real risk for daily-log data with no cloud backup
- ❌ Forces cloud sync into v1 anyway to address the risk
- ❌ Author would have to design + build that sync layer from scratch

### PWA with Directus backend — **chosen**

- ✅ Zero Apple friction (no Developer Program, no review, instant updates)
- ✅ Cloud is the source of truth from day 1 — Safari eviction risk does not apply to data
- ✅ Author's existing Fly.io + Directus + Postgres pattern means deployment is rote, not new work
- ✅ Schema lives in Directus admin UI — no migration code in the app
- ✅ Multi-device falls out for free
- ✅ Analysis pipeline becomes trivial — plain Postgres + DuckDB/pandas/R/Excel
- ✅ Future native iOS app (if v2 HealthKit ambitions activate) would query the same Directus, not require any data migration
- ⚠️ Online-first — daily entry requires network connectivity. See "Offline scope change" below.
- ⚠️ Personal health data lives on a server, not on-device — see "Privacy framing" below.

## Decision

**Build v1 as a Next.js 15 PWA with a Directus backend on Fly.io.** Online-first; offline support deferred or revisited later.

If v2 ambitions activate (HealthKit, Garmin, deep mobile integrations), build a native iOS app that queries the same Directus backend. The data model survives that pivot without migration because the cloud is the source of truth across both clients.

## Commitments (replacing ADR 0001's Expo commitments)

| Layer | Commitment |
|---|---|
| Frontend framework | **Next.js 15** (App Router, TypeScript strict) |
| Hosting (frontend) | **Fly.io** (matches existing TVO infrastructure pattern) |
| Backend | **Directus** (new instance, separate from TVO) on **Fly.io** |
| Database | **PostgreSQL** (managed by Directus) on **Fly.io** |
| Auth | **Directus auth** (token-based, single user for v1) |
| API access | **Directus SDK** (`@directus/sdk`) with **Zod** validation at the boundary |
| Validation | **Zod** at API boundaries; pure TS in `src/lib/domain/` |
| Tests | **Vitest** for domain + API-client tests; **Playwright** or **@testing-library/react** for UI (decided later) |
| ID strategy | **Directus-generated UUIDs** (server-side) for most entities; `date` remains natural key for `DayEntry` |

## Offline scope change

The brief originally stated:

> Werkt offline — invoer zonder netwerk moet kunnen, kalender-sync gebeurt zodra er verbinding is

This requirement is **deliberately relaxed for v1.** Daily entry requires network connectivity; if offline, the UI shows a clear "no network, retry when reconnected" state.

Reason for the relaxation: the brief's offline framing was tied to a local-first architectural assumption that no longer holds. Online-first with Directus removes more friction overall than it introduces, given the author logs primarily in bed at home (high-connectivity contexts).

When to revisit: if real usage shows >5% of intended logging moments are offline, add a local cache + write queue layer. This is a feature, not an architectural rewrite — the data model and API surface stay the same.

## Privacy framing

Personal health data now lives on a Fly.io-hosted Postgres in an EU region, accessed via TLS, behind Directus auth, on infrastructure the author controls. This is materially the same privacy posture as the existing TVO platform.

Compared to local-only on a phone backed up to iCloud, self-hosted Directus is:

- **More controlled** — author is the only admin, owns the keys, can audit everything
- **More portable** — Postgres dump is the user's data, exportable anywhere
- **More exposed** — a server has more attack surface than a locked phone
- **Less private than no-cloud-anywhere** — the data does leave the device

The author's stated privacy stance ("local-first, no telemetry, no ads") survives in spirit: no third-party telemetry, no analytics, no ads, no data sold or shared. "Local-first" is the part that genuinely changes; it was a tech-implementation framing, not an inviolable user promise.

## AI collaborator nuance (same as ADR 0001)

Claude was the AI collaborator for both ADR 0001 and this supersession. The recommendation in ADR 0001 (Expo) was sound given the inputs at that time; this ADR reflects new inputs (Apple Developer Program cost, Safari eviction risk, Directus availability) and reaches a different answer.

Lesson worth preserving: framework decisions deserve re-litigation when their input assumptions change, even after they're "locked." ADR 0001 was right *and* this supersession is right; they aren't in conflict, they reflect different cost models.

## Consequences

### Positive
- v1 ships in 1-2 months (vs. 2-3 for Expo)
- Zero Apple platform costs through v1 and v1.5
- Cloud sync, multi-device, schema admin UI, file uploads all free via Directus
- Author's analysis pipeline can hit Postgres directly with familiar tools
- Open source contributors don't need Mac/Xcode/Apple Developer Program to contribute
- Updates ship instantly, not through App Store review

### Negative
- Online-first means daily entry requires network
- v2 HealthKit / Garmin ambitions, if pursued, require a separate native iOS app (data model ports cleanly, UI rewrites)
- Self-hosted infrastructure means uptime is the author's responsibility (Fly.io makes this mostly painless, but it's still not zero)
- Personal health data lives on a server — different security model than on-device-only

### Migration cost if revisited
- Reverting to Expo + local-first: ~4-6 weeks given the Next.js + Directus learning would already be sunk
- Adding native iOS (v2): ~6-8 weeks; data model is already cloud-backed, so only the UI rewrites
- Adding offline cache + write queue to PWA: ~1-2 weeks as a feature, no architectural change

## When to revisit

Revisit this ADR if any of these become true:

- Network availability becomes a real daily-entry blocker (>5% of logging moments offline)
- HealthKit / Garmin integration shifts from v2 to v1
- Privacy stance hardens: "data must never leave the device"
- Directus or Fly.io become unviable for personal infrastructure
- An external user joins and their threat model demands on-device-only

## Cascade — what this supersession changes elsewhere

Updated in the same session as this ADR:

- `docs/decisions/0001-framework-expo.md` → status changed to **Superseded**
- `README.md` → tech stack section rewritten
- `docs/REQUIREMENTS.md` → framework section, offline requirement, sync requirement
- `docs/architecture/data-model.md` → Platform commitments table rewritten; bucket-A decisions annotated where Directus changes the answer
- `CLAUDE.md` → Expo references replaced with Next.js + Directus framing
- `.claude/conventions.md` → folder layout updated for Next.js App Router
- `.claude/testing.md` → mobile UI test layer references (Maestro, `@testing-library/react-native`) replaced with web UI test layer (Playwright + `@testing-library/react`)

The TDD doctrine, the Vitest setup, the `_scaffold/` proof, the slash-command structure, and the feature-template all carry over unchanged.

## References

- [ADR 0001](0001-framework-expo.md) (superseded by this document)
- [docs/REQUIREMENTS.md](../REQUIREMENTS.md)
- [docs/app_brief_gevoelscore.md](../app_brief_gevoelscore.md)
- [docs/technisch_document.md](../technisch_document.md)
- [docs/architecture/data-model.md](../architecture/data-model.md)
