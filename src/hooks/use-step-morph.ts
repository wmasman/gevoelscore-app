// useStepMorph — drives a two-phase crossfade between named steps.
//
// On every change to `activeStep`, the hook enters phase 'out' for
// `durationMs`, keeping the previously-rendered step on screen, then
// flips to phase 'in' and starts rendering the new step. Consumers
// drive opacity (or any other property) off `phase` to do the crossfade.
//
// Rapid changes within one duration window restart the timer so only
// the most recent step lands. The unmount cleanup clears any pending
// timer so the hook never setState's after unmount.

import { useEffect, useState } from 'react';

type Phase = 'in' | 'out';

export function useStepMorph<S extends string>(
  activeStep: S,
  durationMs = 150,
): { renderedStep: S; phase: Phase } {
  const [renderedStep, setRenderedStep] = useState<S>(activeStep);
  const [phase, setPhase] = useState<Phase>('in');

  useEffect(() => {
    if (activeStep === renderedStep) return;
    setPhase('out');
    const timer = setTimeout(() => {
      setRenderedStep(activeStep);
      setPhase('in');
    }, durationMs);
    return () => clearTimeout(timer);
  }, [activeStep, renderedStep, durationMs]);

  return { renderedStep, phase };
}
