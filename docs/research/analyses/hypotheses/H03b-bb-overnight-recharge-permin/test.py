"""H03b — Per-minute overnight Body Battery recharge as crash precursor.

Pre-registered 2026-06-07 in hypothesis.md. Locked spec executed
2026-06-07 per user-approved decision to run H03b knowing the
locked n>=10 inconclusive threshold will likely trigger
(data-availability investigation showed sleepBodyBattery is empty
for dates before mid-2024).

DATA SOURCE DEVIATION FROM HYPOTHESIS.MD (per playbook section 2.5
audit-trail discipline):
- hypothesis.md section 3 specified the
  /wellness-service/wellness/bodyBattery/events/{date} endpoint.
- Investigation 2026-06-07 confirmed this endpoint returns event
  records (sleep, activities, naps), NOT per-minute samples. For
  2026-05-15, get_body_battery_events returned empty list.
- The actual per-3-min BB during sleep window IS available via the
  sleep API endpoint as sleepBodyBattery array (236 samples for
  2026-05-15, 3-min interval). This is sufficient for the H03b
  metric (overnight recharge = peak_in_sleep_window -
  sleep_onset_value).
- Therefore: this script uses cached sleep API responses
  (api_pull/sleep/) which contain sleepBodyBattery directly. No
  separate BB backfill needed.
- The endpoint-change is documented but does NOT change the
  hypothesis itself (claim, threshold, window, direction, bar all
  unchanged from hypothesis.md). Per playbook section 2.2, only
  spec changes that change the test create a new ID; an
  implementation-source clarification is audit-trail, not respec.

DATA AVAILABILITY (locked finding from 2026-06-07 investigation):
- sleepBodyBattery array is empty for all dates before ~2024-06-15.
- bodyBatteryChange (daily scalar) is None for all dates before
  ~2023-12-31.
- Of 29 crash_v1 episodes, only ~5-6 have both per-minute BB
  available AND a usable lagged baseline (which itself needs
  ≥40 of 60 prior days with valid sleepBodyBattery).
- Therefore: H03b is expected to return INCONCLUSIVE under the
  locked n_clean >= 10 threshold (hypothesis.md section 5).

Output:
- result-data.json: per-crash overnight recharge profiles + null
  sample + verdicts per N_std + data-availability table.
- stdout: dry-run gate + data-availability summary + verdicts.
"""
from __future__ import annotations

import csv
import json
import random
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
GARMIN_ROOT = HERE.parent.parent
LABELS_CSV = GARMIN_ROOT / "hypotheses" / "crash_v2-definition" / "labels_crash_v2.csv"
SLEEP_CACHE = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data\api_pull\sleep"
)
OUT_JSON = HERE / "result-data.json"

ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LEADUP_PRIMARY = 4
LEADUP_SECONDARY = 5
NULL_SAMPLE_SIZE = 200
RANDOM_SEED = 20260605

# Locked thresholds per hypothesis.md section 4.6
N_STD_TIERS = [1.5, 2.0, 2.5]

# Locked 3-criterion bar per hypothesis.md section 5
CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15
# crit (c) median |z| >= N_std / 2

# Validity rules per hypothesis.md section 4.2-4.3
MIN_BB_SAMPLES_PER_NIGHT = 30
BASELINE_WINDOW_START_DAYS = 90
BASELINE_WINDOW_END_DAYS = 30
MIN_VALID_BASELINE_DAYS = 40
SIGMA_FLOOR_BB_POINTS = 3.0
TRIMMED_CUT_LOW = 0.10
TRIMMED_CUT_HIGH = 0.10

INCONCLUSIVE_THRESHOLD = 10


def load_crashes_v1() -> list[date]:
    crashes_by_id: dict[str, list[date]] = {}
    for r in csv.DictReader(LABELS_CSV.open(encoding="utf-8")):
        if r["label"] != "crash":
            continue
        d = date.fromisoformat(r["date"])
        crashes_by_id.setdefault(r["episode_id"], []).append(d)
    return sorted(min(ds) for ds in crashes_by_id.values())


