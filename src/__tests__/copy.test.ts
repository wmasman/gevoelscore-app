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
    expect(Object.keys(copy).sort()).toEqual([
      'app',
      'daily',
      'errors',
      'over',
      'settings',
      'timeline',
    ]);
    expect(Object.keys(copy.daily).sort()).toEqual(['note', 'score', 'tags']);
    expect(Object.keys(copy.over).sort()).toEqual([
      'cta',
      'email',
      'principles',
      'profile',
      'stat',
      'story',
      'subtitle',
      'title',
    ]);
  });

  it('exposes the public landing-page surface in Dutch', () => {
    expect(copy.over.title).toBe('Gevoelscore');
    expect(copy.over.email.address).toBe('Willem@brightpath-studio.nl');
    expect(copy.over.cta.heading).toMatch(/20 mensen/);
    expect(copy.over.principles.items).toHaveLength(4);
    expect(copy.over.profile.items).toHaveLength(4);
    expect(copy.over.stat.number).toBe('1.363');
    expect(copy.over.story.heading).toMatch(/waarom/i);
  });
});
