---
description: Plan a new feature from requirement or idea to implementation-ready steps. Use when starting a v1 feature, breaking down a v1.5/v2 capability, or turning a brief paragraph into something a developer can pick up cold.
---

# Plan Feature

Structured workflow for turning a requirement, idea, or section of the brief into an implementation-ready feature plan under `docs/features/{name}/` — with TDD-shaped steps, cardinal-principle gates, privacy gates, security gates, and v1.5/v2 readiness checks.

**This command never writes source code.** It produces planning docs only. Implementation happens via [`/build-step`](build-step.md), which walks each step through the strict RED → GREEN → REFACTOR loop.

**TDD is mandatory** — see [`.claude/testing.md`](../testing.md) for the doctrine. The step files this command produces must include acceptance criteria, technical constraints, and a test plan that names every test before any code is written. The only escape is pure-styling work (replaced by a visual baseline screenshot, not skipped).

## When to use

- Starting a v1 feature from [docs/REQUIREMENTS.md](../../docs/REQUIREMENTS.md)
- Breaking down a v1.5 or v2 capability from [docs/app_brief_gevoelscore.md](../../docs/app_brief_gevoelscore.md) or [docs/technisch_document.md](../../docs/technisch_document.md)
- Turning a new idea or constraint into a structured plan
- Preparing a feature folder in `docs/features/{feature-name}/`

## Inputs

The user provides one of:

- A reference to a v1 requirement (e.g. "the streak counter", "CSV import of the 1.363-day sheet")
- A reference to a brief section (e.g. "blok 3 projecten", "Google Agenda sync")
- A verbal description of a new feature or constraint
- An optional argument: `/plan-feature <name-or-topic>`

If the input is ambiguous, **ask before designing** — see Phase 1.3.

---

## Phase 1: Understand the requirement

### 1.1 Read the input and the relevant source docs

The source of truth lives in three docs. Read the parts that touch the feature:

- [docs/REQUIREMENTS.md](../../docs/REQUIREMENTS.md) — v1 must-haves, out-of-scope, technical requirements
- [docs/app_brief_gevoelscore.md](../../docs/app_brief_gevoelscore.md) — UX (input flow blokken 1–5), data model, version roadmap
- [docs/technisch_document.md](../../docs/technisch_document.md) — passive context data (HealthKit, Garmin, weather, calendar), privacy, licensing

Identify:

- The core problem this feature solves
- Which version it belongs to (v1 / v1.5 / v2)
- The cardinal principles most at risk
- Adjacent features (already-planned or built) it interacts with

### 1.2 Survey what exists

- If code exists, search `src/` for related modules, screens, and helpers — reuse before reinvent.
- If `docs/features/` has prior plans, scan their READMEs for patterns and naming conventions.
- If nothing exists yet, say so — and use the `docs/features/_template/` skeleton.

### 1.3 Ask clarifying questions

Resolve ambiguity **before** drawing architecture. Always ask if any of these are unclear:

- **Version**: Is this v1, v1.5, or v2? (Different gates apply — see Phase 5.)
- **Scope boundary**: What's in, what's explicitly out, what's "later"?
- **UX flow**: Does this touch the daily screen (Blok 1/2)? If yes, the one-tap and sub-10-second rules apply hard.
- **Data**: Does this introduce new `DayEntry` fields, new collections, or new integration sources?
- **Permissions**: Does this require HealthKit, OAuth, location, calendar, or notification permissions?
- **Security surface**: Does this introduce new at-rest data, new network calls, new untrusted input (imports, deep links, share-sheet), or new dependencies? (Triggers the security gate in Phase 5.3.)

---

## Phase 2: Architect's assessment

### 2.1 Capability audit

For each requirement in the feature, write:

