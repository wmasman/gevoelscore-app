import { beforeEach, describe, expect, it, vi } from 'vitest';

// Hoisted mock functions — vi.hoisted ensures they exist before the vi.mock
// factory runs (which itself is hoisted above the import statements).
const mocks = vi.hoisted(() => ({
  login: vi.fn(),
  request: vi.fn(),
  setToken: vi.fn(),
  refresh: vi.fn(),
  logout: vi.fn(),
}));

vi.mock('@directus/sdk', () => {
  // Build a client that returns itself on .with() so the wrap chain works.
  const client = {
    with: () => client,
    login: mocks.login,
    refresh: mocks.refresh,
    logout: mocks.logout,
    request: mocks.request,
    setToken: mocks.setToken,
  };

  return {
    createDirectus: () => client,
    authentication: () => null,
    rest: () => null,
    // Named REST commands return marker objects so tests can identify the call.
    readMe: () => ({ __cmd: 'readMe' }),
    logout: (args: unknown) => ({ __cmd: 'logout', args }),
    refresh: (args: unknown) => ({ __cmd: 'refresh', args }),
    generateTwoFactorSecret: (password: string) => ({ __cmd: 'generateTfa', password }),
    enableTwoFactor: (secret: string, otp: string) => ({ __cmd: 'enableTfa', secret, otp }),
  };
});

import {
  directusLogin,
  directusLoginWithOtp,
  directusRefresh,
  directusLogout,
  directusGetMe,
  directusGenerateTfaSecret,
  directusEnableTfa,
} from '../directus-auth';

