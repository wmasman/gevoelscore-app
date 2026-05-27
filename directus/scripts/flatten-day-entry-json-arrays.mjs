// Removes the remaining JSON-array foreign-key fields from `day_entries` and
// upgrades `project_entries.tag_ids` to a proper Directus M2M.
//
// Why:
//   day_entries.project_entry_ids / calendar_event_ids were JSON arrays of UUIDs
//   pointing at child collections. But project_entries and calendar_events both
//   have their own `date` column — joining by date is simpler and doesn't
//   require day_entries to keep a synchronised array of ids. Same anti-pattern
//   we removed for tags.
//
//   project_entries.tag_ids was a JSON array like day_entries.tag_ids was before
//   the M2M upgrade. project_entries is empty in v1, so there's no data to
//   migrate.
//
// What this does:
//   1. Deletes day_entries.project_entry_ids (drops the column)
//   2. Deletes day_entries.calendar_event_ids (drops the column)
//   3. Deletes project_entries.tag_ids (drops the column)
//   4. Creates project_entries_tags junction collection
//   5. Creates two relations (CASCADE on both FKs)
//   6. Creates two alias fields (project_entries.tags, tags.project_entries)
//
// Idempotent: each step checks current state and skips if already done.
//
// Pre-flight sanity:
//   - day_entries.project_entry_ids: expected to be NULL / [] on every row
//   - day_entries.calendar_event_ids: expected to be NULL / [] on every row
//   - project_entries: expected to have 0 rows (collection empty in v1)
//
//   We refuse to drop a field if it has non-empty data anywhere. This protects
//   against running this script on a v1.5 instance where these fields are in use.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."
//   node directus/scripts/flatten-day-entry-json-arrays.mjs

import {
  banner,
  collectionExists,
  directusRequest,
} from './lib/directus-request.mjs';

banner('flatten-day-entry-json-arrays');

const idField = {
  field: 'id',
  type: 'uuid',
  schema: { is_primary_key: true, has_auto_increment: false, is_nullable: false },
  meta: { hidden: true, readonly: true, interface: 'input', special: ['uuid'] },
};

async function fieldExists(collection, field) {
  try {
    await directusRequest(`/fields/${collection}/${field}`);
    return true;
  } catch (e) {
    return false;
  }
}

async function relationExists(collection, field) {
  try {
    await directusRequest(`/relations/${collection}/${field}`);
    return true;
  } catch (e) {
    return false;
  }
}

async function ensureFieldDropped(collection, field, preflightCheck) {
  if (!(await fieldExists(collection, field))) {
    console.log(`    ⏩ ${collection}.${field} already dropped`);
    return;
  }
  if (preflightCheck) {
    const nonEmpty = await preflightCheck();
    if (nonEmpty > 0) {
      throw new Error(
        `Pre-flight failed: ${collection}.${field} has ${nonEmpty} non-empty rows. ` +
          `Refusing to drop. Investigate before re-running.`,
      );
    }
  }
  console.log(`    🗑  Dropping ${collection}.${field}`);
  await directusRequest(`/fields/${collection}/${field}`, 'DELETE');
}

// ---------------------------------------------------------------------------
// 1-3. Drop JSON-array fields
// ---------------------------------------------------------------------------

console.log('  Drop JSON-array foreign-key fields:');

await ensureFieldDropped('day_entries', 'project_entry_ids', async () => {
  // a row is "non-empty" if project_entry_ids is not null AND not an empty array
  const r = await directusRequest(
    '/items/day_entries?limit=-1&fields=id,project_entry_ids&filter[project_entry_ids][_nnull]=true',
  );
  const rows = r.data ?? [];
  return rows.filter((row) => Array.isArray(row.project_entry_ids) && row.project_entry_ids.length > 0).length;
});

await ensureFieldDropped('day_entries', 'calendar_event_ids', async () => {
  const r = await directusRequest(
    '/items/day_entries?limit=-1&fields=id,calendar_event_ids&filter[calendar_event_ids][_nnull]=true',
  );
  const rows = r.data ?? [];
  return rows.filter((row) => Array.isArray(row.calendar_event_ids) && row.calendar_event_ids.length > 0).length;
});

await ensureFieldDropped('project_entries', 'tag_ids', async () => {
  // project_entries is expected to be empty in v1
  const r = await directusRequest(
    '/items/project_entries?aggregate[count]=id',
  );
  const count = Number(r.data?.[0]?.count?.id ?? r.data?.[0]?.count ?? 0);
  return count; // any rows at all means we'd need to migrate
});

