import { describe, expect, it } from 'vitest';
import { getClientIp } from '../stores';

function makeRequest(headers: Record<string, string>): Request {
  return new Request('http://localhost/x', { headers });
}

describe('getClientIp', () => {
  it('prefers Fly-Client-IP', () => {
    const r = makeRequest({ 'fly-client-ip': '203.0.113.7' });
    expect(getClientIp(r)).toBe('203.0.113.7');
  });

  it('returns Fly-Client-IP even when X-Forwarded-For is spoofed (H4 bypass attempt)', () => {
    const r = makeRequest({
      'fly-client-ip': '203.0.113.7',
      'x-forwarded-for': 'attacker-rotating-value, 203.0.113.7',
    });
    expect(getClientIp(r)).toBe('203.0.113.7');
  });

  it('falls back to X-Real-IP when Fly-Client-IP is absent', () => {
    const r = makeRequest({ 'x-real-ip': '198.51.100.4' });
    expect(getClientIp(r)).toBe('198.51.100.4');
  });

  it('returns the LAST hop of X-Forwarded-For when neither Fly-Client-IP nor X-Real-IP is set', () => {
    const r = makeRequest({ 'x-forwarded-for': 'poisoned, 198.51.100.4' });
    expect(getClientIp(r)).toBe('198.51.100.4');
  });

  it("returns 'unknown' when no IP headers are present", () => {
    const r = makeRequest({});
    expect(getClientIp(r)).toBe('unknown');
  });
});
