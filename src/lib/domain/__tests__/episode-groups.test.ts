import { describe, expect, it } from 'vitest';
import { groupEpisodes } from '../episode-groups';
import type { Episode } from '../episode';

/** Factory for a minimal valid Episode (an active interventie). */
function ep(overrides: Partial<Episode> = {}): Episode {
  return {
    id: 'ep-default',
    label: 'Default',
    category: 'interventie',
    start_date: '2026-04-01',
    end_date: null,
    description: null,
    calendar_binding: null,
    archived_at: null,
    created_at: '2026-04-01T08:00:00.000Z',
    updated_at: '2026-04-01T08:00:00.000Z',
    ...overrides,
  };
}

const TODAY = '2026-06-02';

describe('episode-groups', () => {
  describe('groupEpisodes — empty', () => {
    it('given an empty list, then all four buckets are empty and totals are 0', () => {
      const result = groupEpisodes([], TODAY);

      expect(result).toEqual({
        interventiesActive: [],
        interventiesDone: [],
        levensgebeurtenissenActive: [],
        levensgebeurtenissenDone: [],
        totalActive: 0,
        totalDone: 0,
      });
    });
  });

  describe('groupEpisodes — interventie bucketing', () => {
    it('given an active interventie (end_date null), then it lands in interventiesActive', () => {
      const e = ep({ id: 'e1', end_date: null });

      const result = groupEpisodes([e], TODAY);

      expect(result.interventiesActive).toEqual([e]);
      expect(result.interventiesDone).toEqual([]);
    });

    it('given an active interventie (end_date in the future), then it lands in interventiesActive', () => {
      const e = ep({ id: 'e1', end_date: '2026-07-15' });

      const result = groupEpisodes([e], TODAY);

      expect(result.interventiesActive).toEqual([e]);
    });

    it('given an interventie whose end_date EQUALS today, then it counts as active (today is inclusive)', () => {
      // end_date >= today → today is inclusive. An episode ending TODAY
      // is still "in progress" today. The user can re-classify tomorrow
      // when end_date < today.
      const e = ep({ id: 'e1', end_date: TODAY });

      const result = groupEpisodes([e], TODAY);

      expect(result.interventiesActive).toEqual([e]);
      expect(result.interventiesDone).toEqual([]);
    });

    it('given an interventie whose end_date is yesterday, then it lands in interventiesDone', () => {
      const e = ep({ id: 'e1', end_date: '2026-06-01' });

      const result = groupEpisodes([e], TODAY);

      expect(result.interventiesDone).toEqual([e]);
      expect(result.interventiesActive).toEqual([]);
    });

    it('given an archived interventie (archived_at not null), then it lands in NO group', () => {
      const e = ep({ id: 'e1', archived_at: '2026-05-15T10:00:00.000Z' });

      const result = groupEpisodes([e], TODAY);

      expect(result.interventiesActive).toEqual([]);
      expect(result.interventiesDone).toEqual([]);
      expect(result.totalActive).toBe(0);
      expect(result.totalDone).toBe(0);
    });
  });

  describe('groupEpisodes — levensgebeurtenis bucketing', () => {
    it('given a levensgebeurtenis with end_date null, then it lands in levensgebeurtenissenActive', () => {
      const e = ep({ id: 'e1', category: 'levensgebeurtenis', end_date: null });

      const result = groupEpisodes([e], TODAY);

      expect(result.levensgebeurtenissenActive).toEqual([e]);
    });

    it('given a closed-range levensgebeurtenis whose end_date is past, then it lands in levensgebeurtenissenDone', () => {
      const e = ep({
        id: 'e1',
        category: 'levensgebeurtenis',
        start_date: '2026-04-01',
        end_date: '2026-04-08',
      });

      const result = groupEpisodes([e], TODAY);

      expect(result.levensgebeurtenissenDone).toEqual([e]);
    });

    it('given a future-dated levensgebeurtenis (vakantie not yet started), then it lands in levensgebeurtenissenActive', () => {
      // Real case: book a vakantie 3 months out. Both start_date and
      // end_date in the future. "Active" semantics here means "not yet
      // completed" — which covers both ongoing AND upcoming.
      const e = ep({
        id: 'e1',
        category: 'levensgebeurtenis',
        start_date: '2026-07-15',
        end_date: '2026-07-22',
      });

      const result = groupEpisodes([e], TODAY);

      expect(result.levensgebeurtenissenActive).toEqual([e]);
    });
  });

  describe('groupEpisodes — mixed distribution', () => {
    it('given a mix across categories and statuses, then each lands in the right bucket', () => {
      const interventieActief = ep({
        id: 'ia',
        label: 'Coaching met Sarah',
        category: 'interventie',
        end_date: null,
      });
      const interventieKlaar = ep({
        id: 'ik',
        label: 'Citalopram afbouw',
        category: 'interventie',
        start_date: '2025-11-01',
        end_date: '2026-01-31',
      });
      const eventActief = ep({
        id: 'ea',
        label: 'Vakantie Texel',
        category: 'levensgebeurtenis',
        start_date: '2026-07-15',
        end_date: '2026-07-22',
      });
      const eventKlaar = ep({
        id: 'ek',
        label: 'Verhuizing',
        category: 'levensgebeurtenis',
        start_date: '2026-03-01',
        end_date: '2026-03-05',
      });
      const archived = ep({
        id: 'arch',
        archived_at: '2026-05-15T10:00:00.000Z',
      });

      const result = groupEpisodes(
        [interventieActief, interventieKlaar, eventActief, eventKlaar, archived],
        TODAY,
      );

      expect(result.interventiesActive).toEqual([interventieActief]);
      expect(result.interventiesDone).toEqual([interventieKlaar]);
      expect(result.levensgebeurtenissenActive).toEqual([eventActief]);
      expect(result.levensgebeurtenissenDone).toEqual([eventKlaar]);
      expect(result.totalActive).toBe(2);
      expect(result.totalDone).toBe(2);
    });
  });

  describe('groupEpisodes — sort order', () => {
    it('within an active bucket, sort by start_date DESC (most recent start first)', () => {
      const older = ep({ id: 'older', start_date: '2026-03-01' });
      const newer = ep({ id: 'newer', start_date: '2026-05-15' });

      const result = groupEpisodes([older, newer], TODAY);

      expect(result.interventiesActive.map((e) => e.id)).toEqual(['newer', 'older']);
    });

    it('within a done bucket, sort by end_date DESC (most recently ended first)', () => {
      const olderEnd = ep({
        id: 'olderEnd',
        start_date: '2025-11-01',
        end_date: '2026-01-15',
      });
      const newerEnd = ep({
        id: 'newerEnd',
        start_date: '2025-11-01',
        end_date: '2026-03-30',
      });

      const result = groupEpisodes([olderEnd, newerEnd], TODAY);

      expect(result.interventiesDone.map((e) => e.id)).toEqual(['newerEnd', 'olderEnd']);
    });
  });
});
