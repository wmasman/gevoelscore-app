// Imports the user's real Gevoel-sheet history from private/real-history.csv
// into the gevoelscore-backend Directus instance, complete with:
//   - date + score (validated against the v1 rules)
//   - cleaned note (multi-column trailing content joined with \n\n)
//   - tag_ids[] populated by matching the note against lib/tag-patterns.mjs
//
// Defaults to DRY-RUN. Pass --commit to actually write.
//
// Idempotent: upsert by date. Re-running rewrites existing rows.

import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { banner, directusRequest } from './lib/directus-request.mjs';
import { matchTags } from './lib/tag-patterns.mjs';

const COMMIT = process.argv.includes('--commit');
const CSV_PATH = resolve(process.cwd(), 'private/real-history.csv');

banner(`import-real-history (${COMMIT ? 'COMMIT' : 'DRY-RUN'})`);
console.log(`  Source: ${CSV_PATH}`);
console.log(`  Mode:   ${COMMIT ? '✏️  writing to Directus' : '🔍 dry-run'}`);
console.log();

// ---------------------------------------------------------------------------
// CSV parser
// ---------------------------------------------------------------------------

function parseCsvRow(line) {
  const cells = [];
  let i = 0;
  const len = line.length;
  while (i < len) {
    const ch = line.charAt(i);
    if (ch === '"') {
      i++;
      let v = '';
      while (i < len) {
        const c = line.charAt(i);
        if (c === '"') {
          if (line.charAt(i + 1) === '"') { v += '"'; i += 2; }
          else { i++; break; }
        } else { v += c; i++; }
      }
      cells.push(v);
      if (line.charAt(i) === ',') i++;
    } else {
      let v = '';
      while (i < len && line.charAt(i) !== ',') { v += line.charAt(i); i++; }
      cells.push(v);
      if (line.charAt(i) === ',') i++;
    }
  }
  return cells;
}

function dutchToIso(s) {
  const m = /^(\d{1,2})-(\d{1,2})-(\d{4})$/.exec(s.trim());
  if (!m) return null;
  return `${m[3]}-${m[2].padStart(2, '0')}-${m[1].padStart(2, '0')}`;
}

function todayIsoLocal() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

const TODAY = todayIsoLocal();

// ---------------------------------------------------------------------------
// Fetch Tag label → UUID map from Directus
// ---------------------------------------------------------------------------

console.log('  Fetching Tag UUIDs from Directus...');
const tagResp = await directusRequest('/items/tags?limit=-1&fields=id,label,category');
const labelToId = new Map();
for (const t of tagResp.data ?? []) {
  labelToId.set(t.label, t.id);
}
console.log(`  ${labelToId.size} tags loaded into UUID map.\n`);

// ---------------------------------------------------------------------------
// Read CSV
// ---------------------------------------------------------------------------

let raw;
try {
  raw = await readFile(CSV_PATH, 'utf8');
} catch (e) {
  console.error(`❌ Could not read ${CSV_PATH}\n   ${e.message}\n`);
  process.exit(1);
}

const dataLines = raw.replace(/^﻿/, '').split(/\r\n|\n/).slice(1);

// ---------------------------------------------------------------------------
// Validate + parse + tag-match every row
// ---------------------------------------------------------------------------

const valid = [];          // { rowIndex, date, score, note, tagLabels, tagIds }
const skipEmpty = [];
const skipDuplicate = [];
const invalid = [];
const seenDates = new Set();
const unknownTagLabels = new Set();

for (let i = 0; i < dataLines.length; i++) {
  const line = dataLines[i];
  const rowIndex = i + 2; // 1-based + header offset

  if (!line.trim()) continue;

  const cells = parseCsvRow(line);
  if (cells.length < 2) {
    invalid.push({ rowIndex, reason: 'wrong_column_count', raw: line });
    continue;
  }

  const dateRaw = (cells[0] ?? '').trim();
  const scoreRaw = (cells[1] ?? '').trim();
  const noteParts = cells.slice(2).map((c) => c.trim()).filter((c) => c.length > 0);

  if (scoreRaw === '') {
    skipEmpty.push({ rowIndex, date: dateRaw });
    continue;
  }

  const iso = dutchToIso(dateRaw);
  if (!iso) {
    invalid.push({ rowIndex, reason: 'invalid_date_format', raw: line });
    continue;
  }
  const [y, mo, d] = iso.split('-').map(Number);
  const reconstructed = new Date(y, mo - 1, d);
  if (
    reconstructed.getFullYear() !== y ||
    reconstructed.getMonth() !== mo - 1 ||
    reconstructed.getDate() !== d
  ) {
    invalid.push({ rowIndex, reason: 'invalid_calendar_date', raw: line });
    continue;
  }
  if (iso > TODAY) {
    invalid.push({ rowIndex, reason: 'future_date', raw: line });
    continue;
  }

  const scoreNum = Number(scoreRaw);
  if (
    !Number.isInteger(scoreNum) ||
    Number.isNaN(scoreNum) ||
    scoreNum < 1 ||
    scoreNum > 10
  ) {
    invalid.push({ rowIndex, reason: 'invalid_score', raw: line });
    continue;
  }

  if (seenDates.has(iso)) {
    skipDuplicate.push({ rowIndex, date: iso });
    continue;
  }
  seenDates.add(iso);

  const noteCombined = noteParts.length === 0 ? null : noteParts.join('\n\n');
  const note = noteCombined && noteCombined.trim().length > 0 ? noteCombined.trim() : null;

  // Tag matching
  const tagLabels = matchTags(note ?? '');
  const tagIds = [];
  for (const label of tagLabels) {
    const id = labelToId.get(label);
    if (id) {
      tagIds.push(id);
    } else {
      unknownTagLabels.add(label);
    }
  }

  valid.push({ rowIndex, date: iso, score: scoreNum, note, tagLabels, tagIds });
}

