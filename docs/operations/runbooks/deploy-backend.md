# Runbook: deploy the backend

Used when you change anything in `directus/` (Dockerfile, fly.toml, or want a Directus version bump).

## Standard deploy

```powershell
cd directus
fly deploy --app gevoelscore-backend
```

Wait ~2 minutes. The deploy:

1. Builds the image (`FROM directus/directus:11.17.2` per current Dockerfile).
2. Pushes it to Fly's registry.
3. Stops old machine + starts new one (rolling).
4. Waits for `/server/info` health check.

If the deploy says "✓ Machine 286ed93a64e5e8 [app] update finished: success" and the verification curl below returns HTTP 200, you're done.

## Verify

```powershell
curl https://gevoelscore-backend.fly.dev/server/info
# expected: HTTP 200, JSON body
```

If it returns 502: machine cold-starting, wait ~15s and retry. If still 502 after a minute, check logs.

## When the deploy fails

```powershell
fly logs --app gevoelscore-backend --no-tail
```

Common failure modes:

| Symptom | Probable cause | Fix |
|---|---|---|
| `connect ECONNREFUSED <postgres>` | Neon connection string wrong | Verify `DB_CONNECTION_STRING` Fly secret. See [rotate-credentials.md](rotate-credentials.md). |
| `error: missing required environment variable "KEY"` | Fly secret unset | `fly secrets set KEY=<32-hex> --app gevoelscore-backend` |
| Machine starts but `/server/info` returns 502 forever | Directus crashed inside the machine | `fly ssh console --app gevoelscore-backend`, check process state |
| Dockerfile change not applied | Cached layer | Add `--no-cache` to the deploy command (rebuilds from scratch, ~5x slower) |

## When to use `--no-cache`

Add `--no-cache` to `fly deploy` when:

- Changing the Directus base image version (e.g. 11.17.2 → 11.17.4)
- Modifying the Dockerfile startup script
- After a long gap (cached layers might be very stale)

For routine fly.toml changes (env tweaks, resource sizes), the default cached build is fine.

## Bumping Directus version

1. Edit `directus/Dockerfile`: change the `FROM directus/directus:<version>` line.
2. Read the [Directus changelog](https://github.com/directus/directus/releases) between current and target versions. Look for breaking changes.
3. `fly deploy --app gevoelscore-backend --no-cache`
4. Wait for deploy to finish.
5. Run `node directus/scripts/verify-schema.mjs` to confirm no fields broke.
6. Update `directus/Dockerfile` comment and [`docs/architecture/current-state.md`](../../architecture/current-state.md) with the new version.

**Don't skip step 5.** Directus version bumps occasionally migrate the system schema; verifying our user-collection types still match is cheap insurance.

## Rolling back

Fly keeps the last several image versions. To roll back:

```powershell
fly releases --app gevoelscore-backend       # find the last-known-good version number
fly deploy --image <previous image URL>      # OR
fly machine clone <old machine id>           # to bring up an old machine alongside
```

For more drastic rollback (e.g. Postgres schema corrupted), see [wipe-and-rebootstrap.md](wipe-and-rebootstrap.md) — but try the schema-only `verify-schema` first, it's usually the cheaper fix.