def load_sleep_day(d: date) -> dict | None:
    """Load cached sleep API response for date d. Returns dict or None."""
    p = SLEEP_CACHE / d.strftime("%Y-%m") / f"{d.isoformat()}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def overnight_recharge_for_day(d: date) -> dict | None:
    """Compute overnight recharge for sleep ending on date d.

    Per hypothesis.md section 4.1:
    - sleep_onset_value: first sleepBodyBattery sample (at sleep onset)
    - peak_during_sleep: max sleepBodyBattery in sleep window
    - overnight_recharge = peak - sleep_onset

    Validity (section 4.2):
    - Sleep window identified from sleepData (sleepStartTimestampGMT)
    - >=30 valid sleepBodyBattery samples
    - overnight_recharge in [0, 100]

    Returns None if invalid.
    """
    raw = load_sleep_day(d)
    if raw is None:
        return None
    dto = raw.get("dailySleepDTO", {})
    sleep_start = dto.get("sleepStartTimestampGMT")
    if not sleep_start:
        return None
    sbb = raw.get("sleepBodyBattery", [])
    if not isinstance(sbb, list) or len(sbb) < MIN_BB_SAMPLES_PER_NIGHT:
        return None
    values = [s.get("value") for s in sbb if isinstance(s, dict) and s.get("value") is not None]
    if len(values) < MIN_BB_SAMPLES_PER_NIGHT:
        return None
    sleep_onset_value = values[0]
    peak = max(values)
    recharge = peak - sleep_onset_value
    if not (0 <= recharge <= 100):
        return None
    return {
        "date": d.isoformat(),
        "sleep_onset_value": sleep_onset_value,
        "peak_during_sleep": peak,
        "overnight_recharge": recharge,
        "n_samples": len(values),
    }


def lagged_baseline(d: date, recharge_by_date: dict[date, dict]) -> dict | None:
    """Compute lagged baseline (trimmed mean + stdev) for day d.

    Per hypothesis.md section 4.3:
    - Window: [d-90, d-30] (60 days)
    - Trimmed mean (10/90 cut)
    - Sigma over same trimmed values
    - Compute only if >=40 valid days
    - If sigma <= 3.0 BB points, flag as low-variability and skip
    """
    window_days = [
        d - timedelta(days=i)
        for i in range(BASELINE_WINDOW_END_DAYS, BASELINE_WINDOW_START_DAYS + 1)
    ]
    valid_recharges = []
    for wd in window_days:
        r = recharge_by_date.get(wd)
        if r is not None:
            valid_recharges.append(r["overnight_recharge"])
    if len(valid_recharges) < MIN_VALID_BASELINE_DAYS:
        return None
    sorted_r = sorted(valid_recharges)
    n = len(sorted_r)
    low_cut = int(n * TRIMMED_CUT_LOW)
    high_cut = n - int(n * TRIMMED_CUT_HIGH)
    trimmed = sorted_r[low_cut:high_cut]
    if len(trimmed) < 10:
        return None
    mu = sum(trimmed) / len(trimmed)
    if len(trimmed) < 2:
        return None
    sigma = (sum((v - mu) ** 2 for v in trimmed) / (len(trimmed) - 1)) ** 0.5
    if sigma <= SIGMA_FLOOR_BB_POINTS:
        return {"mu": mu, "sigma": sigma, "n_valid": len(valid_recharges),
                "low_variability_flag": True}
    return {"mu": mu, "sigma": sigma, "n_valid": len(valid_recharges),
            "low_variability_flag": False}


def per_day_z(d: date, recharge_by_date: dict[date, dict],
              baseline_cache: dict[date, dict | None]) -> dict | None:
    """Compute z-score for day d. Returns None if invalid."""
    r = recharge_by_date.get(d)
    if r is None:
        return None
    if d not in baseline_cache:
        baseline_cache[d] = lagged_baseline(d, recharge_by_date)
    bl = baseline_cache[d]
    if bl is None or bl["low_variability_flag"]:
        return None
    delta = r["overnight_recharge"] - bl["mu"]
    z = delta / bl["sigma"]
    return {
        "date": d.isoformat(),
        "overnight_recharge": r["overnight_recharge"],
        "mu": bl["mu"],
        "sigma": bl["sigma"],
        "delta": delta,
        "z": z,
        "abs_z": abs(z),
    }


