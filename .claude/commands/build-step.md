---
description: Implement one step from a feature plan using the strict RED → GREEN → REFACTOR loop. Use when actually writing code for a step in docs/features/{name}/step-N-*.md.
---

# Build Step

Walks one step file through the full TDD cycle. Input: a step file under `docs/features/{name}/step-N-{slug}.md`. Output: code that turns RED tests into GREEN tests, plus the step file's Done section filled in.

**Pairs with**: [`/plan-feature`](plan-feature.md) — which produced the step file in the first place.
**Doctrine**: [`.claude/testing.md`](../testing.md) — read it before invoking this skill.

## When to use

- A feature has been planned (`docs/features/{name}/README.md` + step files exist).
- You're about to implement one step.
- The step file has Acceptance Criteria and a Test plan section. If it doesn't, stop and run `/plan-feature` first.

## Inputs

- A path to the step file, or a feature name + step number: `/build-step new-feature step-1`
- If no argument: ask which feature and which step.

---

## Phase 1: Load context

### 1.1 Read the step file

Confirm it has:

- [ ] **Acceptance criteria** — bullet checklist of Given/When/Then behaviors
- [ ] **Technical constraints** — offline, encryption, perf, security gates that apply
- [ ] **Test plan** — what test files / what cases the step will produce
- [ ] **Done criteria** — checkboxes for completion

If any is missing, **stop**. Tell the user the step is under-planned and recommend `/plan-feature` to fix it. Do not improvise — TDD without a behavior spec degenerates into "tests that match whatever I wrote".

### 1.2 Read the feature README

Pick up the bigger context: alternatives considered, privacy/security framing, integration shape. Don't repeat the planning work — but if the step file conflicts with the README (different file paths, different types), stop and ask.

### 1.3 Read the doctrine

[`.claude/testing.md`](../testing.md) defines the loop, the test categories, and the test file shape. Apply it strictly.

---

## Phase 2: Write the test (RED)

### 2.1 Locate the test file

Per the doctrine table:

| Layer | Path |
|-------|------|
| Domain | `src/lib/{module}/__tests__/{module}.test.ts` |
| Storage | `src/lib/db/__tests__/{topic}.test.ts` |
| Integration | `src/lib/integrations/{source}/__tests__/{source}.test.ts` |
| Component | `src/components/__tests__/{component}.test.tsx` |

Create the file if it doesn't exist. Follow the test file shape from the doctrine.

### 2.2 Translate each acceptance criterion into an `it` block

One `it` per criterion. The `it` string is the Given/When/Then sentence verbatim — don't paraphrase.

```typescript
describe('score', () => {
  describe('validation', () => {
    it('given a value above 6, when validated, then it is rejected', () => {
      // Arrange — none

      // Act
      const result = validateScore(7);

      // Assert
      expect(result.ok).toBe(false);
      expect(result.error).toBe('out_of_range');
    });
  });
});
```

If a criterion is too vague to translate ("works well", "is fast enough"), **stop and ask the user to refine the criterion** in the step file. Vague criteria yield meaningless tests.

### 2.3 Confirm the test compiles

Run the type-checker on the test file before running the test:

```
npm run typecheck
```

Test code that doesn't compile is not yet RED — it's broken.

### 2.4 Run the test — must be RED

```
npm test -- <pattern>
```

Confirm:

- [ ] The test runs (no syntax error, no import error)
- [ ] The test **fails**
- [ ] It fails **because the assertion mismatches**, not because of a missing module or stack trace from the runner

If it passes on first run, the test isn't testing what you think it's testing. Tighten the assertion until it fails for the right reason.

**Capture the RED output** — one line, for the step's Done section:

```
RED: npm test -- score.test → 1 failed (validation rejects > 6)
```

---

## Phase 3: Implement (GREEN)

### 3.1 Write the smallest code that turns RED → GREEN

Not the cleanest. Not the most general. The smallest.

If you find yourself writing code that no current test requires, you're past the loop boundary. Either:

- Add a new RED test first (back to Phase 2), or
- Delete the extra code.

### 3.2 Run the test — must be GREEN

```
npm test -- <pattern>
```

All previously-RED tests are GREEN. No previously-GREEN tests went RED (regression check).

