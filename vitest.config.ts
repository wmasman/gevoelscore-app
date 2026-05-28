import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'node:path';

// React plugin enables JSX in .tsx test files; per-file `// @vitest-environment
// jsdom` opts component tests into jsdom while leaving the 400+ pure-logic
// tests in the (faster) Node environment.
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  test: {
    include: ['src/**/__tests__/**/*.test.ts', 'src/**/__tests__/**/*.test.tsx'],
    environment: 'node',
    globals: false,
    coverage: {
      provider: 'v8',
      include: ['src/lib/**/*.ts'],
      exclude: ['**/__tests__/**'],
      reporter: ['text', 'html'],
    },
  },
});