def lead_up_profile(ref: date, leadup_days: int,
                    recharge_by_date: dict[date, dict],
                    baseline_cache: dict[date, dict | None]) -> dict | None:
    """Per-episode lead-up profile. Bidirectional primary: max |z|.

    Returns None if validity fails (less than min_valid_days of leadup
    have a valid z-score).
    """
    if leadup_days == LEADUP_PRIMARY:
        min_valid = 3
    else:
        min_valid = 4
    days = [ref - timedelta(days=i) for i in range(1, leadup_days + 1)]
    zs = []
    for d in days:
        z_info = per_day_z(d, recharge_by_date, baseline_cache)
        if z_info is not None:
            zs.append(z_info)
    if len(zs) < min_valid:
        return None
    max_abs_z = max(z["abs_z"] for z in zs)
    # Direction at the max-abs-z day
    max_z_day = max(zs, key=lambda x: x["abs_z"])
    direction = "elevated" if max_z_day["z"] > 0 else "lowered"
    return {
        "ref": ref.isoformat(),
        "n_valid_leadup_days": len(zs),
        "max_abs_z": max_abs_z,
        "direction_at_max": direction,
        "all_z": [z["z"] for z in zs],
    }


def build_recharge_cache() -> dict[date, dict]:
    """Build recharge by date for the analysis window."""
    out = {}
    d = ANALYSIS_START - timedelta(days=BASELINE_WINDOW_START_DAYS)
    while d <= VALIDATE_END:
        r = overnight_recharge_for_day(d)
        if r is not None:
            out[d] = r
        d += timedelta(days=1)
    return out


def build_null_sample(recharge_by_date: dict[date, dict],
                      crash_starts: list[date]) -> list[date]:
    """200 random non-overlapping reference dates. Only valid days eligible."""
    rng = random.Random(RANDOM_SEED)
    occupied: set[date] = set()
    for ref in crash_starts:
        for i in range(1, LEADUP_SECONDARY + 1):
            occupied.add(ref - timedelta(days=i))
    eligible = sorted(
        d for d in recharge_by_date
        if ANALYSIS_START + timedelta(days=BASELINE_WINDOW_START_DAYS) <= d <= VALIDATE_END
    )
    out = []
    attempts = 0
    while len(out) < NULL_SAMPLE_SIZE and attempts < 20000:
        attempts += 1
        ref = rng.choice(eligible)
        leadup = {ref - timedelta(days=i) for i in range(1, LEADUP_PRIMARY + 1)}
        if leadup & occupied:
            continue
        out.append(ref)
    return out


def evaluate(events: list[date], nulls: list[date], window_days: int,
             n_std: float, recharge_by_date: dict[date, dict],
             baseline_cache: dict[date, dict | None],
             era_label: str) -> dict:
    """3-criterion bar evaluation per hypothesis.md section 5.

    Bidirectional primary: trigger if max |z| >= N_std.
    """
    event_profiles = []
    for d in events:
        p = lead_up_profile(d, window_days, recharge_by_date, baseline_cache)
        if p is not None:
            event_profiles.append(p)

    null_profiles = []
    for d in nulls:
        p = lead_up_profile(d, window_days, recharge_by_date, baseline_cache)
        if p is not None:
            null_profiles.append(p)

    if len(event_profiles) < INCONCLUSIVE_THRESHOLD:
        return {
            "era": era_label,
            "window_days": window_days,
            "n_std": n_std,
            "verdict": "inconclusive",
            "n_clean": len(event_profiles),
            "n_null": len(null_profiles),
            "reason": f"n_clean={len(event_profiles)} < {INCONCLUSIVE_THRESHOLD} (insufficient data per playbook + hypothesis.md section 5)",
        }

    frac_event = sum(1 for p in event_profiles if p["max_abs_z"] >= n_std) / len(event_profiles)
    frac_null = sum(1 for p in null_profiles if p["max_abs_z"] >= n_std) / max(1, len(null_profiles))
    disc_pp = (frac_event - frac_null) * 100

    triggering_z = [p["max_abs_z"] for p in event_profiles if p["max_abs_z"] >= n_std]
    median_z = statistics.median(triggering_z) if triggering_z else 0.0

    # Direction split at primary tier
    triggers = [p for p in event_profiles if p["max_abs_z"] >= n_std]
    n_elev = sum(1 for p in triggers if p["direction_at_max"] == "elevated")
    n_low = sum(1 for p in triggers if p["direction_at_max"] == "lowered")
    pct_elev = (n_elev / len(triggers) * 100) if triggers else 0.0
    pct_low = (n_low / len(triggers) * 100) if triggers else 0.0

    c_min = n_std / 2

    a = frac_event >= CRIT_A_FRAC
    b = disc_pp >= CRIT_B_DISC_PP
    c = median_z >= c_min

    return {
        "era": era_label,
        "window_days": window_days,
        "n_std": n_std,
        "n_clean": len(event_profiles),
        "n_null": len(null_profiles),
        "frac_event_triggers": frac_event,
        "frac_null_triggers": frac_null,
        "discrimination_pp": disc_pp,
        "median_abs_z_on_triggering": median_z,
        "pct_elevated_at_max": pct_elev,
        "pct_lowered_at_max": pct_low,
        "crit_a_pass": a,
        "crit_b_pass": b,
        "crit_c_pass": c,
        "verdict": "supported" if (a and b and c) else "refuted",
    }


