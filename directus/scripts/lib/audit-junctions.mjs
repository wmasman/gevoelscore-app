// Audit + dedup helpers for the day_entries_tags + project_entries_tags
// junction tables. Pure functions; dependency-injected directusRequest so
// they can be unit-tested with mocks.
//
// findDuplicateJunctions(directusRequest, collection) →
//   { collection, dupGroups, extraRows, samples }
//
// dedupJunctions({ directusRequest, recomputeTagUsage, collection, commit }) →
//   { kept: string[], deleted: string[], affectedTagIds: string[] }
//
// Junction tables differ only in their first FK field name:
//   day_entries_tags     → day_entries_id
//   project_entries_tags → project_entries_id

const FK_FIELD = {
  day_entries_tags: 'day_entries_id',
  project_entries_tags: 'project_entries_id',
};

const SAMPLE_LIMIT = 5;

export function fkFieldFor(collection) {
  const field = FK_FIELD[collection];
  if (!field) throw new Error(`Unknown junction collection: ${collection}`);
  return field;
}

function resolveId(value) {
  return typeof value === 'string' ? value : value?.id ?? null;
}

async function fetchAndGroup(directusRequest, collection) {
  const fkField = fkFieldFor(collection);
  const resp = await directusRequest(
    `/items/${collection}?limit=-1&fields=id,${fkField},tags_id`,
  );
  const rows = resp?.data ?? [];

  const groups = new Map();
  for (const row of rows) {
    const fk = resolveId(row[fkField]);
    const tag = resolveId(row.tags_id);
    if (!fk || !tag) continue;
    const key = `${fk}:${tag}`;
    let members = groups.get(key);
    if (!members) {
      members = [];
      groups.set(key, members);
    }
    members.push({ id: row.id, [fkField]: fk, tags_id: tag });
  }
  return { groups, fkField };
}

export async function findDuplicateJunctions(directusRequest, collection) {
  const { groups, fkField } = await fetchAndGroup(directusRequest, collection);

  let dupGroups = 0;
  let extraRows = 0;
  const samples = [];
  for (const members of groups.values()) {
    if (members.length <= 1) continue;
    dupGroups += 1;
    extraRows += members.length - 1;
    if (samples.length < SAMPLE_LIMIT) {
      const sample = {
        [fkField]: members[0][fkField],
        tags_id: members[0].tags_id,
        count: members.length,
      };
      samples.push(sample);
    }
  }
  return { collection, dupGroups, extraRows, samples };
}

export async function dedupJunctions({
  directusRequest,
  recomputeTagUsage,
  collection,
  commit,
}) {
  const { groups } = await fetchAndGroup(directusRequest, collection);

  const kept = [];
  const deleted = [];
  const affectedTagIds = new Set();

  for (const members of groups.values()) {
    if (members.length <= 1) continue;
    const sorted = [...members].sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));
    const [keeper, ...toDelete] = sorted;
    kept.push(keeper.id);
    for (const row of toDelete) deleted.push(row.id);
    affectedTagIds.add(keeper.tags_id);
  }

  if (commit && deleted.length > 0) {
    await directusRequest(`/items/${collection}`, 'DELETE', deleted);
    if (recomputeTagUsage) {
      await recomputeTagUsage([...affectedTagIds]);
    }
  }

  return {
    kept,
    deleted,
    affectedTagIds: [...affectedTagIds],
  };
}
