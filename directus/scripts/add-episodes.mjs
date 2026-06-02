// Adds the `episodes` collection + the `tags.parent_episode_id` FK column
// for the v1.5 verloop-and-episodes feature (user-facing tab: Periodes).
//
// Episodes are multi-day spans: interventies (coaching, ergo, meds courses)
// and levensgebeurtenissen (vakantie, partner-weg-weekend, etc). A Tag with
// `parent_episode_id` set is an "occurrence" of an Episode on its day.
// See docs/features/verloop-and-episodes/ for the full design.
//
// Idempotent:
//   - collection-create gated by collectionExists.
//   - field-adds gated by fieldExists.
//   - relation gated by relationExists.
//   Re-running the script is safe and prints only "⏩ already exists" lines.
//
// One POST per collection (per the locked schema-management convention —
// see docs/architecture/directus-schema-management.md "Lesson 3").
//
// ON DELETE SET NULL on tags.parent_episode_id:
//   If an episode is hard-deleted (Directus admin only — the v1.5 UI
//   archives, never hard-deletes), referencing tags revert to standalone
//   (parent_episode_id=null). Safer than CASCADE — a tag is meaningful on
//   its own, dropping a "doctor visit" tag because its parent episode was
//   nuked would be hostile.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "<static admin token>"
//   node directus/scripts/add-episodes.mjs

import {
  banner,
  collectionExists,
  directusRequest,
} from './lib/directus-request.mjs';

banner('add-episodes');

async function fieldExists(collection, field) {
  try {
    await directusRequest(`/fields/${collection}/${field}`);
    return true;
  } catch (e) {
    const msg = String(e.message);
    if (msg.includes('404') || msg.includes('FORBIDDEN')) return false;
    throw e;
  }
}

async function relationExists(collection, field) {
  try {
    await directusRequest(`/relations/${collection}/${field}`);
    return true;
  } catch (e) {
    const msg = String(e.message);
    if (msg.includes('404') || msg.includes('FORBIDDEN')) return false;
    throw e;
  }
}

// ----------------------------------------------------------------------------
// 1) Create the episodes collection (one POST with all 10 fields)
// ----------------------------------------------------------------------------

const idField = {
  field: 'id',
  type: 'uuid',
  schema: { is_primary_key: true, has_auto_increment: false, is_nullable: false },
  meta: { hidden: true, readonly: true, interface: 'input', special: ['uuid'] },
};

const episodesSpec = {
  collection: 'episodes',
  schema: { name: 'episodes' },
  meta: {
    icon: 'event_note',
    note: 'v1.5: Multi-day Episodes (interventies + levensgebeurtenissen). See features/verloop-and-episodes/.',
    collection: 'episodes',
    display_template: '{{label}} ({{start_date}} → {{end_date}})',
    sort_field: 'start_date',
  },
  fields: [
    idField,
    {
      field: 'label',
      type: 'string',
      schema: { is_nullable: false, max_length: 40 },
      meta: {
        interface: 'input',
        required: true,
        note: 'Short label (max 40 chars, no word-count limit). Narrative content goes in description.',
      },
    },
    {
      field: 'category',
      type: 'string',
      schema: { is_nullable: false, max_length: 32 },
      meta: {
        interface: 'select-dropdown',
        options: {
          choices: [
            { text: 'Interventie', value: 'interventie' },
            { text: 'Levensgebeurtenis', value: 'levensgebeurtenis' },
          ],
        },
        required: true,
        note: 'v1.5: interventie | levensgebeurtenis. project + patroon reserved for v2.',
      },
    },
    {
      field: 'start_date',
      type: 'date',
      schema: { is_nullable: false },
      meta: {
        interface: 'datetime',
        required: true,
        note: 'ISO YYYY-MM-DD. No upper bound — future-dated episodes allowed.',
      },
    },
    {
      field: 'end_date',
      type: 'date',
      schema: { is_nullable: true },
      meta: {
        interface: 'datetime',
        note: 'null = ongoing. When set, must be >= start_date (enforced by domain validator).',
      },
    },
    {
      field: 'description',
      type: 'text',
      schema: { is_nullable: true },
      meta: {
        interface: 'input-multiline',
        note: 'Optional free-text notes (dose schedules, frequencies, practitioner details).',
      },
    },
    {
      field: 'calendar_binding',
      type: 'json',
      schema: { is_nullable: true },
      meta: {
        interface: 'input-code',
        options: { language: 'json' },
        note: 'v1.6: Google Calendar series binding. Always null in v1.5 (domain validator enforces).',
      },
    },
    {
      field: 'archived_at',
      type: 'timestamp',
      schema: { is_nullable: true },
      meta: {
        interface: 'datetime',
        note: 'null = active. Soft-delete marker. Hard delete is Directus admin only.',
      },
    },
    {
      field: 'created_at',
      type: 'timestamp',
      schema: { is_nullable: true },
      meta: {
        special: ['date-created'],
        readonly: true,
        hidden: true,
        interface: 'datetime',
      },
    },
    {
      field: 'updated_at',
      type: 'timestamp',
      schema: { is_nullable: true },
      meta: {
        special: ['date-updated'],
        readonly: true,
        hidden: true,
        interface: 'datetime',
      },
    },
  ],
};

