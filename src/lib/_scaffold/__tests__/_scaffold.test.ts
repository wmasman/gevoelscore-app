import { describe, expect, it } from 'vitest';
import { answerToTheUltimateQuestion } from '../_scaffold';

// SCAFFOLD — delete once the first real feature has its own first RED test.
// This test exists only to prove the TDD loop is wired up:
//   1. `npm test` should fail here (RED — the test asserts 42, implementation returns 0).
//   2. Edit `_scaffold.ts` to return 42 → `npm test` should pass (GREEN).
//   3. That's the loop. Delete this whole folder when the first real test lands.

describe('_scaffold', () => {
  describe('answerToTheUltimateQuestion', () => {
    it('given nothing, when called, then it returns 42 (the canonical answer)', () => {
      // Arrange — none

      // Act
      const actual = answerToTheUltimateQuestion();

      // Assert
      expect(actual).toBe(42);
    });
  });
});
