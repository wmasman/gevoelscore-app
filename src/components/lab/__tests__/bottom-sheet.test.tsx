// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BottomSheet } from '../bottom-sheet';

// jsdom doesn't implement Pointer-related APIs that pointer-capture
// touches. Stub them so the drag handlers don't throw.
beforeEach(() => {
  if (!Element.prototype.hasPointerCapture) {
    Element.prototype.hasPointerCapture = vi.fn().mockReturnValue(false);
  }
  if (!Element.prototype.setPointerCapture) {
    Element.prototype.setPointerCapture = vi.fn();
  }
  if (!Element.prototype.releasePointerCapture) {
    Element.prototype.releasePointerCapture = vi.fn();
  }
  // useBodyScrollLock calls window.scrollTo on cleanup — jsdom doesn't
  // implement it; stub once for every case so the noise stays out of the
  // verify-gate output.
  window.scrollTo = vi.fn() as unknown as typeof window.scrollTo;
  Object.defineProperty(window, 'innerHeight', { configurable: true, value: 800 });
});

afterEach(() => {
  cleanup();
  delete (window as unknown as Record<string, unknown>).visualViewport;
});

function installVisualViewportMock(initial: { height: number }) {
  const listeners: Record<string, EventListener[]> = {};
  const state = { ...initial };
  const vv = {
    get offsetTop() { return 0; },
    get offsetLeft() { return 0; },
    get width() { return 400; },
    get height() { return state.height; },
    addEventListener: (type: string, cb: EventListener) => {
      listeners[type] = listeners[type] ?? [];
      listeners[type]!.push(cb);
    },
    removeEventListener: (type: string, cb: EventListener) => {
      listeners[type] = (listeners[type] ?? []).filter((l) => l !== cb);
    },
  } as unknown as VisualViewport;
  Object.defineProperty(window, 'visualViewport', { configurable: true, value: vv });
  return {
    fireResize(next: Partial<typeof initial>) {
      Object.assign(state, next);
      for (const cb of listeners['resize'] ?? []) cb(new Event('resize'));
    },
  };
}

