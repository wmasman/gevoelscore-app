import { describe, expect, it } from 'vitest';
import type { DayEntry } from '../day-entry';
import type { Episode } from '../episode';
import type { Tag } from '../tag';
import { computeLinkedTagDots } from '../linked-tag-dots';

function ep(overrides: Partial<Episode> = {}): Episode {
  return {
    id: 'ep-coaching',
    label: 'Coaching met Sarah',
    category: 'interventie',
    start_date: '2026-05-01',
    end_date: '2026-05-31',
    description: null,
    calendar_binding: null,
    archived_at: null,
    created_at: '2026-05-01T00:00:00.000Z',
    updated_at: '2026-05-01T00:00:00.000Z',
    ...overrides,
  };
}

function tag(overrides: Partial<Tag> = {}): Tag {
  return {
    id: 'tag-pacing',
    label: 'pacing',
    category: 'mentaal',
    project_id: null,
    parent_episode_id: null,
    usage_count: 0,
    archived_at: null,
    created_at: '2026-05-01T00:00:00.000Z',
    ...overrides,
  };
}

function entry(overrides: Partial<DayEntry> = {}): DayEntry {
  return {
    date: '2026-05-05',
    score: 6,
    note: null,
    tag_ids: [],
    sub_scores: null,
    sleep_hours: null,
    special_event: null,
    project_entry_ids: [],
    calendar_event_ids: [],
    garmin: null,
    health: null,
    weather: null,
    derived: null,
    created_at: '2026-05-05T00:00:00.000Z',
    updated_at: '2026-05-05T00:00:00.000Z',
    ...overrides,
  };
}

describe('computeLinkedTagDots', () => {
  it('returns an empty array when there are no entries', () => {
    const result = computeLinkedTagDots(
      [],
      [tag({ id: 't1', parent_episode_id: 'ep-coaching' })],
      [ep()],
      '2026-05-01',
      '2026-05-31',
    );
    expect(result).toEqual([]);
  });

  it('emits a dot for a tag linked to a visible episode on an in-range day', () => {
    const result = computeLinkedTagDots(
      [entry({date: '2026-05-05', tag_ids: ['t1'] })],
      [tag({ id: 't1', parent_episode_id: 'ep-coaching' })],
      [ep({ id: 'ep-coaching' })],
      '2026-05-01',
      '2026-05-31',
    );
    expect(result).toHaveLength(1);
    expect(result[0]).toEqual({
      date: '2026-05-05',
      episodeId: 'ep-coaching',
      tagId: 't1',
      rowIndex: 0,
    });
  });

  it('skips tags with parent_episode_id=null (standalone tags)', () => {
    const result = computeLinkedTagDots(
      [entry({ tag_ids: ['t-standalone'] })],
      [tag({ id: 't-standalone', parent_episode_id: null })],
      [ep()],
      '2026-05-01',
      '2026-05-31',
    );
    expect(result).toEqual([]);
  });

  it('skips tags whose parent episode is archived', () => {
    const result = computeLinkedTagDots(
      [entry({ tag_ids: ['t1'] })],
      [tag({ id: 't1', parent_episode_id: 'ep-archived' })],
      [
        ep({
          id: 'ep-archived',
          archived_at: '2026-05-15T00:00:00.000Z',
        }),
      ],
      '2026-05-01',
      '2026-05-31',
    );
    expect(result).toEqual([]);
  });

  it('skips tags whose parent episode is out of range', () => {
    const result = computeLinkedTagDots(
      [entry({ tag_ids: ['t1'] })],
      [tag({ id: 't1', parent_episode_id: 'ep-far-past' })],
      [
        ep({
          id: 'ep-far-past',
          start_date: '2026-01-01',
          end_date: '2026-01-31',
        }),
      ],
      '2026-05-01',
      '2026-05-31',
    );
    expect(result).toEqual([]);
  });

  it('emits multiple dots when one day has multiple linked tags to different visible episodes', () => {
    const result = computeLinkedTagDots(
      [entry({date: '2026-05-08', tag_ids: ['t1', 't2'] })],
      [
        tag({ id: 't1', parent_episode_id: 'ep-A' }),
        tag({ id: 't2', parent_episode_id: 'ep-B' }),
      ],
      [
        ep({
          id: 'ep-A',
          start_date: '2026-05-01',
          end_date: '2026-05-10',
        }),
        ep({
          id: 'ep-B',
          start_date: '2026-05-05',
          end_date: '2026-05-15',
        }),
      ],
      '2026-05-01',
      '2026-05-31',
    );
    expect(result).toHaveLength(2);
    const byTag = Object.fromEntries(result.map((d) => [d.tagId, d]));
    expect(byTag.t1?.episodeId).toBe('ep-A');
    expect(byTag.t1?.rowIndex).toBe(0);
    expect(byTag.t2?.episodeId).toBe('ep-B');
    expect(byTag.t2?.rowIndex).toBe(1);
  });

  it('does NOT emit dots for tags in the corpus that no entry references in range', () => {
    const result = computeLinkedTagDots(
      [entry({ tag_ids: [] })],
      [tag({ id: 't-orphan', parent_episode_id: 'ep-coaching' })],
      [ep({ id: 'ep-coaching' })],
      '2026-05-01',
      '2026-05-31',
    );
    expect(result).toEqual([]);
  });

  it('skips entries whose date is outside the visible range', () => {
    const result = computeLinkedTagDots(
      [entry({ date: '2026-04-15', tag_ids: ['t1'] })],
      [tag({ id: 't1', parent_episode_id: 'ep-coaching' })],
      [ep({ id: 'ep-coaching' })],
      '2026-05-01',
      '2026-05-31',
    );
    expect(result).toEqual([]);
  });
});
