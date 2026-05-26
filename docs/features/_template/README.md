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

- **Offline**: [must work without network? specify]
- **At rest**: [any new persistent data; encryption stance; backup-exclusion stance]
- **Permissions**: [HealthKit types, OAuth scopes, location, notifications]
- **Performance**: [any timing budget — e.g. "daily-entry flow stays ≤ 10s"]
- **Dependencies**: [any new dep is audited per `.claude/conventions.md`]

---

## Test plan

For each layer touched, name the test file and the cases that will be written. This is the contract between planning and [`/build-step`](../../../.claude/commands/build-step.md). Doctrine: [`.claude/testing.md`](../../../.claude/testing.md).

| File | Cases (one per `it`, mapped to AC) |
|------|------------------------------------|
| `src/lib/{module}/__tests__/{module}.test.ts` | AC1: ...; AC2: ... |
| `src/lib/db/__tests__/{topic}.test.ts` | AC3: ... |

---

## Cardinal-principle impact

Walk each of the 6 cardinal principles. State the impact and how the design stays inside the principle. Be specific — vague statements like "respects the one-tap rule" don't count.

| Principle | Impact | How we stay inside |
|-----------|--------|--------------------|
| One-tap entry | e.g. "adds a chip-row below score" | "score still saves on first tap; chip-row is below and optional" |
| Sub-10-second flow | e.g. "adds ~1s if tags are used" | "tags only render if user has tagged before; defaults to collapsed for new users" |
| Brainfog-friendly | | |
| Local-first | | |
| No telemetry | | |
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

- **OS-level permissions requested**: [HealthKit types / OAuth scope / location / notifications — be specific, no "all"]
- **Data that leaves the device**: [none / aggregates only / specify]
- **Opt-in surface**: [where in the UI the user grants / revokes; per-source toggle]
- **Export coverage**: [confirm new fields are in CSV / JSON / SQLite dump exporters]
- **Delete coverage**: [confirm full-wipe removes all new data, cached tokens, sync queues]

---

## Security

Threat framing: what can be exfiltrated, corrupted, or executed by something/someone that shouldn't. Reference: OWASP MASVS.

- **At rest**: [encryption status of any new persistent data; key storage location — Keychain/Keystore, never AsyncStorage; backup-exclusion stance]
- **In transit**: [HTTPS confirmed for any new network calls; OAuth endpoints; certificate-pinning decision]
- **Injection / untrusted input**: [parameterized SQL; CSV-export formula-injection escaping; import validation rules; deep-link / URL-scheme handling]
- **Permissions (least privilege)**: [confirm narrowest scope used — `HKQuantityType`-level, `calendar.readonly`, no location-by-default]
- **Mobile-specific**: [app-switcher snapshot blur; clipboard discipline; universal-link validation if introduced]
- **Build hygiene**: [no source maps in release; no `console.log` of PII; `__DEV__` gating for debug screens]
- **Supply chain**: [new deps audited — license, last-published, maintainer, transitive telemetry; `npm audit` clean]

---

## v1.5 / v2 readiness

- **`DayEntry` impact**: [unchanged / added field `X` (nullable) / N/A]
- **Other schema impact**: [Project / Tag / CalendarEvent / new collection — describe]
- **Integration shape**: [if this touches a data source: confirm it follows the "fetch + aggregate + store per day" module interface]
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

- Imports from `src/lib/db/`: [...]
- Imports from `src/lib/integrations/`: [...]
- New hooks / screens / components: [...]
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

1. Device walkthrough: open the app on the target device, perform the daily-entry flow, stopwatch it.
2. Brainfog walkthrough: one-handed, low-light, arm's length. Any tap that needs a second attempt is a fail.
3. Offline check: airplane mode, repeat daily-entry flow.
4. Export check: trigger CSV export after using the feature, confirm new fields are present.
5. Delete check: trigger full wipe, confirm no orphan data.

### Testing strategy

[Any new pattern this feature introduces — snapshot tests, fixture format, walkthrough script — describe so the next feature can reuse it.]
