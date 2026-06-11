"""S02 -- Score trajectory: compute trajectories, correlations, triggers.

Implements the pre-registered spec at hypothesis.md (locked + same-day
revised 2026-06-07 before any data inspection).

Outputs:
  - trajectories_score.csv (anchor, n, mean, median, p1..p6)
  - correlation_results.csv (S3.8 Spearman rho with block-bootstrap CI)
  - score-trajectory-with-S01.png (3 panels + zoom strip)
  - score-vs-garmin-normalised.png (S5.2a normalised lead/lag figure)

Trigger evaluation (S7.2 T1/T2/T3/T4) printed to stdout for copy into
notes.md verbatim.
"""
from __future__ import annotations

import csv
import json
import random
import statistics
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

# Reference dates
LC_DIAGNOSIS = date(2022, 5, 6)
GEVOELSCORE_START = date(2022, 9, 3)
ANALYTICAL_SPLIT = date(2023, 12, 31)

# Rolling-window parameters (mirror S01)
WINDOW_DAYS = 90
ANCHOR_STEP_DAYS = 7
TRIMMED_PCT = 0.10
MIN_VALID_IN_WINDOW = 30

# S3.8 correlation parameters
BOOTSTRAP_ITER = 10_000
BLOCK_LEN_DAYS = 90
BOOTSTRAP_SEED = 42

# S7.1 search windows
PEAK_SEARCH_START = date(2022, 12, 2)
PEAK_SEARCH_END = date(2024, 6, 30)
TROUGH_SEARCH_START = date(2024, 7, 1)
TROUGH_GUARD_DAYS = 90

# Paths
HERE = Path(__file__).resolve().parent
UDS_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data"
    r"\DI_CONNECT\DI-Connect-Aggregator"
)
SLEEP_DIR = Path(
    r"C:\Users\Gebruiker\Documents\gevoelscore-data\garmin data"
    r"\DI_CONNECT\DI-Connect-Wellness"
)
SPIKE_CSV = HERE.parent / "H02b-stress-spikes" / "daily_max_spike.csv"
S01_CSV = HERE.parent / "S01-stabilisation-trajectories" / "trajectories.csv"
LABELS_CSV = HERE.parent / "crash_v2-definition" / "labels_crash_v2.csv"
DAY_ENTRIES_CSV = HERE / "day_entries.csv"

OUT_TRAJ_CSV = HERE / "trajectories_score.csv"
OUT_CORR_CSV = HERE / "correlation_results.csv"
OUT_MAIN_PNG = HERE / "score-trajectory-with-S01.png"
OUT_NORM_PNG = HERE / "score-vs-garmin-normalised.png"

INVALID_SLEEP_TYPES = {"UNCONFIRMED", "OFF_WRIST", "NOT_CONFIRMED"}


# ----- Loaders -----

def load_score():
    out = {}
    with DAY_ENTRIES_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[date.fromisoformat(r["date"])] = int(r["score"])
    return out


