# Step 0b: Tier 3 CHECK constraints (single step)

**Estimated time:** ~2 hours. Reuses everything step-0 introduced (sql-migration helper, raw-SQL pattern, verify-schema extension scaffold). No new tooling.
**Test layers:** Vitest unit tests for the audit logic + verifier expectations. Smoke that attempts to INSERT each violation type and asserts Directus rejects.
**Risk:** Low-medium. Adding a CHECK constraint on a column that has violating rows would fail the migration — pre-flight audit gates against this. Once added, the only risk is overly-strict ranges blocking legitimate values; the ranges chosen mirror what the app's domain validators already enforce.
**Prerequisite:** Step-0 shipped (commits `36737f5..2228f63`). `DATABASE_URL` in `.env.local` (same Neon connection step-0 uses).

> Step-0b closes the tier 3 hardening surfaced in the 2026-06-03 architectural audit: DB-level enforcement of the invariants the domain validators already check at the app layer. Belt-and-suspenders for the v1.5d cohort.

---

## Resolved decisions

- **6 CHECK constraints in one SQL migration file.** Same atomic-feel as step-0's migrations. Idempotent via `ADD CONSTRAINT IF NOT EXISTS` (PostgreSQL 17+; if the deployed PG is older, the script falls back to `DO ... IF NOT EXISTS` block).
- **Audit pre-flight, hard gate.** Migration script refuses to run while any violations exist. Same posture as step-0's UNIQUE-add scripts.
- **No automated "fix violations" pass.** A row that violates a CHECK is an app-layer bug to investigate, not a row to silently delete. Script surfaces samples and stops.
- **Ranges mirror the domain validators.** `score 1..10`, `sleep_hours 0..24`, `confidence 0..1`. Category enums match the locked `TAG_CATEGORIES` (8 values) + `EPISODE_CATEGORIES` (2 values).

---

## Acceptance criteria

### Audit + tooling

- [ ] **AC0b.1: New `directus/scripts/lib/audit-check-violations.mjs`** exports `findCheckViolations(directusRequest)` returning `Array<{ name, collection, count, samples }>` covering all 6 constraints. Read-only; client-side filtering over `limit=-1` pulls (collections are small enough).
- [ ] **AC0b.2: New `directus/scripts/find-check-violations.mjs`** CLI wrapper. Outputs human-readable summary + JSON. Exits 0 regardless of violation count (audit, not gate).

### Migration

- [ ] **AC0b.3: New SQL file `directus/migrations/2026-06-03-tier3-check-constraints.sql`** with all 6 ADD CONSTRAINT statements, idempotent via `DO ... IF NOT EXISTS` blocks for portability.

### Constraint-add script

- [ ] **AC0b.4: New `directus/scripts/add-tier3-check-constraints.mjs`** runs the SQL migration via `runSqlFile`. Pre-flight calls `findCheckViolations`; aborts if any returns count > 0 with sample IDs.

### Verifier extension

- [ ] **AC0b.5: `directus/scripts/verify-schema.mjs` extended** to assert the 6 CHECK constraints via `pg_constraint` query. Reuses `queryPg`. Each constraint name + the table it's on is asserted; constraint definition string is regex-matched for the key tokens (score `1.*10`, sleep_hours `0.*24`, etc.).

### Smoke

- [ ] **AC0b.6: New `scripts/tier3-constraint-smoke.mjs`** + PowerShell wrapper. For each constraint: try to INSERT a violating row via the Directus admin API; assert 400/422 with PG error code 23514 (check_violation). Cleanup any seeds even on partial failure.

---

## Constraints, exact shapes

| Name | Collection | Constraint |
|---|---|---|
| `tags_category_check` | `tags` | `CHECK (category IN ('mentaal','fysiek','overall','activiteit','gebeurtenis','interventie','project','custom'))` |
| `episodes_category_check` | `episodes` | `CHECK (category IN ('interventie','levensgebeurtenis'))` |
| `day_entries_score_check` | `day_entries` | `CHECK (score BETWEEN 1 AND 10)` |
| `day_entries_sleep_hours_check` | `day_entries` | `CHECK (sleep_hours IS NULL OR sleep_hours BETWEEN 0 AND 24)` |
| `episodes_date_order_check` | `episodes` | `CHECK (end_date IS NULL OR end_date >= start_date)` |
| `day_entries_tags_confidence_check` | `day_entries_tags` | `CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1)` |
| `project_entries_tags_confidence_check` | `project_entries_tags` | `CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1)` |

(That's 7 constraints — confidence is enforced on both junction tables for symmetry.)

---

## Build order (RED → GREEN per phase)

1. **Audit lib + CLI** — RED on `findCheckViolations` stub, GREEN with all-pass against prod (expect 0 violations).
2. **Migration SQL + add-constraint script** — apply against prod; verify-schema RED before, GREEN after.
3. **Smoke** — assert each violation type is rejected with PG 23514.

Commit at each phase boundary.

---

## Out of scope

- Tier 5 indexes (`tags.archived_at` etc) — premature at current scale.
- Trigger-based `usage_count` maintenance — over-engineering at single-user.
- `NOT NULL DEFAULT 'user'` on `day_entries_tags.source` — v2 LLM provenance.
- A more general "schema invariants registry" — over-engineering for 7 constraints. If a future tier 6+ appears, factor then.
