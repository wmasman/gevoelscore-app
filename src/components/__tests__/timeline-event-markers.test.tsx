/** @vitest-environment jsdom */
// Step-3 Phase 3.B — TimelineEventMarkers (AC3.8-3.16).

import '@testing-library/jest-dom/vitest';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import { TimelineEventMarkers } from '../timeline-event-markers';

const baseProps = {
  fromDate: '2026-06-01',
  toDate: '2026-06-30',
  width: 300,
  height: 80,
};

afterEach(() => cleanup());

describe('TimelineEventMarkers (AC3.8-3.16)', () => {
  it('test 102 (AC3.15): renders nothing when markerDays and spans are both empty', () => {
    const { container } = render(
      <TimelineEventMarkers
        {...baseProps}
        markerDays={new Set()}
        spans={[]}
        onDateSelect={vi.fn()}
      />,
    );

    expect(container.firstChild).toBeNull();
  });

  it('test 103 (AC3.8): renders one tap zone per marker day (N ticks for N marker days)', () => {
    render(
      <TimelineEventMarkers
        {...baseProps}
        markerDays={new Set(['2026-06-05', '2026-06-10', '2026-06-15'])}
        spans={[]}
        onDateSelect={vi.fn()}
      />,
    );

    expect(
      screen.getAllByRole('button', { name: /Activiteit op/ }),
    ).toHaveLength(3);
  });

  it('test 104 (AC3.8): renders one tap zone per span (M bars for M spans), in addition to the per-day ticks', () => {
    render(
      <TimelineEventMarkers
        {...baseProps}
        markerDays={
          new Set([
            '2026-06-05',
            '2026-06-06',
            '2026-06-15',
            '2026-06-16',
            '2026-06-17',
          ])
        }
        spans={[
          { recurrenceId: null, startDate: '2026-06-05', endDate: '2026-06-06' },
          { recurrenceId: null, startDate: '2026-06-15', endDate: '2026-06-17' },
        ]}
        onDateSelect={vi.fn()}
      />,
    );

    expect(
      screen.getAllByRole('button', { name: /Meerdaagse activiteit/ }),
    ).toHaveLength(2);
    expect(
      screen.getAllByRole('button', { name: /^Activiteit op/ }),
    ).toHaveLength(5);
  });

  it('test 105 (AC3.19): spans render BEFORE ticks in DOM order so SVG paints ticks on top', () => {
    const { container } = render(
      <TimelineEventMarkers
        {...baseProps}
        markerDays={new Set(['2026-06-05', '2026-06-06'])}
        spans={[
          { recurrenceId: null, startDate: '2026-06-05', endDate: '2026-06-06' },
        ]}
        onDateSelect={vi.fn()}
      />,
    );

    const groups = Array.from(container.querySelectorAll('g[data-kind]'));
    const kinds = groups.map((g) => g.getAttribute('data-kind'));
    // First group is a span, last group is a tick.
    expect(kinds[0]).toBe('span');
    expect(kinds[kinds.length - 1]).toBe('tick');
  });

  it('test 106 (AC3.13): tick tap zone is at least 44x44', () => {
    render(
      <TimelineEventMarkers
        {...baseProps}
        markerDays={new Set(['2026-06-05'])}
        spans={[]}
        onDateSelect={vi.fn()}
      />,
    );

    const tapZone = screen.getByRole('button', {
      name: /Activiteit op 2026-06-05/,
    });
    expect(Number(tapZone.getAttribute('width'))).toBeGreaterThanOrEqual(44);
    expect(Number(tapZone.getAttribute('height'))).toBeGreaterThanOrEqual(44);
  });

  it('test 107 (AC3.11): tick tap fires onDateSelect with the date', async () => {
    const user = userEvent.setup();
    const onDateSelect = vi.fn();
    render(
      <TimelineEventMarkers
        {...baseProps}
        markerDays={new Set(['2026-06-05'])}
        spans={[]}
        onDateSelect={onDateSelect}
      />,
    );

    await user.click(
      screen.getByRole('button', { name: /Activiteit op 2026-06-05/ }),
    );

    expect(onDateSelect).toHaveBeenCalledTimes(1);
    expect(onDateSelect).toHaveBeenCalledWith('2026-06-05');
  });

  it('test 108 (AC3.12): span tap fires onDateSelect with the span startDate', async () => {
    const user = userEvent.setup();
    const onDateSelect = vi.fn();
    render(
      <TimelineEventMarkers
        {...baseProps}
        markerDays={
          new Set(['2026-06-15', '2026-06-16', '2026-06-17'])
        }
        spans={[
          { recurrenceId: null, startDate: '2026-06-15', endDate: '2026-06-17' },
        ]}
        onDateSelect={onDateSelect}
      />,
    );

    const spanButton = screen.getByRole('button', {
      name: /Meerdaagse activiteit van 2026-06-15 tot 2026-06-17/,
    });
    await user.click(spanButton);

    expect(onDateSelect).toHaveBeenCalledTimes(1);
    expect(onDateSelect).toHaveBeenCalledWith('2026-06-15');
  });

  it('test 109 (AC3.9, AC3.10): visible marks use --color-fg-subtle, NOT warm-orange / alarm-red', () => {
    const { container } = render(
      <TimelineEventMarkers
        {...baseProps}
        markerDays={new Set(['2026-06-05'])}
        spans={[
          { recurrenceId: null, startDate: '2026-06-05', endDate: '2026-06-06' },
        ]}
        onDateSelect={vi.fn()}
      />,
    );

    const visualMarks = container.querySelectorAll('[data-visual-mark]');
    expect(visualMarks.length).toBeGreaterThan(0);
    visualMarks.forEach((mark) => {
      const fill = mark.getAttribute('fill') ?? '';
      expect(fill).toMatch(/fg-subtle|fg-muted/i);
      expect(fill).not.toMatch(/warm|orange|red|alarm/i);
    });
  });
});
