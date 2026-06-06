// Preflight: count crash_v1 episodes under the locked definition.
// Runs before any H01-H05 test.py so we know whether the batch is powered.
//
// crash_v1 = run of >= 2 consecutive days in personal bottom 15% of scores,
// episodes within 3 days merged into one (dated to first day of first run).
//
// READ-ONLY. Run via:
//   powershell -ExecutionPolicy Bypass -File scripts/run-directus-script.ps1 `
//     -Script docs/research/garmin/hypotheses/00-crash_v1-counts/count.mjs

import { directusRequest, URL } from '../../../../../directus/scripts/lib/directus-request.mjs';

const ANALYSIS_START = '2022-09-03';
const TRAIN_END = '2023-12-31';
const VALIDATE_END = '2026-06-05';
// crash_v1 (locked 2026-06-05, revised same day after preflight):
//   score <= LOW_THRESHOLD for >= MIN_RUN_DAYS consecutive days,
//   episodes within MERGE_WITHIN_DAYS merged into one.
// See registry.md §2.
const LOW_THRESHOLD = 3;
const MIN_RUN_DAYS = 2;
const MERGE_WITHIN_DAYS = 3;

console.log(`Target: ${URL}\n`);

// ---------- Fetch all day_entries in window ----------
const PAGE_SIZE = 1000;
let entries = [];
let page = 1;
while (true) {
  const r = await directusRequest(
    `/items/day_entries?fields=date,score&sort=date&limit=${PAGE_SIZE}&page=${page}&filter[date][_gte]=${ANALYSIS_START}`,
  );
  if (!r.data.length) break;
  entries = entries.concat(r.data);
  if (r.data.length < PAGE_SIZE) break;
  page++;
}
const withScore = entries.filter((e) => e.score !== null && e.score !== undefined);
console.log(`day_entries fetched: ${entries.length}  (with score: ${withScore.length})`);

// ---------- Score distribution ----------
const distMap = new Map();
for (const e of withScore) distMap.set(e.score, (distMap.get(e.score) || 0) + 1);
const distSorted = [...distMap.entries()].sort((a, b) => a[0] - b[0]);
const maxCount = Math.max(...distMap.values());
console.log('\n--- score distribution ---');
for (const [score, n] of distSorted) {
  const bar = '#'.repeat(Math.round((n * 50) / maxCount));
  console.log(`  ${score}: ${n.toString().padStart(4)}  ${bar}`);
}

// ---------- Apply absolute threshold ----------
const inLow = withScore.filter((e) => e.score <= LOW_THRESHOLD).length;
console.log(
  `\ncrash_v1 low-day rule: score <= ${LOW_THRESHOLD}  (covers ${inLow} entries = ${((100 * inLow) / withScore.length).toFixed(1)}%)`,
);

// ---------- Build day map and find low-day runs ----------
const dayMap = new Map();
for (const e of withScore) dayMap.set(e.date, { score: e.score, low: e.score <= LOW_THRESHOLD });

function dayDiff(a, b) {
  return Math.round((new Date(b) - new Date(a)) / 86400000);
}

const datesSorted = [...dayMap.keys()].sort();
const runs = [];
let cur = null;
for (const d of datesSorted) {
  const isLow = dayMap.get(d).low;
  if (!isLow) {
    if (cur && cur.days >= MIN_RUN_DAYS) runs.push(cur);
    cur = null;
    continue;
  }
  if (!cur) {
    cur = { start: d, end: d, days: 1 };
    continue;
  }
  const gap = dayDiff(cur.end, d);
  if (gap === 1) {
    cur.end = d;
    cur.days += 1;
  } else {
    if (cur.days >= MIN_RUN_DAYS) runs.push(cur);
    cur = { start: d, end: d, days: 1 };
  }
}
if (cur && cur.days >= MIN_RUN_DAYS) runs.push(cur);

console.log(`\nruns of >= ${MIN_RUN_DAYS} consecutive low days: ${runs.length}`);

// ---------- Merge runs within 3 days ----------
const merged = [];
for (const r of runs) {
  const last = merged[merged.length - 1];
  if (last && dayDiff(last.end, r.start) <= MERGE_WITHIN_DAYS) {
    last.end = r.end;
    last.days += r.days;
    last.runsMerged = (last.runsMerged || 1) + 1;
  } else {
    merged.push({ ...r, runsMerged: 1 });
  }
}
console.log(`crash_v1 episodes after merging within ${MERGE_WITHIN_DAYS} days: ${merged.length}`);

// ---------- Episode span distribution ----------
const spanBuckets = new Map([
  ['2 days', 0],
  ['3-4 days', 0],
  ['5-7 days', 0],
  ['8-14 days', 0],
  ['15+ days', 0],
]);
for (const ep of merged) {
  const span = dayDiff(ep.start, ep.end) + 1;
  const b =
    span <= 2 ? '2 days'
      : span <= 4 ? '3-4 days'
      : span <= 7 ? '5-7 days'
      : span <= 14 ? '8-14 days'
      : '15+ days';
  spanBuckets.set(b, spanBuckets.get(b) + 1);
}
console.log('\n--- episode span (calendar days, first low day to last low day) ---');
for (const [b, n] of spanBuckets) console.log(`  ${b}: ${n}`);

// ---------- Train / validate split ----------
const trainEps = merged.filter((ep) => ep.start <= TRAIN_END);
const valEps = merged.filter((ep) => ep.start > TRAIN_END && ep.start <= VALIDATE_END);
console.log(`\n--- train / validate ---`);
console.log(`  train    (${ANALYSIS_START} -> ${TRAIN_END}): ${trainEps.length} episodes`);
console.log(`  validate (${TRAIN_END}+1 -> ${VALIDATE_END}): ${valEps.length} episodes`);

if (merged.length > 0) {
  console.log(`\nfirst episode: ${merged[0].start}`);
  console.log(`last episode:  ${merged[merged.length - 1].start}`);
}

// ---------- Year distribution (drift sanity check) ----------
const yearMap = new Map();
for (const ep of merged) {
  const y = ep.start.slice(0, 4);
  yearMap.set(y, (yearMap.get(y) || 0) + 1);
}
console.log('\n--- episodes per year (to spot drift in tracking discipline) ---');
for (const [y, n] of [...yearMap.entries()].sort()) console.log(`  ${y}: ${n}`);

// ---------- Verdict ----------
console.log('\n--- preflight verdict ---');
if (trainEps.length >= 10 && valEps.length >= 10) {
  console.log(`OK: both windows have >= 10 episodes. H01-H05 are powered.`);
} else if (merged.length >= 15) {
  console.log(`MIXED: ${merged.length} total but split is uneven (train=${trainEps.length}, validate=${valEps.length}).`);
  console.log(`Consider adjusting the train/validate cutoff before running H01.`);
} else {
  console.log(`WARN: only ${merged.length} episodes total. H01-H05 likely underpowered.`);
  console.log(`Recommend promoting crash_v2 (notes-based labels) before running predictive hypotheses.`);
}
