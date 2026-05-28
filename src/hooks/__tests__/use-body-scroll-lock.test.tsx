// @vitest-environment jsdom
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render } from '@testing-library/react';
import { useBodyScrollLock } from '../use-body-scroll-lock';

function Harness({ active }: { active: boolean }) {
  useBodyScrollLock(active);
  return null;
}

describe('useBodyScrollLock', () => {
  beforeEach(() => {
    document.body.removeAttribute('style');
    window.scrollTo = vi.fn() as unknown as typeof window.scrollTo;
    Object.defineProperty(window, 'scrollY', { writable: true, value: 0 });
  });
  afterEach(() => {
    cleanup();
    document.body.removeAttribute('style');
  });

  it('given active becomes true, when locked, then body gets position:fixed, top:-<scrollY>px, width:100%', () => {
    Object.defineProperty(window, 'scrollY', { writable: true, value: 250 });

    render(<Harness active={true} />);

    expect(document.body.style.position).toBe('fixed');
    expect(document.body.style.top).toBe('-250px');
    expect(document.body.style.width).toBe('100%');
  });

  it('given active becomes false, when unlocked, then body styles are restored and scrollY is reset', () => {
    Object.defineProperty(window, 'scrollY', { writable: true, value: 300 });

    const { rerender } = render(<Harness active={true} />);
    rerender(<Harness active={false} />);

    expect(document.body.style.position).toBe('');
    expect(document.body.style.top).toBe('');
    expect(document.body.style.width).toBe('');
    expect(window.scrollTo).toHaveBeenCalledWith(0, 300);
  });

  it('given two concurrent locks, when only one deactivates, then the body stays locked', () => {
    const a = render(<Harness active={true} />);
    const b = render(<Harness active={true} />);

    a.rerender(<Harness active={false} />);

    // Body should still be locked because the second hook is still active.
    expect(document.body.style.position).toBe('fixed');

    b.rerender(<Harness active={false} />);

    // Now both released — body unlocked.
    expect(document.body.style.position).toBe('');
  });

  it('given the consumer unmounts while active, when teardown runs, then the lock-count decrements and body unlocks', () => {
    Object.defineProperty(window, 'scrollY', { writable: true, value: 100 });

    const { unmount } = render(<Harness active={true} />);
    unmount();

    expect(document.body.style.position).toBe('');
    expect(window.scrollTo).toHaveBeenCalledWith(0, 100);
  });

  it('given active is false from the start, when rendered, then nothing happens (no body mutation)', () => {
    render(<Harness active={false} />);
    expect(document.body.style.position).toBe('');
    expect(document.body.style.top).toBe('');
  });
});
