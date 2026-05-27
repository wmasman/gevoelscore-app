// Server-side wrapper around @directus/sdk for the auth flow.
//
// All functions are stateless — each call constructs a fresh SDK client and
// passes the relevant token explicitly. We do NOT use the SDK's stored-token
// feature because Next.js Route Handlers don't share state across requests.
//
// All functions return Result-shaped values:
//   { ok: true; value: T } | { ok: false; error: ErrorCode }
//
// ErrorCode is a discriminated string so callers can branch exhaustively.

import {
  createDirectus,
  authentication,
  rest,
  readMe,
  logout as sdkLogout,
  refresh as sdkRefresh,
  generateTwoFactorSecret as sdkGenerateTfaSecret,
  enableTwoFactor as sdkEnableTfa,
} from '@directus/sdk';

export type AuthTokens = {
  accessToken: string;
  refreshToken: string;
  expiresInMs: number;
};

export type AuthUser = {
  id: string;
  email: string;
};

export type LoginError = 'otp_required' | 'invalid_credentials' | 'network_error' | 'directus_error';
export type LoginWithOtpError = 'invalid_otp' | 'invalid_credentials' | 'network_error' | 'directus_error';
export type RefreshError = 'invalid_refresh_token' | 'network_error' | 'directus_error';
export type LogoutError = 'network_error' | 'directus_error';
export type GetMeError = 'invalid_token' | 'network_error' | 'directus_error';
export type GenerateTfaError = 'invalid_password' | 'invalid_token' | 'network_error' | 'directus_error';
export type EnableTfaError = 'invalid_otp' | 'invalid_token' | 'network_error' | 'directus_error';

export type TfaSecret = {
  secret: string;
  otpauthUrl: string;
};

export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

function directusUrl(): string {
  return (
    process.env.DIRECTUS_URL ??
    process.env.NEXT_PUBLIC_DIRECTUS_URL ??
    'http://localhost:8055'
  );
}

function createClient() {
  return createDirectus(directusUrl()).with(authentication('json')).with(rest());
}

// Pulls the Directus-style error code out of an unknown thrown value.
// Directus errors look like: { errors: [{ extensions: { code: 'XYZ' } }] }
function errorCode(e: unknown): string | null {
  if (typeof e !== 'object' || e === null) return null;
  const errors = (e as { errors?: unknown }).errors;
  if (!Array.isArray(errors) || errors.length === 0) return null;
  const first = errors[0];
  if (typeof first !== 'object' || first === null) return null;
  const ext = (first as { extensions?: unknown }).extensions;
  if (typeof ext !== 'object' || ext === null) return null;
  const code = (ext as { code?: unknown }).code;
  return typeof code === 'string' ? code : null;
}

function isNetworkError(e: unknown): boolean {
  return e instanceof TypeError && /fetch/i.test(e.message);
}

function mapLoginError(e: unknown): LoginError {
  if (isNetworkError(e)) return 'network_error';
  const code = errorCode(e);
  if (code === 'INVALID_OTP') return 'otp_required';
  if (code === 'INVALID_CREDENTIALS') return 'invalid_credentials';
  return 'directus_error';
}

function mapLoginWithOtpError(e: unknown): LoginWithOtpError {
  if (isNetworkError(e)) return 'network_error';
  const code = errorCode(e);
  if (code === 'INVALID_OTP') return 'invalid_otp';
  if (code === 'INVALID_CREDENTIALS') return 'invalid_credentials';
  return 'directus_error';
}

type SdkAuthResult = {
  access_token?: string | null;
  refresh_token?: string | null;
  expires?: number | null;
};

function toAuthTokens(raw: SdkAuthResult): AuthTokens | null {
  if (!raw.access_token || !raw.refresh_token || typeof raw.expires !== 'number') return null;
  return {
    accessToken: raw.access_token,
    refreshToken: raw.refresh_token,
    expiresInMs: raw.expires,
  };
}

export async function directusLogin(
  email: string,
  password: string,
): Promise<Result<AuthTokens, LoginError>> {
  try {
    const client = createClient();
    const raw = (await client.login(email, password)) as SdkAuthResult;
    const tokens = toAuthTokens(raw);
    if (!tokens) return { ok: false, error: 'directus_error' };
    return { ok: true, value: tokens };
  } catch (e) {
    return { ok: false, error: mapLoginError(e) };
  }
}

