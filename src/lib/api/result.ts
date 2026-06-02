// Discriminated-union shape returned by every SDK wrapper in src/lib/api/.
// The success branch carries the typed domain value; the failure branch
// carries a per-module error variant string. Callers narrow with
// `if (!result.ok)`.
//
// Extracted from src/lib/api/tags.ts + day-entries.ts when src/lib/api/
// episodes.ts became the third caller (the project's 3+ rule for shared
// constructs). The type definition is identical; behaviour is unchanged.

export type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
