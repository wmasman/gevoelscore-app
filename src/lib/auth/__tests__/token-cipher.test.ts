import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { decryptToken, encryptToken, _resetKeyCacheForTests } from '../token-cipher';

// 32 bytes (64 hex chars) — `openssl rand -hex 32`. Deterministic fixture.
const KEY = '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef';

describe('token-cipher (AES-256-GCM)', () => {
  beforeEach(() => {
    process.env.SESSION_TOKEN_KEY = KEY;
    _resetKeyCacheForTests();
  });
  afterEach(() => {
    delete process.env.SESSION_TOKEN_KEY;
    _resetKeyCacheForTests();
  });

  it('round-trips a typical access token', () => {
    const plain = 'eyJhbGciOiJIUzI1NiJ9.eyJpZCI6ImFiYyJ9.signature-bytes-here';
    const encrypted = encryptToken(plain);
    expect(encrypted).not.toBe(plain);
    expect(encrypted.split('.')).toHaveLength(3);
    expect(decryptToken(encrypted)).toBe(plain);
  });

  it('produces a different ciphertext each call (IV must be random)', () => {
    const plain = 'token-x';
    const a = encryptToken(plain);
    const b = encryptToken(plain);
    expect(a).not.toBe(b);
    expect(decryptToken(a)).toBe(plain);
    expect(decryptToken(b)).toBe(plain);
  });

  it('handles legacy plaintext (no dot delimiters) by passthrough', () => {
    // 64-char base64url access tokens — what the migration starts with.
    const legacy = 'Lo4xvrJv5kTWk9Mmb7kbO5hdg65RS3PsRcyiCQZT63EpbGPXG7j_uQ79hxCBAXZi';
    expect(decryptToken(legacy)).toBe(legacy);
  });

  it('handles JWT shape (two dots, JSON header) by passthrough on decrypt failure', () => {
    // A plausible JWT — its first segment decodes to JSON not 12 bytes,
    // so we pass it through. (Decryption could also throw — caught.)
    const jwt =
      'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.abc';
    expect(decryptToken(jwt)).toBe(jwt);
  });

  // Deterministic flip: swap the FIRST char. Tampering the LAST char of a
  // base64url-encoded GCM tag (22 chars for 16 bytes) is flaky because the
  // last char carries only 2 actual data bits (the other 4 are padding);
  // an 'A' ↔ 'B' swap on that char can preserve the 2 data bits and
  // produce a byte-identical tag after decode. The first char always
  // encodes 6 real bits, so a swap there always changes the underlying
  // bytes.
  function flipFirstChar(s: string): string {
    const first = s.slice(0, 1);
    const next = first === 'A' ? 'B' : 'A';
    return next + s.slice(1);
  }

  it('returns the stored string verbatim when ciphertext is tampered (fail-closed at auth layer)', () => {
    const plain = 'token-y';
    const encrypted = encryptToken(plain);
    const [iv, ct, tag] = encrypted.split('.');
    const tampered = `${iv}.${flipFirstChar(ct!)}.${tag}`;
    const result = decryptToken(tampered);
    expect(result).toBe(tampered);
    expect(result).not.toBe(plain);
  });

  it('returns the stored string verbatim when auth-tag is tampered', () => {
    const plain = 'token-z';
    const encrypted = encryptToken(plain);
    const [iv, ct, tag] = encrypted.split('.');
    const tampered = `${iv}.${ct}.${flipFirstChar(tag!)}`;
    expect(decryptToken(tampered)).toBe(tampered);
  });

  it('without SESSION_TOKEN_KEY, encrypt + decrypt are no-ops (legacy / dev path)', () => {
    delete process.env.SESSION_TOKEN_KEY;
    _resetKeyCacheForTests();
    const plain = 'token-w';
    expect(encryptToken(plain)).toBe(plain);
    expect(decryptToken(plain)).toBe(plain);
  });

  it('throws on a wrong-shape key (fail loud rather than silently weak)', () => {
    process.env.SESSION_TOKEN_KEY = 'too-short';
    _resetKeyCacheForTests();
    expect(() => encryptToken('x')).toThrow(/SESSION_TOKEN_KEY/);
  });

  it('throws on non-hex characters in the key', () => {
    process.env.SESSION_TOKEN_KEY = 'z'.repeat(64);
    _resetKeyCacheForTests();
    expect(() => encryptToken('x')).toThrow(/non-hex/);
  });
});