export async function directusLoginWithOtp(
  email: string,
  password: string,
  otp: string,
): Promise<Result<AuthTokens, LoginWithOtpError>> {
  try {
    const client = createClient();
    const raw = (await client.login(email, password, { otp })) as SdkAuthResult;
    const tokens = toAuthTokens(raw);
    if (!tokens) return { ok: false, error: 'directus_error' };
    return { ok: true, value: tokens };
  } catch (e) {
    return { ok: false, error: mapLoginWithOtpError(e) };
  }
}

export async function directusRefresh(
  refreshToken: string,
): Promise<Result<AuthTokens, RefreshError>> {
  try {
    const client = createClient();
    const raw = (await client.request(
      sdkRefresh({ refresh_token: refreshToken } as never) as never,
    )) as SdkAuthResult;
    const tokens = toAuthTokens(raw);
    if (!tokens) return { ok: false, error: 'directus_error' };
    return { ok: true, value: tokens };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    return { ok: false, error: 'invalid_refresh_token' };
  }
}

export async function directusLogout(
  refreshToken: string,
): Promise<Result<void, LogoutError>> {
  try {
    const client = createClient();
    await client.request(sdkLogout({ refresh_token: refreshToken } as never) as never);
    return { ok: true, value: undefined };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    // Logout is idempotent — Directus rejecting an already-invalid token is
    // not an error from our perspective. The user is "logged out" either way.
    return { ok: true, value: undefined };
  }
}

export async function directusGetMe(
  accessToken: string,
): Promise<Result<AuthUser, GetMeError>> {
  try {
    const client = createClient();
    client.setToken(accessToken);
    const raw = (await client.request(readMe() as never)) as { id?: string; email?: string };
    if (typeof raw.id !== 'string' || typeof raw.email !== 'string') {
      return { ok: false, error: 'directus_error' };
    }
    return { ok: true, value: { id: raw.id, email: raw.email } };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    const code = errorCode(e);
    if (code === 'INVALID_TOKEN' || code === 'INVALID_CREDENTIALS') {
      return { ok: false, error: 'invalid_token' };
    }
    return { ok: false, error: 'directus_error' };
  }
}

export async function directusGenerateTfaSecret(
  accessToken: string,
  password: string,
): Promise<Result<TfaSecret, GenerateTfaError>> {
  try {
    const client = createClient();
    client.setToken(accessToken);
    const raw = (await client.request(
      sdkGenerateTfaSecret(password) as never,
    )) as { secret?: string; otpauth_url?: string };
    if (typeof raw.secret !== 'string' || typeof raw.otpauth_url !== 'string') {
      return { ok: false, error: 'directus_error' };
    }
    return { ok: true, value: { secret: raw.secret, otpauthUrl: raw.otpauth_url } };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    const code = errorCode(e);
    if (code === 'INVALID_PAYLOAD' || code === 'INVALID_CREDENTIALS') {
      return { ok: false, error: 'invalid_password' };
    }
    if (code === 'INVALID_TOKEN') return { ok: false, error: 'invalid_token' };
    return { ok: false, error: 'directus_error' };
  }
}

export async function directusEnableTfa(
  accessToken: string,
  secret: string,
  otp: string,
): Promise<Result<void, EnableTfaError>> {
  try {
    const client = createClient();
    client.setToken(accessToken);
    await client.request(sdkEnableTfa(secret, otp) as never);
    return { ok: true, value: undefined };
  } catch (e) {
    if (isNetworkError(e)) return { ok: false, error: 'network_error' };
    const code = errorCode(e);
    if (code === 'INVALID_OTP' || code === 'INVALID_PAYLOAD') {
      return { ok: false, error: 'invalid_otp' };
    }
    if (code === 'INVALID_TOKEN' || code === 'INVALID_CREDENTIALS') {
      return { ok: false, error: 'invalid_token' };
    }
    return { ok: false, error: 'directus_error' };
  }
}
