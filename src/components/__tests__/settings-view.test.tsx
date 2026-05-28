// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// router.push mocked so we can assert navigation without a full Next harness.
const pushMock = vi.fn();
vi.mock('next/navigation', () => ({
  useRouter: () => ({ push: pushMock, refresh: vi.fn() }),
}));

import { SettingsView } from '../settings-view';

describe('<SettingsView />', () => {
  beforeEach(() => {
    pushMock.mockReset();
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => ({ ok: true }) }),
    );
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('renders the Account section + logout button + Data soon placeholders', () => {
    render(<SettingsView />);

    expect(screen.getByRole('heading', { level: 2, name: /account/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /uitloggen/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 2, name: /^data$/i })).toBeInTheDocument();
    expect(screen.getByText(/exporteren/i)).toBeInTheDocument();
    expect(screen.getByText(/account verwijderen/i)).toBeInTheDocument();
    // Soon-labels make it visible that those are not yet active.
    expect(screen.getAllByText(/binnenkort/i).length).toBeGreaterThan(0);
  });

  it('tapping the logout button does NOT immediately fire fetch (confirm step required)', async () => {
    const user = userEvent.setup();
    render(<SettingsView />);

    await user.click(screen.getByRole('button', { name: /^uitloggen$/i }));

    // No fetch yet — the confirm prompt should appear inline.
    expect(global.fetch).not.toHaveBeenCalled();
    expect(screen.getByText(/weet je het zeker/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /ja, uitloggen/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /annuleer/i })).toBeInTheDocument();
  });

  it('cancelling the confirm leaves no side effect (no fetch, no nav, prompt closes)', async () => {
    const user = userEvent.setup();
    render(<SettingsView />);
    await user.click(screen.getByRole('button', { name: /^uitloggen$/i }));

    await user.click(screen.getByRole('button', { name: /annuleer/i }));

    expect(global.fetch).not.toHaveBeenCalled();
    expect(pushMock).not.toHaveBeenCalled();
    expect(screen.queryByText(/weet je het zeker/i)).toBeNull();
  });

  it('confirming logout POSTs /api/auth/logout and navigates to /login', async () => {
    const user = userEvent.setup();
    render(<SettingsView />);
    await user.click(screen.getByRole('button', { name: /^uitloggen$/i }));
    await user.click(screen.getByRole('button', { name: /ja, uitloggen/i }));

    expect(global.fetch).toHaveBeenCalledWith(
      '/api/auth/logout',
      expect.objectContaining({ method: 'POST', credentials: 'same-origin' }),
    );
    expect(pushMock).toHaveBeenCalledWith('/login');
  });

  it('shows an error message and does NOT navigate when the logout fetch fails', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: false, status: 500, json: async () => ({ error: 'server' }) }),
    );
    const user = userEvent.setup();
    render(<SettingsView />);
    await user.click(screen.getByRole('button', { name: /^uitloggen$/i }));
    await user.click(screen.getByRole('button', { name: /ja, uitloggen/i }));

    expect(pushMock).not.toHaveBeenCalled();
    expect(await screen.findByText(/uitloggen lukte niet/i)).toBeInTheDocument();
  });
});
