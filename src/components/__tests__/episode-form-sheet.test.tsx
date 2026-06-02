// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { Episode } from '@/lib/domain/episode';

// Mock the BottomSheet primitive — render children when open. Isolates
// form behaviour from the sheet's portal + animation + drag-to-dismiss.
vi.mock('@/components/lab/bottom-sheet', () => ({
  BottomSheet: ({
    open,
    ariaLabel,
    children,
  }: {
    open: boolean;
    ariaLabel: string;
    onClose: () => void;
    children: React.ReactNode;
  }) =>
    open ? (
      <div role="dialog" aria-label={ariaLabel}>
        {children}
      </div>
    ) : null,
}));

// Mock the hook — full control over what each method returns + observe calls.
const hookMocks = vi.hoisted(() => ({
  create: vi.fn(),
  update: vi.fn(),
  archive: vi.fn(),
  status: 'idle' as 'idle' | 'saving' | 'saved' | 'error',
  lastError: null as string | null,
}));
vi.mock('@/hooks/use-episode-upsert', () => ({
  useEpisodeUpsert: () => hookMocks,
}));

import { EpisodeFormSheet } from '../episode-form-sheet';

const TODAY = '2026-06-02';

const HAPPY_EPISODE: Episode = {
  id: 'ep-01HQ',
  label: 'Coaching met Sarah',
  category: 'interventie',
  start_date: '2026-04-01',
  end_date: null,
  description: 'Wekelijks',
  calendar_binding: null,
  archived_at: null,
  created_at: '2026-04-01T08:00:00.000Z',
  updated_at: '2026-04-01T08:00:00.000Z',
};

beforeEach(() => {
  hookMocks.create.mockReset().mockResolvedValue(HAPPY_EPISODE);
  hookMocks.update.mockReset().mockResolvedValue(HAPPY_EPISODE);
  hookMocks.archive.mockReset().mockResolvedValue(HAPPY_EPISODE);
  hookMocks.status = 'idle';
  hookMocks.lastError = null;
});
afterEach(() => {
  cleanup();
});