// ---------------------------------------------------------------------------
// 4. Junction collection
// ---------------------------------------------------------------------------

console.log('\n  Create project_entries × tags M2M:');

if (await collectionExists('project_entries_tags')) {
  console.log('    ⏩ project_entries_tags junction already exists');
} else {
  console.log('    ➕ Creating project_entries_tags junction collection');
  await directusRequest('/collections', 'POST', {
    collection: 'project_entries_tags',
    schema: { name: 'project_entries_tags' },
    meta: {
      icon: 'link',
      note: 'Junction for project_entries ↔ tags M2M. Cascading deletes on both sides.',
      hidden: true,
    },
    fields: [
      idField,
      {
        field: 'project_entries_id',
        type: 'uuid',
        schema: { is_nullable: false },
        meta: { hidden: true, interface: 'select-dropdown-m2o' },
      },
      {
        field: 'tags_id',
        type: 'uuid',
        schema: { is_nullable: false },
        meta: { hidden: true, interface: 'select-dropdown-m2o' },
      },
      {
        field: 'sort',
        type: 'integer',
        schema: { is_nullable: true },
        meta: { hidden: true, interface: 'input' },
      },
      // Same provenance columns as day_entries_tags — kept consistent.
      {
        field: 'source',
        type: 'string',
        schema: { is_nullable: true, max_length: 20 },
        meta: {
          interface: 'select-dropdown',
          options: {
            choices: [
              { text: 'User chose', value: 'user' },
              { text: 'Note pattern match', value: 'note_pattern' },
              { text: 'CSV import', value: 'csv_import' },
              { text: 'Inferred', value: 'inferred' },
            ],
          },
        },
      },
      {
        field: 'confidence',
        type: 'float',
        schema: { is_nullable: true },
        meta: { interface: 'input' },
      },
      {
        field: 'confirmed_at',
        type: 'timestamp',
        schema: { is_nullable: true },
        meta: { interface: 'datetime' },
      },
    ],
  });
  console.log('    ✅');
}

// ---------------------------------------------------------------------------
// 5. Relations (CASCADE on both)
// ---------------------------------------------------------------------------

if (await relationExists('project_entries_tags', 'project_entries_id')) {
  console.log('    ⏩ relation project_entries_tags.project_entries_id already exists');
} else {
  console.log('    ➕ relation project_entries_tags.project_entries_id → project_entries.id (CASCADE)');
  await directusRequest('/relations', 'POST', {
    collection: 'project_entries_tags',
    field: 'project_entries_id',
    related_collection: 'project_entries',
    meta: { one_field: 'tags', junction_field: 'tags_id', sort_field: 'sort' },
    schema: { on_delete: 'CASCADE', on_update: 'NO ACTION' },
  });
  console.log('    ✅');
}

if (await relationExists('project_entries_tags', 'tags_id')) {
  console.log('    ⏩ relation project_entries_tags.tags_id already exists');
} else {
  console.log('    ➕ relation project_entries_tags.tags_id → tags.id (CASCADE)');
  await directusRequest('/relations', 'POST', {
    collection: 'project_entries_tags',
    field: 'tags_id',
    related_collection: 'tags',
    meta: { one_field: 'project_entries', junction_field: 'project_entries_id', sort_field: 'sort' },
    schema: { on_delete: 'CASCADE', on_update: 'NO ACTION' },
  });
  console.log('    ✅');
}

// ---------------------------------------------------------------------------
// 6. Alias fields (Directus doesn't always auto-create these)
// ---------------------------------------------------------------------------

if (await fieldExists('project_entries', 'tags')) {
  console.log('    ⏩ alias project_entries.tags already exists');
} else {
  console.log('    ➕ alias field project_entries.tags');
  await directusRequest('/fields/project_entries', 'POST', {
    field: 'tags',
    type: 'alias',
    schema: null,
    meta: {
      interface: 'list-m2m',
      special: ['m2m'],
      options: { template: '{{tags_id.label}}' },
    },
  });
  console.log('    ✅');
}

if (await fieldExists('tags', 'project_entries')) {
  console.log('    ⏩ alias tags.project_entries already exists');
} else {
  console.log('    ➕ alias field tags.project_entries');
  await directusRequest('/fields/tags', 'POST', {
    field: 'project_entries',
    type: 'alias',
    schema: null,
    meta: { interface: 'list-m2m', special: ['m2m'] },
  });
  console.log('    ✅');
}

console.log('\n✅ Done.\n');