describe('<BottomSheet />', () => {
  it('given open is false initially, when rendered, then no dialog is in the DOM (clean unmount)', () => {
    const { queryByRole } = render(
      <BottomSheet open={false} onClose={() => {}} ariaLabel="Invoer">
        body
      </BottomSheet>,
    );
    expect(queryByRole('dialog')).toBeNull();
  });

  it('given open is true, when rendered, then a dialog with aria-modal + aria-label is present', () => {
    const { getByRole } = render(
      <BottomSheet open={true} onClose={() => {}} ariaLabel="Invoer">
        body
      </BottomSheet>,
    );
    const dialog = getByRole('dialog');
    expect(dialog).toHaveAttribute('aria-modal', 'true');
    expect(dialog).toHaveAccessibleName('Invoer');
  });

  it('given the backdrop is clicked, when the click fires, then onClose is called', async () => {
    const user = userEvent.setup();
    const onClose = vi.fn();
    const { container } = render(
      <BottomSheet open={true} onClose={onClose} ariaLabel="Invoer">
        body
      </BottomSheet>,
    );
    const backdrop = container.ownerDocument.body.querySelector('[aria-hidden="true"]');
    expect(backdrop).not.toBeNull();
    await user.click(backdrop as HTMLElement);
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('given the sheet is open, when Escape is pressed, then onClose is called', async () => {
    const user = userEvent.setup();
    const onClose = vi.fn();
    render(
      <BottomSheet open={true} onClose={onClose} ariaLabel="Invoer">
        body
      </BottomSheet>,
    );
    await user.keyboard('{Escape}');
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('given the handle is dragged down more than 100px, when released, then onClose is called', () => {
    const onClose = vi.fn();
    const { getByTestId } = render(
      <BottomSheet open={true} onClose={onClose} ariaLabel="Invoer">
        body
      </BottomSheet>,
    );
    const handle = getByTestId('bottom-sheet-handle');
    fireEvent.pointerDown(handle, { clientY: 100, pointerId: 1 });
    fireEvent.pointerMove(handle, { clientY: 250, pointerId: 1 });
    fireEvent.pointerUp(handle, { clientY: 250, pointerId: 1 });
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('given the handle is dragged down less than 100px, when released, then onClose is NOT called', () => {
    const onClose = vi.fn();
    const { getByTestId } = render(
      <BottomSheet open={true} onClose={onClose} ariaLabel="Invoer">
        body
      </BottomSheet>,
    );
    const handle = getByTestId('bottom-sheet-handle');
    fireEvent.pointerDown(handle, { clientY: 100, pointerId: 1 });
    fireEvent.pointerMove(handle, { clientY: 150, pointerId: 1 });
    fireEvent.pointerUp(handle, { clientY: 150, pointerId: 1 });
    expect(onClose).not.toHaveBeenCalled();
  });

  it('given the sheet body (NOT the handle) receives a pointer-down, when released after a downward move, then onClose is NOT called (gesture isolation)', () => {
    const onClose = vi.fn();
    const { getByText } = render(
      <BottomSheet open={true} onClose={onClose} ariaLabel="Invoer">
        <div>body</div>
      </BottomSheet>,
    );
    const body = getByText('body');
    fireEvent.pointerDown(body, { clientY: 100, pointerId: 1 });
    fireEvent.pointerMove(body, { clientY: 300, pointerId: 1 });
    fireEvent.pointerUp(body, { clientY: 300, pointerId: 1 });
    expect(onClose).not.toHaveBeenCalled();
  });

  it('given tint="past", when rendered, then the sheet has the bg-surface-muted class', () => {
    const { getByRole } = render(
      <BottomSheet open={true} onClose={() => {}} tint="past" ariaLabel="Vorige dag">
        body
      </BottomSheet>,
    );
    const dialog = getByRole('dialog');
    expect(dialog.className).toMatch(/bg-surface-muted/);
  });

  it('given the sheet opens with a previously-focused element, when it closes, then focus returns to that element (useFocusTrap wired)', () => {
    const opener = document.createElement('button');
    opener.textContent = 'open-button';
    document.body.appendChild(opener);
    opener.focus();

    const { rerender } = render(
      <BottomSheet open={true} onClose={() => {}} ariaLabel="Invoer">
        <button type="button">inside</button>
      </BottomSheet>,
    );
    expect(document.activeElement?.textContent).toBe('inside');

    rerender(
      <BottomSheet open={false} onClose={() => {}} ariaLabel="Invoer">
        <button type="button">inside</button>
      </BottomSheet>,
    );

    expect(document.activeElement).toBe(opener);
    opener.remove();
  });

  it('given the sheet opens, when locked, then body has position:fixed (useBodyScrollLock wired)', () => {
    Object.defineProperty(window, 'scrollY', { writable: true, value: 0 });
    document.body.style.position = '';
    document.body.style.top = '';
    window.scrollTo = vi.fn() as unknown as typeof window.scrollTo;

    render(
      <BottomSheet open={true} onClose={() => {}} ariaLabel="Invoer">
        body
      </BottomSheet>,
    );

    expect(document.body.style.position).toBe('fixed');
  });

  it('given the visual viewport shrinks (iOS keyboard), when resize fires, then the sheet bottom is offset by innerHeight - viewport.height', () => {
    const { fireResize } = installVisualViewportMock({ height: 800 });

    const { getByRole } = render(
      <BottomSheet open={true} onClose={() => {}} ariaLabel="Invoer">
        body
      </BottomSheet>,
    );

    act(() => {
      fireResize({ height: 500 }); // simulate keyboard taking 300px
    });

    const dialog = getByRole('dialog') as HTMLElement;
    expect(dialog.style.bottom).toBe('300px');
  });
});
