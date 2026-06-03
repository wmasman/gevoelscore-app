// Audit helper for duplicate (LOWER(label), category) groups in `tags` +
// `episodes` collections, scoped to non-archived rows. Pure function;
// dependency-injected directusRequest for unit tests.
//
// findDuplicateTagLabels(directusRequest, collection) →
//   { collection, dupGroups, extraRows, samples }
//
// `collection` is 'tags' or 'episodes'. Both have label / category /
// archived_at fields. Grouping is by LOWER(label) + category, excluding
// archived rows. Matches the PostgreSQL partial unique index this audit
// precedes (step-0 AC0.7).

const SAMPLE_LIMIT = 5;

export async function findDuplicateTagLabels(directusRequest, collection) {
  // Pull non-archived rows; archived_at IS NULL filter mirrors the partial
  // unique index. Limit -1 = no cap; tag corpus is small (~50-200 today).
  const resp = await directusRequest(
    `/items/${collection}?limit=-1&filter[archived_at][_null]=true&fields=id,label,category,archived_at`,
  );
  const rows = resp?.data ?? [];

  const groups = new Map();
  for (const row of rows) {
    if (row.archived_at !== null && row.archived_at !== undefined) continue;
    if (typeof row.label !== 'string' || typeof row.category !== 'string') continue;
    const key = `${row.label.toLowerCase()}::${row.category}`;
    let members = groups.get(key);
    if (!members) {
      members = { label: row.label.toLowerCase(), category: row.category, count: 0 };
      groups.set(key, members);
    }
    members.count += 1;
  }

  let dupGroups = 0;
  let extraRows = 0;
  const samples = [];
  for (const group of groups.values()) {
    if (group.count <= 1) continue;
    dupGroups += 1;
    extraRows += group.count - 1;
    if (samples.length < SAMPLE_LIMIT) {
      samples.push({ label: group.label, category: group.category, count: group.count });
    }
  }
  return { collection, dupGroups, extraRows, samples };
}
