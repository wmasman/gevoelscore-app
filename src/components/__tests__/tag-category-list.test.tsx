// @vitest-environment jsdom
import '@testing-library/jest-dom/vitest';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { Tag } from '@/lib/domain/tag';

const hookMocks = vi.hoisted(() => ({
  save: vi.fn(),
  status: 'idle' as 'idle' | 'saving' | 'saved' | 'error',
  lastError: null as string | null,
}));

vi.mock('@/hooks/use-day-entry-upsert', () => ({
  useDayEntryUpsert: () => ({
    save: hookMocks.save,
    status: hookMocks.status,
    lastError: hookMocks.lastError,
  }),
}));

import { TagCategoryList } from '../tag-category-list';

function tag(id: string, label: string, category: Tag['category']): Tag {
  return {
    id,
    label,
    category,
    project_id: category === 'project' ? 'proj-1' : null,
    usage_count: 0,
    archived_at: null,
    created_at: '2026-01-01T00:00:00.000Z',
  };
}

const ALL_TAGS: Tag[] = [
  tag('m1', 'helder', 'mentaal'),
  tag('m2', 'mistig', 'mentaal'),
  tag('f1', 'moe', 'fysiek'),
  tag('f2', 'energiek', 'fysiek'),
  tag('o1', 'goed', 'overall'),
  tag('a1', 'wandelen', 'activiteit'),
  tag('g1', 'familie', 'gebeurtenis'),
  tag('i1', 'rusten', 'interventie'),
  tag('p1', 'logboek', 'project'),
  tag('c1', 'eigen', 'custom'),
];

const PRIMARY = ['mentaal', 'fysiek', 'overall', 'activiteit'];
const EXTRA = ['gebeurtenis', 'interventie', 'project', 'custom'];

