# Step 2: Retire the `_scaffold` proof

**Estimated time:** 10 minutes
**Test layer:** Visual-baseline-only (test-runner config change; no new logic)
**Risk:** Low — only deletions + a one-line config edit
**Prerequisite:** Step 1 complete (the score test passes, proving the test loop works on real domain code)

> The `_scaffold` proof exists in `src/lib/_scaffold/` for the sole purpose of validating the test loop end-to-end before any real feature ships. Step 1 has now done that with real code. The scaffold's job is done.

---

## Acceptance criteria (this step delivers)

- [ ] AC1: After this step, `src/lib/_scaffold/` does not exist.
- [ ] AC2: After this step, `vitest.config.ts` no longer references `_scaffold` in its coverage `exclude` list.
- [ ] AC3: After this step, `npm test` reports 0 failed tests (the scaffold's intentional RED is gone, and the score test from Step 1 is GREEN).
- [ ] AC4: After this step, `npm run typecheck` is still clean.

## Technical constraints

- [ ] Pure deletion + config change. No new logic introduced.
- [ ] `vitest.config.ts` change is the minimum necessary — don't restructure the config.

## Test plan

No new test file is added in this step. The verification is that the existing test runs are green AFTER the deletion.

This step is "Visual-baseline-only" in the doctrine sense: the success criterion is observable runtime behavior (`npm test` exit code 0, expected file paths absent), not new asserted behavior.

---

## Done criteria

- [ ] `src/lib/_scaffold/` directory removed (verify with `Glob` or `ls`)
- [ ] `vitest.config.ts` no longer mentions `_scaffold`
- [ ] `npm test` → 0 failed, all score tests pass
- [ ] `npm run typecheck` clean
- [ ] No regressions to anything outside the scaffold

---

## Execution order

### 2.1 Baseline

Confirm Step 1 is complete: `npm test` shows the score tests GREEN and the `_scaffold` test RED. That's the baseline.

### 2.2 Delete the scaffold directory

```
rm -rf src/lib/_scaffold/
```

On Windows PowerShell:

```powershell
Remove-Item -Recurse -Force src/lib/_scaffold/
```

### 2.3 Update `vitest.config.ts`

Find the coverage `exclude` array and remove the `'**/_scaffold/**'` entry. Current state:

```typescript
coverage: {
  provider: 'v8',
  include: ['src/lib/**/*.ts'],
  exclude: ['**/__tests__/**', '**/_scaffold/**'],
  reporter: ['text', 'html'],
},
```

Target state:

```typescript
coverage: {
  provider: 'v8',
  include: ['src/lib/**/*.ts'],
  exclude: ['**/__tests__/**'],
  reporter: ['text', 'html'],
},
```

### 2.4 Run the full suite

```
npm test
```

Expected:

- `_scaffold.test.ts` is gone — not in the file list
- `score.test.ts` runs and passes
- Total: 0 failed, N passed (N = however many `it`/`it.each` rows are in score.test.ts)

### 2.5 Run typecheck

```
npm run typecheck
```

Expected: clean. The deletion shouldn't break types — nothing imported from `_scaffold` outside of the test that's also being deleted.

### 2.6 Checkpoint

Commit message:

```
score-validation/step-2: retire _scaffold proof

The scaffold's job (prove the TDD loop is wired up end-to-end) is now done
by the real score-validation tests from step-1. Removing.

- Deleted src/lib/_scaffold/ (3 files)
- Removed _scaffold exclusion from vitest.config.ts coverage
- npm test now reports 0 failed
```

---

## Done (filled in during `/build-step`)

- [x] AC1: `src/lib/_scaffold/` removed — verified with `Glob src/lib/_scaffold/**/*` returning empty on 2026-05-26
- [x] AC2: `vitest.config.ts` no longer mentions `_scaffold` — coverage `exclude` now reads `['**/__tests__/**']` on 2026-05-26
- [x] AC3: `npm test` → 0 failed | 26 passed (1 test file, all `score.test.ts`) on 2026-05-26
- [x] AC4: `npm run typecheck` clean (`tsc --noEmit`, exit 0) on 2026-05-26
- [x] No new HIGH gate findings (pure cleanup)
- [x] No walkthrough (no UI)
- [x] Refactor: none needed

---

## What this step does NOT do

- Does NOT add new tests.
- Does NOT change `package.json` (Vitest dep stays, no tooling change).
- Does NOT update `tsconfig.json` (no path changes).
- Does NOT touch `src/lib/_scaffold/README.md` separately — it's deleted as part of the whole directory.
