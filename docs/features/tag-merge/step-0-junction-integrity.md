# Step 0: Junction + label integrity hardening (single step)

**Estimated time:** ~3-4 hours. New tooling (raw-SQL migration helper) + 2 audit scripts + 1 dedup script + 2 SQL migrations + extended verifier + 1 smoke. No application code.
**Test layers:** Vitest unit tests for the audit/dedup/SQL-helper logic. Integration assertions in `verify-schema.mjs` against a live Directus dev instance. Production smoke that asserts the new constraints are enforced.
**Risk:** Medium. Destructive operations on shared production data (gated by `--commit` + dry-run-by-default). The raw-SQL migration helper is a NEW tooling pattern that future schema work will reuse.
**Prerequisite:** Local PostgreSQL connection string from Fly (`fly secrets list -a gevoelscore-backend` → DATABASE_URL). Set `DATABASE_URL` in `.env.local` (already gitignored).

> Step 0 closes 4 DB-level integrity gaps before step 1 (tag-merge) ships:
> 1. `UNIQUE(day_entries_id, tags_id)` on `day_entries_tags` — prerequisite for merge's dedup-on-overlap correctness.
> 2. `UNIQUE(project_entries_id, tags_id)` on `project_entries_tags` — mirror; surface is schema-ready but data-empty.
> 3. `UNIQUE(LOWER(label), category) WHERE archived_at IS NULL` on `tags` — addresses the OTHER half of the duplicate-tag problem: merge cleans up legacy dups, this prevents new ones from being created.
> 4. `UNIQUE(LOWER(label), category) WHERE archived_at IS NULL` on `episodes` — same pattern.
>
> Plus `verify-schema.mjs` is extended to assert FK `on_delete` for all 6 currently-configured relations + the 4 new uniques, so future migrations can't silently regress any of this.

---

## Resolved decisions

- **Junction duplicates: auto-dedup.** Junction rows are commutative — same (day, tag) means the same fact. Keeping the lowest-id row and deleting the rest is loss-free. Script gated by `--commit`.
- **Tag-label duplicates: manual review only.** Two non-archived tags with the same lowered-label + category encode user intent ambiguity (which is canonical?). Script surfaces them and exits with a clear "merge via UI first" message. No automated dedup at this surface.
- **Constraint-add script refuses to run if audits report > 0.** Hard gate; no `--force` override.
- **Partial unique + composite unique = raw SQL.** Directus' field API doesn't expose `WHERE archived_at IS NULL` partial uniques or composite uniques on multi-collection junctions. New `directus/scripts/lib/sql-migration.mjs` connects directly to PostgreSQL using `DATABASE_URL`.
- **Idempotency = `CREATE UNIQUE INDEX IF NOT EXISTS`.** Safe re-run. Aborted migration leaves no half-state.
- **`pg` as a devDependency.** Added to `package.json` — small cost (~7MB) for a tool that all future PG-specific migrations will need.

---

## Acceptance criteria

### Audit scripts (read-only — no `--commit` gate needed)

- [ ] **AC0.1: New `directus/scripts/find-duplicate-junctions.mjs`** queries both `day_entries_tags` and `project_entries_tags` for tuples `(day_entries_id, tags_id)` and `(project_entries_id, tags_id)` with `COUNT(*) > 1`. Outputs JSON to stdout + human-readable summary. Read-only. Exits 0 even if duplicates found (audit, not gate).
- [ ] **AC0.2: New `directus/scripts/find-duplicate-tag-labels.mjs`** queries `tags` for `(LOWER(label), category) WHERE archived_at IS NULL` groups with `COUNT(*) > 1`; same for `episodes`. Outputs JSON + summary. Read-only.

### Dedup script (`--commit` gated)

- [ ] **AC0.3: New `directus/scripts/dedup-junctions.mjs`** reads find-duplicate-junctions output (or re-queries). For each dup group: keeps the row with the lowest UUID `id` (deterministic lex order), deletes the rest via the Directus SDK. After all deletions, calls `recompute-tag-usage.mjs`'s logic (or imports the helper) to fix any drifted `usage_count`. Dry-run prints the plan as `{group: ..., keep: id, delete: [ids]}` JSON. `--commit` performs.
- [ ] **AC0.4: NO dedup-tag-labels script.** Intentionally not built. find-duplicate-tag-labels surfaces; user merges via the v1.5c UI (post-step-1 ship) or via manual rename. Constraint-add refuses to run while any label-duplicates exist.

