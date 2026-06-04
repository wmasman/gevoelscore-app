// Step-0 AC0.18-AC0.23: assert the calendar-binding schema definitions
// match the README shape. The actual idempotent POST loop runs against
// Directus separately; this test pins the LOCAL definition before any
// wire call.

import { describe, expect, it } from 'vitest';
// @ts-expect-error — .mjs lib without type declarations is intentional;
// the schema lib mirrors the pattern used by audit-junctions.mjs.
import { buildCollectionDefinitions } from '../lib/calendar-schema.mjs';

type FieldDef = {
  field: string;
  type?: string;
  schema?: Record<string, unknown>;
  meta?: Record<string, unknown>;
};

type CollectionDef = {
  collection: string;
  fields: FieldDef[];
};

describe('setup-calendar-collections schema', () => {
  it('given the calendar_connections definition, when inspected, then has 11 fields including refresh_token_encrypted (AC0.21)', () => {
    const defs = buildCollectionDefinitions() as CollectionDef[];

    const connections = defs.find(
      (d) => d.collection === 'calendar_connections',
    );

    expect(connections).toBeDefined();
    const fieldNames = connections!.fields.map((f) => f.field).sort();
    expect(fieldNames).toEqual([
      'connected_at',
      'id',
      'included_calendar_ids',
      'last_sync_error',
      'last_synced_at',
      'provider',
      'provider_account_email',
      'refresh_token_encrypted',
      'scope',
      'status',
      'user_id',
    ]);
  });

  it('given the calendar_events definition (migrated), when inspected, then has the multi-provider shape with no google_event_id (AC0.18, AC0.19)', () => {
    const defs = buildCollectionDefinitions() as CollectionDef[];

    const events = defs.find((d) => d.collection === 'calendar_events');

    expect(events).toBeDefined();
    const fieldNames = events!.fields.map((f) => f.field).sort();
    expect(fieldNames).toContain('provider');
    expect(fieldNames).toContain('provider_event_id');
    expect(fieldNames).toContain('recurrence_id');
    expect(fieldNames).toContain('start_at');
    expect(fieldNames).toContain('end_at');
    expect(fieldNames).toContain('linked_tag_id');
    expect(fieldNames).toContain('linked_episode_id');
    expect(fieldNames).toContain('included_as_context');
    expect(fieldNames).toContain('user_decision');
    // Amendment: 6 additional fields captured for v1.6.x/v2 use
    expect(fieldNames).toContain('event_type');
    expect(fieldNames).toContain('status');
    expect(fieldNames).toContain('transparency');
    expect(fieldNames).toContain('organizer_is_self');
    expect(fieldNames).toContain('ical_uid');
    expect(fieldNames).toContain('html_link');
    expect(fieldNames).not.toContain('google_event_id');
    expect(fieldNames).not.toContain('calendar_source');
    expect(fieldNames).not.toContain('relevance');
    expect(fieldNames).not.toContain('category_hint');
  });

  it('given the calendar_series_exclusions definition, when inspected, then has 4 fields (AC0.22)', () => {
    const defs = buildCollectionDefinitions() as CollectionDef[];

    const exclusions = defs.find(
      (d) => d.collection === 'calendar_series_exclusions',
    );

    expect(exclusions).toBeDefined();
    const fieldNames = exclusions!.fields.map((f) => f.field).sort();
    expect(fieldNames).toEqual([
      'connection_id',
      'excluded_at',
      'id',
      'recurrence_id',
    ]);
  });

  it('given the cron_monitor definition, when inspected, then has 6 fields (AC0.23)', () => {
    const defs = buildCollectionDefinitions() as CollectionDef[];

    const monitor = defs.find((d) => d.collection === 'cron_monitor');

    expect(monitor).toBeDefined();
    const fieldNames = monitor!.fields.map((f) => f.field).sort();
    expect(fieldNames).toEqual([
      'expected_interval_hours',
      'id',
      'is_active',
      'job_name',
      'last_result',
      'last_run_at',
    ]);
  });

  it('given all four definitions, when listed, then the array length is exactly 4 (no stray collections)', () => {
    const defs = buildCollectionDefinitions() as CollectionDef[];

    const collections = defs.map((d) => d.collection).sort();

    expect(collections).toEqual([
      'calendar_connections',
      'calendar_events',
      'calendar_series_exclusions',
      'cron_monitor',
    ]);
  });
});
