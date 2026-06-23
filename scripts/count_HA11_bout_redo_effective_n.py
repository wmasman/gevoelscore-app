"""HA11-bout-redo r2 — pre-lock single-script count of effective n + sigma.

Closes the audit's L3 substantive fire (effective n unpinned pre-lock) and
L3 minor fire (sigma-distribution check on bout_n_fast_recovery_day).

Procedure:
  1. Load udip_counts.csv (HA11 v1) to recover the HA11 v1 'valid' flag per
     date (>= 600 valid per-minute stress samples on d).
  2. Load labels_crash_v2.csv; extract crash episode starts (matching HA11
     v1 test.py load_crashes pattern).
  3. Replay HA11 v1 build_null_sample with seed 20260605 to regenerate the
     200 reference dates (same algorithm, same constants: ANALYSIS_START
     2022-09-03, VALIDATE_END 2026-06-05, LEADUP_PRIMARY=4,
     MIN_LEADUP_VALID_PRIMARY=3).
  4. Load per_day_master.csv for bout_n_fast_recovery_day (col 130) and
     has_garmin_uds (col 18) per date.
  5. Compute the device-baseline-lag exclusion (first 21 days of
     has_garmin_uds=True coverage per parent MD §3.4).
  6. Apply HA11-bout-redo §4.2 + §4.3 + §4.4 restrictions to the reference
     pool:
       - reference date r in unmedicated phase (2022-04-04 <= r <= 2024-04-08).
       - reference date r in train era (2022-09-03 <= r <= 2023-12-31).
       - reference date r not in April 2024 cluster (trivially satisfied).
       - reference date r not in first 21 device-baseline days.
       - bout_n_fast_recovery_day on r not NaN.
  7. Apply §4.5 + §4.7 coverage gate: 4-day window [r-3, r] must have
     >= 3 of 4 days with valid bout_n_fast_recovery_day AND a valid (mu,
     sigma) lagged personal baseline (>= 40 of 60 prior days valid +
     sigma > 0.5 per HA11 v1 §4.5).
  8. Report effective n on the post-restriction reference pool.
  9. Report sigma distribution of bout_n_fast_recovery_day across the
     post-restriction analysis days, plus the HA11 v1 u_dip_count sigma
     distribution on the equivalent pool for comparison.

This is a count script, NOT the test. It does NOT compute discrimination,
trigger frequencies, or block-permutation p-values. It pins two named-counts
per CONVENTIONS §3.6 + audit closure.
"""
from __future__ import annotations

import csv
import os
import random
import statistics
from datetime import date, timedelta
from pathlib import Path


# Constants inherited verbatim from HA11 v1 test.py
ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LEADUP_PRIMARY = 4
MIN_LEADUP_VALID_PRIMARY = 3
NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605
LAGGED_WINDOW_START_DAYS = 30
LAGGED_WINDOW_END_DAYS = 90
MIN_LAGGED_DAYS = 40
TRIMMED_PCT = 0.10
MIN_BASELINE_STD = 0.5

# HA11-bout-redo restrictions
UNMED_START = date(2022, 4, 4)
UNMED_END = date(2024, 4, 8)
TRAIN_START = ANALYSIS_START  # 2022-09-03
DEVICE_BASELINE_LAG_DAYS = 21
APRIL_2024_CLUSTER_START = date(2024, 4, 9)
APRIL_2024_CLUSTER_END = date(2024, 4, 16)

# Resolve data root: env var first, then .env at repo root, then a known
# fallback (per the dispatcher's note that the worktree runs Windows-side
# with the data path stably co-located alongside the app repo).
def _resolve_data_root() -> Path:
    env_val = os.environ.get("GEVOELSCORE_DATA_PATH", "").strip()
    if env_val:
        return Path(env_val)
    # Walk up from this file looking for a .env that defines the var.
    here = Path(__file__).resolve()
    for ancestor in [here.parent, *here.parents]:
        env_file = ancestor / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() == "GEVOELSCORE_DATA_PATH":
                        return Path(v.strip().strip('"').strip("'"))
    raise RuntimeError(
        "GEVOELSCORE_DATA_PATH not set in env and no .env found"
    )


