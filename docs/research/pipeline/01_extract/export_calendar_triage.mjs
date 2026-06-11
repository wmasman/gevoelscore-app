#!/usr/bin/env node
// export_calendar_triage.mjs
//
// Exports calendar events for a given year to a triage CSV, pre-filling
// keep_yn=n for any event whose normalised title appears in prior triage CSVs
// (so recurring "noise" events like "Zen", "W", "JM", "Turnen Tijmen" are
// auto-rejected and the user only triages the new stuff).
//
// Usage:
//   node docs/research/timeline/scripts/export_calendar_triage.mjs 2023
//
// Reads DIRECTUS_URL + DIRECTUS_TOKEN from .env.local (auto-loaded via
// --env-file). Output goes to docs/research/timeline/data/calendar_YYYY_triage.csv.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DATA_DIR = path.join(__dirname, '..', 'data');

const year = process.argv[2];
if (!year || !/^\d{4}$/.test(year)) {
  console.error('Usage: node export_calendar_triage.mjs <YEAR>');
  console.error('  e.g. node export_calendar_triage.mjs 2023');
  process.exit(1);
}

const url = process.env.DIRECTUS_URL;
const token = process.env.DIRECTUS_TOKEN;
if (!url || !token) {
  console.error('DIRECTUS_URL or DIRECTUS_TOKEN not set. Run with:');
  console.error('  node --env-file=.env.local docs/research/timeline/scripts/export_calendar_triage.mjs ' + year);
  process.exit(1);
}

// ---- 1) Collect rejected (keep_yn=n) titles from existing triage CSVs --------

function normaliseTitle(t) {
  if (!t) return '';
  return t
    .replace(/[\u{1F300}-\u{1FAFF}]/gu, '')   // emoji block
    .replace(/[\u{2600}-\u{27BF}]/gu, '')     // misc symbols + dingbats
    .replace(/\u{FE0F}/gu, '')                 // VS16
    .replace(/\s+/g, ' ')
    .trim()
    .toLowerCase();
}

function parseCSV(text) {
  const out = [];
  const lines = text.split(/\r?\n/);
  if (!lines.length) return out;
  const headers = parseCSVRow(lines[0]);
  for (let i = 1; i < lines.length; i++) {
    if (!lines[i]) continue;
    const cells = parseCSVRow(lines[i]);
    const row = {};
    headers.forEach((h, idx) => { row[h] = cells[idx] ?? ''; });
    out.push(row);
  }
  return out;
}
function parseCSVRow(line) {
  const out = [];
  let cur = '';
  let inQ = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (inQ) {
      if (c === '"' && line[i+1] === '"') { cur += '"'; i++; }
      else if (c === '"') { inQ = false; }
      else { cur += c; }
    } else {
      if (c === ',') { out.push(cur); cur = ''; }
      else if (c === '"') { inQ = true; }
      else { cur += c; }
    }
  }
  out.push(cur);
  return out;
}

const rejectedTitles = new Set();
const triageFiles = fs.readdirSync(DATA_DIR).filter(f => /^calendar_\d{4}_triage\.csv$/.test(f));
for (const f of triageFiles) {
  // Path comes from readdirSync against a fixed DATA_DIR filtered by a
  // strict regex — intentional research-script behaviour, not user input.
  // eslint-disable-next-line security/detect-non-literal-fs-filename
  const text = fs.readFileSync(path.join(DATA_DIR, f), 'utf8');
  const rows = parseCSV(text);
  for (const r of rows) {
    if ((r.keep_yn || '').trim().toLowerCase() === 'n') {
      rejectedTitles.add(normaliseTitle(r.title));
    }
  }
  console.log(`  loaded ${rows.length} rows from ${f} (running rejected count: ${rejectedTitles.size})`);
}
console.log(`Rejected-title set size: ${rejectedTitles.size} (from ${triageFiles.length} prior triage CSV(s))`);

// ---- 2) Query Directus for the requested year -------------------------------

const params = new URLSearchParams({
  'filter[start_at][_between]': `${year}-01-01T00:00:00,${year}-12-31T23:59:59`,
  'fields': 'start_at,end_at,title,all_day,location',
  'limit': '2000',
  'sort': 'start_at',
});
const res = await fetch(`${url}/items/calendar_events?${params}`, {
  headers: { Authorization: 'Bearer ' + token }
});
if (!res.ok) {
  console.error(`HTTP ${res.status} ${await res.text()}`);
  process.exit(1);
}
const json = await res.json();
if (json.errors) {
  console.error('Directus errors:', JSON.stringify(json.errors));
  process.exit(1);
}
const events = json.data;
console.log(`Fetched ${events.length} events for ${year}.`);

// ---- 3) Build CSV with pre-filled keep_yn=n for known-rejected titles -------

function csvCell(v) {
  if (v == null) return '';
  const s = String(v);
  if (s.includes(',') || s.includes('"') || s.includes('\n')) {
    return '"' + s.replace(/"/g, '""') + '"';
  }
  return s;
}

const headerRow = 'date_start,date_end,multi_day,title,location,keep_yn,cognitive_load,physical_load,emotional_load,notes';
const rows = [headerRow];
let nPrefilled = 0;
for (const e of events) {
  const s = (e.start_at || '').substring(0, 10);
  const en = (e.end_at || '').substring(0, 10);
  const multi = (s && en && s !== en) ? 'yes' : 'no';
  const t = e.title || '';
  const loc = e.location || '';
  const isRejected = rejectedTitles.has(normaliseTitle(t));
  if (isRejected) nPrefilled++;
  rows.push([
    csvCell(s),
    csvCell(en || s),
    csvCell(multi),
    csvCell(t),
    csvCell(loc),
    csvCell(isRejected ? 'n' : ''),
    '', '', '', '',
  ].join(','));
}

const out = path.join(DATA_DIR, `calendar_${year}_triage.csv`);
// Path is composed inside a fixed DATA_DIR with a sanitised year — intentional
// research-script behaviour, not user input.
// eslint-disable-next-line security/detect-non-literal-fs-filename
fs.writeFileSync(out, rows.join('\n'), 'utf8');
console.log(`\nWrote ${out}`);
console.log(`  ${events.length} total events`);
console.log(`  ${nPrefilled} pre-filled keep_yn=n (matched 2022 rejected titles)`);
console.log(`  ${events.length - nPrefilled} rows awaiting your triage`);
