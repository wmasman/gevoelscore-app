// GET /api/health/cron — unauthenticated cron staleness probe.
//
// No auth gate (AC2.6). Watchdog GHA workflow polls every 6h
// (step-2.F); also pollable by humans during incident triage.
// PII-safe by construction: cron_monitor.last_result carries only
// counts (AC2.2) or short error codes (AC2.3), so verbatim
// passthrough is safe (AC2.12).
//
// Reads cron_monitor with CALENDAR_CRON_DIRECTUS_TOKEN — the only
// available scoped server token with cron_monitor access.
// DIRECTUS_TOKEN is the sessions-only scoped token (S-H1) and can't
// read cron_monitor. v1.6.x hardening candidate: split into a
// dedicated read-only CRON_MONITOR_READ_TOKEN to reduce blast radius
// if this unauthenticated endpoint ever leaks the env var.
//
// Ported from programmeerprobeer's tvoo_frontend/src/app/api/health/
// cron/route.ts with the same status taxonomy (ok/warning/stale/error).
// Single calendar cron today; the rows-iteration pattern keeps the
// endpoint open for additional jobs without code change.

import { NextResponse } from 'next/server';
import {
  type DirectusCronMonitorRow,
  readAllCronMonitorJobs,
} from '@/lib/api/calendars';

type JobStatus = 'ok' | 'stale' | 'never_run' | 'inactive';

type JobReport = {
  jobName: string;
  lastRunAt: string | null;
  lastResult: string | null;
  status: JobStatus;
  hoursSinceRun: number | null;
};

type OverallStatus = 'ok' | 'warning' | 'stale' | 'error';

function classifyJob(row: DirectusCronMonitorRow, now: Date): JobReport {
  if (!row.is_active) {
    return {
      jobName: row.job_name,
      lastRunAt: row.last_run_at,
      lastResult: row.last_result,
      status: 'inactive',
      hoursSinceRun: null,
    };
  }
  if (!row.last_run_at) {
    return {
      jobName: row.job_name,
      lastRunAt: null,
      lastResult: null,
      status: 'never_run',
      hoursSinceRun: null,
    };
  }
  const lastRun = new Date(row.last_run_at);
  const hoursSinceRun =
    Math.round(((now.getTime() - lastRun.getTime()) / 3600000) * 10) / 10;
  const status: JobStatus =
    hoursSinceRun > row.expected_interval_hours ? 'stale' : 'ok';
  return {
    jobName: row.job_name,
    lastRunAt: row.last_run_at,
    lastResult: row.last_result,
    status,
    hoursSinceRun,
  };
}

function overallStatus(jobs: JobReport[]): OverallStatus {
  if (jobs.some((j) => j.status === 'stale')) return 'stale';
  if (jobs.some((j) => j.status === 'never_run')) return 'warning';
  return 'ok';
}

export async function GET() {
  const now = new Date();
  const token = process.env.CALENDAR_CRON_DIRECTUS_TOKEN;
  if (!token) {
    return NextResponse.json(
      {
        status: 'error',
        timestamp: now.toISOString(),
        error: 'CALENDAR_CRON_DIRECTUS_TOKEN unset',
        jobs: [],
      },
      { status: 503 },
    );
  }

  const result = await readAllCronMonitorJobs(token);
  if (!result.ok) {
    return NextResponse.json(
      {
        status: 'error',
        timestamp: now.toISOString(),
        error: `cron_monitor unreachable: ${result.error}`,
        jobs: [],
      },
      { status: 503 },
    );
  }

  const jobs = result.value.map((r) => classifyJob(r, now));
  return NextResponse.json(
    {
      status: overallStatus(jobs),
      timestamp: now.toISOString(),
      schedule: 'daily_calendar_sync runs at 03:00 UTC daily',
      jobs,
    },
    { headers: { 'Cache-Control': 'private, s-maxage=60' } },
  );
}
