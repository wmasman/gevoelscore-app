// Creates the v1 + v1.5/v2-placeholder collections in dependency order.
// Idempotent: re-running is safe (collections already present are skipped).
// Each collection is created with all fields in ONE POST per the one-POST rule
// (see docs/architecture/directus-schema-management.md "Lesson 3").
//
// Usage:
//   $env:DIRECTUS_TOKEN = "<static token>"
//   node directus/scripts/setup-schema.mjs

import {
  banner,
  collectionExists,
  directusRequest,
} from './lib/directus-request.mjs';

banner('setup-schema');

// ----------------------------------------------------------------------------
// Shared field templates
// ----------------------------------------------------------------------------

const idField = {
  field: 'id',
  type: 'uuid',
  schema: { is_primary_key: true, has_auto_increment: false, is_nullable: false },
  meta: { hidden: true, readonly: true, interface: 'input', special: ['uuid'] },
};

const createdAtField = {
  field: 'created_at',
  type: 'timestamp',
  schema: { is_nullable: true },
  meta: {
    special: ['date-created'],
    readonly: true,
    hidden: true,
    interface: 'datetime',
  },
};

const updatedAtField = {
  field: 'updated_at',
  type: 'timestamp',
  schema: { is_nullable: true },
  meta: {
    special: ['date-updated'],
    readonly: true,
    hidden: true,
    interface: 'datetime',
  },
};

// ----------------------------------------------------------------------------
// Collection definitions — IN DEPENDENCY ORDER (collections that other
// collections reference must come first).
// ----------------------------------------------------------------------------