DATA_ROOT = _resolve_data_root()
UDIP_CSV = DATA_ROOT / "analyses" / "hypotheses" / "HA11-stress-udip" / "udip_counts.csv"
LABELS_CSV = DATA_ROOT / "processed" / "crash_labels" / "labels_crash_v2.csv"
PER_DAY_CSV = DATA_ROOT / "unified" / "per_day_master.csv"


def load_udip_counts() -> tuple[dict[date, int], dict[date, bool]]:
    counts: dict[date, int] = {}
    valid: dict[date, bool] = {}
    with UDIP_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            counts[d] = int(r["u_dip_count"])
            valid[d] = r["valid"] == "1"
    return counts, valid


def load_crashes() -> list[date]:
    crashes_by_id: dict[str, list[date]] = {}
    with LABELS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["label"] != "crash":
                continue
            d = date.fromisoformat(r["date"])
            crashes_by_id.setdefault(r["episode_id"], []).append(d)
    return sorted(min(ds) for ds in crashes_by_id.values())


def build_null_sample_replay(
    counts_v1: dict[date, int],
    valid_v1: dict[date, bool],
    crash_starts: list[date],
) -> list[date]:
    """Replay HA11 v1 build_null_sample exactly, returning the 200 reference
    dates (without overlap with crash leadups). Matches HA11 v1 test.py
    lines 190-219 verbatim, except it doesn't compute the episode profile
    (we only need the dates).
    """
    rng = random.Random(RANDOM_SEED)
    occupied: set[date] = set()
    for ref in crash_starts:
        for i in range(1, LEADUP_PRIMARY + 1):
            occupied.add(ref - timedelta(days=i))
    all_dates = sorted(
        d for d in counts_v1
        if valid_v1.get(d, False)
        and ANALYSIS_START + timedelta(days=10) <= d <= VALIDATE_END
    )
    out: list[date] = []
    attempts = 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 10000:
        attempts += 1
        ref = rng.choice(all_dates)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_PRIMARY + 1)}
        if leadup & occupied:
            continue
        # HA11 v1 also required >= 3 of 4 valid in the leadup for the episode
        # profile; we mirror that constraint to match exactly the reference
        # dates that HA11 v1's null sample contains.
        n_valid = sum(
            1 for d in leadup if d in counts_v1 and valid_v1.get(d, False)
        )
        if n_valid < MIN_LEADUP_VALID_PRIMARY:
            continue
        out.append(ref)
    return out


def load_per_day_bouts() -> tuple[dict[date, float | None], dict[date, bool]]:
    """Load bout_n_fast_recovery_day per date + has_garmin_uds per date."""
    bouts: dict[date, float | None] = {}
    has_uds: dict[date, bool] = {}
    with PER_DAY_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            raw = r["bout_n_fast_recovery_day"]
            bouts[d] = float(raw) if raw not in ("", None) else None
            has_uds[d] = r["has_garmin_uds"].strip().lower() == "true"
    return bouts, has_uds


def device_baseline_lag_set(has_uds: dict[date, bool]) -> set[date]:
    """First DEVICE_BASELINE_LAG_DAYS dates with has_garmin_uds=True."""
    uds_dates = sorted(d for d, v in has_uds.items() if v)
    return set(uds_dates[:DEVICE_BASELINE_LAG_DAYS])


def trimmed_list(values: list[float], trim_pct: float) -> list[float]:
    if not values:
        return []
    vs = sorted(values)
    n = len(vs)
    trim = int(n * trim_pct)
    if n - 2 * trim < 1:
        return vs
    return vs[trim:n - trim]


