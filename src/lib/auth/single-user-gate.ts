// Single-user gate. The app is built for one user (Willem) until v1.5
// multi-user lands. Until then, this gate is the runtime enforcement
// of that contract: any successful Directus login whose user id does
// not match WILLEM_USER_ID is rejected before a session row is created.
//
// The contract is also encoded in the schema (day_entries has no
// user_created column — see audit finding S-H3) so a second user
// can't safely use the app today. This gate stops them from even
// getting past the login. After v1.5 adds per-user filtering, remove
// the gate (and remove the WILLEM_USER_ID Fly secret).
//
// Behaviour when WILLEM_USER_ID is unset: the gate is a no-op. Useful
// for tests + first-boot dev. Production sets the secret.

import { directusGetMe, directusLogout } from './directus-auth';

export async function passesSingleUserGate(
  accessToken: string,
  refreshToken: string,
): Promise<boolean> {
  const expected = process.env.WILLEM_USER_ID;
  if (!expected) return true; // gate disabled

  const me = await directusGetMe(accessToken);
  if (!me.ok) {
    // Network / Directus glitch right after a successful login.
    // Don't lock the user out for a transient failure; let them
    // through. The next request's getValidatedSession will retry.
    return true;
  }
  if (me.value.id === expected) return true;

  // Mismatch — a different user (or accidentally a second user)
  // successfully authenticated against Directus. Revoke the
  // just-issued refresh token so no half-state leaks into Directus's
  // session table, then return false. The caller maps to 401 /
  // invalid_credentials, the same response as a wrong-password
  // attempt — no signal to a probing attacker that they hit a real
  // account.
  await directusLogout(refreshToken).catch(() => {
    /* best-effort cleanup; even if logout fails the gate has already
       prevented a frontend_sessions row from being created. */
  });
  return false;
}
