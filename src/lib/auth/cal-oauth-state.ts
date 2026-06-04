// OAuth state cookie for the Google Calendar connect flow.
// Calendar-binding feature, step-1 Phase 1.C.
//
// The state is a random 32-byte value. The cookie + the URL state param
// must match on callback. Cookie is httpOnly + Secure + SameSite=Lax
// (Lax is required so the cookie travels on the OAuth redirect-back from
// Google; Strict would block first-party cross-site GET cookies).
//
// 10-minute Max-Age — the OAuth consent flow is interactive but should
// not legitimately take longer than 10 minutes.
//
// No HMAC signing: httpOnly means an attacker can't read or forge the
// cookie from JS; the equality check against the URL state param is the
// CSRF protection.

import * as crypto from 'node:crypto';

export const STATE_COOKIE_NAME = 'cal_oauth_state';
export const STATE_COOKIE_MAX_AGE_S = 600;
const STATE_BYTES = 32;

export function generateOAuthState(): string {
  return crypto.randomBytes(STATE_BYTES).toString('base64url');
}

export function buildStateCookie(state: string): string {
  return [
    `${STATE_COOKIE_NAME}=${state}`,
    'HttpOnly',
    'Secure',
    'SameSite=Lax',
    'Path=/',
    `Max-Age=${STATE_COOKIE_MAX_AGE_S}`,
  ].join('; ');
}

export function clearStateCookie(): string {
  return [
    `${STATE_COOKIE_NAME}=`,
    'HttpOnly',
    'Secure',
    'SameSite=Lax',
    'Path=/',
    'Max-Age=0',
  ].join('; ');
}

export function parseStateCookie(header: string | null): string | null {
  if (!header) return null;
  for (const raw of header.split(';')) {
    const [name, ...rest] = raw.trim().split('=');
    if (name === STATE_COOKIE_NAME) {
      const value = rest.join('=');
      return value.length > 0 ? value : null;
    }
  }
  return null;
}

export function statesMatch(cookieValue: string, urlValue: string): boolean {
  if (cookieValue.length !== urlValue.length) return false;
  // Constant-time compare to thwart timing oracles.
  try {
    return crypto.timingSafeEqual(
      Buffer.from(cookieValue),
      Buffer.from(urlValue),
    );
  } catch {
    return false;
  }
}
