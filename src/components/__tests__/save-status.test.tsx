// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import { SaveStatus } from '../save-status';

describe('<SaveStatus />', () => {
  afterEach(cleanup);

  it('renders nothing when status is idle', () => {
    const { container } = render(<SaveStatus status="idle" />);
    expect(container.textContent).toBe('');
  });

  it('renders a saving indicator when status is saving', () => {
    render(<SaveStatus status="saving" />);
    expect(screen.getByRole('status')).toHaveAccessibleName(/opslaan/i);
  });

  it('renders a saved indicator when status is saved', () => {
    render(<SaveStatus status="saved" />);
    expect(screen.getByRole('status')).toHaveAccessibleName(/opgeslagen/i);
  });

  it('renders an error banner with role=alert when status is error', () => {
    render(<SaveStatus status="error" error="server_error" />);
    expect(screen.getByRole('alert')).toBeVisible();
    expect(screen.getByRole('alert')).toHaveTextContent(/niet opgeslagen/i);
  });
});
