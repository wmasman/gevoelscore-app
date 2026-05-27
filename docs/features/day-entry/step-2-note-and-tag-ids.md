# Step 2: normalizeNote + validateTagIds

**Estimated time:** 25–35 min
**Test layer:** Domain
**Risk:** Low — two pure functions
**Prerequisite:** Step 1 complete

---

## Acceptance criteria

**normalizeNote:**

- [ ] AC2.1: `normalizeNote(null)` → `{ ok: true, value: null }`.
- [ ] AC2.2: `normalizeNote('')`, `normalizeNote('   ')`, `normalizeNote('\n\t ')` → `{ ok: true, value: null }`.
- [ ] AC2.3: `normalizeNote('hello')` → `{ ok: true, value: 'hello' }`.
- [ ] AC2.4: `normalizeNote('  hello  ')` → `{ ok: true, value: 'hello' }`.
- [ ] AC2.5: Non-string-non-null (number, object, array, boolean) → `{ ok: false, error: 'wrong_type' }`.

**validateTagIds:**

- [ ] AC2.6: `validateTagIds([])` → `{ ok: true, value: [] }`.
- [ ] AC2.7: `validateTagIds(['a','b'])` → `{ ok: true, value: ['a','b'] }`.
- [ ] AC2.8: `validateTagIds(['a','a'])` → `{ ok: false, error: 'duplicates' }`.
- [ ] AC2.9: Non-array input → `{ ok: false, error: 'wrong_type' }`.
- [ ] AC2.10: Array with any non-string element → `{ ok: false, error: 'non_string_element' }`.

## Done criteria

- [x] All ACs GREEN
- [x] RED captured: `npm test` → 19 failed | 62 passed on 2026-05-26 (with note + tag-ids stubs that always return wrong_type).
- [x] GREEN captured: `npm test` → 81/81 passing on 2026-05-26.
- [x] Full suite passes, typecheck clean.
- [x] No new HIGH gate findings.
- [x] Refactor: none needed.
