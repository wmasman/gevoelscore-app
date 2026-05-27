# CSV import parser

**Feature:** Parse the user's 1.363-day Google Sheet CSV export into validated `{ date, score, note }` rows, with structured failure reporting.
**Version:** v1
**Status:** Planning
**Parent doc:** [REQUIREMENTS.md line 35](../../REQUIREMENTS.md), [brief §"Backfill"](../../app_brief_gevoelscore.md)

---

## Overview

- **What:** A pure-TS parser that takes CSV text and returns `{ valid: ParsedRow[], invalid: InvalidRow[] }`. Partial-success by design — one bad row doesn't lose 1,362 good ones.
- **Why:** The user has 1.363 consecutive days of historical scores in a Google Sheet. Without an import path, the new app starts blank and the streak-counter / timeline view are useless on day 1. Per the brief, the existing CSV is the source: column A = date, column B = score, column C = note.
- **Impact:** Once Directus is up (per [ADR 0003](../../decisions/0003-directus-fly-infra-setup.md)) and the daily-entry feature exists, this parser feeds the bulk-insert that backfills the entire history. Standalone domain-layer logic — runs without any infra.

## User need

The user opens the app for the first time, taps "Import history," picks the CSV exported from Google Sheets, and sees: "1,358 days imported. 5 rows had problems — review?" That last group surfaces specific reasons ("row 42: date '2024-02-29' is not a real date" / "row 17: score '0' is below 1") so the user can fix the source and re-import or accept the gaps.

## Acceptance criteria

**parseImportCsv (the function):**

- [ ] AC1: Given a typical 3-column row (date, score, note), the row appears in `valid` with validated date, score, and normalized note.
- [ ] AC2: Given a 2-column CSV (date, score, no note column), each row appears in `valid` with `note: null`.
- [ ] AC3: Given a header row matching `"date","score"[,"note"]` (case-insensitive), it is detected and skipped — does not appear in valid or invalid.
- [ ] AC4: Given a row with a quoted note containing a comma (`"2026-05-26","5","comma, in note"`), the note is parsed correctly.
- [ ] AC5: Given a row with an escaped quote in the note (`"...","5","she said ""hi"""`), the note is `she said "hi"`.
- [ ] AC6: Given a row with an empty / whitespace-only note, the note normalizes to `null`.
- [ ] AC7: Given a row with an invalid date (`'2024-02-30'`), it appears in `invalid` with `rowIndex`, `raw`, and `reason: 'invalid_date'`. Other valid rows are NOT lost.
- [ ] AC8: Given a row with an out-of-range score, it appears in `invalid` with `reason: 'invalid_score'`.
- [ ] AC9: Given a row with a non-numeric score string, it appears in `invalid` with `reason: 'invalid_score'`.
- [ ] AC10: Given a row with the wrong number of columns (4+), it appears in `invalid` with `reason: 'wrong_column_count'`.
- [ ] AC11: CRLF and LF line endings are both handled correctly.
- [ ] AC12: UTF-8 BOM at the start of the file is stripped silently.
- [ ] AC13: Trailing empty lines are skipped (not reported as invalid).
- [ ] AC14: Given empty input (`""`), returns `{ valid: [], invalid: [] }`.

## Technical constraints

- Pure TS, zero deps — domain-adjacent layer (`src/lib/import/`), not allowed to import `papaparse` or any other CSV library.
- Synchronous (the largest historical file is ~1,400 rows; well under any concerning size).
- Reuses `validateDate`, `validateScore`, `normalizeNote` from `src/lib/domain/`.
- `rowIndex` is **1-based** matching what the user sees in their spreadsheet (header = row 1, first data row = row 2).
- Multi-line notes (notes containing newlines, even when quoted) are **out of scope** for v1 — historical sheet had no such rows. If needed later, the cell-parser switches from per-line tokenization to a full-text state machine.

## Test plan

`src/lib/import/__tests__/csv-day-entries.test.ts` — covers AC1–AC14.

## Architecture

```
src/lib/import/
  csv-day-entries.ts          — parseImportCsv(text): ImportResult
  __tests__/
    csv-day-entries.test.ts
```

Imports from `src/lib/domain/` only (`validateDate`, `validateScore`, `normalizeNote`).

## Steps

Single step — small enough to land in one cycle: [step-1-parse-csv.md](step-1-parse-csv.md).
