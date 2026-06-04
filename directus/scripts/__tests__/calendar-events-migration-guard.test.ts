// Step-0 AC0.17: migration guard. Asserts the v1 calendar_events
// placeholder is empty before destructive column drops. If the assertion
// fails, the migration refuses to run.

import { describe, expect, it } from 'vitest';
// @ts-expect-error — .mjs lib without type declarations is intentional.
import { assertCalendarEventsEmpty } from '../lib/calendar-migration-guard.mjs';

describe('calendar-events migration guard (AC0.17)', () => {
  it('given a count of 0 rows, when the guard runs, then resolves with no error', async () => {
    const fakeQuery = async () => [{ count: 0 }];

    await expect(assertCalendarEventsEmpty(fakeQuery)).resolves.toBeUndefined();
  });

  it('given a count of 3 rows, when the guard runs, then throws a not-empty error mentioning refusal', async () => {
    const fakeQuery = async () => [{ count: 3 }];

    await expect(assertCalendarEventsEmpty(fakeQuery)).rejects.toThrow(
      /not empty/i,
    );
  });

  it('given an unexpected query shape (empty result), when the guard runs, then throws', async () => {
    const fakeQuery = async () => [];

    await expect(assertCalendarEventsEmpty(fakeQuery)).rejects.toThrow();
  });

  it('given a count returned as a string (postgres COUNT() returns text by default), when the guard runs, then handles it (0 string passes, non-zero throws)', async () => {
    const fakeQueryZero = async () => [{ count: '0' }];
    const fakeQueryNonZero = async () => [{ count: '5' }];

    await expect(
      assertCalendarEventsEmpty(fakeQueryZero),
    ).resolves.toBeUndefined();
    await expect(assertCalendarEventsEmpty(fakeQueryNonZero)).rejects.toThrow(
      /not empty/i,
    );
  });
});
