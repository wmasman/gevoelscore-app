// @vitest-environment jsdom
import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { useRef } from 'react';
import { cleanup, render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { useFocusTrap } from '../use-focus-trap';

// Test harness component — exposes the hook's effect through a real DOM
// tree so we can drive it with the actual focus + keyboard machinery.
function Harness({
  active,
  empty = false,
}: {
  active: boolean;
  empty?: boolean;
}) {
  const ref = useRef<HTMLDivElement>(null);
  useFocusTrap(ref, active);
  return (
    <div>
      <button type="button">outside-before</button>
      <div ref={ref} data-testid="trap" tabIndex={-1}>
        {!empty && (
          <>
            <button type="button">first</button>
            <button type="button">middle</button>
            <button type="button">last</button>
          </>
        )}
      </div>
      <button type="button">outside-after</button>
    </div>
  );
}

describe('useFocusTrap', () => {
  beforeEach(() => {
    document.body.innerHTML = '';
  });
  afterEach(cleanup);

  it('given active becomes true, when activated, then focus moves to the first focusable element', () => {
    const before = document.createElement('button');
    document.body.appendChild(before);
    before.focus();

    const { getByText } = render(<Harness active={true} />);

    expect(document.activeElement).toBe(getByText('first'));
  });

  it('given active becomes false, when deactivated, then focus returns to the element that had focus on activation', () => {
    const before = document.createElement('button');
    before.textContent = 'opener';
    document.body.appendChild(before);
    before.focus();

    const { rerender } = render(<Harness active={true} />);
    rerender(<Harness active={false} />);

    expect(document.activeElement).toBe(before);
  });

  it('given focus is on the last item, when Tab is pressed, then focus wraps to the first item', async () => {
    const user = userEvent.setup();
    const { getByText } = render(<Harness active={true} />);

    (getByText('last') as HTMLButtonElement).focus();
    await user.tab();

    expect(document.activeElement).toBe(getByText('first'));
  });

  it('given focus is on the first item, when Shift+Tab is pressed, then focus wraps to the last item', async () => {
    const user = userEvent.setup();
    const { getByText } = render(<Harness active={true} />);

    (getByText('first') as HTMLButtonElement).focus();
    await user.tab({ shift: true });

    expect(document.activeElement).toBe(getByText('last'));
  });

  it('given the container is empty, when Tab is pressed, then focus stays on the container (preventDefault path)', async () => {
    const user = userEvent.setup();
    const { getByTestId } = render(<Harness active={true} empty />);
    const container = getByTestId('trap');
    container.focus();

    await user.tab();

    // The hook's empty-container branch preventDefaults Tab; focus must
    // not have left the container.
    expect(document.activeElement === container || container.contains(document.activeElement)).toBe(true);
  });

  it('given the consumer unmounts while active, when teardown runs, then no error is thrown and focus is restored', () => {
    const before = document.createElement('button');
    document.body.appendChild(before);
    before.focus();

    const { unmount } = render(<Harness active={true} />);
    unmount();

    expect(document.activeElement).toBe(before);
  });
});
