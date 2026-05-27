// Reads private/real-history.csv, analyzes the notes using the shared
// pattern map at lib/tag-patterns.mjs, and reports:
//   - frequency of each candidate tag (organized by category)
//   - candidate projects/interventions (date ranges)
//   - sample notes that didn't match ANY tag (PII — console only)
//
// PURE READ. Does NOT write to Directus or to any persisted file in the repo.

import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { TAG_PATTERNS } from './lib/tag-patterns.mjs';

const CSV_PATH = resolve(process.cwd(), 'private/real-history.csv');

// ---------------------------------------------------------------------------
// CSV utils
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

// ---------------------------------------------------------------------------
// Read
// ---------------------------------------------------------------------------

const raw = await readFile(CSV_PATH, 'utf8');
const dataLines = raw.replace(/^﻿/, '').split(/\r\n|\n/).slice(1).filter((l) => l.trim());

const entries = [];
for (const line of dataLines) {
  const cells = parseCsvRow(line);
  if (cells.length < 2) continue;
  const date = dutchToIso(cells[0]);
  const scoreRaw = (cells[1] ?? '').trim();
  if (!date || scoreRaw === '') continue;
  const score = Number(scoreRaw);
  if (!Number.isInteger(score) || score < 1 || score > 10) continue;
  const noteParts = cells.slice(2).map((c) => c.trim()).filter((c) => c.length > 0);
  const note = noteParts.length > 0 ? noteParts.join('\n\n').trim() : null;
  entries.push({ date, score, note });
}

console.log(`Loaded ${entries.length} entries (${entries.filter((e) => e.note).length} with notes)\n`);

// ---------------------------------------------------------------------------
// Frequency analysis
// ---------------------------------------------------------------------------

const tagHits = new Map(); // label → { count, category }
const matchedEntries = new Set();

for (let idx = 0; idx < entries.length; idx++) {
  const e = entries[idx];
  if (!e.note) continue;
  for (const [category, candidates] of Object.entries(TAG_PATTERNS)) {
    for (const { label, patterns } of candidates) {
      if (patterns.some((p) => p.test(e.note))) {
        if (!tagHits.has(label)) tagHits.set(label, { count: 0, category });
        tagHits.get(label).count++;
        matchedEntries.add(idx);
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Print frequency table
// ---------------------------------------------------------------------------

console.log('═'.repeat(78));
console.log('  Tag frequency (uses lib/tag-patterns.mjs)');
console.log('═'.repeat(78));

const byCategory = {};
for (const [label, info] of tagHits) {
  (byCategory[info.category] ??= []).push({ label, count: info.count });
}

for (const cat of ['mentaal', 'fysiek', 'overall', 'activiteit', 'gebeurtenis', 'interventie']) {
  const tags = (byCategory[cat] ?? []).sort((a, b) => b.count - a.count);
  console.log(`\n── ${cat.toUpperCase()} ──`);
  for (const t of tags) {
    const bar = '█'.repeat(Math.min(40, Math.ceil(t.count / 5)));
    console.log(`  ${t.label.padEnd(28)} ${String(t.count).padStart(4)}  ${bar}`);
  }
}

// ---------------------------------------------------------------------------
// Project candidates
// ---------------------------------------------------------------------------

console.log('\n' + '═'.repeat(78));
console.log('  Project candidates — first ↔ last mention');
console.log('═'.repeat(78));

for (const { label, patterns } of TAG_PATTERNS.interventie) {
  const hits = entries.filter((e) => e.note && patterns.some((p) => p.test(e.note)));
  if (hits.length === 0) continue;
  console.log(`  ${label.padEnd(25)} ${hits[0].date} → ${hits[hits.length - 1].date}  (${hits.length} days)`);
}

// ---------------------------------------------------------------------------
// Summary + unmatched sample
// ---------------------------------------------------------------------------

const totalNoted = entries.filter((e) => e.note).length;
const unmatched = entries.filter((e, idx) => e.note && !matchedEntries.has(idx));

console.log('\n' + '═'.repeat(78));
console.log('  Summary');
console.log('═'.repeat(78));
console.log(`  Entries with notes:     ${totalNoted}`);
console.log(`  Matched ≥1 tag:         ${matchedEntries.size}  (${Math.round((matchedEntries.size / totalNoted) * 100)}%)`);
console.log(`  Unmatched:              ${unmatched.length}  (${Math.round((unmatched.length / totalNoted) * 100)}%)`);
console.log(`  Distinct tags hit:      ${tagHits.size}`);
console.log(`  Total tag-match events: ${Array.from(tagHits.values()).reduce((s, t) => s + t.count, 0)}`);

if (process.argv.includes('--show-unmatched')) {
  console.log('\nUnmatched samples (first 10):');
  for (const e of unmatched.slice(0, 10)) {
    const short = e.note.length > 120 ? e.note.slice(0, 120) + '…' : e.note;
    console.log(`  ${e.date}  s=${e.score}  "${short}"`);
  }
}
