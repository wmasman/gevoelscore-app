// Tests moved to tag-category-list.test.tsx after the 4+4 split rename.
// This file is kept as a placeholder so the rename shows up as a delete in
// a follow-up cleanup commit; for now it contains a single sanity test so
// vitest doesn't flag an empty file.

import { describe, expect, it } from 'vitest';
import { TagPicker } from '../tag-picker';

describe('<TagPicker /> (re-export shim)', () => {
  it('re-exports the renamed component', () => {
    expect(typeof TagPicker).toBe('function');
  });
});