### SQL migration tooling (NEW pattern)

- [ ] **AC0.5: New helper `directus/scripts/lib/sql-migration.mjs`** exposes `runSqlFile(path: string): Promise<void>`. Reads the file, connects to PostgreSQL using `process.env.DATABASE_URL`, executes the SQL, returns. Aborts with a clear "DATABASE_URL not set; get it from `fly secrets list -a gevoelscore-backend`" message if env var is missing. Uses the `pg` npm package (added to `devDependencies`).
- [ ] **AC0.6: New SQL file `directus/migrations/2026-06-03-junction-unique-pairs.sql`** containing:
  ```sql
  CREATE UNIQUE INDEX IF NOT EXISTS day_entries_tags_unique_pair
    ON day_entries_tags (day_entries_id, tags_id);
  CREATE UNIQUE INDEX IF NOT EXISTS project_entries_tags_unique_pair
    ON project_entries_tags (project_entries_id, tags_id);
  ```
- [ ] **AC0.7: New SQL file `directus/migrations/2026-06-03-tag-label-uniqueness.sql`** containing:
  ```sql
  CREATE UNIQUE INDEX IF NOT EXISTS tags_label_category_active_unique
    ON tags (LOWER(label), category)
    WHERE archived_at IS NULL;
  CREATE UNIQUE INDEX IF NOT EXISTS episodes_label_category_active_unique
    ON episodes (LOWER(label), category)
    WHERE archived_at IS NULL;
  ```
- [ ] **AC0.8: New `directus/scripts/add-junction-unique-constraints.mjs`** runs the junction SQL file via `runSqlFile`. Pre-flight: calls find-duplicate-junctions logic; aborts with "deduplicate first" message if > 0 dups found.
- [ ] **AC0.9: New `directus/scripts/add-tag-label-unique-constraints.mjs`** runs the tag-label SQL file. Pre-flight: calls find-duplicate-tag-labels logic; aborts with "merge duplicates via UI first" message if > 0 found.

### Verifier extension (`directus/scripts/verify-schema.mjs`)

- [ ] **AC0.10: Verifier asserts 6 FK `on_delete` values:** `day_entries_tags.day_entries_id` → CASCADE, `day_entries_tags.tags_id` → CASCADE, `project_entries_tags.project_entries_id` → CASCADE, `project_entries_tags.tags_id` → CASCADE, `tags.parent_id` → SET NULL, `tags.parent_episode_id` → SET NULL. Uses `/relations/{collection}/{field}` for each and asserts `schema.on_delete` matches.
- [ ] **AC0.11: Verifier asserts 4 new uniques present** by querying `pg_index` via `runSqlFile` (or a new `queryPg(sql)` helper alongside `runSqlFile`):
  - `day_entries_tags_unique_pair` exists, is UNIQUE, covers `(day_entries_id, tags_id)`.
  - `project_entries_tags_unique_pair` exists, same shape.
  - `tags_label_category_active_unique` exists, is UNIQUE, partial (`WHERE archived_at IS NULL`), covers `(LOWER(label), category)`.
  - `episodes_label_category_active_unique` exists, same shape.

### Smoke (production after deploy)

- [ ] **AC0.12: New `scripts/junction-constraint-smoke.mjs`** (with `run-junction-constraint-smoke.ps1` wrapper):
  - Login → fetch a real day_entry with at least one tag.
  - Attempt to create a duplicate junction row (same `day_entries_id`, same `tags_id`) via POST `/items/day_entries_tags`.
  - Expect Directus to reject with 400/422 (PostgreSQL unique violation error code 23505 in the body).
  - Try to create a tag with label `_smoke dup` + category `custom`; immediately create another with the same label + category.
  - Expect 2nd create to fail.
  - Cleanup: hard-delete the first `_smoke dup` tag.
  - Project-junction smoke skipped with a logged note if `project_entries` is empty (currently true in v1).

---

## Technical constraints

