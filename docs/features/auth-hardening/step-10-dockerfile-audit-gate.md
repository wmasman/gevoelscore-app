# Step 10: Dockerfile `npm audit` gate in deps stage

**Estimated time:** 10 minutes
**Test layer:** Smoke-test the docker build locally (or trust the next deploy).
**Risk:** Low — adds one line. Existing builds either pass (no high/critical CVEs) or fail loudly (and we want them to).
**Prerequisite:** Steps 1–9 done.

> Triggered by audit finding **L5**: the Dockerfile has no `npm audit` gate. A vulnerable lockfile could ship to production unnoticed until someone manually runs `npm audit` locally. The [`.claude/security-checklist.md`](../../../.claude/security-checklist.md) supply-chain section mandates zero high/critical CVEs pre-merge.

---

## The problem

`Dockerfile`'s `deps` stage installs from the lockfile and stops. If a transitive dep develops a published high-severity CVE between lockfile updates, the next deploy ships with the vulnerable code. There's no signal until `npm audit` is run by hand.

The Track B `verify:full` script (`npm run audit`) does this locally. The CI job will too (Track B4). The deploy path should fail-closed too — `fly deploy` runs the Dockerfile and rebuilds, so adding the gate there means a deploy of vulnerable code fails the build rather than ships.

## Acceptance criteria

- [ ] AC1: `Dockerfile`'s `deps` stage runs `npm audit --audit-level=high` after `npm ci`. Failure aborts the build.
- [ ] AC2: Current state passes (we know: `npm audit` shows 2 moderate, 0 high, 0 critical).
- [ ] AC3: A comment in the Dockerfile explains the gate.

## Technical constraints

- Audit runs in the `deps` stage, after `npm ci`. Adding it in `builder` would also work but runs slower (full node_modules + source already copied).
- Use `--audit-level=high` — the same threshold as `npm run audit`. Moderate findings don't block; they're tracked manually.
- No `--production` flag: dev deps can also have CVEs, and they get bundled into the Next build chain (Tailwind, Playwright config, etc.).

## Plan

### 10.1 Update `Dockerfile`

```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
# Tailwind v4 uses lightningcss, which ships its native binary as an
# optionalDependency (one per platform). Must NOT use --omit=optional or
# the alpine/linux-x64-musl binary is skipped and the build fails.
RUN npm ci
# Supply-chain gate: zero high/critical CVEs in the lockfile (audit L5).
# Same threshold as `npm run audit` and the CI workflow. Moderate findings
# don't block — track them in audits/*.md.
RUN npm audit --audit-level=high
```

## Test plan

- Manual: run `docker build .` locally; observe the audit line execute. If the user doesn't have a local Docker daemon, defer to the next `fly deploy` (which builds remotely).
- Failure mode: there's no easy way to inject a vulnerable dep without breaking the lockfile — skip the negative test. The threshold itself is the same as `npm run audit`, which has its own behaviour verified.

## Done criteria

- [x] Dockerfile has the `RUN npm audit --audit-level=high` line in the `deps` stage
- [x] Comment explains the threshold + rationale
- [ ] Next `fly deploy` succeeds (Step 10 is implicitly verified by the A2 commit's deploy step — pending)
- [x] Audit doc L5 line marked `[Resolved 2026-05-27 — Step 10]`
