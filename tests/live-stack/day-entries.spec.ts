// Live-stack verification for the day-entries read API.
//
// Calls the SDK wrapper directly against the real Directus on Fly using the
// frontend user's static token (PLAYWRIGHT_TEST_FRONTEND_TOKEN in .env.local).
// Bypasses the route handler's session lookup — that surface is unit-tested
// in src/app/api/day-entries/**/__tests__/route.test.ts. The point of this
// spec is to catch Directus schema drift on the live deploy (M2M expansion
// shape, field names, value types) that mocks can't see.
//
// Skips gracefully if the token isn't set, so the live-stack suite stays
// runnable on machines without credentials.

import { test, expect } from '@playwright/test';
import { readDayEntriesInRange, readDayEntryByDate } from '@/lib/api/day-entries';
import { todayInAmsterdam } from '@/lib/domain/date';

const TOKEN = process.env.PLAYWRIGHT_TEST_FRONTEND_TOKEN;
const hasToken = typeof TOKEN === 'string' && TOKEN.length > 0;

test.describe('day-entries read API against live Directus', () => {
  test.skip(
    !hasToken,
    'PLAYWRIGHT_TEST_FRONTEND_TOKEN not set in .env.local — see step-1 doc',
  );

  test('readDayEntryByDate returns a valid DayEntry shape or null for today', async () => {
    const today = todayInAmsterdam();
    const result = await readDayEntryByDate(TOKEN!, today);

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    if (result.value !== null) {
      expect(result.value.date).toBe(today);
      expect(result.value.score).toBeGreaterThanOrEqual(1);
      expect(result.value.score).toBeLessThanOrEqual(10);
      expect(Array.isArray(result.value.tag_ids)).toBe(true);
    }
  });

  test('readDayEntriesInRange returns chronologically-ordered entries with M2M tags flattened', async () => {
    // Read a known-historical 30-day window. The user's first logged day is
    // 2022-09-03; this window covers ~30 days of that early stretch.
    const result = await readDayEntriesInRange(TOKEN!, '2022-09-03', '2022-10-02');

    expect(result.ok).toBe(true);
    if (!result.ok) return;
    expect(result.value.length).toBeGreaterThan(0);

    // Chronological order.
    const dates = result.value.map((e) => e.date);
    const sorted = [...dates].sort();
    expect(dates).toEqual(sorted);

    // Every row carries the flattened tag_ids array (never the verbose
    // Directus { tags: [{ tags_id }] } shape).
    for (const entry of result.value) {
      expect(Array.isArray(entry.tag_ids)).toBe(true);
      expect(entry.score).toBeGreaterThanOrEqual(1);
      expect(entry.score).toBeLessThanOrEqual(10);
    }

    // At least one row in that range should have been auto-tagged by the
    // note_pattern import (1,338 junction rows across 1,363 days = ~98%
    // tag coverage in the historical dataset). If this fails, the M2M
    // expansion isn't working.
    const taggedRows = result.value.filter((e) => e.tag_ids.length > 0);
    expect(taggedRows.length).toBeGreaterThan(0);
  });
});
