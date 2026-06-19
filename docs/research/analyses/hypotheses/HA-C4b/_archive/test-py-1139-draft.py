"""HA-C4b - Stage 2: stress-low-motion z-score precursor test.

Implements the locked HA-C4b pre-registration (hypothesis.md rev r3
2026-06-15). Loads per_day_master.csv + stress_low_motion_minutes.csv,
applies the exertion-conditioning rule (§4.2), the strict day-validity
gates (§4.3 incl. 1b.i sample-count >=900 + 1b.ii wake-window quartile
coverage), the per-phase lagged baseline (§4.5), per-day z-score
(§4.6), per-episode lead-up profile (§4.7), stationary-bootstrap null
at E[L]=7 (§4.9), and the 3-criterion + RD/OR-CI bar on the locked
headline cell (consolidation x S60_Mlow x N_std=1.5 x primary 4d x
one-sided elevated; §5.0 / §5.1).

Two modes:
  python test.py --dry-run    sample sizes + first-3 episodes + §7 sanity
  python test.py              full evaluation (only if dry-run passes)

§7 sanity-check halt conditions:
  per-phase n < 10 in consolidation in either era
  median primitive distribution outside expected range
  median baseline sigma outside [5, 40]
If any fails -> halt + write dry-run-report.md, do NOT emit result.md.

The wake-window quartile coverage gate (§4.3 1b.ii) requires per-minute
stress sample timestamps. These are not in any cached CSV; the script
walks the monitoring_b FIT files once to build a per-day 30-min-slot
sample-count cache (quartile_coverage_cache.csv) on first --full run.
The dry-run skips 1b.ii by default; the sanity gates rely on 1b.i and
exertion conditioning.
"""
from __future__ import annotations

import argparse
import bisect
import collections
import csv
import io
import json
import math
import os
import random
import statistics
import sys
import zipfile
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

# === Constants per locked hypothesis.md §4-§5 ===

ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LC_ERA_START = date(2022, 4, 4)

# §4.3 day-validity gates
MIN_SAMPLES_HA11 = 600   # inherited gate (the primitive `valid` flag)
MIN_SAMPLES_C4B = 900    # §4.3 1b.i strict
MIN_QUARTILE_SAMPLES = 50  # §4.3 1b.ii

# §4.5 lagged baseline
LAGGED_END_DAYS = 30
LAGGED_START_DAYS = 90
LAGGED_WINDOW_LEN = LAGGED_START_DAYS - LAGGED_END_DAYS  # 60
MIN_BASELINE_DAYS = 40
TRIMMED_PCT = 0.10
MIN_BASELINE_STD = 5.0   # minutes; below -> flag low-variability + skip

# §4.7 lead-up windows
LEADUP_PRIMARY = 4
LEADUP_SECONDARY = 5
MIN_LEADUP_VALID_PRIMARY = 3
MIN_LEADUP_VALID_SECONDARY = 4

# §4.8 N_std tiers
N_STD_PRIMARY = 1.5
N_STD_SECONDARY = 2.0
N_STD_SENSITIVITY = 2.5
N_STD_TIERS = [N_STD_PRIMARY, N_STD_SECONDARY, N_STD_SENSITIVITY]

# §4.9 stationary-bootstrap null
BOOTSTRAP_E_L = 7
B_HEADLINE = 10_000
B_DIAGNOSTIC = 1_000
RANDOM_SEED = 20260615

# §5 SUPPORTED bar (a)+(b)+(c)
CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15.0
# (c) median magnitude bar = N_std / 2

# §6 buildup buffer + April 2024 cluster
BUILDUP_BUFFER_END = date(2024, 4, 30)        # excl strictly before
APRIL2024_CLUSTER_START = date(2024, 4, 9)
APRIL2024_CLUSTER_END_INCL = date(2024, 4, 16)

# §4.4 Citalopram phase boundaries (per phase_stratification §3)
def citalopram_phase(d: date) -> str:
    if d < date(2024, 4, 9):
        return "unmedicated"
    if d < date(2024, 6, 20):
        return "buildup"
    if d < date(2026, 3, 20):
        return "consolidation"
    if d < date(2026, 6, 6):
        return "afbouw"
    return "post_afbouw"


PHASE_ORDER = ["unmedicated", "buildup", "consolidation", "afbouw"]
HEADLINE_PHASE = "consolidation"

# §4.10 sensitivity-ladder columns
PRIMARY_COL = "stress_low_motion_min_count_S60_Mlow"
LADDER_UNIQUE = [
    "stress_low_motion_min_count_S50_Mstrict",
    "stress_low_motion_min_count_S50_Mlow",
    "stress_low_motion_min_count_S60_Mstrict",
    PRIMARY_COL,
    "stress_low_motion_min_count_S75_Mstrict",
    "stress_low_motion_min_count_S75_Mlow",
]
LADDER_DUPLICATES = [
    "stress_low_motion_min_count_S50_Mbelow_mod",  # == S50_Mlow by construction
    "stress_low_motion_min_count_S60_Mbelow_mod",  # == S60_Mlow
    "stress_low_motion_min_count_S75_Mbelow_mod",  # == S75_Mlow
]

# §4.11 construct-disambiguation siblings
SIBLING_PRIMARY = "stress_high_duration_min"     # post-viz primary, rho=0.79
SIBLING_SECONDARY = "u_dip_count"                 # original, rho=0.556

# Respiration companion (§4.11.4)
RESP_COL = "n_minutes_resp_above_18"

# §4.2 heavy-exertion classes
HEAVY_CLASSES = {"heavy", "very_heavy"}

# §7 expected distributions (sanity check)
EXPECTED_MEDIAN_RANGE = {
    "unmedicated": (15, 60),
    "buildup": (20, 80),
    "consolidation": (35, 95),
    "afbouw": (20, 80),
}
SANITY_SIGMA_RANGE = (5.0, 40.0)
SANITY_MIN_EPISODES_PER_PHASE_ERA = 10

# Paths
HERE = Path(__file__).resolve().parent
DATA_ROOT = Path(os.environ.get(
    "GEVOELSCORE_DATA_PATH",
    r"C:\Users\Gebruiker\Documents\gevoelscore-data"))
MASTER_CSV = DATA_ROOT / "unified" / "per_day_master.csv"
SLM_CSV = DATA_ROOT / "processed" / "garmin" / "stress_low_motion_minutes.csv"
QUARTILE_CACHE = DATA_ROOT / "processed" / "garmin" / "stress_quartile_30min_cache.csv"
LABELS_CSV = DATA_ROOT / "processed" / "crash_labels" / "labels_crash_v2.csv"
GARMIN_DUMP = DATA_ROOT / "garmin data" / "DI_CONNECT" / "DI-Connect-Uploaded-Files"
CLASSIFIED_CSV = DATA_ROOT / "analyses" / "garmin_exploration" / "fit_files_classified.csv"

OUT_DATA_JSON = HERE / "result-data.json"
OUT_RESULT_MD = HERE / "result.md"
OUT_DRYRUN_MD = HERE / "dry-run-report.md"


# === Loaders ============================================================

