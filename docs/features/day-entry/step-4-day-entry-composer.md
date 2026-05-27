# Step 4: validateDayEntry composer

**Estimated time:** 45–60 min
**Test layer:** Domain
**Risk:** Medium — orchestrates 6 sub-validators + shape check + timestamp order
**Prerequisite:** Steps 1–3 complete

---

## Acceptance criteria

- [ ] AC4.1: Accepts a minimal valid v1 DayEntry (date, score, normalized note, tag_ids, timestamps, v1.5/v2 fields all null/empty).
- [ ] AC4.2: Accepts a DayEntry with `sub_scores` populated (v2 forward-compat path through `validateSubScores`).
- [ ] AC4.3: Propagates date errors → `'invalid_date'`.
- [ ] AC4.4: Propagates score errors → `'invalid_score'`.
- [ ] AC4.5: Normalizes whitespace-only note to null in the returned value.
- [ ] AC4.6: Propagates tag_ids errors → `'invalid_tag_ids'`.
- [ ] AC4.7: Rejects `created_at > updated_at` → `'invalid_timestamp_order'`.
- [ ] AC4.8: Rejects bad shape (not object, missing/extra keys) → `'invalid_shape'`.
- [ ] AC4.9: Rejects v2 fields (`garmin`/`health`/`weather`/`derived`) when non-null → `'invalid_v2_field'`.
- [ ] AC4.10: Validates `created_at` / `updated_at` are ISO 8601 UTC strings → `'invalid_created_at'` / `'invalid_updated_at'`.

## Done criteria

- [x] All ACs GREEN
- [x] RED captured: `npm test` → 24 failed | 146 passed (with composer stub always returning invalid_shape) on 2026-05-26.
- [x] GREEN captured: `npm test` → 170/170 passing on 2026-05-26.
- [x] Full suite passes, typecheck clean, `npm audit` shows 0 vulnerabilities.
- [x] No new HIGH gate findings (pure domain, no I/O, no new deps, no telemetry).
- [x] Refactor: composer reuses `validateTagIds` for `project_entry_ids` and `calendar_event_ids` (same shape contract); private `isIsoUtcTimestamp` helper consolidates the timestamp check. No duplication.