if (await collectionExists('episodes')) {
  console.log('  ⏩ episodes collection already exists — skipping');
} else {
  console.log(`  ➕ Creating episodes collection (${episodesSpec.fields.length} fields, one POST)...`);
  await directusRequest('/collections', 'POST', episodesSpec);
  console.log('  ✅ episodes');
}

// ----------------------------------------------------------------------------
// 2) Add tags.parent_episode_id (nullable uuid FK)
// ----------------------------------------------------------------------------

console.log('\n  ── tags.parent_episode_id ──');

if (await fieldExists('tags', 'parent_episode_id')) {
  console.log('  ⏩ tags.parent_episode_id already exists — skipping');
} else {
  console.log('  ➕ Adding tags.parent_episode_id (uuid, nullable, FK to episodes.id)');
  await directusRequest('/fields/tags', 'POST', {
    field: 'parent_episode_id',
    type: 'uuid',
    schema: {
      is_nullable: true,
      foreign_key_table: 'episodes',
      foreign_key_column: 'id',
    },
    meta: {
      interface: 'select-dropdown-m2o',
      special: ['m2o'],
      options: { template: '{{label}} ({{category}})' },
      note: 'Optional FK: when set, this tag is an "occurrence" of an Episode on its day. ON DELETE SET NULL.',
    },
  });
  console.log('  ✅');
}

// ----------------------------------------------------------------------------
// 3) Create the relation tags.parent_episode_id → episodes.id (SET NULL)
// ----------------------------------------------------------------------------

if (await relationExists('tags', 'parent_episode_id')) {
  console.log('  ⏩ relation tags.parent_episode_id already exists — skipping');
} else {
  console.log('  ➕ Creating relation tags.parent_episode_id → episodes.id (SET NULL on delete)');
  await directusRequest('/relations', 'POST', {
    collection: 'tags',
    field: 'parent_episode_id',
    related_collection: 'episodes',
    meta: { sort_field: null },
    schema: { on_delete: 'SET NULL', on_update: 'NO ACTION' },
  });
  console.log('  ✅');
}

// ----------------------------------------------------------------------------
// 4) Sanity check — counts only, never PII
// ----------------------------------------------------------------------------

console.log('\n  ── Sanity check ──');

const episodesCount = await directusRequest(
  '/items/episodes?aggregate[count]=id&limit=0',
);
const episodesN = Number(
  episodesCount.data?.[0]?.count?.id ?? episodesCount.data?.[0]?.count ?? 0,
);
console.log(`  episodes rows: ${episodesN} (expected 0)`);

const linkedTagsCount = await directusRequest(
  '/items/tags?aggregate[count]=id&filter[parent_episode_id][_nnull]=true&limit=0',
);
const linkedN = Number(
  linkedTagsCount.data?.[0]?.count?.id ?? linkedTagsCount.data?.[0]?.count ?? 0,
);
console.log(`  tags with parent_episode_id set: ${linkedN} (expected 0)`);

console.log('\n✅ Done. Run verify-schema.mjs next.\n');