def parse_iso_dt(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def load_master() -> dict[date, dict]:
    """date -> selected master columns (string values; cast at use)."""
    out: dict[date, dict] = {}
    needed = [
        "gevoelscore", "is_crash", "crash_episode_id",
        "exertion_class_lagged_lcera", "dose_plasma_mg",
        "sleep_start_gmt", "sleep_end_gmt",
        PRIMARY_COL, SIBLING_PRIMARY, SIBLING_SECONDARY, RESP_COL,
        *LADDER_UNIQUE, *LADDER_DUPLICATES,
    ]
    with MASTER_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                d = date.fromisoformat(row["date"])
            except (KeyError, ValueError):
                continue
            out[d] = {k: row.get(k, "") for k in needed}
    return out


def load_slm_valid() -> dict[date, dict]:
    """date -> {sample_count, valid_ha11}."""
    out: dict[date, dict] = {}
    with SLM_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                d = date.fromisoformat(row["date"])
                out[d] = {
                    "sample_count": int(row["sample_count"]),
                    "valid_ha11": int(row["valid"]) == 1,
                }
            except (KeyError, ValueError):
                continue
    return out


def load_crash_starts() -> list[date]:
    """First date of each crash_v2 episode, sorted."""
    by_id: dict[str, list[date]] = {}
    with LABELS_CSV.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("label") != "crash":
                continue
            try:
                d = date.fromisoformat(row["date"])
            except (KeyError, ValueError):
                continue
            by_id.setdefault(row["episode_id"], []).append(d)
    return sorted(min(ds) for ds in by_id.values())


# === Quartile-coverage cache (§4.3 1b.ii) ===============================

QUARTILE_SLOT_COLS = [f"slot_{i:02d}" for i in range(48)]  # 30-min UTC bins


def build_quartile_cache() -> None:
    """Walk all monitoring_b FITs once; emit per-date sample counts in
    48 x 30-min UTC slots. Skips if cache exists."""
    try:
        import fitdecode  # noqa: F401
    except ImportError:
        print("ERROR: fitdecode not installed; cannot build quartile cache.",
              file=sys.stderr)
        sys.exit(1)
    import fitdecode

    # Reuse the FIT-walk pattern from stress_low_motion_extract.py.
    sys.path.insert(
        0, str(HERE.parent.parent.parent / "analyses" / "garmin_exploration"
                / "scripts"))
    try:
        from fit_utils import Monitoring16Resolver  # noqa: F401
    except ImportError:
        # fit_utils only needed for timestamp_16 resolution on monitoring;
        # stress_level_time and respiration timestamps are full datetimes.
        # The quartile cache only needs stress_level_time -> we can proceed
        # without the resolver.
        pass

    if not CLASSIFIED_CSV.exists():
        print(f"ERROR: {CLASSIFIED_CSV} not found", file=sys.stderr)
        sys.exit(1)
    with CLASSIFIED_CSV.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    mfiles = [r for r in rows if r["type"] == "monitoring_b"]
    print(f"[quartile-cache] walking {len(mfiles)} monitoring_b FITs",
          file=sys.stderr)

    open_zips: dict[str, zipfile.ZipFile] = {}
    for z in {r["zip"] for r in mfiles}:
        open_zips[z] = zipfile.ZipFile(GARMIN_DUMP / z)

    # date -> 48-slot in-range stress sample counts
    slots_by_date: dict[date, list[int]] = collections.defaultdict(
        lambda: [0] * 48)
    # Dedupe to per-minute (latest sample wins) per HA11 / SLM extractor
    in_range_minutes: dict[date, set[tuple[int, int]]] = collections.defaultdict(set)

    for i, r in enumerate(mfiles):
        if i % 500 == 0:
            print(f"  [quartile-cache] {i}/{len(mfiles)}", file=sys.stderr)
        try:
            buf = open_zips[r["zip"]].read(r["filename"])
            with fitdecode.FitReader(io.BytesIO(buf)) as fit:
                for frame in fit:
                    if not isinstance(frame, fitdecode.FitDataMessage):
                        continue
                    if frame.name != "stress_level":
                        continue
                    ts = next((f.value for f in frame.fields
                               if f.name == "stress_level_time"
                               and isinstance(f.value, datetime)), None)
                    val = next((f.value for f in frame.fields
                                if f.name == "stress_level_value"), None)
                    if ts is None or val is None:
                        continue
                    try:
                        v = int(val)
                    except (TypeError, ValueError):
                        continue
                    if not (1 <= v <= 100):
                        continue
                    d = ts.date()
                    minute_key = (ts.hour, ts.minute)
                    if minute_key in in_range_minutes[d]:
                        continue
                    in_range_minutes[d].add(minute_key)
                    slot_idx = ts.hour * 2 + (1 if ts.minute >= 30 else 0)
                    slots_by_date[d][slot_idx] += 1
        except Exception as e:
            print(f"  [quartile-cache] warn: failed {r['filename']}: {e}",
                  file=sys.stderr)
            continue

    QUARTILE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    with QUARTILE_CACHE.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", *QUARTILE_SLOT_COLS])
        for d in sorted(slots_by_date.keys()):
            w.writerow([d.isoformat(), *slots_by_date[d]])
    print(f"[quartile-cache] wrote {QUARTILE_CACHE} "
          f"({len(slots_by_date)} dates)", file=sys.stderr)


def load_quartile_cache() -> dict[date, list[int]]:
    """date -> 48 ints (per-30-min in-range stress sample counts, UTC)."""
    if not QUARTILE_CACHE.exists():
        return {}
    out: dict[date, list[int]] = {}
    with QUARTILE_CACHE.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                d = date.fromisoformat(row["date"])
            except (KeyError, ValueError):
                continue
            out[d] = [int(row[col]) for col in QUARTILE_SLOT_COLS]
    return out


# Fixed quartiles in local NL (CET/CEST). 06-12, 12-18, 18-22, 22-02.
# We use a fixed CEST=UTC+2 assumption for simplicity: 04-10, 10-16,
# 16-20, 20-(00 next day). For the simplified test we count slots within
# the day in UTC; the 22-02 NL quartile spans into d+1 UTC and is
# approximated by counting 20:00-23:59 UTC of day d only. The fallback
# is rare (>98% of LC days have sleep boundaries).
FIXED_QUARTILES_UTC_SLOTS = [
    list(range(8, 20)),   # 04:00-10:00 UTC ~ 06-12 local CEST
    list(range(20, 32)),  # 10:00-16:00 UTC ~ 12-18 local CEST
    list(range(32, 40)),  # 16:00-20:00 UTC ~ 18-22 local CEST
    list(range(40, 48)),  # 20:00-24:00 UTC ~ 22-02 local CEST (no d+1 cross)
]


def passes_quartile_gate(d: date,
                          quartile_cache: dict[date, list[int]],
                          master: dict[date, dict]) -> tuple[bool, str]:
    """§4.3 1b.ii: each of 4 wake-window quartiles has >= 50 samples.
    Returns (passes, mode). mode in {sleep, fixed, no-cache, no-sleep}."""
    slots = quartile_cache.get(d)
    if slots is None:
        return (False, "no-cache")
    row = master.get(d, {})
    s_end = parse_iso_dt(row.get("sleep_end_gmt"))
    s_next = parse_iso_dt(master.get(d + timedelta(days=1), {}).get("sleep_start_gmt"))
    if s_end and s_next and s_next > s_end:
        # Wake window in UTC -> split into 4 equal-length quartiles
        total = (s_next - s_end).total_seconds()
        if total < 4 * 3600:
            # Wake window < 4 hours: degenerate; fall back to fixed
            mode = "fixed"
        else:
            q_dur = total / 4
            samples_per_q = [0, 0, 0, 0]
            for q_i in range(4):
                q_lo = s_end + timedelta(seconds=q_i * q_dur)
                q_hi = s_end + timedelta(seconds=(q_i + 1) * q_dur)
                # Iterate over 30-min slots between q_lo and q_hi
                # 48 slots in d; another 48 in d+1
                samples_per_q[q_i] = _sum_slots_in_range(
                    quartile_cache, d, q_lo, q_hi)
            ok = all(s >= MIN_QUARTILE_SAMPLES for s in samples_per_q)
            return (ok, "sleep")
    else:
        mode = "fixed"
    # Fallback: fixed-time quartiles in UTC approximation
    samples_per_q = [
        sum(slots[i] for i in q_slots)
        for q_slots in FIXED_QUARTILES_UTC_SLOTS
    ]
    ok = all(s >= MIN_QUARTILE_SAMPLES for s in samples_per_q)
    return (ok, mode)


def _sum_slots_in_range(cache: dict[date, list[int]],
                         d: date,
                         lo: datetime, hi: datetime) -> int:
    """Sum cache slot counts overlapping the [lo, hi) UTC interval.
    Slots are 30 min each; index 0 = 00:00-00:30 UTC of date d."""
    total = 0
    for day_offset in (0, 1):
        dd = d + timedelta(days=day_offset)
        slots = cache.get(dd)
        if slots is None:
            continue
        for slot_i in range(48):
            slot_lo = datetime.combine(dd, time()) + timedelta(minutes=slot_i * 30)
            slot_hi = slot_lo + timedelta(minutes=30)
            # Strip tz from sleep dt for compare (master times have +00:00)
            lo_n = lo.replace(tzinfo=None) if lo.tzinfo else lo
            hi_n = hi.replace(tzinfo=None) if hi.tzinfo else hi
            if slot_hi <= lo_n or slot_lo >= hi_n:
                continue
            # Overlap fraction (approximate; treat as full credit for
            # any overlap >= 5 min, otherwise zero)
            overlap_min = (min(slot_hi, hi_n) - max(slot_lo, lo_n)).total_seconds() / 60
            if overlap_min >= 5:
                total += slots[slot_i]
    return total


# === Validity & eligibility =============================================

def day_basic_valid(d: date,
                     slm: dict[date, dict],
                     master: dict[date, dict],
                     enforce_900: bool = True) -> tuple[bool, str]:
    """§4.3 conditions 1 + 1b.i (+ data presence + has crash label).
    Returns (valid, reason_if_invalid)."""
    if d not in master:
        return (False, "no-master")
    if d not in slm:
        return (False, "no-slm")
    if not slm[d]["valid_ha11"]:
        return (False, "ha11-gate-fail (<600 samples)")
    if enforce_900 and slm[d]["sample_count"] < MIN_SAMPLES_C4B:
        return (False, "1b.i-fail (<900 samples)")
    if not master[d].get("is_crash"):
        return (False, "no-crash-label")
    return (True, "")


def day_exertion_eligible(d: date, master: dict[date, dict]) -> tuple[bool, str]:
    """§4.2: exertion_class_lagged_lcera in heavy/very_heavy on d OR d-1."""
    today = (master.get(d) or {}).get("exertion_class_lagged_lcera", "").strip()
    yest = (master.get(d - timedelta(days=1)) or {}).get(
        "exertion_class_lagged_lcera", "").strip()
    if not today and not yest:
        return (False, "no-exertion-data-on-d-or-d-1")
    if today in HEAVY_CLASSES or yest in HEAVY_CLASSES:
        return (True, "")
    return (False, "not-heavy-on-d-or-d-1")


def day_in_buildup_buffer(d: date) -> bool:
    """§6 buildup CPAP-end buffer: exclude strictly before 2024-04-30."""
    return APRIL2024_CLUSTER_START <= d < BUILDUP_BUFFER_END


def day_in_april2024_cluster(d: date) -> bool:
    """§6 structurally-unanalyzable cluster: 2024-04-09 to 2024-04-16."""
    return APRIL2024_CLUSTER_START <= d <= APRIL2024_CLUSTER_END_INCL


def day_eligible(d: date,
                  slm: dict[date, dict],
                  master: dict[date, dict],
                  quartile_cache: dict[date, list[int]] | None) -> tuple[bool, str]:
    """Compose §4.2 + §4.3 + §6 exclusions.
    If quartile_cache is None or empty, 1b.ii is skipped (dry-run mode)."""
    if d < LC_ERA_START:
        return (False, "pre-LC")
    if day_in_april2024_cluster(d):
        return (False, "april-2024-cluster")
    ok, why = day_basic_valid(d, slm, master)
    if not ok:
        return (False, why)
    ok, why = day_exertion_eligible(d, master)
    if not ok:
        return (False, why)
    if quartile_cache:
        ok, mode = passes_quartile_gate(d, quartile_cache, master)
        if not ok:
            return (False, f"1b.ii-fail ({mode})")
    return (True, "")


def get_predictor(d: date, master: dict[date, dict], col: str) -> float | None:
    raw = (master.get(d) or {}).get(col, "")
    if raw == "" or raw is None:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


# === Lagged baseline (§4.5) =============================================

def compute_lagged_baseline(d: date,
                              col: str,
                              eligible_pool_by_phase: dict[str, dict[date, dict[str, float]]],
                              ) -> tuple[float | None, float | None, int]:
    """Trimmed mean + std over [d-90, d-30] valid same-phase days.
    Returns (mu, sigma, n_prior). (None, None, n) if insufficient or
    sigma <= MIN_BASELINE_STD."""
    phase = citalopram_phase(d)
    pool = eligible_pool_by_phase.get(phase, {})
    vals: list[float] = []
    for i in range(LAGGED_END_DAYS + 1, LAGGED_START_DAYS + 1):
        wd = d - timedelta(days=i)
        rec = pool.get(wd)
        if rec and col in rec:
            vals.append(rec[col])
    n_prior = len(vals)
    if n_prior < MIN_BASELINE_DAYS:
        return (None, None, n_prior)
    sv = sorted(vals)
    n = len(sv)
    trim = int(n * TRIMMED_PCT)
    if n - 2 * trim < 2:
        return (None, None, n_prior)
    trimmed = sv[trim:n - trim]
    mu = statistics.mean(trimmed)
    sigma = statistics.stdev(trimmed)
    if sigma <= MIN_BASELINE_STD:
        return (None, None, n_prior)
    return (mu, sigma, n_prior)


# === Per-day z + episode profile (§4.6 + §4.7) ==========================

def per_day_signed_z(d: date,
                       col: str,
                       master: dict[date, dict],
                       eligible_pool_by_phase: dict[str, dict[date, float]],
                       ) -> float | None:
    val = get_predictor(d, master, col)
    if val is None:
        return None
    mu, sigma, _ = compute_lagged_baseline(d, col, eligible_pool_by_phase)
    if mu is None or sigma is None:
        return None
    return (val - mu) / sigma


def episode_profile(ref: date,
                      col: str,
                      master: dict[date, dict],
                      eligible_pool_by_phase: dict[str, dict[date, float]],
                      leadup_days: int,
                      min_valid: int) -> dict | None:
    """Return None if too few valid lead-up days."""
    signed: list[float] = []
    for i in range(1, leadup_days + 1):
        z = per_day_signed_z(ref - timedelta(days=i), col, master,
                              eligible_pool_by_phase)
        if z is None:
            continue
        signed.append(z)
    if len(signed) < min_valid:
        return None
    return {
        "leadup_n": len(signed),
        "all_signed_zs": signed,
        "max_signed_z": max(signed),
        "min_signed_z": min(signed),
        "max_abs_z": max(abs(z) for z in signed),
    }


# === Stationary-bootstrap null (§4.9) ===================================

def stationary_bootstrap_label_indices(n: int,
                                        n_crashes: int,
                                        rng: random.Random) -> list[int]:
    """Generate a permuted sequence of length n; the indices marked as
    crashes are the first n_crashes positions of a random permutation
    of [0..n-1] sampled in stationary-bootstrap fashion: draw blocks of
    length ~Geometric(1/E[L]); each block is a contiguous slice of
    [0..n-1] starting at a random index; concatenate (wrapping) until
    we have n indices; the first n_crashes of those are the permuted
    crash positions.

    This preserves within-block adjacency of the underlying time index
    so that crash 'lumps' are preserved at the block scale."""
    idx: list[int] = []
    p = 1.0 / BOOTSTRAP_E_L
    while len(idx) < n:
        start = rng.randrange(n)
        # geometric block length, mean E[L]
        L = 1
        while rng.random() >= p:
            L += 1
        for j in range(L):
            idx.append((start + j) % n)
            if len(idx) >= n:
                break
    # The first n_crashes indices in the bootstrap-permuted sequence are
    # the crash positions in this draw
    return idx[:n_crashes]


def evaluate_trigger_freq(refs: list[date],
                            col: str,
                            master: dict[date, dict],
                            eligible_pool_by_phase: dict[str, dict[date, float]],
                            leadup_days: int,
                            min_valid: int,
                            N_std: float,
                            mode: str,  # 'one_sided_elevated' or 'bidirectional'
                            ) -> tuple[float, int, list[dict]]:
    """For each ref date in refs, compute episode profile; return
    fraction triggering at N_std + count of valid episodes + per-ep
    profile list."""
    profiles: list[dict] = []
    for r in refs:
        prof = episode_profile(r, col, master, eligible_pool_by_phase,
                                leadup_days, min_valid)
        if prof is None:
            continue
        profiles.append({"ref": r, **prof})
    if not profiles:
        return (0.0, 0, profiles)

    def trigger(p):
        if mode == "bidirectional":
            return p["max_abs_z"] >= N_std
        return p["max_signed_z"] >= N_std

    n_trig = sum(1 for p in profiles if trigger(p))
    return (n_trig / len(profiles), len(profiles), profiles)


def bootstrap_null_distribution(
        eligible_dates: list[date],
        n_crashes: int,
        col: str,
        master: dict[date, dict],
        eligible_pool_by_phase: dict[str, dict[date, float]],
        leadup_days: int,
        min_valid: int,
        N_std: float,
        mode: str,
        B: int,
        rng: random.Random) -> list[float]:
    """Stationary-bootstrap relabeling of is_crash positions within the
    per-phase eligible pool. For each bootstrap draw b:
      - Sample n_crashes positions via stationary bootstrap on the
        eligible_dates index
      - Treat those dates as 'crashes', compute trigger frequency
      - Append to null distribution
    Returns list of B trigger frequencies under permuted labels."""
    n = len(eligible_dates)
    out: list[float] = []
    for _ in range(B):
        perm_idx = stationary_bootstrap_label_indices(n, n_crashes, rng)
        perm_dates = [eligible_dates[i] for i in perm_idx]
        freq, _, _ = evaluate_trigger_freq(
            perm_dates, col, master, eligible_pool_by_phase,
            leadup_days, min_valid, N_std, mode)
        out.append(freq)
    return out


# === Data-driven E[L]* (§4.9.2) =========================================

def estimate_block_length(values: list[float]) -> float:
    """First-principles ACF-based E[L]* estimator. For each lag k,
    compute autocorrelation; integrated autocorrelation time
    tau = 1 + 2 * sum_{k=1..K} rho_k where K is the smallest lag with
    |rho_k| < 2/sqrt(n). E[L]* = 2 * tau (operational anchor).
    Returns NaN if insufficient data."""
    n = len(values)
    if n < 30:
        return float("nan")
    mean = sum(values) / n
    centered = [v - mean for v in values]
    denom = sum(c * c for c in centered)
    if denom == 0:
        return float("nan")
    rhos = [1.0]
    cutoff = 2.0 / math.sqrt(n)
    for k in range(1, min(40, n // 4)):
        num = sum(centered[i] * centered[i + k] for i in range(n - k))
        rho = num / denom
        rhos.append(rho)
        if abs(rho) < cutoff:
            break
    K = len(rhos) - 1
    tau = 1 + 2 * sum(rhos[1:])
    return max(2 * tau, 1.0)


# === Spearman correlation (manual) ======================================

def spearman_rho(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 3:
        return 0.0

    def rank(vs: list[float]) -> list[float]:
        order = sorted(range(len(vs)), key=lambda i: vs[i])
        ranks = [0.0] * len(vs)
        i = 0
        while i < len(vs):
            j = i
            while j + 1 < len(vs) and vs[order[j + 1]] == vs[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[order[k]] = avg
            i = j + 1
        return ranks
    rx, ry = rank(xs), rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ry[i] - my) ** 2 for i in range(n)))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


# === Build eligible-day pools per phase (for baseline + null) ==========

def build_eligible_pools(slm: dict[date, dict],
                          master: dict[date, dict],
                          quartile_cache: dict[date, list[int]] | None,
                          ) -> dict[str, dict[date, dict[str, float]]]:
    """phase -> date -> {col: predictor_value}. Includes all days that
    pass §4.3 validity (not necessarily §4.2 exertion-conditioning, since
    the baseline pool is wider than the test sample per §4.5)."""
    out: dict[str, dict[date, dict[str, float]]] = {p: {} for p in PHASE_ORDER}
    all_cols = list(set(LADDER_UNIQUE) | {PRIMARY_COL})
    for d in sorted(slm.keys()):
        if d < LC_ERA_START or d > VALIDATE_END:
            continue
        if day_in_april2024_cluster(d):
            continue
        ok, _ = day_basic_valid(d, slm, master)
        if not ok:
            continue
        if quartile_cache:
            ok_q, _ = passes_quartile_gate(d, quartile_cache, master)
            if not ok_q:
                continue
        phase = citalopram_phase(d)
        if phase not in out:
            continue
        rec: dict[str, float] = {}
        for col in all_cols:
            v = get_predictor(d, master, col)
            if v is not None:
                rec[col] = v
        if rec:
            out[phase][d] = rec
    return out


# === Filter the full crash list to phase x era x eligibility ===========

def crash_episodes_by_phase_era(crash_starts: list[date],
                                  slm: dict[date, dict],
                                  master: dict[date, dict],
                                  quartile_cache: dict[date, list[int]] | None,
                                  ) -> dict[str, dict[str, list[date]]]:
    """phase -> era -> list of crash-start dates that are §4.2/§4.3-eligible
    AND not in the buildup buffer."""
    out: dict[str, dict[str, list[date]]] = {
        p: {"train": [], "validate": []} for p in PHASE_ORDER}
    for c in crash_starts:
        if c < ANALYSIS_START or c > VALIDATE_END:
            continue
        phase = citalopram_phase(c)
        if phase not in out:
            continue
        if day_in_buildup_buffer(c):
            continue  # buildup post-CPAP-buffer drops these
        ok, _ = day_eligible(c, slm, master, quartile_cache)
        if not ok:
            continue
        era = "train" if c <= TRAIN_END else "validate"
        out[phase][era].append(c)
    return out


# === Dry-run reporting (§10.1) ==========================================

def dry_run(slm: dict[date, dict],
             master: dict[date, dict],
             crash_starts: list[date],
             use_quartile: bool) -> dict:
    """Sample sizes per phase x era; first-3 episodes; sanity gates."""
    quartile_cache: dict[date, list[int]] = {}
    if use_quartile:
        quartile_cache = load_quartile_cache()
        if not quartile_cache:
            print("[dry-run] quartile cache absent; running 1b.i-only mode",
                  file=sys.stderr)

    pools = build_eligible_pools(slm, master, quartile_cache or None)
    cbpe = crash_episodes_by_phase_era(crash_starts, slm, master,
                                        quartile_cache or None)

    # === Section 1: Eligible-pool sizes per phase (baseline universe) ===
    print("\n=== HA-C4b dry-run ===")
    print(f"\n--- §4.3 eligible-day pool sizes (phase universe, "
          f"{'with 1b.ii' if quartile_cache else '1b.i only'}) ---")
    for phase in PHASE_ORDER:
        days_in_pool = pools[phase]
        n = len(days_in_pool)
        meds = {}
        for col in LADDER_UNIQUE:
            vals = [d_rec.get(col) for d_rec in days_in_pool.values()
                    if d_rec.get(col) is not None]
            meds[col] = statistics.median(vals) if vals else float("nan")
        print(f"  {phase:14}: n_eligible_days={n:4}; "
              f"median {PRIMARY_COL.split('_')[-1]}={meds.get(PRIMARY_COL, 'NA'):>6}")

    # === Section 2: Crash episodes per phase x era ===
    print("\n--- crash episodes per phase x era (after §4.2 + §4.3 + §6) ---")
    print(f"  {'phase':14} {'train':>8} {'validate':>8}")
    summary: dict[str, dict] = {}
    for phase in PHASE_ORDER:
        nt = len(cbpe[phase]["train"])
        nv = len(cbpe[phase]["validate"])
        print(f"  {phase:14} {nt:>8} {nv:>8}")
        summary[phase] = {"train_n_eligible": nt, "validate_n_eligible": nv}

    # === Section 3: first 3 episodes per phase x era with details ===
    print("\n--- first 3 episodes per phase x era (PRIMARY column "
          "lead-up profile) ---")
    fields = LEADUP_SECONDARY  # 5-day for max detail
    for phase in PHASE_ORDER:
        for era in ["train", "validate"]:
            eps = cbpe[phase][era][:3]
            if not eps:
                continue
            print(f"\n  -- {phase} {era} --")
            for ref in eps:
                print(f"    crash starting {ref.isoformat()}:")
                for i in range(1, fields + 1):
                    wd = ref - timedelta(days=i)
                    val = get_predictor(wd, master, PRIMARY_COL)
                    mu, sigma, n_prior = compute_lagged_baseline(
                        wd, PRIMARY_COL, pools)
                    if val is None:
                        z_str = "NA"
                    elif mu is None or sigma is None:
                        z_str = f"baseline-na (n_prior={n_prior})"
                    else:
                        z = (val - mu) / sigma
                        z_str = (f"val={val:.0f} mu={mu:.1f} "
                                 f"sig={sigma:.1f} z={z:+.2f}")
                    print(f"      d-{i} ({wd.isoformat()}): {z_str}")
                prof = episode_profile(
                    ref, PRIMARY_COL, master, pools,
                    LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
                if prof:
                    print(f"      4d primary: leadup_n={prof['leadup_n']} "
                          f"max_signed_z={prof['max_signed_z']:+.3f} "
                          f"max|z|={prof['max_abs_z']:.3f}")
                else:
                    print(f"      4d primary: insufficient (leadup_n < "
                          f"{MIN_LEADUP_VALID_PRIMARY})")

    # === Section 4: median baseline sigma per phase ===
    print("\n--- median baseline sigma per phase (sample of eligible days) "
          "for §7 sanity range [5, 40] ---")
    sigma_medians: dict[str, float] = {}
    for phase in PHASE_ORDER:
        sigmas: list[float] = []
        for d in list(pools[phase].keys())[::max(1, len(pools[phase]) // 50)]:
            mu, sig, _ = compute_lagged_baseline(d, PRIMARY_COL, pools)
            if sig is not None:
                sigmas.append(sig)
        med = statistics.median(sigmas) if sigmas else float("nan")
        sigma_medians[phase] = med
        ok = (SANITY_SIGMA_RANGE[0] <= med <= SANITY_SIGMA_RANGE[1])
        print(f"  {phase:14}: sampled_n={len(sigmas):3}, median_sigma="
              f"{med if not math.isnan(med) else 'NaN':<6} "
              f"{'OK' if ok else 'OUT-OF-RANGE'}")

    # === Section 5: §7 sanity gates ===
    print("\n--- §7 sanity-check gates ---")
    fails: list[str] = []

    # Gate 1: consolidation per-era n >= 10
    nt_c = len(cbpe["consolidation"]["train"])
    nv_c = len(cbpe["consolidation"]["validate"])
    if nt_c < SANITY_MIN_EPISODES_PER_PHASE_ERA:
        fails.append(f"consolidation train n={nt_c} < 10 (§7 / §5.3)")
    if nv_c < SANITY_MIN_EPISODES_PER_PHASE_ERA:
        fails.append(f"consolidation validate n={nv_c} < 10 (§7 / §5.3)")
    if nt_c >= SANITY_MIN_EPISODES_PER_PHASE_ERA and \
       nv_c >= SANITY_MIN_EPISODES_PER_PHASE_ERA:
        print(f"  GATE 1 (consolidation n >= 10): PASS "
              f"(train={nt_c}, validate={nv_c})")
    else:
        print(f"  GATE 1 (consolidation n >= 10): FAIL "
              f"(train={nt_c}, validate={nv_c})")

    # Gate 2: median predictor in expected range per phase
    for phase in PHASE_ORDER:
        days_in_pool = pools[phase]
        vals = [r.get(PRIMARY_COL) for r in days_in_pool.values()
                if r.get(PRIMARY_COL) is not None]
        if not vals:
            print(f"  GATE 2 ({phase}): SKIP (no data)")
            continue
        med = statistics.median(vals)
        lo, hi = EXPECTED_MEDIAN_RANGE[phase]
        ok = lo <= med <= hi
        if not ok and phase in ("consolidation", "unmedicated"):
            fails.append(f"{phase} median primary = {med:.1f} outside "
                         f"[{lo}, {hi}] (§7)")
        print(f"  GATE 2 ({phase}): {'PASS' if ok else 'FAIL'} "
              f"(median={med:.1f}, expected [{lo}, {hi}])")

    # Gate 3: median baseline sigma in [5, 40] per phase
    for phase in PHASE_ORDER:
        med = sigma_medians.get(phase, float("nan"))
        if math.isnan(med):
            print(f"  GATE 3 ({phase}): SKIP (no baselines computable)")
            continue
        ok = SANITY_SIGMA_RANGE[0] <= med <= SANITY_SIGMA_RANGE[1]
        if not ok and phase in ("consolidation", "unmedicated"):
            fails.append(f"{phase} median sigma = {med:.1f} outside "
                         f"{SANITY_SIGMA_RANGE} (§7)")
        print(f"  GATE 3 ({phase}): {'PASS' if ok else 'FAIL'} "
              f"(median_sigma={med:.1f})")

    if fails:
        print(f"\n--- DRY-RUN VERDICT: HALT ({len(fails)} sanity failures) ---")
        for f in fails:
            print(f"  - {f}")
        print(f"\nPer §7 + §9 + §10.4: DO NOT run the full test. "
              f"Spec revision (HA-C4b-v2) required.")
    else:
        print("\n--- DRY-RUN VERDICT: PASS (proceed with `python test.py`) ---")

    return {
        "summary_by_phase": summary,
        "median_predictor": {
            p: (statistics.median([r.get(PRIMARY_COL) for r in pools[p].values()
                                    if r.get(PRIMARY_COL) is not None])
                if pools[p] else None)
            for p in PHASE_ORDER},
        "median_baseline_sigma": sigma_medians,
        "sanity_fails": fails,
        "verdict": "HALT" if fails else "PASS",
        "use_quartile_cache": bool(quartile_cache),
    }


def write_dry_run_report(dry_summary: dict) -> None:
    """Emit dry-run-report.md (only when sanity fails)."""
    lines: list[str] = []
    lines.append("# HA-C4b dry-run report (sanity-gate failure)")
    lines.append("")
    lines.append("Drafted by `test.py --dry-run` per locked hypothesis.md "
                 f"§10.4 protocol. Sanity gates failed; full test NOT run; "
                 f"result.md NOT emitted.")
    lines.append("")
    lines.append(f"Quartile cache used: "
                 f"{'yes (1b.ii applied)' if dry_summary['use_quartile_cache'] else 'no (1b.i only — 1b.ii deferred)'}")
    lines.append("")
    lines.append("## Sanity failures (§7)")
    lines.append("")
    for f in dry_summary["sanity_fails"]:
        lines.append(f"- {f}")
    lines.append("")
    lines.append("## Eligible-crash-episodes per phase x era")
    lines.append("")
    lines.append("| phase | train | validate |")
    lines.append("|---|---:|---:|")
    for p in PHASE_ORDER:
        s = dry_summary["summary_by_phase"][p]
        lines.append(f"| {p} | {s['train_n_eligible']} | "
                     f"{s['validate_n_eligible']} |")
    lines.append("")
    lines.append("## Median primary predictor + median baseline sigma per phase")
    lines.append("")
    lines.append("| phase | median predictor | median baseline sigma |")
    lines.append("|---|---:|---:|")
    for p in PHASE_ORDER:
        med_p = dry_summary["median_predictor"].get(p)
        med_s = dry_summary["median_baseline_sigma"].get(p)
        med_p_s = f"{med_p:.1f}" if med_p is not None else "NA"
        med_s_s = (f"{med_s:.1f}"
                   if med_s is not None and not math.isnan(med_s) else "NA")
        lines.append(f"| {p} | {med_p_s} | {med_s_s} |")
    lines.append("")
    lines.append("## Next step")
    lines.append("")
    lines.append(
        "Per the locked-pre-reg discipline (hypothesis.md §10.4 + §9), "
        "the spec must be revised before any further test run; the "
        "revision creates HA-C4b-v2 with the v1 archived. The next "
        "session opens a v2-draft pre-reg session under "
        "[CONVENTIONS §1.2 reviewer-mode-with-authorization].")
    OUT_DRYRUN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT_DRYRUN_MD}", file=sys.stderr)


# === Full-run pipeline (§10.2) =========================================

def _bootstrap_pct_ci(vals: list[float], lo: float = 0.025,
                       hi: float = 0.975) -> tuple[float, float]:
    if not vals:
        return (float("nan"), float("nan"))
    sv = sorted(vals)
    n = len(sv)
    return (sv[int(lo * n)], sv[min(n - 1, int(hi * n))])


def run_full(slm: dict[date, dict],
              master: dict[date, dict],
              crash_starts: list[date]) -> dict:
    """Full evaluation per the locked spec §5. Builds quartile cache
    first if missing."""
    if not QUARTILE_CACHE.exists():
        print("[full] quartile cache missing -> building (slow, ~5-15 min)",
              file=sys.stderr)
        build_quartile_cache()
    quartile_cache = load_quartile_cache()
    if not quartile_cache:
        print("ERROR: quartile cache empty after build attempt", file=sys.stderr)
        sys.exit(1)
    rng = random.Random(RANDOM_SEED)
    pools = build_eligible_pools(slm, master, quartile_cache)
    cbpe = crash_episodes_by_phase_era(crash_starts, slm, master, quartile_cache)

    # Build per-phase eligible-date lists for the null sample (ordered)
    eligible_dates_by_phase: dict[str, list[date]] = {}
    for phase in PHASE_ORDER:
        eligible_dates_by_phase[phase] = sorted(pools[phase].keys())

    results: dict = {"phases": {}, "headline": {}, "ladder": {},
                     "secondary": {}, "e_l_star": {},
                     "config": {"B_HEADLINE": B_HEADLINE,
                                "B_DIAGNOSTIC": B_DIAGNOSTIC,
                                "BOOTSTRAP_E_L": BOOTSTRAP_E_L,
                                "RANDOM_SEED": RANDOM_SEED}}

    # === Per-phase x per-era x per-tier x per-column x per-window x per-mode
    print("\n=== Evaluating headline cell + sensitivity ladder ===")
    for phase in PHASE_ORDER:
        results["phases"][phase] = {"train": {}, "validate": {}}
        for era in ["train", "validate"]:
            refs = cbpe[phase][era]
            era_eligible = [d for d in eligible_dates_by_phase[phase]
                            if (era == "train" and d <= TRAIN_END)
                            or (era == "validate" and d > TRAIN_END)]
            print(f"\n-- {phase} {era}: n_episodes={len(refs)}, "
                  f"n_eligible_pool={len(era_eligible)} --")
            era_block: dict = {"n_episodes": len(refs),
                                "n_eligible_pool": len(era_eligible)}
            for col in LADDER_UNIQUE:
                col_block: dict = {}
                for N_std in N_STD_TIERS:
                    for window_label, leadup, min_v in [
                        ("4d_primary", LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY),
                        ("5d_secondary", LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY),
                    ]:
                        for mode in ["one_sided_elevated", "bidirectional"]:
                            key = f"{window_label}_Nstd{N_std}_{mode}"
                            B = (B_HEADLINE
                                 if (col == PRIMARY_COL
                                     and N_std == N_STD_PRIMARY
                                     and window_label == "4d_primary"
                                     and mode == "one_sided_elevated"
                                     and phase == HEADLINE_PHASE)
                                 else B_DIAGNOSTIC)
                            obs_freq, n_clean, _profs = evaluate_trigger_freq(
                                refs, col, master, pools, leadup,
                                min_v, N_std, mode)
                            if n_clean < SANITY_MIN_EPISODES_PER_PHASE_ERA:
                                col_block[key] = {
                                    "verdict": "inconclusive",
                                    "n_clean": n_clean,
                                    "B": B,
                                }
                                continue
                            if not era_eligible or not refs:
                                col_block[key] = {"verdict": "inconclusive",
                                                    "n_clean": n_clean, "B": B}
                                continue
                            null_freqs = bootstrap_null_distribution(
                                era_eligible, len(refs), col, master, pools,
                                leadup, min_v, N_std, mode, B, rng)
                            null_med = statistics.median(null_freqs) if null_freqs else 0.0
                            p_val = (sum(1 for f in null_freqs if f >= obs_freq)
                                     / max(1, len(null_freqs)))
                            disc_pp = (obs_freq - null_med) * 100
                            # criterion (c) median magnitude
                            mags = []
                            for r in refs:
                                prof = episode_profile(
                                    r, col, master, pools, leadup, min_v)
                                if prof:
                                    if mode == "bidirectional":
                                        mags.append(prof["max_abs_z"])
                                    else:
                                        mags.append(prof["max_signed_z"])
                            med_mag = statistics.median(mags) if mags else 0.0
                            crit_a = obs_freq >= CRIT_A_FRAC
                            crit_b = disc_pp >= CRIT_B_DISC_PP
                            crit_c = med_mag >= N_std / 2
                            verdict = ("supported"
                                       if (crit_a and crit_b and crit_c)
                                       else "refuted")
                            # RD + OR with bootstrap-percentile CIs
                            rd = obs_freq - null_med
                            rd_distrib = [obs_freq - f for f in null_freqs]
                            rd_lo, rd_hi = _bootstrap_pct_ci(rd_distrib)
                            # OR with epsilon guard against 0/1
                            def _or(p_c, p_n):
                                eps = 1e-6
                                p_c = min(max(p_c, eps), 1 - eps)
                                p_n = min(max(p_n, eps), 1 - eps)
                                return ((p_c / (1 - p_c))
                                        / (p_n / (1 - p_n)))
                            or_pt = _or(obs_freq, null_med)
                            or_distrib = [_or(obs_freq, f) for f in null_freqs]
                            or_lo, or_hi = _bootstrap_pct_ci(or_distrib)
                            col_block[key] = {
                                "verdict": verdict,
                                "n_clean": n_clean,
                                "obs_freq": obs_freq,
                                "null_median_freq": null_med,
                                "disc_pp": disc_pp,
                                "p_value": p_val,
                                "median_magnitude": med_mag,
                                "crit_a_pass": crit_a,
                                "crit_b_pass": crit_b,
                                "crit_c_pass": crit_c,
                                "rd_point": rd,
                                "rd_ci": [rd_lo, rd_hi],
                                "or_point": or_pt,
                                "or_ci": [or_lo, or_hi],
                                "B": B,
                            }
                            if (col == PRIMARY_COL
                                    and N_std == N_STD_PRIMARY
                                    and window_label == "4d_primary"
                                    and mode == "one_sided_elevated"
                                    and phase == HEADLINE_PHASE):
                                print(f"   HEADLINE {era}: {verdict} "
                                      f"(obs={obs_freq*100:.1f}%, null="
                                      f"{null_med*100:.1f}%, disc="
                                      f"{disc_pp:+.1f}pp, p={p_val:.4f}, "
                                      f"OR={or_pt:.2f} [{or_lo:.2f},"
                                      f"{or_hi:.2f}])")
                era_block[col] = col_block
            results["phases"][phase][era] = era_block

    # === E[L]* on consolidation eligible pool ===
    print("\n=== Data-driven E[L]* on consolidation primary column ===")
    consol_dates = sorted(pools["consolidation"].keys())
    consol_vals = [pools["consolidation"][d][PRIMARY_COL]
                   for d in consol_dates if PRIMARY_COL in pools["consolidation"][d]]
    el_star = estimate_block_length(consol_vals)
    flag = abs(el_star - BOOTSTRAP_E_L) / BOOTSTRAP_E_L > 0.5 \
        if not math.isnan(el_star) else False
    print(f"  E[L]* = {el_star:.2f} (default = {BOOTSTRAP_E_L})  "
          f"{'FLAG (outside [3.5, 10.5])' if flag else 'within tolerance'}")
    results["e_l_star"] = {"value": el_star, "default": BOOTSTRAP_E_L,
                            "flag_outside_tolerance": flag}

    # === Construct-disambiguation (§4.11.2 + .3) + respiration (§4.11.4) ===
    print("\n=== §4.11 secondary descriptive outcomes ===")
    descriptive: dict = {}
    # Same-day Spearman per phase x era + crash-drop sensitivity
    for phase in PHASE_ORDER:
        for era in ["train", "validate"]:
            d_pool = [d for d in pools[phase]
                      if (era == "train" and d <= TRAIN_END)
                      or (era == "validate" and d > TRAIN_END)]
            xs: list[float] = []
            ys: list[float] = []
            xs_nc: list[float] = []
            ys_nc: list[float] = []
            for d in d_pool:
                v = pools[phase][d].get(PRIMARY_COL)
                g = master.get(d, {}).get("gevoelscore", "")
                if v is None or not g:
                    continue
                try:
                    gf = float(g)
                except ValueError:
                    continue
                xs.append(v)
                ys.append(gf)
                if master[d].get("is_crash") != "True":
                    xs_nc.append(v)
                    ys_nc.append(gf)
            rho_full = spearman_rho(xs, ys) if len(xs) >= 3 else float("nan")
            rho_nc = spearman_rho(xs_nc, ys_nc) if len(xs_nc) >= 3 else float("nan")
            descriptive.setdefault("spearman_primary_vs_gevoelscore",
                                    {}).setdefault(phase, {})[era] = {
                "n_full": len(xs), "rho_full": rho_full,
                "n_no_crash": len(xs_nc), "rho_no_crash": rho_nc,
                "delta_rho": (rho_full - rho_nc)
                if not math.isnan(rho_full) and not math.isnan(rho_nc)
                else float("nan"),
            }
    # Construct disambiguation 2x2 against stress_high_duration_min + u_dip_count
    for sibling, label in [(SIBLING_PRIMARY, "stress_high_duration_min"),
                            (SIBLING_SECONDARY, "u_dip_count")]:
        sibling_block: dict = {}
        for phase in PHASE_ORDER:
            for era in ["train", "validate"]:
                refs = cbpe[phase][era]
                if not refs:
                    continue
                tt = tf = ft = ff = 0
                for r in refs:
                    prof_p = episode_profile(
                        r, PRIMARY_COL, master, pools,
                        LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
                    prof_s = episode_profile(
                        r, sibling, master, pools,
                        LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
                    if prof_p is None or prof_s is None:
                        continue
                    p_fires = prof_p["max_signed_z"] >= N_STD_PRIMARY
                    s_fires = prof_s["max_signed_z"] >= N_STD_PRIMARY
                    if p_fires and s_fires:
                        tt += 1
                    elif p_fires and not s_fires:
                        tf += 1
                    elif not p_fires and s_fires:
                        ft += 1
                    else:
                        ff += 1
                sibling_block.setdefault(phase, {})[era] = {
                    "both_fire": tt, "primary_only": tf,
                    "sibling_only": ft, "neither": ff,
                    "n_evaluated": tt + tf + ft + ff,
                }
        descriptive[f"construct_disambig_vs_{label}"] = sibling_block

    # Respiration-companion sensitivity (§4.11.4)
    resp_block: dict = {}
    for phase in PHASE_ORDER:
        for era in ["train", "validate"]:
            refs = cbpe[phase][era]
            if not refs:
                continue
            primary_fired_resp_elev = 0
            primary_fired_resp_norm = 0
            for r in refs:
                prof_p = episode_profile(
                    r, PRIMARY_COL, master, pools,
                    LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
                if prof_p is None or prof_p["max_signed_z"] < N_STD_PRIMARY:
                    continue
                prof_r = episode_profile(
                    r, RESP_COL, master, pools,
                    LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY)
                if prof_r is None:
                    continue
                if prof_r["max_signed_z"] > 0:
                    primary_fired_resp_elev += 1
                else:
                    primary_fired_resp_norm += 1
            resp_block.setdefault(phase, {})[era] = {
                "primary_fired_resp_elevated": primary_fired_resp_elev,
                "primary_fired_resp_not_elevated": primary_fired_resp_norm,
            }
    descriptive["respiration_companion_sensitivity"] = resp_block
    results["secondary"] = descriptive

    return results


def write_result_md(results: dict, master: dict, pools: dict,
                     cbpe: dict) -> None:
    """Emit result.md per §10.3."""
    H = results["phases"].get(HEADLINE_PHASE, {})
    head_t = (H.get("train", {}).get(PRIMARY_COL, {})
              .get(f"4d_primary_Nstd{N_STD_PRIMARY}_one_sided_elevated", {}))
    head_v = (H.get("validate", {}).get(PRIMARY_COL, {})
              .get(f"4d_primary_Nstd{N_STD_PRIMARY}_one_sided_elevated", {}))

    def vstr(b: dict) -> str:
        if not b or b.get("verdict") == "inconclusive":
            return "INCONCLUSIVE"
        return b.get("verdict", "?").upper()

    overall = "INCONCLUSIVE"
    tv, vv = vstr(head_t), vstr(head_v)
    if tv == "SUPPORTED" and vv == "SUPPORTED":
        overall = "SUPPORTED (both eras)"
    elif tv == "REFUTED" or vv == "REFUTED":
        overall = "REFUTED (per locked single-cell rule)"
    elif tv == "INCONCLUSIVE" or vv == "INCONCLUSIVE":
        overall = "INCONCLUSIVE"

    lines: list[str] = []
    lines.append("# HA-C4b — Result: stress-low-motion count z-score "
                 "as crash precursor")
    lines.append("")
    lines.append(f"**Headline verdict (consolidation × `S60_Mlow` × "
                 f"N_std=1.5 × primary 4d × one-sided elevated): "
                 f"train {tv} ; validate {vv} → overall {overall}**")
    lines.append("")
    lines.append(
        "Per the locked single-cell discipline (hypothesis.md §5.0), the "
        "headline is decided by this ONE cell only; all other cells "
        "(other phases, tiers, columns, windows, directions) are "
        "diagnostic / sensitivity arms and cannot promote.")
    lines.append("")
    lines.append(f"Data: [result-data.json]({OUT_DATA_JSON.name}).")
    lines.append("")
    lines.append("## Headline numbers (primary 4d, N_std=1.5, one-sided "
                 "elevated; consolidation phase)")
    lines.append("")
    if head_t and head_v:
        lines.append("| | train | validate |")
        lines.append("|---|---:|---:|")
        for label, key in [
            ("episodes (clean)", "n_clean"),
            ("frac event (a)", "obs_freq"),
            ("null median freq", "null_median_freq"),
            ("discrimination pp (b)", "disc_pp"),
            ("p-value (block-permutation E[L]=7)", "p_value"),
            ("median magnitude (c)", "median_magnitude"),
            ("RD (point)", "rd_point"),
            ("RD 95% CI", "rd_ci"),
            ("OR (point)", "or_point"),
            ("OR 95% CI", "or_ci"),
            ("crit (a) freq ≥ 60%", "crit_a_pass"),
            ("crit (b) disc ≥ +15pp", "crit_b_pass"),
            ("crit (c) med ≥ 0.75", "crit_c_pass"),
            ("verdict", "verdict"),
        ]:
            tv_, vv_ = head_t.get(key), head_v.get(key)
            def fmt(v):
                if isinstance(v, bool):
                    return "PASS" if v else "FAIL"
                if isinstance(v, list) and len(v) == 2:
                    return f"[{v[0]:+.3f}, {v[1]:+.3f}]"
                if isinstance(v, float):
                    if abs(v) < 10 and key != "p_value":
                        return f"{v:+.3f}"
                    return f"{v:.4f}" if key == "p_value" else f"{v:.1f}"
                return str(v) if v is not None else "—"
            lines.append(f"| {label} | {fmt(tv_)} | {fmt(vv_)} |")
    else:
        lines.append("(headline cell inconclusive — see §5.3)")
    lines.append("")
    lines.append("## E[L]* data-driven block length (consolidation pool)")
    lines.append("")
    el = results["e_l_star"]
    lines.append(f"- E[L]* = {el['value']:.2f}; default E[L] = {el['default']}; "
                 f"flag-outside-tolerance ([3.5, 10.5]): "
                 f"{'YES' if el['flag_outside_tolerance'] else 'no'}")
    lines.append("")
    if el["flag_outside_tolerance"]:
        lines.append("**WARNING**: E[L]* deviates from default by > factor of "
                     "2; per §4.9.2 the headline verdict requires re-evaluation "
                     "at E[L]* before locking.")
        lines.append("")
    lines.append("## All combinations (sensitivity ladder × tiers × windows × modes × phases × eras)")
    lines.append("")
    lines.append("Only the 6 unique columns appear; the 3 `Mbelow_mod` columns are "
                 "identical-by-construction to the corresponding `Mlow` columns in v1 "
                 "(per §4.10 + stress_low_motion_primitive §3.2) and emitted to "
                 "result-data.json but not tabulated here.")
    lines.append("")
    lines.append("| phase | era | col | N_std | window | mode | verdict | "
                 "n_clean | obs_freq | null_med | disc_pp | med_mag | p_val |")
    lines.append("|---|---|---|---:|---|---|---|---:|---:|---:|---:|---:|---:|")
    for phase in PHASE_ORDER:
        for era in ["train", "validate"]:
            blk = results["phases"].get(phase, {}).get(era, {})
            for col in LADDER_UNIQUE:
                col_blk = blk.get(col, {})
                for key, payload in col_blk.items():
                    if not isinstance(payload, dict):
                        continue
                    v = payload.get("verdict", "?")
                    if v == "inconclusive":
                        n = payload.get("n_clean", 0)
                        lines.append(
                            f"| {phase} | {era} | "
                            f"{col.replace('stress_low_motion_min_count_', '')} | "
                            f" | | | {v} | {n} | — | — | — | — | — |")
                        continue
                    parts = key.split("_")
                    # 4d_primary_Nstd1.5_one_sided_elevated
                    if "Nstd" in key:
                        win = parts[0] + "_" + parts[1]
                        nstd = next(p for p in parts if p.startswith("Nstd"))[4:]
                        mode = "_".join(parts[parts.index("Nstd" + nstd) + 1:])
                    else:
                        win = parts[0]
                        nstd = parts[2][4:]
                        mode = parts[3]
                    lines.append(
                        f"| {phase} | {era} | "
                        f"{col.replace('stress_low_motion_min_count_', '')} | "
                        f"{nstd} | {win} | {mode} | {v} | "
                        f"{payload.get('n_clean', 0)} | "
                        f"{payload.get('obs_freq', 0)*100:.1f}% | "
                        f"{payload.get('null_median_freq', 0)*100:.1f}% | "
                        f"{payload.get('disc_pp', 0):+.1f} | "
                        f"{payload.get('median_magnitude', 0):.2f} | "
                        f"{payload.get('p_value', 1):.4f} |")
    lines.append("")
    lines.append("## §4.11 secondary descriptive outcomes")
    lines.append("")
    lines.append("### Same-day Spearman (primary col vs gevoelscore) + "
                 "§3.4 crash-drop row")
    lines.append("")
    sp = results["secondary"].get("spearman_primary_vs_gevoelscore", {})
    lines.append("| phase | era | n_full | rho_full | n_no_crash | rho_no_crash | |Δρ| |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for phase in PHASE_ORDER:
        for era in ["train", "validate"]:
            rec = sp.get(phase, {}).get(era)
            if not rec:
                continue
            d_rho = rec.get("delta_rho", float("nan"))
            flag = "**FLAG**" if not math.isnan(d_rho) and abs(d_rho) > 0.10 else ""
            lines.append(
                f"| {phase} | {era} | {rec['n_full']} | "
                f"{rec['rho_full']:+.3f} | {rec['n_no_crash']} | "
                f"{rec['rho_no_crash']:+.3f} | "
                f"{abs(d_rho):.3f}{' ' + flag if flag else ''} |")
    lines.append("")
    lines.append("### Construct-disambiguation 2x2 (HA-C4b primary vs sibling)")
    lines.append("")
    for sibling_label in [f"construct_disambig_vs_stress_high_duration_min",
                          f"construct_disambig_vs_u_dip_count"]:
        sb = results["secondary"].get(sibling_label, {})
        if not sb:
            continue
        title = sibling_label.replace("construct_disambig_vs_", "")
        lines.append(f"**vs `{title}`** (rho = "
                     f"{'0.79' if 'stress_high' in title else '0.556'}; "
                     f"both eras pooled per phase):")
        lines.append("")
        lines.append("| phase | era | both_fire | primary_only "
                     "(HA-C4b-only) | sibling_only | neither | n_eval |")
        lines.append("|---|---|---:|---:|---:|---:|---:|")
        for phase in PHASE_ORDER:
            for era in ["train", "validate"]:
                rec = sb.get(phase, {}).get(era)
                if not rec:
                    continue
                lines.append(
                    f"| {phase} | {era} | {rec['both_fire']} | "
                    f"{rec['primary_only']} | {rec['sibling_only']} | "
                    f"{rec['neither']} | {rec['n_evaluated']} |")
        lines.append("")
    lines.append("### Respiration-companion sensitivity (§4.11.4)")
    lines.append("")
    lines.append("Among crash episodes where HA-C4b primary fires, "
                 "did `n_minutes_resp_above_18` also show z > 0 in the lead-up?")
    lines.append("")
    rb = results["secondary"].get("respiration_companion_sensitivity", {})
    lines.append("| phase | era | primary_fired_resp_elev | "
                 "primary_fired_resp_normal |")
    lines.append("|---|---|---:|---:|")
    for phase in PHASE_ORDER:
        for era in ["train", "validate"]:
            rec = rb.get(phase, {}).get(era)
            if not rec:
                continue
            lines.append(
                f"| {phase} | {era} | "
                f"{rec['primary_fired_resp_elevated']} | "
                f"{rec['primary_fired_resp_not_elevated']} |")
    lines.append("")
    lines.append("## Caveats (§8 acknowledged)")
    lines.append("")
    for c in [
        "Garmin stress is partly motion-sensitive; the motion filter and the "
        "respiration-companion sensitivity are the within-test checks.",
        "Garmin `intensity` classification has an 81% gap; minutes without an "
        "explicit intensity record default to 'low motion' (generous).",
        "Citalopram dose-modulates the underlying stress channel; per-phase "
        "treatment is the dose-confound control; raw count magnitudes are not "
        "directly comparable across phases.",
        "The `below_moderate` motion class is identical-by-construction to "
        "`low_or_below` in v1; the 9-column ladder effectively reduces to 6.",
        "Exertion-conditioning shrinks n; per-phase verdicts may be inconclusive on "
        "low-n phases (buildup, afbouw).",
        "Construct ρ vs `stress_high_duration_min` = 0.79 — close sibling; "
        "the construct-disambiguation 2x2 is the empirical test of whether the "
        "motion filter does analytical work.",
        "The participant is operationally using the rest-stress trigger; the "
        "protocol disturbs the test.",
        "`crash_v2` mixes mechanisms; multi-mechanism crash population dilutes "
        "any one-mechanism precursor signal.",
        "Multi-comparison: the held-out validate window is the primary defence.",
        "The bootstrap RD/OR CIs are computed against the stationary-bootstrap "
        "null distribution (varying p_null with fixed observed p_crash); this "
        "captures null-side variability only. A fuller joint-bootstrap CI would "
        "require resampling crash episodes as well; deferred.",
    ]:
        lines.append(f"- {c}")
    lines.append("")
    OUT_RESULT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_RESULT_MD}", file=sys.stderr)


# === Main ===============================================================

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Sample-size + sanity-check gate per §10.4 step 1.")
    parser.add_argument("--use-quartile-cache", action="store_true",
                        help="In dry-run, also apply 1b.ii (slower if cache missing).")
    args = parser.parse_args()

    print("Loading per_day_master.csv ...", file=sys.stderr)
    master = load_master()
    print(f"  {len(master)} days", file=sys.stderr)

    print("Loading stress_low_motion_minutes.csv ...", file=sys.stderr)
    slm = load_slm_valid()
    print(f"  {len(slm)} days, "
          f"{sum(1 for v in slm.values() if v['valid_ha11'])} HA11-valid, "
          f"{sum(1 for v in slm.values() if v['sample_count'] >= MIN_SAMPLES_C4B)} "
          f"HA-C4b-1b.i-valid", file=sys.stderr)

    crash_starts = load_crash_starts()
    print(f"  {len(crash_starts)} crash_v2 episodes", file=sys.stderr)

    if args.dry_run:
        dry_summary = dry_run(slm, master, crash_starts,
                              use_quartile=args.use_quartile_cache)
        if dry_summary["verdict"] == "HALT":
            write_dry_run_report(dry_summary)
            return 1
        return 0

    # Full run: gate on dry-run sanity first
    dry_summary = dry_run(slm, master, crash_starts, use_quartile=False)
    if dry_summary["verdict"] == "HALT":
        print("\n[full] aborting: dry-run sanity gates failed",
              file=sys.stderr)
        write_dry_run_report(dry_summary)
        return 1

    results = run_full(slm, master, crash_starts)
    OUT_DATA_JSON.write_text(json.dumps(results, indent=2, default=str),
                             encoding="utf-8")
    print(f"Wrote {OUT_DATA_JSON}", file=sys.stderr)
    quartile_cache = load_quartile_cache()
    pools = build_eligible_pools(slm, master, quartile_cache)
    cbpe = crash_episodes_by_phase_era(crash_starts, slm, master, quartile_cache)
    write_result_md(results, master, pools, cbpe)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