- **`DATABASE_URL` is a NEW env var, NOT the same as `DIRECTUS_TOKEN`.** Source: `fly secrets list -a gevoelscore-backend`. Add to `.env.local` (gitignored). Never echo to chat or commit; PowerShell `Select-String` is the read pattern per existing security ops.
- **Raw SQL approach is for PG-specific primitives only.** Anything Directus' REST API can do continues to use the REST API (consistent with the existing schema-script pattern). The SQL helper exists for partial uniques + composite uniques + future CHECK constraints — things Directus' field-level API doesn't expose.
- **All migrations live in `directus/migrations/*.sql`.** New directory. Files are date-prefixed for ordering but applied via explicit script invocation, not auto-sequenced. Each is idempotent via `IF NOT EXISTS`.
- **No connection pooling.** The SQL helper opens one connection per `runSqlFile` call, runs, closes. One-shot tool; no need for pool management complexity.
- **Tag-label dedup is a USER decision, not a script.** Two same-label tags encode user intent ambiguity; auto-merge would erase that signal. The script surfaces them with clear messages: "Found N duplicate label/category groups. Resolve via the UI (rename one to differ OR merge via tag-management settings) before re-running."
- **Junction dedup uses lowest-id-wins.** Deterministic. UUID lexical order is stable across reruns. Could also use `created_at` but `id` is always present and unique.
- **`verify-schema.mjs` becomes the RED test for this whole step.** Run it FIRST before applying any migrations — it should fail loudly on the 4 missing uniques + the FK assertions (which are currently uncovered). After migrations, it passes. That's the TDD shape: verifier extension lands first (RED), migrations land second (GREEN), constraint enforcement smoke seals it.
- **Smoke runs AFTER frontend deploy** because production frontend doesn't change — the constraints land at the backend (Directus + PostgreSQL). But the smoke script lives in the frontend repo's `scripts/` for consistency with other smokes; it hits the production Directus directly.
- **No frontend dist change in this step.** Step 0 is schema + scripts only. Step 1 (the actual tag-merge UI) is the first step that ships frontend code on top of the new constraints.

---

## Test plan

### Audit scripts — `directus/scripts/__tests__/find-duplicates.test.mjs` (NEW; against mocked Directus aggregate responses)

1. `find-duplicate-junctions` with no duplicates → returns `{ dupGroups: 0, extraRows: 0 }`.
2. `find-duplicate-junctions` with 1 duplicate (3 rows on same `(day, tag)`) → returns `{ dupGroups: 1, extraRows: 2, samples: [{ day_entries_id, tags_id, count: 3 }] }`.
3. `find-duplicate-junctions` checks BOTH `day_entries_tags` and `project_entries_tags`; the totals sum across surfaces.
4. `find-duplicate-tag-labels` with no duplicates → returns `{ dupGroups: 0 }`.
5. `find-duplicate-tag-labels` case-insensitive: "Hoofdpijn" + "hoofdpijn" in same category → 1 dup group.
6. `find-duplicate-tag-labels` ignores `archived_at IS NOT NULL` rows (a same-label archived ghost + a non-archived live tag is NOT a duplicate by this constraint).

### Dedup script — `directus/scripts/__tests__/dedup-junctions.test.mjs` (NEW)

7. `dedup-junctions` with no duplicates → no-op + clean exit + no SDK delete calls.
8. `dedup-junctions` with 1 dup group of 3 rows → 2 delete calls (the 2 non-min-id rows), 0 deletes for the keeper.
9. `dedup-junctions` dry-run does NOT call delete on the SDK; prints the plan instead.
10. `dedup-junctions --commit` calls `recompute-tag-usage` logic at the end for any tags that lost junctions.

### SQL migration helper — `directus/scripts/__tests__/sql-migration.test.mjs` (NEW)

11. `runSqlFile` with valid SQL → connects, executes, closes, resolves.
12. `runSqlFile` with invalid SQL (syntax error) → throws; error message includes the failing statement.
13. `runSqlFile` with missing `DATABASE_URL` → throws with the actionable "get it from `fly secrets list -a gevoelscore-backend`" message.

### Verifier extension — `directus/scripts/__tests__/verify-schema.test.mjs` (NEW) or run as integration

14. `verify-schema` asserts `day_entries_tags.day_entries_id` has `on_delete=CASCADE` (PASS today).
15. `verify-schema` asserts `tags.parent_id` has `on_delete=SET NULL` (PASS today).
16. `verify-schema` asserts `day_entries_tags_unique_pair` index exists and is UNIQUE — **RED** until AC0.6 is applied; GREEN after.
17. `verify-schema` asserts `tags_label_category_active_unique` partial index exists with the correct WHERE clause — **RED** until AC0.7 is applied; GREEN after.
18. Verifier exits non-zero if ANY assertion fails (existing behaviour preserved).

### Constraint enforcement (smoke; against production Directus)

