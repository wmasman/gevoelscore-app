# Step 1: parseImportCsv

**Estimated time:** 45–60 min
**Test layer:** Domain (lives in `src/lib/import/` but logically domain-adjacent — pure TS, no I/O)
**Risk:** Medium — hand-rolled CSV parser has edge cases (quotes, escapes, line endings)
**Prerequisite:** day-entry feature complete (uses `validateDate`, `validateScore`, `normalizeNote`)

## Acceptance criteria

See [README AC1–AC14](README.md).

## Done criteria

- [ ] All ACs GREEN
- [ ] RED captured
- [ ] GREEN captured
- [ ] Full suite + typecheck clean
