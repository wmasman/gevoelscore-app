export const TAG_CATEGORIES = [
  'mentaal',
  'fysiek',
  'overall',
  'activiteit',
  'gebeurtenis',
  'interventie',
  'project',
  'custom',
] as const;

export type TagCategory = (typeof TAG_CATEGORIES)[number];

export type TagCategoryError = 'wrong_type' | 'unknown_category';

export type ValidateTagCategoryResult =
  | { ok: true; value: TagCategory }
  | { ok: false; error: TagCategoryError };

const TAG_CATEGORY_SET: ReadonlySet<string> = new Set(TAG_CATEGORIES);

export function validateTagCategory(input: unknown): ValidateTagCategoryResult {
  if (typeof input !== 'string') {
    return { ok: false, error: 'wrong_type' };
  }
  if (!TAG_CATEGORY_SET.has(input)) {
    return { ok: false, error: 'unknown_category' };
  }
  return { ok: true, value: input as TagCategory };
}
