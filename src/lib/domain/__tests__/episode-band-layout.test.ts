import { describe, expect, it } from 'vitest';
import type { Episode } from '../episode';
import {
  computeEpisodeBandLayout,
  type EpisodeBand,
} from '../episode-band-layout';

function ep(overrides: Partial<Episode> = {}): Episode {
  return {
    id: 'ep-default',
    label: 'Default',
    category: 'interventie',
    start_date: '2026-05-01',
    end_date: '2026-05-10',
    description: null,
    calendar_binding: null,
    archived_at: null,
    created_at: '2026-05-01T00:00:00.000Z',
    updated_at: '2026-05-01T00:00:00.000Z',
    ...overrides,
  };
}

describe('computeEpisodeBandLayout', () => {
  describe('empty / no-overlap cases', () => {
    it('returns an empty array for an empty input', () => {
      const result = computeEpisodeBandLayout([], '2026-05-01', '2026-05-31');
      expect(result).toEqual([]);
    });

    it('skips episodes whose range is entirely before the visible range', () => {
      const result = computeEpisodeBandLayout(
        [ep({ start_date: '2026-04-01', end_date: '2026-04-10' })],
        '2026-05-01',
        '2026-05-31',
      );
      expect(result).toEqual([]);
    });

    it('skips episodes whose range is entirely after the visible range', () => {
      const result = computeEpisodeBandLayout(
        [ep({ start_date: '2026-06-01', end_date: '2026-06-10' })],
        '2026-05-01',
        '2026-05-31',
      );
      expect(result).toEqual([]);
    });

    it('skips archived episodes (defensive — API filters them upstream too)', () => {
      const result = computeEpisodeBandLayout(
        [ep({ archived_at: '2026-05-15T00:00:00.000Z' })],
        '2026-05-01',
        '2026-05-31',
      );
      expect(result).toEqual([]);
    });
  });

  describe('single-episode clamping', () => {
    it('places a single episode fully inside the range in row 0 with unclamped dates', () => {
      const result = computeEpisodeBandLayout(
        [ep({ id: 'a', start_date: '2026-05-05', end_date: '2026-05-10' })],
        '2026-05-01',
        '2026-05-31',
      );
      expect(result).toEqual<EpisodeBand[]>([
        {
          episode: expect.objectContaining({ id: 'a' }),
          rowIndex: 0,
          xStartDate: '2026-05-05',
          xEndDate: '2026-05-10',
        },
      ]);
    });

    it('clamps xStartDate to from when the episode starts before from', () => {
      const result = computeEpisodeBandLayout(
        [ep({ start_date: '2026-04-15', end_date: '2026-05-10' })],
        '2026-05-01',
        '2026-05-31',
      );
      expect(result[0]?.xStartDate).toBe('2026-05-01');
      expect(result[0]?.xEndDate).toBe('2026-05-10');
    });

    it('clamps xEndDate to to when the episode ends after to', () => {
      const result = computeEpisodeBandLayout(
        [ep({ start_date: '2026-05-25', end_date: '2026-06-10' })],
        '2026-05-01',
        '2026-05-31',
      );
      expect(result[0]?.xStartDate).toBe('2026-05-25');
      expect(result[0]?.xEndDate).toBe('2026-05-31');
    });

    it('treats end_date=null (lopend) as clamped to to (right edge)', () => {
      const result = computeEpisodeBandLayout(
        [ep({ start_date: '2026-05-15', end_date: null })],
        '2026-05-01',
        '2026-05-31',
      );
      expect(result[0]?.xStartDate).toBe('2026-05-15');
      expect(result[0]?.xEndDate).toBe('2026-05-31');
    });
  });

  describe('stacking', () => {
    it('places two non-overlapping episodes both in row 0', () => {
      const result = computeEpisodeBandLayout(
        [
          ep({ id: 'a', start_date: '2026-05-01', end_date: '2026-05-05' }),
          ep({ id: 'b', start_date: '2026-05-10', end_date: '2026-05-15' }),
        ],
        '2026-05-01',
        '2026-05-31',
      );
      const byId = Object.fromEntries(result.map((r) => [r.episode.id, r]));
      expect(byId.a?.rowIndex).toBe(0);
      expect(byId.b?.rowIndex).toBe(0);
    });

    it('stacks two overlapping episodes into rows 0 and 1', () => {
      const result = computeEpisodeBandLayout(
        [
          ep({ id: 'a', start_date: '2026-05-01', end_date: '2026-05-15' }),
          ep({ id: 'b', start_date: '2026-05-10', end_date: '2026-05-20' }),
        ],
        '2026-05-01',
        '2026-05-31',
      );
      const byId = Object.fromEntries(result.map((r) => [r.episode.id, r]));
      expect(byId.a?.rowIndex).toBe(0);
      expect(byId.b?.rowIndex).toBe(1);
    });

    it('greedy stack: A(1-10) B(5-15) C(8-20) → A:0, B:1, C:2', () => {
      const result = computeEpisodeBandLayout(
        [
          ep({ id: 'a', start_date: '2026-05-01', end_date: '2026-05-10' }),
          ep({ id: 'b', start_date: '2026-05-05', end_date: '2026-05-15' }),
          ep({ id: 'c', start_date: '2026-05-08', end_date: '2026-05-20' }),
        ],
        '2026-05-01',
        '2026-05-31',
      );
      const byId = Object.fromEntries(result.map((r) => [r.episode.id, r]));
      expect(byId.a?.rowIndex).toBe(0);
      expect(byId.b?.rowIndex).toBe(1);
      expect(byId.c?.rowIndex).toBe(2);
    });

    it('greedy stack reuses row 0 when an earlier band has ended: A(1-5) B(6-10) C(3-8) → A:0, B:0, C:1', () => {
      const result = computeEpisodeBandLayout(
        [
          ep({ id: 'a', start_date: '2026-05-01', end_date: '2026-05-05' }),
          ep({ id: 'b', start_date: '2026-05-06', end_date: '2026-05-10' }),
          ep({ id: 'c', start_date: '2026-05-03', end_date: '2026-05-08' }),
        ],
        '2026-05-01',
        '2026-05-31',
      );
      const byId = Object.fromEntries(result.map((r) => [r.episode.id, r]));
      expect(byId.a?.rowIndex).toBe(0);
      expect(byId.b?.rowIndex).toBe(0);
      expect(byId.c?.rowIndex).toBe(1);
    });
  });

  describe('determinism', () => {
    it('produces identical output across repeated calls with the same input', () => {
      const input = [
        ep({ id: 'a', start_date: '2026-05-01', end_date: '2026-05-10' }),
        ep({ id: 'b', start_date: '2026-05-05', end_date: '2026-05-15' }),
      ];
      const a = computeEpisodeBandLayout(input, '2026-05-01', '2026-05-31');
      const b = computeEpisodeBandLayout(input, '2026-05-01', '2026-05-31');
      expect(a).toEqual(b);
    });

    it('breaks start_date ties by id lexicographic order', () => {
      // Two episodes starting the same day, same end. Both want row 0.
      // The one with the earlier id (lex) takes row 0; the other goes to
      // row 1. Determinism is the contract; the specific tie-break rule
      // is documented so the test serves as a spec.
      const result = computeEpisodeBandLayout(
        [
          ep({ id: 'zz', start_date: '2026-05-01', end_date: '2026-05-10' }),
          ep({ id: 'aa', start_date: '2026-05-01', end_date: '2026-05-10' }),
        ],
        '2026-05-01',
        '2026-05-31',
      );
      const byId = Object.fromEntries(result.map((r) => [r.episode.id, r]));
      expect(byId.aa?.rowIndex).toBe(0);
      expect(byId.zz?.rowIndex).toBe(1);
    });
  });
});
