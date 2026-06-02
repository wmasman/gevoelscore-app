/** @vitest-environment jsdom */

import { afterEach, describe, expect, it } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import { ContextView } from '../context-view';
import type { Episode } from '@/lib/domain/episode';

afterEach(() => {
  cleanup();
});

/** Factory for a minimal valid Episode (an active interventie). */
function ep(overrides: Partial<Episode> = {}): Episode {
  return {
    id: 'ep-default',
    label: 'Default label',
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

describe('<ContextView />', () => {
  describe('accessibility + structure', () => {
    it('the root section has aria-label="Context"', () => {
      render(<ContextView episodes={[]} today={TODAY} />);

      expect(screen.getByLabelText('Context')).toBeTruthy();
    });

    it('renders the Periodes section heading as an h2 (always present)', () => {
      // The Periodes h2 is always there — it's a section WITHIN Context,
      // independent of whether there are any periodes yet. Future v1.6
      // calendar bindings will add a sibling h2 next to it.
      render(<ContextView episodes={[]} today={TODAY} />);

      expect(screen.getByRole('heading', { level: 2, name: 'Periodes' })).toBeTruthy();
    });
  });

  describe('empty state (no periodes)', () => {
    it('given an empty list, renders the "Nog geen periodes." line inside the Periodes section', () => {
      render(<ContextView episodes={[]} today={TODAY} />);

      expect(screen.getByText('Nog geen periodes.')).toBeTruthy();
    });

    it('given an empty list, renders NO sub-group h3 headings', () => {
      render(<ContextView episodes={[]} today={TODAY} />);

      expect(screen.queryByRole('heading', { level: 3 })).toBeNull();
    });

    it('given only archived episodes, renders the empty-state line (archived treated as no-data)', () => {
      // Defense-in-depth: even if archived episodes somehow leak past
      // the API filter, the client-side groupEpisodes drops them. So
      // a list of only-archived behaves identically to an empty list.
      const archived = ep({ archived_at: '2026-05-01T10:00:00.000Z' });

      render(<ContextView episodes={[archived]} today={TODAY} />);

      expect(screen.getByText('Nog geen periodes.')).toBeTruthy();
      expect(screen.queryByRole('heading', { level: 3 })).toBeNull();
    });
  });

  describe('sub-group rendering', () => {
    it('given a single active interventie, renders ONLY the Interventies (actief) h3 sub-group', () => {
      render(
        <ContextView
          episodes={[ep({ id: 'a', label: 'Coaching met Sarah' })]}
          today={TODAY}
        />,
      );

      expect(screen.getByRole('heading', { level: 3, name: 'Interventies (actief)' })).toBeTruthy();
      expect(
        screen.queryByRole('heading', { level: 3, name: 'Interventies (afgerond)' }),
      ).toBeNull();
      expect(
        screen.queryByRole('heading', { level: 3, name: 'Levensgebeurtenissen (actief)' }),
      ).toBeNull();
      expect(
        screen.queryByRole('heading', { level: 3, name: 'Levensgebeurtenissen (afgerond)' }),
      ).toBeNull();
    });

    it('given a single afgerond levensgebeurtenis, renders ONLY the Levensgebeurtenissen (afgerond) h3 sub-group', () => {
      render(
        <ContextView
          episodes={[
            ep({
              id: 'b',
              label: 'Verhuizing',
              category: 'levensgebeurtenis',
              start_date: '2026-03-01',
              end_date: '2026-03-05',
            }),
          ]}
          today={TODAY}
        />,
      );

      expect(
        screen.getByRole('heading', { level: 3, name: 'Levensgebeurtenissen (afgerond)' }),
      ).toBeTruthy();
      expect(
        screen.queryByRole('heading', { level: 3, name: 'Interventies (actief)' }),
      ).toBeNull();
    });

    it('given a full mix, renders all four sub-groups in the documented order under the single Periodes h2', () => {
      const episodes = [
        ep({ id: 'ia', label: 'Coaching met Sarah', category: 'interventie' }),
        ep({
          id: 'ik',
          label: 'Citalopram afbouw',
          category: 'interventie',
          start_date: '2025-11-01',
          end_date: '2026-01-31',
        }),
        ep({
          id: 'ea',
          label: 'Vakantie Texel',
          category: 'levensgebeurtenis',
          start_date: '2026-07-15',
          end_date: '2026-07-22',
        }),
        ep({
          id: 'ek',
          label: 'Verhuizing',
          category: 'levensgebeurtenis',
          start_date: '2026-03-01',
          end_date: '2026-03-05',
        }),
      ];

      render(<ContextView episodes={episodes} today={TODAY} />);

      const h2 = screen.getAllByRole('heading', { level: 2 }).map((h) => h.textContent);
      const h3 = screen.getAllByRole('heading', { level: 3 }).map((h) => h.textContent);

      expect(h2).toEqual(['Periodes']);
      expect(h3).toEqual([
        'Interventies (actief)',
        'Interventies (afgerond)',
        'Levensgebeurtenissen (actief)',
        'Levensgebeurtenissen (afgerond)',
      ]);
    });
  });

  describe('list items', () => {
    it('renders the episode label inside the list', () => {
      render(
        <ContextView
          episodes={[ep({ id: 'a', label: 'Coaching met Sarah' })]}
          today={TODAY}
        />,
      );

      expect(screen.getByText('Coaching met Sarah')).toBeTruthy();
    });

    it('renders the date range as "<start> → lopend" for ongoing episodes', () => {
      render(
        <ContextView
          episodes={[ep({ id: 'a', start_date: '2026-04-01', end_date: null })]}
          today={TODAY}
        />,
      );

      const text = document.body.textContent ?? '';
      expect(text).toContain('→ lopend');
    });

    it('renders the date range as "<start> → <end>" for closed-range episodes', () => {
      render(
        <ContextView
          episodes={[
            ep({
              id: 'a',
              start_date: '2026-04-01',
              end_date: '2026-05-15',
            }),
          ]}
          today={TODAY}
        />,
      );

      const text = document.body.textContent ?? '';
      expect(text).toContain('→');
      expect(text).not.toContain('→ lopend');
    });

    it('list items are NOT buttons — no role=button on the rendered <li>', () => {
      // Defense-in-depth: items become tappable in step-4. Until then,
      // they must be non-interactive.
      render(
        <ContextView
          episodes={[ep({ id: 'a', label: 'Coaching met Sarah' })]}
          today={TODAY}
        />,
      );

      const buttons = screen.queryAllByRole('button');
      expect(buttons.length).toBe(0);
    });
  });
});
