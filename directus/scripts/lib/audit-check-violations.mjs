// Audit helper for tier 3 CHECK constraint violations. Read-only; pulls
// each affected collection in full and JS-filters for rows that would
// violate the constraint about to be applied (collections are small —
// tags ~hundreds, day_entries ~thousands at most, junctions bounded by
// usage_count).
//
// findCheckViolations(directusRequest) →
//   Array<{ name, collection, count, samples }>
//
// Each entry corresponds to one constraint we plan to add. count === 0
// across the board is the precondition for the constraint-add script.

const TAG_CATEGORIES = new Set([
  'mentaal',
  'fysiek',
  'overall',
  'activiteit',
  'gebeurtenis',
  'interventie',
  'project',
  'custom',
]);

const EPISODE_CATEGORIES = new Set(['interventie', 'levensgebeurtenis']);

const SAMPLE_LIMIT = 5;

function inRangeOrNull(value, min, max) {
  if (value === null || value === undefined) return true;
  return typeof value === 'number' && value >= min && value <= max;
}

async function readAll(directusRequest, collection, fields) {
  const url = `/items/${collection}?limit=-1&fields=${fields.join(',')}`;
  const resp = await directusRequest(url);
  return resp?.data ?? [];
}

export async function findCheckViolations(directusRequest) {
  const out = [];

  // tags.category enum
  const tags = await readAll(directusRequest, 'tags', ['id', 'label', 'category']);
  const badTagCats = tags.filter((t) => !TAG_CATEGORIES.has(t.category));
  out.push({
    name: 'tags_category_check',
    collection: 'tags',
    count: badTagCats.length,
    samples: badTagCats.slice(0, SAMPLE_LIMIT),
  });

  // episodes.category enum + date order — both need the episodes set
  const episodes = await readAll(directusRequest, 'episodes', [
    'id',
    'label',
    'category',
    'start_date',
    'end_date',
  ]);

  const badEpCats = episodes.filter((e) => !EPISODE_CATEGORIES.has(e.category));
  out.push({
    name: 'episodes_category_check',
    collection: 'episodes',
    count: badEpCats.length,
    samples: badEpCats.slice(0, SAMPLE_LIMIT),
  });

  const badEpDates = episodes.filter(
    (e) =>
      e.end_date !== null &&
      e.end_date !== undefined &&
      typeof e.end_date === 'string' &&
      typeof e.start_date === 'string' &&
      e.end_date < e.start_date,
  );
  out.push({
    name: 'episodes_date_order_check',
    collection: 'episodes',
    count: badEpDates.length,
    samples: badEpDates.slice(0, SAMPLE_LIMIT),
  });

  // day_entries: score + sleep_hours — both need the day_entries set
  const dayEntries = await readAll(directusRequest, 'day_entries', [
    'id',
    'date',
    'score',
    'sleep_hours',
  ]);

  const badScores = dayEntries.filter(
    (d) => typeof d.score !== 'number' || d.score < 1 || d.score > 10,
  );
  out.push({
    name: 'day_entries_score_check',
    collection: 'day_entries',
    count: badScores.length,
    samples: badScores.slice(0, SAMPLE_LIMIT),
  });

  const badSleep = dayEntries.filter((d) => !inRangeOrNull(d.sleep_hours, 0, 24));
  out.push({
    name: 'day_entries_sleep_hours_check',
    collection: 'day_entries',
    count: badSleep.length,
    samples: badSleep.slice(0, SAMPLE_LIMIT),
  });

  // Junction confidence — both junction tables, independent
  for (const collection of ['day_entries_tags', 'project_entries_tags']) {
    const rows = await readAll(directusRequest, collection, [
      'id',
      'tags_id',
      'confidence',
    ]);
    const bad = rows.filter((r) => !inRangeOrNull(r.confidence, 0, 1));
    out.push({
      name: `${collection}_confidence_check`,
      collection,
      count: bad.length,
      samples: bad.slice(0, SAMPLE_LIMIT),
    });
  }

  return out;
}

export { TAG_CATEGORIES, EPISODE_CATEGORIES, SAMPLE_LIMIT, inRangeOrNull };