def compute_baseline_mu_sigma(
    d: date,
    series: dict[date, float | None],
    is_day_valid: dict[date, bool],
) -> tuple[float | None, float | None]:
    """Trimmed mean + stdev of `series` over [d-90, d-30] for prior days that
    are themselves valid AND have non-None series value. Returns (mu, sigma)
    or (None, None) if < MIN_LAGGED_DAYS valid prior days or sigma <= 0.5.
    """
    prior_vals: list[float] = []
    for i in range(LAGGED_WINDOW_START_DAYS + 1, LAGGED_WINDOW_END_DAYS + 1):
        wd = d - timedelta(days=i)
        if (
            wd in series
            and series[wd] is not None
            and is_day_valid.get(wd, False)
        ):
            prior_vals.append(float(series[wd]))
    if len(prior_vals) < MIN_LAGGED_DAYS:
        return None, None
    trimmed = trimmed_list(prior_vals, TRIMMED_PCT)
    if len(trimmed) < 2:
        return None, None
    mu = statistics.mean(trimmed)
    sigma = statistics.stdev(trimmed)
    if sigma <= MIN_BASELINE_STD:
        return None, None
    return mu, sigma


def day_is_valid_for_bout_redo(
    d: date,
    bouts: dict[date, float | None],
    baseline_lag_set: set[date],
) -> bool:
    """A day enters the bout-redo analysis if:
      - era: TRAIN_START <= d <= TRAIN_END
      - bout_n_fast_recovery_day not NaN
      - not in device-baseline lag set
      - not in April 2024 cluster (trivially satisfied for train-era)
    """
    if not (TRAIN_START <= d <= TRAIN_END):
        return False
    if bouts.get(d) is None:
        return False
    if d in baseline_lag_set:
        return False
    if APRIL_2024_CLUSTER_START <= d <= APRIL_2024_CLUSTER_END:
        return False
    return True