def load_uds():
    rhr, stress = {}, {}
    for p in sorted(UDS_DIR.glob("UDSFile_*.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            if not cd:
                continue
            d = date.fromisoformat(cd)
            v = rec.get("restingHeartRate")
            if v not in (None, 0):
                if d not in rhr or int(v) > rhr[d]:
                    rhr[d] = int(v)
            ad = rec.get("allDayStress") or {}
            agg = ad.get("aggregatorList") or []
            total = next((a for a in agg if a.get("type") == "TOTAL"), None)
            if total:
                vs = total.get("averageStressLevel")
                if vs not in (None, -1, -2):
                    if d not in stress or int(vs) > stress[d]:
                        stress[d] = int(vs)
    return rhr, stress


def load_sleep_efficiency():
    out = {}
    for p in sorted(SLEEP_DIR.glob("*_sleepData.json")):
        with p.open(encoding="utf-8") as fh:
            data = json.load(fh)
        for rec in data:
            cd = rec.get("calendarDate")
            if not cd:
                continue
            if rec.get("sleepWindowConfirmationType") in INVALID_SLEEP_TYPES:
                continue
            deep = int(rec.get("deepSleepSeconds") or 0)
            light = int(rec.get("lightSleepSeconds") or 0)
            rem = int(rec.get("remSleepSeconds") or 0)
            awake = int(rec.get("awakeSleepSeconds") or 0)
            unmeas = int(rec.get("unmeasurableSeconds") or 0)
            tst = deep + light + rem
            tib = tst + awake + unmeas
            if tib < 4 * 3600:
                continue
            d = date.fromisoformat(cd)
            eff = tst / tib
            if d not in out or tib > out[d][1]:
                out[d] = (eff, tib)
    return {d: e for d, (e, _) in out.items()}


def load_max_spike():
    out = {}
    with SPIKE_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["valid"] != "1":
                continue
            out[date.fromisoformat(r["date"])] = float(r["max_spike_minutes"])
    return out


def load_s01_trajectories():
    out = []
    with S01_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            row = {"anchor_date": date.fromisoformat(r["anchor_date"])}
            for k in ("rhr_90d_trimmed_mean", "avg_stress_90d_trimmed_mean",
                      "sleep_efficiency_90d_trimmed_mean",
                      "max_spike_minutes_90d_trimmed_mean"):
                v = r[k].strip()
                row[k] = float(v) if v else None
            out.append(row)
    return out


def load_labels():
    crash_starts, seen_crash_eps = [], set()
    dip_cluster_days = {}
    singletons = []
    with LABELS_CSV.open(encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["date"])
            label = r["label"]
            ep_id = r["episode_id"]
            cl_id = r["dip_cluster_id"].strip()
            if label == "crash" and ep_id and ep_id not in seen_crash_eps:
                seen_crash_eps.add(ep_id)
                crash_starts.append(date.fromisoformat(r["episode_start"]))
            elif label == "dip":
                if cl_id:
                    dip_cluster_days.setdefault(cl_id, []).append(d)
                else:
                    singletons.append(d)
    cluster_spans = sorted(
        (min(ds), max(ds)) for ds in dip_cluster_days.values()
    )
    return crash_starts, cluster_spans, singletons


# ----- Rolling computations -----

def trimmed_mean(values, pct):
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    trim = int(n * pct)
    if n - 2 * trim < 1:
        return statistics.mean(s)
    return statistics.mean(s[trim:n - trim])


def rolling_score_summary(score_by_date, anchors):
    rows = []
    for a in anchors:
        ws = a - timedelta(days=WINDOW_DAYS)
        vals = [v for d, v in score_by_date.items() if ws <= d < a]
        row = {"anchor_date": a, "n_in_window": len(vals)}
        if len(vals) >= MIN_VALID_IN_WINDOW:
            row["score_trimmed_mean"] = trimmed_mean(vals, TRIMMED_PCT)
            row["score_median"] = statistics.median(vals)
            counts = Counter(vals)
            n = len(vals)
            for s in (1, 2, 3, 4, 5, 6):
                row[f"p{s}"] = counts.get(s, 0) / n
        else:
            row["score_trimmed_mean"] = None
            row["score_median"] = None
            for s in (1, 2, 3, 4, 5, 6):
                row[f"p{s}"] = None
        rows.append(row)
    return rows


# ----- S3.8 Spearman + block bootstrap -----

def rankdata(xs):
    n = len(xs)
    idx = sorted(range(n), key=lambda i: xs[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and xs[idx[j + 1]] == xs[idx[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[idx[k]] = avg
        i = j + 1
    return ranks


def spearman(xs, ys):
    rx = rankdata(xs)
    ry = rankdata(ys)
    n = len(xs)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    dx = sum((rx[i] - mx) ** 2 for i in range(n)) ** 0.5
    dy = sum((ry[i] - my) ** 2 for i in range(n)) ** 0.5
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def block_bootstrap_ci(xs, ys, block_len, n_iter, seed, ci=0.95):
    n = len(xs)
    rng = random.Random(seed)
    n_blocks = -(-n // block_len)
    n_possible_starts = n - block_len + 1
    estimates = []
    for _ in range(n_iter):
        bx, by = [], []
        for _ in range(n_blocks):
            start = rng.randrange(n_possible_starts)
            bx.extend(xs[start:start + block_len])
            by.extend(ys[start:start + block_len])
        bx = bx[:n]
        by = by[:n]
        estimates.append(spearman(bx, by))
    estimates.sort()
    lo = estimates[int((1 - ci) / 2 * n_iter)]
    hi = estimates[int((1 + ci) / 2 * n_iter) - 1]
    return lo, hi


def correlate_pair(score_by_date, metric_by_date, ws, we,
                   block_len, n_iter, seed):
    days = sorted(d for d in score_by_date if ws <= d < we)
    n_excl = 0
    xs, ys = [], []
    for d in days:
        if d not in metric_by_date:
            n_excl += 1
            continue
        xs.append(score_by_date[d])
        ys.append(metric_by_date[d])
    rho = spearman(xs, ys)
    lo, hi = block_bootstrap_ci(xs, ys, block_len, n_iter, seed)
    return len(xs), n_excl, rho, lo, hi


def verdict_row(rho, lo, hi):
    abs_rho = abs(rho)
    excludes_zero = (lo > 0 and hi > 0) or (lo < 0 and hi < 0)
    if abs_rho >= 0.30 and excludes_zero:
        if rho > 0:
            return ("INVERSE-DIRECTION SIGNIFICANT "
                    "(expected negative; surprising; flag for S02b reframe)")
        return "co-vary detectably at daily resolution"
    if abs_rho >= 0.30:
        return "suggestive but underpowered"
    if abs_rho < 0.10 and lo >= -0.15 and hi <= 0.15:
        return "no detectable daily co-variation"
    return "ambiguous; underpowered at this resolution"


# ----- S7.1 extrema -----

def pick_peak(dates, vals, ws, we):
    pairs = [(d, v) for d, v in zip(dates, vals)
             if v is not None and ws <= d <= we]
    if not pairs:
        return None, None
    return max(pairs, key=lambda p: (p[1], -p[0].toordinal()))


def pick_trough(dates, vals, ws, we):
    pairs = [(d, v) for d, v in zip(dates, vals)
             if v is not None and ws <= d <= we]
    if not pairs:
        return None, None
    return min(pairs, key=lambda p: (p[1], p[0].toordinal()))


def std_safe(vals):
    clean = [v for v in vals if v is not None]
    return statistics.stdev(clean) if len(clean) >= 2 else 0.0


def percentile_rank(value, all_values):
    clean = [v for v in all_values if v is not None]
    if not clean:
        return 0.0
    below = sum(1 for v in clean if v < value)
    equal = sum(1 for v in clean if v == value)
    return (below + equal / 2) / len(clean)


def recovery_pctl(value, all_values, higher_is_better):
    pr = percentile_rank(value, all_values)
    return pr if higher_is_better else 1 - pr


def interpolate_at(target_date, dates, values):
    """Linear-interpolate `values` at `target_date` given (dates, values).
    Used to align S01's anchor grid (started 2021-11-14) onto S02's
    anchor grid (started 2022-12-02). The two grids are both 7-day
    cadenced but offset by 5 days mod 7 so they never coincide
    exactly; interpolation distance is therefore at most 3 days, which
    is small versus the 90-day smoothing window and produces no
    material distortion of the trajectory. Required for T3 anchor-by-
    anchor comparison; documented here so any future reader of the
    code understands why this exists rather than a direct anchor join.
    """
    pairs = sorted((d, v) for d, v in zip(dates, values) if v is not None)
    if not pairs:
        return None
    if target_date <= pairs[0][0]:
        return pairs[0][1]
    if target_date >= pairs[-1][0]:
        return pairs[-1][1]
    for i in range(len(pairs) - 1):
        if pairs[i][0] <= target_date <= pairs[i + 1][0]:
            d1, v1 = pairs[i]
            d2, v2 = pairs[i + 1]
            frac = (target_date - d1).days / (d2 - d1).days
            return v1 + frac * (v2 - v1)
    return None


# ----- Main -----

def main():
    print("=" * 64)
    print("S02 -- Score trajectory: execution")
    print("=" * 64)

    print("\n[1] Loading data...")
    score = load_score()
    print(f"  day_entries:  {len(score)} days "
          f"({min(score)} -> {max(score)})")
    rhr, avg_stress = load_uds()
    print(f"  UDS:          {len(rhr)} RHR-days, "
          f"{len(avg_stress)} stress-days")
    sleep_eff = load_sleep_efficiency()
    print(f"  Sleep:        {len(sleep_eff)} nights")
    max_spike = load_max_spike()
    print(f"  Max-spike:    {len(max_spike)} days")
    s01 = load_s01_trajectories()
    print(f"  S01 anchors:  {len(s01)} rows")
    crash_starts, cluster_spans, singletons = load_labels()
    print(f"  crash_v2:     {len(crash_starts)} crash, "
          f"{len(cluster_spans)} dip-clusters, "
          f"{len(singletons)} singleton-dips")

    # Anchors
    score_start = min(score)
    score_end = max(score)
    first_anchor = score_start + timedelta(days=WINDOW_DAYS)
    anchors = []
    a = first_anchor
    while a <= score_end:
        anchors.append(a)
        a += timedelta(days=ANCHOR_STEP_DAYS)
    print(f"\n[2] Score anchors: {len(anchors)} "
          f"({anchors[0]} -> {anchors[-1]})")

    # Rolling summaries
    print("\n[3] Computing rolling score summaries...")
    rows = rolling_score_summary(score, anchors)
    valid_rows = [r for r in rows if r["score_trimmed_mean"] is not None]
    print(f"  valid anchors: {len(valid_rows)}/{len(rows)}")

    with OUT_TRAJ_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["anchor_date", "n_in_window", "score_trimmed_mean",
                    "score_median", "p1", "p2", "p3", "p4", "p5", "p6"])
        for r in rows:
            w.writerow([
                r["anchor_date"].isoformat(),
                r["n_in_window"],
                f"{r['score_trimmed_mean']:.4f}" if r["score_trimmed_mean"] is not None else "",
                f"{r['score_median']:.2f}" if r["score_median"] is not None else "",
                *(f"{r[f'p{s}']:.4f}" if r[f"p{s}"] is not None else ""
                  for s in (1, 2, 3, 4, 5, 6)),
            ])
    print(f"  wrote {OUT_TRAJ_CSV.name}")

    # S3.8 correlations
    print("\n[4] S3.8 same-day rank correlations (block bootstrap, "
          f"{BOOTSTRAP_ITER} iter)...")
    ws = GEVOELSCORE_START
    we = score_end + timedelta(days=1)
    corr_results = []
    for ch, met, role, off in [
        ("avg_stress", avg_stress, "primary", 0),
        ("rhr", rhr, "exploratory", 1),
        ("sleep_efficiency", sleep_eff, "exploratory", 2),
        ("max_spike_minutes", max_spike, "exploratory", 3),
    ]:
        n_pairs, n_excl, rho, lo, hi = correlate_pair(
            score, met, ws, we, BLOCK_LEN_DAYS, BOOTSTRAP_ITER,
            BOOTSTRAP_SEED + off
        )
        n_eff = -(-n_pairs // BLOCK_LEN_DAYS)
        v = verdict_row(rho, lo, hi)
        corr_results.append({
            "channel": ch, "role": role, "n_pairs": n_pairs,
            "n_excluded": n_excl, "n_effective_blocks": n_eff,
            "spearman_rho": rho, "ci95_lo": lo, "ci95_hi": hi,
            "verdict_row": v,
        })
        print(f"  {ch:>20s} ({role:>11s}): n={n_pairs:4d} "
              f"rho={rho:+.4f} 95%CI [{lo:+.4f},{hi:+.4f}] "
              f"blocks={n_eff}")
        print(f"    verdict: {v}")

    with OUT_CORR_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["channel", "role", "n_pairs", "n_excluded",
                    "n_effective_blocks", "spearman_rho", "ci95_lo",
                    "ci95_hi", "verdict_row"])
        for r in corr_results:
            w.writerow([
                r["channel"], r["role"], r["n_pairs"], r["n_excluded"],
                r["n_effective_blocks"],
                f"{r['spearman_rho']:.4f}",
                f"{r['ci95_lo']:.4f}", f"{r['ci95_hi']:.4f}",
                r["verdict_row"],
            ])
    print(f"  wrote {OUT_CORR_CSV.name}")

    # S7.1 extrema
    print("\n[5] S7.1 algorithmic peaks/troughs...")
    score_dates = [r["anchor_date"] for r in rows]
    score_mean_vals = [r["score_trimmed_mean"] for r in rows]
    score_peak_d, score_peak_v = pick_peak(
        score_dates, score_mean_vals, PEAK_SEARCH_START, PEAK_SEARCH_END
    )
    last_anchor = anchors[-1]
    score_trough_end = last_anchor - timedelta(days=TROUGH_GUARD_DAYS)
    score_trough_d, score_trough_v = pick_trough(
        score_dates, score_mean_vals, TROUGH_SEARCH_START, score_trough_end
    )
    print(f"  score: peak={score_peak_d} ({score_peak_v:.4f}), "
          f"trough={score_trough_d} ({score_trough_v:.4f})")

    s01_dates = [r["anchor_date"] for r in s01]
    metric_keys = [
        "avg_stress_90d_trimmed_mean",
        "max_spike_minutes_90d_trimmed_mean",
        "rhr_90d_trimmed_mean",
        "sleep_efficiency_90d_trimmed_mean",
    ]
    s01_extrema = {}
    for k in metric_keys:
        vals = [r[k] for r in s01]
        peak_d, peak_v = pick_peak(s01_dates, vals,
                                   PEAK_SEARCH_START, PEAK_SEARCH_END)
        trough_d, trough_v = pick_trough(
            s01_dates, vals, TROUGH_SEARCH_START,
            s01_dates[-1] - timedelta(days=TROUGH_GUARD_DAYS),
        )
        last_v = next((r[k] for r in reversed(s01)
                       if r[k] is not None), None)
        all_vals = [r[k] for r in s01 if r[k] is not None]
        sd = std_safe(all_vals)
        s01_extrema[k] = {
            "peak_d": peak_d, "peak_v": peak_v,
            "trough_d": trough_d, "trough_v": trough_v,
            "last_v": last_v, "std": sd, "all_vals": all_vals,
        }
        short = k.replace("_90d_trimmed_mean", "")
        print(f"  {short:>20s}: peak={peak_d} ({peak_v:.4f}), "
              f"trough={trough_d} ({trough_v:.4f}), "
              f"last={last_v:.4f}, sigma={sd:.4f}")

    score_all = [v for v in score_mean_vals if v is not None]
    score_std = std_safe(score_all)
    score_last_v = score_all[-1]
    print(f"  {'score':>20s}: last={score_last_v:.4f}, "
          f"sigma={score_std:.4f}")

    # S7.2 triggers
    print("\n[6] S7.2 trigger evaluation")

    # T1
    print("\n  T1 -- inflection-date mismatch (>= 91 days)")
    t1_fired = False
    t1_details = []
    for k, label in [
        ("avg_stress_90d_trimmed_mean", "avg stress"),
        ("max_spike_minutes_90d_trimmed_mean", "max spike"),
    ]:
        e = s01_extrema[k]
        pd = abs((score_peak_d - e["peak_d"]).days)
        td = abs((score_trough_d - e["trough_d"]).days)
        pf, tf = pd >= 91, td >= 91
        t1_details.append((label, pd, pf, td, tf,
                           e["peak_d"], e["trough_d"]))
        print(f"    vs {label}: peak D={pd}d ({'FIRES' if pf else 'no'}), "
              f"trough D={td}d ({'FIRES' if tf else 'no'})")
        if pf or tf:
            t1_fired = True
    print(f"  T1: {'FIRED' if t1_fired else 'not fired'}")

    # T2
    print("\n  T2 -- May 2026 channel divergence")
    metric_worsen = {
        "avg_stress_90d_trimmed_mean": "higher",
        "max_spike_minutes_90d_trimmed_mean": "higher",
        "rhr_90d_trimmed_mean": "higher",
        "sleep_efficiency_90d_trimmed_mean": "lower",
    }
    s01_vis_count = 0
    s01_vis_details = []
    for k, dirn in metric_worsen.items():
        e = s01_extrema[k]
        if dirn == "higher":
            thr = e["trough_v"] + e["std"]
            vis = e["last_v"] >= thr
            delta = e["last_v"] - e["trough_v"]
        else:
            thr = e["trough_v"] - e["std"]
            vis = e["last_v"] <= thr
            delta = e["trough_v"] - e["last_v"]
        s01_vis_details.append((k.replace("_90d_trimmed_mean", ""),
                                delta, e["std"], vis))
        short = k.replace("_90d_trimmed_mean", "")
        print(f"    {short:>20s}: last-trough={delta:+.4f}, "
              f"sigma={e['std']:.4f}, visible={vis}")
        if vis:
            s01_vis_count += 1

    score_trough_threshold = score_trough_v - score_std
    score_vis = score_last_v <= score_trough_threshold
    score_delta = score_trough_v - score_last_v
    print(f"    {'score':>20s}: trough-last={score_delta:+.4f}, "
          f"sigma={score_std:.4f}, visible={score_vis}")

    zoom_start = date(2025, 12, 1)
    zoom_days = [(d, score[d]) for d in sorted(score) if d >= zoom_start]
    if len(zoom_days) >= 120:
        recent_30 = [v for _, v in zoom_days[-30:]]
        ref_30 = [v for _, v in zoom_days[-120:-90]]
        zoom_recent_mean = statistics.mean(recent_30)
        zoom_ref_mean = statistics.mean(ref_30)
        zoom_delta = zoom_ref_mean - zoom_recent_mean
        zoom_vis = zoom_delta >= 0.5
        print(f"    {'zoom strip':>20s}: ref30={zoom_ref_mean:.4f}, "
              f"recent30={zoom_recent_mean:.4f}, "
              f"delta={zoom_delta:+.4f}, visible={zoom_vis}")
    else:
        zoom_vis = False
        zoom_recent_mean = zoom_ref_mean = zoom_delta = None
        print(f"    zoom strip: insufficient days "
              f"({len(zoom_days)} < 120); visible=False")

    t2_forward = (s01_vis_count >= 2) and (not score_vis) and (not zoom_vis)
    t2_reverse = (score_vis or zoom_vis) and (s01_vis_count <= 1)
    t2_fired = t2_forward or t2_reverse
    print(f"  T2: S01 visible {s01_vis_count}/4, "
          f"score_vis={score_vis}, zoom_vis={zoom_vis}")
    print(f"  T2: {'FIRED' if t2_fired else 'not fired'} "
          f"({'forward' if t2_forward else ('reverse' if t2_reverse else '-')})")

    # T3
    print("\n  T3 -- score lags Garmin throughout post-stabilisation")
    lag_window_end = last_anchor - timedelta(days=TROUGH_GUARD_DAYS)
    lag_anchors = [d for d in score_dates
                   if score_trough_d <= d <= lag_window_end]
    print(f"  lag window: [{score_trough_d}, {lag_window_end}], "
          f"{len(lag_anchors)} anchors")
    score_pctls = {
        d: recovery_pctl(v, score_all, True)
        for d, v in zip(score_dates, score_mean_vals) if v is not None
    }
    t3_fired = False
    t3_details = []
    for k, label, higher_better in [
        ("avg_stress_90d_trimmed_mean", "avg stress", False),
        ("max_spike_minutes_90d_trimmed_mean", "max spike", False),
    ]:
        e = s01_extrema[k]
        s01_vals_k = [r[k] for r in s01]
        # Interpolate S01 onto score's anchor grid (see interpolate_at
        # docstring for why)
        gaps = []
        for d in lag_anchors:
            if d not in score_pctls:
                continue
            m_val_at_d = interpolate_at(d, s01_dates, s01_vals_k)
            if m_val_at_d is None:
                continue
            m_pctl = recovery_pctl(m_val_at_d, e["all_vals"], higher_better)
            gaps.append(m_pctl - score_pctls[d])
        if not gaps:
            t3_details.append((label, 0, 0, 0.0, False))
            print(f"    vs {label}: no overlapping anchors")
            continue
        share = sum(1 for g in gaps if g >= 0.20) / len(gaps)
        mean_gap = statistics.mean(gaps)
        fires = share >= 0.80
        t3_details.append((label, len(gaps), share, mean_gap, fires))
        print(f"    vs {label}: gap>=0.20 in {share:.1%} "
              f"({sum(1 for g in gaps if g >= 0.20)}/{len(gaps)}), "
              f"mean_gap={mean_gap:+.4f}, fires={fires}")
        if fires:
            t3_fired = True
    print(f"  T3: {'FIRED' if t3_fired else 'not fired'}")

    # T4
    print("\n  T4 -- sustained mean-median divergence")
    divs = []
    for r in rows:
        if r["score_trimmed_mean"] is None or r["score_median"] is None:
            divs.append(None)
        else:
            divs.append(abs(r["score_trimmed_mean"] - r["score_median"]))
    max_run = 0
    cur = 0
    max_start = None
    cur_start = None
    for i, d in enumerate(divs):
        if d is not None and d >= 1.0:
            if cur == 0:
                cur_start = i
            cur += 1
            if cur > max_run:
                max_run = cur
                max_start = cur_start
        else:
            cur = 0
    max_div = max((d for d in divs if d is not None), default=0.0)
    print(f"  max consecutive anchors with |mean-median|>=1.0: {max_run}")
    print(f"  max divergence anywhere: {max_div:.4f}")
    t4_fired = max_run >= 5
    if max_run >= 5:
        s_d = rows[max_start]["anchor_date"]
        e_d = rows[max_start + max_run - 1]["anchor_date"]
        print(f"  longest run: {s_d} -> {e_d}")
    print(f"  T4: {'FIRED' if t4_fired else 'not fired'}")

    print("\n" + "=" * 64)
    print("TRIGGER SUMMARY")
    print("=" * 64)
    for name, f in [("T1", t1_fired), ("T2", t2_fired),
                    ("T3", t3_fired), ("T4", t4_fired)]:
        print(f"  {name}: {'FIRED' if f else 'not fired'}")
    s02b = any([t1_fired, t2_fired, t3_fired, t4_fired])
    print(f"\n  S02b triggered: {'YES' if s02b else 'no'}")

    # Plots
    print("\n[7] Rendering plots...")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from matplotlib.patches import Rectangle
        from matplotlib.lines import Line2D
    except ImportError:
        print("  matplotlib not installed, skipping plots")
        return 0

    # Main figure
    fig = plt.figure(figsize=(14, 14))
    gs = fig.add_gridspec(4, 1, height_ratios=[2.2, 1.6, 1.6, 0.9],
                          hspace=0.40)

    # Panel 1
    ax0 = fig.add_subplot(gs[0])
    for k, label, color in [
        ("rhr_90d_trimmed_mean", "RHR (bpm)", "#c0392b"),
        ("avg_stress_90d_trimmed_mean", "avg stress (0-100)", "#d68910"),
        ("max_spike_minutes_90d_trimmed_mean", "max spike (min)", "#8e44ad"),
    ]:
        xs = [r["anchor_date"] for r in s01 if r[k] is not None]
        ys = [r[k] for r in s01 if r[k] is not None]
        ax0.plot(xs, ys, color=color, linewidth=1.4, label=label)
    ax0.set_ylabel("RHR / stress / spike")
    ax0.set_title("Panel 1 -- S01 Garmin pendulum (re-rendered)")
    ax0.legend(loc="upper left", fontsize=8)
    ax0.grid(alpha=0.25)
    ax0b = ax0.twinx()
    xs = [r["anchor_date"] for r in s01
          if r["sleep_efficiency_90d_trimmed_mean"] is not None]
    ys = [r["sleep_efficiency_90d_trimmed_mean"] for r in s01
          if r["sleep_efficiency_90d_trimmed_mean"] is not None]
    ax0b.plot(xs, ys, color="#16a085", linewidth=1.0,
              linestyle="--", alpha=0.6, label="sleep efficiency")
    ax0b.set_ylabel("sleep efficiency", color="#16a085")
    ax0b.tick_params(axis="y", labelcolor="#16a085")
    ax0b.legend(loc="upper right", fontsize=8)

    # Panel 2
    ax1 = fig.add_subplot(gs[1], sharex=ax0)
    xs = [r["anchor_date"] for r in rows
          if r["score_trimmed_mean"] is not None]
    ys_m = [r["score_trimmed_mean"] for r in rows
            if r["score_trimmed_mean"] is not None]
    ys_d = [r["score_median"] for r in rows
            if r["score_median"] is not None]
    ax1.plot(xs, ys_m, color="#2c3e50", linewidth=1.6,
             label="trimmed mean (10/10)")
    ax1.plot(xs, ys_d, color="#7f8c8d", linewidth=1.2,
             drawstyle="steps-post", label="median (step)")
    ax1.axvline(score_peak_d, color="#27ae60",
                linestyle=":", alpha=0.5)
    ax1.axvline(score_trough_d, color="#c0392b",
                linestyle=":", alpha=0.5)
    ax1.set_ylim(1, 6)
    ax1.set_ylabel("gevoelscore (1-6)")
    ax1.set_title("Panel 2 -- score trimmed mean + median (peak/trough vertical lines)")
    ax1.legend(loc="lower right", fontsize=8)
    ax1.grid(alpha=0.25)

    # Panel 3
    ax2 = fig.add_subplot(gs[2], sharex=ax0)
    vi = [i for i, r in enumerate(rows) if r["p1"] is not None]
    xs_d = [rows[i]["anchor_date"] for i in vi]
    layers = [[rows[i][f"p{s}"] for i in vi] for s in (1, 2, 3, 4, 5, 6)]
    colours = ["#2c1810", "#5b3826", "#8c5a3c",
               "#bd8160", "#e1ab87", "#f5d4b7"]
    ax2.stackplot(xs_d, *layers, colors=colours,
                  labels=[f"score={s}" for s in (1, 2, 3, 4, 5, 6)])
    ax2.set_ylim(0, 1)
    ax2.set_ylabel("share of in-window days")
    ax2.set_title("Panel 3 -- score-level distribution "
                  "(dark = score 1, light = score 6)")
    ax2.legend(loc="upper left", fontsize=7, ncol=6, framealpha=0.9)
    ax2.grid(alpha=0.25)

    # Event overlay on panel 3 bottom margin
    for d in crash_starts:
        ax2.plot(d, 0.02, marker="^", color="black",
                 markersize=6, alpha=1.0)
    for s_d, e_d in cluster_spans:
        ax2.add_patch(Rectangle(
            (mdates.date2num(s_d), 0.0),
            mdates.date2num(e_d) - mdates.date2num(s_d) + 1, 0.04,
            color="#3498db", alpha=0.40, zorder=2,
        ))
    for d in singletons:
        ax2.plot([d, d], [0.0, 0.025], color="#7f8c8d",
                 linewidth=0.5, alpha=0.20)

    # Zoom strip
    ax3 = fig.add_subplot(gs[3])
    zoom_dates = [d for d, _ in zoom_days]
    zoom_scores = [s for _, s in zoom_days]
    rng_j = random.Random(42)
    j = [rng_j.uniform(-0.15, 0.15) for _ in zoom_scores]
    zsj = [s + jj for s, jj in zip(zoom_scores, j)]
    ax3.scatter(zoom_dates, zsj, s=8, alpha=0.5, color="#2c3e50")
    if zoom_dates:
        roll_d, roll_m = [], []
        for i in range(29, len(zoom_dates)):
            roll_m.append(statistics.mean(zoom_scores[i - 29:i + 1]))
            roll_d.append(zoom_dates[i])
        ax3.plot(roll_d, roll_m, color="#c0392b", linewidth=1.6,
                 label="30d rolling mean")
        ax3.legend(loc="lower left", fontsize=7)
    ax3.set_ylim(0.5, 6.5)
    ax3.set_ylabel("score")
    ax3.set_title("Zoom strip -- last ~6 months "
                  "(raw + 30d roll, ±0.15 jitter; PRELIMINARY)",
                  fontsize=9)
    ax3.grid(alpha=0.25)
    ax3.set_facecolor("#fcfcfc")
    ax3.xaxis.set_major_locator(mdates.MonthLocator())
    ax3.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

    # Reference lines on main panels
    for ax in (ax0, ax1, ax2):
        ax.axvline(LC_DIAGNOSIS, color="gray",
                   linestyle=":", alpha=0.7)
        ax.axvline(GEVOELSCORE_START, color="gray",
                   linestyle="--", alpha=0.5)
        ax.axvline(ANALYTICAL_SPLIT, color="gray",
                   linestyle=":", alpha=0.4)

    # "No score data" band on score panels
    for ax in (ax1, ax2):
        ax.axvspan(s01_dates[0], GEVOELSCORE_START,
                   color="#ecf0f1", alpha=0.6, zorder=0)

    ax2.set_xlim(s01_dates[0], anchors[-1])
    for ax in (ax0, ax1, ax2):
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    handles = [
        Line2D([0], [0], color="gray", linestyle=":",
               label="LC dx 2022-05-06"),
        Line2D([0], [0], color="gray", linestyle="--",
               label="gevoelscore start 2022-09-03"),
        Line2D([0], [0], color="gray", linestyle=":", alpha=0.5,
               label="analytical split 2023-12-31 (NOT physiological)"),
    ]
    fig.legend(handles=handles, loc="upper center", ncol=3,
               frameon=False, fontsize=8)
    fig.suptitle("S02 -- score trajectory with S01 overlay",
                 fontsize=13, y=0.995)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(OUT_MAIN_PNG, dpi=110)
    plt.close(fig)
    print(f"  wrote {OUT_MAIN_PNG.name}")

    # Normalised companion
    fig, ax = plt.subplots(figsize=(14, 5))

    def normalise(values, higher_better):
        clean = [v for v in values if v is not None]
        if not clean:
            return values
        lo, hi = min(clean), max(clean)
        if hi == lo:
            return [0.5 if v is not None else None for v in values]
        nv = [(v - lo) / (hi - lo) if v is not None else None
              for v in values]
        if not higher_better:
            nv = [1 - v if v is not None else None for v in nv]
        return nv

    curves = [
        ("score trimmed mean",
         [r["score_trimmed_mean"] for r in rows],
         [r["anchor_date"] for r in rows], True, "#2c3e50"),
        ("score median",
         [r["score_median"] for r in rows],
         [r["anchor_date"] for r in rows], True, "#7f8c8d"),
        ("avg stress",
         [r["avg_stress_90d_trimmed_mean"] for r in s01],
         s01_dates, False, "#d68910"),
        ("max spike",
         [r["max_spike_minutes_90d_trimmed_mean"] for r in s01],
         s01_dates, False, "#8e44ad"),
        ("RHR",
         [r["rhr_90d_trimmed_mean"] for r in s01],
         s01_dates, False, "#c0392b"),
        ("sleep efficiency",
         [r["sleep_efficiency_90d_trimmed_mean"] for r in s01],
         s01_dates, True, "#16a085"),
    ]
    for label, vals, dates, hb, color in curves:
        nv = normalise(vals, hb)
        xs = [d for d, v in zip(dates, nv) if v is not None]
        ys = [v for v in nv if v is not None]
        ax.plot(xs, ys, color=color, linewidth=1.4, label=label)
    ax.set_ylabel("recovery direction (0=worst-in-own-range, "
                  "1=best-in-own-range)")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("S02 normalised -- score vs Garmin (all curves: up = improvement)")
    ax.legend(loc="lower right", fontsize=8, ncol=2)
    ax.grid(alpha=0.25)
    ax.axvline(LC_DIAGNOSIS, color="gray", linestyle=":", alpha=0.7)
    ax.axvline(GEVOELSCORE_START, color="gray", linestyle="--", alpha=0.5)
    ax.axvline(ANALYTICAL_SPLIT, color="gray", linestyle=":", alpha=0.4)
    ax.axvspan(s01_dates[0], GEVOELSCORE_START,
               color="#ecf0f1", alpha=0.6, zorder=0)
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.tight_layout()
    fig.savefig(OUT_NORM_PNG, dpi=110)
    plt.close(fig)
    print(f"  wrote {OUT_NORM_PNG.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