| Requirement | Exists? | Location | Gap |
|-------------|---------|----------|-----|
| [requirement] | Yes / Partial / No | [file path] | [what's missing] |

### 2.2 Identify the critical gaps

What are the 1–3 things that block everything else in this feature? Those become Step 1 (and possibly Step 2).

### 2.3 Consider alternatives — and document the rejected ones

For each major decision, write:

- **What we chose** and why
- **What we considered and rejected**, with reasons
- **When to revisit** (trigger signals — e.g. "if HealthKit gives us workouts but not Body Battery, revisit Garmin direct integration")
- **Migration path** when the trigger fires

The brief mentions specific tradeoffs (Expo vs. Swift, Supabase vs. Firebase, OAuth scopes, Garmin Body Battery gap) — re-decide them in writing for the current feature even if the brief settled them in principle. The brief's reasoning is a starting point, not a closed decision.

---

## Phase 3: Feature breakdown

### 3.1 Each feature should be

- **Self-contained** — own schema entries, screens, components, tests, integration module
- **Independently shippable to the prototype** — adds value on its own
- **3–8 implementation steps** — bigger means split it
- **Clear dependencies** — knows what it needs and what depends on it

### 3.2 Distinguish features from small tasks

Not everything is a feature. Small tasks (no feature folder needed):

- Single-file utility additions
- Copy / wording changes
- Dependency upgrades
- One-off scripts in `scripts/`
- Anonymization / data-prep tasks

If it's a small task, say so — don't force a feature folder.

### 3.3 Map dependencies

Identify what blocks what, what can be built in parallel, and what has external dependencies (e.g., waiting on an answer about iOS minimum version, or on the brief author confirming a UX call).

### 3.4 Recommend build order

Based on: cardinal-principle risk (riskiest UX work first while patterns are still settling), foundation-first (data model and storage before screens), and what unblocks the most parallel work.

---

## Phase 4: Feature documentation

For each feature, create `docs/features/{feature-name}/` with a `README.md` and one file per step (`step-1-{slug}.md`, `step-2-...`).

Use [`docs/features/_template/`](../../docs/features/_template/) as the starting point — copy and edit.

### 4.1 README.md structure

```markdown
# Feature Name

**Feature:** One-line description
**Version:** v1 | v1.5 | v2
**Status:** Planning | In Progress | Complete
**Parent doc:** Link to REQUIREMENTS / brief / technisch_document section

---

## User need
The behavior the user is trying to accomplish, in their words. One paragraph max.

## Acceptance criteria
Bullet checklist of Given/When/Then behaviors. Each line becomes one `it` block in the tests. If a criterion is vague ("works well", "is fast enough"), refine it until it's testable.

- [ ] Given <precondition>, when <action>, then <expected result>
- [ ] Given ..., when ..., then ...

## Technical constraints
Hard constraints from the cardinal principles, privacy/security rules, and v1.5/v2 readiness that apply to this feature specifically.

- Offline: must work without network
- At rest: any new persistent data is in the encrypted SQLite DB
- Permissions: ...
- Performance: ...

## Test plan
For each layer touched, name the test file and the cases that will be written. This is the contract between planning and `/build-step`.

| File | Cases (one per `it`) |
|------|----------------------|
| `src/lib/{module}/__tests__/{module}.test.ts` | rejects > 6; rejects < 1; rejects 4.5 (halves not allowed) |
| `src/lib/db/__tests__/{topic}.test.ts` | round-trip insert + read; overwrites same-day entry |

## Cardinal-principle impact
Which of the 6 cardinal principles this feature touches, and how it stays inside them:
- One-tap entry — does this affect the daily screen? If yes, how do we preserve "one tap = done"?
- Sub-10-second flow — added screens / interactions and their time cost
- Brainfog-friendly — tap target size, screen depth, decisions required
- Local-first — where the data lives
- No telemetry — dependencies introduced
- Export / delete still works — new data covered by export and full-wipe

## Alternatives Considered
For each major decision: chose, rejected (with reasons), when to revisit, migration path.

## Future Considerations
Things deliberately deferred. For each: what it is, trigger signals, proposed approach.

## Privacy & permissions
- Which OS-level permissions are requested (HealthKit types, calendar scope, location, notifications)
- What data leaves the device, if any, and what the opt-in surface looks like
- What the export / delete path looks like for new data this feature introduces

## v1.5 / v2 readiness
- Schema additions: are nullable fields for future passive-data sources preserved?
- Integration shape: if this is or touches a data source, does it follow the standard "fetch + aggregate + store per day" interface?
- What assumptions does this feature deliberately defer to a later version?

## Architecture
- File tree of new / modified files
- Key types and contracts (TypeScript signatures)
- How existing modules integrate (imports, hooks, screens)

## Steps
- Numbered list with one-line summaries
- Each links to its step file

## Key Files
- New files to create (table)
- Files to modify (table)
- Reference docs to extract patterns from (table)

## Verification
- Automated (tests, type check, build)
- Manual (device walkthrough, brainfog walkthrough)
- Testing strategy (any new pattern introduced)
```

### 4.2 Step files (`step-N-{slug}.md`)

Every step is TDD-shaped. The only escape from RED-first is pure-styling work (color, spacing, font, animation timing with no state change), which is replaced — not skipped — by a visual baseline screenshot. See [`.claude/testing.md`](../testing.md) for the doctrine.

Step files are the contract between `/plan-feature` and `/build-step`. They must be complete enough that `/build-step` can execute without re-planning.

```markdown
# Step N: Name

**Estimated time:** X hours
**Test layer:** Domain | Storage | Integration | Component | Screen | Visual-baseline-only
**Risk:** Low / Medium / High — why
**Prerequisite:** Step N-1 complete (or: none)

---

## Acceptance criteria (subset of feature README's criteria that this step delivers)
- [ ] AC1: Given <precondition>, when <action>, then <expected>
- [ ] AC2: ...

## Technical constraints (applicable to this step)
- [ ] Constraint that must hold (e.g. "score validation runs in < 1ms on a 5-year-old phone")
- [ ] Constraint from a gate (e.g. "no telemetry deps added")

## Test plan
Copy-pasteable test code. One `it` block per AC. Test file path is explicit.

**File**: `src/lib/{module}/__tests__/{module}.test.ts`

```typescript
import { describe, expect, it } from 'vitest';
import { thingUnderTest } from '../{module}';

describe('{module}', () => {
  describe('{behavior}', () => {
    it('given <precondition>, when <action>, then <expected>', () => {
      // Arrange
      // Act
      // Assert
      expect(actual).toBe(expected);
    });
  });
});
```

## Done criteria
- [ ] Every AC above is GREEN
- [ ] RED was captured before implementation (output saved below)
- [ ] GREEN was captured after implementation (output saved below)
- [ ] Full suite still passes (no regressions)
- [ ] `npm run typecheck` clean
- [ ] `npm run lint` clean
- [ ] No new HIGH gate findings (cardinal / privacy / security / v1.5-v2)
- [ ] Walkthrough done if step touched daily screen (≤ 10s timed, brainfog pass, offline pass)
- [ ] Refactor pass complete (or "none needed" stated)

---

## Execution order (followed by `/build-step`)

### N.1 Baseline (if modifying existing behavior)
Capture current behavior — failing test output, screenshot, CSV diff — for regression comparison.

### N.2 Write tests (RED)
Paste the test code above into the file. Run:
```
npm test -- {pattern}
```
Must FAIL for the reason stated in each AC. Record the failure line under Done.

### N.3 Implement (GREEN)
Smallest code that turns the RED tests GREEN. Files to create / modify:
- `src/lib/{module}/{file}.ts` — [purpose]

Reference patterns from:
- [path]: [what to extract]

Run again:
```
npm test -- {pattern}
```
Must PASS. Record the pass line under Done.

### N.4 Regression check
```
npm test
```
Everything that was GREEN before must still be GREEN.

### N.5 Refactor
Clean up while GREEN stays GREEN. State what was changed, or "none needed".

### N.6 Walkthrough — if the step changed the daily screen
1. Open on target device / simulator
2. Stopwatch the daily-entry flow — must stay ≤ 10s
3. One-handed, low light, arm's length — any second-attempt tap is a fail
4. Airplane mode, repeat

### N.7 Checkpoint
What's safe to commit at this point. State the commit message that will be used.

---

## What this step does NOT do
Explicit scope boundary — prevents scope creep into adjacent features or future steps.
```

---

## Phase 5: Quality gates

Three mandatory reviews before a feature plan is ready to implement. Do each as a separate pass — don't combine.

### 5.1 Cardinal-principle gate

Walk every step and the README against each of the 6 cardinal principles from [CLAUDE.md](../../CLAUDE.md#cardinal-principles-hard-constraints):

- [ ] **One-tap entry**: nothing this feature adds blocks score-only entry. The score still saves on first tap.
- [ ] **Sub-10-second flow**: total time-on-screen for a typical daily entry stays under 10s with this feature merged. Estimated time cost per added interaction is documented.
- [ ] **No friction on main flow**: no required fields, no dropdowns, no sliders, no modal dialogs on the daily screen.
- [ ] **Brainfog-friendly**: tap targets are large enough for accidental-press tolerance; no screen requires more than one decision; copy is short and unambiguous; no animations or color flashes added.
- [ ] **No notifications / ads / analytics / tracking**: no telemetry deps added; no notifications in v1; if v2 notifications, they meet the silent-and-conditional spec from technisch_document.md.
- [ ] **Local-first**: new data lives on device by default; any sync is opt-in; opt-in surface is documented.

**Output**: HIGH / MEDIUM / LOW findings with specific fixes. Fix all HIGH before proceeding.

### 5.2 Privacy gate

- [ ] No analytics, tracking, ads, telemetry deps added (check `package.json` diffs).
- [ ] No third-party SDKs that phone home. If a dep does this with a toggle, the toggle is disabled and documented.
- [ ] Personal data does not enter the repo. Any sample / fixture data is anonymized.
- [ ] OS-level permissions are requested **per type**, not as a bundle (HealthKit: per `HKQuantityType`; Google Calendar: only `calendar.readonly`).
- [ ] User can see in Settings which data sources / types are active and disable each one.
- [ ] **Export still covers new data this feature introduces.** CSV export, JSON export, SQLite dump all include the new fields.
- [ ] **Delete still wipes new data.** Full-wipe leaves no orphan rows / files / cached tokens / pending sync queues.
- [ ] If cloud sync is touched: only aggregates, not raw HealthKit samples; opt-in per source.

**Output**: same severity scheme. Fix all HIGH before proceeding.

### 5.3 Security gate

Health data on a personal device is a security model with a different shape than a server-side web app — the threats are device compromise, leaky exports, injection from imported data, and supply-chain risk, not CSRF / XSS / SQL injection at an API. Reference frame: **OWASP MASVS** (Mobile Application Security Verification Standard), not the Web Top 10.

**At rest**

- [ ] SQLite encryption is on for the main DB. Master key derived via OS keystore (iOS Keychain / Android Keystore) — never hardcoded, never in `AsyncStorage`, never in a config file.
- [ ] OAuth refresh tokens (v1.5+) stored in Keychain/Keystore. Never in `AsyncStorage`, never in plaintext.
- [ ] SQLite DB is excluded from iCloud / Google Drive auto-backup, OR backup is explicit opt-in with a clear toggle. Health data leaking via "cloud backup the user forgot they enabled" is a real failure mode.

**In transit**

- [ ] All network calls use HTTPS. No HTTP fallback for any URL the app constructs or accepts.
- [ ] For OAuth endpoints (Google Calendar v1.5, sync backend v2): standard TLS validation. Consider certificate pinning for the sync backend specifically when v2 lands.

**Injection / untrusted input**

- [ ] SQL via parameterized queries only. No string-concatenation into SQL.
- [ ] **CSV formula injection on export**: cells starting with `=`, `+`, `-`, `@`, or `\t` are escaped (prefix with `'`). Excel and Sheets will execute formula-looking cells otherwise — real risk when the user opens the export.
- [ ] Import validation: malformed CSV / XLSX doesn't crash or write garbage. Out-of-range scores, dates outside `[2022-09-03, today]`, wrong column count → reject with a clear error, never partial-write.
- [ ] Deep-link / URL-scheme handlers treat input as untrusted. Never parsed straight into SQL, never `eval`-style execution.

**Permissions (least privilege)**

- [ ] HealthKit: requested per `HKQuantityType`. Never the bundled "all" prompt.
- [ ] Google Calendar: `calendar.readonly` only. No write scope, ever.
- [ ] Location: only requested if the feature actually needs it (v2 weather). Decline by default.
- [ ] Notifications: not requested in v1 at all.

**Mobile-specific**

- [ ] App-switcher snapshot doesn't leak the daily entry. Blur or hide the active screen on `applicationWillResignActive` (iOS) / `onPause` (Android) for any screen showing notes or scores.
- [ ] Clipboard interactions are explicit and user-initiated. No auto-copy of notes or tags.
- [ ] Universal links / Android App Links: validate the path before acting; don't accept arbitrary routing from a deep link.

**Build hygiene**

- [ ] No source maps in release builds.
- [ ] No `console.log` of scores, notes, tags, or any user content in production. Dev-only logging gated by `__DEV__`.
- [ ] Debug / inspector / "reset DB" screens gated by `__DEV__`. Hidden from release builds.

**Supply chain**

- [ ] `npm audit` shows zero high / critical before merging.
- [ ] New dependencies are checked: license (no GPL in MIT code), last-published date (no abandoned packages), maintainer reputation, transitive deps for telemetry or analytics.
- [ ] Lockfile committed. No floating versions.

**Output**: HIGH / MEDIUM / LOW findings. Fix all HIGH before proceeding.

### 5.4 v1.5 / v2 readiness gate

The brief is explicit: v1 architecture must enable v1.5 (projects, calendar) and v2 (HealthKit, Garmin, weather, reminders) without schema migrations or large refactors.

- [ ] If `DayEntry` is touched: nullable fields for `garmin`, `health`, `weather`, `calendar_events`, `project_entries`, `derived` remain present and untouched.
- [ ] If `Project` / `ProjectEntry` / `ProjectFieldConfig` is touched: schema stays open enough for arbitrary `numeric_values` / `tag_set` configurations.
- [ ] If `Tag` is touched: category supports `project:<id>` and `custom`.
- [ ] If introducing a data source: follows the standard "fetch + aggregate + store per day" interface so future sources slot in the same way.
- [ ] No assumption is baked in that limits us to "one Google account" or "one HealthKit type" — the data model survives multi-account / multi-type expansion.
- [ ] If choosing storage / sync technology: choice is made against the v2 passive-data load, not v1's needs.

**Output**: same severity scheme.

### 5.5 TDD-readiness check (for steps that have testable logic)

- [ ] Tests are written before implementation in step files (RED → GREEN flow).
- [ ] Test code is copy-pasteable — not pseudocode.
- [ ] Run commands are explicit.
- [ ] Done criteria are checkboxes that can be checked off.
- [ ] Each step has a safe commit point.
- [ ] Baseline capture exists when modifying production code.
- [ ] "What this step does NOT do" prevents scope creep.

### 5.6 Developer-readability check

Could a developer who didn't attend the planning session pick up this plan and execute it?

- [ ] No assumed context — every file referenced by full path from repo root.
- [ ] Execution order is numbered and sequential within each step.
- [ ] Dependencies between steps are explicit ("Prerequisite: Step N complete").
- [ ] Estimated time per step.
- [ ] Risk level per step with explanation.
- [ ] Dutch domain terms (`gevoelscore`, `blok 1`, `fysiek/mentaal/positief/activiteit`, `rustdag/licht/matig/zwaar`) are preserved as-is — don't translate them in the plan.

---

## Phase 6: Handoff

The feature plan is ready when:

1. README.md has all sections filled
2. All step files follow the TDD or walkthrough structure
3. Cardinal-principle, privacy, security, and v1.5/v2 readiness gates all pass with no open HIGH findings
4. Every step has testable / walkable done criteria

Output to the user:

- Summary of what was created (paths)
- Recommended starting step
- Any blocking dependencies or open questions
- Estimated total time

---

## Reference

- [docs/features/_template/](../../docs/features/_template/) — copy this to start a new feature folder
- [CLAUDE.md](../../CLAUDE.md) — cardinal principles, scope, tech stack, key rules
- [docs/REQUIREMENTS.md](../../docs/REQUIREMENTS.md) — v1 requirements
- [docs/app_brief_gevoelscore.md](../../docs/app_brief_gevoelscore.md) — full UX brief + data model + roadmap
- [docs/technisch_document.md](../../docs/technisch_document.md) — passive context, integrations, privacy
