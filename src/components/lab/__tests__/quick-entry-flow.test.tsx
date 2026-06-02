// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { DayEntry } from '@/lib/domain/day-entry';
import type { Tag } from '@/lib/domain/tag';

const hookMocks = vi.hoisted(() => ({
  save: vi.fn(),
}));

vi.mock('@/hooks/use-day-entry-upsert', () => ({
  useDayEntryUpsert: () => ({
    save: hookMocks.save,
    status: 'idle' as const,
    lastError: null,
  }),
}));

import { QuickEntryFlow } from '../quick-entry-flow';

function tag(id: string, label: string, category: Tag['category']): Tag {
  return {
    id,
    label,
    category,
    project_id: null,
    parent_episode_id: null,
    usage_count: 0,
    archived_at: null,
    created_at: '2026-01-01T00:00:00.000Z',
  };
}

const ALL_TAGS: Tag[] = [tag('m1', 'helder', 'mentaal')];

const EXISTING_ENTRY: DayEntry = {
  date: '2026-05-29',
  score: 7,
  note: 'bestaande notitie',
  tag_ids: ['m1'],
  sub_scores: null,
  sleep_hours: null,
  special_event: null,
  project_entry_ids: [],
  calendar_event_ids: [],
  garmin: null,
  health: null,
  weather: null,
  derived: null,
  created_at: '2026-05-29T08:00:00.000Z',
  updated_at: '2026-05-29T08:00:00.000Z',
};

beforeEach(() => {
  hookMocks.save.mockReset();
  hookMocks.save.mockResolvedValue(undefined);
  if (!Element.prototype.hasPointerCapture) {
    Element.prototype.hasPointerCapture = vi.fn().mockReturnValue(true);
  }
  if (!Element.prototype.setPointerCapture) {
    Element.prototype.setPointerCapture = vi.fn();
  }
  if (!Element.prototype.releasePointerCapture) {
    Element.prototype.releasePointerCapture = vi.fn();
  }
  window.scrollTo = vi.fn() as unknown as typeof window.scrollTo;
  Element.prototype.scrollTo = vi.fn() as unknown as Element['scrollTo'];
});
afterEach(cleanup);

function renderFlow(overrides: Partial<React.ComponentProps<typeof QuickEntryFlow>> = {}) {
  return render(
    <QuickEntryFlow
      date="2026-05-29"
      initialEntry={null}
      allTags={ALL_TAGS}
      open={true}
      onClose={() => {}}
      onComplete={() => {}}
      {...overrides}
    />,
  );
}

