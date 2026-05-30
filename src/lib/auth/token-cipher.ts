// AES-256-GCM at-rest encryption for Directus access + refresh tokens
// stored in the `frontend_sessions` collection (audit S-H2, 2026-05-30).
//
// Lifecycle:
//   - On write (create / update), `encryptToken(plain)` produces a
//     URL-safe `<iv>.<ciphertext>.<authTag>` triple-segment string.
//   - On read (peek / get), `decryptToken(stored)` reverses it.
//   - Legacy plaintext rows (no dots in the value) pass through
//     untouched so the migration is zero-downtime: as the Directus
//     refresh-token rotation cycles them, they get re-encrypted.
//
// Key handling:
//   - `SESSION_TOKEN_KEY` env var, 32 bytes encoded as 64 hex chars
//     (`openssl rand -hex 32`). Stored as a Fly secret SEPARATE from
//     `DIRECTUS_TOKEN` — the encryption key never leaves the frontend
//     machine, and a Directus DB dump alone does not yield plaintext.
//   - If the key is missing or wrong shape, encryption is a no-op
//     (plaintext passthrough) and a one-time console warning fires.
//     This keeps dev / first-deploy unblocked; production must set
//     the secret. Lint and the deploy runbook surface the gap.
//
// Tamper protection:
//   - GCM provides integrity. Any flip in iv / ciphertext / tag
//     causes `decipher.final()` to throw with `Unsupported state` /
//     auth-tag mismatch. The decrypt path catches and returns the
//     stored value verbatim — the caller (session store) will pass
//     a meaningless string to Directus, refresh fails, session row
//     is evicted, user re-logs in. Fail-closed at the auth layer.
//
// Why not store iv / authTag in separate columns:
//   - One column rotates atomically with the value, so a partial
//     write can't desync. Cheap to migrate (the existing `text` field
//     just holds a slightly longer string).

import { createCipheriv, createDecipheriv, randomBytes } from 'node:crypto';

const ALGO = 'aes-256-gcm';
const IV_BYTES = 12;
const KEY_BYTES = 32;
const SEPARATOR = '.';

function loadKey(): Buffer | null {
  const hex = process.env.SESSION_TOKEN_KEY;
  if (typeof hex !== 'string' || hex.length === 0) return null;
  if (hex.length !== KEY_BYTES * 2) {
    // Wrong shape — fail loud rather than silently using a short key.
    throw new Error(
      `SESSION_TOKEN_KEY must be ${KEY_BYTES * 2} hex chars (${KEY_BYTES} bytes); got ${hex.length}.`,
    );
  }
  const buf = Buffer.from(hex, 'hex');
  if (buf.length !== KEY_BYTES) {
    throw new Error('SESSION_TOKEN_KEY contains non-hex characters.');
  }
  return buf;
}

// Cache the key per process. Re-loading on every call wastes cycles;
// process restarts pick up env changes.
let keyCache: Buffer | null | undefined;
function key(): Buffer | null {
  if (keyCache === undefined) {
    keyCache = loadKey();
    if (keyCache === null) {
      console.warn(
        '[auth] SESSION_TOKEN_KEY not set — frontend_sessions tokens will be stored in plaintext. Set the Fly secret to enable at-rest encryption (S-H2).',
      );
    }
  }
  return keyCache;
}

export function encryptToken(plain: string): string {
  const k = key();
  if (k === null) return plain;

  const iv = randomBytes(IV_BYTES);
  const cipher = createCipheriv(ALGO, k, iv);
  const ciphertext = Buffer.concat([cipher.update(plain, 'utf8'), cipher.final()]);
  const authTag = cipher.getAuthTag();
  return [
    iv.toString('base64url'),
    ciphertext.toString('base64url'),
    authTag.toString('base64url'),
  ].join(SEPARATOR);
}

export function decryptToken(stored: string): string {
  const k = key();
  if (k === null) return stored;

  // Legacy plaintext rows have no dots. Pass through untouched.
  // Format ambiguity is acceptable here: Directus access tokens are
  // JWTs whose three segments are dot-separated. A JWT has TWO dots
  // (header.payload.signature) — exactly our delimiter count. To
  // disambiguate, also check the first segment decodes as exactly
  // IV_BYTES of base64url (16-char string), which a JWT header never
  // does (it decodes as JSON).
  const parts = stored.split(SEPARATOR);
  if (parts.length !== 3) return stored;
  const [ivPart, ctPart, tagPart] = parts as [string, string, string];
  if (ivPart.length !== Math.ceil((IV_BYTES * 4) / 3)) return stored;

  try {
    const iv = Buffer.from(ivPart, 'base64url');
    if (iv.length !== IV_BYTES) return stored;
    const ciphertext = Buffer.from(ctPart, 'base64url');
    const authTag = Buffer.from(tagPart, 'base64url');
    const decipher = createDecipheriv(ALGO, k, iv);
    decipher.setAuthTag(authTag);
    const out = Buffer.concat([decipher.update(ciphertext), decipher.final()]);
    return out.toString('utf8');
  } catch {
    // Tampered, key rotated, or merely a JWT that happened to share
    // the shape. Returning the stored string verbatim sends it through
    // to Directus, which will reject it; the session row is then
    // evicted and the user re-logs in. Fail-closed at the auth layer
    // rather than throwing 500s up the route handler stack.
    return stored;
  }
}

// Test-only: reset the cached key so a test can swap SESSION_TOKEN_KEY
// between scenarios. Not exported via index; only consumed in tests.
export function _resetKeyCacheForTests(): void {
  keyCache = undefined;
}
