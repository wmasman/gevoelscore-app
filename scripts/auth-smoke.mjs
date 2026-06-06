// Auth smoke against the deployed frontend. Exercises the full
// login → authenticated read → logout → 401-post-logout chain.
// Unit tests cover each piece in isolation; this script catches
// integration regressions that unit tests can't (e.g. a WILLEM_USER_ID
// gate value that locks out the real user, a Fly secret that didn't
// propagate, a scoped-token permission gap).
//
// Run BEFORE pushing any auth-touching change, and after any Fly
// secret swap that involves DIRECTUS_TOKEN / SESSION_TOKEN_KEY /
// WILLEM_USER_ID. ~3 s round-trip against prod.
//
// Credentials are read from .env.local (gitignored, never committed):
//   WILLEM_EMAIL=user@example.com
//   WILLEM_PASSWORD=<your password>
//
// Run via the PowerShell wrapper that sources .env.local:
//   powershell -ExecutionPolicy Bypass -File scripts/run-auth-smoke.ps1
//
// Or directly if env is already in your shell:
//   node scripts/auth-smoke.mjs

import process from 'node:process';

const BASE = process.env.BASE_URL || 'https://gevoelscore-frontend.fly.dev';
const EMAIL = process.env.WILLEM_EMAIL;
const PASSWORD = process.env.WILLEM_PASSWORD;

if (!EMAIL || !PASSWORD) {
  console.error('Missing WILLEM_EMAIL or WILLEM_PASSWORD env var.');
  console.error('Add to .env.local then run scripts/run-auth-smoke.ps1.');
  process.exit(2);
}

const origin = BASE;
let cookieJar = '';

function extractSessionCookie(res) {
  const headers = res.headers.getSetCookie?.() ?? [];
  for (const sc of headers) {
    const [pair] = sc.split(';');
    const [name, value] = pair.split('=');
    if (name?.trim() === 'gs_session') return `gs_session=${value ?? ''}`;
  }
  return '';
}

let allPassed = true;
function step(label, ok, detail) {
  const mark = ok ? '✓' : '✗';
  console.log(`  ${mark} ${label}${detail ? `\n     ${detail}` : ''}`);
  if (!ok) allPassed = false;
}

console.log(`Auth smoke → ${BASE}`);
console.log(`User       → ${EMAIL}`);
console.log('');

// 1) Login
const loginRes = await fetch(`${BASE}/api/auth/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', Origin: origin },
  body: JSON.stringify({ email: EMAIL, password: PASSWORD }),
});
const loginBody = await loginRes.json().catch(() => ({}));

if (loginBody.requires_otp === true) {
  console.log('  ! Login returned requires_otp:true — 2FA is on for this account.');
  console.log('    This smoke does not handle OTP (no TOTP secret available here).');
  console.log('    Either disable 2FA for the smoke user, or extend this script.');
  process.exit(3);
}

step(
  'POST /api/auth/login',
  loginRes.status === 200 && loginBody.ok === true,
  `status=${loginRes.status} body=${JSON.stringify(loginBody)}`,
);

cookieJar = extractSessionCookie(loginRes);
step('Set-Cookie gs_session is non-empty', cookieJar.length > 12, `cookie='${cookieJar.slice(0, 20)}...'`);

if (!cookieJar) {
  console.log('\n✗ AUTH SMOKE FAIL — no session cookie, aborting remaining checks.');
  process.exit(1);
}

// 2) Authenticated read
const readRes = await fetch(`${BASE}/api/day-entries/today`, {
  headers: { Cookie: cookieJar, Origin: origin },
});
step('GET /api/day-entries/today returns 200 with cookie', readRes.status === 200, `status=${readRes.status}`);

// 3) Logout
const logoutRes = await fetch(`${BASE}/api/auth/logout`, {
  method: 'POST',
  headers: { Cookie: cookieJar, Origin: origin },
});
step('POST /api/auth/logout returns 200', logoutRes.status === 200, `status=${logoutRes.status}`);

const clearingSetCookies = logoutRes.headers.getSetCookie?.() ?? [];
const hasClearingCookie = clearingSetCookies.some(
  (c) => c.startsWith('gs_session=') && /(Max-Age=0|Expires=Thu, 01 Jan 1970)/i.test(c),
);
step('Logout clears gs_session cookie', hasClearingCookie, `set-cookies=${clearingSetCookies.length}`);

// 4) Post-logout the same cookie value should be rejected
const reReadRes = await fetch(`${BASE}/api/day-entries/today`, {
  headers: { Cookie: cookieJar, Origin: origin },
});
step(
  'GET /api/day-entries/today returns 401 after logout',
  reReadRes.status === 401,
  `status=${reReadRes.status}`,
);

console.log('');
if (allPassed) {
  console.log('✓ AUTH SMOKE PASS — login → read → logout → 401 chain intact.');
  process.exit(0);
} else {
  console.log('✗ AUTH SMOKE FAIL — see above. Investigate before pushing auth changes.');
  process.exit(1);
}
