"""HA-C4b v2 - Stage 2: stress-low-motion z-score precursor test.

Implements the locked HA-C4b v2 pre-registration (hypothesis.md
LOCKED 2026-06-16 commit 2417043). Replaces v1 (test-v1-archived.py).

v2 headline cell:
  unmedicated phase x train+validate pooled x S60_Mlow x N_std=1.5
  x primary 4d lead-up x one-sided elevated.

v2 deltas from v1 (test-v1-archived.py):
  - Headline retargeted from consolidation x both-eras-independent
    to unmedicated x pooled (n=10).
  - §10.2 spec-sanity-gate replaces v1 §7: pooled-unmedicated n>=10;
    per-phase median primary within +-20% of v2 §7 raw-card values
    (unmedicated 76, buildup 35, consolidation 38, afbouw 63);
    unmedicated median lagged-baseline sigma in [25, 55].
  - §4.11.5 episode-level leave-one-out fragility check.
  - RD/OR + 95% CI applied to the v2 headline only (v1 mechanics
    inherited verbatim).
  - Result.md layout: single headline block + train-only / validate-
    only descriptive companions + LOO range + companion phases.

Modes:
  python test.py --dry-run    sample sizes per phase x era + the
                              §10.2 v2 spec-sanity-gate. If sanity
                              fails -> halt + write dry-run-report.md
                              + recommend v3 per hypothesis_lock_
                              process.md §3.9.
  python test.py              full evaluation (gates on dry-run
                              sanity first; emits result.md +
                              result-data.json directly).

The wake-window quartile coverage gate (§4.3 1b.ii) uses a per-date
30-min UTC sample-count cache. The dry-run defaults to 1b.i-only;
--use-quartile-cache enables 1b.ii at dry-run. The full run requires
the cache (builds it from the FIT corpus on first run, ~5-15 min).
"""
from __future__ import annotations

import argparse
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
from datetime import date, datetime, time, timedelta
from pathlib import Path

# === Constants per locked hypothesis.md v2 §4-§5 + §7 + §10.2 ============

ANALYSIS_START = date(2022, 9, 3)
TRAIN_END = date(2023, 12, 31)
VALIDATE_END = date(2026, 6, 5)
LC_ERA_START = date(2022, 4, 4)

# §4.3 day-validity gates
MIN_SAMPLES_HA11 = 600
MIN_SAMPLES_C4B = 900
MIN_QUARTILE_SAMPLES = 50

# §4.5 lagged baseline
LAGGED_END_DAYS = 30
LAGGED_START_DAYS = 90
MIN_BASELINE_DAYS = 40
TRIMMED_PCT = 0.10
MIN_BASELINE_STD = 5.0

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

# §5 (a)+(b)+(c) bar
CRIT_A_FRAC = 0.60
CRIT_B_DISC_PP = 15.0

# §6
BUILDUP_BUFFER_END = date(2024, 4, 30)
APRIL2024_CLUSTER_START = date(2024, 4, 9)
APRIL2024_CLUSTER_END_INCL = date(2024, 4, 16)


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
HEADLINE_PHASE = "unmedicated"  # v2 relock

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
    "stress_low_motion_min_count_S50_Mbelow_mod",
    "stress_low_motion_min_count_S60_Mbelow_mod",
    "stress_low_motion_min_count_S75_Mbelow_mod",
]

# §4.11 construct-disambiguation siblings
SIBLING_PRIMARY = "stress_high_duration_min"
SIBLING_SECONDARY = "u_dip_count"
RESP_COL = "n_minutes_resp_above_18"

# §4.2 heavy-exertion classes
HEAVY_CLASSES = {"heavy", "very_heavy"}

# §7 v2 raw-card per-phase median anchors (per `per_phase_card.md`;
# raw column, NO §4.3 eligibility restriction)
V2_RAW_CARD_MEDIAN = {
    "unmedicated": 76.0,
    "buildup": 35.0,
    "consolidation": 38.0,
    "afbouw": 63.0,
}
V2_RAW_CARD_TOL = 0.20  # +/- 20% hard gate

# §7 v2 lagged-baseline sigma range (unmedicated only)
V2_UNMED_SIGMA_RANGE = (25.0, 55.0)

# §10.2 v2 spec-sanity-gate
V2_HEADLINE_N_MIN = 10

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

QUARTILE_SLOT_COLS = [f"slot_{i:02d}" for i in range(48)]


def build_quartile_cache() -> None:
    try:
        import fitdecode  # noqa: F401
    except ImportError:
        print("ERROR: fitdecode not installed; cannot build quartile cache.",
              file=sys.stderr)
        sys.exit(1)
    import fitdecode

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

    slots_by_date: dict[date, list[int]] = collections.defaultdict(
        lambda: [0] * 48)
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


FIXED_QUARTILES_UTC_SLOTS = [
    list(range(8, 20)),
    list(range(20, 32)),
    list(range(32, 40)),
    list(range(40, 48)),
]


def _sum_slots_in_range(cache: dict[date, list[int]],
                         d: date,
                         lo: datetime, hi: datetime) -> int:
    total = 0
    for day_offset in (0, 1):
        dd = d + timedelta(days=day_offset)
        slots = cache.get(dd)
        if slots is None:
            continue
        for slot_i in range(48):
            slot_lo = datetime.combine(dd, time()) + timedelta(minutes=slot_i * 30)
            slot_hi = slot_lo + timedelta(minutes=30)
            lo_n = lo.replace(tzinfo=None) if lo.tzinfo else lo
            hi_n = hi.replace(tzinfo=None) if hi.tzinfo else hi
            if slot_hi <= lo_n or slot_lo >= hi_n:
                continue
            overlap_min = (min(slot_hi, hi_n) - max(slot_lo, lo_n)).total_seconds() / 60
            if overlap_min >= 5:
                total += slots[slot_i]
    return total


def passes_quartile_gate(d: date,
                          quartile_cache: dict[date, list[int]],
                          master: dict[date, dict]) -> tuple[bool, str]:
    slots = quartile_cache.get(d)
    if slots is None:
        return (False, "no-cache")
    row = master.get(d, {})
    s_end = parse_iso_dt(row.get("sleep_end_gmt"))
    s_next = parse_iso_dt(master.get(d + timedelta(days=1), {}).get("sleep_start_gmt"))
    if s_end and s_next and s_next > s_end:
        total = (s_next - s_end).total_seconds()
        if total >= 4 * 3600:
            q_dur = total / 4
            samples_per_q = [0, 0, 0, 0]
            for q_i in range(4):
                q_lo = s_end + timedelta(seconds=q_i * q_dur)
                q_hi = s_end + timedelta(seconds=(q_i + 1) * q_dur)
                samples_per_q[q_i] = _sum_slots_in_range(
                    quartile_cache, d, q_lo, q_hi)
            ok = all(s >= MIN_QUARTILE_SAMPLES for s in samples_per_q)
            return (ok, "sleep")
    samples_per_q = [
        sum(slots[i] for i in q_slots)
        for q_slots in FIXED_QUARTILES_UTC_SLOTS
    ]
    ok = all(s >= MIN_QUARTILE_SAMPLES for s in samples_per_q)
    return (ok, "fixed")


# === Validity & eligibility =============================================

def day_basic_valid(d: date,
                     slm: dict[date, dict],
                     master: dict[date, dict],
                     enforce_900: bool = True) -> tuple[bool, str]:
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
    today = (master.get(d) or {}).get("exertion_class_lagged_lcera", "").strip()
    yest = (master.get(d - timedelta(days=1)) or {}).get(
        "exertion_class_lagged_lcera", "").strip()
    if not today and not yest:
        return (False, "no-exertion-data-on-d-or-d-1")
    if today in HEAVY_CLASSES or yest in HEAVY_CLASSES:
        return (True, "")
    return (False, "not-heavy-on-d-or-d-1")


def day_in_buildup_buffer(d: date) -> bool:
    return APRIL2024_CLUSTER_START <= d < BUILDUP_BUFFER_END


def day_in_april2024_cluster(d: date) -> bool:
    return APRIL2024_CLUSTER_START <= d <= APRIL2024_CLUSTER_END_INCL


def day_eligible(d: date,
                  slm: dict[date, dict],
                  master: dict[date, dict],
                  quartile_cache: dict[date, list[int]] | None) -> tuple[bool, str]:
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
                       eligible_pool_by_phase: dict[str, dict[date, dict[str, float]]],
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
                      eligible_pool_by_phase: dict[str, dict[date, dict[str, float]]],
                      leadup_days: int,
                      min_valid: int) -> dict | None:
    signed: list[float] = []
    per_day: list[dict] = []
    for i in range(1, leadup_days + 1):
        wd = ref - timedelta(days=i)
        val = get_predictor(wd, master, col)
        mu, sigma, _ = compute_lagged_baseline(wd, col, eligible_pool_by_phase)
        if val is None or mu is None or sigma is None:
            per_day.append({"d": wd, "z": None})
            continue
        z = (val - mu) / sigma
        signed.append(z)
        per_day.append({"d": wd, "z": z, "val": val, "mu": mu, "sigma": sigma})
    if len(signed) < min_valid:
        return None
    return {
        "leadup_n": len(signed),
        "all_signed_zs": signed,
        "max_signed_z": max(signed),
        "min_signed_z": min(signed),
        "max_abs_z": max(abs(z) for z in signed),
        "per_day": per_day,
    }


# === Stationary-bootstrap null (§4.9) ===================================

