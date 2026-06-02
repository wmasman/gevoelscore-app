import { describe, expect, it } from 'vitest';
import type { DayEntry } from '../day-entry';
import type { Tag } from '../tag';
import { compareTagsForPicker, computeRecencyByTagId } from '../tag-sort';

function entry(date: string, tagIds: string[]): DayEntry {
  return {
    date,
    score: 5 as DayEntry['score'],
    note: null,
    tag_ids: tagIds,
    sub_scores: null,
    sleep_hours: null,
    special_event: null,
    project_entry_ids: [],
    calendar_event_ids: [],
    garmin: null,
    health: null,
    weather: null,
    derived: null,
    created_at: `${date}T08:00:00.000Z`,
    updated_at: `${date}T08:00:00.000Z`,
  };
}

function tag(
  id: string,
  label: string,
  usageCount = 0,
  category: Tag['category'] = 'mentaal',
): Tag {
  return {
    id,
    label,
    category,
    project_id: category === 'project' ? 'p-1' : null,
    parent_episode_id: null,
    usage_count: usageCount,
    archived_at: null,
    created_at: '2026-01-01T00:00:00.000Z',
  };
}

describe('computeRecencyByTagId', () => {
  it('returns an empty object for an empty entries array', () => {
    expect(computeRecencyByTagId([])).toEqual({});
  });

  it('returns the date for a single entry with a single tag_id', () => {
    const result = computeRecencyByTagId([entry('2026-05-28', ['t-1'])]);
    expect(result).toEqual({ 't-1': '2026-05-28' });
  });

  it('returns the LATEST date when a tag-id appears on multiple days', () => {
    const result = computeRecencyByTagId([
      entry('2026-05-20', ['t-1']),
      entry('2026-05-28', ['t-1']),
      entry('2026-05-15', ['t-1']),
    ]);
    expect(result['t-1']).toBe('2026-05-28');
  });

  it('omits tag-ids that never appear in the window', () => {
    const result = computeRecencyByTagId([entry('2026-05-28', ['t-1'])]);
    expect(result['t-2']).toBeUndefined();
  });

  it('handles entries with empty tag_ids arrays gracefully', () => {
    const result = computeRecencyByTagId([
      entry('2026-05-28', []),
      entry('2026-05-27', ['t-1']),
    ]);
    expect(result).toEqual({ 't-1': '2026-05-27' });
  });

  it('output is independent of input order', () => {
    const ascending = computeRecencyByTagId([
      entry('2026-05-20', ['t-1']),
      entry('2026-05-25', ['t-1']),
      entry('2026-05-28', ['t-1']),
    ]);
    const descending = computeRecencyByTagId([
      entry('2026-05-28', ['t-1']),
      entry('2026-05-25', ['t-1']),
      entry('2026-05-20', ['t-1']),
    ]);
    expect(ascending).toEqual(descending);
  });

  it('tracks multiple tag-ids in the same entry independently', () => {
    const result = computeRecencyByTagId([
      entry('2026-05-28', ['t-1', 't-2', 't-3']),
      entry('2026-05-27', ['t-2']),
    ]);
    expect(result).toEqual({
      't-1': '2026-05-28',
      't-2': '2026-05-28',
      't-3': '2026-05-28',
    });
  });
});

describe('compareTagsForPicker', () => {
  it('tag with recency sorts BEFORE tag without recency', () => {
    const recent = tag('t-1', 'a', 0);
    const stale = tag('t-2', 'b', 0);
    const recency = { 't-1': '2026-05-28' };
    expect(compareTagsForPicker(recent, stale, recency)).toBeLessThan(0);
    expect(compareTagsForPicker(stale, recent, recency)).toBeGreaterThan(0);
  });

  it('more-recent tag sorts BEFORE less-recent tag', () => {
    const a = tag('t-1', 'a', 0);
    const b = tag('t-2', 'b', 0);
    const recency = { 't-1': '2026-05-28', 't-2': '2026-05-20' };
    expect(compareTagsForPicker(a, b, recency)).toBeLessThan(0);
    expect(compareTagsForPicker(b, a, recency)).toBeGreaterThan(0);
  });

  it('same recency date → higher usage_count sorts first', () => {
    const high = tag('t-1', 'a', 10);
    const low = tag('t-2', 'b', 1);
    const recency = { 't-1': '2026-05-28', 't-2': '2026-05-28' };
    expect(compareTagsForPicker(high, low, recency)).toBeLessThan(0);
    expect(compareTagsForPicker(low, high, recency)).toBeGreaterThan(0);
  });

  it('same recency + same usage_count → alphabetical ASC, case-insensitive', () => {
    const aLabel = tag('t-1', 'apple', 5);
    const bLabel = tag('t-2', 'Banana', 5);
    const recency = { 't-1': '2026-05-28', 't-2': '2026-05-28' };
    expect(compareTagsForPicker(aLabel, bLabel, recency)).toBeLessThan(0);
  });

  it('both no-recency → tiebreak on usage_count DESC, then alphabetical', () => {
    const heavyUsed = tag('t-1', 'zeta', 7);
    const lightUsed = tag('t-2', 'alpha', 1);
    // Both are stale (not in recency map).
    const recency: Record<string, string> = {};
    expect(compareTagsForPicker(heavyUsed, lightUsed, recency)).toBeLessThan(0);
  });

  it('produces a stable sort when fed to Array.prototype.sort', () => {
    // Smoke test: a list with a mix of recency/no-recency and ties.
    const recency = {
      't-2': '2026-05-28',
      't-3': '2026-05-25',
      't-5': '2026-05-28',
    };
    const list = [
      tag('t-1', 'cobalt', 3),
      tag('t-2', 'helder', 0),
      tag('t-3', 'kalm', 5),
      tag('t-4', 'aurora', 7),
      tag('t-5', 'apex', 0),
    ];
    list.sort((a, b) => compareTagsForPicker(a, b, recency));
    // Expected order:
    //   - t-5 (apex)   — recency 2026-05-28, usage 0
    //   - t-2 (helder) — recency 2026-05-28, usage 0, alphabetical after apex
    //   - t-3 (kalm)   — recency 2026-05-25
    //   - t-4 (aurora) — no recency, usage 7
    //   - t-1 (cobalt) — no recency, usage 3
    expect(list.map((t) => t.id)).toEqual(['t-5', 't-2', 't-3', 't-4', 't-1']);
  });
});