def data_availability_summary(recharge_by_date: dict[date, dict],
                              crash_starts: list[date]) -> dict:
    """Summarise data availability across the analysis window."""
    train = [d for d in crash_starts if d <= TRAIN_END]
    val = [d for d in crash_starts if d > TRAIN_END]

    # Per-crash: does the 4-day primary lead-up have any valid recharge?
    def crash_has_leadup_data(ref):
        for i in range(1, LEADUP_PRIMARY + 1):
            if (ref - timedelta(days=i)) in recharge_by_date:
                return True
        return False

    # Per-crash: does the lagged baseline window have >=40 valid days?
    def crash_has_baseline(ref):
        # Use any leadup day for baseline reference
        for i in range(1, LEADUP_PRIMARY + 1):
            ld = ref - timedelta(days=i)
            bl = lagged_baseline(ld, recharge_by_date)
            if bl is not None and not bl.get("low_variability_flag", False):
                return True
        return False

    train_with_data = sum(1 for d in train if crash_has_leadup_data(d))
    train_with_baseline = sum(1 for d in train if crash_has_baseline(d))
    val_with_data = sum(1 for d in val if crash_has_leadup_data(d))
    val_with_baseline = sum(1 for d in val if crash_has_baseline(d))

    sorted_dates = sorted(recharge_by_date.keys())
    first_valid = sorted_dates[0].isoformat() if sorted_dates else None
    last_valid = sorted_dates[-1].isoformat() if sorted_dates else None

    return {
        "total_valid_recharge_days": len(recharge_by_date),
        "first_valid_recharge_date": first_valid,
        "last_valid_recharge_date": last_valid,
        "train_crashes_total": len(train),
        "train_crashes_with_any_leadup_recharge": train_with_data,
        "train_crashes_with_usable_baseline": train_with_baseline,
        "validate_crashes_total": len(val),
        "validate_crashes_with_any_leadup_recharge": val_with_data,
        "validate_crashes_with_usable_baseline": val_with_baseline,
    }


def dry_run_print(train: list[date], validate: list[date],
                  recharge_by_date: dict[date, dict],
                  baseline_cache: dict[date, dict | None]) -> dict:
    samples = []
    print("\n=== Dry-run gate (per playbook section 2.3) ===")
    for label, events in [("TRAIN", train[:3]), ("VALIDATE", validate[:3])]:
        print(f"\n--- {label} (first 3 crash starts) ---")
        for ref in events:
            print(f"\n  Crash start: {ref.isoformat()}")
            for i in range(1, LEADUP_PRIMARY + 1):
                ld = ref - timedelta(days=i)
                z_info = per_day_z(ld, recharge_by_date, baseline_cache)
                r = recharge_by_date.get(ld)
                if z_info:
                    print(f"    D-{i} ({ld.isoformat()}): recharge={r['overnight_recharge']:.1f}, "
                          f"baseline mu={z_info['mu']:.1f} sigma={z_info['sigma']:.2f}, "
                          f"z={z_info['z']:+.2f}")
                elif r:
                    bl = baseline_cache.get(ld)
                    bl_state = "no baseline" if bl is None else "low-variability baseline"
                    print(f"    D-{i} ({ld.isoformat()}): recharge={r['overnight_recharge']:.1f}, "
                          f"{bl_state}")
                else:
                    print(f"    D-{i} ({ld.isoformat()}): NO RECHARGE DATA")
            samples.append({"era": label.lower(), "ref": ref.isoformat()})
    return {"samples": samples}


