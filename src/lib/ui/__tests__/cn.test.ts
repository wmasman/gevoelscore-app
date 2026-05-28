import { describe, expect, it } from 'vitest';
import { cn } from '../cn';

describe('cn', () => {
  it('merges conflicting Tailwind classes via tailwind-merge (last wins)', () => {
    expect(cn('p-2', 'p-4')).toBe('p-4');
  });

  it('drops falsy values and concatenates the rest', () => {
    expect(cn('text-red-500', false, 'text-blue-500')).toBe('text-blue-500');
    expect(cn('m-2', null, undefined, 'gap-4')).toBe('m-2 gap-4');
  });
});
