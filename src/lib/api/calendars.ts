// Server-side SDK wrapper for the calendar-binding feature (v1.6).
// Mirrors the shape of tags.ts / episodes.ts / day-entries.ts:
// stateless functions, fresh client per call, Result-shaped returns.
//
// Step-0 ships only the 4 row types + the minimal getCronMonitorJob
// helper used by the step-2 health endpoint. The remaining methods
// (connect/disconnect/sync orchestration) land in step-1.
//
// See docs/features/calendar-binding/step-0-data-model-and-provider.md
// AC0.14-AC0.16.

import {
  createDirectus,
  readItems,
  rest,
  staticToken,
} from '@directus/sdk';
import type { Result } from './result';

export type CalendarsError = 'network_error' | 'directus_error';

export type DirectusCalendarConnectionRow = {
  id: string;
  user_id: string;
  provider: 'google';
  provider_account_email: string;
  refresh_token_encrypted: string;
  scope: string;
  connected_at: string;
  last_synced_at: string | null;
  last_sync_error: string | null;
  status: 'active' | 'disconnected' | 'error';
  included_calendar_ids: string[];
};

export type DirectusCalendarEventRow = {
  id: string;
  connection_id: string;
  provider: 'google';
  provider_event_id: string;
  recurrence_id: string | null;
  start_at: string;
  end_at: string;
  all_day: boolean;
  title: string;
  location: string | null;
  attendees_count: number;
  declined: boolean;
  event_type: string | null;
  status: 'confirmed' | 'tentative' | 'cancelled';
  transparency: 'opaque' | 'transparent';
  organizer_is_self: boolean;
  ical_uid: string | null;
  html_link: string | null;
  linked_tag_id: string | null;
  linked_episode_id: string | null;
  included_as_context: boolean;
  user_decision: 'auto' | 'user_included' | 'user_excluded';
  created_at: string;
  updated_at: string;
};

export type DirectusCalendarSeriesExclusionRow = {
  id: string;
  connection_id: string;
  recurrence_id: string;
  excluded_at: string;
};

export type DirectusCronMonitorRow = {
  id: string;
  job_name: string;
  last_run_at: string | null;
  last_result: string | null;
  expected_interval_hours: number;
  is_active: boolean;
};

type DirectusSchema = {
  calendar_connections: DirectusCalendarConnectionRow[];
  calendar_events: DirectusCalendarEventRow[];
  calendar_series_exclusions: DirectusCalendarSeriesExclusionRow[];
  cron_monitor: DirectusCronMonitorRow[];
};

function directusUrl(): string {
  return (
    process.env.DIRECTUS_URL ??
    process.env.NEXT_PUBLIC_DIRECTUS_URL ??
    'http://localhost:8055'
  );
}

function isNetworkError(e: unknown): boolean {
  return e instanceof TypeError && /fetch/i.test(e.message);
}

export async function getCronMonitorJob(
  accessToken: string,
  jobName: string,
): Promise<Result<DirectusCronMonitorRow | null, CalendarsError>> {
  try {
    const client = createDirectus<DirectusSchema>(directusUrl())
      .with(rest())
      .with(staticToken(accessToken));

    const rows = (await client.request(
      readItems('cron_monitor', {
        filter: { job_name: { _eq: jobName } },
        limit: 1,
      } as never),
    )) as DirectusCronMonitorRow[];

    return { ok: true, value: rows[0] ?? null };
  } catch (e) {
    if (isNetworkError(e)) {
      return { ok: false, error: 'network_error' };
    }
    return { ok: false, error: 'directus_error' };
  }
}