describe('<TagCategoryList />', () => {
  beforeEach(() => {
    hookMocks.save.mockReset();
    hookMocks.save.mockResolvedValue(undefined);
    hookMocks.status = 'idle';
    hookMocks.lastError = null;
  });

  afterEach(cleanup);

  it('renders the 4 primary headers + an "Extra opties" toggle; the 4 extras are not in the DOM by default', () => {
    render(
      <TagCategoryList
        date="2026-05-28"
        allTags={ALL_TAGS}
        initialTagIds={[]}
        disabled={false}
      />,
    );

    for (const c of PRIMARY) {
      // eslint-disable-next-line security/detect-non-literal-regexp -- test fixture iterating over a const enum
      expect(screen.getByRole('button', { name: new RegExp(c, 'i') })).toBeInTheDocument();
    }
    expect(screen.getByRole('button', { name: /extra opties/i })).toBeInTheDocument();
    for (const c of EXTRA) {
      // eslint-disable-next-line security/detect-non-literal-regexp -- test fixture iterating over a const enum
      expect(screen.queryByRole('button', { name: new RegExp(`^${c}`, 'i') })).toBeNull();
    }
  });

  it('tapping "Extra opties" reveals the 4 extra categories inline; tapping again collapses them. aria-expanded flips', async () => {
    const user = userEvent.setup();
    render(
      <TagCategoryList
        date="2026-05-28"
        allTags={ALL_TAGS}
        initialTagIds={[]}
        disabled={false}
      />,
    );

    const extraToggle = screen.getByRole('button', { name: /extra opties/i });
    expect(extraToggle).toHaveAttribute('aria-expanded', 'false');

    await user.click(extraToggle);
    expect(extraToggle).toHaveAttribute('aria-expanded', 'true');
    for (const c of EXTRA) {
      // eslint-disable-next-line security/detect-non-literal-regexp -- test fixture
      expect(screen.getByRole('button', { name: new RegExp(`^${c}`, 'i') })).toBeInTheDocument();
    }

    await user.click(extraToggle);
    expect(extraToggle).toHaveAttribute('aria-expanded', 'false');
    for (const c of EXTRA) {
      // eslint-disable-next-line security/detect-non-literal-regexp -- test fixture
      expect(screen.queryByRole('button', { name: new RegExp(`^${c}`, 'i') })).toBeNull();
    }
  });

  it('tapping a category header expands its chips inline; aria-expanded flips', async () => {
    const user = userEvent.setup();
    render(
      <TagCategoryList
        date="2026-05-28"
        allTags={ALL_TAGS}
        initialTagIds={[]}
        disabled={false}
      />,
    );

    const fysiekHeader = screen.getByRole('button', { name: /fysiek/i });
    expect(fysiekHeader).toHaveAttribute('aria-expanded', 'false');

    await user.click(fysiekHeader);
    expect(fysiekHeader).toHaveAttribute('aria-expanded', 'true');
    expect(screen.getByRole('button', { name: 'moe' })).toBeVisible();
    expect(screen.getByRole('button', { name: 'energiek' })).toBeVisible();
  });

  it('multiple category headers can be expanded simultaneously across primary/extra boundary', async () => {
    const user = userEvent.setup();
    render(
      <TagCategoryList
        date="2026-05-28"
        allTags={ALL_TAGS}
        initialTagIds={[]}
        disabled={false}
      />,
    );

    await user.click(screen.getByRole('button', { name: /mentaal/i }));
    await user.click(screen.getByRole('button', { name: /extra opties/i }));
    // Strict prefix-match — "Extra opties (Interventie, Project, etc)" also
    // contains "interventie".
    await user.click(screen.getByRole('button', { name: /^interventie/i }));

    expect(screen.getByRole('button', { name: /mentaal/i })).toHaveAttribute('aria-expanded', 'true');
    expect(screen.getByRole('button', { name: /^interventie/i })).toHaveAttribute('aria-expanded', 'true');
    expect(screen.getByRole('button', { name: 'helder' })).toBeVisible();
    expect(screen.getByRole('button', { name: 'rusten' })).toBeVisible();
  });

  it('tapping an unselected chip fires save with the new tag_ids array', async () => {
    const user = userEvent.setup();
    render(
      <TagCategoryList
        date="2026-05-28"
        allTags={ALL_TAGS}
        initialTagIds={['m1']}
        disabled={false}
      />,
    );

    await user.click(screen.getByRole('button', { name: /fysiek/i }));
    await user.click(screen.getByRole('button', { name: 'moe' }));

    expect(hookMocks.save).toHaveBeenCalledOnce();
    const [patch] = hookMocks.save.mock.calls[0]!;
    expect(new Set(patch.tag_ids)).toEqual(new Set(['m1', 'f1']));
  });

  it('tapping a selected chip toggles it off (save called with reduced array)', async () => {
    const user = userEvent.setup();
    render(
      <TagCategoryList
        date="2026-05-28"
        allTags={ALL_TAGS}
        initialTagIds={['m1', 'f1']}
        disabled={false}
      />,
    );

    await user.click(screen.getByRole('button', { name: /fysiek/i }));
    await user.click(screen.getByRole('button', { name: 'moe' }));

    expect(hookMocks.save).toHaveBeenCalledOnce();
    const [patch] = hookMocks.save.mock.calls[0]!;
    expect(patch.tag_ids).toEqual(['m1']);
  });

  it('selection count badge ("· N") appears on a header when ≥1 chip in that category is selected', () => {
    render(
      <TagCategoryList
        date="2026-05-28"
        allTags={ALL_TAGS}
        initialTagIds={['m1', 'm2', 'f1']}
        disabled={false}
      />,
    );

    const mentaalHeader = screen.getByRole('button', { name: /mentaal/i });
    const fysiekHeader = screen.getByRole('button', { name: /fysiek/i });
    const overallHeader = screen.getByRole('button', { name: /overall/i });

    expect(within(mentaalHeader).getByText(/·\s*2/)).toBeInTheDocument();
    expect(within(fysiekHeader).getByText(/·\s*1/)).toBeInTheDocument();
    expect(within(overallHeader).queryByText(/·/)).toBeNull();
  });

  it('"Extra opties" toggle shows a count of selected chips in the hidden categories', () => {
    render(
      <TagCategoryList
        date="2026-05-28"
        allTags={ALL_TAGS}
        initialTagIds={['i1', 'p1', 'm1']}
        disabled={false}
      />,
    );

    // 2 of the 3 selected are in the extra categories (i1, p1). m1 is in mentaal.
    expect(screen.getByRole('button', { name: /extra opties.*\(2\)/i })).toBeInTheDocument();
  });

  it('renders cleanly under error status (banner is parent\'s concern post-2026-05-28 audit L2)', () => {
    // After L2: TagCategoryList no longer renders its own <SaveStatus />.
    // Error state is broadcast via useReportSaveStatus → the parent
    // (TodayShell or DayDetailSheet) renders the banner. This unit test
    // verifies the component still mounts cleanly with status='error';
    // the banner rendering is covered by today-shell.test.tsx + the e2e
    // specs that drive a 500 response.
    hookMocks.status = 'error';
    hookMocks.lastError = 'server_error';
    render(
      <TagCategoryList
        date="2026-05-28"
        allTags={ALL_TAGS}
        initialTagIds={[]}
        disabled={false}
      />,
    );

    expect(screen.getByRole('heading', { level: 2, name: /tags/i })).toBeInTheDocument();
    expect(screen.queryByText(/niet opgeslagen/i)).toBeNull();
  });
});