// ---------------------------------------------------------------------------
// Report
// ---------------------------------------------------------------------------

console.log('═'.repeat(64));
console.log('  Parse + match results');
console.log('═'.repeat(64));
console.log(`  Valid:               ${valid.length}`);
console.log(`  Skipped (empty):     ${skipEmpty.length}  (future-prefilled blank rows)`);
console.log(`  Skipped (duplicate): ${skipDuplicate.length}  (second occurrence of a date)`);
console.log(`  Invalid:             ${invalid.length}`);
console.log();
console.log(`  Total tag-match events:    ${valid.reduce((s, r) => s + r.tagLabels.length, 0)}`);
console.log(`  Entries with ≥1 tag:       ${valid.filter((r) => r.tagLabels.length > 0).length} / ${valid.filter((r) => r.note).length} noted`);
console.log(`  Unknown tag labels (skipped): ${unknownTagLabels.size}`);
if (unknownTagLabels.size > 0) {
  console.log(`    → ${Array.from(unknownTagLabels).join(', ')}`);
  console.log(`    Run seed-tags.mjs to create these in Directus first.`);
}
console.log();

if (invalid.length > 0) {
  console.log('  Sample invalid rows:');
  for (const inv of invalid.slice(0, 10)) {
    console.log(`    row ${inv.rowIndex} (${inv.reason}): ${inv.raw.substring(0, 100)}…`);
  }
  console.log();
}

if (skipDuplicate.length > 0) {
  console.log('  Duplicate dates (first kept):');
  for (const d of skipDuplicate) console.log(`    row ${d.rowIndex}: ${d.date}`);
  console.log();
}

if (valid.length > 0) {
  console.log('  Sample (first 3 with tags):');
  let n = 0;
  for (const r of valid) {
    if (r.tagLabels.length === 0) continue;
    console.log(`    ${r.date}  score=${r.score}  tags=[${r.tagLabels.join(', ')}]`);
    n++;
    if (n >= 3) break;
  }
  console.log();
}

// ---------------------------------------------------------------------------
// Stop here if dry-run
// ---------------------------------------------------------------------------

if (!COMMIT) {
  console.log('🔍 DRY-RUN complete. Nothing written to Directus.');
  console.log(`   Re-run with --commit to upsert ${valid.length} rows.\n`);
  process.exit(0);
}

// ---------------------------------------------------------------------------
// Commit: upsert each row
// ---------------------------------------------------------------------------

console.log('═'.repeat(64));
console.log('  Writing to Directus...');
console.log('═'.repeat(64));

let created = 0;
let updated = 0;
let failed = 0;
const failures = [];

for (const row of valid) {
  try {
    const existing = await directusRequest(
      `/items/day_entries?filter[date][_eq]=${row.date}&fields=id&limit=1`,
    );
    // M2M payload: `tags: [{tags_id: <uuid>, source, confidence}, ...]`
    // REPLACES the full relation set on PATCH — Directus deletes existing
    // junction rows for this day_entry and re-creates them. Idempotent upsert
    // semantics. Source='note_pattern' marks these as auto-inferred from the
    // regex library — distinguishes them from user-chosen tags later.
    const tagsPayload = row.tagIds.map((id) => ({
      tags_id: id,
      source: 'note_pattern',
      confidence: 1.0,
    }));

    if (existing.data && existing.data.length > 0) {
      await directusRequest(`/items/day_entries/${existing.data[0].id}`, 'PATCH', {
        score: row.score,
        note: row.note,
        tags: tagsPayload,
      });
      updated++;
    } else {
      await directusRequest('/items/day_entries', 'POST', {
        date: row.date,
        score: row.score,
        note: row.note,
        tags: tagsPayload,
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
    if ((created + updated) % 100 === 0) {
      console.log(`  …${created + updated}/${valid.length} (${created} new, ${updated} updated)`);
    }
  } catch (e) {
    failed++;
    failures.push({ row, error: e.message });
    if (failures.length <= 5) {
      console.error(`  ❌ ${row.date}: ${e.message.split('\n')[0]}`);
    }
  }
}

console.log('\n' + '═'.repeat(64));
console.log(`  Created: ${created}`);
console.log(`  Updated: ${updated}`);
console.log(`  Failed:  ${failed}`);
console.log('═'.repeat(64));

if (failed > 0) process.exit(1);
console.log('\n✅ Import complete.\n');