describe('<EpisodeFormSheet />', () => {
  // ===========================================================================
  // Create mode
  // ===========================================================================

  describe('create mode', () => {
    it('renders title "Nieuwe interventie" when mode=create + category=interventie', () => {
      const onClose = vi.fn();
      const onSaved = vi.fn();
      const onArchived = vi.fn();
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={onClose}
          onSaved={onSaved}
          onArchived={onArchived}
        />,
      );

      expect(
        screen.getByRole('heading', { name: 'Nieuwe interventie' }),
      ).toBeInTheDocument();
    });

    it('renders title "Nieuwe periode" when category=levensgebeurtenis', () => {
      render(
        <EpisodeFormSheet
          mode="create"
          category="levensgebeurtenis"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      expect(
        screen.getByRole('heading', { name: 'Nieuwe periode' }),
      ).toBeInTheDocument();
    });

    it('start_date input defaults to today', () => {
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      const startInput = screen.getByLabelText(/begindatum/i) as HTMLInputElement;
      expect(startInput.value).toBe(TODAY);
    });

    it('lopend toggle defaults to ON, so end_date input is HIDDEN', () => {
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      const toggle = screen.getByLabelText(/lopend/i) as HTMLInputElement;
      expect(toggle.checked).toBe(true);
      expect(screen.queryByLabelText(/^einddatum/i)).toBeNull();
    });

    it('toggling lopend OFF reveals the end_date input', async () => {
      const user = userEvent.setup();
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      await user.click(screen.getByLabelText(/lopend/i));

      expect(screen.getByLabelText(/^einddatum/i)).toBeInTheDocument();
    });

    it('archive button is NOT rendered in create mode', () => {
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      expect(screen.queryByRole('button', { name: /archiveer/i })).toBeNull();
    });

    it('valid form + tap Bewaar → calls hook.create with the normalised payload', async () => {
      const user = userEvent.setup();
      const onSaved = vi.fn();
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={onSaved}
          onArchived={vi.fn()}
        />,
      );

      await user.type(screen.getByLabelText(/naam/i), '  Coaching met Sarah  ');
      await user.click(screen.getByRole('button', { name: /bewaar/i }));

      await waitFor(() => {
        expect(hookMocks.create).toHaveBeenCalledTimes(1);
      });
      expect(hookMocks.create).toHaveBeenCalledWith({
        label: 'Coaching met Sarah', // trimmed
        category: 'interventie',
        start_date: TODAY,
        end_date: null,
        description: null,
      });
      await waitFor(() => expect(onSaved).toHaveBeenCalledWith(HAPPY_EPISODE));
    });

    it('submit with empty label → hook.create NOT called + inline error visible', async () => {
      const user = userEvent.setup();
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      // Don't type anything; Bewaar is initially disabled, but tap anyway.
      await user.click(screen.getByRole('button', { name: /bewaar/i }));

      expect(hookMocks.create).not.toHaveBeenCalled();
      // Submit-attempt forces the label-error visible.
      expect(
        screen.getByText('Geef een naam.'),
      ).toBeInTheDocument();
    });

    it('end_date < start_date → inline error + submit NOT fired', async () => {
      const user = userEvent.setup();
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      await user.type(screen.getByLabelText(/naam/i), 'X');
      // Set start_date and end_date in reverse order.
      const startInput = screen.getByLabelText(/begindatum/i) as HTMLInputElement;
      await user.clear(startInput);
      await user.type(startInput, '2026-07-15');
      await user.click(screen.getByLabelText(/lopend/i)); // toggle OFF
      const endInput = screen.getByLabelText(/^einddatum/i) as HTMLInputElement;
      await user.type(endInput, '2026-06-01');

      await user.click(screen.getByRole('button', { name: /bewaar/i }));

      expect(hookMocks.create).not.toHaveBeenCalled();
      expect(
        screen.getByText('Einddatum moet ná de begindatum liggen.'),
      ).toBeInTheDocument();
    });

    it('server error → sheet stays open + serverError banner visible', () => {
      // Mock hook to leave lastError set after a failed create.
      hookMocks.lastError = 'server_error';
      const onSaved = vi.fn();
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={onSaved}
          onArchived={vi.fn()}
        />,
      );

      expect(
        screen.getByText('Opslaan lukte niet, probeer opnieuw.'),
      ).toBeInTheDocument();
      // onSaved must NOT have been invoked.
      expect(onSaved).not.toHaveBeenCalled();
    });
  });

  // ===========================================================================
  // Edit mode
  // ===========================================================================

  describe('edit mode', () => {
    it('pre-fills label / start_date / description from initialEpisode', () => {
      render(
        <EpisodeFormSheet
          mode="edit"
          category="interventie"
          initialEpisode={HAPPY_EPISODE}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      expect((screen.getByLabelText(/naam/i) as HTMLInputElement).value).toBe(
        'Coaching met Sarah',
      );
      expect((screen.getByLabelText(/begindatum/i) as HTMLInputElement).value).toBe(
        '2026-04-01',
      );
      expect((screen.getByLabelText(/beschrijving/i) as HTMLTextAreaElement).value).toBe(
        'Wekelijks',
      );
    });

    it('lopend toggle is ON when initialEpisode.end_date is null', () => {
      render(
        <EpisodeFormSheet
          mode="edit"
          category="interventie"
          initialEpisode={HAPPY_EPISODE}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      expect(
        (screen.getByLabelText(/lopend/i) as HTMLInputElement).checked,
      ).toBe(true);
      expect(screen.queryByLabelText(/^einddatum/i)).toBeNull();
    });

    it('lopend toggle is OFF when initialEpisode.end_date is set + end_date input pre-filled', () => {
      const closedRange: Episode = {
        ...HAPPY_EPISODE,
        end_date: '2026-06-01',
      };
      render(
        <EpisodeFormSheet
          mode="edit"
          category="interventie"
          initialEpisode={closedRange}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      expect(
        (screen.getByLabelText(/lopend/i) as HTMLInputElement).checked,
      ).toBe(false);
      expect(
        (screen.getByLabelText(/^einddatum/i) as HTMLInputElement).value,
      ).toBe('2026-06-01');
    });

    it('archive button IS rendered in edit mode', () => {
      render(
        <EpisodeFormSheet
          mode="edit"
          category="interventie"
          initialEpisode={HAPPY_EPISODE}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      expect(
        screen.getByRole('button', { name: /archiveer/i }),
      ).toBeInTheDocument();
    });

    it('tapping archive → calls hook.archive(id) + onArchived fired', async () => {
      const user = userEvent.setup();
      const onArchived = vi.fn();
      render(
        <EpisodeFormSheet
          mode="edit"
          category="interventie"
          initialEpisode={HAPPY_EPISODE}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={onArchived}
        />,
      );

      await user.click(screen.getByRole('button', { name: /archiveer/i }));

      await waitFor(() => {
        expect(hookMocks.archive).toHaveBeenCalledWith('ep-01HQ');
      });
      await waitFor(() => expect(onArchived).toHaveBeenCalledWith(HAPPY_EPISODE));
    });

    it('valid edit + tap Bewaar → calls hook.update with the form payload', async () => {
      const user = userEvent.setup();
      const onSaved = vi.fn();
      render(
        <EpisodeFormSheet
          mode="edit"
          category="interventie"
          initialEpisode={HAPPY_EPISODE}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={onSaved}
          onArchived={vi.fn()}
        />,
      );

      // Change description.
      const desc = screen.getByLabelText(/beschrijving/i) as HTMLTextAreaElement;
      await user.clear(desc);
      await user.type(desc, 'Nieuwe tekst');

      await user.click(screen.getByRole('button', { name: /bewaar/i }));

      await waitFor(() => {
        expect(hookMocks.update).toHaveBeenCalledWith('ep-01HQ', {
          label: 'Coaching met Sarah',
          category: 'interventie',
          start_date: '2026-04-01',
          end_date: null,
          description: 'Nieuwe tekst',
        });
      });
      await waitFor(() => expect(onSaved).toHaveBeenCalledWith(HAPPY_EPISODE));
    });
  });

  // ===========================================================================
  // Dismiss
  // ===========================================================================

  describe('dismiss', () => {
    it('tapping the close ✕ → onClose fires + no save attempted', async () => {
      const user = userEvent.setup();
      const onClose = vi.fn();
      const onSaved = vi.fn();
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={onClose}
          onSaved={onSaved}
          onArchived={vi.fn()}
        />,
      );

      await user.type(screen.getByLabelText(/naam/i), 'Half-typed');
      await user.click(screen.getByRole('button', { name: /sluit/i }));

      expect(onClose).toHaveBeenCalledTimes(1);
      expect(hookMocks.create).not.toHaveBeenCalled();
      expect(onSaved).not.toHaveBeenCalled();
    });
  });

  // ===========================================================================
  // Accessibility
  // ===========================================================================

  describe('accessibility', () => {
    it('label input has aria-required="true"', () => {
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      const labelInput = screen.getByLabelText(/naam/i);
      expect(labelInput).toHaveAttribute('aria-required', 'true');
    });

    it('the dialog has aria-label="Periode bewerken"', () => {
      render(
        <EpisodeFormSheet
          mode="create"
          category="interventie"
          initialEpisode={null}
          today={TODAY}
          open
          onClose={vi.fn()}
          onSaved={vi.fn()}
          onArchived={vi.fn()}
        />,
      );

      expect(screen.getByRole('dialog', { name: 'Periode bewerken' })).toBeInTheDocument();
    });
  });
});
