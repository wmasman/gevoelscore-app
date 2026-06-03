// Step 0 / AC0.10 + AC0.11 — verifier extensions for FK on_delete behavior
// (via Directus' /relations API) and UNIQUE indexes (via direct
// pg_indexes query).
//
// Both functions take DI'd transports so they unit-test cleanly:
//   verifyRelations(directusRequest, expectations)
//   verifyUniqueIndexes(queryPg, expectations)
//
// Each returns { passes: string[], failures: Array<{ name, issues: string[] }> }.
// Caller decides exit code from failures.length.

export async function verifyRelations(directusRequest, expectations) {
  const passes = [];
  const failures = [];

  for (const expected of expectations) {
    const name = `${expected.collection}.${expected.field}`;
    const issues = [];
    try {
      const res = await directusRequest(
        `/relations/${expected.collection}/${expected.field}`,
      );
      const data = res?.data;
      const actualRelated = data?.related_collection;
      const actualOnDelete = data?.schema?.on_delete;

      if (actualRelated !== expected.related_collection) {
        issues.push(
          `related_collection: expected ${expected.related_collection}, got ${actualRelated}`,
        );
      }
      if (actualOnDelete !== expected.on_delete) {
        issues.push(
          `on_delete: expected ${expected.on_delete}, got ${actualOnDelete}`,
        );
      }
    } catch (e) {
      const reason = e instanceof Error ? e.message : String(e);
      issues.push(`fetch failed: ${reason.split('\n')[0]}`);
    }

    if (issues.length === 0) {
      passes.push(name);
    } else {
      failures.push({ name, issues });
    }
  }

  return { passes, failures };
}

export async function verifyUniqueIndexes(queryPg, expectations) {
  const passes = [];
  const failures = [];

  // One query for all indexes; filter client-side. pg_indexes is cheap.
  const rows = await queryPg(
    "SELECT indexname, indexdef FROM pg_indexes WHERE schemaname = 'public'",
  );
  const byName = new Map(rows.map((r) => [r.indexname, r.indexdef]));

  for (const expected of expectations) {
    const issues = [];
    const def = byName.get(expected.indexname);
    if (!def) {
      issues.push('not found in pg_indexes');
    } else if (
      expected.definitionMustMatch &&
      !expected.definitionMustMatch.test(def)
    ) {
      issues.push(
        `definitionMustMatch: pattern ${expected.definitionMustMatch} did not match actual def "${def}"`,
      );
    }

    if (issues.length === 0) {
      passes.push(expected.indexname);
    } else {
      failures.push({ name: expected.indexname, issues });
    }
  }

  return { passes, failures };
}