describe('directus-auth', () => {
  beforeEach(() => {
    mocks.login.mockReset();
    mocks.request.mockReset();
    mocks.setToken.mockReset();
    mocks.refresh.mockReset();
    mocks.logout.mockReset();
    process.env.DIRECTUS_URL = 'https://example.directus.test';
  });

  describe('directusLogin', () => {
    it('on success returns the access + refresh tokens', async () => {
      mocks.login.mockResolvedValue({
        access_token: 'at-1',
        refresh_token: 'rt-1',
        expires: 900_000,
      });

      const result = await directusLogin('a@b.com', 'pw');

      expect(result).toEqual({
        ok: true,
        value: { accessToken: 'at-1', refreshToken: 'rt-1', expiresInMs: 900_000 },
      });
      expect(mocks.login).toHaveBeenCalledWith('a@b.com', 'pw');
    });

    it('on Directus "OTP required" error returns otp_required', async () => {
      mocks.login.mockRejectedValue({
        errors: [{ extensions: { code: 'INVALID_OTP' } }],
      });

      const result = await directusLogin('a@b.com', 'pw');
      expect(result).toEqual({ ok: false, error: 'otp_required' });
    });

    it('on invalid credentials returns invalid_credentials', async () => {
      mocks.login.mockRejectedValue({
        errors: [{ extensions: { code: 'INVALID_CREDENTIALS' } }],
      });

      const result = await directusLogin('a@b.com', 'wrong');
      expect(result).toEqual({ ok: false, error: 'invalid_credentials' });
    });

    it('on network error (TypeError from fetch) returns network_error', async () => {
      mocks.login.mockRejectedValue(new TypeError('fetch failed'));

      const result = await directusLogin('a@b.com', 'pw');
      expect(result).toEqual({ ok: false, error: 'network_error' });
    });

    it('on unexpected error shape returns directus_error', async () => {
      mocks.login.mockRejectedValue(new Error('Internal Server Error'));

      const result = await directusLogin('a@b.com', 'pw');
      expect(result).toEqual({ ok: false, error: 'directus_error' });
    });
  });

  describe('directusLoginWithOtp', () => {
    it('forwards the otp in the options object', async () => {
      mocks.login.mockResolvedValue({
        access_token: 'at-2',
        refresh_token: 'rt-2',
        expires: 900_000,
      });

      const result = await directusLoginWithOtp('a@b.com', 'pw', '123456');

      expect(result.ok).toBe(true);
      expect(mocks.login).toHaveBeenCalledWith('a@b.com', 'pw', { otp: '123456' });
    });

    it('on invalid OTP returns invalid_otp', async () => {
      mocks.login.mockRejectedValue({
        errors: [{ extensions: { code: 'INVALID_OTP' } }],
      });

      const result = await directusLoginWithOtp('a@b.com', 'pw', '000000');
      expect(result).toEqual({ ok: false, error: 'invalid_otp' });
    });
  });

  describe('directusRefresh', () => {
    it('on success returns fresh tokens via client.request(refresh(...))', async () => {
      mocks.request.mockResolvedValue({
        access_token: 'at-3',
        refresh_token: 'rt-3',
        expires: 900_000,
      });

      const result = await directusRefresh('old-rt');
      expect(result).toEqual({
        ok: true,
        value: { accessToken: 'at-3', refreshToken: 'rt-3', expiresInMs: 900_000 },
      });
      expect(mocks.request).toHaveBeenCalledWith({
        __cmd: 'refresh',
        args: { refresh_token: 'old-rt' },
      });
    });
  });

  describe('directusLogout', () => {
    it('calls client.request(logout({ refresh_token }))', async () => {
      mocks.request.mockResolvedValue(undefined);

      const result = await directusLogout('rt-1');
      expect(result).toEqual({ ok: true, value: undefined });
      expect(mocks.request).toHaveBeenCalledWith({
        __cmd: 'logout',
        args: { refresh_token: 'rt-1' },
      });
    });

    it('treats a 401 (already-invalid token) as success — logout is idempotent', async () => {
      mocks.request.mockRejectedValue({
        errors: [{ extensions: { code: 'INVALID_CREDENTIALS' } }],
        response: { status: 401 },
      });

      const result = await directusLogout('stale-rt');
      expect(result.ok).toBe(true);
    });
  });

  describe('directusGetMe', () => {
    it('returns the current user when token is valid', async () => {
      mocks.request.mockResolvedValue({ id: 'user-uuid', email: 'a@b.com' });

      const result = await directusGetMe('at-1');
      expect(result).toEqual({ ok: true, value: { id: 'user-uuid', email: 'a@b.com' } });
      expect(mocks.setToken).toHaveBeenCalledWith('at-1');
      expect(mocks.request).toHaveBeenCalledWith({ __cmd: 'readMe' });
    });

    it('returns invalid_token when Directus rejects the access token', async () => {
      mocks.request.mockRejectedValue({
        errors: [{ extensions: { code: 'INVALID_TOKEN' } }],
      });

      const result = await directusGetMe('at-bad');
      expect(result).toEqual({ ok: false, error: 'invalid_token' });
    });
  });

  describe('directusGenerateTfaSecret', () => {
    it('returns secret + otpauthUrl on success', async () => {
      mocks.request.mockResolvedValue({
        secret: 'JBSWY3DPEHPK3PXP',
        otpauth_url: 'otpauth://totp/Directus:a@b.com?secret=JBSWY3DPEHPK3PXP&issuer=Directus',
      });

      const result = await directusGenerateTfaSecret('at-1', 'mypassword');
      expect(result).toEqual({
        ok: true,
        value: {
          secret: 'JBSWY3DPEHPK3PXP',
          otpauthUrl: 'otpauth://totp/Directus:a@b.com?secret=JBSWY3DPEHPK3PXP&issuer=Directus',
        },
      });
      expect(mocks.setToken).toHaveBeenCalledWith('at-1');
      expect(mocks.request).toHaveBeenCalledWith({ __cmd: 'generateTfa', password: 'mypassword' });
    });

    it('returns invalid_password when Directus rejects the password', async () => {
      mocks.request.mockRejectedValue({
        errors: [{ extensions: { code: 'INVALID_CREDENTIALS' } }],
      });

      const result = await directusGenerateTfaSecret('at-1', 'wrong');
      expect(result).toEqual({ ok: false, error: 'invalid_password' });
    });

    it('returns invalid_token when access token is rejected', async () => {
      mocks.request.mockRejectedValue({
        errors: [{ extensions: { code: 'INVALID_TOKEN' } }],
      });

      const result = await directusGenerateTfaSecret('at-bad', 'pw');
      expect(result).toEqual({ ok: false, error: 'invalid_token' });
    });

    it('returns network_error on fetch failure', async () => {
      mocks.request.mockRejectedValue(new TypeError('fetch failed'));

      const result = await directusGenerateTfaSecret('at-1', 'pw');
      expect(result).toEqual({ ok: false, error: 'network_error' });
    });
  });

  describe('directusEnableTfa', () => {
    it('returns ok:true on success', async () => {
      mocks.request.mockResolvedValue(undefined);

      const result = await directusEnableTfa('at-1', 'secret-abc', '123456');
      expect(result).toEqual({ ok: true, value: undefined });
      expect(mocks.setToken).toHaveBeenCalledWith('at-1');
      expect(mocks.request).toHaveBeenCalledWith({
        __cmd: 'enableTfa',
        secret: 'secret-abc',
        otp: '123456',
      });
    });

    it('returns invalid_otp when the code is wrong', async () => {
      mocks.request.mockRejectedValue({
        errors: [{ extensions: { code: 'INVALID_OTP' } }],
      });

      const result = await directusEnableTfa('at-1', 'secret-abc', '000000');
      expect(result).toEqual({ ok: false, error: 'invalid_otp' });
    });

    it('returns invalid_token when access token is rejected', async () => {
      mocks.request.mockRejectedValue({
        errors: [{ extensions: { code: 'INVALID_TOKEN' } }],
      });

      const result = await directusEnableTfa('at-bad', 'secret-abc', '123456');
      expect(result).toEqual({ ok: false, error: 'invalid_token' });
    });
  });
});
