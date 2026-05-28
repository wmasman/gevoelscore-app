// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Per docs/architecture/frontend-conventions.md "Common gotchas": fake
// timers only inside specific tests that advance time. Tests using userEvent
// + real interactions stay on real timers.

const hookMocks = vi.hoisted(() => ({
  save: vi.fn(),
}));

vi.mock('@/hooks/use-day-entry-upsert', () => ({
  useDayEntryUpsert: () => ({
    save: hookMocks.save,
    status: 'idle' as const,
    lastError: null,
  }),
}));

import { NoteField } from '../note-field';

describe('<NoteField />', () => {
  beforeEach(() => {
    hookMocks.save.mockReset();
    hookMocks.save.mockResolvedValue(undefined);
  });

  afterEach(() => {
    vi.useRealTimers();
    cleanup();
  });

  it('typing calls hook.save({note}) after 1.5s of pause', async () => {
    vi.useFakeTimers();
    render(<NoteField date="2026-05-28" initialNote={null} disabled={false} />);

    const textarea = screen.getByRole('textbox', { name: /notitie/i });
    // fireEvent.change is synchronous and timer-friendly — userEvent.type
    // hangs under fake timers per the conventions doc.
    fireEvent.change(textarea, { target: { value: 'goed gewerkt' } });

    // Before the debounce settles, no save yet.
    expect(hookMocks.save).not.toHaveBeenCalled();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(1500);
    });

    expect(hookMocks.save).toHaveBeenCalledOnce();
    expect(hookMocks.save).toHaveBeenCalledWith({ note: 'goed gewerkt' }, { flush: true });
  });

  it('continued typing within 1.5s coalesces into one save', async () => {
    vi.useFakeTimers();
    render(<NoteField date="2026-05-28" initialNote={null} disabled={false} />);

    const textarea = screen.getByRole('textbox', { name: /notitie/i });
    fireEvent.change(textarea, { target: { value: 'eer' } });

    // Wait 1s — still under the threshold.
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1000);
    });
    expect(hookMocks.save).not.toHaveBeenCalled();

    // Resume typing — should reset the debounce.
    fireEvent.change(textarea, { target: { value: 'eerste deel' } });
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1000);
    });
    expect(hookMocks.save).not.toHaveBeenCalled();

    // Now wait the full settle window after the last keystroke.
    await act(async () => {
      await vi.advanceTimersByTimeAsync(1500);
    });
    expect(hookMocks.save).toHaveBeenCalledOnce();
    expect(hookMocks.save).toHaveBeenCalledWith({ note: 'eerste deel' }, { flush: true });
  });

  it('blur flushes the pending debounce immediately', async () => {
    const user = userEvent.setup();
    render(<NoteField date="2026-05-28" initialNote={null} disabled={false} />);

    const textarea = screen.getByRole('textbox', { name: /notitie/i });
    await user.type(textarea, 'snel');
    await user.tab();

    // No timer wait — blur fires the save synchronously.
    expect(hookMocks.save).toHaveBeenCalledOnce();
    expect(hookMocks.save).toHaveBeenCalledWith({ note: 'snel' }, { flush: true });
  });

  it('empty/whitespace value saves as note: null', async () => {
    const user = userEvent.setup();
    render(<NoteField date="2026-05-28" initialNote="oude tekst" disabled={false} />);

    const textarea = screen.getByRole('textbox', { name: /notitie/i });
    await user.clear(textarea);
    await user.type(textarea, '   ');
    await user.tab();

    expect(hookMocks.save).toHaveBeenCalledOnce();
    expect(hookMocks.save).toHaveBeenCalledWith({ note: null }, { flush: true });
  });

  it('is disabled when the disabled prop is true', () => {
    render(<NoteField date="2026-05-28" initialNote={null} disabled={true} />);
    const textarea = screen.getByRole('textbox', { name: /notitie/i });
    expect(textarea).toBeDisabled();
  });
});
