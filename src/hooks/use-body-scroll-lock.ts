// useBodyScrollLock — reference-counted scroll lock on document.body.
// While at least one consumer is `active`, scroll is locked via the
// position:fixed+negative-top pattern (iOS Safari ignores plain
// overflow:hidden on body). On the last consumer's release, body styles
// reset and the original scrollY is restored.
//
// Reference counting + saved scroll position are module-level singletons.
// Modal-inside-a-modal stacks correctly, but the saved scroll position
// is captured only at the first lock — nested locks inherit it.

import { useEffect } from 'react';

let lockCount = 0;
let savedScrollY = 0;

export function useBodyScrollLock(active: boolean): void {
  useEffect(() => {
    if (!active) return;
    if (typeof window === 'undefined') return;
    if (lockCount === 0) {
      savedScrollY = window.scrollY;
      document.body.style.position = 'fixed';
      document.body.style.top = `-${savedScrollY}px`;
      document.body.style.width = '100%';
    }
    lockCount += 1;
    return () => {
      lockCount -= 1;
      if (lockCount === 0) {
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        window.scrollTo(0, savedScrollY);
      }
    };
  }, [active]);
}
