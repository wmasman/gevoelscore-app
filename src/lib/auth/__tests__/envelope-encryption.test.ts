// Step-0 AC0.8-AC0.13: AES-GCM envelope encryption helper.
// Round-trip + tamper detection + wrong-KEK rejection + version prefix +
// no external deps.

import { describe, expect, it } from 'vitest';
import { encrypt, decrypt } from '../envelope-encryption';

// 32-byte base64 test KEKs. Generated with `openssl rand -base64 32`.
// SAFE TO COMMIT: these are test fixtures, not real production keys.
const KEK_A = 'Pl/MWtPFs1lwGyN4nQqzhDtIRiOJfP8j+kHRsZ7TgXg=';
const KEK_B = 'YkW2K5sN0p7uVcD+aFr/I5LqxRz1y7sjJ4kP3vBgGoQ=';

describe('envelope-encryption', () => {
  describe('round-trip (AC0.10)', () => {
    it('given an ascii plaintext, when encrypted then decrypted with the same KEK, then yields the original plaintext', () => {
      const plaintext = 'fake_google_refresh_token_abc123';

      const ciphertext = encrypt(plaintext, KEK_A);

      expect(decrypt(ciphertext, KEK_A)).toBe(plaintext);
    });

    it('given a utf-8 plaintext with multibyte chars, when round-tripped, then yields the original plaintext', () => {
      const plaintext = 'ééé ñññ 한국어 🔐';

      const ciphertext = encrypt(plaintext, KEK_A);

      expect(decrypt(ciphertext, KEK_A)).toBe(plaintext);
    });

    it('given a 1KB plaintext, when round-tripped, then yields the original plaintext', () => {
      const plaintext = 'X'.repeat(1024);

      const ciphertext = encrypt(plaintext, KEK_A);

      expect(decrypt(ciphertext, KEK_A)).toBe(plaintext);
    });
  });

  describe('output format (AC0.9)', () => {
    it('given any plaintext, when encrypted, then output starts with v1. prefix and has three base64 segments separated by dots', () => {
      const ciphertext = encrypt('hello', KEK_A);

      expect(ciphertext).toMatch(
        /^v1\.[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+$/,
      );
    });

    it('given the same plaintext encrypted twice, when compared, then the ciphertexts differ (random IV)', () => {
      const a = encrypt('hello', KEK_A);
      const b = encrypt('hello', KEK_A);

      expect(a).not.toBe(b);
    });
  });

  describe('tamper detection (AC0.11)', () => {
    it('given a flipped byte in the ciphertext segment, when decrypted, then throws', () => {
      const ciphertext = encrypt('secret', KEK_A);
      const parts = ciphertext.split('.');
      const buf = Buffer.from(parts[2]!, 'base64');
      buf[0] = buf[0]! ^ 0x01;
      parts[2] = buf.toString('base64');
      const tampered = parts.join('.');

      expect(() => decrypt(tampered, KEK_A)).toThrow();
    });

    it('given a flipped byte in the authtag segment, when decrypted, then throws', () => {
      const ciphertext = encrypt('secret', KEK_A);
      const parts = ciphertext.split('.');
      const buf = Buffer.from(parts[3]!, 'base64');
      buf[0] = buf[0]! ^ 0x01;
      parts[3] = buf.toString('base64');
      const tampered = parts.join('.');

      expect(() => decrypt(tampered, KEK_A)).toThrow();
    });
  });

  describe('wrong KEK (AC0.12)', () => {
    it('given a ciphertext encrypted with one KEK, when decrypted with a different KEK, then throws', () => {
      const ciphertext = encrypt('secret', KEK_A);

      expect(() => decrypt(ciphertext, KEK_B)).toThrow();
    });
  });

  describe('version prefix (AC0.9)', () => {
    it('given a ciphertext with an unknown version prefix, when decrypted, then throws an unsupported-version error', () => {
      expect(() => decrypt('v0.aaa.bbb.ccc', KEK_A)).toThrow(
        /unsupported version/i,
      );
    });

    it('given a ciphertext with too few segments, when decrypted, then throws', () => {
      expect(() => decrypt('v1.aaa.bbb', KEK_A)).toThrow();
    });
  });

  describe('no external deps (AC0.13)', () => {
    it('given the envelope-encryption module source, when scanned for imports, then only node:crypto is imported', async () => {
      const fs = await import('node:fs/promises');
      const source = await fs.readFile(
        'src/lib/auth/envelope-encryption.ts',
        'utf8',
      );
      const imports = source.match(/^import .*from ['"](.+)['"]/gm) ?? [];
      const externals = imports.filter(
        (line) => !line.includes('node:crypto'),
      );

      expect(externals).toEqual([]);
    });
  });
});