const collections = [
  // -----------------------------------------------------------
  // projects — v1.5 (schema exists in v1, no rows written)
  // -----------------------------------------------------------
  {
    collection: 'projects',
    schema: { name: 'projects' },
    meta: {
      icon: 'medication',
      note: 'v1.5: Active interventies/projecten. Empty in v1.',
      collection: 'projects',
      hidden: false,
    },
    fields: [
      idField,
      {
        field: 'name',
        type: 'string',
        schema: { is_nullable: false, max_length: 200 },
        meta: { interface: 'input', required: true },
      },
      {
        field: 'type',
        type: 'string',
        schema: { is_nullable: false, max_length: 30 },
        meta: {
          interface: 'select-dropdown',
          options: {
            choices: [
              { text: 'Medicatie', value: 'medicatie' },
              { text: 'Therapie', value: 'therapie' },
              { text: 'Oefening', value: 'oefening' },
              { text: 'Anders', value: 'anders' },
            ],
          },
          required: true,
        },
      },
      {
        field: 'start_date',
        type: 'date',
        schema: { is_nullable: false },
        meta: { interface: 'datetime', required: true },
      },
      {
        field: 'end_date',
        type: 'date',
        schema: { is_nullable: true },
        meta: { interface: 'datetime', note: 'null = open-ended' },
      },
      {
        field: 'status',
        type: 'string',
        schema: { is_nullable: false, max_length: 20, default_value: 'active' },
        meta: {
          interface: 'select-dropdown',
          options: {
            choices: [
              { text: 'Active', value: 'active' },
              { text: 'Paused', value: 'paused' },
              { text: 'Completed', value: 'completed' },
              { text: 'Archived', value: 'archived' },
            ],
          },
        },
      },
      {
        field: 'description',
        type: 'text',
        schema: { is_nullable: true },
        meta: { interface: 'input-multiline' },
      },
      createdAtField,
      updatedAtField,
    ],
  },

  // -----------------------------------------------------------
  // tags — v1 (CORE: every day_entry can have many tags)
  // -----------------------------------------------------------
  {
    collection: 'tags',
    schema: { name: 'tags' },
    meta: {
      icon: 'sell',
      note: 'v1 tag clusters: mentaal/fysiek/overall/activiteit/gebeurtenis + interventie/project/custom',
      collection: 'tags',
    },
    fields: [
      idField,
      {
        field: 'label',
        type: 'string',
        schema: { is_nullable: false, max_length: 100 },
        meta: { interface: 'input', required: true },
      },
      {
        field: 'category',
        type: 'string',
        schema: { is_nullable: false, max_length: 20 },
        meta: {
          interface: 'select-dropdown',
          options: {
            choices: [
              { text: 'Mentaal', value: 'mentaal' },
              { text: 'Fysiek', value: 'fysiek' },
              { text: 'Overall', value: 'overall' },
              { text: 'Activiteit', value: 'activiteit' },
              { text: 'Gebeurtenis', value: 'gebeurtenis' },
              { text: 'Interventie', value: 'interventie' },
              { text: 'Project', value: 'project' },
              { text: 'Custom', value: 'custom' },
            ],
          },
          required: true,
        },
      },
      {
        field: 'project_id',
        type: 'uuid',
        schema: {
          is_nullable: true,
          foreign_key_table: 'projects',
          foreign_key_column: 'id',
        },
        meta: {
          interface: 'select-dropdown-m2o',
          note: "Required when category='project', forbidden otherwise — enforced by domain layer",
        },
      },
      {
        field: 'usage_count',
        type: 'integer',
        schema: { is_nullable: false, default_value: 0 },
        meta: { interface: 'input', readonly: true },
      },
      {
        field: 'archived_at',
        type: 'timestamp',
        schema: { is_nullable: true },
        meta: { interface: 'datetime', note: 'null = active' },
      },
      createdAtField,
    ],
  },

  // -----------------------------------------------------------
  // project_field_configs — v1.5
  // -----------------------------------------------------------
  {
    collection: 'project_field_configs',
    schema: { name: 'project_field_configs' },
    meta: {
      icon: 'settings',
      note: 'v1.5: Per-project field definitions. Empty in v1.',
    },
    fields: [
      idField,
      {
        field: 'project_id',
        type: 'uuid',
        schema: {
          is_nullable: false,
          foreign_key_table: 'projects',
          foreign_key_column: 'id',
        },
        meta: { interface: 'select-dropdown-m2o', required: true },
      },
      {
        field: 'key',
        type: 'string',
        schema: { is_nullable: false, max_length: 50 },
        meta: { interface: 'input', required: true },
      },
      {
        field: 'label',
        type: 'string',
        schema: { is_nullable: false, max_length: 100 },
        meta: { interface: 'input', required: true },
      },
      {
        field: 'type',
        type: 'string',
        schema: { is_nullable: false, max_length: 20 },
        meta: {
          interface: 'select-dropdown',
          options: {
            choices: [
              { text: 'Text', value: 'text' },
              { text: 'Tag set', value: 'tag_set' },
              { text: 'Number', value: 'number' },
            ],
          },
        },
      },
      {
        field: 'unit',
        type: 'string',
        schema: { is_nullable: true, max_length: 20 },
        meta: { interface: 'input', note: 'e.g. "mg", "min"' },
      },
      {
        field: 'default_visible',
        type: 'boolean',
        schema: { is_nullable: false, default_value: true },
        meta: { interface: 'boolean' },
      },
    ],
  },

  // -----------------------------------------------------------
  // day_entries — THE cardinal entity (v1)
  // -----------------------------------------------------------
  // Tags are a proper Directus M2M relation via the `day_entries_tags`
  // junction collection (created after this loop, see "M2M setup" below).
  // The M2M alias field `day_entries.tags` is added in that same phase.
  //
  // Still-JSON in v1 (deferred until used): project_entry_ids,
  // calendar_event_ids — these are empty in v1 and will likely become proper
  // 1:N relations via a `day_entry_id` FK on the child collections in v1.5.
  // -----------------------------------------------------------
  {
    collection: 'day_entries',
    schema: { name: 'day_entries' },
    meta: {
      icon: 'calendar_today',
      note: 'The cardinal entity — one row per local-date the user has logged.',
      collection: 'day_entries',
      display_template: '{{date}} — score {{score}}',
    },
    fields: [
      idField,
      {
        field: 'date',
        type: 'date',
        schema: { is_nullable: false, is_unique: true },
        meta: { interface: 'datetime', required: true, note: 'Natural identity; UNIQUE per local-date' },
      },
      {
        field: 'score',
        type: 'integer',
        schema: { is_nullable: false },
        meta: {
          interface: 'input',
          required: true,
          note: 'Integer 1-10 (no halves). Domain-validated.',
        },
      },
      {
        field: 'note',
        type: 'text',
        schema: { is_nullable: true },
        meta: { interface: 'input-multiline' },
      },
      // NOTE: `tags` is an M2M alias field, created in the M2M setup phase
      // after this collection loop completes. It is NOT a real DB column on
      // day_entries — the relation lives in the day_entries_tags junction.
      {
        field: 'sub_scores',
        type: 'json',
        schema: { is_nullable: true },
        meta: {
          interface: 'input-code',
          options: { language: 'json' },
          note: 'v2: { cognitive, physical, mental } each 1-6 or null. Null in v1.',
        },
      },
      {
        field: 'sleep_hours',
        type: 'float',
        schema: { is_nullable: true },
        meta: { interface: 'input', note: 'v2: 0-24, decimals allowed. Null in v1.' },
      },
      {
        field: 'special_event',
        type: 'string',
        schema: { is_nullable: true, max_length: 500 },
        meta: { interface: 'input', note: 'v1.5: handmatige "iets speciaals". Null in v1.' },
      },
      {
        field: 'project_entry_ids',
        type: 'json',
        schema: { is_nullable: true },
        meta: {
          interface: 'input-code',
          options: { language: 'json' },
          note: 'v1.5: JSON array of ProjectEntry.id UUIDs. Empty in v1.',
        },
      },
      {
        field: 'calendar_event_ids',
        type: 'json',
        schema: { is_nullable: true },
        meta: {
          interface: 'input-code',
          options: { language: 'json' },
          note: 'v1.5: JSON array of CalendarEvent.id UUIDs. Empty in v1.',
        },
      },
      {
        field: 'garmin',
        type: 'json',
        schema: { is_nullable: true },
        meta: { interface: 'input-code', options: { language: 'json' }, note: 'v2 only. Null in v1/v1.5.' },
      },
      {
        field: 'health',
        type: 'json',
        schema: { is_nullable: true },
        meta: { interface: 'input-code', options: { language: 'json' }, note: 'v2 only. Null in v1/v1.5.' },
      },
      {
        field: 'weather',
        type: 'json',
        schema: { is_nullable: true },
        meta: { interface: 'input-code', options: { language: 'json' }, note: 'v2 only. Null in v1/v1.5.' },
      },
      {
        field: 'derived',
        type: 'json',
        schema: { is_nullable: true },
        meta: { interface: 'input-code', options: { language: 'json' }, note: 'v2 only. Null in v1/v1.5.' },
      },
      createdAtField,
      updatedAtField,
    ],
  },

  // -----------------------------------------------------------
  // project_entries — v1.5
  // -----------------------------------------------------------
  {
    collection: 'project_entries',
    schema: { name: 'project_entries' },
    meta: { icon: 'note_add', note: 'v1.5: Per-project per-day entries. Empty in v1.' },
    fields: [
      idField,
      {
        field: 'date',
        type: 'date',
        schema: { is_nullable: false },
        meta: { interface: 'datetime' },
      },
      {
        field: 'project_id',
        type: 'uuid',
        schema: {
          is_nullable: false,
          foreign_key_table: 'projects',
          foreign_key_column: 'id',
        },
        meta: { interface: 'select-dropdown-m2o' },
      },
      {
        field: 'note',
        type: 'text',
        schema: { is_nullable: true },
        meta: { interface: 'input-multiline' },
      },
      {
        field: 'tag_ids',
        type: 'json',
        schema: { is_nullable: true },
        meta: { interface: 'input-code', options: { language: 'json' } },
      },
      {
        field: 'numeric_values',
        type: 'json',
        schema: { is_nullable: true },
        meta: { interface: 'input-code', options: { language: 'json' }, note: 'Shape: { [field_key]: number }' },
      },
      createdAtField,
      updatedAtField,
    ],
  },

  // -----------------------------------------------------------
  // calendar_events — v1.5 (Google Calendar sync target)
  // -----------------------------------------------------------
  {
    collection: 'calendar_events',
    schema: { name: 'calendar_events' },
    meta: { icon: 'event', note: 'v1.5: Google Calendar read-only sync. Empty in v1.' },
    fields: [
      idField,
      {
        field: 'google_event_id',
        type: 'string',
        schema: { is_nullable: false, is_unique: true, max_length: 200 },
        meta: { interface: 'input', readonly: true },
      },
      {
        field: 'date',
        type: 'date',
        schema: { is_nullable: false },
        meta: { interface: 'datetime' },
      },
      {
        field: 'title',
        type: 'string',
        schema: { is_nullable: false, max_length: 500 },
        meta: { interface: 'input' },
      },
      {
        field: 'start_time',
        type: 'timestamp',
        schema: { is_nullable: true },
        meta: { interface: 'datetime' },
      },
      {
        field: 'end_time',
        type: 'timestamp',
        schema: { is_nullable: true },
        meta: { interface: 'datetime' },
      },
      {
        field: 'all_day',
        type: 'boolean',
        schema: { is_nullable: false, default_value: false },
        meta: { interface: 'boolean' },
      },
      {
        field: 'calendar_source',
        type: 'string',
        schema: { is_nullable: false, max_length: 200 },
        meta: { interface: 'input' },
      },
      {
        field: 'attendees_count',
        type: 'integer',
        schema: { is_nullable: true },
        meta: { interface: 'input' },
      },
      {
        field: 'location',
        type: 'string',
        schema: { is_nullable: true, max_length: 500 },
        meta: { interface: 'input' },
      },
      {
        field: 'relevance',
        type: 'string',
        schema: { is_nullable: false, max_length: 10, default_value: 'normal' },
        meta: {
          interface: 'select-dropdown',
          options: {
            choices: [
              { text: 'High', value: 'high' },
              { text: 'Normal', value: 'normal' },
              { text: 'Hidden', value: 'hidden' },
            ],
          },
        },
      },
      {
        field: 'category_hint',
        type: 'string',
        schema: { is_nullable: true, max_length: 50 },
        meta: { interface: 'input' },
      },
    ],
  },

  // -----------------------------------------------------------
  // v2 placeholders — schema-readiness rule per data-model.md
  // Minimum fields (id, date UNIQUE, data JSON) so the schema exists
  // before v2 features write to it. Refine when v2 work begins.
  // -----------------------------------------------------------
  {
    collection: 'garmin_daily',
    schema: { name: 'garmin_daily' },
    meta: { icon: 'watch', note: 'v2 only — empty placeholder, refine when v2 lands.' },
    fields: [
      idField,
      {
        field: 'date',
        type: 'date',
        schema: { is_nullable: false, is_unique: true },
        meta: { interface: 'datetime' },
      },
      {
        field: 'data',
        type: 'json',
        schema: { is_nullable: true },
        meta: { interface: 'input-code', options: { language: 'json' } },
      },
    ],
  },
  {
    collection: 'health_daily',
    schema: { name: 'health_daily' },
    meta: { icon: 'health_and_safety', note: 'v2 only — empty placeholder.' },
    fields: [
      idField,
      {
        field: 'date',
        type: 'date',
        schema: { is_nullable: false, is_unique: true },
        meta: { interface: 'datetime' },
      },
      {
        field: 'data',
        type: 'json',
        schema: { is_nullable: true },
        meta: { interface: 'input-code', options: { language: 'json' } },
      },
    ],
  },
  {
    collection: 'weather_daily',
    schema: { name: 'weather_daily' },
    meta: { icon: 'cloud', note: 'v2 only — empty placeholder.' },
    fields: [
      idField,
      {
        field: 'date',
        type: 'date',
        schema: { is_nullable: false, is_unique: true },
        meta: { interface: 'datetime' },
      },
      {
        field: 'data',
        type: 'json',
        schema: { is_nullable: true },
        meta: { interface: 'input-code', options: { language: 'json' } },
      },
    ],
  },
];

