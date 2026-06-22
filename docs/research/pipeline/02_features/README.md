# `pipeline/02_features/` — derived per-bout / per-event features

Producer-mode feature-extraction stage. Sits between `01_extract/` (raw FIT
parsing) and `03_consolidate/` (per-day master join). Each script consumes
the cached per-day artefacts in `processed/garmin/` (or re-parses FIT
files when no cache exists yet) and emits a feature dataset to
`$GEVOELSCORE_DATA_PATH/unified/` for downstream joins.

## Scripts

### `extract_stress_bouts.py`

Producer-mode implementation of
[`methodology/bout_level_recovery_dynamics.md`](../../methodology/bout_level_recovery_dynamics.md)
(LOCKED `c57ff3f` 2026-06-21).

**What it does**: parses the per-minute Garmin stress trace from
`monitoring_b` FIT files, detects bouts per §3 (onset/peak/end with
hysteresis, minimum-separation, return-window cap), computes 21 per-bout
features per §4, joins per-day citalopram covariates (`dose_plasma_mg`,
`citalopram_phase`, `is_unmedicated`), and emits both the per-bout dataset
and the 5 per-day aggregations specified in user-ratified Decision 2
(2026-06-22).

**Inputs**:
- `monitoring_b` FIT files (re-parsed each run; mirrors the discipline of
  `01_extract/stress_low_motion_extract.py` and
  `analyses/hypotheses/HA11-stress-udip/extract_udip_counts.py` — no
  per-minute cache exists in the project).
- Sleep windows from Garmin `*_sleepData.json` (for `bout_during_sleep_flag`
  + `truncated_at_sleep_flag`).
- `processed/garmin/daily_uds.csv` (for the §3.4 21-day device-baseline-lag
  exclusion).

**Outputs (external, gitignored)**:
- `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.csv` — one row per bout
  (25 columns: identity + features + flags + citalopram covariates).
- `$GEVOELSCORE_DATA_PATH/unified/per_bout_master.parquet` — sidecar for
  faster downstream load (e.g. recalibration sub-MD session).
- `$GEVOELSCORE_DATA_PATH/unified/per_bout_aggregations_daily.csv` — the 5
  per-day aggregation columns consumed by
  `03_consolidate/build_unified_dataset.py`.

**Per-bout CSV columns** (25 total):

Identity + timing (6):
`bout_id, date, bout_index_within_day, t_onset, t_peak, t_end`

Headline features (8):
`peak_height, peak_minute, pre_bout_baseline, peak_minus_baseline,
recovery_half_life, tail_length, decay_slope, AUC_above_baseline`

Flags (8):
`motion_confound_flag, did_not_return_flag, did_not_half_recover_flag,
baseline_invalid_flag, truncated_at_sleep_flag, multi_peak_flag,
transient_flag, bout_during_sleep_flag`

Citalopram covariates (3, joined per day per §4):
`dose_plasma_mg, citalopram_phase, is_unmedicated`

**Per-day aggregations** (5 columns added to `per_day_master.csv` by the
extended `build_unified_dataset.py`):

| column | aggregation | use |
|---|---|---|
| `bout_n_fast_recovery_day` | count of bouts with `recovery_half_life <= 15` AND `tail_length <= 45` | HA11-bout-redo framework-validity operand (per MD §6.1) |
| `bout_n_per_day` | total bout count | coverage |
| `bout_n_did_not_return` | count of `did_not_return_flag = True` | recovery-quality flag count |
| `bout_max_peak_height_day` | max `peak_height` (NaN if no bouts) | intensity |
| `bout_total_AUC_day` | sum of `AUC_above_baseline` across day's bouts | integrated stress burden |

Per-day convention: count columns emit `0` on valid days with no bouts;
max/AUC emit blank (NaN). Invalid days (per §3.4 gate) emit blank on all
5.

## How to regenerate

```powershell
cd C:\Users\Gebruiker\Documents\gevoelscore-app
python docs/research/pipeline/02_features/extract_stress_bouts.py
python docs/research/pipeline/03_consolidate/build_unified_dataset.py
```

Runtime ~3-5 min on a full 7,888-file FIT corpus (most of which is FIT
parsing; bout detection itself is fast).

## Smoke tests

```powershell
python docs/research/pipeline/02_features/extract_stress_bouts.py --smoke-tests
```

Runs 6 inline edge-case assertions on tiny synthetic traces:

1. Canonical bout: peak above 60, clean baseline, returns within window.
2. `did_not_return`: sustained elevation hits the 180-min cap.
3. Midnight-spanning bout: peak at 00:00 attributed to `t_peak.date()`
   (the day-of-peak, per MD §3.2).
4. NaN handling: gaps in pre-window fail the 10-of-15 hysteresis check
   (no bout detected).
5. Transient: `t_peak - t_onset < 5 min` flagged as transient (still in
   primary operand per §3.1 r2 absorb).
6. `motion_confound_flag` tri-state honesty:
   - intensity records all 0 -> `False`
   - intensity records >= 2 -> `True`
   - NO intensity record in bout window -> `None` (NaN; per §3.4 r2
     absorb)

## Spot-check verification

```powershell
python docs/research/pipeline/02_features/extract_stress_bouts.py --verify
```

Picks 5 random bouts and prints all 25 columns at end of run. For
deeper manual verification: load `per_bout_master.csv` against the
per-minute trace for that day (e.g. by re-running the FIT parser for
that one day and inspecting the trace + features side-by-side).

The verification log for the 2026-06-22 first-run is recorded in the
session handoff brief
`C:/Users/Gebruiker/.claude/plans/session-bout-level-pipeline-construction-handoff-2026-06-22.md`.

## HALT-point context

This pipeline is the GATE for the bout-level cascade per the PM brief
`research-pm-brief-bout-level-recovery-pivot-2026-06-19.md` §5:

1. **HA11-bout-redo** (next-after-this-pipeline pre-reg): framework-validity
   reproduction check on `bout_n_fast_recovery_day` restricted to
   unmedicated × train era × calm-day pool. The pipeline must land + verify
   before that pre-reg drafting unblocks.
2. **HA-C4c** (later pre-reg, depends on HA11-bout-redo passing):
   substantive Wiggers C4 retest at bout-level. Inherits Approach A
   dose-adjustment per MD §5.3.
3. **Bout-level β recalibration** (sub-MD
   [`methodology/bout_level_dose_response_calibration.md`](../../methodology/bout_level_dose_response_calibration.md)):
   per user-ratified Decision 3 (2026-06-22), this is a SEPARATE
   downstream session — NOT bundled with the pipeline.

## Scope discipline (per session-handoff 2026-06-22 user-ratified decisions)

| # | Decision | Locked |
|---|---|---|
| 1 | Per-bout dataset location | External (`$GEVOELSCORE_DATA_PATH/unified/`) |
| 2 | Per-day aggregations | Moderate 5-column set (above) |
| 3 | Pipeline scope | Pipeline alone (recalibration is separate session) |
| 4 | Verification model | Ad-hoc inline + 5 spot-checks (no formal pytest) |

The pipeline implements only what the methodology MD §3-§4 + Decision 2
specify. The `extract_stress_bouts.py` script does NOT pre-author HA
pre-reg content + does NOT execute the bout-level β recalibration.
