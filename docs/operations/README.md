# Operations docs — index

Anything you'd need to run, change, troubleshoot, or rotate.

| Document | Use when |
|----------|---------|
| [credentials.md](credentials.md) | You need to know where a credential lives (or rotate it). **No values stored here** — just locations + rotation procedures. |
| [scripts.md](scripts.md) | You want to know what's in `directus/scripts/` and how to run it. |
| [runbooks/deploy-backend.md](runbooks/deploy-backend.md) | Pushing a backend change (Directus version bump, Dockerfile edit). |
| [runbooks/rotate-credentials.md](runbooks/rotate-credentials.md) | Rotating the Directus static token, database password, or admin password. |
| [runbooks/wipe-and-rebootstrap.md](runbooks/wipe-and-rebootstrap.md) | Nuclear option — wipe the Fly Postgres database and re-run schema/permissions setup. |

For "what's currently deployed" see [`../architecture/current-state.md`](../architecture/current-state.md).

For "why we made this architectural choice" see [`../decisions/`](../decisions/).
