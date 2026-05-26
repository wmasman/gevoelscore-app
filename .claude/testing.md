# Testing doctrine — TDD is the default

Every feature, every step, every behavior change goes through the same loop. There is no "we'll add tests later".

Loaded on demand by Claude when planning (`/plan-feature`) or implementing (`/build-step`). Linked from [CLAUDE.md](../CLAUDE.md).

---

## The loop

```
1. User need              — what the user is trying to accomplish, in their words
2. Acceptance criteria    — testable behavior (bullet checklist: "Given X, when Y, then Z")
3. Technical constraints  — offline, encryption, perf, deps, security gates
4. Tests                  — failing tests that pin each acceptance criterion
5. RED                    — run tests, confirm they fail for the right reason
6. Implement              — write the smallest code that turns RED → GREEN
7. GREEN                  — run tests, confirm they pass
8. Refactor               — clean up while GREEN stays GREEN
```

**Steps 1–3** are done by `/plan-feature` and live in the feature README.
**Steps 4–8** are done by `/build-step` and happen per step file.

---

## When TDD is mandatory

**Mandatory** for any code path with testable behavior:

- Domain logic — `DayEntry`, `Tag`, `Project`, score validation, date math, streak calculation
- API client — Directus query/mutation wrappers, response validation, error mapping
- Importers — CSV / XLSX / Google Sheet parsing, validation, dedup
- Exporters — CSV / JSON generation (including CSV formula-injection escaping)
- Integrations — Google Calendar (v1.5) / weather (v2) fetchers, aggregation, "store per day" pipeline
- Security utilities — encryption key derivation, OAuth token storage, sanitizers

**Replaced by visual baseline** (not skipped — replaced) for pure-styling work:

- Color palette tweaks, spacing adjustments, font choices
- Animation timing changes that don't affect logic
- Pure layout shuffles with no state changes

The replacement is: capture a baseline screenshot before, capture the new screenshot after, compare side by side. Attach both to the step's Done section.

**Never an exception**:

- "It's just a one-liner" — one-liners are the easiest tests to write and the most common bug sites.
- "I tested it manually" — manual testing doesn't survive the next refactor.
- "It's prototype code" — prototype code that ships becomes production code.

---

## Test categories

| Layer | What | Runner | Location |
|-------|------|--------|----------|
| **Domain** | Pure logic on plain TS types — score validation, tag merging, date math, CSV parsing. No React, no Directus client, no network. | Vitest (Node) | `src/lib/{module}/__tests__/*.test.ts` |
| **API client** | Directus client wrappers — query shape, response validation, error mapping. Uses a mocked Directus SDK or a real Directus test instance. | Vitest (Node) | `src/lib/api/__tests__/*.test.ts` |
| **Integration** | Per-source modules (Google Calendar v1.5, weather v2) with mocked transport but real aggregation. | Vitest (Node) | `src/lib/integrations/{source}/__tests__/*.test.ts` |
| **Component** | Render-and-assert for React components. `@testing-library/react`. | Vitest (jsdom) | `src/components/__tests__/*.test.tsx` |
| **Screen / flow** | End-to-end behavior on the daily-entry flow, timeline, import. Playwright. | Playwright | `e2e/` |
| **Walkthrough** | Brainfog walkthrough, sub-10s flow check — human-in-the-loop, not automated. | n/a | Done checkboxes in step file |

In v1 we will primarily write **domain**, **API-client**, and **integration** tests. Component / screen / e2e tests come in once the first daily-entry screen exists.

---

## Test file shape

Every test file follows this skeleton:

```typescript
import { describe, expect, it } from 'vitest';
// ... imports under test

describe('<module-name>', () => {
  describe('<behavior or function>', () => {
    it('given <precondition>, when <action>, then <expected>', () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```

Rules:

- One `describe` per module, one nested `describe` per behavior cluster.
- `it` strings are full Given/When/Then sentences. They double as documentation.
- Arrange / Act / Assert sections are visually separated by blank lines. No fluent chains that hide the three phases.
- One assertion per `it` where possible. If multiple, they must all be aspects of the same behavior.
- No conditional logic in tests (`if`, `for` with branching). If you need branches, write multiple `it` blocks.
- No shared mutable state between tests. Use `beforeEach` to reset; never rely on test order.

---

## RED is mandatory before GREEN

When you run the test for the first time after writing it:

1. It **must fail**.
2. It must fail **for the reason you expect** — the assertion mismatches, not a syntax error or missing import.
3. Capture the failing output in the step file's Done section (one line: `npm test -- score.test → 1 failed: score validation rejects > 6`).

If the test passes on first run, you wrote a test that doesn't test anything new — the behavior already existed. Either:

- Delete the test (it's redundant), or
- Tighten the assertion until it fails, then GREEN it.

---

## GREEN is the smallest change

Once RED:

- Write the **smallest** code that turns it GREEN. Not the cleanest, not the most general — the smallest.
- Resist adding features the test doesn't demand. Those are separate `it` blocks with separate RED-GREEN cycles.
- Resist adding abstractions ("I'll need a class for this later"). YAGNI applies inside the loop.

Once GREEN, you can refactor — but the test stays GREEN throughout. If refactoring turns it RED, you broke something.

---

## What a step's "Done" looks like

Every step file ends with this section, filled in during `/build-step`:

```markdown
## Done

- [x] Acceptance criteria 1: `<criterion>` — test `<file>:<test name>` GREEN
- [x] Acceptance criteria 2: ...
- [x] RED captured: `<command>` → `<failure summary>` on <date>
- [x] GREEN captured: `<command>` → `<X passing>` on <date>
- [x] Type check: `npm run typecheck` clean
- [x] Lint: `npm run lint` clean
- [x] No new HIGH cardinal-principle / privacy / security findings
- [x] Walkthrough (if daily-screen changed): timed <X>s, brainfog pass
- [x] Refactor pass: <one-line summary, or "none needed">
```

A step is only complete when every checkbox is checked.

---

## Tooling (current)

- **Runner**: Vitest (Node-based, framework-agnostic, fast TS)
- **Run all**: `npm test`
- **Run one file**: `npm test -- <pattern>`
- **Watch**: `npm test -- --watch`
- **Coverage**: `npm test -- --coverage` (target: 100% on `src/lib/domain/` and `src/lib/db/`, best-effort elsewhere)

The runner is configured in `vitest.config.ts`. The TS config is `tsconfig.json`. Both stay platform-agnostic for the domain + API-client layers; when component / screen tests land, a jsdom environment + `@testing-library/react` config will be added without removing the domain-layer setup.

---

## Anti-patterns (don't do these)

- **Tests after the fact.** "I'll write tests once the feature works" → tests will be skipped or shaped to fit the code, defeating their purpose.
- **Mocking what you don't own to the point of testing the mock.** If you're mocking the Directus SDK so heavily that you're asserting your own mock returned what you told it to return, the test is worthless. Either mock at the transport (`fetch`) boundary or run against a real ephemeral Directus test instance.
- **Snapshot-everything.** Snapshots are good for stable HTML/text output. They are bad for testing logic — a logic test should assert a specific value, not "matches snapshot".
- **`expect(true).toBe(true)` as a placeholder.** A test that can't fail is worse than no test.
- **Skipped tests left in the suite.** `it.skip` is a TODO that the suite stops reminding you about. Delete or fix.
- **Tests that depend on the current date / time / timezone without mocking.** Tomorrow's CI run will fail. Mock the clock.
- **Tests that touch real network / real Directus production / real Google.** Stub the transport at the integration boundary, or run against an ephemeral local Directus instance.
