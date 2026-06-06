// Pulls all day_entries (date, score, note) from Directus.
// Includes notes this time — that's the new data source.
//
// Run:
//   powershell -ExecutionPolicy Bypass -File scripts/run-directus-script.ps1 `
//     -Script docs/research/notes/01-language-around-crashes/fetch_day_entries_with_notes.mjs

import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { directusRequest, URL } from '../../../../directus/scripts/lib/directus-request.mjs';

const ANALYSIS_START = '2022-09-03';
const HERE = dirname(fileURLToPath(import.meta.url));
const OUT_JSON = join(HERE, 'day_entries_with_notes.json');

console.log(`Target: ${URL}`);
const PAGE_SIZE = 500;
let entries = [];
let page = 1;
while (true) {
  const r = await directusRequest(
    `/items/day_entries?fields=id,date,score,note&sort=date&limit=${PAGE_SIZE}&page=${page}&filter[date][_gte]=${ANALYSIS_START}`,
  );
  if (!r.data.length) break;
  entries = entries.concat(r.data);
  if (r.data.length < PAGE_SIZE) break;
  page++;
}

writeFileSync(OUT_JSON, JSON.stringify(entries, null, 2), 'utf-8');
const withNote = entries.filter((e) => e.note && e.note.trim()).length;
console.log(`fetched ${entries.length} entries  (${withNote} with non-empty note) -> ${OUT_JSON}`);