19. Attempt to POST a duplicate `day_entries_tags` row → Directus returns 400 with PG error code 23505 in the body.
20. Attempt to POST a duplicate `tags` row (same lowered-label + category, both non-archived) → 400 with 23505.
21. Smoke cleanup: hard-delete the first `_smoke dup` tag; assert no orphan junctions left behind (CASCADE should have run on the failed parent — actually no, the parent succeeded; only the 2nd was rejected).

---

## Build order (RED → GREEN per phase, verify gate at boundary)

5 phases. Commit at each boundary.

1. **Audit + dedup tooling** — find-duplicate-junctions, find-duplicate-tag-labels, dedup-junctions (tests 1-10). **Run against current prod (read-only)** to establish baseline. If any duplicates surfaced → pause, surface to user, decide per-case. Expected outcome: 0 dups in both audits (app-layer prevention has held up).

2. **SQL migration helper + `pg` dep** — `lib/sql-migration.mjs` (tests 11-13). Add `pg` to `devDependencies` via `npm install --save-dev pg`. Verify `DATABASE_URL` works locally by running a trivial `SELECT 1` through the helper.

3. **Verifier extension** — `verify-schema.mjs` additions (tests 14-18). **Run it — it should RED on the 4 missing uniques.** Commit the RED-passing scaffold + assertion code so the next phase has a test to turn GREEN.

4. **Apply migrations** — run `add-junction-unique-constraints.mjs --commit` (pre-flight check passes because phase 1 surfaced 0 dups). Then `add-tag-label-unique-constraints.mjs --commit` (same). Run `verify-schema.mjs` → all checks GREEN. If any RED remains, fix the migration SQL before continuing.

5. **Smoke + commit + deploy** — `junction-constraint-smoke.mjs` (tests 19-21). Commit migration SQL files + script changes + `package.json` + `verify-schema.mjs` changes. **No frontend deploy needed** for step 0 (constraints are backend-side); production frontend deploys with step 1 changes later.

---

## Out of scope (deferred — see `tier 3` / `tier 5` of the 2026-06-03 architectural audit)

- **CHECK constraints** (tier 3 of the audit): category enum check on `tags.category` + `episodes.category`, score range on `day_entries.score`, sleep_hours range, episode date order, confidence range. These are application-validated; DB-level enforcement is defense-in-depth, lower hazard than uniqueness gaps. **Follow-on as step-0b** if T1+T2 prove stable.
- **Performance indexes** (tier 5): `tags.archived_at`, `episodes.archived_at`, composite query indexes. Premature at current scale (~50-200 tags). Revisit at 10x.
- **Trigger-based `usage_count` maintenance.** Revisit when `usage_count` has 3+ consumers (currently: v1.5b delete-gate, v1.5c merge).
- **`NOT NULL DEFAULT 'user'` on `day_entries_tags.source`.** Revisit with v2 LLM provenance.
- **Schema snapshot / drift detection in CI.** Worthwhile, separate effort. The `verify-schema.mjs` extension is the manual equivalent for now; CI integration is a v1.6+ ergonomic.

---

## Notes for the next feature

- **The raw-SQL migration helper is the new pattern for PG-specific constraints.** Use it for step-0b's CHECK constraints. Use it any time Directus' API can't express a PG primitive (partial indexes, composite uniques, generated columns, CHECKs, triggers).
- **Verifier coverage is the safety net.** Every new constraint added in any future step MUST come with a `verify-schema.mjs` assertion. The pattern is established now; no excuse to skip.
- **The audit → dedup → add-constraint shape is reusable.** Tier 3 CHECK constraints follow the same shape: audit existing rows for violations, fix them (or refuse to add the constraint), then add, then verify.
- **Step-1 (tag-merge) gets a stronger correctness guarantee from this step.** With `UNIQUE(day_entries_id, tags_id)` live, the bulk PATCH after bulk DELETE ordering is BOTH semantically clean AND DB-enforced. A future refactor that flipped the order would surface the bug immediately as a PG 23505 error instead of silently creating duplicate junctions. Update [step-1-tag-merge.md](./step-1-tag-merge.md) AC5's Technical Constraints to reflect this transition from "we assume" → "we enforce".
- **Tag-label uniqueness preempts duplicate-creation pressure.** With the partial unique live, future inline-tag-creation (race or buggy retry) can no longer create "hoofdpijn" + "Hoofdpijn" + " hoofdpijn  " as separate rows in `fysiek`. The merge feature continues to exist for the legacy case (already-created duplicates) and for the genuine case (different labels that the user wants consolidated, e.g. "moe" + "vermoeid").
