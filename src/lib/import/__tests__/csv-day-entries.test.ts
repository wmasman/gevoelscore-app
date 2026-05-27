import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { parseImportCsv } from '../csv-day-entries';

describe('parseImportCsv', () => {
  // Pin today so the user's historical dates (2022–2026) all pass the future-date check.
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date(2026, 4, 26, 12, 0, 0));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  describe('happy paths', () => {
    it('parses a 3-column row (date, score, note)', () => {
      const csv = '"2026-05-26","5","goede dag"';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([{ date: '2026-05-26', score: 5, note: 'goede dag' }]);
      expect(result.invalid).toEqual([]);
    });

    it('parses a 2-column CSV (no note column) with note: null', () => {
      const csv = '"2026-05-26","5"\n"2026-05-25","4"';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([
        { date: '2026-05-26', score: 5, note: null },
        { date: '2026-05-25', score: 4, note: null },
      ]);
    });

    it('detects and skips a header row', () => {
      const csv = '"date","score","note"\n"2026-05-26","5","goede dag"';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([{ date: '2026-05-26', score: 5, note: 'goede dag' }]);
      expect(result.invalid).toEqual([]);
    });

    it('detects a 2-column header (no note column)', () => {
      const csv = '"date","score"\n"2026-05-26","5"';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([{ date: '2026-05-26', score: 5, note: null }]);
    });

    it('header detection is case-insensitive', () => {
      const csv = '"Date","Score","Note"\n"2026-05-26","5","x"';

      const result = parseImportCsv(csv);

      expect(result.valid).toHaveLength(1);
    });

    it('handles quoted note with comma', () => {
      const csv = '"2026-05-26","5","comma, in note"';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([
        { date: '2026-05-26', score: 5, note: 'comma, in note' },
      ]);
    });

    it('handles escaped quotes inside a note', () => {
      const csv = '"2026-05-26","5","she said ""hi"""';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([
        { date: '2026-05-26', score: 5, note: 'she said "hi"' },
      ]);
    });

    it('normalizes whitespace-only note to null', () => {
      const csv = '"2026-05-26","5","   "';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([{ date: '2026-05-26', score: 5, note: null }]);
    });

    it('normalizes empty note cell to null', () => {
      const csv = '"2026-05-26","5",""';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([{ date: '2026-05-26', score: 5, note: null }]);
    });

    it('handles unquoted cells', () => {
      const csv = '2026-05-26,5,hoofdpijn';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([
        { date: '2026-05-26', score: 5, note: 'hoofdpijn' },
      ]);
    });

    it('handles CRLF line endings', () => {
      const csv = '"2026-05-26","5","a"\r\n"2026-05-25","4","b"';

      const result = parseImportCsv(csv);

      expect(result.valid).toHaveLength(2);
    });

    it('strips UTF-8 BOM at the start of the file', () => {
      const csv = '﻿"date","score","note"\n"2026-05-26","5","x"';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([{ date: '2026-05-26', score: 5, note: 'x' }]);
    });

    it('skips trailing empty lines', () => {
      const csv = '"2026-05-26","5","x"\n\n\n';

      const result = parseImportCsv(csv);

      expect(result.valid).toHaveLength(1);
      expect(result.invalid).toHaveLength(0);
    });

    it('returns empty result for empty input', () => {
      const result = parseImportCsv('');

      expect(result).toEqual({ valid: [], invalid: [] });
    });
  });

  describe('invalid rows are collected, valid rows survive', () => {
    it('reports invalid date but keeps valid rows', () => {
      const csv = '"2026-02-30","5","bad date"\n"2026-05-26","6","good"';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([
        { date: '2026-05-26', score: 6, note: 'good' },
      ]);
      expect(result.invalid).toEqual([
        { rowIndex: 1, raw: '"2026-02-30","5","bad date"', reason: 'invalid_date' },
      ]);
    });

    it('reports out-of-range score', () => {
      const csv = '"2026-05-26","11","too high"';

      const result = parseImportCsv(csv);

      expect(result.valid).toEqual([]);
      expect(result.invalid).toEqual([
        { rowIndex: 1, raw: '"2026-05-26","11","too high"', reason: 'invalid_score' },
      ]);
    });

    it('reports non-numeric score', () => {
      const csv = '"2026-05-26","abc","not a number"';

      const result = parseImportCsv(csv);

      expect(result.invalid).toEqual([
        { rowIndex: 1, raw: '"2026-05-26","abc","not a number"', reason: 'invalid_score' },
      ]);
    });

    it('reports decimal score', () => {
      const csv = '"2026-05-26","5.5","halves not allowed"';

      const result = parseImportCsv(csv);

      expect(result.invalid).toEqual([
        {
          rowIndex: 1,
          raw: '"2026-05-26","5.5","halves not allowed"',
          reason: 'invalid_score',
        },
      ]);
    });

    it('reports wrong column count (4+ columns)', () => {
      const csv = '"2026-05-26","5","note","extra"';

      const result = parseImportCsv(csv);

      expect(result.invalid).toEqual([
        {
          rowIndex: 1,
          raw: '"2026-05-26","5","note","extra"',
          reason: 'wrong_column_count',
        },
      ]);
    });

    it('reports wrong column count (1 column)', () => {
      const csv = '"only-one"';

      const result = parseImportCsv(csv);

      expect(result.invalid).toEqual([
        { rowIndex: 1, raw: '"only-one"', reason: 'wrong_column_count' },
      ]);
    });

    it('rowIndex is 1-based and accounts for header', () => {
      const csv =
        '"date","score","note"\n"2026-05-26","5","ok"\n"2026-02-30","5","bad"\n"2026-05-24","6","ok"';

      const result = parseImportCsv(csv);

      expect(result.valid).toHaveLength(2);
      expect(result.invalid).toEqual([
        {
          rowIndex: 3,
          raw: '"2026-02-30","5","bad"',
          reason: 'invalid_date',
        },
      ]);
    });
  });
});