**Capture the GREEN output** — one line, for the Done section:

```
GREEN: npm test -- score.test → 3 passed
```

### 3.3 Run the full suite (regression check)

```
npm test
```

Everything that was GREEN before this step is still GREEN. If something went RED, you regressed — fix it before continuing.

---

## Phase 4: Refactor (while GREEN stays GREEN)

### 4.1 Clean while protected

Now that the test pins behavior, refactor freely:

- Rename for clarity
- Extract obvious duplication (3+ occurrences only — don't pre-abstract)
- Tighten types
- Remove dead branches the test confirmed unreachable

After each change, re-run the test. GREEN stays GREEN — or you broke something.

### 4.2 What NOT to refactor in this step

- Adjacent code the step doesn't touch (out of scope)
- Patterns the step doesn't establish (premature abstraction)
- Anything that would change the public interface — that's a new step, not a refactor

---

## Phase 5: Quality checks

### 5.1 Type check

```
npm run typecheck
```

Zero errors. No `@ts-ignore`, no `@ts-expect-error` introduced. No `any`, `unknown` without narrowing, or `Record<string, any>` for domain data.

### 5.2 Lint

```
npm run lint
```

Zero errors. Warnings reviewed and either fixed or explicitly suppressed with reason.

### 5.3 Gates re-check (lightweight)

Walk the four gates from `/plan-feature` Phase 5 against the actual code, not the plan:

- [ ] **Cardinal-principle**: nothing this step added blocks one-tap / sub-10s flow / brainfog-friendly.
- [ ] **Privacy**: new data fields are covered by export and full-wipe.
- [ ] **Security**: new at-rest data is encrypted; new network calls use HTTPS; new untrusted input is validated; no new telemetry deps.
- [ ] **v1.5/v2 readiness**: schema additions preserve nullable fields for future passive-data sources.

A "this looks fine, no new findings" is a valid result — but you have to look.

### 5.4 Walkthrough (only if the step changed the daily screen)

- [ ] Open the app on target device / simulator
- [ ] Time the daily entry flow with a stopwatch — must stay ≤ 10s on a good-day simulation
- [ ] One-handed, low light, arm's length — any tap that needs a second attempt is a fail
- [ ] Offline check: airplane mode, repeat the flow

---

## Phase 6: Fill in the step's Done section

Open the step file. Tick each Done-criteria checkbox. Add the RED and GREEN capture lines verbatim. Add a one-line refactor summary or "none needed".

Example:

```markdown
## Done

- [x] AC1: Score > 6 is rejected — test `score.test.ts:validation rejects > 6` GREEN
- [x] AC2: Score < 1 is rejected — test `score.test.ts:validation rejects < 1` GREEN
- [x] AC3: Half-values are allowed — test `score.test.ts:validation accepts 4.5` GREEN
- [x] RED captured: `npm test -- score.test` → 3 failed (validation rejects > 6, < 1, accepts 4.5) on 2026-05-26
- [x] GREEN captured: `npm test -- score.test` → 3 passed on 2026-05-26
- [x] Type check: `npm run typecheck` clean
- [x] Lint: `npm run lint` clean
- [x] No new HIGH gate findings
- [x] Refactor: extracted `isInRange()` helper for reuse in storage layer
```

If any checkbox can't be ticked, the step is not done. Stop, address the gap, then continue.

---

## Phase 7: Commit point

Commit message format:

```
<feature-name>/step-<N>: <one-line summary>

Acceptance criteria addressed:
- AC1: <criterion>
- AC2: <criterion>

Tests: <X new, Y passing total>
```

Commit only when the Done section is fully ticked. Never commit RED.

---

## Anti-patterns this skill explicitly prevents

- **Implement-first, test-later** — Phase 2 (test) precedes Phase 3 (implement). Not negotiable.
- **Tests that pass on first run** — Phase 2.4 explicitly requires RED first.
- **Tests that test the implementation** — `it` strings come from acceptance criteria, not from the code structure.
- **Refactoring while RED** — Phase 4 only happens after Phase 3 GREEN.
- **Skipping the regression run** — Phase 3.3 runs the full suite, not just the new test.
- **Marking a step done with un-ticked criteria** — Phase 6 requires every checkbox checked.
