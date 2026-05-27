// Seeds the v1 Project entities for ongoing interventions identified during
// the real-history analysis. Idempotent by project name (skip if exists).
//
// These dates come from:
//   - the user's brief (the active interventies list)
//   - the analyze-notes.mjs first-mention output
//   - direct user input (see 2026-05-27 conversation about CPAP / Citalopram dates)

import { banner, directusRequest } from './lib/directus-request.mjs';

banner('seed-projects');

const PROJECTS = [
  {
    name: 'Citalopram',
    type: 'medicatie',
    start_date: '2024-04-09',
    end_date: null,
    status: 'active',
    description: 'SSRI. Tapering since 2026-03-20 (30mg → 20mg → 10mg → 8mg druppels).',
  },
  {
    name: 'CPAP',
    type: 'therapie',
    start_date: '2024-01-10',
    end_date: '2024-04-16',
    status: 'completed',
    description: 'Slaapapneu apparaat. Gestopt na ~3 maanden — aanpassing was te zwaar.',
  },
  {
    name: 'Naproxen',
    type: 'medicatie',
    start_date: '2025-03-27',
    end_date: null,
    status: 'active',
    description: 'Pijnstiller, op-verzoek-basis voor hoofdpijn.',
  },
  {
    name: 'Breinvoeding',
    type: 'therapie',
    start_date: '2026-05-01',
    end_date: null,
    status: 'active',
    description: 'Therapie traject, ~6 sessies.',
  },
  {
    name: 'HeartMath',
    type: 'oefening',
    start_date: '2026-05-01',
    end_date: null,
    status: 'active',
    description: 'HRV / coherence ademhalingsoefening, dagelijks. Onderdeel van Breinvoeding traject.',
  },
];

const existing = await directusRequest('/items/projects?limit=-1&fields=id,name');
const existingByName = new Map((existing.data ?? []).map((p) => [p.name.toLowerCase(), p]));

let created = 0;
let skipped = 0;
let failed = 0;

for (const p of PROJECTS) {
  if (existingByName.has(p.name.toLowerCase())) {
    skipped++;
    console.log(`  ⏩ ${p.name.padEnd(15)} already exists`);
    continue;
  }
  try {
    const r = await directusRequest('/items/projects', 'POST', p);
    console.log(`  ➕ ${p.name.padEnd(15)} ${p.start_date} → ${p.end_date ?? 'ongoing'.padEnd(10)}  type=${p.type.padEnd(10)} status=${p.status}`);
    created++;
  } catch (e) {
    failed++;
    console.error(`  ❌ ${p.name}: ${e.message.split('\n')[0]}`);
  }
}

console.log('\n' + '─'.repeat(64));
console.log(`  Created: ${created}`);
console.log(`  Skipped: ${skipped}`);
console.log(`  Failed:  ${failed}`);
console.log('─'.repeat(64));
if (failed > 0) process.exit(1);
console.log('\n✅ Projects seeded.\n');