def stationary_bootstrap_label_indices(n: int,
                                        n_crashes: int,
                                        rng: random.Random) -> list[int]:
    """Geometric-block stationary bootstrap: draw blocks of length
    ~Geometric(1/E[L]), concatenate (wrapping) until length >= n,
    return the first n_crashes positions as the permuted crash labels."""
    idx: list[int] = []
    p = 1.0 / BOOTSTRAP_E_L
    while len(idx) < n:
        start = rng.randrange(n)
        L = 1
        while rng.random() >= p:
            L += 1
        for j in range(L):
            idx.append((start + j) % n)
            if len(idx) >= n:
                break
    return idx[:n_crashes]


def evaluate_trigger_freq(refs: list[date],
                            col: str,
                            master: dict[date, dict],
                            eligible_pool_by_phase: dict[str, dict[date, dict[str, float]]],
                            leadup_days: int,
                            min_valid: int,
                            N_std: float,
                            mode: str,
                            ) -> tuple[float, int, list[dict]]:
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
        eligible_pool_by_phase: dict[str, dict[date, dict[str, float]]],
        leadup_days: int,
        min_valid: int,
        N_std: float,
        mode: str,
        B: int,
        rng: random.Random) -> list[float]:
    n = len(eligible_dates)
    if n == 0:
        return []
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
    tau = 1 + 2 * sum(rhos[1:])
    return max(2 * tau, 1.0)


# === Spearman correlation (manual) ======================================