// ----------------------------------------------------------------------------
// Execute
// ----------------------------------------------------------------------------

async function createOrSkip(spec) {
  const name = spec.collection;
  if (await collectionExists(name)) {
    console.log(`  ⏩ ${name} already exists — skipping (idempotent re-run)`);
    return;
  }
  console.log(`  ➕ Creating ${name} (${spec.fields.length} fields, one POST)...`);
  await directusRequest('/collections', 'POST', spec);
  console.log(`  ✅ ${name}`);
}

for (const spec of collections) {
  await createOrSkip(spec);
}

// ----------------------------------------------------------------------------
// M2M setup: day_entries × tags
// ----------------------------------------------------------------------------
// Junction collection + two relations (with CASCADE) + two alias fields.
// Idempotent: skip if junction / relation / alias already exists.

console.log('\n  ── M2M setup: day_entries × tags ──');

async function relationExists(collection, field) {
  try {
    await directusRequest(`/relations/${collection}/${field}`);
    return true;
  } catch (e) {
    return false;
  }
}

async function fieldExists(collection, field) {
  try {
    await directusRequest(`/fields/${collection}/${field}`);
    return true;
  } catch (e) {
    return false;
  }
}

// Junction collection
if (await collectionExists('day_entries_tags')) {
  console.log('  ⏩ day_entries_tags junction already exists');
} else {
  console.log('  ➕ Creating day_entries_tags junction collection...');
  await directusRequest('/collections', 'POST', {
    collection: 'day_entries_tags',
    schema: { name: 'day_entries_tags' },
    meta: {
      icon: 'link',
      note: 'Junction for day_entries ↔ tags M2M. Cascading deletes on both sides.',
      hidden: true,
    },
    fields: [
      idField,
      {
        field: 'day_entries_id',
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
    ],
  });
  console.log('  ✅');
}

// Relations (CASCADE on both sides)
if (await relationExists('day_entries_tags', 'day_entries_id')) {
  console.log('  ⏩ relation day_entries_tags.day_entries_id already exists');
} else {
  console.log('  ➕ Creating relation: day_entries_tags.day_entries_id → day_entries.id (CASCADE)');
  await directusRequest('/relations', 'POST', {
    collection: 'day_entries_tags',
    field: 'day_entries_id',
    related_collection: 'day_entries',
    meta: { one_field: 'tags', junction_field: 'tags_id', sort_field: 'sort' },
    schema: { on_delete: 'CASCADE', on_update: 'NO ACTION' },
  });
  console.log('  ✅');
}

if (await relationExists('day_entries_tags', 'tags_id')) {
  console.log('  ⏩ relation day_entries_tags.tags_id already exists');
} else {
  console.log('  ➕ Creating relation: day_entries_tags.tags_id → tags.id (CASCADE)');
  await directusRequest('/relations', 'POST', {
    collection: 'day_entries_tags',
    field: 'tags_id',
    related_collection: 'tags',
    meta: { one_field: 'day_entries', junction_field: 'day_entries_id', sort_field: 'sort' },
    schema: { on_delete: 'CASCADE', on_update: 'NO ACTION' },
  });
  console.log('  ✅');
}

// Alias fields (Directus doesn't always auto-create these from relations)
if (await fieldExists('day_entries', 'tags')) {
  console.log('  ⏩ alias day_entries.tags already exists');
} else {
  console.log('  ➕ Creating alias field day_entries.tags');
  await directusRequest('/fields/day_entries', 'POST', {
    field: 'tags',
    type: 'alias',
    schema: null,
    meta: {
      interface: 'list-m2m',
      special: ['m2m'],
      options: { template: '{{tags_id.label}}' },
    },
  });
  console.log('  ✅');
}

if (await fieldExists('tags', 'day_entries')) {
  console.log('  ⏩ alias tags.day_entries already exists');
} else {
  console.log('  ➕ Creating alias field tags.day_entries');
  await directusRequest('/fields/tags', 'POST', {
    field: 'day_entries',
    type: 'alias',
    schema: null,
    meta: { interface: 'list-m2m', special: ['m2m'] },
  });
  console.log('  ✅');
}

console.log('\n✅ Schema setup complete. Run verify-schema.mjs next.\n');
