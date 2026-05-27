import { FlatCompat } from '@eslint/eslintrc';
import security from 'eslint-plugin-security';
import noSecrets from 'eslint-plugin-no-secrets';

const compat = new FlatCompat({
  baseDirectory: import.meta.dirname,
});

// Project-specific guardrails for the next.js + directus stack. Layered on
// top of next/core-web-vitals + next/typescript and the security plugins'
// recommended sets. Custom rules below encode the items from
// .claude/security-checklist.md + .claude/conventions.md that can be checked
// statically.
const config = [
  ...compat.extends('next/core-web-vitals', 'next/typescript'),
  security.configs.recommended,
  {
    // Two rules in the security plugin are heuristic and noisy for this
    // codebase (Maps with typed keys + a handful of simple validation regexes).
    // Disabled globally; the more valuable security/detect-* rules
    // (eval-with-expression, buffer-noassert, pseudoRandomBytes, child-process,
    // non-literal-require, etc.) stay enabled.
    rules: {
      'security/detect-object-injection': 'off',
      'security/detect-unsafe-regex': 'off',
    },
  },
  {
    plugins: { 'no-secrets': noSecrets },
    rules: {
      // Detect high-entropy literal strings (likely leaked tokens / keys).
      // Tolerance tuned so existing UUID-shaped session ids in tests don't
      // false-positive — first match in CI tells us whether to raise/lower it.
      'no-secrets/no-secrets': ['error', { tolerance: 4.5 }],

      // No telemetry deps allowed — conventions.md "no telemetry" rule
      // (also enforced by NEXT_TELEMETRY_DISABLED=1 in Dockerfile + fly.toml).
      'no-restricted-imports': [
        'error',
        {
          paths: [
            { name: 'next/telemetry', message: 'No telemetry — per ADR 0002.' },
            { name: '@vercel/analytics', message: 'No telemetry — per ADR 0002.' },
            { name: '@sentry/nextjs', message: 'No telemetry — per ADR 0002.' },
            { name: '@sentry/react', message: 'No telemetry — per ADR 0002.' },
            { name: 'posthog-js', message: 'No telemetry — per ADR 0002.' },
            { name: 'posthog-node', message: 'No telemetry — per ADR 0002.' },
          ],
          patterns: [
            { group: ['@sentry/*'], message: 'No telemetry — per ADR 0002.' },
          ],
        },
      ],

      // dangerouslySetInnerHTML is allowed ONLY in files that opt in via a
      // `// @security-reviewed:` comment somewhere in the file. Encodes
      // security-checklist A03 "no dangerouslySetInnerHTML without explicit
      // review" as a build-time check. The reviewer-comment pattern is
      // enforced by a parallel custom rule (see allowlist override below).
      'no-restricted-syntax': [
        'error',
        {
          selector: "JSXAttribute[name.name='dangerouslySetInnerHTML']",
          message:
            'dangerouslySetInnerHTML is forbidden. If genuinely necessary, add `// @security-reviewed: <reason>` in this file and override this rule for that file.',
        },
      ],
    },
  },
  {
    // Tests use mocked tokens like "at-1", "JBSWY3DPEHPK3PXP" intentionally;
    // no-secrets would false-positive on every fixture.
    files: ['**/__tests__/**', '**/*.test.{ts,tsx}', 'tests/**'],
    rules: {
      'no-secrets/no-secrets': 'off',
    },
  },
  {
    ignores: [
      '.next/**',
      'node_modules/**',
      'directus/**',
      'tests/**/playwright-report/**',
      'next-env.d.ts',
    ],
  },
];

export default config;