def spearman_rho(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 3:
        return float("nan")

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
        return float("nan")
    return num / (dx * dy)


# === Build eligible-day pools per phase =================================

def build_eligible_pools(slm: dict[date, dict],
                          master: dict[date, dict],
                          quartile_cache: dict[date, list[int]] | None,
                          ) -> dict[str, dict[date, dict[str, float]]]:
    """phase -> date -> {col: predictor_value} for §4.3-valid days.
    No §4.2 exertion-conditioning here; the baseline pool is wider than
    the test sample per §4.5."""
    out: dict[str, dict[date, dict[str, float]]] = {p: {} for p in PHASE_ORDER}
    all_cols = list(set(LADDER_UNIQUE) | {PRIMARY_COL, SIBLING_PRIMARY,
                                            SIBLING_SECONDARY, RESP_COL})
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


# === Filter the full crash list to phase x era x eligibility ============

def crash_episodes_by_phase_era(crash_starts: list[date],
                                  slm: dict[date, dict],
                                  master: dict[date, dict],
                                  quartile_cache: dict[date, list[int]] | None,
                                  ) -> dict[str, dict[str, list[date]]]:
    out: dict[str, dict[str, list[date]]] = {
        p: {"train": [], "validate": []} for p in PHASE_ORDER}
    for c in crash_starts:
        if c < ANALYSIS_START or c > VALIDATE_END:
            continue
        phase = citalopram_phase(c)
        if phase not in out:
            continue
        if day_in_buildup_buffer(c):
            continue
        ok, _ = day_eligible(c, slm, master, quartile_cache)
        if not ok:
            continue
        era = "train" if c <= TRAIN_END else "validate"
        out[phase][era].append(c)
    return out


# === Raw per-phase median (no §4.3 eligibility filter) — v2 §7 anchor ==

def raw_per_phase_median_primary(master: dict[date, dict]) -> dict[str, float]:
    """Median PRIMARY_COL per phase across ALL LC-era days that have a
    value, with NO §4.3 eligibility filter. Matches v2 §7 raw-card."""
    vals_by_phase: dict[str, list[float]] = {p: [] for p in PHASE_ORDER}
    for d, row in master.items():
        if d < LC_ERA_START or d > VALIDATE_END:
            continue
        if day_in_april2024_cluster(d):
            continue
        phase = citalopram_phase(d)
        if phase not in vals_by_phase:
            continue
        v = get_predictor(d, master, PRIMARY_COL)
        if v is not None:
            vals_by_phase[phase].append(v)
    return {
        p: (statistics.median(vs) if vs else float("nan"))
        for p, vs in vals_by_phase.items()
    }


# === Dry-run (§10.4 step 1; §10.2 v2 spec-sanity-gate) ==================

def dry_run(slm: dict[date, dict],
             master: dict[date, dict],
             crash_starts: list[date],
             use_quartile: bool) -> dict:
    quartile_cache: dict[date, list[int]] = {}
    if use_quartile:
        quartile_cache = load_quartile_cache()
        if not quartile_cache:
            print("[dry-run] quartile cache absent; running 1b.i-only mode",
                  file=sys.stderr)

    pools = build_eligible_pools(slm, master, quartile_cache or None)
    cbpe = crash_episodes_by_phase_era(crash_starts, slm, master,
                                        quartile_cache or None)

    print("\n=== HA-C4b v2 dry-run ===")
    print("(v2 headline: unmedicated phase x train+validate POOLED "
          "x S60_Mlow x N_std=1.5 x primary 4d x one-sided elevated)")
    print(f"(quartile-cache 1b.ii: "
          f"{'applied' if quartile_cache else 'deferred (1b.i only)'})")

    # === Section 1: Eligible-pool sizes per phase (baseline universe) ===
    print(f"\n--- §4.3 eligible-day pool sizes (phase universe) ---")
    for phase in PHASE_ORDER:
        n = len(pools[phase])
        vals = [r.get(PRIMARY_COL) for r in pools[phase].values()
                if r.get(PRIMARY_COL) is not None]
        med = statistics.median(vals) if vals else float("nan")
        print(f"  {phase:14}: n_eligible_days={n:4}; "
              f"median_S60_Mlow_§4.3-eligible={med:>6.1f}")

    # === Section 2: Crash episodes per phase x era ===
    print("\n--- crash episodes per phase x era (after §4.2 + §4.3 + §6) ---")
    print(f"  {'phase':14} {'train':>8} {'validate':>8} {'pooled':>8}")
    summary: dict[str, dict] = {}
    for phase in PHASE_ORDER:
        nt = len(cbpe[phase]["train"])
        nv = len(cbpe[phase]["validate"])
        print(f"  {phase:14} {nt:>8} {nv:>8} {nt + nv:>8}")
        summary[phase] = {"train_n_eligible": nt,
                           "validate_n_eligible": nv,
                           "pooled_n_eligible": nt + nv}

    # === Section 3: first 3 episodes per phase x era ===
    print("\n--- first 3 episodes per phase x era (PRIMARY column "
          "lead-up profile, 5d secondary detail) ---")
    fields = LEADUP_SECONDARY
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

    # === Section 4: median lagged-baseline sigma per phase ===
    print("\n--- median baseline sigma per phase (sample of §4.3-eligible "
          "days) — v2 §7 unmedicated range [25, 55] ---")
    sigma_medians: dict[str, float] = {}
    for phase in PHASE_ORDER:
        sigmas: list[float] = []
        keys = list(pools[phase].keys())
        if not keys:
            sigma_medians[phase] = float("nan")
            print(f"  {phase:14}: sampled_n=0, median_sigma=NaN")
            continue
        step = max(1, len(keys) // 50)
        for d in keys[::step]:
            mu, sig, _ = compute_lagged_baseline(d, PRIMARY_COL, pools)
            if sig is not None:
                sigmas.append(sig)
        med = statistics.median(sigmas) if sigmas else float("nan")
        sigma_medians[phase] = med
        flag = ""
        if phase == "unmedicated" and not math.isnan(med):
            ok = V2_UNMED_SIGMA_RANGE[0] <= med <= V2_UNMED_SIGMA_RANGE[1]
            flag = "OK" if ok else "OUT-OF-RANGE"
        print(f"  {phase:14}: sampled_n={len(sigmas):3}, median_sigma="
              f"{med if not math.isnan(med) else 'NaN':<6} {flag}")

    # === Section 5: raw per-phase median primary (v2 §7 anchor — no §4.3) ===
    print("\n--- raw per-phase median PRIMARY_COL (NO §4.3 filter, "
          "anchored to v2 §7 card medians ±20%) ---")
    raw_medians = raw_per_phase_median_primary(master)
    for phase in PHASE_ORDER:
        card = V2_RAW_CARD_MEDIAN[phase]
        med = raw_medians[phase]
        lo = card * (1 - V2_RAW_CARD_TOL)
        hi = card * (1 + V2_RAW_CARD_TOL)
        ok = (not math.isnan(med)) and lo <= med <= hi
        print(f"  {phase:14}: raw_median={med:>6.1f}  "
              f"(card={card}, tol±20% -> [{lo:.1f}, {hi:.1f}])  "
              f"{'PASS' if ok else 'FAIL'}")

    # === Section 6: pooled-unmedicated n with §4.5 baseline availability ===
    print("\n--- pooled-unmedicated n_clean after §4.5 baseline-availability "
          "exclusions (4d primary lead-up; min 3 of 4 valid) ---")
    unmed_pool_refs = cbpe["unmedicated"]["train"] + cbpe["unmedicated"]["validate"]
    _, n_clean_pooled, _ = evaluate_trigger_freq(
        unmed_pool_refs, PRIMARY_COL, master, pools,
        LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY,
        N_STD_PRIMARY, "one_sided_elevated")
    n_pre_baseline = len(unmed_pool_refs)
    print(f"  pre-§4.5: n_pooled = {n_pre_baseline} "
          f"({len(cbpe['unmedicated']['train'])} train + "
          f"{len(cbpe['unmedicated']['validate'])} validate)")
    print(f"  post-§4.5: n_clean_pooled = {n_clean_pooled}  "
          f"(v2 §10.2 gate: n >= {V2_HEADLINE_N_MIN} -> "
          f"{'PASS' if n_clean_pooled >= V2_HEADLINE_N_MIN else 'FAIL'})")

    # === Section 7: v2 §10.2 spec-sanity-gate summary ===
    print("\n--- v2 §10.2 spec-sanity-gate summary ---")
    fails: list[str] = []

    # Gate 1: pooled-unmedicated n >= 10 post-§4.5
    if n_clean_pooled < V2_HEADLINE_N_MIN:
        fails.append(f"pooled-unmedicated n_clean = {n_clean_pooled} < "
                     f"{V2_HEADLINE_N_MIN} (v2 §10.2 gate 1; §5.3 bar)")
        print(f"  GATE 1 (pooled-unmedicated n >= {V2_HEADLINE_N_MIN}): FAIL "
              f"(n_clean={n_clean_pooled})")
    else:
        print(f"  GATE 1 (pooled-unmedicated n >= {V2_HEADLINE_N_MIN}): PASS "
              f"(n_clean={n_clean_pooled})")

    # Gate 2: per-phase raw median primary within ±20% of v2 §7 card
    for phase in PHASE_ORDER:
        card = V2_RAW_CARD_MEDIAN[phase]
        med = raw_medians[phase]
        lo = card * (1 - V2_RAW_CARD_TOL)
        hi = card * (1 + V2_RAW_CARD_TOL)
        if math.isnan(med):
            print(f"  GATE 2 ({phase}): SKIP (no data)")
            continue
        ok = lo <= med <= hi
        if not ok:
            fails.append(f"{phase} raw median = {med:.1f} outside "
                         f"[{lo:.1f}, {hi:.1f}] (v2 §7 card {card} ±20%)")
        print(f"  GATE 2 ({phase}): {'PASS' if ok else 'FAIL'} "
              f"(raw_median={med:.1f}, card={card}, [{lo:.1f}, {hi:.1f}])")

    # Gate 3: unmedicated median baseline sigma in [25, 55]
    med_sig_unmed = sigma_medians.get("unmedicated", float("nan"))
    if math.isnan(med_sig_unmed):
        print(f"  GATE 3 (unmedicated sigma in {V2_UNMED_SIGMA_RANGE}): SKIP "
              f"(no baselines computable)")
    else:
        ok = V2_UNMED_SIGMA_RANGE[0] <= med_sig_unmed <= V2_UNMED_SIGMA_RANGE[1]
        if not ok:
            fails.append(f"unmedicated median_sigma = {med_sig_unmed:.1f} "
                         f"outside {V2_UNMED_SIGMA_RANGE} (v2 §7)")
        print(f"  GATE 3 (unmedicated sigma in {V2_UNMED_SIGMA_RANGE}): "
              f"{'PASS' if ok else 'FAIL'} "
              f"(median_sigma={med_sig_unmed:.1f})")

    if fails:
        print(f"\n--- DRY-RUN VERDICT: HALT ({len(fails)} sanity failure"
              f"{'s' if len(fails) != 1 else ''}) ---")
        for f in fails:
            print(f"  - {f}")
        print(f"\nPer v2 §9 + §10.4 + hypothesis_lock_process.md §3.9: "
              f"DO NOT run the full test. Spec revision (HA-C4b-v3) required.")
    else:
        print("\n--- DRY-RUN VERDICT: PASS (proceed with `python test.py`) ---")

    return {
        "summary_by_phase": summary,
        "raw_per_phase_median_primary": raw_medians,
        "median_predictor_eligible": {
            p: (statistics.median([r.get(PRIMARY_COL) for r in pools[p].values()
                                    if r.get(PRIMARY_COL) is not None])
                if pools[p] else None)
            for p in PHASE_ORDER},
        "median_baseline_sigma": sigma_medians,
        "n_pooled_unmed_pre_baseline": n_pre_baseline,
        "n_pooled_unmed_post_baseline": n_clean_pooled,
        "sanity_fails": fails,
        "verdict": "HALT" if fails else "PASS",
        "use_quartile_cache": bool(quartile_cache),
    }


def write_dry_run_report(dry_summary: dict, verdict_class: str) -> None:
    """Emit dry-run-report.md (sanity-gate failure or pass companion)."""
    lines: list[str] = []
    if verdict_class == "HALT":
        lines.append("# HA-C4b v2 dry-run report — SANITY-GATE FAILURE (HALT)")
    else:
        lines.append("# HA-C4b v2 dry-run report — sanity gates PASS")
    lines.append("")
    lines.append(
        "Drafted by `test.py --dry-run` per locked v2 hypothesis.md §10.4 "
        "protocol. v2 headline cell: unmedicated × train+validate POOLED × "
        "`S60_Mlow` × N_std=1.5 × primary 4d × one-sided elevated.")
    lines.append("")
    lines.append(
        f"Quartile cache (§4.3 1b.ii): "
        f"{'applied' if dry_summary['use_quartile_cache'] else 'deferred (1b.i only — full run will build cache + reapply)'}")
    lines.append("")

    if verdict_class == "HALT":
        lines.append("## v2 §10.2 spec-sanity-gate failures")
        lines.append("")
        for f in dry_summary["sanity_fails"]:
            lines.append(f"- {f}")
        lines.append("")
        lines.append(
            "Per hypothesis.md v2 §9 + §10.4 + the locked-pre-reg discipline "
            "(`hypothesis_lock_process.md` §3.9), the full test is NOT run "
            "and `result.md` is NOT emitted. The spec must be revised before "
            "any further test run; the revision creates HA-C4b-v3 with v2 "
            "archived alongside v1.")
        lines.append("")

    lines.append("## Eligible-crash-episodes per phase × era")
    lines.append("")
    lines.append("| phase | train | validate | pooled |")
    lines.append("|---|---:|---:|---:|")
    for p in PHASE_ORDER:
        s = dry_summary["summary_by_phase"][p]
        lines.append(f"| {p} | {s['train_n_eligible']} | "
                     f"{s['validate_n_eligible']} | {s['pooled_n_eligible']} |")
    lines.append("")

    lines.append("## Pooled-unmedicated n (v2 headline cell)")
    lines.append("")
    lines.append(
        f"- Pre-§4.5: n = {dry_summary['n_pooled_unmed_pre_baseline']} "
        f"(eligible-crash count after §4.2/§4.3/§6)")
    lines.append(
        f"- Post-§4.5 baseline-availability: n_clean = "
        f"{dry_summary['n_pooled_unmed_post_baseline']} "
        f"(v2 §10.2 gate: n ≥ {V2_HEADLINE_N_MIN} — "
        f"{'PASS' if dry_summary['n_pooled_unmed_post_baseline'] >= V2_HEADLINE_N_MIN else 'FAIL'})")
    lines.append("")

    lines.append("## v2 §7 raw per-phase median PRIMARY_COL (no §4.3 filter)")
    lines.append("")
    lines.append("| phase | raw median | v2 §7 card | tol ±20% range | gate |")
    lines.append("|---|---:|---:|---|---|")
    for p in PHASE_ORDER:
        med = dry_summary["raw_per_phase_median_primary"].get(p, float("nan"))
        card = V2_RAW_CARD_MEDIAN[p]
        lo = card * (1 - V2_RAW_CARD_TOL)
        hi = card * (1 + V2_RAW_CARD_TOL)
        if math.isnan(med):
            gate = "SKIP"
            med_s = "NA"
        else:
            gate = "PASS" if lo <= med <= hi else "FAIL"
            med_s = f"{med:.1f}"
        lines.append(f"| {p} | {med_s} | {card} | [{lo:.1f}, {hi:.1f}] | {gate} |")
    lines.append("")

    lines.append("## Median lagged-baseline σ per phase (§4.3-eligible sample)")
    lines.append("")
    lines.append("| phase | median σ | v2 §7 range (unmedicated [25, 55]) |")
    lines.append("|---|---:|---|")
    for p in PHASE_ORDER:
        med = dry_summary["median_baseline_sigma"].get(p, float("nan"))
        if math.isnan(med):
            med_s = "NA"
            gate = "(unmedicated only)" if p != "unmedicated" else "SKIP"
        else:
            med_s = f"{med:.1f}"
            if p == "unmedicated":
                ok = V2_UNMED_SIGMA_RANGE[0] <= med <= V2_UNMED_SIGMA_RANGE[1]
                gate = "PASS" if ok else "FAIL"
            else:
                gate = "(unmedicated only)"
        lines.append(f"| {p} | {med_s} | {gate} |")
    lines.append("")

    if verdict_class == "HALT":
        lines.append("## Next step (HALT branch)")
        lines.append("")
        lines.append(
            "Per the locked-pre-reg discipline (hypothesis.md v2 §10.4 + §9), "
            "the spec must be revised before any further test run; the "
            "revision creates HA-C4b-v3 with v2 archived. Open a fresh-session "
            "v3-draft per `hypothesis_lock_process.md` §3.2.")
    else:
        lines.append("## Next step (PASS branch)")
        lines.append("")
        lines.append(
            "Sanity gates passed; the full test runs immediately after the "
            "dry-run inside the same `python test.py` invocation, emitting "
            "`result.md` + `result-data.json`.")
    OUT_DRYRUN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {OUT_DRYRUN_MD}", file=sys.stderr)


# === Full-run helpers ====================================================

def _bootstrap_pct_ci(vals: list[float], lo: float = 0.025,
                       hi: float = 0.975) -> tuple[float, float]:
    if not vals:
        return (float("nan"), float("nan"))
    sv = sorted(vals)
    n = len(sv)
    return (sv[int(lo * n)], sv[min(n - 1, int(hi * n))])


def _odds_ratio(p_c: float, p_n: float) -> float:
    eps = 1e-6
    p_c = min(max(p_c, eps), 1 - eps)
    p_n = min(max(p_n, eps), 1 - eps)
    return (p_c / (1 - p_c)) / (p_n / (1 - p_n))


def evaluate_cell(refs: list[date],
                    eligible_dates: list[date],
                    col: str,
                    master: dict[date, dict],
                    pools: dict[str, dict[date, dict[str, float]]],
                    leadup_days: int,
                    min_valid: int,
                    N_std: float,
                    mode: str,
                    B: int,
                    rng: random.Random) -> dict:
    """Evaluate (a)+(b)+(c) + RD/OR with bootstrap-percentile CI on a
    single cell. Returns a dict; verdict 'inconclusive' if n_clean < 10."""
    obs_freq, n_clean, profs = evaluate_trigger_freq(
        refs, col, master, pools, leadup_days, min_valid, N_std, mode)
    out = {"n_pre_§4.5": len(refs), "n_clean": n_clean, "B": B, "N_std": N_std}
    if n_clean < V2_HEADLINE_N_MIN or not eligible_dates:
        out["verdict"] = "inconclusive"
        out["obs_freq"] = obs_freq if n_clean > 0 else None
        return out
    null_freqs = bootstrap_null_distribution(
        eligible_dates, len(refs), col, master, pools,
        leadup_days, min_valid, N_std, mode, B, rng)
    null_med = statistics.median(null_freqs) if null_freqs else 0.0
    p_val = (sum(1 for f in null_freqs if f >= obs_freq)
             / max(1, len(null_freqs)))
    disc_pp = (obs_freq - null_med) * 100
    if mode == "bidirectional":
        mags = [p["max_abs_z"] for p in profs]
    else:
        mags = [p["max_signed_z"] for p in profs]
    med_mag = statistics.median(mags) if mags else 0.0
    crit_a = obs_freq >= CRIT_A_FRAC
    crit_b = disc_pp >= CRIT_B_DISC_PP
    crit_c = med_mag >= N_std / 2
    verdict = ("supported" if (crit_a and crit_b and crit_c) else "refuted")
    rd_distrib = [obs_freq - f for f in null_freqs]
    rd_lo, rd_hi = _bootstrap_pct_ci(rd_distrib)
    or_pt = _odds_ratio(obs_freq, null_med)
    or_distrib = [_odds_ratio(obs_freq, f) for f in null_freqs]
    or_lo, or_hi = _bootstrap_pct_ci(or_distrib)
    out.update({
        "verdict": verdict,
        "obs_freq": obs_freq,
        "null_median_freq": null_med,
        "disc_pp": disc_pp,
        "p_value": p_val,
        "median_magnitude": med_mag,
        "crit_a_pass": crit_a,
        "crit_b_pass": crit_b,
        "crit_c_pass": crit_c,
        "rd_point": obs_freq - null_med,
        "rd_ci": [rd_lo, rd_hi],
        "or_point": or_pt,
        "or_ci": [or_lo, or_hi],
        "null_freqs": null_freqs,
        "profs_per_ep": [
            {"ref": p["ref"].isoformat(),
             "max_signed_z": p["max_signed_z"],
             "max_abs_z": p["max_abs_z"],
             "all_signed_zs": p["all_signed_zs"],
             "triggered_one_sided": p["max_signed_z"] >= N_std,
             "triggered_bidir": p["max_abs_z"] >= N_std}
            for p in profs
        ],
    })
    return out


def descriptive_cell(refs: list[date],
                       col: str,
                       master: dict[date, dict],
                       pools: dict[str, dict[date, dict[str, float]]],
                       leadup_days: int,
                       min_valid: int,
                       N_std: float,
                       mode: str) -> dict:
    """Descriptive (no null): just (a) and (c) for a sub-bar n cell."""
    obs_freq, n_clean, profs = evaluate_trigger_freq(
        refs, col, master, pools, leadup_days, min_valid, N_std, mode)
    if mode == "bidirectional":
        mags = [p["max_abs_z"] for p in profs]
    else:
        mags = [p["max_signed_z"] for p in profs]
    med_mag = statistics.median(mags) if mags else float("nan")
    return {
        "n_pre_§4.5": len(refs),
        "n_clean": n_clean,
        "obs_freq": obs_freq if n_clean > 0 else None,
        "median_magnitude": med_mag,
        "N_std": N_std,
        "per_episode": [
            {"ref": p["ref"].isoformat(),
             "max_signed_z": p["max_signed_z"],
             "max_abs_z": p["max_abs_z"],
             "triggered_one_sided": p["max_signed_z"] >= N_std,
             "triggered_bidir": p["max_abs_z"] >= N_std}
            for p in profs
        ],
    }


def loo_fragility(headline_cell: dict,
                    refs: list[date],
                    train_end: date,
                    null_med: float,
                    null_freqs: list[float]) -> dict:
    """§4.11.5 episode-level leave-one-out fragility check.
    Reuses the headline cell's fixed null distribution; recomputes
    (a)/(b)/(c) on the n-1 surviving episodes per LOO drop."""
    profs = headline_cell["profs_per_ep"]
    n = len(profs)
    if n != V2_HEADLINE_N_MIN:
        # LOO only meaningful at headline; flag and proceed
        pass
    triggered = [p["triggered_one_sided"] for p in profs]
    k_total = sum(triggered)
    loo_rows: list[dict] = []
    load_bearing: list[dict] = []
    headline_a_pass = headline_cell["crit_a_pass"]
    for i, p in enumerate(profs):
        drop_ref_iso = p["ref"]
        drop_era = ("train" if date.fromisoformat(drop_ref_iso) <= train_end
                    else "validate")
        # Surviving n-1
        survivors = profs[:i] + profs[i + 1:]
        n_surv = len(survivors)
        k_surv = sum(1 for s in survivors if s["triggered_one_sided"])
        a_loo = k_surv / n_surv if n_surv > 0 else float("nan")
        disc_loo_pp = (a_loo - null_med) * 100
        mags_surv = [s["max_signed_z"] for s in survivors]
        c_loo = statistics.median(mags_surv) if mags_surv else float("nan")
        a_loo_pass = a_loo >= CRIT_A_FRAC
        flipped = (headline_a_pass and not a_loo_pass) or (
            (not headline_a_pass) and a_loo_pass)
        row = {
            "dropped_ref": drop_ref_iso,
            "dropped_era": drop_era,
            "dropped_triggered_in_headline": triggered[i],
            "dropped_max_signed_z": p["max_signed_z"],
            "a_loo": a_loo,
            "disc_loo_pp": disc_loo_pp,
            "c_loo": c_loo,
            "a_loo_pass": a_loo_pass,
            "flips_a_verdict": flipped,
        }
        loo_rows.append(row)
        if flipped:
            load_bearing.append(row)
    a_loos = [r["a_loo"] for r in loo_rows if not math.isnan(r["a_loo"])]
    c_loos = [r["c_loo"] for r in loo_rows if not math.isnan(r["c_loo"])]
    stability = {
        "a_loo_min": min(a_loos) if a_loos else float("nan"),
        "a_loo_max": max(a_loos) if a_loos else float("nan"),
        "a_loo_mean": statistics.mean(a_loos) if a_loos else float("nan"),
        "a_loo_std": (statistics.stdev(a_loos)
                      if len(a_loos) > 1 else float("nan")),
        "c_loo_mean": statistics.mean(c_loos) if c_loos else float("nan"),
        "c_loo_std": (statistics.stdev(c_loos)
                      if len(c_loos) > 1 else float("nan")),
    }
    return {
        "n_total": n,
        "k_total_triggered": k_total,
        "headline_a_rate": k_total / n if n > 0 else float("nan"),
        "headline_a_pass": headline_a_pass,
        "loo_rows": loo_rows,
        "stability": stability,
        "load_bearing_episodes": load_bearing,
        "load_bearing_count": len(load_bearing),
        "boundary_distance_note": (
            "Per v2 §4.11.5 boundary-fragility note: at pooled n=10 the §5.1 "
            "(a) gate fires when k>=6. LOO flips only happen at k=6 exactly "
            "(every firing-drop flips to 5/9=0.556<0.60). At k>=7 no LOO flip "
            "(worst 6/9=0.667 passes); at k<=5 no LOO flip (best 5/9=0.556 "
            f"fails). Observed k={k_total} -> "
            f"{'AT BOUNDARY (k=6)' if k_total == 6 else ('ABOVE BOUNDARY (k>=7)' if k_total >= 7 else 'BELOW BOUNDARY (k<=5)')}; "
            "empty load-bearing list at k!=6 is a boundary-distance signal, "
            "NOT 'no fragility detected'."
        ),
    }


# === Full run (§10.4 step 2) ============================================

def run_full(slm: dict[date, dict],
              master: dict[date, dict],
              crash_starts: list[date],
              dry_summary: dict) -> dict:
    if not QUARTILE_CACHE.exists():
        print("[full] quartile cache missing -> building (slow, ~5-15 min)",
              file=sys.stderr)
        build_quartile_cache()
    quartile_cache = load_quartile_cache()
    if not quartile_cache:
        print("ERROR: quartile cache empty after build attempt",
              file=sys.stderr)
        sys.exit(1)

    # Rebuild pools and cbpe under §4.3 1b.ii now applied (full discipline)
    pools = build_eligible_pools(slm, master, quartile_cache)
    cbpe = crash_episodes_by_phase_era(crash_starts, slm, master,
                                         quartile_cache)

    rng = random.Random(RANDOM_SEED)

    eligible_dates_by_phase: dict[str, list[date]] = {
        phase: sorted(pools[phase].keys()) for phase in PHASE_ORDER}

    results: dict = {
        "v2_spec_commit": "2417043",
        "config": {
            "B_HEADLINE": B_HEADLINE,
            "B_DIAGNOSTIC": B_DIAGNOSTIC,
            "BOOTSTRAP_E_L": BOOTSTRAP_E_L,
            "RANDOM_SEED": RANDOM_SEED,
            "headline_phase": HEADLINE_PHASE,
            "headline_pooled": True,
            "headline_col": PRIMARY_COL,
            "headline_N_std": N_STD_PRIMARY,
            "headline_window": "primary 4d",
            "headline_mode": "one_sided_elevated",
        },
        "dry_run_summary": {
            "n_pooled_unmed_pre_baseline": dry_summary["n_pooled_unmed_pre_baseline"],
            "n_pooled_unmed_post_baseline": dry_summary["n_pooled_unmed_post_baseline"],
            "raw_per_phase_median_primary": dry_summary["raw_per_phase_median_primary"],
            "median_baseline_sigma": dry_summary["median_baseline_sigma"],
        },
    }

    # === v2 HEADLINE: unmedicated × pooled × S60_Mlow × N_std=1.5 ×
    #                    primary 4d × one-sided elevated
    print("\n=== v2 HEADLINE: unmedicated × pooled × S60_Mlow × "
          "N_std=1.5 × primary 4d × one-sided elevated ===")
    unmed_pool_refs = cbpe["unmedicated"]["train"] + cbpe["unmedicated"]["validate"]
    unmed_eligible = eligible_dates_by_phase["unmedicated"]
    print(f"  pooled refs: {len(unmed_pool_refs)} "
          f"({len(cbpe['unmedicated']['train'])} train + "
          f"{len(cbpe['unmedicated']['validate'])} validate)")
    print(f"  unmedicated eligible pool: {len(unmed_eligible)} days")

    headline = evaluate_cell(
        unmed_pool_refs, unmed_eligible, PRIMARY_COL, master, pools,
        LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY,
        N_STD_PRIMARY, "one_sided_elevated", B_HEADLINE, rng)
    if headline["verdict"] != "inconclusive":
        print(f"  HEADLINE verdict: {headline['verdict'].upper()} "
              f"(obs={headline['obs_freq']*100:.1f}%, "
              f"null={headline['null_median_freq']*100:.1f}%, "
              f"disc={headline['disc_pp']:+.1f}pp, "
              f"p={headline['p_value']:.4f}, "
              f"med_z={headline['median_magnitude']:+.2f}, "
              f"OR={headline['or_point']:.2f} "
              f"[{headline['or_ci'][0]:.2f},{headline['or_ci'][1]:.2f}])")
        print(f"    (a) freq ≥ 60%:       "
              f"{'PASS' if headline['crit_a_pass'] else 'FAIL'} "
              f"({headline['obs_freq']*100:.1f}%)")
        print(f"    (b) disc ≥ +15pp:     "
              f"{'PASS' if headline['crit_b_pass'] else 'FAIL'} "
              f"({headline['disc_pp']:+.1f}pp)")
        print(f"    (c) med |z| ≥ 0.75:   "
              f"{'PASS' if headline['crit_c_pass'] else 'FAIL'} "
              f"({headline['median_magnitude']:+.2f})")
    else:
        print(f"  HEADLINE verdict: INCONCLUSIVE (n_clean={headline['n_clean']})")
    results["headline"] = headline

    # === §4.11.5 LOO fragility check (on the headline) ===
    print("\n=== §4.11.5 LOO fragility check ===")
    if headline["verdict"] != "inconclusive":
        loo = loo_fragility(headline, unmed_pool_refs, TRAIN_END,
                              headline["null_median_freq"], headline["null_freqs"])
        print(f"  k_total triggered = {loo['k_total_triggered']}/{loo['n_total']} "
              f"({loo['headline_a_rate']*100:.1f}%)")
        print(f"  a_loo range: [{loo['stability']['a_loo_min']*100:.1f}%, "
              f"{loo['stability']['a_loo_max']*100:.1f}%]; "
              f"mean {loo['stability']['a_loo_mean']*100:.1f}% "
              f"± {loo['stability']['a_loo_std']*100:.1f}%")
        print(f"  load-bearing episodes (verdict flippers): "
              f"{loo['load_bearing_count']}")
        if loo['load_bearing_count']:
            for r in loo["load_bearing_episodes"]:
                print(f"    - {r['dropped_ref']} ({r['dropped_era']}); "
                      f"dropped trig={r['dropped_triggered_in_headline']}; "
                      f"a_loo={r['a_loo']*100:.1f}%")
        results["loo_fragility"] = loo
    else:
        print(f"  LOO skipped (headline inconclusive)")
        results["loo_fragility"] = None

    # === Descriptive companions on the headline cell: train-only,
    #     validate-only directional consistency
    print("\n=== Train-only / validate-only descriptive companions ===")
    train_unmed = cbpe["unmedicated"]["train"]
    validate_unmed = cbpe["unmedicated"]["validate"]
    desc_train = descriptive_cell(
        train_unmed, PRIMARY_COL, master, pools,
        LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY,
        N_STD_PRIMARY, "one_sided_elevated")
    desc_validate = descriptive_cell(
        validate_unmed, PRIMARY_COL, master, pools,
        LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY,
        N_STD_PRIMARY, "one_sided_elevated")
    print(f"  train-only (n={desc_train['n_clean']}): "
          f"a={desc_train['obs_freq']*100 if desc_train['obs_freq'] is not None else float('nan'):.1f}%, "
          f"med_z={desc_train['median_magnitude']:+.2f}")
    print(f"  validate-only (n={desc_validate['n_clean']}): "
          f"a={desc_validate['obs_freq']*100 if desc_validate['obs_freq'] is not None else float('nan'):.1f}%, "
          f"med_z={desc_validate['median_magnitude']:+.2f}")
    results["companion_train_only"] = desc_train
    results["companion_validate_only"] = desc_validate

    # === Companion-phase descriptive cells (consol/buildup/afbouw × validate)
    print("\n=== Companion-phase descriptive cells (all pre-declared "
          "INCONCLUSIVE per v2 §5.3) ===")
    companion_phases: dict[str, dict] = {}
    for phase in ["consolidation", "buildup", "afbouw"]:
        for era in ["train", "validate"]:
            refs = cbpe[phase][era]
            if not refs:
                continue
            desc = descriptive_cell(
                refs, PRIMARY_COL, master, pools,
                LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY,
                N_STD_PRIMARY, "one_sided_elevated")
            companion_phases.setdefault(phase, {})[era] = desc
            print(f"  {phase} × {era} (n={desc['n_clean']}): "
                  f"a={(desc['obs_freq']*100) if desc['obs_freq'] is not None else float('nan'):.1f}%, "
                  f"med_z={desc['median_magnitude']:+.2f}")
    results["companion_phases"] = companion_phases

    # === Sensitivity ladder: unmedicated × pooled × 6 unique cols ×
    #     N_std={1.5, 2.0, 2.5} × primary 4d × one-sided
    print("\n=== Sensitivity ladder (unmedicated × pooled × 6 unique cols × "
          "N_std tiers × primary 4d × one-sided) ===")
    ladder: dict[str, dict] = {}
    for col in LADDER_UNIQUE:
        ladder[col] = {}
        for N_std in N_STD_TIERS:
            cell = evaluate_cell(
                unmed_pool_refs, unmed_eligible, col, master, pools,
                LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY,
                N_std, "one_sided_elevated", B_DIAGNOSTIC, rng)
            cell.pop("null_freqs", None)
            cell.pop("profs_per_ep", None)
            ladder[col][f"N_std={N_std}"] = cell
            if cell.get("verdict") == "inconclusive":
                print(f"  {col.replace('stress_low_motion_min_count_', ''):20} "
                      f"N_std={N_std}: INCONCLUSIVE (n={cell['n_clean']})")
            else:
                print(f"  {col.replace('stress_low_motion_min_count_', ''):20} "
                      f"N_std={N_std}: {cell['verdict']:9} "
                      f"a={cell['obs_freq']*100:5.1f}% "
                      f"null={cell['null_median_freq']*100:5.1f}% "
                      f"disc={cell['disc_pp']:+5.1f}pp "
                      f"med_z={cell['median_magnitude']:+.2f}")
    results["sensitivity_ladder"] = ladder

    # Note duplicate columns
    results["sensitivity_ladder_duplicates"] = {
        c: f"identical-by-construction to {c.replace('Mbelow_mod','Mlow')} (per stress_low_motion_primitive §3.2)"
        for c in LADDER_DUPLICATES
    }

    # === Secondary 5d + bidirectional sensitivity on headline cell
    print("\n=== Headline cell sensitivity arms (5d secondary, bidirectional) ===")
    sens_arms: dict[str, dict] = {}
    for window_label, leadup, min_v in [
        ("4d_primary", LEADUP_PRIMARY, MIN_LEADUP_VALID_PRIMARY),
        ("5d_secondary", LEADUP_SECONDARY, MIN_LEADUP_VALID_SECONDARY),
    ]:
        for arm_mode in ["one_sided_elevated", "bidirectional"]:
            if window_label == "4d_primary" and arm_mode == "one_sided_elevated":
                continue  # is the headline itself
            cell = evaluate_cell(
                unmed_pool_refs, unmed_eligible, PRIMARY_COL, master, pools,
                leadup, min_v, N_STD_PRIMARY, arm_mode, B_DIAGNOSTIC, rng)
            cell.pop("null_freqs", None)
            cell.pop("profs_per_ep", None)
            sens_arms[f"{window_label}_{arm_mode}"] = cell
            v = cell.get("verdict", "?")
            if v == "inconclusive":
                print(f"  {window_label} {arm_mode}: INCONCLUSIVE")
            else:
                print(f"  {window_label} {arm_mode}: {v} a={cell['obs_freq']*100:.1f}% "
                      f"disc={cell['disc_pp']:+.1f}pp")
    results["headline_sensitivity_arms"] = sens_arms

    # === E[L]* on unmedicated eligible pool (companion) ===
    print("\n=== Data-driven E[L]* on unmedicated PRIMARY_COL ===")
    unmed_dates = sorted(pools["unmedicated"].keys())
    unmed_vals = [pools["unmedicated"][d][PRIMARY_COL]
                   for d in unmed_dates
                   if PRIMARY_COL in pools["unmedicated"][d]]
    el_star = estimate_block_length(unmed_vals)
    flag = (abs(el_star - BOOTSTRAP_E_L) / BOOTSTRAP_E_L > 0.5
            if not math.isnan(el_star) else False)
    print(f"  E[L]* = {el_star:.2f} (default = {BOOTSTRAP_E_L}); "
          f"factor-of-2 flag: {'YES' if flag else 'no'}")
    results["e_l_star"] = {"value": el_star, "default": BOOTSTRAP_E_L,
                            "flag_outside_tolerance": flag}

    # === §4.11 secondary descriptive outcomes ===
    print("\n=== §4.11 secondary descriptive outcomes ===")
    secondary: dict = {}

    # Same-day Spearman per phase × era + crash-drop sensitivity
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
            secondary.setdefault("spearman_primary_vs_gevoelscore",
                                  {}).setdefault(phase, {})[era] = {
                "n_full": len(xs), "rho_full": rho_full,
                "n_no_crash": len(xs_nc), "rho_no_crash": rho_nc,
                "delta_rho": (rho_full - rho_nc)
                if not math.isnan(rho_full) and not math.isnan(rho_nc)
                else float("nan"),
            }

    # v2-specific: Spearman ON pooled-unmedicated heavy-exertion-conditioned
    # subset (the headline cell's "universe" — exertion-conditioned days only,
    # all unmedicated, train + validate pooled).
    xs_h: list[float] = []
    ys_h: list[float] = []
    for d in eligible_dates_by_phase["unmedicated"]:
        ok, _ = day_exertion_eligible(d, master)
        if not ok:
            continue
        v = pools["unmedicated"][d].get(PRIMARY_COL)
        g = master.get(d, {}).get("gevoelscore", "")
        if v is None or not g:
            continue
        try:
            gf = float(g)
        except ValueError:
            continue
        xs_h.append(v)
        ys_h.append(gf)
    rho_h = spearman_rho(xs_h, ys_h) if len(xs_h) >= 3 else float("nan")
    secondary["spearman_unmed_pooled_exertion_conditioned"] = {
        "n": len(xs_h),
        "rho": rho_h,
    }

    # Construct disambiguation 2x2
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
        secondary[f"construct_disambig_vs_{label}"] = sibling_block

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
    secondary["respiration_companion_sensitivity"] = resp_block

    results["secondary"] = secondary

    # === Strip null_freqs from headline (large) before serialising ===
    if "null_freqs" in results["headline"]:
        # Keep only summary stats; drop the full B-length list for JSON size
        nf = results["headline"]["null_freqs"]
        results["headline"]["null_freqs_summary"] = {
            "B": len(nf),
            "min": min(nf) if nf else None,
            "max": max(nf) if nf else None,
            "p05": _bootstrap_pct_ci(nf, 0.025, 0.975)[0],
            "p95": _bootstrap_pct_ci(nf, 0.025, 0.975)[1],
            "median": statistics.median(nf) if nf else None,
        }
        del results["headline"]["null_freqs"]

    return results


# === Result.md writer (§10.3 v2 layout) =================================

def _fmt_pct(v: float | None) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    return f"{v * 100:.1f}%"


def _fmt_z(v: float | None) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    return f"{v:+.2f}"


def _fmt_pp(v: float | None) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    return f"{v:+.1f}pp"


def write_result_md(results: dict) -> None:
    H = results.get("headline", {})
    verdict_raw = H.get("verdict", "inconclusive")
    if verdict_raw == "supported":
        verdict = "SUPPORTED"
    elif verdict_raw == "refuted":
        verdict = "NOT-SUPPORTED"
    else:
        verdict = "INCONCLUSIVE"

    lines: list[str] = []
    lines.append("# HA-C4b v2 — Result: stress-with-low-motion minute count "
                 "as crash precursor (unmedicated pooled headline)")
    lines.append("")
    lines.append(
        f"**Headline verdict ({HEADLINE_PHASE} phase × train+validate "
        f"POOLED × `{PRIMARY_COL}` × N_std={N_STD_PRIMARY} × primary 4d × "
        f"one-sided elevated): {verdict}**")
    lines.append("")
    lines.append(
        f"Single-cell lock per v2 §5.0; no other cell can promote. "
        f"Data: [result-data.json]({OUT_DATA_JSON.name}). "
        f"Companion: [dry-run-report.md]({OUT_DRYRUN_MD.name}).")
    lines.append("")

    # === v1 → v2 transition disclosure (prominently placed per v2 §8) ===
    lines.append("## v1 → v2 relock disclosure (per v2 §8 caveat)")
    lines.append("")
    lines.append(
        "The headline cell was relocked from `consolidation × both-eras` "
        "(v1) to `unmedicated × train+validate pooled` (v2) AFTER v1's "
        "dry-run halt (2026-06-15). The relock honoured the locked-pre-reg "
        "discipline (v1 archived at [`hypothesis-v1-archived.md`](hypothesis-v1-archived.md); "
        "v2 drafted in a fresh session per [`hypothesis_lock_process.md` §3.2](../../../methodology/hypothesis_lock_process.md#32-drafting-step-step-1-of-the-arc) "
        "with per-episode z-scores held out from the v2 drafting session), "
        "but introduces a researcher-degrees-of-freedom concern: the "
        "corpus's available cells were known at v2 drafting time (the "
        "eligible-n table from v1's dry-run report), and the pooled-"
        "unmedicated cell was selected partly because it was the only "
        "above-bar cell available on the corpus.")
    lines.append("")
    lines.append(
        "The within-test discipline against this concern: §5.0 single-cell "
        "lock + descriptive companion treatment of all other arms (other "
        "phases, train-only / validate-only subsets, LOO drops, N_std "
        "tiers, secondary 5d, bidirectional). The inferential defence: the "
        "stationary-bootstrap null at E[L]=7 from §4.9. The upstream defence "
        "for future pre-regs: the `hypothesis_lock_process.md` v1.2 §5 row "
        "(structural-completeness + EXACT-column anchor) that v2 closes.")
    lines.append("")
    lines.append(
        "Independent of this concern, **v2's pooled headline is structurally "
        "NOT a both-eras finding** in the project's HA-family sense. The "
        "HA11/HA06b/HA10 family pattern of independent train + validate "
        "verdicts is abandoned for this hypothesis; v2 pools train (n=8) + "
        "validate (n=2) within the unmedicated phase to clear the §5.3 n≥10 "
        "bar. The compensating mechanism is the descriptive directional-"
        "consistency companion on the train-only and validate-only subsets "
        "(below). See v2 §8 caveat 2.")
    lines.append("")

    # === Headline numbers ===
    lines.append(
        f"## Headline numbers (unmedicated × pooled × `{PRIMARY_COL}` × "
        f"N_std=1.5 × primary 4d × one-sided elevated)")
    lines.append("")
    if H.get("verdict") == "inconclusive":
        lines.append(
            f"Cell INCONCLUSIVE: n_clean = {H.get('n_clean', 'NA')} "
            f"(pre-§4.5: {H.get('n_pre_§4.5', 'NA')}); did not clear v2 "
            f"§5.3 bar (n ≥ {V2_HEADLINE_N_MIN}).")
        lines.append("")
    else:
        lines.append("| metric | value |")
        lines.append("|---|---:|")
        lines.append(f"| episodes pre-§4.5 | {H['n_pre_§4.5']} |")
        lines.append(f"| episodes post-§4.5 (n_clean) | {H['n_clean']} |")
        lines.append(f"| (a) frac event (observed) | {_fmt_pct(H['obs_freq'])} |")
        lines.append(f"| null median freq (B={B_HEADLINE}) | {_fmt_pct(H['null_median_freq'])} |")
        lines.append(f"| (b) discrimination pp | {_fmt_pp(H['disc_pp'])} |")
        lines.append(f"| p-value (one-sided, block-permutation E[L]={BOOTSTRAP_E_L}) | {H['p_value']:.4f} |")
        lines.append(f"| (c) median magnitude (max_signed_z) | {_fmt_z(H['median_magnitude'])} |")
        lines.append(f"| RD (point) | {H['rd_point']:+.3f} |")
        lines.append(f"| RD 95% CI | [{H['rd_ci'][0]:+.3f}, {H['rd_ci'][1]:+.3f}] |")
        lines.append(f"| OR (point) | {H['or_point']:.2f} |")
        lines.append(f"| OR 95% CI | [{H['or_ci'][0]:.2f}, {H['or_ci'][1]:.2f}] |")
        lines.append(f"| crit (a) freq ≥ 60% | {'PASS' if H['crit_a_pass'] else 'FAIL'} |")
        lines.append(f"| crit (b) disc ≥ +15pp | {'PASS' if H['crit_b_pass'] else 'FAIL'} |")
        lines.append(f"| crit (c) med ≥ 0.75 | {'PASS' if H['crit_c_pass'] else 'FAIL'} |")
        lines.append(f"| overall verdict | **{verdict}** |")
        lines.append("")

    # === Per-episode (the 10 pooled episodes, ordered chronologically) ===
    if H.get("verdict") != "inconclusive" and H.get("profs_per_ep"):
        lines.append("### Per-episode lead-up (pooled unmedicated, n = "
                     f"{H['n_clean']})")
        lines.append("")
        lines.append("| episode date | era | max_signed_z | max|z| | triggered (one-sided ≥1.5) |")
        lines.append("|---|---|---:|---:|---|")
        for p in H["profs_per_ep"]:
            era = ("train" if date.fromisoformat(p["ref"]) <= TRAIN_END
                   else "validate")
            lines.append(
                f"| {p['ref']} | {era} | {p['max_signed_z']:+.2f} | "
                f"{p['max_abs_z']:.2f} | "
                f"{'YES' if p['triggered_one_sided'] else 'no'} |")
        lines.append("")

    # === Train-only / validate-only directional consistency ===
    lines.append("## Train-only / validate-only descriptive companions "
                 "(pre-declared INCONCLUSIVE per v2 §5.3; reported for "
                 "directional consistency only)")
    lines.append("")
    dt = results.get("companion_train_only", {})
    dv = results.get("companion_validate_only", {})
    lines.append("| subset | n_clean | (a) rate | median max_signed_z |")
    lines.append("|---|---:|---:|---:|")
    lines.append(
        f"| train-only unmedicated | {dt.get('n_clean', 'NA')} | "
        f"{_fmt_pct(dt.get('obs_freq'))} | "
        f"{_fmt_z(dt.get('median_magnitude'))} |")
    lines.append(
        f"| validate-only unmedicated | {dv.get('n_clean', 'NA')} | "
        f"{_fmt_pct(dv.get('obs_freq'))} | "
        f"{_fmt_z(dv.get('median_magnitude'))} |")
    lines.append("")
    if dv.get("per_episode"):
        lines.append("### Validate-only unmedicated per-episode (n = "
                     f"{dv.get('n_clean', 'NA')})")
        lines.append("")
        lines.append("| episode date | max_signed_z | max|z| | triggered (one-sided ≥1.5) |")
        lines.append("|---|---:|---:|---|")
        for p in dv["per_episode"]:
            lines.append(
                f"| {p['ref']} | {p['max_signed_z']:+.2f} | "
                f"{p['max_abs_z']:.2f} | "
                f"{'YES' if p['triggered_one_sided'] else 'no'} |")
        lines.append("")

    # === LOO fragility ===
    loo = results.get("loo_fragility")
    lines.append("## Episode-level leave-one-out (LOO) fragility check (§4.11.5)")
    lines.append("")
    if loo is None:
        lines.append("Skipped — headline cell was INCONCLUSIVE.")
        lines.append("")
    else:
        lines.append(
            f"Pooled n = {loo['n_total']}; k_total triggered = "
            f"{loo['k_total_triggered']} ({loo['headline_a_rate']*100:.1f}%). "
            f"Headline (a) gate: "
            f"{'PASS' if loo['headline_a_pass'] else 'FAIL'} (≥60%).")
        lines.append("")
        lines.append(
            f"LOO (a) range: "
            f"[{loo['stability']['a_loo_min']*100:.1f}%, "
            f"{loo['stability']['a_loo_max']*100:.1f}%]. "
            f"Mean ± std: "
            f"{loo['stability']['a_loo_mean']*100:.1f}% ± "
            f"{loo['stability']['a_loo_std']*100:.1f}%. "
            f"LOO median magnitude (c) mean ± std: "
            f"{loo['stability']['c_loo_mean']:+.2f} ± "
            f"{loo['stability']['c_loo_std']:.2f}.")
        lines.append("")
        lines.append(f"Load-bearing episodes (removal flips the §5.1 (a) "
                     f"verdict at the 60% gate): "
                     f"**{loo['load_bearing_count']}**.")
        lines.append("")
        lines.append("**Boundary-fragility note** (per v2 §4.11.5):")
        lines.append("")
        lines.append("> " + loo["boundary_distance_note"].replace("\n", " "))
        lines.append("")
        lines.append("### LOO range table (per drop)")
        lines.append("")
        lines.append("| dropped episode | era | trigger in headline | a_loo | disc_loo_pp | c_loo | flips (a) verdict |")
        lines.append("|---|---|---|---:|---:|---:|---|")
        for r in loo["loo_rows"]:
            lines.append(
                f"| {r['dropped_ref']} | {r['dropped_era']} | "
                f"{'YES' if r['dropped_triggered_in_headline'] else 'no'} | "
                f"{r['a_loo']*100:.1f}% | {r['disc_loo_pp']:+.1f}pp | "
                f"{r['c_loo']:+.2f} | "
                f"{'**YES**' if r['flips_a_verdict'] else 'no'} |")
        lines.append("")
        if loo["load_bearing_episodes"]:
            lines.append("### Load-bearing episodes (case-study candidates)")
            lines.append("")
            for r in loo["load_bearing_episodes"]:
                lines.append(
                    f"- **{r['dropped_ref']}** ({r['dropped_era']}); "
                    f"triggered in headline: "
                    f"{'YES' if r['dropped_triggered_in_headline'] else 'no'}; "
                    f"max_signed_z={r['dropped_max_signed_z']:+.2f}; "
                    f"a_loo={r['a_loo']*100:.1f}%.")
            lines.append("")

    # === Companion phases ===
    lines.append("## Companion-phase descriptive cells (pre-declared "
                 "INCONCLUSIVE per v2 §5.3)")
    lines.append("")
    lines.append("Phases other than unmedicated have train arms empty by "
                 "phase-boundary construction (train ends 2023-12-31; "
                 "consolidation/buildup/afbouw start ≥ 2024-04-09). Only "
                 "validate arms are reported; none promotes to SUPPORTED.")
    lines.append("")
    cp = results.get("companion_phases", {})
    lines.append("| phase × era | n_pre_§4.5 | n_clean | (a) rate | median max_signed_z |")
    lines.append("|---|---:|---:|---:|---:|")
    for phase in ["consolidation", "buildup", "afbouw"]:
        for era in ["validate"]:
            rec = cp.get(phase, {}).get(era)
            if not rec:
                continue
            lines.append(
                f"| {phase} × {era} | {rec['n_pre_§4.5']} | {rec['n_clean']} | "
                f"{_fmt_pct(rec['obs_freq'])} | "
                f"{_fmt_z(rec['median_magnitude'])} |")
    lines.append("")

    # === Sensitivity ladder ===
    lines.append("## Sensitivity ladder (unmedicated × pooled × 6 unique "
                 "cols × 3 N_std tiers × primary 4d × one-sided)")
    lines.append("")
    lines.append(
        "Per v2 §4.10 + stress_low_motion_primitive §3.2: 6 unique columns "
        "+ 3 identical-by-construction duplicates (`Mbelow_mod` ≡ `Mlow` at "
        "same S threshold; duplicates emitted to result-data.json but not "
        "tabulated here). Threshold-monotonicity check: at the same motion "
        "class, S=50 ≥ S=60 ≥ S=75 in firing rate (per primitive §8.3). "
        "Verdicts diagnostic only; none promotes to SUPPORTED per §5.0.")
    lines.append("")
    lines.append("| col | N_std=1.5 | N_std=2.0 | N_std=2.5 |")
    lines.append("|---|---|---|---|")
    ladder = results.get("sensitivity_ladder", {})
    for col in LADDER_UNIQUE:
        col_short = col.replace("stress_low_motion_min_count_", "")
        row = [col_short]
        for N_std in N_STD_TIERS:
            cell = ladder.get(col, {}).get(f"N_std={N_std}", {})
            v = cell.get("verdict", "?")
            if v == "inconclusive":
                row.append(f"INCONC (n={cell.get('n_clean', 0)})")
            else:
                obs = cell.get("obs_freq")
                if obs is None:
                    row.append("—")
                    continue
                row.append(
                    f"{v[:4]} a={obs*100:.0f}% "
                    f"d={cell.get('disc_pp', 0):+.0f}pp")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    # === Headline sensitivity arms (5d + bidirectional) ===
    lines.append("## Headline cell sensitivity arms (transparency only, "
                 "no SUPPORTED promotion)")
    lines.append("")
    arms = results.get("headline_sensitivity_arms", {})
    lines.append("| arm | n_clean | verdict | (a) | disc_pp | med_z |")
    lines.append("|---|---:|---|---:|---:|---:|")
    for key, cell in arms.items():
        v = cell.get("verdict", "?")
        n = cell.get("n_clean", 0)
        obs = cell.get("obs_freq")
        disc = cell.get("disc_pp", float("nan"))
        med_mag = cell.get("median_magnitude", float("nan"))
        lines.append(
            f"| {key} | {n} | {v} | {_fmt_pct(obs)} | "
            f"{_fmt_pp(disc) if not (isinstance(disc, float) and math.isnan(disc)) else '—'} | "
            f"{_fmt_z(med_mag)} |")
    lines.append("")

    # === E[L]* ===
    el = results.get("e_l_star", {})
    lines.append("## E[L]* data-driven block length (unmedicated pool)")
    lines.append("")
    if not math.isnan(el.get("value", float("nan"))):
        lines.append(
            f"- E[L]* = {el['value']:.2f}; default E[L] = {el['default']}; "
            f"factor-of-2 flag: "
            f"{'YES — verdict requires re-evaluation at E[L]*' if el['flag_outside_tolerance'] else 'no — within tolerance'}.")
    else:
        lines.append("- E[L]* = NaN (insufficient data)")
    lines.append("")

    # === §4.11 secondary descriptive outcomes ===
    lines.append("## §4.11 secondary descriptive outcomes")
    lines.append("")

    # Same-day Spearman per phase x era + crash-drop sensitivity row
    lines.append("### Same-day Spearman (PRIMARY_COL vs gevoelscore) with "
                 "§3.4 crash-drop sensitivity")
    lines.append("")
    sp = results.get("secondary", {}).get("spearman_primary_vs_gevoelscore", {})
    lines.append("| phase | era | n_full | ρ_full | n_no_crash | ρ_no_crash | |Δρ| |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for phase in PHASE_ORDER:
        for era in ["train", "validate"]:
            rec = sp.get(phase, {}).get(era)
            if not rec:
                continue
            d_rho = rec.get("delta_rho", float("nan"))
            flag = "**FLAG**" if not math.isnan(d_rho) and abs(d_rho) > 0.10 else ""
            def _f(v):
                return "—" if math.isnan(v) else f"{v:+.3f}"
            lines.append(
                f"| {phase} | {era} | {rec['n_full']} | "
                f"{_f(rec['rho_full'])} | {rec['n_no_crash']} | "
                f"{_f(rec['rho_no_crash'])} | "
                f"{('—' if math.isnan(d_rho) else f'{abs(d_rho):.3f}')}"
                f"{(' ' + flag) if flag else ''} |")
    lines.append("")

    # v2-specific Spearman on pooled-unmedicated exertion-conditioned subset
    sub = results.get("secondary", {}).get(
        "spearman_unmed_pooled_exertion_conditioned", {})
    lines.append("### v2 Spearman on pooled-unmedicated heavy-exertion-"
                 "conditioned subset (headline cell's universe)")
    lines.append("")
    if sub:
        rho = sub.get("rho", float("nan"))
        rho_s = "—" if math.isnan(rho) else f"{rho:+.3f}"
        lines.append(f"- n = {sub.get('n', 'NA')}, ρ = {rho_s}")
    lines.append("")

    # Construct disambiguation
    lines.append("### Construct-disambiguation 2×2 (HA-C4b primary vs sibling)")
    lines.append("")
    for sibling_label, rho_text in [
        ("construct_disambig_vs_stress_high_duration_min", "ρ = 0.79"),
        ("construct_disambig_vs_u_dip_count", "ρ = 0.556"),
    ]:
        sb = results.get("secondary", {}).get(sibling_label, {})
        if not sb:
            continue
        title = sibling_label.replace("construct_disambig_vs_", "")
        lines.append(f"**vs `{title}`** ({rho_text}):")
        lines.append("")
        lines.append("| phase | era | both_fire | primary_only (HA-C4b only) | sibling_only | neither | n_eval |")
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

    # Respiration companion
    lines.append("### Respiration-companion sensitivity (§4.11.4)")
    lines.append("")
    lines.append(
        "Among crash episodes where HA-C4b primary fires (one-sided ≥1.5), "
        "did `n_minutes_resp_above_18` also show z > 0 in the lead-up?")
    lines.append("")
    rb = results.get("secondary", {}).get("respiration_companion_sensitivity", {})
    lines.append("| phase | era | primary_fired_resp_elev | primary_fired_resp_normal |")
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

    # === Caveats (§8) ===
    lines.append("## Caveats (v2 §8 acknowledged)")
    lines.append("")
    for c in [
        "**v1 → v2 relock disclosure**. The headline cell was relocked from "
        "`consolidation × both-eras` (v1) to `unmedicated × train+validate "
        "pooled` (v2) after v1's dry-run halt; researcher-degrees-of-freedom "
        "concern from the relock is acknowledged (the corpus's available "
        "cells were known at v2 drafting time, and the pooled-unmedicated "
        "cell was selected partly because it was the only above-bar cell "
        "available). Surfaced in the introduction block above.",
        "**No cross-era independent replication for v2's headline cell**. "
        "v2 pools train (n=8) + validate (n=2) within unmedicated to clear "
        "the n ≥ 10 bar; the HA11-family both-eras-independent rule is "
        "abandoned for this hypothesis. The compensating mechanism is the "
        "descriptive directional-consistency companion on the train-only "
        "(n=8) and validate-only (n=2) subsets reported above. **Not a "
        "full substitute** for independent verdicts.",
        "**Power-calc dispatch**. Power calculation is inapplicable per "
        "Daza 2018 within-subject design — the n-of-1 corpus does not have "
        "separate treatment and control arms in the sense classical power "
        "calculations require. The block-permutation null at E[L]=7 (§4.9) "
        "is the within-subject inferential machinery; the §5.1 (a)+(b)+(c) "
        "gates determine SUPPORTED / NOT-SUPPORTED rather than a power-"
        "thresholded p-value.",
        "**Unmedicated = pre-citalopram corpus, not 'no medication overall'**. "
        "The participant was unmedicated for SSRI in 2022-04 → 2024-04 but "
        "had other lived-experience interventions in that window (CPAP "
        "started 2024-01-10 — the last ~3 months of unmedicated; daily "
        "pacing protocols evolved; PEM-pacing practice was being established). "
        "The unmedicated headline is 'no SSRI' not 'no intervention'. §4.2 "
        "exertion-conditioning and §4.5 phase-stratified baseline absorb "
        "most of this, but it is residual context.",
        "**Garmin stress is partly motion-sensitive**; the motion filter "
        "and respiration-companion sensitivity above are the within-test "
        "checks.",
        "**Garmin `intensity` classification has an 81% gap**; minutes "
        "without an explicit intensity record default to 'low motion' "
        "(generous; per stress_low_motion_primitive §3.3a).",
        "**Citalopram dose-modulates the underlying stress channel** "
        "(per `citalopram_dose_response_stress_mean_sleep.md §5.6` multi-"
        "channel confirmation: 30 mg plasma suppresses raw stress by "
        "~12-17 points). Per-phase treatment is the dose-confound control; "
        "raw count magnitudes not directly comparable across phases. v2's "
        "unmedicated phase headline is the cleanest test ground precisely "
        "because the suppression cascade is absent.",
        "**The `below_moderate` motion class is identical-by-construction "
        "to `low_or_below`** in this corpus; the 9-column ladder effectively "
        "reduces to 6 unique columns.",
        "**Exertion-conditioning shrinks n** sharply; per-phase verdicts "
        "outside unmedicated × pooled may be inconclusive on low-n phases "
        "(reflected in the consolidation / buildup / afbouw companion "
        "table above).",
        "**Construct ρ vs `stress_high_duration_min` = 0.79** — close "
        "sibling; the construct-disambiguation 2×2 above is the empirical "
        "test of whether the motion filter does analytical work.",
        "**The participant is operationally using the rest-stress trigger** "
        "(per `garmin_pacing_practice.md §3.3`); the protocol disturbs the "
        "test. NOT-SUPPORTED reads may indicate a PROTECTIVE-rather-than-"
        "PREDICTIVE trigger; SUPPORTED reads survive despite the disturbance.",
        "**`crash_v2` mixes mechanisms**; multi-mechanism crash population "
        "dilutes any one-mechanism precursor signal.",
        "**Multi-comparison defence**: the §5.0 single-cell discipline + "
        "the stationary-bootstrap null at E[L]=7 are the inferential "
        "machinery; descriptive companions never promote per §5.2.",
        "**The bootstrap RD/OR CIs are computed against the stationary-"
        "bootstrap null distribution** (varying p_null with fixed observed "
        "p_crash); this captures null-side variability only. A fuller "
        "joint-bootstrap CI would require resampling crash episodes as "
        "well; deferred (inherited from v1 §8).",
        "**§4.11.5 LOO boundary-fragility**: an empty load-bearing list is "
        "NOT 'no fragility detected' — it is a boundary-distance signal "
        "indicating k is not exactly at the 60% gate boundary. Restated in "
        "the LOO section above.",
    ]:
        lines.append(f"- {c}")
    lines.append("")

    OUT_RESULT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_RESULT_MD}", file=sys.stderr)


# === Main ===============================================================

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Sample-size + v2 §10.2 spec-sanity-gate per "
                             "§10.4 step 1.")
    parser.add_argument("--use-quartile-cache", action="store_true",
                        help="In dry-run, also apply 1b.ii (slower if "
                             "cache missing).")
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
        write_dry_run_report(dry_summary, dry_summary["verdict"])
        return 1 if dry_summary["verdict"] == "HALT" else 0

    # Full run: gate on dry-run first
    dry_summary = dry_run(slm, master, crash_starts, use_quartile=False)
    write_dry_run_report(dry_summary, dry_summary["verdict"])
    if dry_summary["verdict"] == "HALT":
        print("\n[full] aborting: v2 §10.2 spec-sanity-gate failed",
              file=sys.stderr)
        return 1

    results = run_full(slm, master, crash_starts, dry_summary)
    OUT_DATA_JSON.write_text(json.dumps(results, indent=2, default=str),
                             encoding="utf-8")
    print(f"Wrote {OUT_DATA_JSON}", file=sys.stderr)
    write_result_md(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
