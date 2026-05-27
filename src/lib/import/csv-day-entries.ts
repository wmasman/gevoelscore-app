import { validateDate } from '../domain/date';
import { normalizeNote } from '../domain/note';
import { validateScore, type Score } from '../domain/score';

export interface ParsedRow {
  date: string;
  score: Score;
  note: string | null;
}

export type InvalidReason =
  | 'invalid_date'
  | 'invalid_score'
  | 'invalid_note'
  | 'wrong_column_count';

export interface InvalidRow {
  rowIndex: number;
  raw: string;
  reason: InvalidReason;
}

export interface ImportResult {
  valid: ParsedRow[];
  invalid: InvalidRow[];
}

export function parseImportCsv(input: string): ImportResult {
  // Strip UTF-8 BOM if present.
  const text = input.startsWith('﻿') ? input.slice(1) : input;
  const lines = text.split(/\r\n|\n/);

  const valid: ParsedRow[] = [];
  const invalid: InvalidRow[] = [];

  // Header detection: skip the first non-empty line if it looks like a header.
  let firstDataIndex = 0;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i] ?? '';
    if (line.trim().length === 0) {
      firstDataIndex = i + 1;
      continue;
    }
    if (isHeader(line)) {
      firstDataIndex = i + 1;
    } else {
      firstDataIndex = i;
    }
    break;
  }

  for (let i = firstDataIndex; i < lines.length; i++) {
    const line = lines[i] ?? '';
    if (line.trim().length === 0) continue;

    const rowIndex = i + 1; // 1-based for human-readable error reporting
    const cells = parseCsvRow(line);

    if (cells.length !== 2 && cells.length !== 3) {
      invalid.push({ rowIndex, raw: line, reason: 'wrong_column_count' });
      continue;
    }

    const dateRaw = (cells[0] ?? '').trim();
    const scoreRaw = (cells[1] ?? '').trim();

    const dateResult = validateDate(dateRaw);
    if (!dateResult.ok) {
      invalid.push({ rowIndex, raw: line, reason: 'invalid_date' });
      continue;
    }

    const scoreNum = scoreRaw === '' ? Number.NaN : Number(scoreRaw);
    const scoreResult = validateScore(scoreNum);
    if (!scoreResult.ok) {
      invalid.push({ rowIndex, raw: line, reason: 'invalid_score' });
      continue;
    }

    // 2-column rows have no note; 3-column rows pass the cell through normalizeNote.
    const noteInput = cells.length === 3 ? (cells[2] ?? '') : null;
    const noteResult = normalizeNote(noteInput);
    if (!noteResult.ok) {
      invalid.push({ rowIndex, raw: line, reason: 'invalid_note' });
      continue;
    }

    valid.push({
      date: dateResult.value,
      score: scoreResult.value,
      note: noteResult.value,
    });
  }

  return { valid, invalid };
}

function isHeader(line: string): boolean {
  const cells = parseCsvRow(line).map((c) => c.trim().toLowerCase());
  if (cells.length < 2 || cells.length > 3) return false;
  if (cells[0] !== 'date' || cells[1] !== 'score') return false;
  if (cells.length === 3 && cells[2] !== 'note') return false;
  return true;
}

/**
 * Parse a single CSV row into cells. Handles RFC 4180-style quoting:
 * - `"foo,bar"` → `foo,bar` (commas inside quoted cells are literal)
 * - `"she said ""hi"""` → `she said "hi"` (escaped quotes)
 *
 * Does NOT handle multi-line cells (notes containing embedded newlines).
 * The historical Google Sheet has no such rows; revisit if v1.5 import does.
 */
function parseCsvRow(line: string): string[] {
  const cells: string[] = [];
  let i = 0;
  const len = line.length;

  while (i < len) {
    const char = line.charAt(i);
    if (char === '"') {
      // Quoted cell
      i++;
      let value = '';
      while (i < len) {
        const c = line.charAt(i);
        if (c === '"') {
          if (line.charAt(i + 1) === '"') {
            value += '"';
            i += 2;
          } else {
            i++; // closing quote
            break;
          }
        } else {
          value += c;
          i++;
        }
      }
      cells.push(value);
      if (line.charAt(i) === ',') i++;
    } else {
      // Unquoted cell
      let value = '';
      while (i < len && line.charAt(i) !== ',') {
        value += line.charAt(i);
        i++;
      }
      cells.push(value);
      if (line.charAt(i) === ',') i++;
    }
  }

  return cells;
}
