// Step-2 Phase 2.C — GET /api/health/cron tests (AC2.6-2.12).
//
// Unauthenticated by design (matches programmeerprobeer's
// tvoo_frontend/src/app/api/health/cron/route.ts). The watchdog GHA
// workflow + humans during triage poll it. PII-safe by construction:
// cron_monitor.last_result is counts-only or short error codes per
// AC2.2/2.3, so verbatim passthrough is safe.

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

const mocks = vi.hoisted(() => ({
  readAllCronMonitorJobs: vi.fn(),
}));

vi.mock('@/lib/api/calendars', () => ({
  readAllCronMonitorJobs: mocks.readAllCronMonitorJobs,
}));

import { GET } from '../route';

const NOW = '2026-06-05T12:00:00.000Z';

function makeRow(overrides: Partial<{
  id: string;
  job_name: string;
  last_run_at: string | null;
  last_result: string | null;
  expected_interval_hours: number;
  is_active: boolean;
}> = {}) {
  return {
    id: 'cm-1',
    job_name: 'daily_calendar_sync',
    last_run_at: '2026-06-05T07:00:00.000Z', // 5h ago — fresh
    last_result: '{"ok":true,"details":{"connections":1}}',
    expected_interval_hours: 26,
    is_active: true,
    ...overrides,
  };
}

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(NOW));
  vi.unstubAllEnvs();
  vi.stubEnv('CALENDAR_CRON_DIRECTUS_TOKEN', 'cron-token');
  mocks.readAllCronMonitorJobs.mockReset();
});

afterEach(() => {
  vi.useRealTimers();
});

