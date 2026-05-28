'use client';

// SaveStatusProvider — one source of save-feedback per screen.
//
// Three components on the Today screen (score row, note field, tag
// category list) each own their own useDayEntryUpsert(date) instance —
// each has its own debounce timing and abort lifecycle. But the *display*
// of save status should be unified: a single glyph in the page header,
// not three indicators competing for attention.
//
// Each component calls useReportSaveStatus(key, status, error) to publish
// into a shared map. The provider merges by priority (error > saving >
// saved > idle) and exposes the merged value via useMergedSaveStatus().
//
// Closed Step 4b's half-finish (header glyph from the wheel only) per
// the 2026-05-28 audit's L2.

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from 'react';
import type { SaveStatus as SaveStatusValue } from '@/hooks/use-day-entry-upsert';

type SourceStatus = { status: SaveStatusValue; error: string | null };

type Reporter = (key: string, value: SourceStatus) => void;

const ReportContext = createContext<Reporter | null>(null);
const MergedContext = createContext<SourceStatus>({ status: 'idle', error: null });

function mergeStatuses(map: Map<string, SourceStatus>): SourceStatus {
  const all = [...map.values()];
  // Priority: error > saving > saved > idle. Returns the first match.
  return (
    all.find((s) => s.status === 'error') ??
    all.find((s) => s.status === 'saving') ??
    all.find((s) => s.status === 'saved') ??
    { status: 'idle', error: null }
  );
}

export function SaveStatusProvider({ children }: { children: ReactNode }) {
  const sourcesRef = useRef<Map<string, SourceStatus>>(new Map());
  const [merged, setMerged] = useState<SourceStatus>({ status: 'idle', error: null });

  const report = useCallback<Reporter>((key, value) => {
    sourcesRef.current.set(key, value);
    setMerged(mergeStatuses(sourcesRef.current));
  }, []);

  return (
    <ReportContext.Provider value={report}>
      <MergedContext.Provider value={merged}>{children}</MergedContext.Provider>
    </ReportContext.Provider>
  );
}

// Reports a component's save status into the shared map. No-op outside a
// SaveStatusProvider so leaf components can still be tested in isolation.
export function useReportSaveStatus(
  key: string,
  status: SaveStatusValue,
  error: string | null,
): void {
  const report = useContext(ReportContext);
  useEffect(() => {
    if (report) report(key, { status, error });
  }, [report, key, status, error]);
}

export function useMergedSaveStatus(): SourceStatus {
  return useContext(MergedContext);
}
