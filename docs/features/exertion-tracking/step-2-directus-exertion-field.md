# Step 2: Directus — add the `exertion` JSON field + verify

**Estimated time:** 30–45 min
**Test layer:** Schema (idempotent migration + `verify-schema.mjs` assertion)
**Risk:** Low — one nullable JSON column on an existing collection.
**Prerequisite:** none (independent of Step 1).

---

## Acceptance criteria (this step)

- [ ] AC6: `day_entries` has a nullable `exertion` column of type `json`. Running the migration script twice is idempotent (second run is a no-op, exit 0, no duplicate-field error).
- [ ] AC7: `verify-schema.mjs` asserts the `exertion` column exists, is type `json`, and is nullable. The `gevoelscore-frontend-api` role can read **and** write the field.

## Technical constraints

- **Idempotent REST script** in `directus/scripts/add-exertion-field.mjs`. One-POST rule: POST the field definition to `/fields/day_entries`; if it already exists (Directus 400/409), treat as success. **Never** `schema apply` / `schema.yml`.
- Field definition mirrors the existing `sub_scores` field in [`setup-schema.mjs`](../../../directus/scripts/setup-schema.mjs): `{ field: 'exertion', type: 'json', schema: { is_nullable: true }, meta: { interface: 'input-code', ... } }`.
- Uses the **admin token** (local script), per [memory: scoped-directus-token] — not the scoped frontend token.
- After adding the field, confirm the frontend role's field access. `day_entries` is already an allowed collection; if its policy grants fields `*` the new column is covered automatically — verify, and only re-run [`setup-permissions.mjs`](../../../directus/scripts/setup-permissions.mjs) if fields are enumerated.

### Standards-enforcement

| Concern | Checklist sections | Applies? | Note |
|---|---|---|---|
| New route handler | A01,A03,A08 | No | schema script only |
| New collection storing user data | GDPR Art 9, NEN 7510 | Partial | new *field* on existing health-data collection; covered by existing retention + export/delete of `day_entries` |
| New dependency | ADR/rationale | No | reuses `@directus/sdk` / fetch already in scripts |
| New env var with secret | A02,A05 | No | reuses existing `DIRECTUS_URL` + admin token |
| New telemetry dep | Cardinal no-telemetry | No | — |

## Test plan

| File | Cases |
|------|-------|
| `directus/scripts/add-exertion-field.mjs` | manual: run once (creates), run twice (no-op). Confirm via Directus admin + a `readField` call. |
| `directus/scripts/verify-schema.mjs` (extend) | new assertion: `exertion` present, `type === 'json'`, `is_nullable === true`. Prod verifier count goes up by 1, stays all-green. |
| `tests/live-stack/` (optional) | round-trip: write `{cognitive:2,physical:4,emotional:1}` to a throwaway date, read it back, assert equality, delete. |

## Done criteria

- [ ] Migration applied to the dev/prod Directus; second run idempotent (output recorded).
- [ ] `verify-schema.mjs` extended; full prod verifier green (count incremented by 1).
- [ ] Frontend role can read + write `exertion` (verified via a frontend-token read/write, or by confirming `*` field access).
- [ ] No HIGH gate findings.

---

## Execution order

### 2.1 Baseline
Record current `verify-schema.mjs` pass count (e.g. "56/56"). Confirm `exertion` does **not** yet exist (`readField('day_entries','exertion')` → 403/404).

### 2.2 Write the migration
`directus/scripts/add-exertion-field.mjs` — connect with admin token, POST the field def, catch already-exists and log "exertion field already present, skipping". Mirror any existing single-field-add script in `directus/scripts/` for house style; otherwise model the field object on `setup-schema.mjs`'s `sub_scores`.

### 2.3 Apply
Run against dev first, then prod. Run twice; second run must be a clean no-op.

### 2.4 Extend the verifier
Add the `exertion` column assertion to `verify-schema.mjs` (it already inspects `day_entries` columns + the junction FKs). Run the full verifier — all green.

### 2.5 Permission check
With a **frontend** (scoped) token, read a `day_entries` row including `exertion`, and PATCH `exertion` on a throwaway date. If either 403s, re-run `setup-permissions.mjs` after adding `exertion` to the field list (per [memory: setup-permissions-drift]). Most likely `*` access already covers it.

### 2.6 Checkpoint
Commit: `feat(exertion/step-2): add nullable exertion json field + schema verify`.

---

## What this step does NOT do
No domain validation (Step 1), no app-side read/write wiring (Step 3), no UI (Step 4). Does not add a DB-level CHECK constraint on the 1–4 range — the JSON column is unconstrained at the DB; the 1–4 rule lives in the domain validator (consistent with how `sub_scores` is handled). A CHECK could be a later hardening step if desired.
