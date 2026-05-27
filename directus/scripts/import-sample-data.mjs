// Imports docs/sample-data.csv (anonymized 60-day sample, date+score only)
// into the gevoelscore-backend Directus instance.
//
// Idempotent: upsert by date. Re-running is safe — existing rows are PATCHed,
// new ones are POSTed.
//
// Scope-note: this script has a deliberately minimal inline CSV parser because
// the sample is 2-column quoted-CSV with no commas-in-fields and no escapes.
// The canonical 3-column parser lives in src/lib/import/csv-day-entries.ts
// and will be used by the user-facing import flow (which runs inside Next.js
// where TS is native — no `tsx` needed there).

import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { banner, directusRequest } from './lib/directus-request.mjs';

const CSV_PATH = resolve(
  new URL('.', import.meta.url).pathname.replace(/^\/(\w):/, '$1:'), // Windows path fix
  '../../docs/sample-data.csv',
);

banner('import-sample-data');
console.log(`  Source CSV: ${CSV_PATH}\n`);

// ---------------------------------------------------------------------------
// 1. Read + parse the CSV (2-column: "date","score")
// ---------------------------------------------------------------------------

const raw = await readFile(CSV_PATH, 'utf8');
const lines = raw.replace(/^﻿/, '').split(/\r\n|\n/).filter((l) => l.trim());

// Skip header if present
const hasHeader = /^"?date"?\s*,\s*"?score"?/i.test(lines[0] ?? '');
const dataLines = hasHeader ? lines.slice(1) : lines;

console.log(`  Parsed ${dataLines.length} data rows (header ${hasHeader ? 'detected and skipped' : 'absent'})\n`);

// ---------------------------------------------------------------------------
// 2. Validate + parse each row
// ---------------------------------------------------------------------------

const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;
const today = (() => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
})();

const parsed = [];
const skipped = [];
for (let i = 0; i < dataLines.length; i++) {
  const line = dataLines[i];
  const rowIndex = i + (hasHeader ? 2 : 1);

  // Minimal quoted-CSV split — handles `"date","score"` safely
  const cells = line.match(/("([^"]*)"|[^,]+)/g)?.map((c) => c.replace(/^"|"$/g, ''));
  if (!cells || cells.length !== 2) {
    skipped.push({ rowIndex, reason: 'wrong_column_count', raw: line });
    continue;
  }

  const date = cells[0].trim();
  const scoreStr = cells[1].trim();

  if (!ISO_DATE.test(date)) {
    skipped.push({ rowIndex, reason: 'invalid_date_format', raw: line });
    continue;
  }
  if (date > today) {
    skipped.push({ rowIndex, reason: 'future_date', raw: line });
    continue;
  }
  const score = Number(scoreStr);
  if (!Number.isInteger(score) || score < 1 || score > 10) {
    skipped.push({ rowIndex, reason: 'invalid_score', raw: line });
    continue;
  }
  parsed.push({ rowIndex, date, score });
}

console.log(`  Validation: ${parsed.length} valid, ${skipped.length} skipped`);
if (skipped.length > 0) {
  console.log('  Skipped rows:');
  for (const s of skipped.slice(0, 5)) {
    console.log(`    row ${s.rowIndex}: ${s.reason} — ${s.raw}`);
  }
  if (skipped.length > 5) console.log(`    ... +${skipped.length - 5} more`);
}
console.log();

// ---------------------------------------------------------------------------
// 3. Upsert each row to Directus
// ---------------------------------------------------------------------------

let created = 0;
let updated = 0;
let failed = 0;
const failures = [];

for (const row of parsed) {
  try {
    // Check if a day_entry already exists for this date
    const existing = await directusRequest(
      `/items/day_entries?filter[date][_eq]=${row.date}&fields=id&limit=1`,
    );

    if (existing.data && existing.data.length > 0) {
      // PATCH existing
      await directusRequest(
        `/items/day_entries/${existing.data[0].id}`,
        'PATCH',
        { score: row.score },
      );
      updated++;
    } else {
      // POST new — sample CSV is date+score only, no tags
      await directusRequest('/items/day_entries', 'POST', {
        date: row.date,
        score: row.score,
        note: null,
        tags: [],
        sub_scores: null,
        sleep_hours: null,
        special_event: null,
        garmin: null,
        health: null,
        weather: null,
        derived: null,
      });
      created++;
    }
    // Print progress every 10 rows
    if ((created + updated) % 10 === 0) {
      console.log(`  …${created + updated}/${parsed.length} (${created} new, ${updated} updated)`);
    }
  } catch (e) {
    failed++;
    failures.push({ row, error: e.message });
    if (failures.length <= 3) {
      console.error(`  ❌ ${row.date}: ${e.message.split('\n')[0]}`);
    }
  }
}

console.log('\n' + '─'.repeat(64));
console.log(`  Created: ${created}`);
console.log(`  Updated: ${updated}`);
console.log(`  Failed:  ${failed}`);
console.log(`  Skipped: ${skipped.length} (validation failures)`);
console.log('─'.repeat(64));

if (failed > 0) {
  console.log('\nFirst failures:');
  for (const f of failures.slice(0, 5)) {
    console.log(`  ${f.row.date} score=${f.row.score}`);
    console.log(`    ${f.error.split('\n').slice(0, 2).join('\n    ')}`);
  }
  process.exit(1);
}

console.log('\n✅ Sample data imported successfully.');
console.log('\nVerify via the Directus admin UI or:');
console.log('  curl -H "Authorization: Bearer $DIRECTUS_TOKEN" \\');
console.log('       "https://gevoelscore-backend.fly.dev/items/day_entries?aggregate[count]=*"');
