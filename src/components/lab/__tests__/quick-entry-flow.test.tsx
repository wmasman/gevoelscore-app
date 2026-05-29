// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react';
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
  it('given startStep=score (default), when rendered, then the score-circle is the visible layer and back+forward buttons are hidden', () => {
    const { getByRole, queryByRole } = renderFlow();

    expect(getByRole('slider', { name: /score/i })).toBeInTheDocument();
    // No back/forward yet — auto-advance handles the score→note transition.
    expect(queryByRole('button', { name: /score|notitie|tags|klaar|volgende/i })).toBeNull();
  });

  it('given the ScoreCircle commits, when it fires, then save is called with { score }', () => {
    const { getByRole } = renderFlow();
    const slider = getByRole('slider', { name: /score/i });

    fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
    fireEvent.pointerMove(slider, { clientX: 120, pointerId: 1 });
    fireEvent.pointerUp(slider, { clientX: 120, pointerId: 1 });

    expect(hookMocks.save).toHaveBeenCalledWith(
      { score: 6 },
      expect.objectContaining({ flush: true }),
    );
  });

  it('given initialEntry is null, when the score commits, then after 500ms the flow auto-advances to the note step', () => {
    vi.useFakeTimers();
    try {
      const { getByRole, queryByRole } = renderFlow({ initialEntry: null });
      const slider = getByRole('slider', { name: /score/i });

      fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
      fireEvent.pointerMove(slider, { clientX: 120, pointerId: 1 });
      fireEvent.pointerUp(slider, { clientX: 120, pointerId: 1 });

      // Before the auto-advance timer: no back button yet.
      expect(queryByRole('button', { name: /^←\s*Score$/i })).toBeNull();

      act(() => {
        vi.advanceTimersByTime(500);
      });

      // Back button is rendered once we've left the score step.
      expect(getByRole('button', { name: /^←\s*Score$/i })).toBeInTheDocument();
    } finally {
      vi.useRealTimers();
    }
  });

  it('given initialEntry already exists, when the score commits, then NO auto-advance fires (reviewing an existing entry must not yank the user forward)', () => {
    vi.useFakeTimers();
    try {
      const { getByRole, queryByRole } = renderFlow({ initialEntry: EXISTING_ENTRY });
      const slider = getByRole('slider', { name: /score/i });

      fireEvent.pointerDown(slider, { clientX: 100, pointerId: 1 });
      fireEvent.pointerMove(slider, { clientX: 120, pointerId: 1 });
      fireEvent.pointerUp(slider, { clientX: 120, pointerId: 1 });

      act(() => {
        vi.advanceTimersByTime(2000);
      });

      // Still on the score step — no back button.
      expect(queryByRole('button', { name: /^←\s*Score$/i })).toBeNull();
    } finally {
      vi.useRealTimers();
    }
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
