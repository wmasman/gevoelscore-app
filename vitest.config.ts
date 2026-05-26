import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['src/**/__tests__/**/*.test.ts', 'src/**/__tests__/**/*.test.tsx'],
    environment: 'node',
    globals: false,
    coverage: {
      provider: 'v8',
      include: ['src/lib/**/*.ts'],
      exclude: ['**/__tests__/**', '**/_scaffold/**'],
      reporter: ['text', 'html'],
    },
  },
});