def main():
    crash_starts = load_crashes_v1()
    train = [d for d in crash_starts if d <= TRAIN_END]
    validate = [d for d in crash_starts if d > TRAIN_END]
    print(f"crash_v1 total: {len(crash_starts)} (train={len(train)}, validate={len(validate)})")

    print("\nBuilding overnight recharge cache from sleep API data...")
    recharge_by_date = build_recharge_cache()
    print(f"  Valid overnight recharge days: {len(recharge_by_date)}")
    if recharge_by_date:
        sorted_dates = sorted(recharge_by_date.keys())
        print(f"  First valid: {sorted_dates[0]}")
        print(f"  Last valid:  {sorted_dates[-1]}")

    baseline_cache: dict[date, dict | None] = {}

    print("\nData-availability summary:")
    avail = data_availability_summary(recharge_by_date, crash_starts)
    for k, v in avail.items():
        print(f"  {k}: {v}")

    nulls = build_null_sample(recharge_by_date, crash_starts)
    print(f"\nNull sample: {len(nulls)} non-overlapping references "
          f"(target {NULL_SAMPLE_SIZE})")

    dry_run_data = dry_run_print(train, validate, recharge_by_date, baseline_cache)

    print("\n=== Running H03b evaluation grid (3 N_std x 2 windows x 2 eras) ===")
    results = []
    for window in [LEADUP_PRIMARY, LEADUP_SECONDARY]:
        for n_std in N_STD_TIERS:
            for events, era in [(train, "train"), (validate, "validate")]:
                r = evaluate(events, nulls, window, n_std,
                             recharge_by_date, baseline_cache, era)
                results.append(r)

    out = {
        "hypothesis": "H03b-bb-overnight-recharge-permin",
        "pre_registered": "2026-06-07 in hypothesis.md",
        "run_date": "2026-06-07",
        "data_source_deviation_note": (
            "hypothesis.md section 3 specified /wellness-service/wellness/bodyBattery/events/{date}; "
            "this endpoint actually returns event records (sleep/activities/naps), NOT per-minute samples. "
            "The per-3-min BB during sleep window IS available via the sleep API as sleepBodyBattery. "
            "Implementation uses cached sleep API data; the substantive metric "
            "(peak_during_sleep - sleep_onset_value) is unchanged. Per playbook section 2.2, "
            "this is an audit-trail clarification, not a spec change requiring a new ID."
        ),
        "config": {
            "analysis_start": ANALYSIS_START.isoformat(),
            "train_end": TRAIN_END.isoformat(),
            "validate_end": VALIDATE_END.isoformat(),
            "leadup_primary": LEADUP_PRIMARY,
            "leadup_secondary": LEADUP_SECONDARY,
            "null_sample_size": NULL_SAMPLE_SIZE,
            "random_seed": RANDOM_SEED,
            "n_std_tiers": N_STD_TIERS,
            "crit_a_frac": CRIT_A_FRAC,
            "crit_b_disc_pp": CRIT_B_DISC_PP,
            "baseline_window": f"[d-{BASELINE_WINDOW_START_DAYS}, d-{BASELINE_WINDOW_END_DAYS}]",
            "min_valid_baseline_days": MIN_VALID_BASELINE_DAYS,
            "sigma_floor_bb_points": SIGMA_FLOOR_BB_POINTS,
            "min_bb_samples_per_night": MIN_BB_SAMPLES_PER_NIGHT,
        },
        "data_availability": avail,
        "results": results,
        "dry_run": dry_run_data,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")

    print("\n=== Results table ===")
    print(f"{'era':10} {'window':>7} {'n_std':>6} {'verdict':12} {'n_clean':>8} {'disc_pp':>9} {'freq':>7}")
    for r in results:
        if r["verdict"] == "inconclusive":
            print(f"{r['era']:10} {r['window_days']:>7}d {r['n_std']:>6.1f} "
                  f"{r['verdict']:12} {r['n_clean']:>8}  "
                  f"(n_clean<{INCONCLUSIVE_THRESHOLD})")
        else:
            print(f"{r['era']:10} {r['window_days']:>7}d {r['n_std']:>6.1f} "
                  f"{r['verdict']:12} {r['n_clean']:>8} "
                  f"{r['discrimination_pp']:>+8.1f}  {r['frac_event_triggers']*100:>6.1f}%")

    print(f"\nWrote {OUT_JSON}")

    n_inc = sum(1 for r in results if r["verdict"] == "inconclusive")
    n_sup = sum(1 for r in results if r["verdict"] == "supported")
    n_ref = sum(1 for r in results if r["verdict"] == "refuted")
    print(f"\n=== Summary ===")
    print(f"  {n_inc} inconclusive / {n_sup} supported / {n_ref} refuted (of {len(results)} cells)")


if __name__ == "__main__":
    main()
