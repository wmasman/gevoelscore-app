# Preflight — crash_v1 episode counts

Run before any H01–H05 test.py to confirm the locked `crash_v1`
definition produces enough episodes for held-out validation, and to
surface any structural problems with the test design.

Script: [count.mjs](count.mjs). Raw output: [count-output.txt](count-output.txt).

## Verdict

**OK to proceed**, but only after two design revisions surfaced by this
preflight:

1. **`crash_v1` threshold changed from percentile-based to absolute.**
   Original "personal bottom 15%" rule landed on tied scores and
   captured ~50% of days instead of ~15%. Re-locked as **score ≤ 3**.
2. **Train / validate split changed from time-proportional to
   episode-balanced.** Original 70/30 by date gave only 3 validate
   episodes due to a recovery cliff in 2025. Re-locked at 2023-12-31
   (14 train / 15 validate).

Both revisions documented in [registry.md](../registry.md) §1 and §2.

## Findings

### 1. Coverage is excellent

- **1.372 day_entries** in the analysis window (2022-09-03 → 2026-06-05)
- **100% have a score**
- No coverage gaps worth excluding

### 2. The score scale is 1–6, heavily clustered around 4–5

| score | days | % | meaning (inferred from distribution) |
|------:|-----:|----:|---|
| 1 | 6 | 0.4% | rock bottom |
| 2 | 33 | 2.4% | really bad |
| 3 | 152 | 11.1% | noticeably bad |
| 4 | 489 | 35.6% | sub-baseline |
| 5 | 615 | 44.8% | normal |
| 6 | 77 | 5.6% | great |

The cleavage is natural between 3 and 4: "bad enough to register" vs
"not great but functional". This drove the choice of `score ≤ 3` as the
revised crash_v1 threshold (option B1, picked over B2's `score ≤ 2`
which would have been clinically purer but underpowered).

### 3. crash_v1 yields 29 episodes total

Locked rule: **score ≤ 3 for ≥2 consecutive days, episodes within 3
days merged into one**, dated to the first day of the first run.

- 191 days have score ≤ 3 (13.9% of all days)
- 32 raw runs of ≥2 consecutive low days
- After merging within 3 days: **29 crash episodes**

**Episode span (calendar days from first to last low day in the
episode):**

| span | episodes |
|------|---------:|
| 2 days | 19 |
| 3–4 days | 4 |
| 5–7 days | 3 |
| 8–14 days | 3 |
| 15+ days | 0 |

Most episodes are short (2 days), but ~10 are sustained week+
episodes. The merging rule prevented any 15+ day super-episodes.

### 4. The recovery cliff — the most important finding here

**Episodes per year:**

| year | episodes | note |
|------|---------:|---|
| 2022 | 5 | partial year (~4 months) |
| 2023 | 9 | |
| 2024 | 11 | peak |
| **2025** | **2** | full year |
| 2026 | 2 | partial (~5 months) |

From ~10/year in 2023–24 to ~2/year in 2025–26. The user confirms this
is **real PEM-frequency recovery**, not score-interpretation drift.

This is a research finding in its own right — it deserves its own
descriptive insight card eventually (see registry §4 deferred:
"recovery-trajectory card"). It also forced a revision of the
train/validate split, because a time-proportional 70/30 would have
isolated only 3 episodes into the validate window.

### 5. The train/validate split

After the recovery-cliff discovery, the split was re-cut to balance
episode count rather than time:

| window | dates | episodes |
|---|---|---:|
| train | 2022-09-03 → 2023-12-31 (~16 months) | 14 |
| validate | 2024-01-01 → 2026-06-05 (~29 months) | 15 |

Both halves clear the 10-episode minimum, so H01–H05 are powered.
Importantly, the recovery cliff sits *inside* the validate window —
which makes the validation harder, not easier. A precursor pattern
that only worked in the 2022–23 high-frequency period will fail
validation. A pattern that's genuinely PEM-related should still appear
in the residual 2024+ episodes.

## What this changes for H01–H05

- **H01–H04 (precursor hypotheses)**: use the revised train/validate
  split, but the test logic is unchanged.
- **H05 (recovery time)**: now has 29 episodes to characterise, with a
  natural pre/post 2025 comparison built in. May want a secondary
  output: "did recovery time itself shorten?"
- **Deferred batch**: a recovery-trajectory descriptive card was added
  to registry §4, anchored to the cliff this preflight surfaced.

## What this does *not* change

- The crash_v1 spirit ("a multi-day low-score episode") is unchanged.
- The hypothesis pre-registrations in H01-rhr-drift/hypothesis.md and
  later H02–H05 reference crash_v1 by reference to the registry — they
  consume whatever crash_v1 is, so the threshold change doesn't
  invalidate the pre-registration.
- The held-out validation principle stands; only the split point
  moved.

## Re-run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-directus-script.ps1 `
  -Script docs/research/garmin/hypotheses/00-crash_v1-counts/count.mjs
```

---

*Preflight run 2026-06-05. Re-run any time crash_v1 is revised in the
registry.*
