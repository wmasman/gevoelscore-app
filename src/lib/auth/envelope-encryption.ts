// AES-GCM envelope encryption helper for refresh tokens at rest.
// Calendar-binding feature, v1.6 (step-0). See docs/features/calendar-binding/
// step-0-data-model-and-provider.md AC0.8-AC0.13.
//
// Output format: `v1.<base64-iv>.<base64-ciphertext>.<base64-authtag>`.
// The `v1` prefix supports future algorithm rotation without breaking
// existing rows.
//
// KEK (key-encryption key): 32-byte base64-encoded secret read from
// the `CALENDAR_KEK` Fly secret at the call site. Tests inject a test
// KEK directly. The KEK is the AES-256 key; we use it directly as the
// data encryption key for the refresh token. (True envelope encryption
// — per-row DEK encrypted by the KEK — is a future-rotation concern;
// v1.6 ships single-key encryption with the v1 prefix as the
// versioning hook.)

import {
  createCipheriv,
  createDecipheriv,
  randomBytes,
} from 'node:crypto';

const VERSION = 'v1';
const IV_LENGTH_BYTES = 12; // 96-bit IV, AES-GCM recommended length
const KEY_LENGTH_BYTES = 32; // AES-256
const AUTH_TAG_LENGTH_BYTES = 16;

function decodeKek(kekBase64: string): Buffer {
  const buf = Buffer.from(kekBase64, 'base64');
  if (buf.length !== KEY_LENGTH_BYTES) {
    throw new Error(
      `KEK must decode to ${KEY_LENGTH_BYTES} bytes (got ${buf.length})`,
    );
  }
  return buf;
}

export function encrypt(plaintext: string, kekBase64: string): string {
  const key = decodeKek(kekBase64);
  const iv = randomBytes(IV_LENGTH_BYTES);

  const cipher = createCipheriv('aes-256-gcm', key, iv);
  const ciphertext = Buffer.concat([
    cipher.update(plaintext, 'utf8'),
    cipher.final(),
  ]);
  const authTag = cipher.getAuthTag();

  return [
    VERSION,
    iv.toString('base64'),
    ciphertext.toString('base64'),
    authTag.toString('base64'),
  ].join('.');
}

export function decrypt(ciphertext: string, kekBase64: string): string {
  const parts = ciphertext.split('.');
  if (parts.length !== 4) {
    throw new Error(
      `malformed ciphertext: expected 4 dot-separated segments, got ${parts.length}`,
    );
  }
  const [version, ivB64, ctB64, authTagB64] = parts as [
    string,
    string,
    string,
    string,
  ];
  if (version !== VERSION) {
    throw new Error(`unsupported version: ${version}`);
  }

  const key = decodeKek(kekBase64);
  const iv = Buffer.from(ivB64, 'base64');
  const ct = Buffer.from(ctB64, 'base64');
  const authTag = Buffer.from(authTagB64, 'base64');

  if (authTag.length !== AUTH_TAG_LENGTH_BYTES) {
    throw new Error(
      `malformed authTag: expected ${AUTH_TAG_LENGTH_BYTES} bytes, got ${authTag.length}`,
    );
  }

  const decipher = createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(authTag);

  const plaintext = Buffer.concat([decipher.update(ct), decipher.final()]);
  return plaintext.toString('utf8');
}
