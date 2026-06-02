/** @vitest-environment jsdom */

import { afterEach, describe, expect, it } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import { PeriodesView } from '../periodes-view';
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

describe('<PeriodesView />', () => {
  describe('empty state', () => {
    it('given an empty list, renders the "Nog geen periodes." line', () => {
      render(<PeriodesView episodes={[]} today={TODAY} />);

      expect(screen.getByText('Nog geen periodes.')).toBeTruthy();
    });

    it('given an empty list, renders NO section headers', () => {
      render(<PeriodesView episodes={[]} today={TODAY} />);

      expect(screen.queryByRole('heading', { level: 2 })).toBeNull();
    });

    it('given only archived episodes, renders the empty-state line (archived treated as no-data)', () => {
      // Defense-in-depth: even if archived episodes somehow leak past
      // the API filter, the client-side groupEpisodes drops them. So
      // a list of only-archived behaves identically to an empty list.
      const archived = ep({ archived_at: '2026-05-01T10:00:00.000Z' });

      render(<PeriodesView episodes={[archived]} today={TODAY} />);

      expect(screen.getByText('Nog geen periodes.')).toBeTruthy();
      expect(screen.queryByRole('heading', { level: 2 })).toBeNull();
    });
  });

  describe('section rendering', () => {
    it('given a single active interventie, renders ONLY the Interventies (actief) section', () => {
      render(
        <PeriodesView
          episodes={[ep({ id: 'a', label: 'Coaching met Sarah' })]}
          today={TODAY}
        />,
      );

      expect(screen.getByRole('heading', { level: 2, name: 'Interventies (actief)' })).toBeTruthy();
      expect(
        screen.queryByRole('heading', { level: 2, name: 'Interventies (afgerond)' }),
      ).toBeNull();
      expect(
        screen.queryByRole('heading', { level: 2, name: 'Levensgebeurtenissen (actief)' }),
      ).toBeNull();
      expect(
        screen.queryByRole('heading', { level: 2, name: 'Levensgebeurtenissen (afgerond)' }),
      ).toBeNull();
    });

    it('given a single afgerond levensgebeurtenis, renders ONLY the Levensgebeurtenissen (afgerond) section', () => {
      render(
        <PeriodesView
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
        screen.getByRole('heading', { level: 2, name: 'Levensgebeurtenissen (afgerond)' }),
      ).toBeTruthy();
      expect(
        screen.queryByRole('heading', { level: 2, name: 'Interventies (actief)' }),
      ).toBeNull();
    });

    it('given a full mix, renders all four sections in the documented order', () => {
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

      render(<PeriodesView episodes={episodes} today={TODAY} />);

      const headings = screen
        .getAllByRole('heading', { level: 2 })
        .map((h) => h.textContent);

      expect(headings).toEqual([
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
        <PeriodesView
          episodes={[ep({ id: 'a', label: 'Coaching met Sarah' })]}
          today={TODAY}
        />,
      );

      expect(screen.getByText('Coaching met Sarah')).toBeTruthy();
    });

    it('renders the date range as "<start> → lopend" for ongoing episodes', () => {
      render(
        <PeriodesView
          episodes={[ep({ id: 'a', start_date: '2026-04-01', end_date: null })]}
          today={TODAY}
        />,
      );

      // formatDateDutch may format as "1 apr 2026" or similar; we just
      // assert the "→ lopend" suffix is present somewhere in the rendered
      // text. The exact format is locked elsewhere; here we only check
      // the dateRange composition.
      const text = document.body.textContent ?? '';
      expect(text).toContain('→ lopend');
    });

    it('renders the date range as "<start> → <end>" for closed-range episodes', () => {
      render(
        <PeriodesView
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

      // For closed range we expect TWO Dutch dates separated by →. Just
      // assert that there's a "→" present AND no "lopend" suffix.
      const text = document.body.textContent ?? '';
      expect(text).toContain('→');
      expect(text).not.toContain('→ lopend');
    });

    it('list items are NOT buttons — no role=button on the rendered <li>', () => {
      // Defense-in-depth for AC13: items become tappable in step-4.
      // Until then, they must be non-interactive.
      render(
        <PeriodesView
          episodes={[ep({ id: 'a', label: 'Coaching met Sarah' })]}
          today={TODAY}
        />,
      );

      const buttons = screen.queryAllByRole('button');
      // The empty-state path has 0 buttons; the populated path has 0
      // buttons. PeriodesView in step-3 does not render any
      // interactive element.
      expect(buttons.length).toBe(0);
    });
  });

  describe('accessibility', () => {
    it('the root section has aria-label="Periodes"', () => {
      render(<PeriodesView episodes={[]} today={TODAY} />);

      expect(screen.getByLabelText('Periodes')).toBeTruthy();
    });
  });
});
