// Idempotent Directus collection / field definitions for calendar-binding (v1.6).
// Mirrors the shape used in directus/scripts/setup-schema.mjs so the
// definitions can be POSTed via the same /collections + /fields routes.
//
// See docs/features/calendar-binding/step-0-data-model-and-provider.md
// AC0.18-AC0.23.
//
// Note: this lib returns DEFINITIONS only. The actual idempotent POST
// loop lives in directus/scripts/setup-calendar-collections.mjs (the
// runner). Tests pin the definitions in isolation before any wire call.

const idField = {
  field: 'id',
  type: 'uuid',
  schema: {
    is_primary_key: true,
    has_auto_increment: false,
    is_nullable: false,
  },
  meta: {
    hidden: true,
    readonly: true,
    interface: 'input',
    special: ['uuid'],
  },
};

const createdAtField = {
  field: 'created_at',
  type: 'timestamp',
  schema: { is_nullable: true },
  meta: { interface: 'datetime', readonly: true, special: ['date-created'] },
};

const updatedAtField = {
  field: 'updated_at',
  type: 'timestamp',
  schema: { is_nullable: true },
  meta: { interface: 'datetime', readonly: true, special: ['date-updated'] },
};

export function buildCollectionDefinitions() {
  return [
    // -------------------------------------------------------------
    // calendar_connections — one row per (user, provider, account_email)
    // -------------------------------------------------------------
    {
      collection: 'calendar_connections',
      schema: { name: 'calendar_connections' },
      meta: {
        icon: 'sync',
        note: 'v1.6: per-user calendar OAuth connections. refresh_token_encrypted via envelope encryption (CALENDAR_KEK).',
        collection: 'calendar_connections',
        display_template: '{{provider_account_email}} ({{provider}})',
      },
      fields: [
        idField,
        {
          field: 'user_id',
          type: 'uuid',
          schema: { is_nullable: false },
          meta: { interface: 'input', readonly: true },
        },
        {
          field: 'provider',
          type: 'string',
          schema: { is_nullable: false, max_length: 20 },
          meta: { interface: 'input' },
        },
        {
          field: 'provider_account_email',
          type: 'string',
          schema: { is_nullable: false, max_length: 320 },
          meta: { interface: 'input' },
        },
        {
          field: 'refresh_token_encrypted',
          type: 'text',
          schema: { is_nullable: false },
          meta: { interface: 'input-multiline', readonly: true },
        },
        {
          field: 'scope',
          type: 'string',
          schema: { is_nullable: false, max_length: 500 },
          meta: { interface: 'input' },
        },
        {
          field: 'connected_at',
          type: 'timestamp',
          schema: { is_nullable: false },
          meta: { interface: 'datetime' },
        },
        {
          field: 'last_synced_at',
          type: 'timestamp',
          schema: { is_nullable: true },
          meta: { interface: 'datetime' },
        },
        {
          field: 'last_sync_error',
          type: 'text',
          schema: { is_nullable: true },
          meta: { interface: 'input-multiline' },
        },
        {
          field: 'status',
          type: 'string',
          schema: { is_nullable: false, max_length: 20, default_value: 'active' },
          meta: {
            interface: 'select-dropdown',
            options: {
              choices: [
                { text: 'Active', value: 'active' },
                { text: 'Disconnected', value: 'disconnected' },
                { text: 'Error', value: 'error' },
              ],
            },
          },
        },
        {
          field: 'included_calendar_ids',
          type: 'json',
          schema: { is_nullable: false, default_value: '[]' },
          meta: { interface: 'input-code', options: { language: 'json' } },
        },
      ],
    },

    // -------------------------------------------------------------
    // calendar_events — multi-provider events (migrated from the v1
    // Google-specific placeholder). The migration to this shape is
    // gated by assertCalendarEventsEmpty in the runner.
    // -------------------------------------------------------------
    {
      collection: 'calendar_events',
      schema: { name: 'calendar_events' },
      meta: {
        icon: 'event',
        note: 'v1.6: multi-provider calendar events; see docs/features/calendar-binding/',
        collection: 'calendar_events',
        display_template: '{{title}} ({{start_at}})',
      },
      fields: [
        idField,
        {
          field: 'connection_id',
          type: 'uuid',
          schema: { is_nullable: false },
          meta: { interface: 'input', readonly: true },
        },
        {
          field: 'provider',
          type: 'string',
          schema: { is_nullable: false, max_length: 20 },
          meta: { interface: 'input' },
        },
        {
          field: 'provider_event_id',
          type: 'string',
          schema: { is_nullable: false, max_length: 200 },
          meta: { interface: 'input', readonly: true },
        },
        {
          field: 'recurrence_id',
          type: 'string',
          schema: { is_nullable: true, max_length: 200 },
          meta: { interface: 'input', readonly: true },
        },
        {
          field: 'start_at',
          type: 'timestamp',
          schema: { is_nullable: false },
          meta: { interface: 'datetime' },
        },
        {
          field: 'end_at',
          type: 'timestamp',
          schema: { is_nullable: false },
          meta: { interface: 'datetime' },
        },
        {
          field: 'all_day',
          type: 'boolean',
          schema: { is_nullable: false, default_value: false },
          meta: { interface: 'boolean' },
        },
        {
          field: 'title',
          type: 'string',
          schema: { is_nullable: false, max_length: 500 },
          meta: { interface: 'input' },
        },
        {
          field: 'location',
          type: 'string',
          schema: { is_nullable: true, max_length: 500 },
          meta: { interface: 'input' },
        },
        {
          field: 'attendees_count',
          type: 'integer',
          schema: { is_nullable: false, default_value: 0 },
          meta: { interface: 'input' },
        },
        {
          field: 'declined',
          type: 'boolean',
          schema: { is_nullable: false, default_value: false },
          meta: { interface: 'boolean' },
        },
        {
          field: 'event_type',
          type: 'string',
          schema: { is_nullable: true, max_length: 32 },
          meta: { interface: 'input', readonly: true },
        },
        {
          field: 'status',
          type: 'string',
          schema: { is_nullable: false, max_length: 20, default_value: 'confirmed' },
          meta: {
            interface: 'select-dropdown',
            options: {
              choices: [
                { text: 'Confirmed', value: 'confirmed' },
                { text: 'Tentative', value: 'tentative' },
                { text: 'Cancelled', value: 'cancelled' },
              ],
            },
          },
        },
        {
          field: 'transparency',
          type: 'string',
          schema: { is_nullable: false, max_length: 20, default_value: 'opaque' },
          meta: {
            interface: 'select-dropdown',
            options: {
              choices: [
                { text: 'Opaque (busy)', value: 'opaque' },
                { text: 'Transparent (free)', value: 'transparent' },
              ],
            },
          },
        },
        {
          field: 'organizer_is_self',
          type: 'boolean',
          schema: { is_nullable: false, default_value: false },
          meta: { interface: 'boolean' },
        },
        {
          field: 'ical_uid',
          type: 'string',
          schema: { is_nullable: true, max_length: 500 },
          meta: { interface: 'input', readonly: true },
        },
        {
          field: 'html_link',
          type: 'string',
          schema: { is_nullable: true, max_length: 1000 },
          meta: { interface: 'input', readonly: true },
        },
        {
          field: 'linked_tag_id',
          type: 'uuid',
          schema: { is_nullable: true },
          meta: { interface: 'input' },
        },
        {
          field: 'linked_episode_id',
          type: 'uuid',
          schema: { is_nullable: true },
          meta: { interface: 'input' },
        },
        {
          field: 'included_as_context',
          type: 'boolean',
          schema: { is_nullable: false, default_value: true },
          meta: { interface: 'boolean' },
        },
        {
          field: 'user_decision',
          type: 'string',
          schema: { is_nullable: false, max_length: 20, default_value: 'auto' },
          meta: {
            interface: 'select-dropdown',
            options: {
              choices: [
                { text: 'Auto (rules-based)', value: 'auto' },
                { text: 'User included', value: 'user_included' },
                { text: 'User excluded', value: 'user_excluded' },
              ],
            },
          },
        },
        createdAtField,
        updatedAtField,
      ],
    },

    // -------------------------------------------------------------
    // calendar_series_exclusions — when present, new events of this
    // recurrence default to included_as_context=false at pull time.
    // -------------------------------------------------------------
    {
      collection: 'calendar_series_exclusions',
      schema: { name: 'calendar_series_exclusions' },
      meta: {
        icon: 'event_busy',
        note: 'v1.6: user opted to exclude a calendar recurrence series from context.',
        collection: 'calendar_series_exclusions',
      },
      fields: [
        idField,
        {
          field: 'connection_id',
          type: 'uuid',
          schema: { is_nullable: false },
          meta: { interface: 'input', readonly: true },
        },
        {
          field: 'recurrence_id',
          type: 'string',
          schema: { is_nullable: false, max_length: 200 },
          meta: { interface: 'input' },
        },
        {
          field: 'excluded_at',
          type: 'timestamp',
          schema: { is_nullable: false },
          meta: { interface: 'datetime' },
        },
      ],
    },

    // -------------------------------------------------------------
    // cron_monitor — shared infrastructure for any scheduled job in
    // this app. v1.6 seeds it with one row (daily_calendar_sync) but
    // future jobs (export, retention sweeps) reuse the collection.
    // -------------------------------------------------------------
    {
      collection: 'cron_monitor',
      schema: { name: 'cron_monitor' },
      meta: {
        icon: 'schedule',
        note: 'Shared cron infrastructure (introduced v1.6). Each scheduled job writes a row after running. Read by /api/health/cron.',
        collection: 'cron_monitor',
        display_template: '{{job_name}} — {{last_run_at}}',
      },
      fields: [
        idField,
        {
          field: 'job_name',
          type: 'string',
          schema: { is_nullable: false, max_length: 100 },
          meta: { interface: 'input' },
        },
        {
          field: 'last_run_at',
          type: 'timestamp',
          schema: { is_nullable: true },
          meta: { interface: 'datetime' },
        },
        {
          field: 'last_result',
          type: 'text',
          schema: { is_nullable: true },
          meta: { interface: 'input-multiline' },
        },
        {
          field: 'expected_interval_hours',
          type: 'integer',
          schema: { is_nullable: false, default_value: 26 },
          meta: { interface: 'input' },
        },
        {
          field: 'is_active',
          type: 'boolean',
          schema: { is_nullable: false, default_value: true },
          meta: { interface: 'boolean' },
        },
      ],
    },
  ];
}
