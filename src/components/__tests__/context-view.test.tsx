/** @vitest-environment jsdom */
import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { Episode } from '@/lib/domain/episode';

// Mock EpisodeFormSheet — we want to assert on its props (mode +
// category + initialEpisode) without rendering its full form internals.
// The form's behaviour is covered in episode-form-sheet.test.tsx.
const sheetMock = vi.hoisted(() => ({
  rendered: vi.fn(),
}));
vi.mock('../episode-form-sheet', () => ({
  EpisodeFormSheet: (props: {
    mode: 'create' | 'edit';
    category: 'interventie' | 'levensgebeurtenis';
    initialEpisode: Episode | null;
    open: boolean;
    onClose: () => void;
  }) => {
    sheetMock.rendered(props);
    return props.open ? (
      <div
        data-testid="episode-form-sheet"
        data-mode={props.mode}
        data-category={props.category}
        data-id={props.initialEpisode?.id ?? 'null'}
      >
        <button type="button" onClick={props.onClose}>
          mock-close
        </button>
      </div>
    ) : null;
  },
}));

import { ContextView } from '../context-view';

afterEach(() => {
  sheetMock.rendered.mockReset();
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

  });

  // ===========================================================================
  // Step-4: launcher buttons + tap-to-edit
  // ===========================================================================

  describe('launchers', () => {
    it('renders the "+ Nieuwe interventie" launcher button', () => {
      render(<ContextView episodes={[]} today={TODAY} />);

      expect(
        screen.getByRole('button', { name: '+ Nieuwe interventie' }),
      ).toBeInTheDocument();
    });

    it('renders the "+ Nieuwe periode" launcher button', () => {
      render(<ContextView episodes={[]} today={TODAY} />);

      expect(
        screen.getByRole('button', { name: '+ Nieuwe periode' }),
      ).toBeInTheDocument();
    });

    it('tapping "+ Nieuwe interventie" opens the sheet in create mode with category=interventie', async () => {
      const user = userEvent.setup();
      render(<ContextView episodes={[]} today={TODAY} />);

      // The sheet is rendered but closed (open=false) initially.
      expect(screen.queryByTestId('episode-form-sheet')).toBeNull();

      await user.click(
        screen.getByRole('button', { name: '+ Nieuwe interventie' }),
      );

      const sheet = screen.getByTestId('episode-form-sheet');
      expect(sheet.dataset.mode).toBe('create');
      expect(sheet.dataset.category).toBe('interventie');
      expect(sheet.dataset.id).toBe('null');
    });

    it('tapping "+ Nieuwe periode" opens the sheet in create mode with category=levensgebeurtenis', async () => {
      const user = userEvent.setup();
      render(<ContextView episodes={[]} today={TODAY} />);

      await user.click(
        screen.getByRole('button', { name: '+ Nieuwe periode' }),
      );

      const sheet = screen.getByTestId('episode-form-sheet');
      expect(sheet.dataset.mode).toBe('create');
      expect(sheet.dataset.category).toBe('levensgebeurtenis');
    });
  });

  describe('tap-to-edit on list items', () => {
    it('each list item is now a button (was non-interactive in step-3)', () => {
      render(
        <ContextView
          episodes={[ep({ id: 'a', label: 'Coaching met Sarah' })]}
          today={TODAY}
        />,
      );

      // Now the item should be a button.
      expect(
        screen.getByRole('button', { name: /coaching met sarah/i }),
      ).toBeInTheDocument();
    });

    it('the list-item button has an aria-label that reads the full episode summary', () => {
      // Per copy.context.form.listItemAriaLabel — "<label>, <start> tot
      // lopend, tik om te bewerken" for ongoing.
      render(
        <ContextView
          episodes={[
            ep({
              id: 'a',
              label: 'Coaching met Sarah',
              start_date: '2026-04-01',
              end_date: null,
            }),
          ]}
          today={TODAY}
        />,
      );

      const btn = screen.getByRole('button', { name: /coaching met sarah/i });
      expect(btn.getAttribute('aria-label')).toMatch(/coaching met sarah/i);
      expect(btn.getAttribute('aria-label')).toMatch(/lopend/i);
      expect(btn.getAttribute('aria-label')).toMatch(/tik om te bewerken/i);
    });

    it('tapping a list item opens the sheet in edit mode with the episode pre-filled', async () => {
      const user = userEvent.setup();
      const epActief = ep({
        id: 'ep-coach',
        label: 'Coaching met Sarah',
        category: 'interventie',
      });
      render(<ContextView episodes={[epActief]} today={TODAY} />);

      await user.click(
        screen.getByRole('button', { name: /coaching met sarah/i }),
      );

      const sheet = screen.getByTestId('episode-form-sheet');
      expect(sheet.dataset.mode).toBe('edit');
      expect(sheet.dataset.category).toBe('interventie');
      expect(sheet.dataset.id).toBe('ep-coach');
    });

    it('the sheet onClose handler resets sheet state to closed', async () => {
      const user = userEvent.setup();
      render(<ContextView episodes={[]} today={TODAY} />);

      // Open the sheet.
      await user.click(
        screen.getByRole('button', { name: '+ Nieuwe interventie' }),
      );
      expect(screen.getByTestId('episode-form-sheet')).toBeInTheDocument();

      // Close it.
      await user.click(screen.getByText('mock-close'));
      expect(screen.queryByTestId('episode-form-sheet')).toBeNull();
    });
  });
});
