// Shared ISO UTC timestamp helper. Previously inlined into `tag.ts`,
// `day-entry.ts`, and `episode.ts` — the rule "two is a pattern, three
// demands extraction" was hit by step-1 of tag-management-settings
// (AC0). All three callers now import from here; episode.ts's archived_at
// + created_at + updated_at checks, day-entry's created_at + updated_at,
// and tag.ts's archived_at + created_at all share one regex + round-trip.
//
// Validation: the regex pinpoints the syntactic shape; the `new Date()`
// round-trip rejects syntactically-valid but impossible dates ("month 13").
// Returns the discriminated `Result<T, E>` shape that every other domain
// validator uses, plus an `isIsoUtcTimestamp` type-guard for the
// imperative call-sites (the validateTag / validateDayEntry / validateEpisode
// strict-shape checks already structured around an if-and-bail pattern).

const ISO_UTC_TIMESTAMP_REGEX =
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;

export type IsoUtcTimestampError = 'invalid_iso_timestamp';

export type ValidateIsoUtcTimestampResult =
  | { ok: true; value: string }
  | { ok: false; error: IsoUtcTimestampError };

export function isIsoUtcTimestamp(input: unknown): input is string {
  if (typeof input !== 'string') return false;
  if (!ISO_UTC_TIMESTAMP_REGEX.test(input)) return false;
  const parsed = new Date(input);
  return !Number.isNaN(parsed.getTime());
}

export function validateIsoUtcTimestamp(
  input: unknown,
): ValidateIsoUtcTimestampResult {
  if (isIsoUtcTimestamp(input)) {
    return { ok: true, value: input };
  }
  return { ok: false, error: 'invalid_iso_timestamp' };
}