def main() -> int:
    print(f"DATA_ROOT = {DATA_ROOT}")
    print(f"UDIP_CSV  = {UDIP_CSV}")
    print(f"LABELS    = {LABELS_CSV}")
    print(f"PER_DAY   = {PER_DAY_CSV}")
    print()

    # 1. HA11 v1 reference-pool inputs.
    counts_v1, valid_v1 = load_udip_counts()
    crashes = load_crashes()
    print(f"HA11 v1 udip_counts.csv rows: {len(counts_v1)}; "
          f"valid days: {sum(valid_v1.values())}")
    print(f"crash episode starts (from labels_crash_v2.csv): {len(crashes)}")
    print()

    # 2. Regenerate the 200 HA11 v1 null-pool reference dates.
    null_refs = build_null_sample_replay(counts_v1, valid_v1, crashes)
    print(f"HA11 v1 null-pool reference dates (replayed, seed {RANDOM_SEED}): "
          f"{len(null_refs)}")
    print(f"  earliest: {min(null_refs)}; latest: {max(null_refs)}")
    n_train = sum(1 for r in null_refs if TRAIN_START <= r <= TRAIN_END)
    n_train_unmed = sum(
        1 for r in null_refs
        if TRAIN_START <= r <= TRAIN_END and UNMED_START <= r <= UNMED_END
    )
    print(f"  in train era (2022-09-03..2023-12-31): {n_train}")
    print(f"  in train era AND unmedicated phase: {n_train_unmed}")
    print()

    # 3. Bout-redo data + device-baseline-lag set.
    bouts, has_uds = load_per_day_bouts()
    print(f"per_day_master.csv rows: {len(bouts)}; "
          f"has_garmin_uds=True days: {sum(has_uds.values())}; "
          f"bout column non-NaN: "
          f"{sum(1 for v in bouts.values() if v is not None)}")
    baseline_lag = device_baseline_lag_set(has_uds)
    print(f"device-baseline-lag set (first {DEVICE_BASELINE_LAG_DAYS} UDS=True "
          f"days): {min(baseline_lag)} .. {max(baseline_lag)}")
    print()

    # 4. Build the per-day validity map for bout-redo (HA11-bout-redo §4.4).
    bout_redo_valid: dict[date, bool] = {
        d: day_is_valid_for_bout_redo(d, bouts, baseline_lag) for d in bouts
    }
    n_bout_redo_valid_train = sum(
        1 for d, v in bout_redo_valid.items() if v
    )
    print(f"bout-redo-valid days in train era: {n_bout_redo_valid_train}")
    print()

    # 5. Build the analysis-day pool: bout-redo-valid AND has valid (mu, sigma)
    # lagged baseline on bout_n_fast_recovery_day.
    analysis_day_z_inputs: list[tuple[date, float, float, float]] = []  # (d, bout, mu, sigma)
    sigma_skips = 0
    insufficient_baseline_skips = 0
    for d in sorted(bouts):
        if not bout_redo_valid[d]:
            continue
        mu, sigma = compute_baseline_mu_sigma(d, bouts, bout_redo_valid)
        if mu is None and sigma is None:
            # Either insufficient prior days OR sigma <= 0.5. Re-compute to
            # distinguish.
            prior_vals = [
                float(bouts[d - timedelta(days=i)])
                for i in range(LAGGED_WINDOW_START_DAYS + 1, LAGGED_WINDOW_END_DAYS + 1)
                if (d - timedelta(days=i)) in bouts
                and bouts[d - timedelta(days=i)] is not None
                and bout_redo_valid.get(d - timedelta(days=i), False)
            ]
            if len(prior_vals) < MIN_LAGGED_DAYS:
                insufficient_baseline_skips += 1
            else:
                trimmed = trimmed_list(prior_vals, TRIMMED_PCT)
                if len(trimmed) >= 2:
                    sigma_emp = statistics.stdev(trimmed)
                    if sigma_emp <= MIN_BASELINE_STD:
                        sigma_skips += 1
                    else:
                        insufficient_baseline_skips += 1
                else:
                    insufficient_baseline_skips += 1
            continue
        bv = bouts[d]
        assert bv is not None  # bout_redo_valid implies non-None
        analysis_day_z_inputs.append((d, float(bv), float(mu), float(sigma)))

    print(f"analysis days with valid lagged baseline (>= 40/60 prior valid, "
          f"sigma > 0.5): {len(analysis_day_z_inputs)}")
    print(f"  skipped: insufficient baseline = {insufficient_baseline_skips}; "
          f"sigma <= 0.5 (low-variability) = {sigma_skips}")
    print()

    # 6. Compute effective n: number of reference dates r in null_refs such
    # that r is in the analysis pool AND the 4-day window [r-3, r] has >= 3
    # of 4 days with a valid bout_n_fast_recovery_day AND a valid (mu,sigma).
    analysis_day_set = {row[0] for row in analysis_day_z_inputs}
    refs_in_unmed_train: list[date] = [
        r for r in null_refs
        if TRAIN_START <= r <= TRAIN_END
        and UNMED_START <= r <= UNMED_END
    ]
    print(f"reference dates in unmed x train era (pre-window-coverage): "
          f"{len(refs_in_unmed_train)}")

    eligible_refs: list[date] = []
    for r in refs_in_unmed_train:
        window = [r - timedelta(days=i) for i in range(0, LEADUP_PRIMARY)]  # [r-3, r-2, r-1, r]
        n_valid_in_window = sum(1 for d in window if d in analysis_day_set)
        if n_valid_in_window >= MIN_LEADUP_VALID_PRIMARY:
            eligible_refs.append(r)
    print()
    print("===========================================================")
    print(f"EFFECTIVE n (post all restrictions per §4.4 + §4.5 + §4.7):")
    print(f"  {len(eligible_refs)}")
    print(f"  walk-forward gate §4.9 (n >= 30 in calm-day pool): "
          f"{'PASS' if len(eligible_refs) >= 30 else 'FAIL'}")
    print("===========================================================")
    print()

    # 7. Sigma distribution of bout_n_fast_recovery_day across the analysis
    # days, plus the equivalent u_dip_count sigma distribution from HA11 v1.
    sigmas_bout = [row[3] for row in analysis_day_z_inputs]
    if sigmas_bout:
        sb = sorted(sigmas_bout)
        n = len(sb)
        median = sb[n // 2]
        q1 = sb[n // 4]
        q3 = sb[3 * n // 4]
        print(f"sigma distribution of bout_n_fast_recovery_day across "
              f"{n} analysis days:")
        print(f"  min/Q1/median/Q3/max = "
              f"{sb[0]:.3f} / {q1:.3f} / {median:.3f} / "
              f"{q3:.3f} / {sb[-1]:.3f}")
        print(f"  mean / stdev-of-sigmas = "
              f"{statistics.mean(sb):.3f} / {statistics.stdev(sb):.3f}")
    else:
        print("sigma distribution of bout_n_fast_recovery_day: NO ANALYSIS DAYS")
    print()

    # Compute the HA11 v1 u_dip_count sigma distribution on the equivalent pool
    # (unmed x train era, satisfying HA11 v1 validity).
    udip_sigmas: list[float] = []
    for d in sorted(counts_v1):
        if not (TRAIN_START <= d <= TRAIN_END):
            continue
        if not (UNMED_START <= d <= UNMED_END):
            continue
        if not valid_v1.get(d, False):
            continue
        # Compute lagged baseline using HA11 v1's own valid flag.
        prior_vals = []
        for i in range(LAGGED_WINDOW_START_DAYS + 1, LAGGED_WINDOW_END_DAYS + 1):
            wd = d - timedelta(days=i)
            if wd in counts_v1 and valid_v1.get(wd, False):
                prior_vals.append(float(counts_v1[wd]))
        if len(prior_vals) < MIN_LAGGED_DAYS:
            continue
        trimmed = trimmed_list(prior_vals, TRIMMED_PCT)
        if len(trimmed) < 2:
            continue
        sigma = statistics.stdev(trimmed)
        if sigma <= MIN_BASELINE_STD:
            continue
        udip_sigmas.append(sigma)
    if udip_sigmas:
        us = sorted(udip_sigmas)
        n = len(us)
        median = us[n // 2]
        q1 = us[n // 4]
        q3 = us[3 * n // 4]
        print(f"sigma distribution of HA11 v1 u_dip_count on equivalent pool "
              f"({n} analysis days):")
        print(f"  min/Q1/median/Q3/max = "
              f"{us[0]:.3f} / {q1:.3f} / {median:.3f} / "
              f"{q3:.3f} / {us[-1]:.3f}")
        print(f"  mean / stdev-of-sigmas = "
              f"{statistics.mean(us):.3f} / {statistics.stdev(us):.3f}")
    print()

    # Distribution of bout_n_fast_recovery_day values themselves
    # (mean + median + zero-rate) on the analysis pool — context for the
    # sigma-distribution comparison.
    bout_vals = [row[1] for row in analysis_day_z_inputs]
    if bout_vals:
        bv = sorted(bout_vals)
        nz = sum(1 for v in bv if v == 0)
        print(f"bout_n_fast_recovery_day distribution across "
              f"{len(bv)} analysis days:")
        print(f"  mean / median = {statistics.mean(bv):.3f} / "
              f"{bv[len(bv) // 2]:.3f}")
        print(f"  zero-day count / fraction = {nz} / "
              f"{nz / len(bv):.3f}")
        print(f"  min/max = {bv[0]:.0f} / {bv[-1]:.0f}")
        try:
            print(f"  raw stdev = {statistics.stdev(bv):.3f}")
        except statistics.StatisticsError:
            pass
    udip_vals_unmed_train = [
        counts_v1[d] for d in counts_v1
        if TRAIN_START <= d <= TRAIN_END
        and UNMED_START <= d <= UNMED_END
        and valid_v1.get(d, False)
    ]
    if udip_vals_unmed_train:
        uv = sorted(udip_vals_unmed_train)
        nz = sum(1 for v in uv if v == 0)
        print(f"HA11 v1 u_dip_count distribution on equivalent pool "
              f"({len(uv)} days):")
        print(f"  mean / median = {statistics.mean(uv):.3f} / "
              f"{uv[len(uv) // 2]:.3f}")
        print(f"  zero-day count / fraction = {nz} / "
              f"{nz / len(uv):.3f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