describe('GET /api/health/cron', () => {
  it('test 68 (AC2.9): returns 200 with { status, timestamp, schedule, jobs } shape', async () => {
    mocks.readAllCronMonitorJobs.mockResolvedValue({
      ok: true,
      value: [makeRow()],
    });

    const res = await GET();

    expect(res.status).toBe(200);
    const body = (await res.json()) as {
      status: string;
      timestamp: string;
      schedule: string;
      jobs: Array<{ jobName: string; status: string }>;
    };
    expect(body.status).toBe('ok');
    expect(body.timestamp).toBe(NOW);
    expect(typeof body.schedule).toBe('string');
    expect(body.jobs).toHaveLength(1);
    expect(body.jobs[0]!.jobName).toBe('daily_calendar_sync');
  });

  it('test 69 (AC2.6): no auth header required — GET() works with no request object', async () => {
    mocks.readAllCronMonitorJobs.mockResolvedValue({
      ok: true,
      value: [makeRow()],
    });

    // GET() takes no args (no auth gate, no header inspection).
    const res = await GET();

    expect(res.status).toBe(200);
  });

  it('test 70 (AC2.8): fresh last_run_at (5h ago, 26h threshold) → status ok', async () => {
    mocks.readAllCronMonitorJobs.mockResolvedValue({
      ok: true,
      value: [makeRow({ last_run_at: '2026-06-05T07:00:00.000Z' })],
    });

    const res = await GET();

    const body = (await res.json()) as {
      jobs: Array<{ status: string; hoursSinceRun: number }>;
    };
    expect(body.jobs[0]!.status).toBe('ok');
    expect(body.jobs[0]!.hoursSinceRun).toBe(5);
  });

  it('test 71 (AC2.8, AC2.9): last_run_at = null + is_active → status never_run, overall warning', async () => {
    mocks.readAllCronMonitorJobs.mockResolvedValue({
      ok: true,
      value: [makeRow({ last_run_at: null })],
    });

    const res = await GET();

    const body = (await res.json()) as {
      status: string;
      jobs: Array<{ status: string; hoursSinceRun: number | null }>;
    };
    expect(body.jobs[0]!.status).toBe('never_run');
    expect(body.jobs[0]!.hoursSinceRun).toBeNull();
    expect(body.status).toBe('warning');
  });

  it('test 72 (AC2.8, AC2.9): last_run_at older than expected_interval_hours → status stale, overall stale', async () => {
    mocks.readAllCronMonitorJobs.mockResolvedValue({
      ok: true,
      value: [makeRow({ last_run_at: '2026-06-04T06:00:00.000Z' })], // 30h ago
    });

    const res = await GET();

    const body = (await res.json()) as {
      status: string;
      jobs: Array<{ status: string; hoursSinceRun: number }>;
    };
    expect(body.jobs[0]!.status).toBe('stale');
    expect(body.jobs[0]!.hoursSinceRun).toBe(30);
    expect(body.status).toBe('stale');
  });

  it('test 73 (AC2.8): is_active = false → status inactive, does not affect overall', async () => {
    mocks.readAllCronMonitorJobs.mockResolvedValue({
      ok: true,
      value: [
        makeRow({ is_active: false, last_run_at: '2024-01-01T00:00:00.000Z' }),
        makeRow({
          id: 'cm-2',
          job_name: 'fresh_job',
          last_run_at: '2026-06-05T11:00:00.000Z',
        }),
      ],
    });

    const res = await GET();

    const body = (await res.json()) as {
      status: string;
      jobs: Array<{ jobName: string; status: string }>;
    };
    const inactive = body.jobs.find((j) => j.jobName === 'daily_calendar_sync');
    expect(inactive!.status).toBe('inactive');
    expect(body.status).toBe('ok'); // the inactive one is ignored
  });

  it('test 74 (AC2.9): mixed stale + fresh → overall stale', async () => {
    mocks.readAllCronMonitorJobs.mockResolvedValue({
      ok: true,
      value: [
        makeRow({ last_run_at: '2026-06-04T06:00:00.000Z' }), // 30h ago, stale
        makeRow({
          id: 'cm-2',
          job_name: 'fresh_job',
          last_run_at: '2026-06-05T11:00:00.000Z',
        }),
      ],
    });

    const res = await GET();

    const body = (await res.json()) as { status: string };
    expect(body.status).toBe('stale');
  });

  it('test 75 (AC2.9): mixed never_run + fresh → overall warning', async () => {
    mocks.readAllCronMonitorJobs.mockResolvedValue({
      ok: true,
      value: [
        makeRow({ last_run_at: null }),
        makeRow({
          id: 'cm-2',
          job_name: 'fresh_job',
          last_run_at: '2026-06-05T11:00:00.000Z',
        }),
      ],
    });

    const res = await GET();

    const body = (await res.json()) as { status: string };
    expect(body.status).toBe('warning');
  });

  it('test 76 (AC2.10): readAllCronMonitorJobs returns error Result → 503 with error field', async () => {
    mocks.readAllCronMonitorJobs.mockResolvedValue({
      ok: false,
      error: 'directus_error',
    });

    const res = await GET();

    expect(res.status).toBe(503);
    const body = (await res.json()) as {
      status: string;
      error: string;
      jobs: unknown[];
    };
    expect(body.status).toBe('error');
    expect(body.error).toBeTruthy();
    expect(body.jobs).toEqual([]);
  });

  it('test 77 (AC2.11): response includes Cache-Control: private, s-maxage=60', async () => {
    mocks.readAllCronMonitorJobs.mockResolvedValue({
      ok: true,
      value: [makeRow()],
    });

    const res = await GET();

    expect(res.headers.get('cache-control')).toBe('private, s-maxage=60');
  });

  it('test 78 (AC2.12): lastResult surfaced verbatim from the row', async () => {
    const lastResult = '{"ok":true,"details":{"connections":1,"events_pulled":42}}';
    mocks.readAllCronMonitorJobs.mockResolvedValue({
      ok: true,
      value: [makeRow({ last_result: lastResult })],
    });

    const res = await GET();

    const body = (await res.json()) as {
      jobs: Array<{ lastResult: string }>;
    };
    expect(body.jobs[0]!.lastResult).toBe(lastResult);
  });
});
