# `_scaffold` — TDD loop sanity check

This folder exists only to prove the test runner is wired up correctly before any real feature lands. **It is meant to be deleted** once the first real feature has its own first RED test.

## What's here

- [`_scaffold.ts`](_scaffold.ts) — a single function returning the wrong value on purpose.
- [`__tests__/_scaffold.test.ts`](__tests__/_scaffold.test.ts) — a single test that asserts the right value, so the test starts RED.

## Walkthrough — your first TDD loop on this repo

```bash
# 1. Install once
npm install

# 2. RED — the test should fail because the implementation returns 0, not 42.
npm test
# Expected: 1 failed | 0 passed
# Failure line: AssertionError: expected 0 to be 42

# 3. GREEN — edit src/lib/_scaffold/_scaffold.ts so it returns 42, then:
npm test
# Expected: 0 failed | 1 passed

# 4. That's the loop. Delete this whole folder when the first real test arrives.
```

## Why a scaffold instead of just an empty repo

A test runner with zero tests can't tell you whether it's correctly wired up. A scaffold with one RED test that you can turn GREEN by editing one line is the cheapest possible way to confirm:

- Vitest finds the test file via the glob in `vitest.config.ts`.
- TypeScript compiles the test file via `tsconfig.json`.
- `npm test` returns exit code 1 on RED, 0 on GREEN — important for CI later.
- The Given/When/Then test-file shape works end to end.

Once the first real feature (probably CSV import of the existing Google Sheet, or score validation) has its own first RED test, this whole folder goes away.

## Removal checklist

- [ ] First real test file exists under `src/lib/{module}/__tests__/`
- [ ] First real test goes RED on `npm test`
- [ ] `rm -rf src/lib/_scaffold/`
- [ ] `npm test` — confirm the real test is still found and still RED
- [ ] `vitest.config.ts` — `_scaffold` exclude line in coverage can be removed too
