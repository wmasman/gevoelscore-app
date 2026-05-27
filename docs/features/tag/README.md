# Tag domain

**Feature:** Domain-layer validation for `Tag` — label, category enum, project_id correlation, usage_count, archived state.
**Version:** v1
**Status:** Complete (2026-05-26)
**Tests:** 63 new tests (233 total project tests, all GREEN)
**Parent doc:** [docs/architecture/data-model.md "Tag"](../../architecture/data-model.md)

---

## Overview

Validates the `Tag` entity end-to-end. Label rules (trimmed, non-empty), category enum (the 5 v1 clusters + interventie/project/custom), project_id correlation (required for `category === 'project'`, forbidden otherwise), usage_count (non-negative integer), archived_at (ISO 8601 UTC or null), created_at (ISO 8601 UTC).

Completes the v1 domain layer alongside [score-validation](../score-validation/) and [day-entry](../day-entry/).

---

## User need

Tags are personal and dynamic — the user adds them, renames them, archives them, merges them. The domain must enforce the rules that prevent garbage from reaching Directus: empty labels, mismatched category/project_id, negative usage counts. The UI needs typed error codes so it can show specific feedback ("label can't be empty", "this label already exists in this cluster") rather than generic "save failed".

---

## Acceptance criteria

**validateTagLabel:**

- [ ] AC1: Accepts non-empty trimmed strings.
- [ ] AC2: Trims surrounding whitespace.
- [ ] AC3: Rejects empty string → `'empty'`.
- [ ] AC4: Rejects whitespace-only → `'empty'`.
- [ ] AC5: Rejects non-string (number, null, undefined, object) → `'wrong_type'`.

**validateTagCategory:**

- [ ] AC6: Accepts each of `'mentaal'`, `'fysiek'`, `'overall'`, `'activiteit'`, `'gebeurtenis'`, `'interventie'`, `'project'`, `'custom'`.
- [ ] AC7: Rejects unknown strings (including the retired `'positief'`) → `'unknown_category'`.
- [ ] AC8: Rejects non-string → `'wrong_type'`.

**validateTag (composer):**

- [ ] AC9: Accepts a minimal valid Tag.
- [ ] AC10: Propagates label errors → `'invalid_label'`.
- [ ] AC11: Propagates category errors → `'invalid_category'`.
- [ ] AC12: `category === 'project'` requires `project_id` non-null → `'missing_project_id'`.
- [ ] AC13: `category !== 'project'` requires `project_id === null` → `'unexpected_project_id'`.
- [ ] AC14: Rejects negative `usage_count` → `'invalid_usage_count'`.
- [ ] AC15: Rejects non-integer `usage_count` → `'invalid_usage_count'`.
- [ ] AC16: Rejects malformed `archived_at` (non-null, non-ISO) → `'invalid_archived_at'`.
- [ ] AC17: Rejects malformed `created_at` → `'invalid_created_at'`.
- [ ] AC18: Rejects bad shape → `'invalid_shape'`.

---

## Technical constraints

- Pure TS, zero deps. Domain layer.
- Result-style return, matching `validateScore` and others.
- Reuses ISO 8601 UTC timestamp logic from `day-entry.ts` (extract to a shared helper if used a third time).

## Test plan

| File | Cases |
|------|-------|
| `src/lib/domain/__tests__/tag-label.test.ts` | AC1–AC5 |
| `src/lib/domain/__tests__/tag-category.test.ts` | AC6–AC8 |
| `src/lib/domain/__tests__/tag.test.ts` | AC9–AC18 |

---

## Architecture

```
src/lib/domain/
  tag-label.ts        — validateTagLabel
  tag-category.ts     — validateTagCategory (with the locked enum)
  tag.ts              — Tag type, validateTag composer
  __tests__/
    tag-label.test.ts
    tag-category.test.ts
    tag.test.ts
```

## Steps

- Step 1: [step-1-tag-label-and-category.md](step-1-tag-label-and-category.md)
- Step 2: [step-2-tag-composer.md](step-2-tag-composer.md)
