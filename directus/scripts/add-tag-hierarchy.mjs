// Adds a self-FK `parent_id` to `tags` so tags can form an intra-cluster
// hierarchy: `migraine.parent_id = hoofdpijn.id`, both with category='fysiek'.
//
// Why not move categories to their own table:
//   The 6 v1 clusters are locked-by-UX (chip rows on the daily screen) and
//   are deliberately not user-creatable. Per-category metadata (color, icon,
//   sort order) lives in code constants — see src/lib/domain/tag-category-meta.ts
//   (to be created when the UI lands).
//
// Why hierarchy:
//   Patterns matched against notes generate sibling tags today (hoofdpijn,
//   migraine, druk hoofd are all flat). Aggregating "all headache-like days"
//   currently means OR-ing labels. With parent_id, a query can walk the tree.
//
// Idempotent: re-runnable.
//
// ON DELETE SET NULL: if you delete a parent tag, children become orphans
// (parent_id=null), not deleted with it. Safer than CASCADE for a feature that
// hasn't proven itself yet.
//
// Usage:
//   $env:DIRECTUS_TOKEN = "..."
//   node directus/scripts/add-tag-hierarchy.mjs

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('add-tag-hierarchy');

async function fieldExists(collection, field) {
  try {
    await directusRequest(`/fields/${collection}/${field}`);
    return true;
  } catch (e) {
    return false;
  }
}

if (await fieldExists('tags', 'parent_id')) {
  console.log('  ⏩ tags.parent_id already exists — nothing to do');
} else {
  console.log('  ➕ Adding tags.parent_id (uuid, nullable, self-FK)');
  await directusRequest('/fields/tags', 'POST', {
    field: 'parent_id',
    type: 'uuid',
    schema: {
      is_nullable: true,
      foreign_key_table: 'tags',
      foreign_key_column: 'id',
    },
    meta: {
      interface: 'select-dropdown-m2o',
      special: ['m2o'],
      options: { template: '{{label}} ({{category}})' },
      note: 'Optional parent tag for intra-cluster hierarchy. e.g. migraine.parent_id = hoofdpijn.id',
    },
  });

  // Relation with ON DELETE SET NULL — children survive parent deletion.
  console.log('  ➕ Creating relation tags.parent_id → tags.id (SET NULL on delete)');
  await directusRequest('/relations', 'POST', {
    collection: 'tags',
    field: 'parent_id',
    related_collection: 'tags',
    meta: { sort_field: null },
    schema: { on_delete: 'SET NULL', on_update: 'NO ACTION' },
  });
  console.log('  ✅');
}

console.log('\n✅ Done. Set parent_id on tags via Directus admin UI or PATCH /items/tags/{id}.\n');
