// useVisualViewport — re-snapshots `window.visualViewport` on its resize
// + scroll events. Used by the bottom-sheet to anchor to the visible
// viewport when the iOS soft keyboard rises (keyboard pushes the
// visible viewport up; document height stays the same).
//
// Fallback path for browsers without the API (older Android Chrome,
// some embedded webviews): uses window.innerWidth/Height with
// offsetTop=0. Means the sheet just won't dodge the keyboard, but
// nothing crashes.

import { useEffect, useState } from 'react';

type ViewportSnapshot = {
  offsetTop: number;
  offsetLeft: number;
  width: number;
  height: number;
};

function snapshot(): ViewportSnapshot {
  if (typeof window === 'undefined') {
    return { offsetTop: 0, offsetLeft: 0, width: 0, height: 0 };
  }
  const vv = window.visualViewport;
  if (vv) {
    return {
      offsetTop: vv.offsetTop,
      offsetLeft: vv.offsetLeft,
      width: vv.width,
      height: vv.height,
    };
  }
  return {
    offsetTop: 0,
    offsetLeft: 0,
    width: window.innerWidth,
    height: window.innerHeight,
  };
}

export function useVisualViewport(): ViewportSnapshot {
  const [state, setState] = useState<ViewportSnapshot>(snapshot);

  useEffect(() => {
    if (typeof window === 'undefined' || !window.visualViewport) return;
    const onChange = (): void => setState(snapshot());
    const vv = window.visualViewport;
    vv.addEventListener('resize', onChange);
    vv.addEventListener('scroll', onChange);
    return () => {
      vv.removeEventListener('resize', onChange);
      vv.removeEventListener('scroll', onChange);
    };
  }, []);

  return state;
}
