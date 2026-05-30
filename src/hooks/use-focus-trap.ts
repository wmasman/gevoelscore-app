// useFocusTrap — when `active` is true, focus is moved into the
// container and Tab/Shift+Tab cycles within it. When `active` becomes
// false (or the consumer unmounts), focus is restored to whatever held
// it at activation time.
//
// Note on the FOCUSABLE_SELECTOR: it does not traverse shadow DOM. This
// feature does not use shadow roots, so the simpler selector is fine.
// If a future surface relies on shadow DOM, extend this query.

import { useEffect, type RefObject } from 'react';

const FOCUSABLE_SELECTOR =
  'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

export function useFocusTrap(
  containerRef: RefObject<HTMLElement | null>,
  active: boolean,
): void {
  useEffect(() => {
    if (!active) return;
    const container = containerRef.current;
    if (!container) return;
    const previouslyFocused = document.activeElement as HTMLElement | null;

    // Initial focus targeting. Without an explicit hint, focus lands on
    // the first focusable in DOM order — which inside BottomSheet is the
    // close ✕ button. One stray Enter and the user dismisses what they
    // just opened (audit A-H2). Components can opt out by marking the
    // wrapper of the primary action with `data-autofocus="true"`; the
    // first focusable inside that wrapper wins.
    const focusables = container.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR);
    const autofocusWrapper = container.querySelector<HTMLElement>('[data-autofocus="true"]');
    const preferred = autofocusWrapper?.querySelector<HTMLElement>(FOCUSABLE_SELECTOR) ?? null;
    const first = preferred ?? focusables[0] ?? container;
    first.focus();

    function onKeyDown(event: KeyboardEvent): void {
      if (event.key !== 'Tab') return;
      const items = Array.from(
        container!.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR),
      );
      if (items.length === 0) {
        // Empty container: trap by preventing the focus from leaving.
        event.preventDefault();
        return;
      }
      const firstItem = items[0]!;
      const lastItem = items[items.length - 1]!;
      if (event.shiftKey && document.activeElement === firstItem) {
        event.preventDefault();
        lastItem.focus();
      } else if (!event.shiftKey && document.activeElement === lastItem) {
        event.preventDefault();
        firstItem.focus();
      }
    }

    document.addEventListener('keydown', onKeyDown);
    return () => {
      document.removeEventListener('keydown', onKeyDown);
      previouslyFocused?.focus();
    };
  }, [active, containerRef]);
}
