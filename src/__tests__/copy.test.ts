import { describe, expect, it } from 'vitest';
import { copy } from '../copy';

describe('copy', () => {
  it('exposes the daily-entry feature surface in Dutch', () => {
    expect(copy.app.title).toBe('Gevoelscore');
    expect(copy.daily.score.label).toBe('Score');
    expect(copy.daily.note.label).toBe('Notitie');
    expect(copy.daily.tags.label).toBe('Tags');
    expect(copy.errors.notSaved).toMatch(/niet opgeslagen/i);
  });

  it('streak formatter handles 0, 1, plural', () => {
    expect(copy.timeline.streak(0)).toBe('0 dagen achter elkaar');
    expect(copy.timeline.streak(1)).toBe('1 dag achter elkaar');
    expect(copy.timeline.streak(7)).toBe('7 dagen achter elkaar');
  });

  it('top-level structure is stable (snapshot lock)', () => {
    expect(Object.keys(copy).sort()).toEqual(['app', 'daily', 'errors', 'timeline']);
    expect(Object.keys(copy.daily).sort()).toEqual(['note', 'score', 'tags']);
  });
});