describe('<QuickEntryFlow />', () => {
  it('given startStep=score (default), when rendered, then the score-circle is the visible layer; the "Volgende: notitie" forward button is present-but-disabled until a commit', () => {
    const { getByRole, queryByRole } = renderFlow();

    expect(getByRole('slider', { name: /score/i })).toBeInTheDocument();
    // No back button on the first step.
    expect(queryByRole('button', { name: /^←/i })).toBeNull();
    // Forward button present but disabled — no anchoring on the default 5.
    const forward = getByRole('button', { name: /Volgende: notitie/i });
    expect(forward).toBeDisabled();
  });

  it('given the ScoreCircle commits, when it fires, then save is called with { score }', () => {
    const { getByRole } = renderFlow();
    const slider = getByRole('slider', { name: /score/i });

    fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
    fireEvent.pointerMove(slider, { clientX: 120, pointerId: 1 });
    fireEvent.pointerUp(slider, { clientX: 120, pointerId: 1 });

    // Per M-M3 (audit 2026-05-30): no { flush: true }. The hook's
    // 500 ms debounce coalesces a keyboard arrow-burst into one PUT.
    // Touch drag is already one pointerup event so debounce is a
    // microsecond delay there.
    expect(hookMocks.save).toHaveBeenCalledWith({ score: 6 });
  });

  it('given initialEntry is null and no commit yet, when rendered, then the "Volgende: notitie" forward button is disabled', () => {
    // Why: the score circle shows 5 by default; the brief is explicit
    // about not anchoring the user before they decide. The forward
    // button only enables after an explicit commit (drag / keypress).
    const { getByRole } = renderFlow({ initialEntry: null });
    const forward = getByRole('button', { name: /Volgende: notitie/i });
    expect(forward).toBeDisabled();
  });

  it('given the score commits, when the user taps "Volgende: notitie", then the flow advances to the note step — NO auto-advance', () => {
    // Replaces the prior 500 ms auto-advance behaviour. Per A-H1 from
    // the 2026-05-30 audit, motion-triggered step morphs violate
    // WCAG 2.2 SC 2.2.1 (Timing Adjustable) and contradict the brief's
    // "no time pressure" rule. Advance is now explicit.
    const { getByRole, queryByRole } = renderFlow({ initialEntry: null });
    const slider = getByRole('slider', { name: /score/i });

    fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
    fireEvent.pointerMove(slider, { clientX: 120, pointerId: 1 });
    fireEvent.pointerUp(slider, { clientX: 120, pointerId: 1 });

    // No setTimeout in the system any more — the surface stays on
    // score until the user taps forward.
    expect(queryByRole('button', { name: /^←\s*Score$/i })).toBeNull();

    // After commit the forward button must be enabled.
    const forward = getByRole('button', { name: /Volgende: notitie/i });
    expect(forward).not.toBeDisabled();
    fireEvent.click(forward);

    // Now we're on the note step — back button to Score appears.
    expect(getByRole('button', { name: /^←\s*Score$/i })).toBeInTheDocument();
  });

  it('given initialEntry already exists, when rendered, then "Volgende: notitie" is enabled immediately (no commit required to advance)', () => {
    // Edit-mode review: the entry already has a score, so editable
    // starts true and the user can advance without re-committing.
    const { getByRole } = renderFlow({ initialEntry: EXISTING_ENTRY });
    const forward = getByRole('button', { name: /Volgende: notitie/i });
    expect(forward).not.toBeDisabled();
  });

  it('given startStep="note" with an existing entry, when rendered, then the note step opens with back="← Score" and forward="Volgende: tags"', () => {
    const { getByRole } = renderFlow({
      initialEntry: EXISTING_ENTRY,
      startStep: 'note',
    });

    expect(getByRole('button', { name: /^←\s*Score$/i })).toBeInTheDocument();
    expect(getByRole('button', { name: /Volgende: tags/i })).toBeInTheDocument();
  });

  it('given the note step + forward, when pressed, then the flow morphs to the tags step (forward becomes "Klaar")', async () => {
    const user = userEvent.setup();
    const { getByRole } = renderFlow({
      initialEntry: EXISTING_ENTRY,
      startStep: 'note',
    });

    await user.click(getByRole('button', { name: /Volgende: tags/i }));

    expect(getByRole('button', { name: /Klaar/i })).toBeInTheDocument();
  });

  it('given the tags step + Klaar, when pressed, then onComplete is called', async () => {
    const user = userEvent.setup();
    const onComplete = vi.fn();
    const { getByRole } = renderFlow({
      initialEntry: EXISTING_ENTRY,
      startStep: 'tags',
      onComplete,
    });

    await user.click(getByRole('button', { name: /Klaar/i }));

    expect(onComplete).toHaveBeenCalledTimes(1);
  });

  it('given the tags step + Back, when pressed, then the flow returns to the note step', async () => {
    const user = userEvent.setup();
    const { getByRole } = renderFlow({
      initialEntry: EXISTING_ENTRY,
      startStep: 'tags',
    });

    await user.click(getByRole('button', { name: /^←\s*Notitie$/i }));

    expect(getByRole('button', { name: /Volgende: tags/i })).toBeInTheDocument();
  });

  it('given isPastDay is true, when rendered, then the BottomSheet uses the past tint (bg-surface-muted on the dialog)', () => {
    const { getByRole } = renderFlow({
      initialEntry: EXISTING_ENTRY,
      isPastDay: true,
    });
    const dialog = getByRole('dialog');
    expect(dialog.className).toMatch(/bg-surface-muted/);
  });

  it('given the sheet is closed-then-reopened with startStep="note", when re-rendered, then the note step (not score) becomes active — startStep must drive step on every open, not only at first mount', () => {
    // Why: useState(startStep) only reads the prop once. After the
    // initial mount, prop changes are ignored. In production this
    // shows up as "every edit pencil opens the score screen" because
    // QuickEntryFlow mounts once at page load with sheet.startStep
    // initialised to 'score'.
    const { rerender, getByRole } = render(
      <QuickEntryFlow
        date="2026-05-29"
        initialEntry={EXISTING_ENTRY}
        allTags={ALL_TAGS}
        open={false}
        startStep="score"
        onClose={() => {}}
        onComplete={() => {}}
      />,
    );

    rerender(
      <QuickEntryFlow
        date="2026-05-29"
        initialEntry={EXISTING_ENTRY}
        allTags={ALL_TAGS}
        open={true}
        startStep="note"
        onClose={() => {}}
        onComplete={() => {}}
      />,
    );

    // The note step is the only one that exposes both "← Score" and
    // "Volgende: tags". If internal `step` stayed at 'score', neither
    // button is rendered.
    expect(getByRole('button', { name: /^←\s*Score$/i })).toBeInTheDocument();
    expect(getByRole('button', { name: /Volgende: tags/i })).toBeInTheDocument();
  });

  it('given the sheet is closed-then-reopened with startStep="tags", when re-rendered, then the tags step (not score) becomes active', () => {
    const { rerender, getByRole } = render(
      <QuickEntryFlow
        date="2026-05-29"
        initialEntry={EXISTING_ENTRY}
        allTags={ALL_TAGS}
        open={false}
        startStep="score"
        onClose={() => {}}
        onComplete={() => {}}
      />,
    );

    rerender(
      <QuickEntryFlow
        date="2026-05-29"
        initialEntry={EXISTING_ENTRY}
        allTags={ALL_TAGS}
        open={true}
        startStep="tags"
        onClose={() => {}}
        onComplete={() => {}}
      />,
    );

    // The tags step is the only one with "Klaar" + "← Notitie".
    expect(getByRole('button', { name: /Klaar/i })).toBeInTheDocument();
    expect(getByRole('button', { name: /^←\s*Notitie$/i })).toBeInTheDocument();
  });

  it('given initialEntry is null, when rendered, then NoteField + TagCategoryList are disabled until the first score commit', () => {
    renderFlow({ initialEntry: null, startStep: 'score' });

    // The sheet renders into a Portal at document.body; query via `screen`.
    const textarea = screen.getByRole('textbox', { name: /notitie/i });
    expect(textarea).toBeDisabled();

    const slider = screen.getByRole('slider', { name: /score/i });
    fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
    fireEvent.pointerMove(slider, { clientX: 120, pointerId: 1 });
    fireEvent.pointerUp(slider, { clientX: 120, pointerId: 1 });

    expect(textarea).not.toBeDisabled();
  });
});
