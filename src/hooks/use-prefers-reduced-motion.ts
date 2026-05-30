'use client';

// usePrefersReducedMotion — true when the OS-level reduced-motion
// preference is on. Listens for changes (some platforms toggle this
// dynamically: Windows transparency settings, iOS accessibility shortcut).
//
// The globals.css `@media (prefers-reduced-motion: reduce)` block
// already pins all CSS transitions/animations to 0.01 ms, but
// state-triggered behaviour (auto-advance setTimeouts, pulse-class
// toggles) needs to read this flag in JS to suppress.
//
// SSR returns false — server can't know the user's preference; the
// real value applies after hydration.

import { useEffect, useState } from 'react';

const QUERY = '(prefers-reduced-motion: reduce)';

export function usePrefersReducedMotion(): boolean {
  const [prefers, setPrefers] = useState<boolean>(false);

  useEffect(() => {
    if (typeof window === 'undefined' || !window.matchMedia) return;
    const mql = window.matchMedia(QUERY);
    setPrefers(mql.matches);
    const onChange = (e: MediaQueryListEvent): void => setPrefers(e.matches);
    mql.addEventListener('change', onChange);
    return () => mql.removeEventListener('change', onChange);
  }, []);

  return prefers;
}
