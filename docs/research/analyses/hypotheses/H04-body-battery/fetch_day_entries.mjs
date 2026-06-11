// H04 day_entries fetcher — copy of H01/H02/H03's.

import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { directusRequest, URL } from '../../../../../directus/scripts/lib/directus-request.mjs';

const ANALYSIS_START = '2022-09-03';
const HERE = dirname(fileURLToPath(import.meta.url));
const OUT_CSV = join(HERE, 'day_entries.csv');

console.log(`Target: ${URL}`);
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

const lines = ['date,score'];
for (const e of entries) lines.push(`${e.date},${e.score ?? ''}`);
writeFileSync(OUT_CSV, lines.join('\n') + '\n', 'utf-8');
console.log(`wrote ${entries.length} rows -> ${OUT_CSV}`);
